from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from communities.models import Community
from crafts import sample_data as data
from crafts.models import (
    Craft,
    CraftMaterial,
    CraftTechnique,
    Material,
    Media,
    Technique,
)
from crafts.seeding import ensure_craft_types


def _dec(value):
    return None if value is None else Decimal(str(value))


class Command(BaseCommand):
    help = "Create or update the fictional sample crafts (safe to run repeatedly)."

    @transaction.atomic
    def handle(self, *args, **options):
        communities = {}
        for c in data.COMMUNITIES:
            communities[c["slug"]], _ = Community.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                    "region": c["region"],
                    "description": c["description"],
                    "is_sample": True,
                },
            )

        types = ensure_craft_types()

        for (
            slug,
            title,
            type_slug,
            community_slug,
            visibility,
            materials,
            techniques,
            attributes,
            summary,
        ) in data.CRAFTS:
            community = communities[community_slug]
            extra = data.DETAILS.get(slug, {})
            place_name, country, lat, lng = extra.get("place", ("", "", None, None))
            height, width, depth, size_unit = extra.get("size", (None, None, None, ""))
            weight, weight_unit = extra.get("weight", (None, ""))
            craft, _ = Craft.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "summary": summary,
                    "description": data.DESCRIPTION.format(summary=summary),
                    "process": extra.get("process", ""),
                    "cultural_context": data.CULTURAL_CONTEXT,
                    "craft_type": types[type_slug],
                    "community": community,
                    "maker_credit": "Sample maker (fictional)",
                    "year_made": extra.get("year_made"),
                    "year_is_approximate": extra.get("year_is_approximate", False),
                    "period": "",
                    "place_name": place_name or community.region,
                    "country": country,
                    "latitude": _dec(lat),
                    "longitude": _dec(lng),
                    "location_precision": extra.get("precision", "approximate"),
                    "height": _dec(height),
                    "width": _dec(width),
                    "depth": _dec(depth),
                    "size_unit": size_unit,
                    "weight": _dec(weight),
                    "weight_unit": weight_unit,
                    "traditional_measure": extra.get("traditional_measure", ""),
                    "attributes": attributes,
                    "visibility": visibility,
                    "status": Craft.Status.PUBLISHED,
                    "is_sample": True,
                },
            )

            material_rows = extra.get("materials") or [(m, "", "") for m in materials]
            craft.craft_materials.all().delete()
            for order, (name, origin, notes) in enumerate(material_rows):
                CraftMaterial.objects.create(
                    craft=craft,
                    material=Material.objects.get_or_create(name=name)[0],
                    origin=origin,
                    notes=notes,
                    order=order,
                )
            technique_rows = extra.get("techniques") or [(t, "") for t in techniques]
            craft.craft_techniques.all().delete()
            for order, (name, notes) in enumerate(technique_rows):
                CraftTechnique.objects.create(
                    craft=craft,
                    technique=Technique.objects.get_or_create(name=name)[0],
                    notes=notes,
                    order=order,
                )

            Media.objects.update_or_create(
                craft=craft,
                order=0,
                defaults={
                    "static_path": f"img/samples/{type_slug}-{slug.removeprefix('sample-')}.svg",
                    "alt_text": f"Sample illustration: abstract pattern for {title.lower()}",
                    "caption": "Sample illustration",
                    "credit": "Generated pattern, not a photograph",
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample data ready: {len(data.CRAFTS)} crafts, {len(data.CRAFT_TYPES)} craft "
                f"types, {len(data.COMMUNITIES)} communities."
            )
        )
