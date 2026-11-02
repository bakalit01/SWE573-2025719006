"""Members' stories on crafts."""

import pytest
from django.core import mail
from django.urls import reverse

from accounts.models import User
from crafts.models import Craft, CraftStory

from .factories import CommunityFactory, CraftFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def craft():
    community = CommunityFactory()
    owner = UserFactory(email="owner@example.com")
    return CraftFactory(title="Coiled basket", community=community, created_by=owner)


def add(client, craft, text="My grandmother made these.", connection="family"):
    return client.post(
        reverse("crafts:add_story", args=[craft.slug]), {"connection": connection, "text": text}
    )


def test_members_can_share_stories(client, craft):
    member = UserFactory(role=User.Role.MEMBER, display_name="Ayşe")
    client.force_login(member)
    response = add(client, craft)
    story = CraftStory.objects.get()
    assert response.url.endswith(f"#story-{story.pk}")
    assert story.author == member and story.connection == "family"
    html = client.get(craft.get_absolute_url()).content.decode()
    assert "My grandmother made these." in html and "Share your story" in html
    assert mail.outbox[0].to == ["owner@example.com"]
    client.logout()
    html = client.get(craft.get_absolute_url()).content.decode()
    assert "My grandmother made these." in html and "Ayşe" in html
    assert "Log in</a> or" in html and "Share your story" not in html


def test_visitors_cannot_post(client, craft):
    response = add(client, craft)
    assert response.status_code == 302 and "/accounts/login/" in response.url
    assert not CraftStory.objects.exists()


def test_not_on_crafts_you_cannot_see(client, craft):
    craft.visibility = Craft.Visibility.RESTRICTED
    craft.save()
    client.force_login(UserFactory(role=User.Role.MEMBER))
    assert add(client, craft).status_code == 404


def test_story_needs_text_and_connection(client, craft):
    client.force_login(UserFactory())
    add(client, craft, text=" ", connection="")
    assert not CraftStory.objects.exists()


def test_authors_edit_and_delete_only_their_own(client, craft):
    mine = CraftStory.objects.create(
        craft=craft, author=UserFactory(), connection="saw", text="Old"
    )
    other = UserFactory()
    client.force_login(other)
    assert client.get(reverse("crafts:edit_story", args=[mine.pk])).status_code == 404
    assert client.post(reverse("crafts:delete_story", args=[mine.pk])).status_code == 404
    client.force_login(mine.author)
    client.post(reverse("crafts:edit_story", args=[mine.pk]), {"connection": "own", "text": "New"})
    mine.refresh_from_db()
    assert mine.text == "New" and mine.connection == "own"
    client.post(reverse("crafts:delete_story", args=[mine.pk]))
    assert not CraftStory.objects.exists()


def test_stewards_hide_and_show_stories(client, craft):
    story = CraftStory.objects.create(
        craft=craft, author=UserFactory(), connection="other", text="Private family detail"
    )
    url = reverse("crafts:moderate_story", args=[story.pk])
    outsider = UserFactory(role=User.Role.STEWARD)
    CommunityFactory().stewards.add(outsider)
    client.force_login(outsider)
    assert client.post(url, {"action": "hide"}).status_code == 404
    steward = UserFactory(role=User.Role.STEWARD)
    craft.community.stewards.add(steward)
    client.force_login(steward)
    client.post(url, {"action": "hide", "reason": "Asked by the family"})
    story.refresh_from_db()
    assert story.is_hidden and story.hidden_by == steward
    assert "Private family detail" in client.get(reverse("crafts:review_queue")).content.decode()
    client.logout()
    assert "Private family detail" not in client.get(craft.get_absolute_url()).content.decode()
    client.force_login(story.author)
    html = client.get(craft.get_absolute_url()).content.decode()
    assert "Private family detail" in html and "Asked by the family" in html
    client.force_login(steward)
    client.post(url, {"action": "show"})
    story.refresh_from_db()
    assert not story.is_hidden
