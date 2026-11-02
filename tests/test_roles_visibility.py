"""US-05 roles and permissions, US-22 visibility levels, US-27 managing users."""

import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from accounts.models import AccountChange, User
from crafts.models import Craft, Media

from .factories import CommunityFactory, CraftFactory, UserFactory

pytestmark = pytest.mark.django_db
V = Craft.Visibility


@pytest.fixture
def world():
    """Two communities, a craft at each visibility level in community A, and one user per role."""
    a, b = CommunityFactory(name="Community A"), CommunityFactory(name="Community B")
    author = UserFactory(role=User.Role.MAKER)
    crafts = {
        level: CraftFactory(
            title=f"{level} craft", community=a, visibility=level, created_by=author
        )
        for level in V.values
    }
    crafts["draft"] = CraftFactory(
        title="draft craft", community=a, status=Craft.Status.DRAFT, created_by=author
    )
    steward_a = UserFactory(role=User.Role.STEWARD)
    a.stewards.add(steward_a)
    steward_b = UserFactory(role=User.Role.STEWARD)
    b.stewards.add(steward_b)
    users = {
        "visitor": None,
        "member": UserFactory(role=User.Role.MEMBER),
        "member of A": UserFactory(role=User.Role.MEMBER, community=a),
        "member of B": UserFactory(role=User.Role.MEMBER, community=b),
        "steward of A": steward_a,
        "steward of B": steward_b,
        "admin": UserFactory(role=User.Role.ADMIN),
        "author": author,
    }
    return {"a": a, "b": b, "crafts": crafts, "users": users}


EVERYTHING = {"public", "members", "community", "restricted", "draft"}
EXPECTED = {
    "visitor": {"public"},
    "member": {"public", "members"},
    "member of A": {"public", "members", "community"},
    "member of B": {"public", "members"},
    "steward of A": EVERYTHING - {"draft"},  # not other people's unsubmitted drafts
    "steward of B": {"public", "members"},
    "admin": EVERYTHING,
    "author": EVERYTHING,  # authors always see their own records
}


@pytest.mark.parametrize("who", EXPECTED)
def test_visibility_matrix(world, who, client):
    user = world["users"][who]
    seen = {
        key
        for key, craft in world["crafts"].items()
        if Craft.objects.visible_to(user).filter(pk=craft.pk).exists()
    }
    assert seen == EXPECTED[who]
    # Pages agree with the queryset: hidden records are 404, never "forbidden".
    if user:
        client.force_login(user)
    for key, craft in world["crafts"].items():
        status = client.get(craft.get_absolute_url()).status_code
        assert status == (200 if key in EXPECTED[who] else 404), (who, key)


def test_catalogue_never_lists_restricted_records(world, client):
    client.force_login(world["users"]["member of A"])
    html = client.get(reverse("crafts:list")).content.decode()
    assert "community craft" in html and "restricted craft" not in html


class TestRoles:
    def test_members_cannot_add_crafts(self, client):
        client.force_login(UserFactory(role=User.Role.MEMBER))
        assert client.get(reverse("crafts:create")).status_code == 403
        assert client.post(reverse("crafts:create"), {"title": "x"}).status_code == 403
        assert "Add a craft" not in client.get(reverse("crafts:list")).content.decode()

    def test_makers_can_add_crafts(self, client):
        client.force_login(UserFactory(role=User.Role.MAKER))
        assert client.get(reverse("crafts:create")).status_code == 200

    def test_new_sign_ups_are_makers(self, client):
        client.post(
            reverse("account_signup"),
            {
                "email": "new@example.com",
                "password1": "Woven-Basket-2026",
                "password2": "Woven-Basket-2026",
            },
        )
        assert User.objects.get(email="new@example.com").role == User.Role.MAKER

    def test_who_can_edit(self, world, client):
        craft = world["crafts"]["public"]
        url = reverse("crafts:edit", args=[craft.slug])
        allowed = {"author", "steward of A", "admin"}
        for who, user in world["users"].items():
            client.logout()
            if user:
                client.force_login(user)
            status = client.get(url).status_code
            if who == "visitor":
                assert status == 302  # to the login page
            else:
                assert (status == 200) == (who in allowed), who

    def test_member_author_loses_edit_rights(self, world, client):
        author = world["users"]["author"]
        author.role = User.Role.MEMBER
        author.save()
        client.force_login(author)
        craft = world["crafts"]["public"]
        assert client.get(reverse("crafts:edit", args=[craft.slug])).status_code == 404

    def test_admin_role_gets_admin_site(self):
        user = UserFactory(role=User.Role.ADMIN)
        assert user.is_staff
        user.role = User.Role.MAKER
        user.save()
        assert not user.is_staff


class TestManageUsers:
    def test_suspended_users_cannot_log_in(self, client, password):
        user = UserFactory()
        user.is_active = False
        user.save()
        assert not client.login(email=user.email, password=password)
        response = client.post(
            reverse("account_login"), {"login": user.email, "password": password}
        )
        assert "_auth_user_id" not in client.session
        assert response.status_code in (200, 302)

    def test_role_changes_and_suspensions_are_logged(self):
        admin, user = UserFactory(role=User.Role.ADMIN), UserFactory()
        user.role = User.Role.STEWARD
        user.changed_by = admin
        user.save()
        user.is_active = False
        user.save()
        changes = list(AccountChange.objects.filter(user=user).order_by("changed_at"))
        assert [(c.field, c.old_value, c.new_value) for c in changes] == [
            ("role", "maker", "steward"),
            ("is_active", "True", "False"),
        ]
        assert changes[0].changed_by == admin

    def test_admin_actions_suspend_and_log(self, client):
        admin = User.objects.create_superuser("root@example.com", "Correct-Horse-42")
        target = UserFactory()
        client.force_login(admin)
        client.post(
            reverse("admin:accounts_user_changelist"),
            {"action": "suspend", "_selected_action": [target.pk, admin.pk]},
        )
        target.refresh_from_db()
        admin.refresh_from_db()
        assert not target.is_active and admin.is_active  # never suspends yourself
        assert AccountChange.objects.get(user=target).changed_by == admin

    def test_admin_can_search_and_change_role(self, client):
        admin = User.objects.create_superuser("root@example.com", "Correct-Horse-42")
        target = UserFactory(email="weaver@example.com")
        client.force_login(admin)
        html = client.get(reverse("admin:accounts_user_changelist"), {"q": "weaver"}).content
        assert b"weaver@example.com" in html
        page = client.get(reverse("admin:accounts_user_change", args=[target.pk]))
        assert page.status_code == 200 and b'name="role"' in page.content


def test_uploaded_photos_follow_craft_visibility(world, client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10)).save(buffer, "JPEG")
    media = Media(craft=world["crafts"]["restricted"], alt_text="A photo")
    media.image.save("secret.jpg", SimpleUploadedFile("secret.jpg", buffer.getvalue()), save=True)
    url = "/media/" + media.image.name
    assert client.get(url).status_code == 404
    client.force_login(world["users"]["member of A"])
    assert client.get(url).status_code == 404
    client.force_login(world["users"]["steward of A"])
    response = client.get(url)
    assert response.status_code == 200 and response["Cache-Control"].startswith("private")
    assert client.get("/media/crafts/not-a-photo.jpg").status_code == 404


@pytest.mark.django_db
def test_createsuperuser_gets_admin_role():
    from django.contrib.auth import get_user_model

    admin = get_user_model().objects.create_superuser("root@example.com", "Long-Password-2026")
    assert admin.role == "admin"
    assert admin.is_staff and admin.is_superuser
