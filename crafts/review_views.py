"""Steward review queue, decisions and reports (US-24, US-25)."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.permissions import can_review, is_site_admin, stewarded_community_ids

from . import review
from .forms import DecisionForm, ReportForm
from .models import Craft, Report, ReviewDecision


def _require_reviewer(user):
    if not (is_site_admin(user) or stewarded_community_ids(user)):
        raise PermissionDenied("The review queue is for community stewards and admins.")


@login_required
def review_queue(request):
    _require_reviewer(request.user)
    pending = (
        review.pending_for(request.user)
        .select_related("community", "craft_type", "created_by", "consent")
        .order_by("updated_at")
    )
    reports = review.open_reports_for(request.user).select_related("craft", "craft__community")
    recent = ReviewDecision.objects.filter(
        craft__in=Craft.objects.filter(review.queue_filter(request.user)).values("pk")
    ).select_related("craft", "reviewer")[:10]
    communities = (
        "all communities"
        if is_site_admin(request.user)
        else ", ".join(request.user.stewarded_communities.values_list("name", flat=True))
    )
    return render(
        request,
        "crafts/review_queue.html",
        {"pending": pending, "reports": reports, "recent": recent, "communities": communities},
    )


@require_POST
@login_required
def review_craft(request, slug):
    craft = get_object_or_404(Craft, slug=slug)
    if not can_review(request.user, craft):
        raise Http404
    form = DecisionForm(request.POST)
    if not form.is_valid():
        errors = "; ".join(e for errs in form.errors.values() for e in errs)
        messages.error(request, f"Decision not saved: {errors}")
        return redirect(craft)
    decision = form.cleaned_data["decision"]
    review.decide(request, craft, decision, form.cleaned_data["comment"].strip())
    messages.success(
        request, f"“{craft.title}”: {ReviewDecision.Decision(decision).label.lower()}."
    )
    return redirect("crafts:review_queue")


def report_craft(request, slug):
    """US-25: anyone who can see a craft can report it, without logging in."""
    craft = get_object_or_404(Craft.objects.visible_to(request.user), slug=slug)
    form = ReportForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not form.is_spam:
            report = form.save(commit=False)
            report.craft = craft
            if request.user.is_authenticated:
                report.reporter = request.user
            report.save()
            review.notify_reviewers(
                request,
                craft,
                f"Report on “{craft.title}”",
                f"Someone reported “{craft.title}”: {report.get_reason_display()}.\n\n"
                f"{report.details}",
            )
        messages.success(
            request,
            "Thank you. The community's stewards and the site admins have been told and will "
            "look at it.",
        )
        return redirect(craft)
    return render(request, "crafts/report_form.html", {"craft": craft, "form": form})


@require_POST
@login_required
def handle_report(request, pk):
    report = get_object_or_404(Report.objects.select_related("craft"), pk=pk)
    if not can_review(request.user, report.craft):
        raise Http404
    note = request.POST.get("note", "").strip()
    if request.POST.get("action") == "unpublish":
        review.decide(
            request,
            report.craft,
            ReviewDecision.Decision.UNPUBLISHED,
            note or f"Unpublished after a report: {report.get_reason_display()}.",
        )
        review.resolve_report(request, report, note or "Craft unpublished.")
        messages.success(request, f"“{report.craft.title}” is unpublished.")
    else:
        review.resolve_report(request, report, note)
        messages.success(request, "Report marked as resolved.")
    return redirect("crafts:review_queue")
