"""Create or repair the site's admin account from environment variables.

Runs on Render start-up (render.yaml). Set DJANGO_SUPERUSER_EMAIL and
DJANGO_SUPERUSER_PASSWORD. Logging in with those values also works on its own
(accounts/backends.py), in case the start command does not run this.
"""

from django.core.management.base import BaseCommand

from accounts.backends import admin_credentials, ensure_admin_account


class Command(BaseCommand):
    help = "Create or update the admin account from DJANGO_SUPERUSER_EMAIL / _PASSWORD."

    def handle(self, *args, **options):
        email, password = admin_credentials()
        if not email:
            self.stdout.write(
                "ensure_admin: DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD "
                "(10+ characters) "
                "are not both set; no admin account created."
            )
            return
        _, created = ensure_admin_account(email, password)
        action = "created" if created else "updated (password and admin rights reset)"
        self.stdout.write(f"ensure_admin: admin account {email} {action}.")
