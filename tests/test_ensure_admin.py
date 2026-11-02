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


@pytest.mark.django_db
def test_login_with_the_variables_creates_admin_even_if_start_step_never_ran(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "Ege@Example.com ")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", PASSWORD + "\n")  # pasted with a newline
    assert not User.objects.exists()
    r = _login("ege@example.com")
    assert r.status_code == 302
    assert Client().get("/admin/").status_code == 302  # fresh client is not logged in
    user = User.objects.get()
    assert user.role == "admin" and user.is_superuser and user.check_password(PASSWORD)


@pytest.mark.django_db
def test_wrong_password_does_not_create_or_change_the_admin(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "ege@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", PASSWORD)
    assert _login("ege@example.com", "wrong-password-1").status_code == 200
    assert _login("someone@example.com").status_code == 200
    assert not User.objects.exists()


@pytest.mark.django_db
def test_admin_login_from_variables_reaches_admin_index(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "ege@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", PASSWORD)
    c = Client()
    c.post("/admin/login/?next=/admin/", {"username": "Ege@example.com", "password": PASSWORD})
    assert c.get("/admin/").status_code == 200
