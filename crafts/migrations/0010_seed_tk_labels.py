"""Load the managed list of TK / BC labels (US-26); the list is in crafts/tk_labels_data.py."""

from django.db import migrations

from crafts.tk_labels_data import BC, BC_LABELS, TK, TK_LABELS


def seed(apps, schema_editor):
    TKLabel = apps.get_model("crafts", "TKLabel")
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


def unseed(apps, schema_editor):
    TKLabel = apps.get_model("crafts", "TKLabel")
    names = [name for _, name, _, _ in TK_LABELS + BC_LABELS]
    TKLabel.objects.filter(name__in=names, crafts__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [("crafts", "0009_names_labels_sensitive_photos")]

    operations = [migrations.RunPython(seed, unseed)]
