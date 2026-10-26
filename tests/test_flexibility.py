"""'Other (type your own)' for craft type, community, units and choice fields; own details; tags."""

import pytest
from django.urls import reverse

from communities.models import Community
from crafts import units
from crafts.forms import OTHER, parse_tags
from crafts.models import AttributeDefinition, Craft, CraftType, Tag

from .factories import AttributeDefinitionFactory, CraftFactory
from .test_contribute import payload

pytestmark = pytest.mark.django_db


def post(client, data, craft=None):
    url = reverse("crafts:edit", args=[craft.slug]) if craft else reverse("crafts:create")
    return client.post(url, data)


class TestOtherTypeAndCommunity:
    def test_typed_craft_type_and_community_are_added(self, member_client, user, setup):
        data = payload(
            setup,
            craft_type=OTHER,
            craft_type_other="  Felt   making ",
            community=OTHER,
            community_other="Yörük",
        )
        response = post(member_client, data)
        craft = Craft.objects.get()
        assert response.status_code == 302
        assert craft.craft_type.name == "Felt making" and craft.craft_type.added_by == user
        assert craft.craft_type.slug == "felt-making"
        assert craft.community.name == "Yörük" and craft.community.added_by == user
        assert craft.attributes == {}  # a new type has no set fields

    def test_typed_name_reuses_an_existing_entry(self, member_client, setup):
        data = payload(
            setup,
            craft_type=OTHER,
            craft_type_other="carving",
            community=OTHER,
            community_other=setup["community"].name.upper(),
        )
        post(member_client, data)
        craft = Craft.objects.get()
        assert craft.craft_type == setup["type"]
        assert craft.community == setup["community"]
        assert CraftType.objects.count() == 1 and Community.objects.count() == 1

    def test_other_needs_a_name(self, member_client, setup):
        response = post(member_client, payload(setup, craft_type=OTHER, community=OTHER))
        assert response.status_code == 200
        assert not Craft.objects.exists()
        assert response.content.decode().count("Type the name, or choose one from the list.") == 2

    def test_new_entries_appear_in_lists_and_filters(self, member_client, client, setup):
        post(member_client, payload(setup, community=OTHER, community_other="Sámi of Inari"))
        form_page = member_client.get(reverse("crafts:create")).content.decode()
        assert "Sámi of Inari" in form_page and "Other (type your own)" in form_page
        assert "Sámi of Inari" in client.get(reverse("crafts:list")).content.decode()

    def test_type_fields_endpoint_explains_new_type(self, member_client):
        html = member_client.get(reverse("crafts:attribute_fields"), {"craft_type": OTHER})
        assert "A new craft type has no set fields yet" in html.content.decode()

    def test_edit_form_preselects_current_choices(self, member_client, setup):
        post(member_client, payload(setup))
        craft = Craft.objects.get()
        page = member_client.get(reverse("crafts:edit", args=[craft.slug])).content.decode()
        assert f'<option value="{setup["type"].pk}" selected>' in page
        assert f'<option value="{setup["community"].pk}" selected>' in page


class TestOtherUnits:
    def test_typed_units_are_kept_and_not_converted(self, member_client, client, setup):
        data = payload(
            setup,
            size_unit=units.OTHER,
            size_unit_other="karış",
            weight_unit=units.OTHER,
            weight_unit_other="okka",
        )
        post(member_client, data)
        craft = Craft.objects.get()
        assert craft.size == {"original": "6 × 14 × 5 karış", "axes": "H × W × D", "converted": ""}
        assert craft.weight_display == {"original": "1.8 okka", "converted": ""}
        page = client.get(craft.get_absolute_url()).content.decode()
        assert "6 × 14 × 5 karış" in page and "1.8 okka" in page

    def test_other_unit_needs_a_name(self, member_client, setup):
        response = post(member_client, payload(setup, size_unit=units.OTHER))
        assert response.status_code == 200
        assert "Type the unit you measured in." in response.content.decode()

    def test_typed_unit_is_cleared_when_a_listed_unit_is_chosen(self, member_client, setup):
        post(member_client, payload(setup, size_unit_other="karış"))
        assert Craft.objects.get().size_unit_other == ""


class TestOtherInCraftDetails:
    @pytest.fixture
    def multi(self, setup):
        return AttributeDefinitionFactory(
            craft_type=setup["type"],
            key="woods",
            label="Woods",
            data_type=AttributeDefinition.DataType.MULTI_CHOICE,
            options=["Cedar", "Birch"],
        )

    def test_choice_and_multi_choice_accept_own_values(self, member_client, setup, multi):
        data = payload(setup, **{"attr-finish": OTHER, "attr-finish__other": "Smoked"})
        data["attr-woods"] = ["Cedar", OTHER]
        data["attr-woods__other"] = "Juniper, Olive, cedar"
        post(member_client, data)
        craft = Craft.objects.get()
        assert craft.attributes["finish"] == "Smoked"
        assert craft.attributes["woods"] == ["Cedar", "Juniper", "Olive", "cedar"]
        page = member_client.get(reverse("crafts:edit", args=[craft.slug])).content.decode()
        assert 'value="Smoked"' in page  # typed value goes back into the Other box
        assert 'value="Juniper, Olive, cedar"' in page

    def test_other_choice_needs_a_value(self, member_client, setup):
        response = post(member_client, payload(setup, **{"attr-finish": OTHER}))
        assert response.status_code == 200
        assert "Type your own value, or choose one above." in response.content.decode()

    def test_own_details_are_saved_and_shown(self, member_client, client, setup):
        data = payload(
            setup,
            **{
                "det-TOTAL_FORMS": "3",
                "det-0-label": "Dye source",
                "det-0-value": "Walnut husks",
                "det-1-label": "",
                "det-1-value": "",
                "det-2-label": "Used for",
                "det-2-value": "Weddings",
            },
        )
        post(member_client, data)
        craft = Craft.objects.get()
        assert craft.extra_details == [
            {"label": "Dye source", "value": "Walnut husks"},
            {"label": "Used for", "value": "Weddings"},
        ]
        assert ("Dye source", "Walnut husks") in craft.attribute_rows()
        page = client.get(craft.get_absolute_url()).content.decode()
        assert "Walnut husks" in page
        edit = member_client.get(reverse("crafts:edit", args=[craft.slug])).content.decode()
        assert 'value="Weddings"' in edit

    def test_detail_row_needs_both_parts(self, member_client, setup):
        data = payload(setup, **{"det-0-label": "", "det-0-value": "Walnut husks"})
        response = post(member_client, data)
        assert response.status_code == 200 and "Name this detail." in response.content.decode()


class TestTags:
    def test_parse_tags(self):
        assert parse_tags(" Ceremonial, natural  dye,#ceremonial,, everyday use ") == [
            "Ceremonial",
            "natural dye",
            "everyday use",
        ]

    def test_tags_saved_reused_and_shown(self, member_client, client, setup):
        Tag.objects.create(name="ceremonial", slug="ceremonial")
        post(member_client, payload(setup, tags="Ceremonial, natural dye"))
        craft = Craft.objects.get()
        assert sorted(t.name for t in craft.tags.all()) == ["ceremonial", "natural dye"]
        assert Tag.objects.count() == 2
        page = client.get(craft.get_absolute_url()).content.decode()
        assert "#natural dye" in page and "?tag=natural-dye" in page
        edit = member_client.get(reverse("crafts:edit", args=[craft.slug])).content.decode()
        assert "ceremonial, natural dye" in edit
        assert 'data-add-tag="ceremonial"' in edit  # suggestions from tags already in use

    def test_catalogue_filters_by_tag(self, member_client, client, setup):
        post(member_client, payload(setup, tags="ceremonial"))
        CraftFactory(title="Untagged bowl")
        html = client.get(reverse("crafts:list"), {"tag": "ceremonial"}).content.decode()
        assert "Carved pipe" in html and "Untagged bowl" not in html
        assert "#ceremonial" in html

    def test_tag_limits(self, member_client, setup):
        many = ", ".join(f"tag {n}" for n in range(16))
        response = post(member_client, payload(setup, tags=many))
        assert "Use at most 15 tags." in response.content.decode()
        response = post(member_client, payload(setup, tags="x" * 41))
        assert "Keep each tag under 40 characters" in response.content.decode()

    def test_removing_tags_on_edit(self, member_client, setup):
        post(member_client, payload(setup, tags="ceremonial, gift"))
        craft = Craft.objects.get()
        post(member_client, payload(setup, tags="gift"), craft=craft)
        assert [t.name for t in craft.tags.all()] == ["gift"]
