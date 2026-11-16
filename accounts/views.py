from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from crafts.models import Craft

from .forms import ProfileForm
from .models import User


def profile(request, pk):
    """Public maker profile (US-04): who they are and the crafts they added."""
    maker = get_object_or_404(User.objects.select_related("community"), pk=pk, is_active=True)
    crafts = (
        Craft.objects.listed_for(request.user)
        .filter(created_by=maker)
        .select_related("craft_type", "community")
        .prefetch_related("media")
    )
    return render(request, "accounts/profile.html", {"maker": maker, "crafts": crafts})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile is updated.")
        return redirect(request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})
