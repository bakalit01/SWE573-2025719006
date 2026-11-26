"""US-18: members favourite crafts and group them into named collections."""

import pytest
from django.urls import reverse

from accounts.models import User
from crafts.models import Collection, Craft, Favourite

from .factories import CraftFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def member(client):
    user = UserFactory(role=User.Role.MEMBER)
    client.force_login(user)
    return user


@pytest.fixture
def craft():
    return CraftFactory(title="Coiled basket")


def test_favourite_and_unfavourite(client, member, craft):
    url = reverse("crafts:favourite", args=[craft.slug])
    client.post(url)
    assert Favourite.objects.filter(user=member, craft=craft).exists()
    page = client.get(craft.get_absolute_url()).content.decode()
    assert 'aria-pressed="true"' in page and "In your favourites" in page
    saved = client.get(reverse("collections:saved"))
    assert list(saved.context["favourites"]) == [craft]
    client.post(url)
    assert not Favourite.objects.filter(user=member).exists()


def test_visitors_see_no_save_card_and_cannot_save(client, craft):
    assert "Add to favourites" not in client.get(craft.get_absolute_url()).content.decode()
    response = client.post(reverse("crafts:favourite", args=[craft.slug]))
    assert "/accounts/login/" in response.url
    assert not Favourite.objects.exists()


def test_add_to_a_new_and_an_existing_collection(client, member, craft):
    url = reverse("crafts:collections", args=[craft.slug])
    client.post(url, {"new_collection": "  Natural   dyes "})
    dyes = Collection.objects.get(owner=member)
    assert dyes.name == "Natural dyes" and not dyes.is_public  # private by default
    assert list(dyes.crafts.all()) == [craft]
    other = Collection.objects.create(owner=member, name="Gifts")
    client.post(url, {"collection": [str(other.pk)]})  # unticking "Natural dyes"
    assert list(other.crafts.all()) == [craft] and not dyes.crafts.exists()


def test_collection_names_are_unique_per_member(client, member, craft):
    Collection.objects.create(owner=member, name="Gifts")
    response = client.post(reverse("collections:create"), {"name": "gifts"})
    assert response.status_code == 400
    assert "You already have a collection called “gifts”." in response.content.decode()
    other = UserFactory()
    Collection.objects.create(owner=other, name="Gifts")  # someone else may use the name
    assert Collection.objects.filter(name__iexact="gifts").count() == 2


def test_private_collection_is_hidden_from_others(client, member, craft):
    collection = Collection.objects.create(owner=member, name="Mine")
    collection.crafts.add(craft)
    assert client.get(collection.get_absolute_url()).status_code == 200
    client.force_login(UserFactory())
    assert client.get(collection.get_absolute_url()).status_code == 404
    client.logout()
    assert client.get(collection.get_absolute_url()).status_code == 404
    assert "Mine" not in client.get(member.get_absolute_url()).content.decode()


def test_public_collection_is_shown_on_the_profile(client, member, craft):
    collection = Collection.objects.create(owner=member, name="Baskets", is_public=True)
    collection.crafts.add(craft)
    client.logout()
    profile = client.get(member.get_absolute_url()).content.decode()
    assert "Baskets" in profile and "1 craft" in profile
    page = client.get(collection.get_absolute_url())
    assert list(page.context["crafts"]) == [craft] and page.context["form"] is None


def test_losing_access_hides_the_craft_from_collections_and_favourites(client, member, craft):
    collection = Collection.objects.create(owner=member, name="Mine")
    collection.crafts.add(craft)
    Favourite.objects.create(user=member, craft=craft)
    craft.status = Craft.Status.UNPUBLISHED
    craft.save()
    assert list(client.get(collection.get_absolute_url()).context["crafts"]) == []
    saved = client.get(reverse("collections:saved"))
    assert list(saved.context["favourites"]) == []
    assert saved.context["collections"][0].n_visible == 0
    assert collection.crafts.filter(pk=craft.pk).exists()  # kept, in case access returns
    craft.status = Craft.Status.PUBLISHED
    craft.save()
    assert list(client.get(collection.get_absolute_url()).context["crafts"]) == [craft]


def test_members_only_craft_is_hidden_from_visitors_in_a_public_collection(client, member):
    members_only = CraftFactory(visibility=Craft.Visibility.MEMBERS)
    collection = Collection.objects.create(owner=member, name="Shared", is_public=True)
    collection.crafts.add(members_only)
    client.logout()
    assert list(client.get(collection.get_absolute_url()).context["crafts"]) == []


def test_cannot_save_a_craft_you_cannot_see(client, member):
    draft = CraftFactory(status=Craft.Status.DRAFT)
    assert client.post(reverse("crafts:favourite", args=[draft.slug])).status_code == 404
    url = reverse("crafts:collections", args=[draft.slug])
    assert client.post(url, {"new_collection": "Sneaky"}).status_code == 404
    assert not Collection.objects.exists()


def test_owner_edits_removes_and_deletes(client, member, craft):
    collection = Collection.objects.create(owner=member, name="Old")
    collection.crafts.add(craft)
    edit = reverse("collections:edit", args=[collection.pk])
    client.post(edit, {"name": "New", "description": "Mine", "is_public": "on"})
    collection.refresh_from_db()
    assert (collection.name, collection.is_public) == ("New", True)
    client.post(reverse("collections:remove", args=[collection.pk, craft.slug]))
    assert not collection.crafts.exists()
    client.post(reverse("collections:delete", args=[collection.pk]))
    assert not Collection.objects.exists() and Craft.objects.filter(pk=craft.pk).exists()


def test_others_cannot_change_a_collection(client, member, craft):
    collection = Collection.objects.create(owner=member, name="Mine", is_public=True)
    collection.crafts.add(craft)
    client.force_login(UserFactory())
    for url in (
        reverse("collections:edit", args=[collection.pk]),
        reverse("collections:delete", args=[collection.pk]),
        reverse("collections:remove", args=[collection.pk, craft.slug]),
    ):
        assert client.post(url, {"name": "Taken"}).status_code == 404
    collection.refresh_from_db()
    assert collection.name == "Mine" and collection.crafts.exists()


def test_back_link_only_to_this_site(client, member, craft):
    url = reverse("crafts:favourite", args=[craft.slug])
    assert client.post(url, {"next": "https://evil.example/"}).url == craft.get_absolute_url()
    assert client.post(url, {"next": "/saved/"}).url == "/saved/"
