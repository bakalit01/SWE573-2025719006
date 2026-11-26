"""Is accent-insensitive search available? (US-10)

Search uses PostgreSQL's `unaccent` extension, enabled by migration 0009. If a database
couldn't enable it, search still works, matching accents exactly.
"""

from functools import cache

from django.db import connection


@cache
def has_unaccent():
    if connection.vendor != "postgresql":
        return False
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'unaccent'")
        return cursor.fetchone() is not None


def contains_lookup():
    return "unaccent__icontains" if has_unaccent() else "icontains"
