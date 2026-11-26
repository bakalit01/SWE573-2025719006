"""Admin action "Merge selected …" with a confirmation page (US-28)."""

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.template.response import TemplateResponse

from .taxonomy import link_count, merge


@admin.action(description="Merge selected into one (keeps every link to crafts)")
def merge_selected(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    items = list(queryset)
    if len(items) < 2:
        modeladmin.message_user(request, "Select two or more to merge.", messages.WARNING)
        return None
    keep_pk = request.POST.get("keep")
    if keep_pk and request.POST.get("confirm"):
        keep = next((i for i in items if str(i.pk) == keep_pk), None)
        if keep is None:
            modeladmin.message_user(request, "Choose which one to keep.", messages.ERROR)
            return None
        others = [i for i in items if i.pk != keep.pk]
        names = ", ".join(f"“{o}”" for o in others)
        moved = merge(keep, others)
        modeladmin.message_user(
            request,
            f"Merged {names} into “{keep}”: {moved} link(s) moved; the old names are kept "
            "as other spellings.",
            messages.SUCCESS,
        )
        return None
    biggest = max(items, key=link_count)
    return TemplateResponse(
        request,
        "admin/merge_terms.html",
        {
            **modeladmin.admin_site.each_context(request),
            "title": f"Merge {opts.verbose_name_plural}",
            "opts": opts,
            "items": [(i, link_count(i)) for i in items],
            "suggested": biggest.pk,
            "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
            "uses": "communities" if opts.model_name == "region" else "crafts",
        },
    )
