from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    """Users log in with their email address; there is no username."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("An email address is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if not extra["is_staff"] or not extra["is_superuser"]:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    community = models.ForeignKey(
        "communities.Community",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
        help_text="Community the user belongs to or works with (optional)",
    )
    location = models.CharField(max_length=120, blank=True, help_text="City or region (optional)")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})

    @property
    def public_name(self):
        """Name shown in the header and on credits; falls back to the email's local part."""
        return self.display_name or self.get_full_name() or self.email.split("@")[0]
