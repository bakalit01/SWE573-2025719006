from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AccountChange, User


class AccountChangeInline(admin.TabularInline):
    model = AccountChange
    fk_name = "user"
    extra = 0
    can_delete = False
    fields = ["changed_at", "field", "old_value", "new_value", "changed_by"]
    readonly_fields = fields
    verbose_name_plural = "Change log (roles and suspensions)"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """US-27: search users, change roles, see stewardships, suspend accounts."""

    ordering = ["email"]
    list_display = ["email", "display_name", "role", "is_active", "community", "date_joined"]
    list_filter = ["role", "is_active", "community"]
    search_fields = ["email", "display_name", "first_name", "last_name"]
    readonly_fields = ["stewards_for", "last_login", "date_joined"]
    inlines = [AccountChangeInline]
    actions = ["suspend", "reactivate"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("display_name", "first_name", "last_name", "bio", "community")}),
        (
            "Role and access",
            {
                "fields": ("role", "stewards_for", "is_active"),
                "description": "Suspend an account by unticking Active: the user can no "
                "longer log in. Assign stewards under Communities.",
            },
        ),
        (
            "Django permissions",
            {
                "classes": ("collapse",),
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "role", "password1", "password2")}),
    )

    @admin.display(description="Steward for")
    def stewards_for(self, obj):
        names = [c.name for c in obj.stewarded_communities.all()] if obj.pk else []
        return ", ".join(names) or "—"

    def save_model(self, request, obj, form, change):
        obj.changed_by = request.user
        super().save_model(request, obj, form, change)

    def _set_active(self, request, queryset, active):
        count = 0
        for user in queryset.exclude(pk=request.user.pk):  # never lock yourself out
            if user.is_active != active:
                user.is_active = active
                user.changed_by = request.user
                user.save()
                count += 1
        verb = "reactivated" if active else "suspended"
        self.message_user(request, f"{count} account(s) {verb}.", messages.SUCCESS)

    @admin.action(description="Suspend selected accounts (they can't log in)")
    def suspend(self, request, queryset):
        self._set_active(request, queryset, False)

    @admin.action(description="Reactivate selected accounts")
    def reactivate(self, request, queryset):
        self._set_active(request, queryset, True)


@admin.register(AccountChange)
class AccountChangeAdmin(admin.ModelAdmin):
    list_display = ["changed_at", "user", "field", "old_value", "new_value", "changed_by"]
    list_filter = ["field"]
    search_fields = ["user__email"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
