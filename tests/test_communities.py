"""US-17 community pages."""

import pytest
from django.urls import reverse

from accounts.models import User
from crafts.models import Craft

from .factories import CommunityFactory, CraftFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def community():
    return CommunityFactory(name="Diné", other_names="Navajo, Navaho", region="Southwest")


def test_page_shows_own_name_first_and_crafts(client, community):
    CraftFactory(title="Rug", community=community)
    CraftFactory(title="Members rug", community=community, visibility=Craft.Visibility.MEMBERS)
    html = client.get(community.get_absolute_url()).content.decode()
    assert html.index("<h1>Diné</h1>") < html.index("Also known as Navajo, Navaho")
    assert "Rug" in html and "Members rug" not in html
    assert "Edit page" not in html


def test_craft_pages_link_to_the_community_page(client, community):
    craft = CraftFactory(community=community)
    assert community.get_absolute_url() in client.get(craft.get_absolute_url()).content.decode()


def test_stewards_edit_the_description(client, community):
    steward = UserFactory(role=User.Role.STEWARD)
    community.stewards.add(steward)
    url = reverse("communities:edit", args=[community.slug])
    client.force_login(steward)
    assert "Edit page" in client.get(community.get_absolute_url()).content.decode()
    client.post(
        url, {"other_names": "Navajo", "region": "Navajo Nation", "description": "Our words."}
    )
    community.refresh_from_db()
    assert community.description == "Our words." and community.name == "Diné"


@pytest.mark.parametrize("role", [User.Role.MAKER, User.Role.STEWARD])
def test_others_cannot_edit(client, community, role):
    client.force_login(UserFactory(role=role))  # a steward, but of no community here
    url = reverse("communities:edit", args=[community.slug])
    assert client.get(url).status_code == 404
    assert client.post(url, {"description": "x"}).status_code == 404


def test_admins_can_edit(client, community):
    client.force_login(UserFactory(role=User.Role.ADMIN))
    assert client.get(reverse("communities:edit", args=[community.slug])).status_code == 200


def test_non_ascii_community_names_have_pages(client):
    community = CommunityFactory(name="Yörük", slug="yörük")
    craft = CraftFactory(community=community)
    assert client.get(craft.get_absolute_url()).status_code == 200
    assert client.get(community.get_absolute_url()).status_code == 200
