from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from communities.models import Community
from crafts import reference_data as data
from crafts.models import Craft, CraftMaterial, CraftTechnique, Material, Media, Technique
from crafts.seeding import ensure_craft_types

COMMUNITY_NOTE = (
    "Records about this community are compiled from public sources such as museums and "
    "encyclopedias. Community members can ask for any record to be corrected or removed."
)


def _dec(value):
    return None if value is None else Decimal(str(value))


class Command(BaseCommand):
    help = "Create or update real-world reference crafts from public sources (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace-samples",
            action="store_true",
            help="Delete the fictional sample crafts and sample communities.",
        )

    @transaction.atomic
    def handle(self, *args, replace_samples=False, **options):
        if replace_samples:
            removed, _ = Craft.objects.filter(is_sample=True).delete()
            Community.objects.filter(is_sample=True, crafts__isnull=True).delete()
            self.stdout.write(f"Removed sample records ({removed} rows).")

        types = ensure_craft_types()
        communities = {}
        for slug, name, region in data.COMMUNITIES:
            communities[slug], _ = Community.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "region": region,
                    "description": COMMUNITY_NOTE,
                    "is_sample": False,
                },
            )

        for record in data.CRAFTS:
            place_name, country, lat, lng = record["place"]
            craft, _ = Craft.objects.update_or_create(
                slug=record["slug"],
                defaults={
                    "title": record["title"],
                    "summary": record["summary"],
                    "description": record["description"],
                    "process": record["process"],
                    "cultural_context": record["cultural_context"],
                    "craft_type": types[record["type"]],
                    "community": communities[record["community"]],
                    "maker_credit": record["maker"],
                    "year_made": record.get("year"),
                    "year_is_approximate": False,
                    "period": record.get("period", ""),
                    "place_name": place_name,
                    "country": country,
                    "latitude": _dec(lat),
                    "longitude": _dec(lng),
                    "location_precision": Craft.LocationPrecision.APPROXIMATE,
                    "attributes": record["attributes"],
                    "visibility": Craft.Visibility.PUBLIC,
                    "status": Craft.Status.PUBLISHED,
                    "is_sample": False,
                    "is_reference": True,
                    "sources": "\n".join(f"{t} | {u}" for t, u in record["sources"]),
                },
            )

            craft.craft_materials.all().delete()
            for order, (name, origin, notes) in enumerate(record["materials"]):
                CraftMaterial.objects.create(
                    craft=craft,
                    material=Material.objects.get_or_create(name=name)[0],
                    origin=origin,
                    notes=notes,
                    order=order,
                )
            craft.craft_techniques.all().delete()
            for order, (name, notes) in enumerate(record["techniques"]):
                CraftTechnique.objects.create(
                    craft=craft,
                    technique=Technique.objects.get_or_create(name=name)[0],
                    notes=notes,
                    order=order,
                )

            craft.media.filter(image="").delete()  # keep any photos users uploaded
            for order, (file_name, alt, caption, credit) in enumerate(record["images"]):
                Media.objects.create(
                    craft=craft,
                    commons_file=file_name,
                    alt_text=alt,
                    caption=caption,
                    credit=credit or "Wikimedia Commons",
                    order=order,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Reference crafts ready: {len(data.CRAFTS)} crafts, "
                f"{len(data.COMMUNITIES)} communities."
            )
        )
