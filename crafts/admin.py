from django.contrib import admin

from .models import AttributeDefinition, Craft, CraftType, Material, Media, Technique


class AttributeDefinitionInline(admin.TabularInline):
    model = AttributeDefinition
    extra = 0
    fields = ["order", "key", "label", "data_type", "unit", "options", "required", "is_active"]


@admin.register(CraftType)
class CraftTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AttributeDefinitionInline]


class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    fields = ["order", "image", "static_path", "alt_text", "credit", "is_sensitive"]


@admin.register(Craft)
class CraftAdmin(admin.ModelAdmin):
    list_display = ["title", "craft_type", "community", "visibility", "status", "is_sample"]
    list_filter = ["status", "visibility", "craft_type", "is_sample"]
    search_fields = ["title", "summary", "description", "maker_credit"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["materials", "techniques"]
    inlines = [MediaInline]


admin.site.register(Material)
admin.site.register(Technique)
admin.site.site_header = "Indigenous Crafts Platform – admin"
