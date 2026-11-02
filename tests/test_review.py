"""US-23 consent, US-24 steward review, US-25 reports."""

import pytest
from django.core import mail
from django.urls import reverse

from accounts.models import User
from crafts.models import Consent, Craft, Report, ReviewDecision

from .factories import CommunityFactory, CraftFactory, UserFactory
from .test_contribute import payload

pytestmark = pytest.mark.django_db


@pytest.fixture
def people(setup):
    """A maker, a steward of the craft's community, a steward of another community, an admin."""
    community = setup["community"]
    steward = UserFactory(role=User.Role.STEWARD, email="steward@example.com")
    community.stewards.add(steward)
    other = UserFactory(role=User.Role.STEWARD)
    CommunityFactory().stewards.add(other)
    return {
        "maker": UserFactory(role=User.Role.MAKER, email="maker@example.com"),
        "steward": steward,
        "other steward": other,
        "admin": UserFactory(role=User.Role.ADMIN),
    }


def as_user(client, user):
    client.logout()
    if user:
        client.force_login(user)
    return client


def submit(client, setup, **overrides):
    return client.post(reverse("crafts:create"), payload(setup, **overrides))


class TestConsent:
    def test_needed_to_submit(self, client, setup, people):
        as_user(client, people["maker"])
        response = submit(client, setup, **{"consent-granted_by": "", "consent-date": ""})
        assert response.status_code == 200
        assert "Needed before the craft can be submitted or published." in response.content.decode()
        assert not Craft.objects.exists()

    def test_optional_for_drafts(self, client, setup, people):
        as_user(client, people["maker"])
        submit(
            client,
            setup,
            action="draft",
            **{
                "consent-granted_by": "",
                "consent-granted_by_role": "",
                "consent-date": "",
                "consent-scope": "",
            },
        )
        craft = Craft.objects.get()
        assert craft.status == Craft.Status.DRAFT and not Consent.objects.exists()

    def test_partial_consent_on_a_draft_is_checked(self, client, setup, people):
        as_user(client, people["maker"])
        response = submit(client, setup, action="draft", **{"consent-date": ""})
        assert response.status_code == 200 and not Craft.objects.exists()

    def test_visible_to_stewards_and_admins_only(self, client, setup, people):
        as_user(client, people["maker"])
        submit(client, setup)
        craft = Craft.objects.get()
        assert craft.consent.granted_by == "The carving family"
        assert craft.consent.recorded_by == people["maker"]
        url = craft.get_absolute_url()
        assert (
            "The carving family" not in as_user(client, people["maker"]).get(url).content.decode()
        )
        for who in ("steward", "admin"):
            assert "The carving family" in as_user(client, people[who]).get(url).content.decode()
        craft.status = Craft.Status.PUBLISHED
        craft.save()
        for who in (None, people["other steward"]):
            assert "The carving family" not in as_user(client, who).get(url).content.decode()


class TestReview:
    def test_maker_submission_waits_for_review(self, client, setup, people):
        as_user(client, people["maker"])
        response = submit(client, setup)
        craft = Craft.objects.get()
        assert craft.status == Craft.Status.PENDING
        assert response.url == craft.get_absolute_url()
        assert mail.outbox and "steward@example.com" in mail.outbox[0].to
        assert as_user(client, None).get(craft.get_absolute_url()).status_code == 404
        assert as_user(client, people["maker"]).get(craft.get_absolute_url()).status_code == 200

    def test_queue_lists_only_my_communities(self, client, setup, people):
        as_user(client, people["maker"])
        submit(client, setup)
        queue = reverse("crafts:review_queue")
        assert "Carved pipe" in as_user(client, people["steward"]).get(queue).content.decode()
        assert "Carved pipe" in as_user(client, people["admin"]).get(queue).content.decode()
        assert (
            "Carved pipe"
            not in as_user(client, people["other steward"]).get(queue).content.decode()
        )
        assert as_user(client, people["maker"]).get(queue).status_code == 403
        nav = as_user(client, people["steward"]).get(reverse("crafts:list")).content.decode()
        assert 'aria-label="1 waiting"' in nav

    @pytest.mark.parametrize(
        "decision, comment, status",
        [
            ("approved", "", Craft.Status.PUBLISHED),
            ("changes", "Please add the dye source.", Craft.Status.DRAFT),
            ("rejected", "This is a sacred object.", Craft.Status.UNPUBLISHED),
        ],
    )
    def test_decisions(self, client, setup, people, decision, comment, status):
        as_user(client, people["maker"])
        submit(client, setup)
        craft = Craft.objects.get()
        mail.outbox.clear()
        as_user(client, people["steward"]).post(
            reverse("crafts:review", args=[craft.slug]), {"decision": decision, "comment": comment}
        )
        craft.refresh_from_db()
        assert craft.status == status
        assert ReviewDecision.objects.get(craft=craft).reviewer == people["steward"]
        assert mail.outbox[0].to == ["maker@example.com"]
        if comment:
            assert comment in mail.outbox[0].body
            page = as_user(client, people["maker"]).get(craft.get_absolute_url()).content.decode()
            assert comment in page
            mine = client.get(reverse("crafts:mine")).content.decode()
            assert comment in mine

    def test_changes_and_rejection_need_a_comment(self, client, setup, people):
        as_user(client, people["maker"])
        submit(client, setup)
        craft = Craft.objects.get()
        as_user(client, people["steward"]).post(
            reverse("crafts:review", args=[craft.slug]), {"decision": "rejected", "comment": " "}
        )
        craft.refresh_from_db()
        assert craft.status == Craft.Status.PENDING and not ReviewDecision.objects.exists()

    def test_only_this_communitys_reviewers_decide(self, client, setup, people):
        as_user(client, people["maker"])
        submit(client, setup)
        craft = Craft.objects.get()
        url = reverse("crafts:review", args=[craft.slug])
        for who in ("maker", "other steward"):
            assert (
                as_user(client, people[who]).post(url, {"decision": "approved"}).status_code == 404
            )
        craft.refresh_from_db()
        assert craft.status == Craft.Status.PENDING

    def test_maker_edits_go_back_to_review(self, client, setup, people):
        craft = CraftFactory(created_by=people["maker"], community=setup["community"])
        as_user(client, people["maker"])
        client.post(reverse("crafts:edit", args=[craft.slug]), payload(setup, title="Changed"))
        craft.refresh_from_db()
        assert craft.title == "Changed" and craft.status == Craft.Status.PENDING

    def test_stewards_publish_directly(self, client, setup, people):
        as_user(client, people["steward"])
        submit(client, setup)
        assert Craft.objects.get().status == Craft.Status.PUBLISHED

    def test_form_button_matches_role(self, client, setup, people):
        page = as_user(client, people["maker"]).get(reverse("crafts:create")).content.decode()
        assert "Submit for review" in page
        page = as_user(client, people["steward"]).get(reverse("crafts:create")).content.decode()
        assert "Submit for review" not in page and ">Publish<" in page


class TestReports:
    def test_anyone_can_report_without_logging_in(self, client, setup, people):
        craft = CraftFactory(community=setup["community"])
        url = reverse("crafts:report", args=[craft.slug])
        assert url in client.get(craft.get_absolute_url()).content.decode()
        assert client.get(url).status_code == 200
        response = client.post(
            url, {"reason": "permission", "details": "This is my grandmother's work."}
        )
        assert response.url == craft.get_absolute_url()
        report = Report.objects.get()
        assert report.status == Report.Status.OPEN and report.reporter is None
        assert "steward@example.com" in mail.outbox[0].to

    def test_spam_trap(self, client, setup):
        craft = CraftFactory(community=setup["community"])
        client.post(
            reverse("crafts:report", args=[craft.slug]),
            {"reason": "other", "details": "buy now", "website": "http://spam"},
        )
        assert not Report.objects.exists()

    def test_cannot_report_what_you_cannot_see(self, client, setup):
        craft = CraftFactory(community=setup["community"], visibility=Craft.Visibility.RESTRICTED)
        assert client.get(reverse("crafts:report", args=[craft.slug])).status_code == 404

    def test_reports_in_queue_and_unpublish_now(self, client, setup, people):
        craft = CraftFactory(community=setup["community"], created_by=people["maker"])
        report = Report.objects.create(craft=craft, reason="sensitive", details="Sacred design.")
        queue = reverse("crafts:review_queue")
        assert "Sacred design." in as_user(client, people["steward"]).get(queue).content.decode()
        assert (
            "Sacred design."
            not in as_user(client, people["other steward"]).get(queue).content.decode()
        )
        handle = reverse("crafts:handle_report", args=[report.pk])
        assert (
            as_user(client, people["other steward"])
            .post(handle, {"action": "unpublish"})
            .status_code
            == 404
        )
        as_user(client, people["steward"]).post(
            handle, {"action": "unpublish", "note": "Taken down."}
        )
        craft.refresh_from_db()
        report.refresh_from_db()
        assert craft.status == Craft.Status.UNPUBLISHED
        assert report.status == Report.Status.RESOLVED and report.resolved_by == people["steward"]
        assert ReviewDecision.objects.get(craft=craft).decision == "unpublished"
        assert as_user(client, None).get(craft.get_absolute_url()).status_code == 404

    def test_mark_resolved_keeps_the_record(self, client, setup, people):
        craft = CraftFactory(community=setup["community"])
        report = Report.objects.create(craft=craft, reason="inaccurate", details="Wrong year.")
        as_user(client, people["admin"]).post(
            reverse("crafts:handle_report", args=[report.pk]),
            {"action": "resolve", "note": "Fixed"},
        )
        report.refresh_from_db()
        craft.refresh_from_db()
        assert report.status == Report.Status.RESOLVED and report.resolution_note == "Fixed"
        assert craft.status == Craft.Status.PUBLISHED
