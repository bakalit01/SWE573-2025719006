from urllib.parse import urlencode

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from communities.models import Community

from .models import Craft, CraftType

PAGE_SIZE = 24


def _visible(request):
    return (
        Craft.objects.visible_to(request.user)
        .select_related("craft_type", "community")
        .prefetch_related("media")
    )


def home(request):
    crafts = _visible(request)
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
    crafts = _visible(request)
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


def craft_detail(request, slug):
    # Crafts the user may not see return 404, never "forbidden" (US-07).
    craft = get_object_or_404(
        _visible(request).prefetch_related("materials", "techniques"), slug=slug
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
        {"craft": craft, "attribute_rows": craft.attribute_rows(), "report_url": report_url},
    )
