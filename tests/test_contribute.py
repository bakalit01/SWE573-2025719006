"""US-08 add, US-09 edit/delete, US-11 type fields, US-20 photos, FB-01…FB-04 details."""

import io
from decimal import Decimal

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from crafts.models import AttributeDefinition, Craft, CraftMaterial, Media

from .factories import AttributeDefinitionFactory, CommunityFactory, CraftFactory, CraftTypeFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


def photo(name="photo.jpg", size=(2400, 1200)):
    buffer = io.BytesIO()
    Image.new("RGB", size, (180, 120, 80)).save(buffer, "JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


@pytest.fixture
def setup():
    craft_type = CraftTypeFactory(name="Carving", slug="carving")
    AttributeDefinitionFactory(craft_type=craft_type, key="tools", label="Tools")
    AttributeDefinitionFactory(
        craft_type=craft_type,
        key="finish",
        label="Finish",
        data_type=AttributeDefinition.DataType.CHOICE,
        options=["Oiled", "Waxed"],
    )
    return {"type": craft_type, "community": CommunityFactory()}


def payload(setup, **overrides):
    data = {
        "title": "Carved pipe",
        "craft_type": setup["type"].pk,
        "community": setup["community"].pk,
        "summary": "A pipe bowl.",
        "maker_credit": "A workshop",
        "year_made": "1978",
        "year_is_approximate": "on",
        "place_name": "Eskişehir",
        "country": "Türkiye",
        "latitude": "39.7767",
        "longitude": "30.5206",
        "location_precision": "exact",
        "height": "6",
        "width": "14",
        "depth": "5",
        "size_unit": "cm",
        "weight": "1.8",
        "weight_unit": "oz",
        "traditional_measure": "A hand span",
        "process": "Soaked, carved, polished.",
        "visibility": "public",
        "mat-TOTAL_FORMS": "2",
        "mat-INITIAL_FORMS": "0",
        "mat-MIN_NUM_FORMS": "1",
        "mat-MAX_NUM_FORMS": "30",
        "mat-0-name": "Meerschaum",
        "mat-0-origin": "Mined nearby",
        "mat-0-notes": "Soaked",
        "mat-1-name": "Beeswax",
        "mat-1-origin": "",
        "mat-1-notes": "",
        "tec-TOTAL_FORMS": "1",
        "tec-INITIAL_FORMS": "0",
        "tec-MIN_NUM_FORMS": "1",
        "tec-MAX_NUM_FORMS": "30",
        "tec-0-name": "Knife carving",
        "tec-0-notes": "Carved wet",
        "img-TOTAL_FORMS": "1",
        "img-INITIAL_FORMS": "0",
        "img-MIN_NUM_FORMS": "0",
        "img-MAX_NUM_FORMS": "12",
        "attr-tools": "Knives",
        "attr-finish": "Waxed",
        "action": "publish",
    }
    data.update(overrides)
    return data


class TestAdd:
    def test_requires_login(self, client):
        response = client.get(reverse("crafts:create"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_publish_saves_everything(self, member_client, user, setup):
        data = payload(
            setup,
            **{"img-0-image": photo(), "img-0-alt_text": "A carved bowl", "img-0-credit": "Me"},
        )
        response = member_client.post(reverse("crafts:create"), data)
        craft = Craft.objects.get(title="Carved pipe")
        assert response.status_code == 302 and response.url == craft.get_absolute_url()
        assert craft.created_by == user
        assert craft.status == Craft.Status.PUBLISHED
        assert craft.attributes == {"tools": "Knives", "finish": "Waxed"}
        assert craft.made_in == "c. 1978"
        assert craft.made_from == "Meerschaum, Beeswax"
        assert craft.place_label == "Eskişehir, Türkiye"
        assert craft.latitude == Decimal("39.776700")
        assert craft.size["original"] == "6 × 14 × 5 cm"
        assert craft.weight_display == {"original": "1.8 oz", "converted": "≈ 51 g"}
        cm = CraftMaterial.objects.get(craft=craft, material__name="Meerschaum")
        assert (cm.origin, cm.notes) == ("Mined nearby", "Soaked")
        media = Media.objects.get(craft=craft)
        assert media.alt_text == "A carved bowl"
        assert max(media.image.width, media.image.height) == 1600  # resized

    def test_publish_needs_a_material(self, member_client, setup):
        data = payload(
            setup, **{"mat-0-name": "", "mat-0-origin": "", "mat-0-notes": "", "mat-1-name": ""}
        )
        response = member_client.post(reverse("crafts:create"), data)
        assert response.status_code == 200
        assert "Add at least one material." in response.content.decode()
        assert not Craft.objects.exists()

    def test_draft_without_material_is_private(self, member_client, client, setup):
        data = payload(
            setup,
            action="draft",
            **{"mat-0-name": "", "mat-0-origin": "", "mat-0-notes": "", "mat-1-name": ""},
        )
        member_client.post(reverse("crafts:create"), data)
        craft = Craft.objects.get()
        assert craft.status == Craft.Status.DRAFT
        assert member_client.get(craft.get_absolute_url()).status_code == 200
        assert craft.title not in member_client.get(reverse("crafts:list")).content.decode()
        client.logout()
        assert client.get(craft.get_absolute_url()).status_code == 404

    def test_photo_needs_alt_text(self, member_client, setup):
        data = payload(setup, **{"img-0-image": photo(), "img-0-alt_text": ""})
        response = member_client.post(reverse("crafts:create"), data)
        assert "Describe the photo" in response.content.decode()
        assert not Craft.objects.exists()

    @pytest.mark.parametrize(
        ("overrides", "message"),
        [
            ({"year_made": "2999"}, "can&#x27;t be in the future"),
            ({"longitude": ""}, "Give both latitude and longitude"),
            ({"size_unit": ""}, "Choose the unit for the size."),
            ({"weight_unit": ""}, "Choose the unit for the weight."),
            ({"attr-finish": "Painted"}, "Select a valid choice"),
            ({"maker_credit": ""}, "This field is required"),
        ],
    )
    def test_validation(self, member_client, setup, overrides, message):
        response = member_client.post(reverse("crafts:create"), payload(setup, **overrides))
        assert response.status_code == 200
        assert message in response.content.decode()
        assert not Craft.objects.exists()

    def test_reserved_slug_is_avoided(self, member_client, setup):
        member_client.post(reverse("crafts:create"), payload(setup, title="Add"))
        assert Craft.objects.get().slug == "add-craft"

    def test_required_attribute_field(self, member_client, setup):
        AttributeDefinitionFactory(
            craft_type=setup["type"], key="wood", label="Wood", required=True
        )
        response = member_client.post(reverse("crafts:create"), payload(setup))
        assert response.status_code == 200
        assert not Craft.objects.exists()


class TestAttributeFieldsEndpoint:
    def test_returns_fields_for_type(self, member_client, setup):
        html = member_client.get(
            reverse("crafts:attribute_fields"), {"craft_type": setup["type"].pk}
        ).content.decode()
        assert 'name="attr-tools"' in html and 'name="attr-finish"' in html
        assert "Waxed" in html

    def test_no_type_shows_hint(self, member_client):
        html = member_client.get(reverse("crafts:attribute_fields")).content.decode()
        assert "Choose a craft type" in html


class TestEditDelete:
    def test_owner_can_edit_and_rows_are_prefilled(self, member_client, user, setup):
        member_client.post(reverse("crafts:create"), payload(setup))
        craft = Craft.objects.get()
        page = member_client.get(reverse("crafts:edit", args=[craft.slug])).content.decode()
        assert 'value="Meerschaum"' in page and 'value="Knives"' in page
        member_client.post(
            reverse("crafts:edit", args=[craft.slug]),
            payload(setup, title="Carved pipe (edited)", **{"mat-TOTAL_FORMS": "1"}),
        )
        craft.refresh_from_db()
        assert craft.title == "Carved pipe (edited)"
        assert craft.made_from == "Meerschaum"
        assert craft.created_by == user

    def test_others_cannot_edit_or_delete(self, member_client):
        other = CraftFactory()
        assert member_client.get(reverse("crafts:edit", args=[other.slug])).status_code == 404
        assert member_client.post(reverse("crafts:delete", args=[other.slug])).status_code == 404
        assert Craft.objects.filter(pk=other.pk).exists()

    def test_delete_asks_then_deletes(self, member_client, user):
        craft = CraftFactory(created_by=user)
        url = reverse("crafts:delete", args=[craft.slug])
        assert "be undone" in member_client.get(url).content.decode()
        assert Craft.objects.filter(pk=craft.pk).exists()
        response = member_client.post(url)
        assert response.url == reverse("crafts:mine")
        assert not Craft.objects.filter(pk=craft.pk).exists()

    def test_my_crafts_lists_only_mine_including_drafts(self, member_client, user):
        CraftFactory(title="Mine draft", created_by=user, status=Craft.Status.DRAFT)
        CraftFactory(title="Someone else's")
        html = member_client.get(reverse("crafts:mine")).content.decode()
        assert "Mine draft" in html and "Someone else" not in html


class TestCraftPage:
    def test_made_summary_and_units(self, client):
        craft = CraftFactory(
            maker_credit="Ayşe",
            year_made=1990,
            year_is_approximate=True,
            height=Decimal("10"),
            width=Decimal("4"),
            size_unit="in",
            weight=Decimal("2"),
            weight_unit="kg",
            traditional_measure="Two spans",
        )
        html = client.get(craft.get_absolute_url()).content.decode()
        for text in (
            "Made by",
            "Ayşe",
            "c. 1990",
            "10 × 4 in",
            "≈ 25.4 × 10.2 cm",
            "2 kg",
            "≈ 4.4 lb",
            "Two spans",
        ):
            assert text in html, text

    def test_hidden_location_never_reaches_the_page(self, client):
        craft = CraftFactory(
            place_name="Secret valley",
            latitude=Decimal("12.345678"),
            longitude=Decimal("45.678901"),
            location_precision="hidden",
        )
        html = client.get(craft.get_absolute_url()).content.decode()
        assert "Secret valley" in html
        assert "12.34" not in html and "45.67" not in html
        assert "kept private" in html

    def test_approximate_location_is_rounded(self, client):
        craft = CraftFactory(
            latitude=Decimal("12.345678"),
            longitude=Decimal("45.678901"),
            location_precision="approximate",
        )
        html = client.get(craft.get_absolute_url()).content.decode()
        assert 'data-lat="12.3"' in html and 'data-lng="45.7"' in html
        assert "12.345" not in html
