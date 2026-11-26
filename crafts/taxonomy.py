"""Merge duplicate terms without losing their links to crafts (US-28).

`merge(keep, others)` moves every link from the duplicates to the term that is kept, records
the duplicates' names as alternate spellings of it (so search still finds them), and then
deletes the duplicates. Works for materials, techniques, communities, regions and tags.
"""

from django.db import transaction

from accounts.models import User
from communities.models import Community, Region

from .models import Craft, CraftMaterial, CraftTechnique, Material, Tag, Technique
from .terms import join_names, split_names


def _move_links(link_model, field, keep, others, detail_fields):
    """Point craft links at `keep`; where a craft already links to it, keep one row and fill
    its empty details from the duplicate's."""
    moved = 0
    for row in link_model.objects.filter(**{f"{field}__in": others}).order_by("pk"):
        existing = link_model.objects.filter(craft=row.craft, **{field: keep}).first()
        if existing:
            for name in detail_fields:
                if not getattr(existing, name) and getattr(row, name):
                    setattr(existing, name, getattr(row, name))
            existing.save()
            row.delete()
        else:
            setattr(row, field, keep)
            row.save(update_fields=[field])
        moved += 1
    return moved


def link_count(term):
    """How many crafts (or, for a region, communities) use a term."""
    if isinstance(term, Region):
        return term.communities.count()
    return term.crafts.count()


@transaction.atomic
def merge(keep, others):
    """Merge `others` into `keep`; returns how many links were moved."""
    others = [o for o in others if o.pk != keep.pk and type(o) is type(keep)]
    if not others:
        return 0
    if isinstance(keep, Material):
        moved = _move_links(CraftMaterial, "material", keep, others, ["origin", "notes"])
    elif isinstance(keep, Technique):
        moved = _move_links(CraftTechnique, "technique", keep, others, ["notes"])
    elif isinstance(keep, Community):
        moved = Craft.objects.filter(community__in=others).update(community=keep)
        User.objects.filter(community__in=others).update(community=keep)
        for other in others:
            keep.stewards.add(*other.stewards.all())
            keep.description = keep.description or other.description
            keep.region = keep.region or other.region
    elif isinstance(keep, Region):
        moved = Community.objects.filter(region__in=others).update(region=keep)
    elif isinstance(keep, Tag):
        moved = 0
        for craft in Craft.objects.filter(tags__in=others).distinct():
            craft.tags.add(keep)
            moved += 1
    else:
        raise TypeError(f"Can't merge {type(keep).__name__}")
    if hasattr(keep, "other_names"):
        names = split_names(keep.other_names)
        for other in others:
            names += [other.name, *split_names(other.other_names)]
        keep.other_names = join_names(names, exclude=[keep.name])[:300]
    keep.save()
    for other in others:
        other.delete()
    return moved
