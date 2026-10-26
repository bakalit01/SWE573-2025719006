"""Take the UI design screenshots in docs/design/screenshots/.

Usage: python scripts/take_screenshots.py http://127.0.0.1:8000 docs/design/screenshots

Expects a fresh database with the real examples loaded (`seed_reference_crafts`).
Needs internet access for Wikimedia Commons photos and OpenStreetMap tiles, so it runs
in GitHub Actions (workflow "UI screenshots").
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeout

BASE = sys.argv[1].rstrip("/")
OUT = Path(sys.argv[2])
EXAMPLE = "/crafts/pomo-coiled-dowry-basket-jenny-hughes/"
PASSWORD = "Woven-Basket-2026"  # noqa: S105 (throwaway demo account in CI)
OFFLINE = bool(os.environ.get("SCREENSHOT_OFFLINE"))  # selector check without internet


def settle(page: Page, maps=False):
    """Wait until photos (and map tiles) have loaded, so screenshots aren't half-empty."""
    page.wait_for_load_state("domcontentloaded" if OFFLINE else "networkidle")
    page.evaluate(
        "document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')"
    )
    if not OFFLINE:
        try:
            page.wait_for_function(
                "Array.from(document.images).every(i => i.complete)", timeout=30_000
            )
            if maps:
                page.wait_for_selector(".leaflet-tile-loaded", timeout=30_000)
        except PlaywrightTimeout:
            print("  warning: some images or map tiles did not load in time")
    page.wait_for_timeout(1500)


def shot(page: Page, name, full=True, maps=False):
    settle(page, maps)
    page.screenshot(path=OUT / name, full_page=full)
    print("saved", name)


def sign_up(page: Page, email):
    page.goto(f"{BASE}/accounts/signup/")
    page.fill("input[name=email]", email)
    page.fill("input[name=password1]", PASSWORD)
    page.fill("input[name=password2]", PASSWORD)
    page.locator("button[type=submit]").click()
    page.wait_for_load_state()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE") or None
        )

        # ---- Visitor, desktop ----
        desk = browser.new_context(viewport={"width": 1280, "height": 800}, locale="en-GB")
        page = desk.new_page()
        page.goto(BASE + "/")
        shot(page, "01-home.png")
        page.goto(BASE + "/crafts/")
        shot(page, "02-catalogue.png")
        page.goto(BASE + EXAMPLE)
        shot(page, "03-craft-detail.png", maps=True)
        page.goto(BASE + "/crafts/?tag=painted")
        shot(page, "09-catalogue-tag-filter.png")

        page.goto(f"{BASE}/accounts/signup/")
        page.fill("input[name=email]", "someone@example.com")
        page.fill("input[name=password1]", "short")
        page.fill("input[name=password2]", "short")
        page.locator("button[type=submit]").click()
        shot(page, "04-signup-validation.png", full=False)

        page.goto(f"{BASE}/accounts/login/")
        page.fill("input[name=login]", "nobody@example.com")
        page.fill("input[name=password]", "wrong-password-123")
        page.locator("button[type=submit]").click()
        shot(page, "06-login-error.png", full=False)

        # ---- Signed-in maker ----
        sign_up(page, "demo.maker@example.com")
        page.goto(f"{BASE}/accounts/profile/edit/")
        page.fill("#id_display_name", "Demo maker")
        page.fill("#id_bio", "Documents felt and weaving traditions with the makers' permission.")
        page.fill("#id_location", "İstanbul, Türkiye")
        page.get_by_role("button", name="Save profile").click()
        page.goto(BASE + "/crafts/")
        shot(page, "05-signed-in-catalogue.png", full=False)

        # Add form: "Other" craft type, community and unit, tags, own details.
        page.goto(BASE + "/crafts/add/")
        page.wait_for_selector("form[data-ready=true]", state="attached")
        page.fill("#id_title", "Felt rug")
        page.select_option("#id_craft_type", "__other__")
        page.fill("#id_craft_type_other", "Felt making")
        page.select_option("#id_community", "__other__")
        page.fill("#id_community_other", "Yörük")
        page.fill("#id_summary", "A rug of pressed wool with a ram's-horn motif.")
        page.fill("#id_tags", "nomadic, wool, everyday use")
        page.fill("#id_maker_credit", "A Yörük family workshop")
        page.fill("#id_year_made", "1990")
        page.check("#id_year_is_approximate")
        if OFFLINE:
            page.fill("#id_place_name", "Konya")
            page.fill("#id_country", "Türkiye")
        else:
            page.fill("#place-search", "Konya, Türkiye")
            page.locator("[data-map-search-button]").click()
            page.wait_for_function(
                "document.querySelector('[data-map-status]').textContent.startsWith('Found')",
                timeout=20_000,
            )
        page.fill("#id_mat-0-name", "Wool")
        page.fill("#id_mat-0-origin", "The family's own sheep")
        page.fill("#id_mat-0-notes", "Washed, carded and dyed by hand")
        page.fill("#id_tec-0-name", "Wet felting")
        page.fill("#id_tec-0-notes", "Rolled in a reed mat with hot water")
        page.fill("#id_height", "180")
        page.fill("#id_width", "120")
        page.select_option("#id_size_unit", "cm")
        page.fill("#id_weight", "3")
        page.select_option("#id_weight_unit", "other")
        page.fill("#id_weight_unit_other", "okka")
        page.fill("#id_det-0-label", "Dye source")
        page.fill("#id_det-0-value", "Madder root")
        page.fill("#id_description", "Made for the family's winter tent.")
        page.check("input[name=visibility][value=public]")
        page.locator("#sec-basics").scroll_into_view_if_needed()
        settle(page)
        page.locator("#sec-basics").screenshot(path=OUT / "13-form-other-and-tags.png")
        print("saved 13-form-other-and-tags.png")
        shot(page, "10-add-craft-form.png", maps=True)
        page.locator("button[value=publish]").click()
        page.wait_for_load_state()
        shot(page, "14-craft-page-own-entries.png", maps=True)
        profile_url = page.locator(".craft-meta a").first.get_attribute("href")

        # A draft, so "My crafts" shows both states.
        page.goto(BASE + "/crafts/add/")
        page.wait_for_selector("form[data-ready=true]", state="attached")
        page.fill("#id_title", "Kilim (work in progress)")
        page.select_option("#id_craft_type", label="Textile")
        page.select_option("#id_community", index=1)
        page.fill("#id_maker_credit", "A Yörük family workshop")
        page.locator("button[value=draft]").click()
        page.wait_for_load_state()
        page.goto(BASE + "/crafts/mine/")
        shot(page, "11-my-crafts.png")
        page.goto(BASE + profile_url)
        shot(page, "12-maker-profile.png")
        desk.close()

        # ---- Visitor, phone ----
        phone = browser.new_context(
            viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="en-GB"
        )
        page = phone.new_page()
        page.goto(BASE + "/")
        shot(page, "07-mobile-home.png", full=False)
        page.goto(BASE + EXAMPLE)
        shot(page, "08-mobile-detail.png", maps=True)
        phone.close()
        browser.close()


if __name__ == "__main__":
    main()
