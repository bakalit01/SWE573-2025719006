from django.conf import settings


def site(request):
    return {"REPO_URL": settings.REPO_URL, "APP_VERSION": settings.APP_VERSION}
