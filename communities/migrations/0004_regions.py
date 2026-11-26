"""Regions become managed terms (US-28): each distinct region text becomes one Region."""

import django.db.models.deletion
from django.db import migrations, models


def text_to_regions(apps, schema_editor):
    Community = apps.get_model("communities", "Community")
    Region = apps.get_model("communities", "Region")
    by_key = {}
    for community in Community.objects.exclude(region_text=""):
        name = " ".join(community.region_text.split())[:200]
        if not name:
            continue
        region = by_key.get(name.casefold())
        if region is None:
            region = Region.objects.create(name=name)
            by_key[name.casefold()] = region
        community.region = region
        community.save(update_fields=["region"])


def regions_to_text(apps, schema_editor):
    Community = apps.get_model("communities", "Community")
    for community in Community.objects.exclude(region=None).select_related("region"):
        community.region_text = community.region.name
        community.save(update_fields=["region_text"])


class Migration(migrations.Migration):
    dependencies = [("communities", "0003_community_stewards")]

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                (
                    "other_names",
                    models.CharField(
                        blank=True,
                        help_text="Comma-separated; search finds the region by these too",
                        max_length=300,
                        verbose_name="Other names or spellings",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.RenameField("community", "region", "region_text"),
        migrations.AddField(
            model_name="community",
            name="region",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="communities",
                to="communities.region",
            ),
        ),
        migrations.RunPython(text_to_regions, regions_to_text),
        migrations.RemoveField("community", "region_text"),
    ]
