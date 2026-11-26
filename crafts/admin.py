from django import forms
from django.contrib import admin
from django.db.models import Count

from .admin_merge import merge_selected
from .models import (
    AttributeDefinition,
    Collection,
    Consent,
    Craft,
    CraftMaterial,
    CraftName,
    CraftTechnique,
    CraftType,
    Material,
    Media,
    Report,
    ReviewDecision,
    Tag,
    Technique,
)

# ---------- Craft types and their fields, managed in the admin (US-13) ----------


class LinesField(forms.CharField):
    """A list of strings edited as one item per line (blank lines and repeats dropped)."""

    widget = forms.Textarea(attrs={"rows": 3, "cols": 22})

    def prepare_value(self, value):
        return "\n".join(value) if isinstance(value, list) else value

    def to_python(self, value):
        items = []
        for line in (super().to_python(value) or "").splitlines():
            line = " ".join(line.split())
            if line and line not in items:
                items.append(line)
        return items


class AttributeDefinitionForm(forms.ModelForm):
    options = LinesField(
        label="Choices", required=False, help_text="One per line (choice fields only)"
    )

    class Meta:
        model = AttributeDefinition
        fields = [
            "order",
            "key",
            "label",
            "data_type",
            "unit",
            "options",
            "help_text",
            "required",
            "is_active",
        ]
        labels = {"is_active": "Active", "order": "Order"}
        help_texts = {"is_active": "Untick to retire: hidden from forms, data kept"}


class AttributeDefinitionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.deleted_forms:
            definition = form.instance
            if definition.pk:
                count = definition.crafts_with_values().count()
                if count:
                    raise forms.ValidationError(
                        f"“{definition.label}” has values in {count} craft(s), so it can't be "
                        "deleted. Untick Active to retire it instead; its data is kept."
                    )


class AttributeDefinitionInline(admin.TabularInline):
    """Add, edit, reorder (↑ ↓ or the Order numbers) and retire a craft type's fields."""

    model = AttributeDefinition
    form = AttributeDefinitionForm
    formset = AttributeDefinitionFormSet
    extra = 1
    fields = [
        "order",
        "key",
        "label",
        "data_type",
        "unit",
        "options",
        "help_text",
        "required",
        "is_active",
    ]
    ordering = ["order", "id"]

    class Media:
        js = ["js/admin_attributes.js"]
        css = {"all": ["css/admin.css"]}


@admin.register(CraftType)
class CraftTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "field_count", "craft_count", "added_by"]
    list_filter = [("added_by", admin.EmptyFieldListFilter)]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AttributeDefinitionInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                n_fields=Count("attributes", distinct=True),
                n_crafts=Count("crafts", distinct=True),
            )
        )

    @admin.display(description="Fields", ordering="n_fields")
    def field_count(self, obj):
        return obj.n_fields

    @admin.display(description="Crafts", ordering="n_crafts")
    def craft_count(self, obj):
        return obj.n_crafts


class CraftMaterialInline(admin.TabularInline):
    model = CraftMaterial
    extra = 0
    fields = ["order", "material", "origin", "notes"]
    autocomplete_fields = ["material"]


class CraftTechniqueInline(admin.TabularInline):
    model = CraftTechnique
    extra = 0
    fields = ["order", "technique", "notes"]
    autocomplete_fields = ["technique"]


class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    fields = ["order", "image", "commons_file", "alt_text", "caption", "credit", "is_sensitive"]


class CraftNameInline(admin.TabularInline):
    model = CraftName
    extra = 0
    fields = ["order", "name", "language", "lang_code", "is_primary"]


@admin.register(Craft)
class CraftAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "craft_type",
        "community",
        "year_made",
        "visibility",
        "status",
        "is_sample",
    ]
    list_filter = ["status", "visibility", "craft_type", "is_sample"]
    search_fields = ["title", "names__name", "summary", "description", "maker_credit", "place_name"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CraftNameInline, CraftMaterialInline, CraftTechniqueInline, MediaInline]
    filter_horizontal = ["tags"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "craft_type", "community", "summary")}),
        ("Story", {"fields": ("description", "process", "cultural_context")}),
        ("Made", {"fields": ("maker_credit", "year_made", "year_is_approximate", "period")}),
        (
            "Place",
            {"fields": ("place_name", "country", "latitude", "longitude", "location_precision")},
        ),
        (
            "Size",
            {
                "fields": (
                    "height",
                    "width",
                    "depth",
                    "size_unit",
                    "weight",
                    "size_unit_other",
                    "weight_unit",
                    "weight_unit_other",
                    "traditional_measure",
                )
            },
        ),
        ("Details", {"fields": ("attributes", "extra_details", "tags")}),
        ("Publishing", {"fields": ("visibility", "status", "is_sample", "created_by")}),
    )


@admin.register(Material, Technique)
class TermAdmin(admin.ModelAdmin):
    """Materials and techniques (US-28): alternate spellings, and merging duplicates."""

    list_display = ["name", "other_names", "craft_count"]
    search_fields = ["name", "other_names", "description"]
    fields = ["name", "other_names", "description"]
    actions = [merge_selected]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(n_crafts=Count("crafts", distinct=True))

    @admin.display(description="Crafts", ordering="n_crafts")
    def craft_count(self, obj):
        return obj.n_crafts


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Members' collections (US-18); private ones are for support only."""

    list_display = ["name", "owner", "is_public", "craft_count", "updated_at"]
    list_filter = ["is_public"]
    search_fields = ["name", "owner__email", "owner__display_name"]
    autocomplete_fields = ["owner"]
    filter_horizontal = ["crafts"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(n_crafts=Count("crafts"))

    @admin.display(description="Crafts", ordering="n_crafts")
    def craft_count(self, obj):
        return obj.n_crafts


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    actions = [merge_selected]


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["craft", "granted_by", "date", "scope", "recorded_by"]
    search_fields = ["craft__title", "granted_by"]
    autocomplete_fields = ["craft"]


@admin.register(ReviewDecision)
class ReviewDecisionAdmin(admin.ModelAdmin):
    list_display = ["created_at", "craft", "decision", "reviewer"]
    list_filter = ["decision"]
    search_fields = ["craft__title", "comment"]

    def has_change_permission(self, request, obj=None):
        return False  # decisions are a history; make a new one instead


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["created_at", "craft", "reason", "status", "resolved_by"]
    list_filter = ["status", "reason"]
    search_fields = ["craft__title", "details", "contact_email"]
    readonly_fields = ["created_at", "reporter"]


admin.site.site_header = "Indigenous Crafts Platform – admin"
