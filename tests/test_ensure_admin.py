import pytest
from django.core.management import call_command
from django.test import Client

from accounts.models import User

PASSWORD = "Long-Password-2026"


def _login(email, password=PASSWORD):
    return Client().post("/admin/login/?next=/admin/", {"username": email, "password": password})


@pytest.mark.django_db
def test_creates_admin_who_can_log_in_with_any_capitals(monkeypatch, capsys):
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "Ege.Asan@Example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", PASSWORD)
    call_command("ensure_admin")
    assert "created" in capsys.readouterr().out
    user = User.objects.get()
    assert user.email == "ege.asan@example.com"
    assert user.role == "admin" and user.is_superuser and user.is_staff
    for typed in ["ege.asan@example.com", "Ege.Asan@Example.com", "EGE.ASAN@EXAMPLE.COM"]:
        assert _login(typed).status_code == 302


@pytest.mark.django_db
def test_repairs_an_existing_account(monkeypatch):
    User.objects.create_user("Ege@Example.com", "old-password-123", is_active=False)
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "ege@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", PASSWORD)
    call_command("ensure_admin")
    call_command("ensure_admin")  # runs on every start-up
    user = User.objects.get()
    assert user.is_active and user.role == "admin" and user.check_password(PASSWORD)
    assert _login("ege@example.com").status_code == 302


@pytest.mark.django_db
def test_does_nothing_without_variables(monkeypatch, capsys):
    monkeypatch.delenv("DJANGO_SUPERUSER_EMAIL", raising=False)
    monkeypatch.delenv("DJANGO_SUPERUSER_PASSWORD", raising=False)
    call_command("ensure_admin")
    assert "not both set" in capsys.readouterr().out
    assert not User.objects.exists()


@pytest.mark.django_db
def test_site_login_ignores_capitals():
    User.objects.create_user("Maker@Example.com", PASSWORD)
    r = Client().post("/accounts/login/", {"login": "MAKER@example.com", "password": PASSWORD})
    assert r.status_code == 302
