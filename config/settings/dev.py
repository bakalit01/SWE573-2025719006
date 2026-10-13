from .base import *  # noqa: F403
from .base import STORAGES

DEBUG = True
ALLOWED_HOSTS = ["*"]
STORAGES = {
    **STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
