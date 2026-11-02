"""US-15 search and US-16 filters and sorting."""

import pytest
from django.urls import reverse

from crafts.models import Craft, CraftMaterial, CraftTechnique, Material, Technique

from .factories import CommunityFactory, CraftFactory, CraftTypeFactory

pytestmark = pytest.mark.django_db


def titles(client, **params):
    response = client.get(reverse("crafts:list"), params)
    return [c.title for c in response.context["crafts"]]


@pytest.fixture
def catalogue():
    pomo = CommunityFactory(name="Pomo", other_names="Pomoan")
    basketry = CraftTypeFactory(name="Basketry", slug="basketry")
    basket = CraftFactory(
        title="Coiled dowry basket",
        community=pomo,
        craft_type=basketry,
        description="Fine coiled work with feathers.",
        country="United States",
        year_made=1900,
    )
    rug = CraftFactory(
        title="Yörük kilim", summary="A flat-woven rug.", country="Türkiye", year_made=1950
    )
    pot = CraftFactory(title="Water pot", process="Built in coils and fired.", country="Peru")
    CraftMaterial.objects.create(craft=basket, material=Material.objects.create(name="Sedge root"))
    CraftMaterial.objects.create(craft=rug, material=Material.objects.create(name="Wool"))
    CraftTechnique.objects.create(
        craft=rug, technique=Technique.objects.create(name="Slit tapestry")
    )
    CraftFactory(title="Hidden basket", visibility=Craft.Visibility.RESTRICTED, community=pomo)
    return {"basket": basket, "rug": rug, "pot": pot}


class TestSearch:
    @pytest.mark.parametrize(
        "query, expected",
        [
            ("basket", ["Coiled dowry basket"]),  # title, part of a word
            ("feathers", ["Coiled dowry basket"]),  # description
            ("sedge", ["Coiled dowry basket"]),  # material
            ("tapestry", ["Yörük kilim"]),  # technique
            ("pomoan basket", ["Coiled dowry basket"]),  # community's other name + title
            ("türkiye", ["Yörük kilim"]),  # country
            ("coils", ["Water pot"]),  # how it is made
            ("basket wool", []),  # every word must match the same craft
        ],
    )
    def test_finds_by_any_field(self, client, catalogue, query, expected):
        assert titles(client, q=query) == expected

    def test_restricted_records_never_found(self, client, member_client, catalogue):
        assert "Hidden basket" not in titles(client, q="hidden")
        assert "Hidden basket" not in titles(member_client, q="hidden")

    def test_empty_state_helps(self, client, catalogue):
        html = client.get(reverse("crafts:list"), {"q": "zzz"}).content.decode()
        assert "No crafts match “zzz”" in html and "clear all filters" in html

    def test_title_matches_rank_first(self, client, catalogue):
        CraftFactory(title="Bag", description="Carried with a basket.")
        assert titles(client, q="basket") == ["Coiled dowry basket", "Bag"]


class TestFiltersAndSort:
    def test_material_technique_country_filters(self, client, catalogue):
        assert titles(client, material="wool") == ["Yörük kilim"]
        assert titles(client, technique="Slit tapestry") == ["Yörük kilim"]
        assert titles(client, country="Peru") == ["Water pot"]

    def test_filters_combine_with_search(self, client, catalogue):
        assert titles(client, q="basket", country="Peru") == []
        assert titles(client, type="basketry", country="United States") == ["Coiled dowry basket"]

    @pytest.mark.parametrize(
        "sort, expected",
        [
            ("title", ["Coiled dowry basket", "Water pot", "Yörük kilim"]),
            ("oldest", ["Coiled dowry basket", "Yörük kilim", "Water pot"]),
            ("newest", ["Yörük kilim", "Coiled dowry basket", "Water pot"]),
            ("recent", ["Water pot", "Yörük kilim", "Coiled dowry basket"]),
        ],
    )
    def test_sorting(self, client, catalogue, sort, expected):
        assert titles(client, sort=sort) == expected

    def test_filters_are_kept_in_page_links(self, client, catalogue):
        for n in range(30):
            CraftFactory(title=f"Basket {n:02d}")
        html = client.get(reverse("crafts:list"), {"q": "basket", "sort": "title"}).content
        assert b"?q=basket&amp;sort=title&amp;page=2" in html

    def test_options_only_from_visible_crafts(self, client, catalogue):
        hidden = CraftFactory(title="Secret", visibility=Craft.Visibility.RESTRICTED)
        CraftMaterial.objects.create(
            craft=hidden, material=Material.objects.create(name="Secret fibre")
        )
        html = client.get(reverse("crafts:list")).content.decode()
        assert "Sedge root" in html and "Secret fibre" not in html
