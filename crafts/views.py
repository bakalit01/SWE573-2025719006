from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, F, Q
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from accounts.permissions import (
    can_contribute,
    can_delete,
    can_edit,
    can_review,
    is_site_admin,
    stewarded_community_ids,
)
from communities.models import Community

from . import review
from .forms import (
    OTHER,
    AttributesForm,
    ConsentForm,
    CraftForm,
    DecisionForm,
    DetailRows,
    ImageRows,
    MaterialRows,
    TechniqueRows,
    craft_type_from,
    resized_image,
)
from .models import (
    Craft,
    CraftMaterial,
    CraftTechnique,
    CraftType,
    Material,
    Media,
    Tag,
    Technique,
)

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


SEARCH_FIELDS = [
    "title",
    "summary",
    "description",
    "process",
    "cultural_context",
    "maker_credit",
    "place_name",
    "country",
    "community__name",
    "community__other_names",
    "craft_type__name",
    "craft_materials__material__name",
    "craft_techniques__technique__name",
    "tags__name",
]
SORTS = {
    "relevance": "Best match",
    "title": "Name (A–Z)",
    "recent": "Recently added",
    "oldest": "Oldest made first",
    "newest": "Newest made first",
}


def search(crafts, query):
    """US-15: every word must appear somewhere (names, text, materials, techniques, community,
    tags); results are ranked by full-text relevance of the craft's own text."""
    words = query.split()[:8]
    for word in words:
        match = Q()
        for field in SEARCH_FIELDS:
            match |= Q(**{f"{field}__icontains": word})
        crafts = crafts.filter(pk__in=Craft.objects.filter(match).values("pk"))
    vector = SearchVector("title", weight="A", config="simple") + SearchVector(
        "summary", "description", "process", "cultural_context", weight="B", config="simple"
    )
    return crafts.annotate(rank=SearchRank(vector, SearchQuery(" ".join(words), config="simple")))


def craft_list(request):
    visible = _listed(request)
    crafts = visible
    get = request.GET
    query = " ".join(get.get("q", "").split())[:100]
    craft_type = get.get("type", "")
    community = get.get("community", "")
    material = get.get("material", "")
    technique = get.get("technique", "")
    country = get.get("country", "")
    # Tag search: an exact tag (from a tag link or a suggestion), else any tag containing the text.
    tag_query = " ".join(get.get("tag", "").lstrip("#").split())
    tag = (
        Tag.objects.filter(Q(slug=tag_query) | Q(name__iexact=tag_query)).first()
        if tag_query
        else None
    )
    if query:
        crafts = search(crafts, query)
    if craft_type:
        crafts = crafts.filter(craft_type__slug=craft_type)
    if community:
        crafts = crafts.filter(community__slug=community)
    if material:
        crafts = crafts.filter(
            pk__in=CraftMaterial.objects.filter(material__name__iexact=material).values("craft")
        )
    if technique:
        crafts = crafts.filter(
            pk__in=CraftTechnique.objects.filter(technique__name__iexact=technique).values("craft")
        )
    if country:
        crafts = crafts.filter(country__iexact=country)
    if tag:
        crafts = crafts.filter(tags=tag)
    elif tag_query:
        crafts = crafts.filter(
            pk__in=Craft.objects.filter(tags__name__icontains=tag_query).values("pk")
        )

    sort = get.get("sort") or ("relevance" if query else "title")
    if sort not in SORTS or (sort == "relevance" and not query):
        sort = "title"
    crafts = crafts.order_by(
        *{
            "relevance": [F("rank").desc(), "title"] if query else ["title"],
            "title": [Lower("title")],
            "recent": ["-created_at"],
            "oldest": [F("year_made").asc(nulls_last=True), "title"],
            "newest": [F("year_made").desc(nulls_last=True), "title"],
        }[sort]
    )

    page = Paginator(crafts, PAGE_SIZE).get_page(get.get("page"))
    selected = {
        "q": query,
        "type": craft_type,
        "community": community,
        "material": material,
        "technique": technique,
        "country": country,
        "tag": tag.slug if tag else tag_query,
    }
    filters = {k: v for k, v in selected.items() if v}
    if sort != ("relevance" if query else "title"):
        filters["sort"] = sort
    visible_ids = visible.values("pk")
    return render(
        request,
        "crafts/list.html",
        {
            "page": page,
            "crafts": page.object_list,
            "query": query,
            "craft_types": CraftType.objects.filter(crafts__in=visible_ids).distinct(),
            "communities": Community.objects.filter(crafts__in=visible_ids).distinct(),
            "materials": Material.objects.filter(crafts__in=visible_ids)
            .distinct()
            .order_by(Lower("name")),
            "techniques": Technique.objects.filter(crafts__in=visible_ids)
            .distinct()
            .order_by(Lower("name")),
            "countries": visible.exclude(country="")
            .order_by("country")
            .values_list("country", flat=True)
            .distinct(),
            "selected": selected,
            "tag_value": tag.name if tag else tag_query,
            "tag_options": Tag.objects.filter(crafts__in=visible_ids)
            .distinct()
            .order_by(Lower("name")),  # only tags on crafts this user can see
            "sorts": [(k, v) for k, v in SORTS.items() if k != "relevance" or query],
            "sort": sort,
            "any_filter": bool(filters),
            "other_filters": any(v for k, v in filters.items() if k not in ("q", "sort")),
            "filter_query": urlencode(filters),
        },
    )


def craft_detail(request, slug):
    # Crafts the user may not see return 404, never "forbidden" (US-07).
    craft = get_object_or_404(
        Craft.objects.visible_to(request.user)
        .select_related("craft_type", "community", "created_by")
        .prefetch_related(
            "media", "tags", "craft_materials__material", "craft_techniques__technique"
        ),
        slug=slug,
    )
    reviewer = can_review(request.user, craft)
    is_author = request.user.is_authenticated and craft.created_by_id == request.user.pk
    return render(
        request,
        "crafts/detail.html",
        {
            "craft": craft,
            "attribute_rows": craft.attribute_rows(),
            "report_url": reverse("crafts:report", args=[craft.slug]),
            "can_edit": can_edit(request.user, craft),
            "map_point": craft.map_point,
            "is_reviewer": reviewer,
            "consent": getattr(craft, "consent", None) if reviewer else None,
            "decisions": craft.decisions.select_related("reviewer")[:5]
            if (reviewer or is_author)
            else [],
            "decision_form": DecisionForm() if reviewer else None,
            "open_reports": craft.reports.filter(status="open") if reviewer else [],
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

    form = CraftForm(data, instance=craft, user=request.user)
    craft_type = craft_type_from(data, craft)
    attr_form = AttributesForm(
        data, craft_type=craft_type, values=craft.attributes if craft else None
    )
    material_initial, technique_initial = _row_initial(craft)
    materials = MaterialRows(data, prefix="mat", initial=None if data else material_initial)
    techniques = TechniqueRows(data, prefix="tec", initial=None if data else technique_initial)
    details = DetailRows(
        data, prefix="det", initial=None if data else (craft.extra_details if craft else None)
    )
    images = ImageRows(data, files, prefix="img")
    existing_consent = getattr(craft, "consent", None) if editing else None
    consent_form = ConsentForm(data, instance=existing_consent)

    if request.method == "POST":
        submit = request.POST.get("action") != "draft"
        materials.require_one = submit
        consent_form.require = submit
        parts = (form, attr_form, materials, techniques, details, images, consent_form)
        valid = all([f.is_valid() for f in parts])
        if valid:
            was_published = editing and craft.status == Craft.Status.PUBLISHED
            with transaction.atomic():
                craft = form.save(commit=False)
                if not editing:
                    craft.created_by = request.user
                craft.attributes = attr_form.json_values()
                craft.extra_details = details.json_values()
                craft.status = (
                    review.status_after_submit(request.user, craft)
                    if submit
                    else Craft.Status.DRAFT
                )
                craft.save()
                form.save_tags(craft)
                _save_rows(craft, materials.filled_rows(), techniques.filled_rows())
                _save_images(request, craft, images)
                if consent_form.has_data:
                    consent = consent_form.save(commit=False)
                    consent.craft = craft
                    consent.recorded_by = consent.recorded_by or request.user
                    consent.save()
            if craft.status == Craft.Status.PUBLISHED:
                messages.success(request, f"“{craft.title}” is published.")
            elif craft.status == Craft.Status.PENDING:
                review.notify_reviewers(
                    request,
                    craft,
                    f"Review needed: “{craft.title}”",
                    f"{request.user.public_name} submitted “{craft.title}” "
                    f"({craft.community.name}) for review.",
                )
                messages.success(
                    request,
                    f"“{craft.title}” is sent to the {craft.community.name} stewards for review."
                    + (" It is hidden from others until approved." if was_published else "")
                    + " You'll get an e-mail when they decide.",
                )
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
            "details": details,
            "images": images,
            "craft": craft,
            "editing": editing,
            "consent_form": consent_form,
            "publishes_directly": is_site_admin(request.user)
            or bool(stewarded_community_ids(request.user)),
            "new_type": form.new_type_chosen,
            "popular_tags": Tag.objects.annotate(n=Count("crafts")).order_by("-n", Lower("name"))[
                :12
            ],
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
    if not can_contribute(request.user):
        raise PermissionDenied("Your account can browse crafts but not add them.")
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
    if not can_delete(request.user, craft):
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
        .prefetch_related("media", "decisions")
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
        {
            "attr_form": AttributesForm(craft_type=craft_type, values=values),
            "new_type": request.GET.get("craft_type") == OTHER,
        },
    )
