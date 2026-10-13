# UI design: M1 running demo

The low-fidelity wireframes (T-06) were replaced by the working pages of the M1 demo. These screenshots are the current UI reference. Later milestones add the pages below the line.

| Page | Desktop / state | Phone (390 px) |
|---|---|---|
| Home | ![Home](screenshots/01-home.png) | ![Home on phone](screenshots/07-mobile-home.png) |
| Catalogue (visitor: public crafts only) | ![Catalogue](screenshots/02-catalogue.png) | |
| Craft detail with craft-type details, credits and report link | ![Detail](screenshots/03-craft-detail.png) | ![Detail on phone](screenshots/08-mobile-detail.png) |
| Sign up with validation (password ≥ 10 characters) | ![Sign up](screenshots/04-signup-validation.png) | |
| Signed in: name in header, members-only crafts visible | ![Signed in](screenshots/05-signed-in-catalogue.png) | |
| Login with generic error message | ![Login error](screenshots/06-login-error.png) | |

## Layout principles
- **Credit first:** maker and community sit directly under the title on every craft page.
- **Sample data is always labelled.** No real cultural content is shown without consent.
- **Craft-type details** come from the attribute definitions, so each type shows its own fields.
- **Accessible basics:** skip link, visible focus ring, labelled form fields, alt text on every image, AA colour contrast.
- **Low bandwidth:** server-rendered HTML, one CSS file, lazy-loaded images, no JavaScript framework.

---
Next pages (M2–M4): add/edit craft form with dynamic fields, image upload, my crafts, profile, search & filters, steward review queue, report form.
