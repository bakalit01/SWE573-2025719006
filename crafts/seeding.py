"""Helpers shared by the seed commands."""

from . import sample_data
from .models import AttributeDefinition, CraftType


def ensure_craft_types():
    """Create/update the craft types and their attribute definitions; return {slug: type}."""
    types = {}
    for t in sample_data.CRAFT_TYPES:
        craft_type, _ = CraftType.objects.update_or_create(
            slug=t["slug"], defaults={"name": t["name"], "description": t["description"]}
        )
        types[t["slug"]] = craft_type
        keys = []
        for order, (key, label, data_type, unit, options) in enumerate(t["attributes"]):
            keys.append(key)
            AttributeDefinition.objects.update_or_create(
                craft_type=craft_type,
                key=key,
                defaults={
                    "label": label,
                    "data_type": data_type,
                    "unit": unit,
                    "options": options,
                    "order": order,
                    "is_active": True,
                },
            )
        # Fields dropped from the schema are retired, never deleted (data is kept).
        craft_type.attributes.exclude(key__in=keys).update(is_active=False)
    return types
