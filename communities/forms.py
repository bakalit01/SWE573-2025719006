from django import forms

from .models import Community


class CommunityForm(forms.ModelForm):
    """What a community's stewards may edit about it (US-17)."""

    class Meta:
        model = Community
        fields = ["other_names", "region", "description"]
        labels = {
            "other_names": "Other names or spellings",
            "region": "Region",
            "description": "About the community",
        }
        help_texts = {
            "description": "In the community's own words: who you are, where, and what your "
            "crafts mean to you.",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 8})}
