"""Materials and techniques get per-craft detail (FB-02); region becomes place name (FB-01).

Django can't add `through=` to an existing ManyToManyField, so the links are copied into the
new CraftMaterial / CraftTechnique tables before the old fields are replaced.
"""

import django.db.models.deletion
from django.db import migrations, models


def copy_links(apps, schema_editor):
    Craft = apps.get_model("crafts", "Craft")
    CraftMaterial = apps.get_model("crafts", "CraftMaterial")
    CraftTechnique = apps.get_model("crafts", "CraftTechnique")
    for craft in Craft.objects.all():
        for i, material in enumerate(craft.materials.all()):
            CraftMaterial.objects.create(craft=craft, material=material, order=i)
        for i, technique in enumerate(craft.techniques.all()):
            CraftTechnique.objects.create(craft=craft, technique=technique, order=i)


def copy_links_back(apps, schema_editor):
    Craft = apps.get_model("crafts", "Craft")
    CraftMaterial = apps.get_model("crafts", "CraftMaterial")
    CraftTechnique = apps.get_model("crafts", "CraftTechnique")
    for craft in Craft.objects.all():
        craft.materials.set(
            [cm.material for cm in CraftMaterial.objects.filter(craft=craft)]
        )
        craft.techniques.set(
            [ct.technique for ct in CraftTechnique.objects.filter(craft=craft)]
        )


class Migration(migrations.Migration):
    dependencies = [("crafts", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="material",
            name="description",
            field=models.TextField(blank=True, help_text="Short general explanation (glossary)"),
        ),
        migrations.AddField(
            model_name="technique",
            name="description",
            field=models.TextField(blank=True, help_text="Short general explanation (glossary)"),
        ),
        migrations.CreateModel(
            name="CraftMaterial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("origin", models.CharField(blank=True, max_length=200,
                                            help_text="Where it comes from, e.g. 'mined near Eskişehir'")),
                ("notes", models.CharField(blank=True, max_length=400,
                                           help_text="How it is used or prepared in this craft")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("craft", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name="craft_materials", to="crafts.craft")),
                ("material", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                               to="crafts.material")),
            ],
            options={
                "ordering": ["order", "id"],
                "constraints": [models.UniqueConstraint(fields=("craft", "material"),
                                                        name="unique_craft_material")],
            },
        ),
        migrations.CreateModel(
            name="CraftTechnique",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("notes", models.CharField(blank=True, max_length=400)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("craft", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name="craft_techniques", to="crafts.craft")),
                ("technique", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                                to="crafts.technique")),
            ],
            options={
                "ordering": ["order", "id"],
                "constraints": [models.UniqueConstraint(fields=("craft", "technique"),
                                                        name="unique_craft_technique")],
            },
        ),
        migrations.RunPython(copy_links, copy_links_back),
        migrations.RemoveField(model_name="craft", name="materials"),
        migrations.RemoveField(model_name="craft", name="techniques"),
        migrations.AddField(
            model_name="craft",
            name="materials",
            field=models.ManyToManyField(blank=True, related_name="crafts",
                                         through="crafts.CraftMaterial", to="crafts.material"),
        ),
        migrations.AddField(
            model_name="craft",
            name="techniques",
            field=models.ManyToManyField(blank=True, related_name="crafts",
                                         through="crafts.CraftTechnique", to="crafts.technique"),
        ),
        migrations.RenameField(model_name="craft", old_name="region", new_name="place_name"),
    ]
