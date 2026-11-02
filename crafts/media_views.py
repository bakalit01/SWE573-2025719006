"""Uploaded photos are served only to people who may see their craft (US-22)."""

from django.conf import settings
from django.http import Http404
from django.views.static import serve

from .models import Craft, Media


def protected_media(request, path):
    media = Media.objects.filter(image=path).only("craft_id").first()
    visible = Craft.objects.visible_to(request.user)
    if media is None or not visible.filter(pk=media.craft_id).exists():
        raise Http404

    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response["Cache-Control"] = "private, max-age=3600"
    return response
