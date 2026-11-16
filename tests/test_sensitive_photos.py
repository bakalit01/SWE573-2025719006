"""US-21: culturally sensitive photos are blurred behind a notice until the viewer chooses."""

import pytest
from django.urls import reverse

from crafts.models import DEFAULT_SENSITIVE_NOTICE, Craft, Media

from .factories import CraftFactory
from .test_contribute import payload, photo

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def craft():
    craft = CraftFactory(title="Ceremonial mask")
    Media.objects.create(
        craft=craft,
        static_path="img/samples/carving-carved-cedar-bowl.svg",
        alt_text="A mask with red and black paint",
        is_sensitive=True,
    )
    return craft


def test_upload_marked_sensitive_is_blurred_with_the_standard_notice(member_client, setup):
    data = payload(
        setup,
        **{"img-0-image": photo(), "img-0-alt_text": "A carved mask", "img-0-is_sensitive": "on"},
    )
    member_client.post(reverse("crafts:create"), data)
    craft = Craft.objects.get(title="Carved pipe")
    assert craft.media.get().is_sensitive
    html = member_client.get(craft.get_absolute_url()).content.decode()
    assert 'class="gallery-main is-sensitive"' in html
    assert DEFAULT_SENSITIVE_NOTICE in html
    assert "Show photo</button>" in html
    assert 'alt="" data-alt="A carved mask"' in html  # alt text is read only after "Show photo"


def test_record_has_its_own_notice(client, craft):
    craft.sensitive_notice = "Shown with the family's permission. Please do not copy."
    craft.save()
    html = client.get(craft.get_absolute_url()).content.decode()
    assert "Shown with the family&#x27;s permission. Please do not copy." in html
    assert DEFAULT_SENSITIVE_NOTICE not in html


def test_notice_is_set_in_the_form(member_client, setup):
    data = payload(setup, sensitive_notice="  Please view with respect.  ")
    member_client.post(reverse("crafts:create"), data)
    assert Craft.objects.get().photo_notice == "Please view with respect."


def test_other_photos_are_not_blurred(client):
    craft = CraftFactory()
    Media.objects.create(craft=craft, static_path="img/x.svg", alt_text="A bowl")
    html = client.get(craft.get_absolute_url()).content.decode()
    assert 'class="gallery-main"' in html and 'alt="A bowl"' in html
    assert "data-sensitive-cover hidden" in html


def test_thumbnails_and_credits_do_not_describe_the_sensitive_photo(client, craft):
    Media.objects.create(craft=craft, static_path="img/y.svg", alt_text="The back", order=5)
    html = client.get(craft.get_absolute_url()).content.decode()
    assert 'alt="Show photo 1 (culturally sensitive)"' in html
    assert 'data-sensitive="true"' in html and 'class="thumb-sensitive"' in html
    assert "<li>Culturally sensitive photo:" in html  # credits list
    assert 'alt="Show photo 2: The back"' in html


def test_cards_show_a_blurred_cover(client, craft):
    html = client.get(reverse("crafts:list")).content.decode()
    card = html.split("Ceremonial mask")[0].rsplit('<li class="card">', 1)[1]
    assert 'class="card-img card-img-sensitive"' in card and 'alt=""' in card
    assert "Sensitive photo" in card
    assert "A mask with red and black paint" not in html


def test_editor_marks_and_unmarks_an_existing_photo(member_client, setup):
    member_client.post(reverse("crafts:create"), payload(setup))
    craft = Craft.objects.get()
    media = Media.objects.create(craft=craft, static_path="img/z.svg", alt_text="A pipe")
    edit = reverse("crafts:edit", args=[craft.slug])
    alt = f"media-{media.pk}-alt_text"
    member_client.post(edit, payload(setup, **{alt: "A pipe", f"media-{media.pk}-sensitive": "1"}))
    media.refresh_from_db()
    assert media.is_sensitive
    form = member_client.get(edit).content.decode()
    assert f'name="media-{media.pk}-sensitive" value="1" checked' in form
    member_client.post(edit, payload(setup, **{alt: "A pipe"}))
    media.refresh_from_db()
    assert not media.is_sensitive
