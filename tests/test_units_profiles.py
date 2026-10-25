"""Units (FB-04), profiles (US-04) and password reset (US-03)."""

from decimal import Decimal

import pytest
from django.core import mail
from django.urls import reverse

from crafts import units
from crafts.models import Craft

from .factories import CommunityFactory, CraftFactory, UserFactory


class TestUnits:
    def test_metric_size_converts_to_inches(self):
        size = units.describe_size(Decimal("24"), Decimal("18"), Decimal("9"), "cm")
        assert size == {
            "original": "24 × 18 × 9 cm",
            "axes": "H × W × D",
            "converted": "≈ 9.4 × 7.1 × 3.5 in",
        }

    def test_imperial_size_converts_to_cm_and_skips_missing_axes(self):
        size = units.describe_size(None, Decimal("2"), Decimal("1.5"), "ft")
        assert size == {"original": "2 × 1.5 ft", "axes": "W × D", "converted": "≈ 61 × 45.7 cm"}

    def test_no_size_without_values_or_unit(self):
        assert units.describe_size(None, None, None, "cm") is None
        assert units.describe_size(Decimal("3"), None, None, "") is None

    @pytest.mark.parametrize(
        ("weight", "unit", "converted"),
        [
            ("250", "g", "≈ 8.8 oz"),
            ("2", "kg", "≈ 4.4 lb"),
            ("3", "lb", "≈ 1.4 kg"),
            ("4", "oz", "≈ 113 g"),
        ],
    )
    def test_weight(self, weight, unit, converted):
        assert units.describe_weight(Decimal(weight), unit)["converted"] == converted

    def test_fmt_trims_zeros(self):
        assert units.fmt(Decimal("24.00")) == "24"
        assert units.fmt(Decimal("1.50")) == "1.5"


@pytest.mark.django_db
class TestProfiles:
    def test_public_profile_lists_published_crafts(self, client):
        maker = UserFactory(display_name="Ayşe K.", bio="Weaver.", community=CommunityFactory())
        CraftFactory(title="Public rug", created_by=maker)
        CraftFactory(title="Draft rug", created_by=maker, status=Craft.Status.DRAFT)
        html = client.get(maker.get_absolute_url()).content.decode()
        assert "Ayşe K." in html and "Weaver." in html and maker.community.name in html
        assert "Public rug" in html and "Draft rug" not in html

    def test_edit_profile(self, member_client, user):
        community = CommunityFactory()
        response = member_client.post(
            reverse("accounts:edit_profile"),
            {
                "display_name": "New Name",
                "bio": "Hello",
                "community": community.pk,
                "location": "Ankara",
            },
        )
        assert response.url == user.get_absolute_url()
        user.refresh_from_db()
        assert (user.display_name, user.community, user.location) == (
            "New Name",
            community,
            "Ankara",
        )

    def test_edit_profile_requires_login(self, client):
        assert client.get(reverse("accounts:edit_profile")).status_code == 302

    def test_added_by_links_to_profile(self, client, user):
        craft = CraftFactory(created_by=user)
        html = client.get(craft.get_absolute_url()).content.decode()
        assert user.get_absolute_url() in html


@pytest.mark.django_db
class TestPasswordReset:
    def test_login_page_links_to_reset(self, client):
        html = client.get(reverse("account_login")).content.decode()
        assert reverse("account_reset_password") in html

    def test_reset_email_is_sent_and_link_works(self, client, user):
        client.post(reverse("account_reset_password"), {"email": user.email})
        assert len(mail.outbox) == 1
        link = next(w for w in mail.outbox[0].body.split() if "/password/reset/key/" in w)
        path = link.split("://", 1)[-1].split("/", 1)[1]
        response = client.get("/" + path, follow=True)
        assert response.status_code == 200
        assert 'name="password1"' in response.content.decode()

    def test_unknown_email_gives_no_hint(self, client, user):
        known = client.post(reverse("account_reset_password"), {"email": user.email}, follow=True)
        unknown = client.post(
            reverse("account_reset_password"), {"email": "nobody@example.com"}, follow=True
        )
        assert known.status_code == unknown.status_code == 200
        assert known.redirect_chain[-1][0] == unknown.redirect_chain[-1][0]
