"""US-28: admins manage communities, regions, materials and techniques: merge duplicates
without losing links to crafts, and keep alternate spellings that search uses."""

import pytest
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.urls import reverse

from accounts.models import User
from communities.models import Community, Region
from crafts.models import Craft, CraftMaterial, CraftTechnique, Material, Tag, Technique
from crafts.taxonomy import merge
from crafts.terms import find_term, join_names, split_names

from .factories import CommunityFactory, CraftFactory, UserFactory
from .test_contribute import payload

pytestmark = pytest.mark.django_db


def titles(client, **params):
    return sorted(c.title for c in client.get(reverse("crafts:list"), params).context["crafts"])


def test_split_and_join_names():
    assert split_names(" Navajo ,  Navaho,, ") == ["Navajo", "Navaho"]
    assert join_names(["Wool", "wool", "Sheep wool", "Yün"], exclude=["Yün"]) == "Wool, Sheep wool"


def test_find_term_by_name_or_alternate_spelling():
    wool = Material.objects.create(name="Wool", other_names="Yün, sheep's wool")
    assert find_term(Material, "wool") == wool
    assert find_term(Material, "YÜN") == wool
    assert find_term(Material, "sheep") is None  # whole names only


class TestMerge:
    def test_materials_keep_every_craft_link_and_fill_details(self):
        wool = Material.objects.create(name="Wool")
        dupe = Material.objects.create(name="wool yarn", other_names="yün")
        both = CraftFactory(title="Both")
        only_dupe = CraftFactory(title="Only the duplicate")
        CraftMaterial.objects.create(craft=both, material=wool)
        CraftMaterial.objects.create(craft=both, material=dupe, origin="Local flocks")
        CraftMaterial.objects.create(craft=only_dupe, material=dupe, notes="Hand spun")
        assert merge(wool, [dupe]) == 2
        assert not Material.objects.filter(pk=dupe.pk).exists()
        wool.refresh_from_db()
        assert wool.other_names == "wool yarn, yün"
        assert both.craft_materials.get().origin == "Local flocks"  # one row, details kept
        assert only_dupe.craft_materials.get().material == wool
        assert only_dupe.craft_materials.get().notes == "Hand spun"

    def test_techniques(self):
        keep = Technique.objects.create(name="Twining")
        dupe = Technique.objects.create(name="Twined weaving")
        craft = CraftFactory()
        CraftTechnique.objects.create(craft=craft, technique=dupe, notes="Close twining")
        merge(keep, [dupe])
        assert craft.craft_techniques.get().technique == keep

    def test_communities_move_crafts_members_and_stewards(self):
        keep = CommunityFactory(name="Diné", region="Southwest")
        dupe = CommunityFactory(name="Navajo", other_names="Navaho", description="Words")
        craft = CraftFactory(community=dupe)
        member = UserFactory(community=dupe)
        steward = UserFactory(role=User.Role.STEWARD)
        dupe.stewards.add(steward)
        merge(keep, [dupe])
        craft.refresh_from_db()
        member.refresh_from_db()
        keep.refresh_from_db()
        assert craft.community == keep and member.community == keep
        assert list(keep.stewards.all()) == [steward]
        assert keep.other_names == "Navajo, Navaho" and keep.description == "Words"
        assert not Community.objects.filter(pk=dupe.pk).exists()

    def test_regions(self):
        keep = Region.objects.create(name="Black Sea")
        dupe = Region.objects.create(name="Black sea coast")
        community = CommunityFactory(region=dupe)
        merge(keep, [dupe])
        community.refresh_from_db()
        assert community.region == keep and keep.other_names == "Black sea coast"

    def test_tags(self):
        keep, dupe = Tag.objects.create(name="dye", slug="dye"), Tag.objects.create(
            name="dyes", slug="dyes"
        )
        craft = CraftFactory()
        craft.tags.add(dupe)
        merge(keep, [dupe])
        assert list(craft.tags.all()) == [keep]


class TestAdminMerge:
    @pytest.fixture
    def admin_client(self, client):
        client.force_login(UserFactory(role=User.Role.ADMIN, is_superuser=True))
        return client

    def test_confirm_page_then_merge(self, admin_client):
        wool = Material.objects.create(name="Wool")
        dupe = Material.objects.create(name="Wool yarn")
        CraftMaterial.objects.create(craft=CraftFactory(), material=wool)
        url = reverse("admin:crafts_material_changelist")
        chosen = {"action": "merge_selected", ACTION_CHECKBOX_NAME: [wool.pk, dupe.pk]}
        page = admin_client.post(url, chosen)
        html = page.content.decode()
        assert page.status_code == 200 and "Choose the one to keep" in html
        assert f'value="{wool.pk}" checked' in html  # the one with most crafts is suggested
        done = admin_client.post(url, chosen | {"keep": wool.pk, "confirm": "yes"}, follow=True)
        assert "Merged “Wool yarn” into “Wool”" in done.content.decode()
        assert list(Material.objects.values_list("name", "other_names")) == [
            ("Wool", "Wool yarn")
        ]

    def test_needs_two(self, admin_client):
        wool = Material.objects.create(name="Wool")
        url = reverse("admin:crafts_material_changelist")
        response = admin_client.post(
            url, {"action": "merge_selected", ACTION_CHECKBOX_NAME: [wool.pk]}, follow=True
        )
        assert "Select two or more to merge." in response.content.decode()

    @pytest.mark.parametrize(
        "url_name",
        [
            "admin:communities_region_changelist",
            "admin:communities_community_changelist",
            "admin:crafts_technique_changelist",
            "admin:crafts_tag_changelist",
        ],
    )
    def test_other_lists_offer_merging(self, admin_client, url_name):
        response = admin_client.get(reverse(url_name))
        model_admin = response.context["cl"].model_admin
        assert "merge_selected" in model_admin.get_actions(response.wsgi_request)


class TestAlternateSpellingsInSearch:
    def test_material_and_technique(self, client):
        craft = CraftFactory(title="Rug")
        wool = Material.objects.create(name="Wool", other_names="Yün")
        CraftMaterial.objects.create(craft=craft, material=wool)
        knotting = Technique.objects.create(name="Knotting", other_names="Ghiordes knot")
        CraftTechnique.objects.create(craft=craft, technique=knotting)
        assert titles(client, q="yün") == ["Rug"]
        assert titles(client, q="ghiordes") == ["Rug"]

    def test_region_and_community(self, client):
        CraftFactory(
            title="Rug",
            community=CommunityFactory(
                name="Yörük", region="Taurus Mountains", other_names="Yuruk"
            ),
        )
        Region.objects.filter(name="Taurus Mountains").update(other_names="Toros Dağları")
        assert titles(client, q="toros") == ["Rug"]
        assert titles(client, q="yuruk") == ["Rug"]
        assert titles(client, place="taurus") == ["Rug"]


class TestFormsUseExistingTerms:
    def test_typed_material_matches_alternate_spelling(self, member_client, setup):
        wool = Material.objects.create(name="Wool", other_names="Yün")
        member_client.post(
            reverse("crafts:create"), payload(setup, **{"mat-0-name": "yün", "mat-0-origin": ""})
        )
        craft = Craft.objects.get(title="Carved pipe")
        assert wool in craft.materials.all()
        assert not Material.objects.filter(name__iexact="yün").exists()

    def test_typed_community_matches_alternate_spelling(self, member_client, setup):
        dine = CommunityFactory(name="Diné", other_names="Navajo, Navaho")
        data = payload(setup, community="__other__", community_other="navajo")
        member_client.post(reverse("crafts:create"), data)
        assert Craft.objects.get(title="Carved pipe").community == dine

    def test_steward_region_matches_or_creates(self, client):
        steward = UserFactory(role=User.Role.STEWARD)
        community = CommunityFactory(region="")
        community.stewards.add(steward)
        Region.objects.create(name="Black Sea", other_names="Karadeniz")
        client.force_login(steward)
        url = reverse("communities:edit", args=[community.slug])
        client.post(url, {"other_names": "", "region": "karadeniz", "description": "Ours"})
        community.refresh_from_db()
        assert community.region.name == "Black Sea"
        client.post(url, {"other_names": "", "region": "Pontic Alps", "description": "Ours"})
        community.refresh_from_db()
        assert community.region.name == "Pontic Alps" and Region.objects.count() == 2
        assert 'value="Pontic Alps"' in client.get(url).content.decode()


def test_start_up_seed_keeps_a_region_set_by_an_admin():
    from django.core.management import call_command

    call_command("seed_reference_crafts")
    yoruk = Community.objects.get(slug="yoruk")
    yoruk.region = Region.objects.create(name="Mediterranean Türkiye")
    yoruk.save()
    call_command("seed_reference_crafts")
    yoruk.refresh_from_db()
    assert yoruk.region.name == "Mediterranean Türkiye"
