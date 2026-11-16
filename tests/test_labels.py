"""US-26: community stewards attach Traditional Knowledge / Biocultural labels to crafts."""

import pytest
from django.urls import reverse

from accounts.models import User
from crafts.models import Craft, TKLabel
from crafts.seeding import ensure_tk_labels

from .factories import CommunityFactory, CraftFactory, UserFactory
from .test_contribute import payload

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def labels(db):
    """The list comes from a data migration; browser tests empty the database, so reload it."""
    ensure_tk_labels()


@pytest.fixture
def world(setup):
    community = setup["community"]
    steward = UserFactory(role=User.Role.STEWARD)
    community.stewards.add(steward)
    other_steward = UserFactory(role=User.Role.STEWARD)
    CommunityFactory().stewards.add(other_steward)
    maker = UserFactory(role=User.Role.MAKER)
    craft = CraftFactory(community=community, craft_type=setup["type"], created_by=maker)
    return {
        "craft": craft,
        "steward": steward,
        "other steward": other_steward,
        "maker": maker,
        "admin": UserFactory(role=User.Role.ADMIN),
        "attribution": TKLabel.objects.get(code="TK A"),
        "seasonal": TKLabel.objects.get(code="TK S"),
    }


def label_ids(*labels):
    return [str(label.pk) for label in labels]


def test_managed_list_has_the_local_contexts_labels():
    tk = TKLabel.objects.filter(kind=TKLabel.Kind.TK)
    bc = TKLabel.objects.filter(kind=TKLabel.Kind.BC)
    assert tk.count() == 20 and bc.count() == 10
    assert {"TK Attribution", "TK Secret / Sacred", "TK Outreach"} <= set(
        tk.values_list("name", flat=True)
    )
    assert all(label.description and label.url.startswith("https://") for label in tk)
    assert set(TKLabel.objects.values_list("category", flat=True)) == {
        "provenance",
        "protocol",
        "permission",
    }


class TestSteward:
    def test_sets_labels_from_the_craft_page(self, client, world):
        client.force_login(world["steward"])
        url = reverse("crafts:labels", args=[world["craft"].slug])
        response = client.post(url, {"tk_labels": label_ids(world["attribution"])})
        assert response.status_code == 302
        assert list(world["craft"].tk_labels.all()) == [world["attribution"]]
        client.logout()  # anyone who can see the craft sees its labels
        html = client.get(world["craft"].get_absolute_url()).content.decode()
        assert "Traditional Knowledge labels" in html
        assert '<span class="tk-icon tk-icon-tk" aria-hidden="true">TK A</span>' in html
        assert "TK Attribution" in html and world["attribution"].description in html
        assert "About TK Attribution (Local Contexts)" in html
        assert "Save labels" not in html  # visitors can't change them

    def test_removes_all_labels(self, client, world):
        world["craft"].tk_labels.set([world["attribution"], world["seasonal"]])
        client.force_login(world["steward"])
        client.post(reverse("crafts:labels", args=[world["craft"].slug]), {})
        assert not world["craft"].tk_labels.exists()

    def test_sees_the_labels_form_with_current_labels_ticked(self, client, world):
        world["craft"].tk_labels.set([world["seasonal"]])
        client.force_login(world["steward"])
        response = client.get(world["craft"].get_absolute_url())
        form = response.context["labels_form"]
        assert list(form.initial["tk_labels"]) == [world["seasonal"]]
        assert "Change labels" in response.content.decode()

    def test_sets_labels_in_the_craft_form(self, member_client, setup, world):
        # The `setup` user stewards the community, so they publish directly with labels.
        data = payload(setup, tk_labels=label_ids(world["attribution"], world["seasonal"]))
        member_client.post(reverse("crafts:create"), data)
        craft = Craft.objects.get(title="Carved pipe")
        assert set(craft.tk_labels.all()) == {world["attribution"], world["seasonal"]}


@pytest.mark.parametrize("who", ["maker", "other steward", None])
def test_others_cannot_set_labels(client, world, who):
    if who:
        client.force_login(world[who])
    url = reverse("crafts:labels", args=[world["craft"].slug])
    response = client.post(url, {"tk_labels": label_ids(world["attribution"])})
    assert response.status_code in (302, 404)
    if who:
        assert response.status_code == 404
    else:
        assert "/accounts/login/" in response.url
    assert not world["craft"].tk_labels.exists()
    if who:
        page = client.get(world["craft"].get_absolute_url())
        assert page.context["labels_form"] is None


def test_admin_can_set_labels(client, world):
    client.force_login(world["admin"])
    client.post(
        reverse("crafts:labels", args=[world["craft"].slug]),
        {"tk_labels": label_ids(world["seasonal"])},
    )
    assert list(world["craft"].tk_labels.all()) == [world["seasonal"]]


def test_maker_form_has_no_labels_field(client, world):
    client.force_login(world["maker"])
    response = client.get(reverse("crafts:create"))
    assert "tk_labels" not in response.context["form"].fields


def test_labels_for_another_community_are_not_applied(client, setup, world):
    """A steward of community B adds a craft to community A: labels are A's call."""
    client.force_login(world["other steward"])
    data = payload(setup, tk_labels=label_ids(world["attribution"]))
    response = client.post(reverse("crafts:create"), data, follow=True)
    craft = Craft.objects.get(title="Carved pipe")
    assert not craft.tk_labels.exists()
    assert "The TK / BC labels were not changed" in response.content.decode()


def test_retired_label_is_not_offered_but_kept_where_used(client, world):
    world["craft"].tk_labels.set([world["seasonal"]])
    world["seasonal"].is_active = False
    world["seasonal"].save()
    client.force_login(world["steward"])
    new_form = client.get(reverse("crafts:create")).context["form"]
    assert world["seasonal"] not in new_form.fields["tk_labels"].queryset
    page = client.get(world["craft"].get_absolute_url())
    assert world["seasonal"] in page.context["labels_form"].fields["tk_labels"].queryset
    assert "TK Seasonal" in page.content.decode()
