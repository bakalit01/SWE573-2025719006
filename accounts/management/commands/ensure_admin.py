"""Create or repair the site's admin account from environment variables.

Used on Render start-up (render.yaml), where there is no shell to run
createsuperuser. Set DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD.
Every run makes sure the account exists, is active, is an admin and has that
password, so changing the variable and redeploying resets a lost password.
"""

import os

from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = "Create or update the admin account from DJANGO_SUPERUSER_EMAIL / _PASSWORD."

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip().lower()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        if not email or not password:
            self.stdout.write(
                "ensure_admin: DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD "
                "are not both set; no admin account created."
            )
            return
        if len(password) < 10:
            self.stdout.write("ensure_admin: the password must be at least 10 characters; skipped.")
            return

        user = User.objects.filter(email__iexact=email).first()
        created = user is None
        if created:
            user = User(email=email)
        user.role = User.Role.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        action = "created" if created else "updated (password and admin rights reset)"
        self.stdout.write(f"ensure_admin: admin account {email} {action}.")
