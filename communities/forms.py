from django import forms

from .models import Community, Region


class CommunityForm(forms.ModelForm):
    """What a community's stewards may edit about it (US-17)."""

    class Meta:
        model = Community
        fields = ["other_names", "description"]
        labels = {
            "other_names": "Other names or spellings",
            "description": "About the community",
        }
        help_texts = {
            "description": "In the community's own words: who you are, where, and what your "
            "crafts mean to you.",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 8})}

    field_order = ["other_names", "region", "description"]
    region = forms.CharField(
        label="Region",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"list": "region-options", "autocomplete": "off"}),
        help_text="Choose a region from the list, or type a new one.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.region_id:
            self.initial["region"] = self.instance.region.name
        self.region_options = Region.objects.values_list("name", flat=True)

    def save(self, commit=True):
        self.instance.region = Region.for_name(self.cleaned_data.get("region"))
        return super().save(commit)
