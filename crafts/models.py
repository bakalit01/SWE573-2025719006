import datetime

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.templatetags.static import static
from django.urls import reverse

from . import units


class Term(models.Model):
    """Base for small controlled vocabularies (materials, techniques)."""

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, help_text="Short general explanation (glossary)")

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Material(Term):
    pass


class Technique(Term):
    pass


class CraftType(models.Model):
    """Textile, pottery, beadwork… Each type defines its own extra attributes."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AttributeDefinition(models.Model):
    """One craft-type-specific field. Forms and detail pages are built from these rows."""

    class DataType(models.TextChoices):
        TEXT = "text", "Text"
        LONG_TEXT = "long_text", "Long text"
        NUMBER = "number", "Number"
        CHOICE = "choice", "Single choice"
        MULTI_CHOICE = "multi_choice", "Multiple choice"
        BOOLEAN = "boolean", "Yes / no"
        DATE = "date", "Date or period"
        URL = "url", "Link"

    craft_type = models.ForeignKey(CraftType, on_delete=models.CASCADE, related_name="attributes")
    key = models.SlugField(max_length=60, help_text="Stored key in Craft.attributes")
    label = models.CharField(max_length=120)
    data_type = models.CharField(max_length=20, choices=DataType.choices, default=DataType.TEXT)
    unit = models.CharField(max_length=20, blank=True)
    options = models.JSONField(default=list, blank=True, help_text="Choices for choice fields")
    required = models.BooleanField(default=False)
    help_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Retired fields keep their data")

    class Meta:
        ordering = ["craft_type", "order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["craft_type", "key"], name="unique_attribute_key")
        ]

    def __str__(self):
        return f"{self.craft_type}: {self.label}"

    def display_value(self, value):
        """Human-readable value for the detail page."""
        if value in (None, "", []):
            return ""
        if self.data_type == self.DataType.BOOLEAN:
            return "Yes" if value else "No"
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        return f"{value} {self.unit}".strip() if self.unit else str(value)


class CraftQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Craft.Status.PUBLISHED)

    def visible_to(self, user):
        """The single place that decides which crafts a user may see (US-22).

        Visitors: published + public. Members: also published + members-only.
        Everyone also sees their own records (drafts included). Staff see everything.
        """
        if user is not None and user.is_authenticated and user.is_staff:
            return self.all()
        levels = [Craft.Visibility.PUBLIC]
        if user is not None and user.is_authenticated:
            levels.append(Craft.Visibility.MEMBERS)
        rule = Q(status=Craft.Status.PUBLISHED, visibility__in=levels)
        if user is not None and user.is_authenticated:
            rule |= Q(created_by=user)
        return self.filter(rule)

    def listed_for(self, user):
        """What appears in public lists: visible AND published (own drafts live in My crafts)."""
        return self.visible_to(user).filter(status=Craft.Status.PUBLISHED)


class Craft(models.Model):
    class LocationPrecision(models.TextChoices):
        EXACT = "exact", "Exact point"
        APPROXIMATE = "approximate", "Approximate area (about 10 km)"
        HIDDEN = "hidden", "Hidden: show the place name only"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        MEMBERS = "members", "Members only"
        COMMUNITY = "community", "Community only"
        RESTRICTED = "restricted", "Restricted"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending review"
        PUBLISHED = "published", "Published"
        UNPUBLISHED = "unpublished", "Unpublished"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    cultural_context = models.TextField(blank=True)
    craft_type = models.ForeignKey(CraftType, on_delete=models.PROTECT, related_name="crafts")
    community = models.ForeignKey(
        "communities.Community", on_delete=models.PROTECT, related_name="crafts"
    )
    process = models.TextField("How it is made", blank=True)

    # Made by / Made in (FB-03)
    maker_credit = models.CharField(
        "Made by", max_length=300, help_text="Makers credited on the record (FR-P6: required)"
    )
    year_made = models.PositiveSmallIntegerField(
        "Year made",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
    )
    year_is_approximate = models.BooleanField("Approximate year (circa)", default=False)
    period = models.CharField(
        max_length=120, blank=True, help_text="If the year is unknown, e.g. 'early 20th century'"
    )

    # Place (FB-01)
    place_name = models.CharField("Place", max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    location_precision = models.CharField(
        max_length=12,
        choices=LocationPrecision.choices,
        default=LocationPrecision.EXACT,
        help_text="Use 'approximate' or 'hidden' for sensitive places",
    )

    # Size (FB-04)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size_unit = models.CharField(max_length=4, choices=units.LENGTH_UNITS, blank=True)
    weight = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    weight_unit = models.CharField(max_length=4, choices=units.WEIGHT_UNITS, blank=True)
    traditional_measure = models.CharField(
        "Local or traditional measure",
        max_length=200,
        blank=True,
        help_text="e.g. 'two hand spans long' or '1 arşın'",
    )

    # Materials and techniques with per-craft detail (FB-02)
    materials = models.ManyToManyField(
        Material, through="CraftMaterial", blank=True, related_name="crafts"
    )
    techniques = models.ManyToManyField(
        Technique, through="CraftTechnique", blank=True, related_name="crafts"
    )
    attributes = models.JSONField(default=dict, blank=True)
    visibility = models.CharField(
        max_length=20, choices=Visibility.choices, default=Visibility.MEMBERS
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_sample = models.BooleanField(
        default=False, help_text="Fictional sample record, labelled on screen"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="crafts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CraftQuerySet.as_manager()

    class Meta:
        ordering = ["title"]
        indexes = [GinIndex(fields=["attributes"], name="craft_attributes_gin")]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("crafts:detail", kwargs={"slug": self.slug})

    @property
    def cover(self):
        return self.media.first()

    def clean(self):
        super().clean()
        this_year = datetime.date.today().year
        if self.year_made and self.year_made > this_year:
            raise ValidationError({"year_made": "The year made can't be in the future."})
        if (self.latitude is None) != (self.longitude is None):
            raise ValidationError("Give both latitude and longitude, or neither.")
        if any(v is not None for v in (self.height, self.width, self.depth)) and not self.size_unit:
            raise ValidationError({"size_unit": "Choose the unit for the size."})
        if self.weight is not None and not self.weight_unit:
            raise ValidationError({"weight_unit": "Choose the unit for the weight."})

    # ---- "Made" summary (FB-03) ----
    @property
    def made_in(self):
        if self.year_made:
            return f"c. {self.year_made}" if self.year_is_approximate else str(self.year_made)
        return self.period

    @property
    def made_from(self):
        return ", ".join(cm.material.name for cm in self.craft_materials.all())

    @property
    def place_label(self):
        return ", ".join(p for p in (self.place_name, self.country) if p)

    # ---- Location for maps (FB-01) ----
    @property
    def map_point(self):
        """Coordinates safe to publish, or None. Approximate places are rounded (~10 km)."""
        if self.latitude is None or self.longitude is None:
            return None
        if self.location_precision == self.LocationPrecision.HIDDEN:
            return None
        lat, lng = float(self.latitude), float(self.longitude)
        if self.location_precision == self.LocationPrecision.APPROXIMATE:
            return {"lat": round(lat, 1), "lng": round(lng, 1), "approximate": True}
        return {"lat": round(lat, 5), "lng": round(lng, 5), "approximate": False}

    # ---- Size (FB-04) ----
    @property
    def size(self):
        return units.describe_size(self.height, self.width, self.depth, self.size_unit)

    @property
    def weight_display(self):
        return units.describe_weight(self.weight, self.weight_unit)

    def attribute_rows(self):
        """(label, value) pairs for the active attribute definitions that have a value."""
        rows = []
        for definition in self.craft_type.attributes.filter(is_active=True):
            shown = definition.display_value(self.attributes.get(definition.key))
            if shown:
                rows.append((definition.label, shown))
        return rows


class CraftMaterial(models.Model):
    """A material used in one craft, with where it comes from and how it is used."""

    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name="craft_materials")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    origin = models.CharField(
        max_length=200, blank=True, help_text="Where it comes from, e.g. 'mined near Eskişehir'"
    )
    notes = models.CharField(
        max_length=400, blank=True, help_text="How it is used or prepared in this craft"
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["craft", "material"], name="unique_craft_material")
        ]

    def __str__(self):
        return f"{self.craft}: {self.material}"


class CraftTechnique(models.Model):
    """A technique used in one craft, with notes on how it is applied."""

    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name="craft_techniques")
    technique = models.ForeignKey(Technique, on_delete=models.PROTECT)
    notes = models.CharField(max_length=400, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["craft", "technique"], name="unique_craft_technique")
        ]

    def __str__(self):
        return f"{self.craft}: {self.technique}"


class Media(models.Model):
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to="crafts/%Y/%m/", blank=True)
    static_path = models.CharField(
        max_length=200, blank=True, help_text="Bundled sample illustration (static file path)"
    )
    alt_text = models.CharField(max_length=300)
    caption = models.CharField(max_length=300, blank=True)
    credit = models.CharField(max_length=200, blank=True)
    is_sensitive = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "media"

    def __str__(self):
        return self.alt_text

    @property
    def url(self):
        if self.image:
            return self.image.url
        return static(self.static_path) if self.static_path else ""
