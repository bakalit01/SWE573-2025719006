"""Favourites and collections (US-18).

Members save crafts with ♡ and group them into named collections. Collections are private
by default; an owner can show one on their profile. Every list is filtered through
`Craft.objects.visible_to`, so a craft someone can no longer see drops out of their
favourites and collections without being deleted from them.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CollectionForm
from .models import Collection, Craft, Favourite


def _back(request, fallback):
    target = request.POST.get("next") or request.GET.get("next")
    if target and url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(target)
    return redirect(fallback)


def _visible_craft(request, slug):
    return get_object_or_404(Craft.objects.visible_to(request.user), slug=slug)


def with_visible_counts(collections, viewer):
    visible = Craft.objects.visible_to(viewer).values("pk")
    return collections.annotate(
        n_visible=Count("crafts", filter=Q(crafts__in=visible), distinct=True)
    )


@login_required
def saved(request):
    """The member's own page: favourites, then collections."""
    favourites = (
        Craft.objects.visible_to(request.user)
        .filter(favourited_by__user=request.user)
        .select_related("craft_type", "community")
        .prefetch_related("media", "names")
        .order_by("-favourited_by__created_at")
    )
    collections = with_visible_counts(request.user.collections.all(), request.user)
    form = CollectionForm(owner=request.user)
    return render(
        request,
        "crafts/saved.html",
        {"favourites": favourites, "collections": collections, "form": form},
    )


@require_POST
@login_required
def collection_create(request):
    form = CollectionForm(request.POST, owner=request.user)
    if form.is_valid():
        collection = form.save()
        messages.success(request, f"Collection “{collection.name}” created.")
        return redirect(collection)
    favourites = Craft.objects.none()
    collections = with_visible_counts(request.user.collections.all(), request.user)
    return render(
        request,
        "crafts/saved.html",
        {"favourites": favourites, "collections": collections, "form": form},
        status=400,
    )


def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.select_related("owner"), pk=pk)
    if not collection.can_view(request.user):
        raise Http404
    is_owner = request.user.is_authenticated and request.user.pk == collection.owner_id
    crafts = (
        collection.visible_crafts(request.user)
        .select_related("craft_type", "community")
        .prefetch_related("media", "names")
        .order_by("title")
    )
    return render(
        request,
        "crafts/collection_detail.html",
        {
            "collection": collection,
            "crafts": crafts,
            "is_owner": is_owner,
            "form": CollectionForm(instance=collection, owner=request.user) if is_owner else None,
        },
    )


def _own_collection(request, pk):
    return get_object_or_404(Collection, pk=pk, owner=request.user)


@require_POST
@login_required
def collection_edit(request, pk):
    collection = _own_collection(request, pk)
    form = CollectionForm(request.POST, instance=collection, owner=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Collection saved.")
    else:
        messages.error(request, " ".join(e for errors in form.errors.values() for e in errors))
    return redirect(collection)


@require_POST
@login_required
def collection_delete(request, pk):
    collection = _own_collection(request, pk)
    name = collection.name
    collection.delete()  # the crafts themselves are untouched
    messages.success(request, f"Collection “{name}” deleted.")
    return redirect("collections:saved")


@require_POST
@login_required
def collection_remove(request, pk, slug):
    collection = _own_collection(request, pk)
    craft = get_object_or_404(Craft, slug=slug)
    collection.crafts.remove(craft)
    messages.success(request, f"Removed “{craft.title}” from “{collection.name}”.")
    return _back(request, collection.get_absolute_url())


@require_POST
@login_required
def toggle_favourite(request, slug):
    craft = _visible_craft(request, slug)
    favourite = Favourite.objects.filter(user=request.user, craft=craft)
    if favourite.exists():
        favourite.delete()
        messages.success(request, f"Removed “{craft.title}” from your favourites.")
    else:
        try:
            with transaction.atomic():
                Favourite.objects.create(user=request.user, craft=craft)
        except IntegrityError:  # a double click
            pass
        messages.success(request, f"Saved “{craft.title}” to your favourites.")
    return _back(request, craft.get_absolute_url())


@require_POST
@login_required
def craft_collections(request, slug):
    """Set which of my collections hold this craft; optionally start a new one."""
    craft = _visible_craft(request, slug)
    mine = request.user.collections.all()
    chosen = set(request.POST.getlist("collection"))
    for collection in mine:
        if str(collection.pk) in chosen:
            collection.crafts.add(craft)
        else:
            collection.crafts.remove(craft)
    new_name = " ".join(request.POST.get("new_collection", "").split())
    if new_name:
        form = CollectionForm({"name": new_name}, owner=request.user)
        if form.is_valid():
            form.save().crafts.add(craft)
        else:
            messages.error(request, " ".join(form.errors.get("name", [])))
            return redirect(craft)
    in_count = mine.filter(crafts=craft).count()
    messages.success(
        request,
        f"“{craft.title}” is in {in_count} of your collections."
        if in_count
        else f"“{craft.title}” is not in any of your collections.",
    )
    return redirect(reverse("crafts:detail", args=[craft.slug]))
