"""US-10: a craft's names in several languages; the community's own name is shown first."""

import unicodedata

import pytest
from django.db import IntegrityError, transaction
from django.urls import reverse

from crafts.models import Craft, CraftName

from .factories import CommunityFactory, CraftFactory
from .test_contribute import payload

pytestmark = pytest.mark.django_db


def names(rows):
    """Form data for the "Names in other languages" rows."""
    data = {
        "nam-TOTAL_FORMS": str(len(rows)),
        "nam-INITIAL_FORMS": "0",
        "nam-MIN_NUM_FORMS": "1",
        "nam-MAX_NUM_FORMS": "12",
    }
    for i, (name, language, code, primary) in enumerate(rows):
        data |= {f"nam-{i}-name": name, f"nam-{i}-language": language, f"nam-{i}-lang_code": code}
        if primary:
            data[f"nam-{i}-is_primary"] = "on"
    return data


def titles(client, q):
    return [c.title for c in client.get(reverse("crafts:list"), {"q": q}).context["crafts"]]


class TestForm:
    def test_names_are_saved_and_the_primary_one_is_shown_first(self, member_client, setup):
        rows = [("Lüle", "Turkish", "tr", False), ("ʔəʔamɩn", "ɬaʔamɩn", "", True)]
        member_client.post(reverse("crafts:create"), payload(setup, **names(rows)))
        craft = Craft.objects.get(title="Carved pipe")
        assert [(n.name, n.is_primary) for n in craft.names.all()] == [
            ("ʔəʔamɩn", True),
            ("Lüle", False),
        ]
        html = member_client.get(craft.get_absolute_url()).content.decode()
        h1 = html.split("<h1>", 1)[1].split("</h1>", 1)[0]
        assert h1.index("ʔəʔamɩn") < h1.index("Carved pipe")
        assert '<span lang="tr">Lüle</span> <span class="muted">(Turkish)</span>' in html

    def test_only_one_name_can_be_shown_first(self, member_client, setup):
        rows = [("A", "Language A", "", True), ("B", "Language B", "", True)]
        response = member_client.post(reverse("crafts:create"), payload(setup, **names(rows)))
        assert response.status_code == 200
        assert "Choose only one name to show first." in response.content.decode()
        assert not Craft.objects.exists()

    def test_a_name_needs_its_language(self, member_client, setup):
        response = member_client.post(
            reverse("crafts:create"), payload(setup, **names([("Lüle", "", "", False)]))
        )
        assert "Say which language this name is in." in response.content.decode()

    def test_language_code_is_checked(self, member_client, setup):
        rows = [("Lüle", "Turkish", "not a code", False)]
        response = member_client.post(reverse("crafts:create"), payload(setup, **names(rows)))
        assert "Use a language code such as" in response.content.decode()

    def test_editing_replaces_the_names_and_shows_them_in_the_form(self, member_client, setup):
        member_client.post(
            reverse("crafts:create"), payload(setup, **names([("Old", "Turkish", "", True)]))
        )
        craft = Craft.objects.get()
        edit = reverse("crafts:edit", args=[craft.slug])
        assert 'value="Old"' in member_client.get(edit).content.decode()
        member_client.post(edit, payload(setup, **names([("Lüle", "Turkish", "tr", False)])))
        assert [n.name for n in craft.names.all()] == ["Lüle"]

    def test_a_form_without_name_rows_keeps_the_names(self, member_client, setup):
        """e.g. a page opened before this feature was deployed."""
        member_client.post(
            reverse("crafts:create"), payload(setup, **names([("Lüle", "Turkish", "", True)]))
        )
        craft = Craft.objects.get()
        member_client.post(reverse("crafts:edit", args=[craft.slug]), payload(setup))
        assert [n.name for n in craft.names.all()] == ["Lüle"]


def test_one_primary_name_per_craft_in_the_database():
    craft = CraftFactory()
    CraftName.objects.create(craft=craft, name="A", language="X", is_primary=True)
    with pytest.raises(IntegrityError), transaction.atomic():
        CraftName.objects.create(craft=craft, name="B", language="Y", is_primary=True)


def test_names_are_stored_in_one_unicode_form():
    decomposed = unicodedata.normalize("NFD", "Diyogí")
    name = CraftName.objects.create(craft=CraftFactory(), name=decomposed, language="Diné")
    assert name.name == unicodedata.normalize("NFC", "Diyogí") and name.name != decomposed


class TestSearch:
    @pytest.fixture
    def crafts(self):
        masks = CraftFactory(title="Hahoe masks")
        CraftName.objects.create(
            craft=masks, name="하회탈", language="Korean", lang_code="ko", is_primary=True
        )
        tent = CraftFactory(title="Yörük black tent", community=CommunityFactory(name="Yörük"))
        CraftName.objects.create(craft=tent, name="kara çadır", language="Turkish")
        carpet = CraftFactory(title="Döşemealtı carpet")
        return {"masks": masks, "tent": tent, "carpet": carpet}

    def test_finds_a_craft_by_any_of_its_names(self, client, crafts):
        assert titles(client, "하회탈") == ["Hahoe masks"]
        assert titles(client, "kara çadır") == ["Yörük black tent"]
        assert titles(client, "korean") == ["Hahoe masks"]  # the language too

    def test_ignores_accents_and_special_letters(self, client, crafts):
        assert titles(client, "dosemealti") == ["Döşemealtı carpet"]
        assert titles(client, "kara cadir") == ["Yörük black tent"]
        assert titles(client, "YORUK") == ["Yörük black tent"]

    def test_search_still_works_without_unaccent(self, client, crafts, monkeypatch):
        """If a database couldn't enable the extension, search matches accents exactly."""
        monkeypatch.setattr("crafts.views.contains_lookup", lambda: "icontains")
        assert titles(client, "döşemealtı") == ["Döşemealtı carpet"]
        assert titles(client, "dosemealti") == []

    def test_query_typed_in_another_unicode_form_matches(self, client, crafts):
        assert titles(client, unicodedata.normalize("NFD", "Döşemealtı")) == ["Döşemealtı carpet"]


def test_cards_show_the_primary_name_first(client):
    craft = CraftFactory(title="Ainu attus robe")
    CraftName.objects.create(
        craft=craft, name="attus", language="Ainu", lang_code="ain", is_primary=True
    )
    html = client.get(reverse("crafts:list")).content.decode()
    assert (
        '<h3 class="card-title"><span lang="ain">attus</span> '
        '<span class="card-subtitle">Ainu attus robe</span></h3>'
    ) in html
