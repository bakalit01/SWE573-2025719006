"""Helpers shared by the seed commands."""

from . import sample_data
from .models import AttributeDefinition, CraftType, TKLabel
from .tk_labels_data import BC, BC_LABELS, TK, TK_LABELS


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


def ensure_tk_labels():
    """Add any missing label of the managed TK / BC list (US-26). Labels admins edited or
    retired are left as they are."""
    for kind, url, labels in (("tk", TK, TK_LABELS), ("bc", BC, BC_LABELS)):
        for order, (code, name, category, description) in enumerate(labels):
            TKLabel.objects.get_or_create(
                name=name,
                defaults={
                    "code": code,
                    "kind": kind,
                    "category": category,
                    "description": description,
                    "url": url,
                    "order": order,
                },
            )
