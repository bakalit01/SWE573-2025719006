from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path

from crafts import views as craft_views
from crafts.media_views import protected_media


def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("", craft_views.home, name="home"),
    path("crafts/", include("crafts.urls")),
    path("communities/", include("communities.urls")),
    path("", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("healthz", healthz, name="healthz"),
]

if settings.DEBUG or settings.SERVE_MEDIA:
    # Without object storage, Django serves uploaded photos itself, checking that the
    # viewer may see the craft each photo belongs to.
    urlpatterns += [re_path(r"^media/(?P<path>.+)$", protected_media, name="media")]
