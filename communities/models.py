from django.conf import settings
from django.db import models
from django.urls import reverse


class Community(models.Model):
    """A community or nation. `name` is the community's own (self-designated) name."""

    name = models.CharField(max_length=200, unique=True, help_text="Self-designated name")
    slug = models.SlugField(max_length=220, unique=True)
    other_names = models.CharField(
        max_length=300, blank=True, help_text="Other names or spellings, comma-separated"
    )
    region = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_sample = models.BooleanField(
        default=False, help_text="Fictional sample record used for demos and tests"
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
        return reverse("crafts:list") + f"?community={self.slug}"
