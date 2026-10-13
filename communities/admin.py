from django.contrib import admin

from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "is_sample"]
    list_filter = ["is_sample"]
    search_fields = ["name", "other_names", "region"]
    prepopulated_fields = {"slug": ("name",)}
