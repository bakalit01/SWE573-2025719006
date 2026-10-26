"""Forms for adding and editing crafts (US-08, US-09, US-11, US-20 and feedback FB-01…FB-04)."""

import io
from decimal import Decimal

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image, ImageOps

from communities.models import Community

from . import units
from .models import AttributeDefinition, Craft, CraftType, Tag

OTHER = "__other__"  # "Other (type your own)" in craft type, community and choice fields
MAX_TAGS = 15
MAX_TAG_LENGTH = 40

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_SIDE = 1600
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


def other_box(label, select_name, max_length=120, **attrs):
    """A text box shown when "Other" is chosen in the select or checkbox group `select_name`."""
    return forms.CharField(
        label=label,
        max_length=max_length,
        required=False,
        widget=forms.TextInput(attrs={"data-other-for": select_name, **attrs}),
    )


def parse_tags(text):
    """'Ceremonial, natural dye, #ceremonial' → ['Ceremonial', 'natural dye'].

    The first spelling of a tag wins; a leading # is dropped.
    """
    seen, tags = set(), []
    for raw in (text or "").replace("\n", ",").split(","):
        name = " ".join(raw.strip().lstrip("#").split())
        if name and name.lower() not in seen:
            seen.add(name.lower())
            tags.append(name)
    return tags


def unique_slug_for(model, name, field="slug"):
    base = slugify(name, allow_unicode=True)[:100] or model.__name__.lower()
    slug, n = base, 2
    while model.objects.filter(**{field: slug}).exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


class CraftForm(forms.ModelForm):
    """Core fields shared by every craft.

    Craft type and community offer "Other (type your own)": the typed name is matched to an
    existing entry (ignoring case) or added as a new one, marked as added by this user.
    """

    craft_type = forms.ChoiceField(
        label="Craft type", widget=forms.Select(attrs={"data-craft-type": ""})
    )
    craft_type_other = other_box("Name of the craft type", "craft_type")
    community = forms.ChoiceField(label="Community")
    community_other = other_box(
        "Name of the community",
        "community",
        max_length=200,
        placeholder="The community's own name for itself",
    )
    tags = forms.CharField(
        label="Tags",
        required=False,
        max_length=800,
        help_text=(
            "Your own keywords, separated by commas, e.g. ceremonial, natural dye, everyday use."
        ),
        widget=forms.TextInput(attrs={"data-tags": "", "autocomplete": "off"}),
    )

    class Meta:
        model = Craft
        fields = [
            "title",
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
            "size_unit_other",
            "weight",
            "weight_unit",
            "weight_unit_other",
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
            "size_unit_other": "Your unit",
            "weight_unit": "Unit",
            "weight_unit_other": "Your unit",
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
            "size_unit_other": forms.TextInput(
                attrs={"data-other-for": "size_unit", "placeholder": "e.g. karış, hand spans"}
            ),
            "weight_unit_other": forms.TextInput(
                attrs={"data-other-for": "weight_unit", "placeholder": "e.g. okka, dirhem"}
            ),
        }

    field_order = ["title", "craft_type", "craft_type_other", "community", "community_other"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        other = [(OTHER, "Other (type your own)")]
        self.fields["craft_type"].choices = (
            [("", "Choose a craft type")]
            + [(str(t.pk), t.name) for t in CraftType.objects.all()]
            + other
        )
        self.fields["community"].choices = (
            [("", "Choose a community")]
            + [(str(c.pk), c.name) for c in Community.objects.all()]
            + other
        )
        if self.instance.pk:
            self.initial.setdefault("craft_type", str(self.instance.craft_type_id))
            self.initial.setdefault("community", str(self.instance.community_id))
            self.initial.setdefault("tags", ", ".join(t.name for t in self.instance.tags.all()))
        # Community-only and restricted visibility arrive with steward review (M3).
        self.fields["visibility"].choices = [
            (Craft.Visibility.PUBLIC, "Public: anyone can see it"),
            (Craft.Visibility.MEMBERS, "Members only: signed-in users"),
        ]
        self.fields["visibility"].widget = forms.RadioSelect(
            choices=self.fields["visibility"].choices
        )
        self.fields["size_unit"].choices = [("", "Choose unit")] + list(units.LENGTH_UNITS)
        self.fields["weight_unit"].choices = [("", "Choose unit")] + list(units.WEIGHT_UNITS)
        for name in ("height", "width", "depth", "weight"):
            self.fields[name].widget.attrs.update({"min": 0, "step": "any"})
        self.fields["latitude"].label = "Latitude"
        self.fields["longitude"].label = "Longitude"

    def _pick(self, name, model, max_length):
        """The chosen entry, or the name typed under "Other" (validated, not yet saved)."""
        value = self.cleaned_data.get(name)
        if value != OTHER:
            return model.objects.filter(pk=value).first() if value else None
        typed = " ".join((self.cleaned_data.get(f"{name}_other") or "").split())
        if not typed:
            self.add_error(f"{name}_other", "Type the name, or choose one from the list.")
            return None
        return model.objects.filter(name__iexact=typed).first() or typed[:max_length]

    def clean(self):
        data = super().clean()
        data["craft_type"] = self._pick("craft_type", CraftType, 120)
        data["community"] = self._pick("community", Community, 200)
        tags = parse_tags(data.get("tags"))
        if len(tags) > MAX_TAGS:
            self.add_error("tags", f"Use at most {MAX_TAGS} tags.")
        long = [t for t in tags if len(t) > MAX_TAG_LENGTH]
        if long:
            self.add_error("tags", f"Keep each tag under {MAX_TAG_LENGTH} characters: {long[0]}")
        data["tag_names"] = tags
        return data

    def _saved(self, value, model):
        if isinstance(value, model) or value is None:
            return value
        existing = model.objects.filter(name__iexact=value).first()
        if existing:
            return existing
        added_by = self.user if self.user and self.user.is_authenticated else None
        return model.objects.create(
            name=value, slug=unique_slug_for(model, value), added_by=added_by
        )

    @property
    def new_type_chosen(self):
        return self.data.get("craft_type") == OTHER if self.is_bound else False

    def save(self, commit=True):
        craft = super().save(commit=False)
        craft.craft_type = self._saved(self.cleaned_data["craft_type"], CraftType)
        craft.community = self._saved(self.cleaned_data["community"], Community)
        if craft.size_unit != units.OTHER:
            craft.size_unit_other = ""
        if craft.weight_unit != units.OTHER:
            craft.weight_unit_other = ""
        if not craft.slug:
            craft.slug = unique_slug(craft.title)
        if commit:
            craft.save()
            self.save_tags(craft)
        return craft

    def save_tags(self, craft):
        tags = []
        for name in self.cleaned_data.get("tag_names", []):
            tag = Tag.objects.filter(name__iexact=name).first()
            tags.append(tag or Tag.objects.create(name=name, slug=unique_slug_for(Tag, name)))
        craft.tags.set(tags)


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
    other = [(OTHER, "Other (type your own)")]
    if definition.data_type == T.CHOICE:
        return forms.ChoiceField(choices=[("", "—")] + options + other, **common)
    if definition.data_type == T.MULTI_CHOICE:
        return forms.MultipleChoiceField(
            choices=options + other, widget=forms.CheckboxSelectMultiple, **common
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
        T = AttributeDefinition.DataType
        for d in self.definitions:
            self.fields[d.key] = field_for(d)
            value = values.get(d.key)
            if d.data_type in (T.CHOICE, T.MULTI_CHOICE):
                self.fields[self.other_key(d)] = other_box(
                    f"Other {d.label.lower()}",
                    f"{self.prefix}-{d.key}",
                    max_length=200,
                    placeholder=(
                        "Separate several with commas" if d.data_type == T.MULTI_CHOICE else ""
                    ),
                )
                value = self._split_other(d, value)
            if d.data_type == T.BOOLEAN and value is not None:
                value = "yes" if value else "no"
            if value not in (None, ""):
                self.initial[d.key] = value

    @staticmethod
    def other_key(definition):
        return f"{definition.key}__other"

    def _split_other(self, d, value):
        """Saved values that aren't in the option list go back into the "Other" box."""
        options = set(d.options or [])
        if d.data_type == AttributeDefinition.DataType.CHOICE:
            if value and value not in options:
                self.initial[self.other_key(d)] = value
                return OTHER
            return value
        values = value if isinstance(value, list) else ([value] if value else [])
        extra = [v for v in values if v not in options]
        if extra:
            self.initial[self.other_key(d)] = ", ".join(str(v) for v in extra)
            return [v for v in values if v in options] + [OTHER]
        return values

    def clean(self):
        data = super().clean()
        for d in self.definitions:
            value = data.get(d.key)
            chose_other = value == OTHER or (isinstance(value, list) and OTHER in value)
            if chose_other and not (data.get(self.other_key(d)) or "").strip():
                self.add_error(self.other_key(d), "Type your own value, or choose one above.")
        return data

    def json_values(self):
        """Cleaned values as JSON-safe data for Craft.attributes."""
        out = {}
        T = AttributeDefinition.DataType
        for d in self.definitions:
            value = self.cleaned_data.get(d.key)
            typed = (self.cleaned_data.get(self.other_key(d)) or "").strip()
            if d.data_type == T.CHOICE and value == OTHER:
                value = " ".join(typed.split())
            elif d.data_type == T.MULTI_CHOICE and value:
                value = [v for v in value if v != OTHER]
                if OTHER in self.cleaned_data.get(d.key):
                    value += [t for t in parse_tags(typed) if t not in value]
            if value in (None, "", []):
                continue
            if isinstance(value, Decimal):
                value = int(value) if value == value.to_integral() else float(value)
            if d.data_type == T.BOOLEAN:
                value = value == "yes"
            out[d.key] = value
        return out


# ---------- The contributor's own details (any label, any value) ----------


class DetailRowForm(forms.Form):
    label = forms.CharField(
        label="Detail",
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. Dye source"}),
    )
    value = forms.CharField(
        label="Value",
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. walnut husks"}),
    )

    def clean(self):
        data = super().clean()
        label, value = (data.get("label") or "").strip(), (data.get("value") or "").strip()
        if value and not label:
            self.add_error("label", "Name this detail.")
        elif label and not value:
            self.add_error("value", "Add a value, or remove the row.")
        return data


class DetailFormSet(forms.BaseFormSet):
    def json_values(self):
        rows = []
        for form in self.forms:
            if form.is_valid() and form.cleaned_data.get("label"):
                rows.append(
                    {
                        "label": form.cleaned_data["label"].strip(),
                        "value": form.cleaned_data["value"].strip(),
                    }
                )
        return rows


DetailRows = forms.formset_factory(
    DetailRowForm, formset=DetailFormSet, extra=0, min_num=1, max_num=30
)


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
    raw = (data or {}).get("craft_type") if data else None
    raw = raw or (instance.craft_type_id if instance else None)
    try:
        return CraftType.objects.get(pk=int(raw)) if raw else None
    except (ValueError, CraftType.DoesNotExist):
        return None
