"""Members' stories on craft pages."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.permissions import can_add_story, can_moderate_story

from .forms import StoryForm
from .models import Craft, CraftStory


def visible_stories(craft, user):
    """Everyone sees shown stories; authors also see their own hidden ones; reviewers see all."""
    stories = craft.stories.select_related("author")
    if user.is_authenticated and can_moderate_story(user, CraftStory(craft=craft)):
        return stories
    if user.is_authenticated:
        return stories.filter(is_hidden=False) | stories.filter(author=user)
    return stories.filter(is_hidden=False)


@require_POST
@login_required
def add_story(request, slug):
    craft = get_object_or_404(Craft.objects.visible_to(request.user), slug=slug)
    if not can_add_story(request.user):
        raise Http404
    form = StoryForm(request.POST)
    if not form.is_valid():
        messages.error(
            request, "Your story wasn't saved: choose your connection and write a story."
        )
        return redirect(craft.get_absolute_url() + "#stories")
    story = form.save(commit=False)
    story.craft = craft
    story.author = request.user
    story.save()
    owner = craft.created_by
    if owner and owner.email and owner != request.user:
        send_mail(
            f"A new story on “{craft.title}”",
            f"{request.user.public_name} shared a story on “{craft.title}”:\n\n{story.text}\n\n"
            f"{request.build_absolute_uri(craft.get_absolute_url())}#stories",
            settings.DEFAULT_FROM_EMAIL,
            [owner.email],
            fail_silently=True,
        )
    messages.success(request, "Thank you for sharing your story.")
    return redirect(craft.get_absolute_url() + f"#story-{story.pk}")


@login_required
def edit_story(request, pk):
    story = get_object_or_404(
        CraftStory.objects.select_related("craft"), pk=pk, author=request.user
    )
    form = StoryForm(request.POST or None, instance=story)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your story is updated.")
        return redirect(story.craft.get_absolute_url() + f"#story-{story.pk}")
    return render(request, "crafts/story_edit.html", {"form": form, "story": story})


@require_POST
@login_required
def delete_story(request, pk):
    story = get_object_or_404(
        CraftStory.objects.select_related("craft"), pk=pk, author=request.user
    )
    craft = story.craft
    story.delete()
    messages.success(request, "Your story is deleted.")
    return redirect(craft.get_absolute_url() + "#stories")


@require_POST
@login_required
def moderate_story(request, pk):
    """Stewards of the craft's community and admins hide or show a story."""
    story = get_object_or_404(CraftStory.objects.select_related("craft"), pk=pk)
    if not can_moderate_story(request.user, story):
        raise Http404
    hide = request.POST.get("action") == "hide"
    story.is_hidden = hide
    story.hidden_by = request.user if hide else None
    story.hidden_reason = request.POST.get("reason", "").strip()[:300] if hide else ""
    story.save()
    messages.success(request, "The story is hidden." if hide else "The story is shown again.")
    return redirect(request.POST.get("next") or story.craft.get_absolute_url() + "#stories")
