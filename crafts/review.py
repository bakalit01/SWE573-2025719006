"""Publishing workflow (US-23, US-24, US-25): who publishes directly, who goes to review,
what a decision does, and who is told.

- Makers submit; the record waits as "Pending review" for the community's stewards.
- Stewards of the craft's community, and admins, publish directly.
- Edits by makers to a published record send it back to review.
- A decision (approve, request changes, reject, unpublish) is recorded and e-mailed to the
  author; new submissions and reports are e-mailed to the community's reviewers.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from accounts.permissions import can_review, is_site_admin, stewarded_community_ids

from .models import Craft, Report, ReviewDecision


def status_after_submit(user, craft):
    return Craft.Status.PUBLISHED if can_review(user, craft) else Craft.Status.PENDING


def reviewers_for(community_id):
    """Active stewards of the community, plus admins."""
    return (
        User.objects.filter(is_active=True)
        .filter(
            Q(role=User.Role.STEWARD, stewarded_communities=community_id)
            | Q(role=User.Role.ADMIN)
            | Q(is_superuser=True)
        )
        .distinct()
    )


def _mail(recipients, subject, body):
    emails = sorted({e for e in recipients if e})
    if emails:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, emails, fail_silently=True)


def notify_reviewers(request, craft, subject, body):
    link = request.build_absolute_uri(craft.get_absolute_url())
    queue = request.build_absolute_uri(reverse("crafts:review_queue"))
    _mail(
        reviewers_for(craft.community_id).values_list("email", flat=True),
        subject,
        f"{body}\n\n{link}\n\nReview queue: {queue}",
    )


def decide(request, craft, decision, comment=""):
    """Record a decision, change the craft's status and tell the author."""
    ReviewDecision.objects.create(
        craft=craft, reviewer=request.user, decision=decision, comment=comment
    )
    craft.status = ReviewDecision.NEW_STATUS[decision]
    craft.save(update_fields=["status", "updated_at"])
    author = craft.created_by
    if author and author.email and author != request.user:
        label = ReviewDecision.Decision(decision).label
        note = f"\n\nNote from the reviewer:\n{comment}" if comment else ""
        _mail(
            [author.email],
            f"“{craft.title}”: {label.lower()}",
            f"Your craft “{craft.title}” was reviewed: {label}.{note}\n\n"
            f"{request.build_absolute_uri(craft.get_absolute_url())}",
        )


def resolve_report(request, report, note=""):
    report.status = Report.Status.RESOLVED
    report.resolved_by = request.user
    report.resolved_at = timezone.now()
    report.resolution_note = note
    report.save()


def queue_filter(user):
    """Q for crafts in the communities this user reviews (all, for admins)."""
    if is_site_admin(user):
        return Q()
    return Q(community_id__in=stewarded_community_ids(user))


def pending_for(user):
    return Craft.objects.filter(queue_filter(user), status=Craft.Status.PENDING)


def open_reports_for(user):
    crafts = Craft.objects.filter(queue_filter(user)).values("pk")
    return Report.objects.filter(status=Report.Status.OPEN, craft__in=crafts)
