"""Real-world reference crafts compiled from public sources."""

import pytest
from django.core.management import call_command

from communities.models import Community
from crafts import reference_data
from crafts.models import Craft, Media, commons_image_url

from .factories import CraftFactory

pytestmark = pytest.mark.django_db


def test_seed_creates_published_public_reference_crafts():
    call_command("seed_reference_crafts")
    crafts = Craft.objects.filter(is_reference=True)
    assert crafts.count() == len(reference_data.CRAFTS) >= 5
    for craft in crafts:
        assert craft.status == Craft.Status.PUBLISHED
        assert craft.visibility == Craft.Visibility.PUBLIC
        assert not craft.is_sample
        assert craft.maker_credit
        assert craft.source_links(), craft.slug
        assert all(url.startswith("https://") for _, url in craft.source_links())
        assert craft.media.exists(), craft.slug
        assert craft.craft_materials.exists() and craft.craft_techniques.exists()
    assert not Media.objects.filter(craft__is_reference=True, alt_text="").exists()
    assert not Media.objects.filter(craft__is_reference=True, commons_file="").exists()


def test_seed_is_idempotent():
    call_command("seed_reference_crafts")
    counts = (Craft.objects.count(), Media.objects.count(), Community.objects.count())
    call_command("seed_reference_crafts")
    assert (Craft.objects.count(), Media.objects.count(), Community.objects.count()) == counts


def test_replace_samples_keeps_user_records():
    call_command("seed_sample_data")
    sample_community = Community.objects.filter(is_sample=True).first()
    users_craft = CraftFactory(title="Added by a user", community=sample_community)
    call_command("seed_reference_crafts", replace_samples=True)
    assert not Craft.objects.filter(is_sample=True).exists()
    assert Craft.objects.filter(pk=users_craft.pk).exists()
    assert Community.objects.filter(pk=sample_community.pk).exists()  # still in use
    assert Community.objects.filter(is_sample=True).count() == 1


def test_commons_urls_are_encoded():
    assert commons_image_url("Kuksa, Inari åå.jpg", width=640) == (
        "https://commons.wikimedia.org/wiki/Special:FilePath/"
        "Kuksa%2C_Inari_%C3%A5%C3%A5.jpg?width=640"
    )


def test_craft_page_shows_sources_credits_and_badge(client):
    call_command("seed_reference_crafts")
    html = client.get("/crafts/pomo-coiled-dowry-basket-jenny-hughes/").content.decode()
    assert "Real example · from public sources" in html
    assert "Jenny Hughes (Pomo)" in html
    assert "https://en.wikipedia.org/wiki/Pomo" in html
    assert "https://commons.wikimedia.org/wiki/Special:FilePath/" in html
    assert 'data-commons-credit="WLA brooklynmuseum Jenny Hughes' in html
    assert "file page and license" in html


def test_public_domain_credit_is_static(client):
    call_command("seed_reference_crafts")
    html = client.get("/crafts/dine-navajo-rug-on-an-upright-loom/").content.decode()
    assert "U.S. National Archives (NARA), 1933 · Public domain" in html
    assert "data-commons-credit" not in html  # no lookup needed for known public domain


def test_catalogue_card_badge(client):
    call_command("seed_reference_crafts")
    html = client.get("/crafts/").content.decode()
    assert html.count("Real example") == len(reference_data.CRAFTS)
