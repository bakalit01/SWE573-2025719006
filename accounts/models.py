from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    """Users log in with their email address; there is no username."""

    use_in_migrations = True

    def get_by_natural_key(self, email):
        # Email addresses are matched without regard to capital letters, so
        # "Ege@…" and "ege@…" are the same account (the admin login uses this).
        return self.get(email__iexact=email)

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("An email address is required")
        email = self.normalize_email(email).lower()
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
        extra.setdefault("role", "admin")
        if not extra["is_staff"] or not extra["is_superuser"]:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    """Platform user. The role decides what they may do (US-05); see accounts/permissions.py."""

    class Role(models.TextChoices):
        MEMBER = "member", "Member: browse, including members-only records"
        MAKER = "maker", "Maker: also add and edit their own crafts"
        STEWARD = "steward", "Community steward: also review their communities' records"
        ADMIN = "admin", "Admin: manage everything"

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
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MAKER,
        help_text="Stewards also need communities assigned (Communities → stewards).",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loaded = {"role": self.role, "is_active": self.is_active}
        self.changed_by = None  # set by the admin so the log records who made a change

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Admins get the admin site; demoted admins lose it (superusers keep it).
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        elif self._loaded["role"] == self.Role.ADMIN and not self.is_superuser:
            self.is_staff = False
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if not is_new:
            for field in ("role", "is_active"):
                old, new = self._loaded[field], getattr(self, field)
                if old != new:
                    AccountChange.objects.create(
                        user=self,
                        field=field,
                        old_value=str(old),
                        new_value=str(new),
                        changed_by=self.changed_by,
                    )
        self._loaded = {"role": self.role, "is_active": self.is_active}

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})

    @property
    def public_name(self):
        """Name shown in the header and on credits; falls back to the email's local part."""
        return self.display_name or self.get_full_name() or self.email.split("@")[0]


class AccountChange(models.Model):
    """Log of role changes and suspensions (US-27: "role changes are logged")."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_changes")
    field = models.CharField(max_length=20)
    old_value = models.CharField(max_length=40)
    new_value = models.CharField(max_length=40)
    changed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.user}: {self.field} {self.old_value} → {self.new_value}"
