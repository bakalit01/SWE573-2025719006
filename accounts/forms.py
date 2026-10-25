from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import filter_users_by_email
from django import forms

from .models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["display_name", "bio", "community", "location"]
        labels = {
            "display_name": "Display name",
            "bio": "About you",
            "community": "Community affiliation",
            "location": "Where you are based",
        }
        help_texts = {
            "display_name": "Shown on your profile and next to crafts you add.",
            "community": "Optional. If yours is missing, report it and an admin will add it.",
        }
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["community"].empty_label = "None"


class SameResponseResetPasswordForm(ResetPasswordForm):
    """US-03: the reset page responds the same whether or not the email has an account.

    (Sign-up still says when an email is already registered, as US-01 requires.)
    """

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True, prefer_verified=True)
        return self.cleaned_data["email"]
