from django.contrib import admin

from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "is_sample", "added_by"]
    list_filter = ["is_sample", ("added_by", admin.EmptyFieldListFilter)]
    search_fields = ["name", "other_names", "region"]
    prepopulated_fields = {"slug": ("name",)}
