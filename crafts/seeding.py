"""Helpers shared by the seed commands."""

from . import sample_data
from .models import AttributeDefinition, CraftType


def ensure_craft_types():
    """Create the starter craft types and their attribute definitions; return {slug: type}.

    Since US-13, admins manage craft types and fields in the admin, and the seed commands
    run on every start-up on Render. So this only adds what is missing: it never renames,
    reorders, retires or re-activates a type or field an admin has edited.
    """
    types = {}
    for t in sample_data.CRAFT_TYPES:
        craft_type, _ = CraftType.objects.get_or_create(
            slug=t["slug"], defaults={"name": t["name"], "description": t["description"]}
        )
        types[t["slug"]] = craft_type
        for order, (key, label, data_type, unit, options) in enumerate(t["attributes"]):
            AttributeDefinition.objects.get_or_create(
                craft_type=craft_type,
                key=key,
                defaults={
                    "label": label,
                    "data_type": data_type,
                    "unit": unit,
                    "options": options,
                    "order": order,
                },
            )
    return types
