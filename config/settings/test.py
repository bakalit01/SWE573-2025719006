from .base import *  # noqa: F403
from .base import STORAGES

DEBUG = False
ALLOWED_HOSTS = ["*"]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]  # fast tests only
STORAGES = {
    **STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# WhiteNoise is only needed when serving collected static files (production).
MIDDLEWARE = [m for m in MIDDLEWARE if not m.startswith("whitenoise")]  # noqa: F405
