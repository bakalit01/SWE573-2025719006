"""US-19: filter the catalogue by the chosen craft type's own fields."""

import pytest
from django.urls import reverse

from crafts.models import AttributeDefinition, Craft

from .factories import AttributeDefinitionFactory, CraftFactory, CraftTypeFactory

pytestmark = pytest.mark.django_db
T = AttributeDefinition.DataType


@pytest.fixture
def textiles():
    textile = CraftTypeFactory(name="Textile", slug="textile")
    for order, (key, label, data_type, options, unit) in enumerate(
        [
            ("dyes", "Dyes", T.CHOICE, ["Natural", "Synthetic"], ""),
            ("fibres", "Fibres", T.MULTI_CHOICE, ["Wool", "Cotton"], ""),
            ("handmade", "Handmade", T.BOOLEAN, [], ""),
            ("knots", "Knot density", T.NUMBER, [], "per dm²"),
            ("loom", "Loom notes", T.TEXT, [], ""),
        ]
    ):
        AttributeDefinitionFactory(
            craft_type=textile,
            key=key,
            label=label,
            data_type=data_type,
            options=options,
            unit=unit,
            order=order,
        )
    CraftFactory(
        title="Kilim",
        craft_type=textile,
        attributes={"dyes": "Natural", "fibres": ["Wool"], "handmade": True, "knots": 30},
    )
    CraftFactory(
        title="Towel",
        craft_type=textile,
        attributes={"dyes": "Synthetic", "fibres": ["Cotton"], "handmade": False, "knots": "12"},
    )
    CraftFactory(
        title="Felt",
        craft_type=textile,
        attributes={"dyes": "Walnut husk", "fibres": "Wool", "loom": "none"},
    )
    CraftFactory(title="Bowl", attributes={"dyes": "Natural"})  # another type
    return textile


def titles(client, **params):
    return sorted(c.title for c in client.get(reverse("crafts:list"), params).context["crafts"])


def test_filters_appear_only_once_a_single_type_is_chosen(client, textiles):
    assert client.get(reverse("crafts:list")).context["attribute_specs"] == []
    specs = client.get(reverse("crafts:list"), {"type": "textile"}).context["attribute_specs"]
    assert [s["definition"].key for s in specs] == ["dyes", "fibres", "handmade", "knots"]
    html = client.get(reverse("crafts:list"), {"type": "textile"}).content.decode()
    assert "Textile details" in html and "Knot density (per dm²)" in html
    assert "Loom notes" not in html  # text fields aren't filterable


def test_choice_options_include_values_typed_under_other(client, textiles):
    specs = client.get(reverse("crafts:list"), {"type": "textile"}).context["attribute_specs"]
    assert specs[0]["options"] == ["Natural", "Synthetic", "Walnut husk"]


def test_choice_filter(client, textiles):
    assert titles(client, type="textile", a_dyes="natural") == ["Kilim"]
    assert titles(client, type="textile", a_dyes="Walnut husk") == ["Felt"]


def test_multi_choice_filter_matches_lists_and_single_values(client, textiles):
    assert titles(client, type="textile", a_fibres="Wool") == ["Felt", "Kilim"]


def test_yes_no_filter(client, textiles):
    assert titles(client, type="textile", a_handmade="yes") == ["Kilim"]
    assert titles(client, type="textile", a_handmade="no") == ["Towel"]
    assert titles(client, type="textile", a_handmade="maybe") == ["Felt", "Kilim", "Towel"]


def test_number_range_includes_numbers_stored_as_text(client, textiles):
    assert titles(client, type="textile", a_knots_min="10", a_knots_max="20") == ["Towel"]
    assert titles(client, type="textile", a_knots_min="25") == ["Kilim"]
    assert titles(client, type="textile", a_knots_max="abc") == ["Felt", "Kilim", "Towel"]


def test_filters_combine_and_stay_in_page_links(client, textiles):
    response = client.get(
        reverse("crafts:list"), {"type": "textile", "a_fibres": "Wool", "a_handmade": "yes"}
    )
    assert [c.title for c in response.context["crafts"]] == ["Kilim"]
    assert "a_fibres=Wool" in response.context["filter_query"]
    assert response.context["any_filter"]


def test_attribute_params_are_ignored_without_a_type(client, textiles):
    assert titles(client, a_dyes="Natural") == ["Bowl", "Felt", "Kilim", "Towel"]


def test_retired_fields_are_not_offered(client, textiles):
    textiles.attributes.filter(key="dyes").update(is_active=False)
    specs = client.get(reverse("crafts:list"), {"type": "textile"}).context["attribute_specs"]
    assert "dyes" not in [s["definition"].key for s in specs]


def test_only_visible_crafts_feed_the_options(client, textiles):
    hidden = Craft.objects.get(title="Felt")
    hidden.visibility = Craft.Visibility.MEMBERS
    hidden.save()
    specs = client.get(reverse("crafts:list"), {"type": "textile"}).context["attribute_specs"]
    assert "Walnut husk" not in specs[0]["options"]
