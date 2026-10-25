from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from communities.models import Community

from .forms import (
    AttributesForm,
    CraftForm,
    ImageRows,
    MaterialRows,
    TechniqueRows,
    craft_type_from,
    resized_image,
)
from .models import Craft, CraftMaterial, CraftTechnique, CraftType, Material, Media, Technique

PAGE_SIZE = 24


def _listed(request):
    return (
        Craft.objects.listed_for(request.user)
        .select_related("craft_type", "community")
        .prefetch_related("media")
    )


def home(request):
    crafts = _listed(request)
    return render(
        request,
        "crafts/home.html",
        {
            "featured": crafts[:6],
            "craft_count": crafts.count(),
            "type_count": CraftType.objects.count(),
            "community_count": Community.objects.count(),
        },
    )


def craft_list(request):
    crafts = _listed(request)
    craft_type = request.GET.get("type", "")
    community = request.GET.get("community", "")
    if craft_type:
        crafts = crafts.filter(craft_type__slug=craft_type)
    if community:
        crafts = crafts.filter(community__slug=community)

    page = Paginator(crafts, PAGE_SIZE).get_page(request.GET.get("page"))
    filters = {k: v for k, v in {"type": craft_type, "community": community}.items() if v}
    return render(
        request,
        "crafts/list.html",
        {
            "page": page,
            "crafts": page.object_list,
            "craft_types": CraftType.objects.all(),
            "communities": Community.objects.all(),
            "selected_type": craft_type,
            "selected_community": community,
            "filter_query": urlencode(filters),
        },
    )


def can_edit(user, craft):
    return user.is_authenticated and (user.is_staff or craft.created_by_id == user.pk)


def craft_detail(request, slug):
    # Crafts the user may not see return 404, never "forbidden" (US-07).
    craft = get_object_or_404(
        Craft.objects.visible_to(request.user)
        .select_related("craft_type", "community", "created_by")
        .prefetch_related("media", "craft_materials__material", "craft_techniques__technique"),
        slug=slug,
    )
    report_url = f"{settings.REPO_URL}/issues/new?" + urlencode(
        {
            "title": f"Report: {craft.title}",
            "body": f"Craft page: {request.build_absolute_uri()}\n\nWhat is wrong?\n",
            "labels": "type: bug",
        }
    )
    return render(
        request,
        "crafts/detail.html",
        {
            "craft": craft,
            "attribute_rows": craft.attribute_rows(),
            "report_url": report_url,
            "can_edit": can_edit(request.user, craft),
            "map_point": craft.map_point,
        },
    )


# ---------- Add / edit / delete (US-08, US-09, US-11, US-20) ----------


def _row_initial(craft):
    if craft is None:
        return [{}], [{}]
    materials = [
        {"name": cm.material.name, "origin": cm.origin, "notes": cm.notes}
        for cm in craft.craft_materials.select_related("material")
    ] or [{}]
    techniques = [
        {"name": ct.technique.name, "notes": ct.notes}
        for ct in craft.craft_techniques.select_related("technique")
    ] or [{}]
    return materials, techniques


def _craft_form_page(request, craft=None):
    editing = craft is not None
    data = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None

    form = CraftForm(data, instance=craft)
    craft_type = craft_type_from(data, craft)
    attr_form = AttributesForm(
        data, craft_type=craft_type, values=craft.attributes if craft else None
    )
    material_initial, technique_initial = _row_initial(craft)
    materials = MaterialRows(data, prefix="mat", initial=None if data else material_initial)
    techniques = TechniqueRows(data, prefix="tec", initial=None if data else technique_initial)
    images = ImageRows(data, files, prefix="img")

    if request.method == "POST":
        publish = request.POST.get("action") != "draft"
        materials.require_one = publish
        valid = all([f.is_valid() for f in (form, attr_form, materials, techniques, images)])
        if valid:
            with transaction.atomic():
                craft = form.save(commit=False)
                if not editing:
                    craft.created_by = request.user
                craft.attributes = attr_form.json_values()
                craft.status = Craft.Status.PUBLISHED if publish else Craft.Status.DRAFT
                craft.save()
                _save_rows(craft, materials.filled_rows(), techniques.filled_rows())
                _save_images(request, craft, images)
            if publish:
                messages.success(request, f"“{craft.title}” is published.")
            else:
                messages.success(
                    request, f"“{craft.title}” is saved as a draft. Only you can see it."
                )
            return redirect(craft)
        messages.error(request, "Please fix the highlighted fields below.")

    return render(
        request,
        "crafts/form.html",
        {
            "form": form,
            "attr_form": attr_form,
            "materials": materials,
            "techniques": techniques,
            "images": images,
            "craft": craft,
            "editing": editing,
            "material_names": Material.objects.values_list("name", flat=True),
            "technique_names": Technique.objects.values_list("name", flat=True),
        },
    )


def _save_rows(craft, material_rows, technique_rows):
    craft.craft_materials.all().delete()
    for order, row in enumerate(material_rows):
        material = Material.objects.filter(name__iexact=row["name"]).first()
        material = material or Material.objects.create(name=row["name"])
        CraftMaterial.objects.create(
            craft=craft,
            material=material,
            origin=row.get("origin", ""),
            notes=row.get("notes", ""),
            order=order,
        )
    craft.craft_techniques.all().delete()
    for order, row in enumerate(technique_rows):
        technique = Technique.objects.filter(name__iexact=row["name"]).first()
        technique = technique or Technique.objects.create(name=row["name"])
        CraftTechnique.objects.create(
            craft=craft, technique=technique, notes=row.get("notes", ""), order=order
        )


def _save_images(request, craft, images):
    remove_ids = request.POST.getlist("remove_media")
    if remove_ids:
        craft.media.filter(pk__in=remove_ids).delete()
    for media in craft.media.all():  # alt text edits on existing photos
        alt = request.POST.get(f"media-{media.pk}-alt_text")
        if alt is not None and alt.strip() and alt.strip() != media.alt_text:
            media.alt_text = alt.strip()
            media.save(update_fields=["alt_text"])
    next_order = (craft.media.order_by("-order").values_list("order", flat=True).first() or 0) + 1
    for form in images:
        upload = form.cleaned_data.get("image") if form.is_valid() else None
        if not upload:
            continue
        content, name = resized_image(upload)
        media = Media(
            craft=craft,
            alt_text=form.cleaned_data["alt_text"].strip(),
            credit=form.cleaned_data.get("credit", ""),
            caption=form.cleaned_data.get("caption", ""),
            order=next_order,
        )
        media.image.save(name, content, save=True)
        next_order += 1


@login_required
def craft_create(request):
    return _craft_form_page(request)


@login_required
def craft_edit(request, slug):
    craft = get_object_or_404(Craft, slug=slug)
    if not can_edit(request.user, craft):
        raise Http404
    return _craft_form_page(request, craft)


@login_required
def craft_delete(request, slug):
    craft = get_object_or_404(Craft, slug=slug)
    if not can_edit(request.user, craft):
        raise Http404
    if request.method == "POST":
        title = craft.title
        craft.delete()
        messages.success(request, f"“{title}” was deleted.")
        return redirect("crafts:mine")
    return render(request, "crafts/confirm_delete.html", {"craft": craft})


@login_required
def my_crafts(request):
    crafts = (
        Craft.objects.filter(created_by=request.user)
        .select_related("craft_type", "community")
        .prefetch_related("media")
        .order_by("-updated_at")
    )
    return render(request, "crafts/mine.html", {"crafts": crafts})


@require_GET
@login_required
def attribute_fields(request):
    """Partial HTML: the craft-type-specific fields for the chosen type (US-11)."""
    craft_type = craft_type_from(request.GET)
    values = None
    slug = request.GET.get("craft")
    if slug:
        craft = Craft.objects.filter(slug=slug).first()
        if (
            craft
            and can_edit(request.user, craft)
            and craft.craft_type_id == getattr(craft_type, "pk", None)
        ):
            values = craft.attributes
    return render(
        request,
        "crafts/_attribute_fields.html",
        {"attr_form": AttributesForm(craft_type=craft_type, values=values)},
    )
