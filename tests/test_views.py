import pytest
from django.urls import reverse

from crafts.models import Craft

from .factories import CraftFactory, CraftTypeFactory

pytestmark = pytest.mark.django_db


def test_health_check(client):
    assert client.get("/healthz").content == b"ok"


def test_home_lists_public_crafts(client):
    craft = CraftFactory(title="Coiled basket")
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert craft.title in response.content.decode()


class TestCatalogue:
    def test_lists_only_visible_crafts(self, client):
        CraftFactory(title="Open record")
        CraftFactory(title="Members record", visibility=Craft.Visibility.MEMBERS)
        CraftFactory(title="Draft record", status=Craft.Status.DRAFT)
        html = client.get(reverse("crafts:list")).content.decode()
        assert "Open record" in html
        assert "Members record" not in html
        assert "Draft record" not in html

    def test_member_sees_members_only_records(self, member_client):
        CraftFactory(title="Members record", visibility=Craft.Visibility.MEMBERS)
        assert "Members record" in member_client.get(reverse("crafts:list")).content.decode()

    def test_filter_by_craft_type(self, client):
        pottery = CraftTypeFactory(name="Pottery", slug="pottery")
        CraftFactory(title="Clay jar", craft_type=pottery)
        CraftFactory(title="Woven sash")
        html = client.get(reverse("crafts:list"), {"type": "pottery"}).content.decode()
        assert "Clay jar" in html
        assert "Woven sash" not in html

    def test_pagination_24_per_page(self, client):
        craft_type = CraftTypeFactory()
        for i in range(30):
            CraftFactory(title=f"Item {i:02d}", craft_type=craft_type)
        response = client.get(reverse("crafts:list"))
        assert len(response.context["crafts"]) == 24
        assert len(client.get(reverse("crafts:list"), {"page": 2}).context["crafts"]) == 6

    def test_sample_records_are_labelled(self, client):
        CraftFactory(is_sample=True)
        assert "Sample data" in client.get(reverse("crafts:list")).content.decode()


class TestDetail:
    def test_shows_credits_and_report_link(self, client):
        craft = CraftFactory(maker_credit="Maker Name")
        html = client.get(craft.get_absolute_url()).content.decode()
        assert "Maker Name" in html
        assert craft.community.name in html
        assert "Report or request removal" in html

    @pytest.mark.parametrize(
        "visibility",
        [Craft.Visibility.MEMBERS, Craft.Visibility.COMMUNITY, Craft.Visibility.RESTRICTED],
    )
    def test_hidden_records_are_not_found_for_visitors(self, client, visibility):
        craft = CraftFactory(visibility=visibility)
        assert client.get(craft.get_absolute_url()).status_code == 404

    def test_members_only_visible_after_login(self, member_client):
        craft = CraftFactory(visibility=Craft.Visibility.MEMBERS)
        assert member_client.get(craft.get_absolute_url()).status_code == 200

    def test_unknown_slug_is_404(self, client):
        assert client.get(reverse("crafts:detail", args=["nope"])).status_code == 404
