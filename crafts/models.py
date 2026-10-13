from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Term(models.Model):
    """Base for small controlled vocabularies (materials, techniques)."""

    name = models.CharField(max_length=120, unique=True)

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
        """The single place that decides which crafts a user may see (US-22)."""
        qs = self.published()
        if user is not None and user.is_authenticated and user.is_staff:
            return self.all()
        levels = [Craft.Visibility.PUBLIC]
        if user is not None and user.is_authenticated:
            levels.append(Craft.Visibility.MEMBERS)
        return qs.filter(visibility__in=levels)


class Craft(models.Model):
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
    region = models.CharField(max_length=200, blank=True)
    maker_credit = models.CharField(
        max_length=300, help_text="Makers credited on the record (FR-P6: required)"
    )
    period = models.CharField(max_length=120, blank=True, help_text="Date made or period")
    materials = models.ManyToManyField(Material, blank=True, related_name="crafts")
    techniques = models.ManyToManyField(Technique, blank=True, related_name="crafts")
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

    def attribute_rows(self):
        """(label, value) pairs for the active attribute definitions that have a value."""
        rows = []
        for definition in self.craft_type.attributes.filter(is_active=True):
            shown = definition.display_value(self.attributes.get(definition.key))
            if shown:
                rows.append((definition.label, shown))
        return rows


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
