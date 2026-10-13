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
