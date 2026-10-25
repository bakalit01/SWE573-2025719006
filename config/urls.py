from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.views.static import serve

from crafts import views as craft_views


def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("", craft_views.home, name="home"),
    path("crafts/", include("crafts.urls")),
    path("", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("healthz", healthz, name="healthz"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.SERVE_MEDIA:
    # Demo hosting without object storage: Django serves uploaded photos itself.
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
