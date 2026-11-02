"""Search by location: crafts within a distance of a point.

Distances use only the coordinates a craft *publishes* (Craft.map_point): exact points,
approximate ones rounded to about 10 km, and nothing for hidden places, so a location
search can never reveal more than the craft page shows.
"""

from math import asin, cos, radians, sin, sqrt

DISTANCES_KM = [25, 50, 100, 250, 500, 1000, 2500]
DEFAULT_KM = 250


def distance_km(lat1, lng1, lat2, lng2):
    """Great-circle distance (haversine), in km."""
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lng2 - lng1) / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(a))


def parse_point(lat, lng):
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return None
    if -90 <= lat <= 90 and -180 <= lng <= 180:
        return lat, lng
    return None


def parse_km(value):
    try:
        km = int(value)
    except (TypeError, ValueError):
        return DEFAULT_KM
    return km if km in DISTANCES_KM else DEFAULT_KM


def distances_within(crafts, point, km):
    """{craft pk: km} for crafts whose published point lies within `km` of `point`."""
    from .models import Craft

    found = {}
    rows = crafts.exclude(latitude=None).exclude(location_precision=Craft.LocationPrecision.HIDDEN)
    rows = rows.select_related(None).prefetch_related(None)
    for craft in rows.only("pk", "latitude", "longitude", "location_precision"):
        shown = craft.map_point
        if shown:
            d = distance_km(point[0], point[1], shown["lat"], shown["lng"])
            if d <= km:
                found[craft.pk] = d
    return found
