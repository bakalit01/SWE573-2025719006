"""Log in the site admin defined by environment variables.

On Render the start command may not be the one in render.yaml (a service made
by hand, or a blueprint that has not synced), so ensure_admin may never run.
This backend makes the variables enough on their own: logging in with exactly
DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD creates or repairs that
admin account. Any other login falls through to the normal backends.
"""

import os
from hmac import compare_digest

from accounts.models import User


def admin_credentials():
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip().lower()
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "").strip()
    if not email or len(password) < 10:
        return None, None
    return email, password


def ensure_admin_account(email, password):
    """Create the admin account, or make sure it is an active admin with this password."""
    user = User.objects.filter(email__iexact=email).first()
    created = user is None
    if created:
        user = User(email=email)
    user.role = User.Role.ADMIN
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    if created or not user.check_password(password):
        user.set_password(password)
    user.save()
    return user, created


class EnvAdminBackend:
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        typed = (username or email or "").strip().lower()
        env_email, env_password = admin_credentials()
        if not env_email or not typed or password is None:
            return None
        if typed != env_email or not compare_digest(password.strip(), env_password):
            return None
        user, _ = ensure_admin_account(env_email, env_password)
        return user

    def get_user(self, user_id):
        user = User.objects.filter(pk=user_id).first()
        return user if user and user.is_active else None
