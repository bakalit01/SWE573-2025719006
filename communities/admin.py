from django.contrib import admin

from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "is_sample", "added_by"]
    list_filter = ["is_sample", ("added_by", admin.EmptyFieldListFilter)]
    search_fields = ["name", "other_names", "region"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["stewards"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "stewards":
            from accounts.models import User

            kwargs["queryset"] = User.objects.filter(role=User.Role.STEWARD, is_active=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
