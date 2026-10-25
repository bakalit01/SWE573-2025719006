"""Forms for adding and editing crafts (US-08, US-09, US-11, US-20 and feedback FB-01…FB-04)."""

import io
from decimal import Decimal

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image, ImageOps

from . import units
from .models import AttributeDefinition, Craft, CraftType

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_SIDE = 1600
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


class CraftForm(forms.ModelForm):
    """Core fields shared by every craft."""

    class Meta:
        model = Craft
        fields = [
            "title",
            "craft_type",
            "community",
            "summary",
            "maker_credit",
            "year_made",
            "year_is_approximate",
            "period",
            "place_name",
            "country",
            "latitude",
            "longitude",
            "location_precision",
            "process",
            "height",
            "width",
            "depth",
            "size_unit",
            "weight",
            "weight_unit",
            "traditional_measure",
            "description",
            "cultural_context",
            "visibility",
        ]
        labels = {
            "title": "Name",
            "summary": "One-line summary",
            "maker_credit": "Made by",
            "year_made": "Year made",
            "year_is_approximate": "The year is approximate (circa)",
            "period": "Or a period, if the year is unknown",
            "place_name": "Place",
            "location_precision": "How precisely to show the place",
            "process": "How it is made",
            "size_unit": "Unit",
            "weight_unit": "Unit",
            "description": "About this craft",
            "cultural_context": "Cultural context",
        }
        help_texts = {
            "maker_credit": "Name the makers, or the family or workshop. Required.",
            "summary": "Shown on cards and at the top of the page.",
            "process": "Describe the steps, from preparing materials to finishing.",
            "cultural_context": "How it is used, what it means, who may make or see it.",
            "traditional_measure": "Optional, e.g. 'two hand spans long' or '1 arşın'.",
        }
        widgets = {
            "summary": forms.TextInput(attrs={"maxlength": 300}),
            "process": forms.Textarea(attrs={"rows": 4}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "cultural_context": forms.Textarea(attrs={"rows": 3}),
            "latitude": forms.NumberInput(attrs={"step": "any", "data-map-lat": ""}),
            "longitude": forms.NumberInput(attrs={"step": "any", "data-map-lng": ""}),
            "place_name": forms.TextInput(attrs={"data-map-place": "", "autocomplete": "off"}),
            "country": forms.TextInput(attrs={"data-map-country": ""}),
            "location_precision": forms.RadioSelect,
            "year_made": forms.NumberInput(
                attrs={"min": 1, "max": 9999, "placeholder": "e.g. 1998"}
            ),
            "craft_type": forms.Select(attrs={"data-craft-type": ""}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Community-only and restricted visibility arrive with steward review (M3).
        self.fields["visibility"].choices = [
            (Craft.Visibility.PUBLIC, "Public: anyone can see it"),
            (Craft.Visibility.MEMBERS, "Members only: signed-in users"),
        ]
        self.fields["visibility"].widget = forms.RadioSelect(
            choices=self.fields["visibility"].choices
        )
        self.fields["craft_type"].empty_label = "Choose a craft type"
        self.fields["community"].empty_label = "Choose a community"
        self.fields["size_unit"].choices = [("", "Choose unit")] + list(units.LENGTH_UNITS)
        self.fields["weight_unit"].choices = [("", "Choose unit")] + list(units.WEIGHT_UNITS)
        for name in ("height", "width", "depth", "weight"):
            self.fields[name].widget.attrs.update({"min": 0, "step": "any"})
        self.fields["latitude"].label = "Latitude"
        self.fields["longitude"].label = "Longitude"

    def save(self, commit=True):
        craft = super().save(commit=False)
        if not craft.slug:
            craft.slug = unique_slug(craft.title)
        if commit:
            craft.save()
        return craft


RESERVED_SLUGS = {"add", "mine", "fields"}


def unique_slug(title):
    base = slugify(title)[:200] or "craft"
    if base in RESERVED_SLUGS:
        base = f"{base}-craft"
    slug, n = base, 2
    while Craft.objects.filter(slug=slug).exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


# ---------- Craft-type-specific fields (US-11) ----------

YES_NO = [("", "Not recorded"), ("yes", "Yes"), ("no", "No")]


def field_for(definition: AttributeDefinition, initial=None):
    """Turn one AttributeDefinition row into a Django form field."""
    T = AttributeDefinition.DataType
    label = f"{definition.label} ({definition.unit})" if definition.unit else definition.label
    common = {"label": label, "required": definition.required, "help_text": definition.help_text}
    options = [(o, o) for o in (definition.options or [])]
    if definition.data_type == T.LONG_TEXT:
        return forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), **common)
    if definition.data_type == T.NUMBER:
        return forms.DecimalField(widget=forms.NumberInput(attrs={"step": "any"}), **common)
    if definition.data_type == T.CHOICE:
        return forms.ChoiceField(choices=[("", "—")] + options, **common)
    if definition.data_type == T.MULTI_CHOICE:
        return forms.MultipleChoiceField(
            choices=options, widget=forms.CheckboxSelectMultiple, **common
        )
    if definition.data_type == T.BOOLEAN:
        return forms.ChoiceField(choices=YES_NO, **common)
    if definition.data_type == T.URL:
        return forms.URLField(assume_scheme="https", **common)
    return forms.CharField(**common)


class AttributesForm(forms.Form):
    """Built at run time from the chosen craft type's attribute definitions."""

    prefix = "attr"

    def __init__(self, *args, craft_type=None, values=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.craft_type = craft_type
        self.definitions = list(craft_type.attributes.filter(is_active=True)) if craft_type else []
        values = values or {}
        for d in self.definitions:
            self.fields[d.key] = field_for(d)
            value = values.get(d.key)
            if d.data_type == AttributeDefinition.DataType.BOOLEAN and value is not None:
                value = "yes" if value else "no"
            if value not in (None, ""):
                self.initial[d.key] = value

    def json_values(self):
        """Cleaned values as JSON-safe data for Craft.attributes."""
        out = {}
        for d in self.definitions:
            value = self.cleaned_data.get(d.key)
            if value in (None, "", []):
                continue
            if isinstance(value, Decimal):
                value = int(value) if value == value.to_integral() else float(value)
            if d.data_type == AttributeDefinition.DataType.BOOLEAN:
                value = value == "yes"
            out[d.key] = value
        return out


# ---------- Materials and techniques with detail (FB-02) ----------


class MaterialRowForm(forms.Form):
    name = forms.CharField(
        label="Material",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"list": "material-options", "placeholder": "e.g. Wool"}),
    )
    origin = forms.CharField(
        label="Where it comes from",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. gathered on the riverbank"}),
    )
    notes = forms.CharField(
        label="How it is used or prepared",
        max_length=400,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. spun by hand, dyed with roots"}),
    )

    def clean(self):
        data = super().clean()
        if not data.get("name") and (data.get("origin") or data.get("notes")):
            self.add_error("name", "Name the material for this row.")
        return data


class TechniqueRowForm(forms.Form):
    name = forms.CharField(
        label="Technique",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"list": "technique-options", "placeholder": "e.g. Coiling"}),
    )
    notes = forms.CharField(
        label="How it is applied",
        max_length=400,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. coils pinched and scraped smooth"}),
    )

    def clean(self):
        data = super().clean()
        if not data.get("name") and data.get("notes"):
            self.add_error("name", "Name the technique for this row.")
        return data


class BaseRowFormSet(forms.BaseFormSet):
    def filled_rows(self):
        seen, rows = set(), []
        for form in self.forms:
            if not form.is_valid():
                continue
            name = (form.cleaned_data.get("name") or "").strip()
            if name and name.lower() not in seen:
                seen.add(name.lower())
                rows.append({**form.cleaned_data, "name": name})
        return rows


class MaterialFormSet(BaseRowFormSet):
    require_one = True  # drafts may be saved without materials; publishing needs one

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if self.require_one and not self.filled_rows():
            raise forms.ValidationError("Add at least one material.")


MaterialRows = forms.formset_factory(
    MaterialRowForm, formset=MaterialFormSet, extra=0, min_num=1, max_num=30
)
TechniqueRows = forms.formset_factory(
    TechniqueRowForm, formset=BaseRowFormSet, extra=0, min_num=1, max_num=30
)


# ---------- Images (US-20) ----------


class ImageRowForm(forms.Form):
    image = forms.ImageField(required=False, label="Photo")
    alt_text = forms.CharField(
        label="Describe the photo (alt text)",
        max_length=300,
        required=False,
        help_text="What a person who can't see the photo needs to know.",
    )
    credit = forms.CharField(label="Photo credit", max_length=200, required=False)
    caption = forms.CharField(label="Caption", max_length=300, required=False)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
        if image.size > MAX_IMAGE_BYTES:
            raise forms.ValidationError("Photos can be at most 10 MB.")
        fmt = getattr(getattr(image, "image", None), "format", None)
        if fmt and fmt.upper() not in ALLOWED_IMAGE_FORMATS:
            raise forms.ValidationError("Use a JPEG, PNG or WebP photo.")
        return image

    def clean(self):
        data = super().clean()
        if data.get("image") and not (data.get("alt_text") or "").strip():
            self.add_error("alt_text", "Describe the photo for people who can't see it.")
        return data


ImageRows = forms.formset_factory(ImageRowForm, extra=1, max_num=12)


def resized_image(upload):
    """Return (ContentFile, name): EXIF-rotated, at most 1600 px on the long side, as JPEG/PNG."""
    upload.seek(0)
    img = ImageOps.exif_transpose(Image.open(upload))
    img.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))
    keep_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    buffer = io.BytesIO()
    stem = slugify(upload.name.rsplit(".", 1)[0])[:60] or "photo"
    if keep_alpha:
        img.save(buffer, "PNG", optimize=True)
        name = f"{stem}.png"
    else:
        img.convert("RGB").save(buffer, "JPEG", quality=85, optimize=True, progressive=True)
        name = f"{stem}.jpg"
    return ContentFile(buffer.getvalue()), name


def craft_type_from(data, instance=None):
    raw = (data or {}).get("craft_type") or (instance.craft_type_id if instance else None)
    try:
        return CraftType.objects.get(pk=int(raw)) if raw else None
    except (ValueError, CraftType.DoesNotExist):
        return None
