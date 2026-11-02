"""Search by location."""

from decimal import Decimal

import pytest
from django.urls import reverse

from crafts import geo
from crafts.models import Craft

from .factories import CommunityFactory, CraftFactory

pytestmark = pytest.mark.django_db
P = Craft.LocationPrecision


def at(title, lat, lng, precision=P.EXACT, **extra):
    return CraftFactory(
        title=title,
        latitude=Decimal(str(lat)),
        longitude=Decimal(str(lng)),
        location_precision=precision,
        **extra,
    )


@pytest.fixture
def places():
    at("Antalya kilim", 36.89, 30.70, place_name="Antalya", country="Türkiye")
    at("Konya felt", 37.87, 32.48, place_name="Konya", country="Türkiye")
    at("Hidden place", 36.90, 30.71, P.HIDDEN, country="Türkiye")
    at("Approximate pot", 36.94, 30.84, P.APPROXIMATE)
    at("Lima textile", -12.05, -77.04, place_name="Lima", country="Peru")
    CraftFactory(title="No location", community=CommunityFactory(region="Antalya coast"))


def titles(client, **params):
    return [c.title for c in client.get(reverse("crafts:list"), params).context["crafts"]]


def test_distance():
    assert round(geo.distance_km(36.89, 30.70, 37.87, 32.48)) == 191  # Antalya–Konya


def test_within_distance_nearest_first(client, places):
    near_antalya = {"lat": "36.89", "lng": "30.70", "place": "Antalya"}
    assert titles(client, km=50, **near_antalya) == ["Antalya kilim", "Approximate pot"]
    assert titles(client, km=250, **near_antalya) == [
        "Antalya kilim",
        "Approximate pot",
        "Konya felt",
    ]


def test_hidden_places_never_found_by_location(client, places):
    assert "Hidden place" not in titles(client, lat="36.90", lng="30.71", km=25)


def test_approximate_places_use_the_rounded_point(client, places):
    # The pot's real point is ~1.5 km from here, but only its rounded point (36.9, 30.8),
    # about 4 km away, is published; a tight search must not find it by its real point.
    page = client.get(reverse("crafts:list"), {"lat": "36.94", "lng": "30.84", "km": 25})
    pot = next(c for c in page.context["crafts"] if c.title == "Approximate pot")
    assert pot.distance_km == pytest.approx(geo.distance_km(36.94, 30.84, 36.9, 30.8))
    assert "(approximate)" in page.content.decode()


def test_cards_show_distance_and_map_data(client, places):
    html = client.get(
        reverse("crafts:list"), {"lat": "36.89", "lng": "30.70", "km": 250, "place": "Antalya"}
    ).content.decode()
    assert "≈ 191 km away" in html and 'id="map-points"' in html
    assert "Showing crafts within 250 km of Antalya" in html
    assert "Hidden place" not in html.split('id="map-points"')[1]


def test_place_text_without_coordinates_matches_names(client, places):
    assert titles(client, place="Antalya") == ["Antalya kilim", "No location"]
    assert titles(client, place="Peru") == ["Lima textile"]


def test_location_combines_with_other_filters(client, places):
    assert titles(client, lat="36.89", lng="30.70", km=1000, q="felt") == ["Konya felt"]


@pytest.mark.parametrize("params", [{"lat": "abc", "lng": "1"}, {"lat": "95", "lng": "0"}])
def test_bad_coordinates_are_ignored(client, places, params):
    assert len(titles(client, **params)) == 6  # every craft listed, no error


def test_unknown_distance_falls_back_to_default(client, places):
    response = client.get(reverse("crafts:list"), {"lat": "0", "lng": "0", "km": "7"})
    assert response.context["km"] == geo.DEFAULT_KM
