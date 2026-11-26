"""US-13: admins manage craft types and their fields in the admin, without a code change."""

import pytest
from django.urls import reverse

from accounts.models import User
from crafts.forms import AttributesForm
from crafts.models import AttributeDefinition, CraftType, attribute_value_fits
from crafts.seeding import ensure_craft_types

from .factories import AttributeDefinitionFactory, CraftFactory, CraftTypeFactory, UserFactory

pytestmark = pytest.mark.django_db
T = AttributeDefinition.DataType


@pytest.fixture
def admin_client(client):
    client.force_login(UserFactory(role=User.Role.ADMIN, is_superuser=True))
    return client


@pytest.fixture
def pottery():
    craft_type = CraftTypeFactory(name="Pottery", slug="pottery")
    firing = AttributeDefinitionFactory(
        craft_type=craft_type, key="firing", label="Firing", order=10
    )
    height = AttributeDefinitionFactory(
        craft_type=craft_type, key="height", label="Height", data_type=T.TEXT, order=20
    )
    return {"type": craft_type, "firing": firing, "height": height}


def row(definition, **changes):
    """One inline row of the craft type admin page, as the browser would send it."""
    values = {
        "id": definition.pk,
        "craft_type": definition.craft_type_id,
        "order": definition.order,
        "key": definition.key,
        "label": definition.label,
        "data_type": definition.data_type,
        "unit": definition.unit,
        "options": "\n".join(definition.options),
        "help_text": definition.help_text,
        "required": "on" if definition.required else "",
        "is_active": "on" if definition.is_active else "",
    }
    values.update(changes)
    return {k: v for k, v in values.items() if v != ""}


def save_type(client, craft_type, rows, new_rows=()):
    data = {
        "name": craft_type.name,
        "slug": craft_type.slug,
        "description": craft_type.description,
        "attributes-TOTAL_FORMS": str(len(rows) + len(new_rows)),
        "attributes-INITIAL_FORMS": str(len(rows)),
        "attributes-MIN_NUM_FORMS": "0",
        "attributes-MAX_NUM_FORMS": "1000",
    }
    for i, values in enumerate([*rows, *new_rows]):
        data.update({f"attributes-{i}-{k}": v for k, v in values.items()})
    url = reverse("admin:crafts_crafttype_change", args=[craft_type.pk])
    return client.post(url, data)


def form_fields(craft_type):
    return list(AttributesForm(craft_type=craft_type).fields)


class TestCreate:
    def test_admin_creates_type_with_fields_used_by_the_form_at_once(self, admin_client, user):
        data = {
            "name": "Glass beads",
            "slug": "glass-beads",
            "description": "",
            "attributes-TOTAL_FORMS": "2",
            "attributes-INITIAL_FORMS": "0",
            "attributes-MIN_NUM_FORMS": "0",
            "attributes-MAX_NUM_FORMS": "1000",
            "attributes-0-order": "1",
            "attributes-0-key": "bead_size",
            "attributes-0-label": "Bead size",
            "attributes-0-data_type": "number",
            "attributes-0-unit": "mm",
            "attributes-0-is_active": "on",
            "attributes-1-order": "2",
            "attributes-1-key": "colour",
            "attributes-1-label": "Colour",
            "attributes-1-data_type": "choice",
            "attributes-1-options": "Red\n\nBlue\nRed\n  White  ",
            "attributes-1-is_active": "on",
        }
        response = admin_client.post(reverse("admin:crafts_crafttype_add"), data)
        assert response.status_code == 302
        glass = CraftType.objects.get(slug="glass-beads")
        colour = glass.attributes.get(key="colour")
        assert colour.options == ["Red", "Blue", "White"]  # one per line, blanks/repeats dropped
        assert form_fields(glass) == ["bead_size", "colour", "colour__other"]
        user.role = User.Role.MAKER
        user.save()
        client = admin_client
        client.force_login(user)
        html = client.get(reverse("crafts:attribute_fields"), {"craft_type": glass.pk})
        assert "Bead size (mm)" in html.content.decode()

    def test_type_list_shows_field_and_craft_counts(self, admin_client, pottery):
        CraftFactory(craft_type=pottery["type"])
        response = admin_client.get(reverse("admin:crafts_crafttype_changelist"))
        assert response.status_code == 200
        row_html = response.content.decode().split("Pottery", 1)[1].split("</tr>", 1)[0]
        assert '<td class="field-field_count">2</td>' in row_html
        assert '<td class="field-craft_count">1</td>' in row_html

    def test_change_page_loads_with_reorder_script(self, admin_client, pottery):
        url = reverse("admin:crafts_crafttype_change", args=[pottery["type"].pk])
        html = admin_client.get(url).content.decode()
        assert "js/admin_attributes.js" in html and "Firing" in html


class TestEdit:
    def test_reordering_changes_the_form_at_once(self, admin_client, pottery):
        rows = [row(pottery["firing"], order=20), row(pottery["height"], order=10)]
        assert save_type(admin_client, pottery["type"], rows).status_code == 302
        assert form_fields(pottery["type"]) == ["height", "firing"]

    def test_retiring_hides_the_field_but_keeps_data(self, admin_client, client, pottery):
        craft = CraftFactory(craft_type=pottery["type"], attributes={"firing": "Open pit"})
        rows = [row(pottery["firing"], is_active=""), row(pottery["height"])]
        assert save_type(admin_client, pottery["type"], rows).status_code == 302
        assert form_fields(pottery["type"]) == ["height"]
        craft.refresh_from_db()
        assert craft.attributes == {"firing": "Open pit"}
        client.logout()
        assert "Open pit" not in client.get(craft.get_absolute_url()).content.decode()

    def test_type_change_is_blocked_when_stored_values_would_not_fit(self, admin_client, pottery):
        CraftFactory(title="Tall jar", craft_type=pottery["type"], attributes={"height": "tall"})
        rows = [row(pottery["firing"]), row(pottery["height"], data_type="number")]
        response = save_type(admin_client, pottery["type"], rows)
        assert response.status_code == 200
        html = response.content.decode()
        assert "Can&#x27;t change to “Number”: 1 craft(s)" in html and "Tall jar" in html
        pottery["height"].refresh_from_db()
        assert pottery["height"].data_type == T.TEXT

    def test_type_change_is_allowed_when_stored_values_fit(self, admin_client, pottery):
        CraftFactory(craft_type=pottery["type"], attributes={"height": "30"})
        rows = [row(pottery["firing"]), row(pottery["height"], data_type="number", unit="cm")]
        assert save_type(admin_client, pottery["type"], rows).status_code == 302
        pottery["height"].refresh_from_db()
        assert (pottery["height"].data_type, pottery["height"].unit) == (T.NUMBER, "cm")

    def test_renaming_a_key_with_stored_values_is_blocked(self, admin_client, pottery):
        CraftFactory(craft_type=pottery["type"], attributes={"firing": "Kiln"})
        rows = [row(pottery["firing"], key="firing_method"), row(pottery["height"])]
        response = save_type(admin_client, pottery["type"], rows)
        assert response.status_code == 200
        assert "1 craft(s) store values under “firing”" in response.content.decode()
        pottery["firing"].refresh_from_db()
        assert pottery["firing"].key == "firing"

    def test_renaming_a_key_without_values_is_allowed(self, admin_client, pottery):
        rows = [row(pottery["firing"], key="firing_method"), row(pottery["height"])]
        assert save_type(admin_client, pottery["type"], rows).status_code == 302
        pottery["firing"].refresh_from_db()
        assert pottery["firing"].key == "firing_method"

    def test_deleting_a_field_with_values_is_blocked(self, admin_client, pottery):
        CraftFactory(craft_type=pottery["type"], attributes={"firing": "Kiln"})
        rows = [row(pottery["firing"], DELETE="on"), row(pottery["height"])]
        response = save_type(admin_client, pottery["type"], rows)
        assert response.status_code == 200
        assert "Untick Active to retire it instead" in response.content.decode()
        assert AttributeDefinition.objects.filter(pk=pottery["firing"].pk).exists()

    def test_deleting_an_unused_field_is_allowed(self, admin_client, pottery):
        rows = [row(pottery["firing"], DELETE="on"), row(pottery["height"])]
        assert save_type(admin_client, pottery["type"], rows).status_code == 302
        assert not AttributeDefinition.objects.filter(pk=pottery["firing"].pk).exists()

    def test_adding_a_field_to_an_existing_type(self, admin_client, pottery):
        new = {"order": "30", "key": "glaze", "label": "Glaze", "data_type": "boolean"}
        rows = [row(pottery["firing"]), row(pottery["height"])]
        assert save_type(admin_client, pottery["type"], rows, [new | {"is_active": "on"}])
        assert form_fields(pottery["type"]) == ["firing", "height", "glaze"]


@pytest.mark.parametrize(
    ("data_type", "value", "fits"),
    [
        (T.TEXT, "Knives", True),
        (T.TEXT, 30, True),
        (T.TEXT, ["a", "b"], False),
        (T.TEXT, True, False),
        (T.NUMBER, 30, True),
        (T.NUMBER, "30.5", True),
        (T.NUMBER, "tall", False),
        (T.NUMBER, True, False),
        (T.CHOICE, "Not in the options", True),  # shown as "Other"
        (T.MULTI_CHOICE, ["Glass", "Shell"], True),
        (T.MULTI_CHOICE, "Glass", True),
        (T.BOOLEAN, False, True),
        (T.BOOLEAN, "yes", False),
        (T.URL, "https://example.org/a", True),
        (T.URL, "example", False),
        (T.LONG_TEXT, None, True),
    ],
)
def test_attribute_value_fits(data_type, value, fits):
    assert attribute_value_fits(data_type, value) is fits


def test_start_up_seed_keeps_admin_changes(db):
    types = ensure_craft_types()
    loom = types["textile"].attributes.get(key="loom_type")
    loom.label, loom.is_active, loom.order = "Loom", False, 99
    loom.save()
    types["textile"].name = "Weaving"
    types["textile"].save()
    ensure_craft_types()  # runs on every start-up on Render
    loom.refresh_from_db()
    assert (loom.label, loom.is_active, loom.order) == ("Loom", False, 99)
    assert CraftType.objects.get(slug="textile").name == "Weaving"
