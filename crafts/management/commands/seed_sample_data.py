from django.core.management.base import BaseCommand
from django.db import transaction

from communities.models import Community
from crafts import sample_data as data
from crafts.models import AttributeDefinition, Craft, CraftType, Material, Media, Technique


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

        types = {}
        for t in data.CRAFT_TYPES:
            craft_type, _ = CraftType.objects.update_or_create(
                slug=t["slug"], defaults={"name": t["name"], "description": t["description"]}
            )
            types[t["slug"]] = craft_type
            for order, (key, label, data_type, unit, options) in enumerate(t["attributes"]):
                AttributeDefinition.objects.update_or_create(
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
            craft, _ = Craft.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "summary": summary,
                    "description": data.DESCRIPTION.format(summary=summary),
                    "cultural_context": data.CULTURAL_CONTEXT,
                    "craft_type": types[type_slug],
                    "community": community,
                    "region": community.region,
                    "maker_credit": "Sample maker (fictional)",
                    "period": "Sample record",
                    "attributes": attributes,
                    "visibility": visibility,
                    "status": Craft.Status.PUBLISHED,
                    "is_sample": True,
                },
            )
            craft.materials.set([Material.objects.get_or_create(name=m)[0] for m in materials])
            craft.techniques.set([Technique.objects.get_or_create(name=t)[0] for t in techniques])
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
