from django.contrib import admin
from django.db.models import Count

from crafts.admin_merge import merge_selected

from .models import Community, Region


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "is_sample", "added_by"]
    list_filter = ["is_sample", "region", ("added_by", admin.EmptyFieldListFilter)]
    search_fields = ["name", "other_names", "region__name"]
    autocomplete_fields = ["region"]
    actions = [merge_selected]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["stewards"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "stewards":
            from accounts.models import User

            kwargs["queryset"] = User.objects.filter(role=User.Role.STEWARD, is_active=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """Regions communities belong to (US-28): alternate spellings and merging duplicates."""

    list_display = ["name", "other_names", "community_count"]
    search_fields = ["name", "other_names"]
    actions = [merge_selected]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(n_communities=Count("communities"))

    @admin.display(description="Communities", ordering="n_communities")
    def community_count(self, obj):
        return obj.n_communities
