from django.conf import settings
from django.db import models
from django.urls import reverse


class Region(models.Model):
    """A region communities belong to, managed by admins (US-28)."""

    name = models.CharField(max_length=200, unique=True)
    other_names = models.CharField(
        "Other names or spellings",
        max_length=300,
        blank=True,
        help_text="Comma-separated; search finds the region by these too",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @classmethod
    def for_name(cls, name):
        """The region with this name or alternate spelling, created if it is new."""
        from crafts.terms import find_term

        name = " ".join((name or "").split())[:200]
        if not name:
            return None
        return find_term(cls, name) or cls.objects.create(name=name)


class Community(models.Model):
    """A community or nation. `name` is the community's own (self-designated) name."""

    name = models.CharField(max_length=200, unique=True, help_text="Self-designated name")
    slug = models.SlugField(max_length=220, unique=True)
    other_names = models.CharField(
        max_length=300, blank=True, help_text="Other names or spellings, comma-separated"
    )
    region = models.ForeignKey(
        Region, null=True, blank=True, on_delete=models.SET_NULL, related_name="communities"
    )
    description = models.TextField(blank=True)
    is_sample = models.BooleanField(
        default=False, help_text="Fictional sample record used for demos and tests"
    )
    stewards = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="stewarded_communities",
        help_text="Users with the steward role who review this community's records",
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Set when a contributor typed a new community under 'Other'",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "communities"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("communities:detail", kwargs={"slug": self.slug})
