from django.contrib import admin

from .models import (
    AttributeDefinition,
    Craft,
    CraftMaterial,
    CraftTechnique,
    CraftType,
    Material,
    Media,
    Tag,
    Technique,
)


class AttributeDefinitionInline(admin.TabularInline):
    model = AttributeDefinition
    extra = 0
    fields = ["order", "key", "label", "data_type", "unit", "options", "required", "is_active"]


@admin.register(CraftType)
class CraftTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "added_by"]
    list_filter = [("added_by", admin.EmptyFieldListFilter)]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AttributeDefinitionInline]


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
    fields = ["order", "image", "static_path", "alt_text", "credit", "is_sensitive"]


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
    search_fields = ["title", "summary", "description", "maker_credit", "place_name"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CraftMaterialInline, CraftTechniqueInline, MediaInline]
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
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.site_header = "Indigenous Crafts Platform – admin"
