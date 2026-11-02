from django.conf import settings

from accounts.permissions import can_contribute, is_site_admin, stewarded_community_ids


def site(request):
    user = getattr(request, "user", None)
    is_reviewer = is_site_admin(user) or bool(stewarded_community_ids(user))
    review_count = 0
    if is_reviewer:
        from .review import open_reports_for, pending_for

        review_count = pending_for(user).count() + open_reports_for(user).count()
    return {
        "REPO_URL": settings.REPO_URL,
        "APP_VERSION": settings.APP_VERSION,
        "APP_COMMIT": settings.APP_COMMIT,
        "user_can_contribute": can_contribute(user),
        "user_is_reviewer": is_reviewer,
        "review_count": review_count,
    }
