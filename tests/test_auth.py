"""US-01 Register an account · US-02 Log in and log out."""

import pytest
from django.urls import reverse

from accounts.models import User

pytestmark = pytest.mark.django_db

GOOD_PASSWORD = "Woven-Basket-2026"


def signup(client, email="new@example.com", password=GOOD_PASSWORD, password2=None):
    return client.post(
        reverse("account_signup"),
        {"email": email, "password1": password, "password2": password2 or password},
    )


class TestRegister:
    def test_signup_creates_user_signs_in_and_redirects_home(self, client):
        response = signup(client)
        assert response.status_code == 302
        assert response.url == reverse("home")
        user = User.objects.get(email="new@example.com")
        assert user.password != GOOD_PASSWORD  # stored hashed
        assert user.check_password(GOOD_PASSWORD)
        assert "Signed in as" in client.get(reverse("home")).content.decode()

    def test_password_shorter_than_10_is_rejected(self, client):
        response = signup(client, password="Short-1")
        assert response.status_code == 200
        assert "at least 10 characters" in response.content.decode()
        assert not User.objects.exists()

    def test_invalid_email_is_rejected(self, client):
        signup(client, email="not-an-email")
        assert not User.objects.exists()

    def test_duplicate_email_shows_clear_error(self, client, user):
        response = signup(client, email=user.email)
        assert response.status_code == 200
        assert "already registered" in response.content.decode()
        assert User.objects.count() == 1


class TestLogin:
    def test_login_shows_name_in_header(self, client, user, password):
        response = client.post(
            reverse("account_login"), {"login": user.email, "password": password}, follow=True
        )
        html = response.content.decode()
        assert "Signed in as" in html
        assert user.public_name in html
        assert "Log out" in html

    @pytest.mark.parametrize("which", ["email", "password"])
    def test_wrong_credentials_give_the_same_generic_error(self, client, user, password, which):
        data = {"login": user.email, "password": password}
        data["login" if which == "email" else "password"] = (
            "nobody@example.com" if which == "email" else "Wrong-Password-1"
        )
        html = client.post(reverse("account_login"), data).content.decode()
        assert "The email address and/or password you specified are not correct." in html

    def test_logout_requires_post_and_ends_session(self, member_client):
        member_client.get(reverse("account_logout"))  # GET only shows a confirmation page
        assert "_auth_user_id" in member_client.session
        member_client.post(reverse("account_logout"))
        assert "_auth_user_id" not in member_client.session
