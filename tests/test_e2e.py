"""End-to-end demo flow in a real browser (Playwright). Run with: pytest -m e2e"""

import os

import pytest
from django.core.management import call_command

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def seeded(transactional_db):
    call_command("seed_sample_data")


def test_demo_flow(live_server, page, seeded):
    page.goto(live_server.url)
    assert "credited to the people who make them" in page.content()

    page.get_by_role("link", name="Browse crafts").first.click()
    anonymous_count = page.locator(".grid .card").count()
    assert anonymous_count >= 8

    page.locator(".card").first.click()
    assert page.get_by_text("Made by").is_visible()
    assert page.get_by_text("Sample data").first.is_visible()

    page.goto(f"{live_server.url}/accounts/signup/")
    page.fill("input[name=email]", "e2e@example.com")
    page.fill("input[name=password1]", "Woven-Basket-2026")
    page.fill("input[name=password2]", "Woven-Basket-2026")
    page.locator("button[type=submit]").click()
    assert page.locator(".nav-user").inner_text().startswith("Signed in as")

    page.goto(f"{live_server.url}/crafts/")
    assert page.locator(".grid .card").count() > anonymous_count  # members-only records

    page.get_by_role("button", name="Log out").click()
    assert page.get_by_role("link", name="Log in").is_visible()


def test_no_horizontal_scroll_on_phone(live_server, browser, seeded):
    context = browser.new_context(viewport={"width": 360, "height": 780})
    phone = context.new_page()
    for path in ["/", "/crafts/", "/crafts/sample-coiled-sedge-basket/", "/accounts/login/"]:
        phone.goto(live_server.url + path)
        assert not phone.evaluate("document.documentElement.scrollWidth > innerWidth"), path
    context.close()


def test_add_craft_in_browser(live_server, page, seeded):
    """US-08/US-11 + feedback: type-specific fields appear, rows can be added, page shows Made."""
    page.goto(f"{live_server.url}/accounts/signup/")
    page.fill("input[name=email]", "maker@example.com")
    page.fill("input[name=password1]", "Woven-Basket-2026")
    page.fill("input[name=password2]", "Woven-Basket-2026")
    page.locator("button[type=submit]").click()

    page.get_by_role("link", name="Add a craft").click()
    page.wait_for_selector("form[data-ready=true]", state="attached")
    page.fill("#id_title", "Twined bag")
    page.select_option("#id_craft_type", label="Basketry")
    page.wait_for_selector("#id_attr-weave")  # fields for the chosen type load
    page.select_option("#id_attr-weave", "Twined")
    page.select_option("#id_community", index=1)
    page.fill("#id_maker_credit", "E2E Maker")
    page.fill("#id_year_made", "2001")
    page.fill("#id_mat-0-name", "Spruce root")
    page.fill("#id_mat-0-origin", "Forest floor")
    page.get_by_role("button", name="+ Add material").click()
    page.fill("#id_mat-1-name", "Bark")
    page.fill("#id_height", "30")
    page.select_option("#id_size_unit", "cm")
    page.locator("button[value=publish]").click()

    facts = page.locator(".facts").inner_text()
    assert "E2E Maker" in facts
    assert "Spruce root, Bark" in facts
    assert "2001" in facts
    assert "30 cm" in facts and "11.8 in" in facts
    assert page.get_by_text("Forest floor").is_visible()
    assert page.get_by_role("link", name="Edit").is_visible()
