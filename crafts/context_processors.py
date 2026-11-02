from django.conf import settings

from accounts.permissions import can_contribute, is_site_admin, stewarded_community_ids


def site(request):
    user = getattr(request, "user", None)
    return {
        "REPO_URL": settings.REPO_URL,
        "APP_VERSION": settings.APP_VERSION,
        "user_can_contribute": can_contribute(user),
        "user_is_reviewer": is_site_admin(user) or bool(stewarded_community_ids(user)),
    }
