from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import can_edit_community
from crafts.models import Craft

from .forms import CommunityForm
from .models import Community


def community_detail(request, slug):
    """US-17: the community's own name first, its description, and its crafts."""
    community = get_object_or_404(Community, slug=slug)
    crafts = (
        Craft.objects.listed_for(request.user)
        .filter(community=community)
        .select_related("craft_type", "community")
        .prefetch_related("media")
    )
    return render(
        request,
        "communities/detail.html",
        {
            "community": community,
            "other_names": [n.strip() for n in community.other_names.split(",") if n.strip()],
            "crafts": crafts,
            "stewards": community.stewards.filter(is_active=True),
            "can_edit": can_edit_community(request.user, community),
        },
    )


@login_required
def community_edit(request, slug):
    community = get_object_or_404(Community, slug=slug)
    if not can_edit_community(request.user, community):
        raise Http404
    form = CommunityForm(request.POST or None, instance=community)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"The {community.name} page is updated.")
        return redirect(community)
    return render(request, "communities/edit.html", {"community": community, "form": form})
