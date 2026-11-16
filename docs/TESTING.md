# Tests

The project has **192 automated tests** (160 test functions; some run several times with different inputs). They cover **97 %** of the code. GitHub runs all of them on every pull request and every push to `main` (see [CI](#how-the-tests-run)).

| Kind | What it means | Where |
|---|---|---|
| **Unit** | Checks one small piece on its own, e.g. a unit conversion or a distance | `test_units_profiles.py` (units), `test_location.py::test_distance`, `test_flexibility.py::test_parse_tags`, `test_models.py` |
| **Integration** | Loads pages and submits forms through Django against a real PostgreSQL database, then checks the response and what was saved | Most files |
| **End-to-end** | Opens the site in a real browser (Chromium, through Playwright) and clicks through it like a user | `test_e2e.py` |

**Test data** comes from small factories (`tests/factories.py`) that create a craft, user or community with sensible defaults, plus shared fixtures in `tests/conftest.py`:
- `user` / `password`: a signed-up maker with a known password
- `member_client`: a browser session already logged in as that user
- `setup`: a craft type ("Carving", with *tools* and *finish* fields) and a community whose steward is that user

The add-a-craft tests send one complete form (`payload()` in `test_contribute.py`): a carved meerschaum pipe from Eskişehir with two materials, one technique, size, weight, location and a consent record. Each test changes only the part it is checking.

## How the tests run

```bash
uv run pytest                      # everything
uv run pytest tests/test_search.py # one file
uv run pytest -k visibility        # tests whose name contains "visibility"
uv run pytest -m e2e               # browser tests only (first: uv run playwright install chromium)
uv run pytest --cov                # with the coverage report
```

In CI ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) the tests run after linting, Django's checks and the requirements check, and the run fails if coverage drops below 80 %.

---

## 1. Accounts and login · `test_auth.py` (9)
Stories US-01 Register, US-02 Log in and out, US-03 Password reset.

| Test | What it does | Expected result |
|---|---|---|
| `test_signup_creates_user_signs_in_and_redirects_home` | Signs up with a valid email and password | Redirect to home; the account exists; the password is stored hashed, not as typed; header says "Signed in as" |
| `test_password_shorter_than_10_is_rejected` | Signs up with a 7-character password | Form shown again with "at least 10 characters"; no account created |
| `test_invalid_email_is_rejected` | Signs up with "not-an-email" | No account created |
| `test_duplicate_email_shows_clear_error` | Signs up with an email that's already registered | "already registered" error; still only one account |
| `test_login_shows_name_in_header` | Logs in with the right email and password | Header shows "Signed in as", the user's name and "Log out" |
| `test_wrong_credentials_give_the_same_generic_error` (×2) | Logs in once with a wrong email, once with a wrong password | Same generic message both times, so it doesn't reveal which field was wrong |
| `test_logout_requires_post_and_ends_session` | Visits the logout address, then submits the logout form | Just visiting doesn't log out (only a confirmation page); submitting the form ends the session |
| `test_password_reset_link_expires_after_one_hour` | Reads the reset-link lifetime setting | 3,600 seconds (1 hour) |

## 2. Admin account set-up · `test_ensure_admin.py` (7)
The admin account for the live site comes from the `DJANGO_SUPERUSER_EMAIL` and `DJANGO_SUPERUSER_PASSWORD` variables.

| Test | What it does | Expected result |
|---|---|---|
| `test_creates_admin_who_can_log_in_with_any_capitals` | Runs `ensure_admin` with "Ege.Asan@Example.com", then logs in three ways (lower case, mixed, upper case) | Account created in lower case with the admin role; all three logins succeed |
| `test_repairs_an_existing_account` | An existing suspended account with an old password; `ensure_admin` runs twice | Account is active, an admin and has the new password; login works |
| `test_does_nothing_without_variables` | Runs `ensure_admin` with no variables set | Prints "not both set"; no account created |
| `test_site_login_ignores_capitals` | Account "Maker@Example.com"; logs in on the site as "MAKER@example.com" | Login succeeds |
| `test_login_with_the_variables_creates_admin_even_if_start_step_never_ran` | No account exists; variables contain a stray space and a line break; logs in at `/admin/` | Login succeeds and creates the admin account with the cleaned-up password |
| `test_wrong_password_does_not_create_or_change_the_admin` | Logs in with a wrong password, then with a different email | Both fail; no account created |
| `test_admin_login_from_variables_reaches_admin_index` | Logs in at `/admin/` with the variables | The admin home page opens (200) |

## 3. Roles and visibility · `test_roles_visibility.py` (21)
Stories US-05 Roles, US-22 Visibility levels, US-27 Manage users. Most tests use one shared "world": two communities (A and B), one craft at each visibility level in community A plus a draft, and one user per role.

| Test | What it does | Expected result |
|---|---|---|
| `test_visibility_matrix` (×8) | For each of 8 people (visitor, member, member of A, member of B, steward of A, steward of B, admin, author) checks which of the 5 crafts they can see, both in the database rule and by opening each page | Visitor: public only. Member: + members-only. Member of A: + community-only. Steward of A: everything except other people's drafts. Steward of B: public + members. Admin and author: everything. Hidden pages answer "not found" (404), never "forbidden" |
| `test_catalogue_never_lists_restricted_records` | Member of A opens the catalogue | Community-only craft listed; restricted craft not |
| `test_members_cannot_add_crafts` | A "member" (browse-only) opens and submits Add a craft | 403 both times; no "Add a craft" link shown |
| `test_makers_can_add_crafts` | A maker opens Add a craft | Page opens |
| `test_new_sign_ups_are_makers` | Signs up a new account | Its role is maker |
| `test_who_can_edit` | Each of the 8 people opens the edit page of the public craft | Only author, steward of A and admin get the form; visitor is sent to log in; others get 404 |
| `test_member_author_loses_edit_rights` | The author is changed to the member role, then opens their edit page | 404 |
| `test_admin_role_gets_admin_site` | Gives a user the admin role, then takes it away | Admin-site access switches on, then off |
| `test_suspended_users_cannot_log_in` | Suspends a user, then tries to log in | Login refused; no session |
| `test_role_changes_and_suspensions_are_logged` | An admin changes a user to steward, then suspends them | Two log entries (role maker → steward, active True → False), the first recording which admin made it |
| `test_admin_actions_suspend_and_log` | In the admin, selects a user and the admin's own account and runs "Suspend" | The user is suspended; the admin is not (you can't suspend yourself); the change is logged |
| `test_admin_can_search_and_change_role` | Admin searches users for "weaver" and opens the result | User found; edit page has the role field |
| `test_uploaded_photos_follow_craft_visibility` | Uploads a photo to the restricted craft, then requests its address as visitor, member of A and steward of A | 404, 404, then the photo (marked private so it isn't cached publicly); an unknown photo address is 404 |
| `test_createsuperuser_gets_admin_role` | Creates a superuser | Role is admin; staff and superuser flags set |

## 4. Adding, editing and deleting crafts · `test_contribute.py` (22)
Stories US-08 Add, US-09 Edit/delete, US-11 Type-specific fields, US-20 Photos; feedback FB-01–FB-04.

| Test | What it does | Expected result |
|---|---|---|
| `test_requires_login` | A visitor opens Add a craft | Sent to the login page |
| `test_publish_saves_everything` | Publishes the full form with a 2400 × 1200 photo | Every field saved: author, status, type fields, "c. 1978", "Meerschaum, Beeswax", "Eskişehir, Türkiye", coordinates, "6 × 14 × 5 cm", "1.8 oz ≈ 51 g", material origin and notes, alt text; photo resized to 1600 px |
| `test_publish_needs_a_material` | Publishes with no materials | "Add at least one material."; nothing saved |
| `test_draft_without_material_is_private` | Saves a draft with no materials | Saved as draft; author can open it; not in the catalogue; a visitor gets 404 |
| `test_photo_needs_alt_text` | Adds a photo without a description | "Describe the photo"; nothing saved |
| `test_validation` (×6) | Sends one bad value at a time: year 2999, latitude without longitude, size without unit, weight without unit, a type-field value not in its list, no maker credit | Matching error message each time; nothing saved |
| `test_reserved_slug_is_avoided` | Titles a craft "Add" (which would clash with `/crafts/add/`) | Its address becomes `add-craft` |
| `test_required_attribute_field` | The craft type has a required "Wood" field left empty | Not saved |
| `test_returns_fields_for_type` | Asks for the extra fields of the Carving type | The *tools* and *finish* fields, with finish's options |
| `test_no_type_shows_hint` | Asks for extra fields with no type chosen | "Choose a craft type" |
| `test_owner_can_edit_and_rows_are_prefilled` | Author opens the edit form, then saves a new title and drops a material | Form shows the saved values; title and materials update; author unchanged |
| `test_others_cannot_edit_or_delete` | Another maker opens edit and submits delete on someone else's craft | 404 both times; craft still exists |
| `test_delete_asks_then_deletes` | Author opens delete, then confirms | First a "can't be undone" page; after confirming, the craft is gone and they land on My crafts |
| `test_my_crafts_lists_only_mine_including_drafts` | Opens My crafts | Own draft listed; other people's crafts not |
| `test_made_summary_and_units` | Opens a craft with maker, approximate year, size in inches and weight in kg | Page shows "Made by", "c. 1990", "10 × 4 in ≈ 25.4 × 10.2 cm", "2 kg ≈ 4.4 lb" and the local measure |
| `test_hidden_location_never_reaches_the_page` | Opens a craft whose location is set to hidden | Place name shown; coordinates nowhere in the page; "kept private" note |
| `test_approximate_location_is_rounded` | Opens a craft with an approximate location | Map gets 12.3 / 45.7 (rounded); the exact value is not in the page |

## 5. "Other" choices, own details and tags · `test_flexibility.py` (20)
Feedback FB-05: nothing is forced into a fixed list.

| Test | What it does | Expected result |
|---|---|---|
| `test_typed_craft_type_and_community_are_added` | Chooses "Other" and types "  Felt   making " and "Yörük" | New type "Felt making" (spaces tidied) and community "Yörük" created and marked "added by" this user |
| `test_typed_name_reuses_an_existing_entry` | Types "carving" and the community's name in capitals | Existing entries reused; no duplicates |
| `test_other_needs_a_name` | Chooses "Other" for both and types nothing | Two "Type the name…" errors; nothing saved |
| `test_new_entries_appear_in_lists_and_filters` | Adds a craft with a new community, then an admin approves it | New community offered in the form; craft waits for review (no stewards yet); after approval it is listed |
| `test_type_fields_endpoint_explains_new_type` | Asks for extra fields of a typed-in type | "A new craft type has no set fields yet" |
| `test_edit_form_preselects_current_choices` | Opens the edit form | Current type and community are selected |
| `test_typed_units_are_kept_and_not_converted` | Types "karış" for size and "okka" for weight | Shown as "6 × 14 × 5 karış" and "1.8 okka", with no converted value |
| `test_other_unit_needs_a_name` | Chooses "Other" unit and types nothing | "Type the unit you measured in." |
| `test_typed_unit_is_cleared_when_a_listed_unit_is_chosen` | Types a unit but picks "cm" from the list | Typed unit discarded |
| `test_choice_and_multi_choice_accept_own_values` | Types "Smoked" as a finish and "Juniper, Olive, cedar" as extra woods | Saved as typed; edit form puts them back in the Other boxes |
| `test_other_choice_needs_a_value` | Chooses "Other" finish and types nothing | "Type your own value…" |
| `test_own_details_are_saved_and_shown` | Adds "Dye source: Walnut husks" and "Used for: Weddings" | Saved in order, shown on the page and in the edit form |
| `test_detail_row_needs_both_parts` | Gives a value without a label | "Name this detail." |
| `test_parse_tags` | Splits " Ceremonial, natural  dye,#ceremonial,, everyday use " | ["Ceremonial", "natural dye", "everyday use"]: tidied, # removed, duplicates and empties dropped |
| `test_tags_saved_reused_and_shown` | Tags a craft "Ceremonial, natural dye" when "ceremonial" exists | Existing tag reused; tags link to `?tag=`; edit form offers tags already in use |
| `test_catalogue_filters_by_tag` | Filters the catalogue by "ceremonial" | Only the tagged craft; the Tag box shows the filter |
| `test_tag_search_by_name_or_part_of_a_tag` | Searches tags for "natural dye", "#Natural dye" and "dye", then nonsense | First three find the craft; nonsense shows "No crafts match" |
| `test_tag_suggestions_only_from_visible_crafts` | A members-only craft has a tag; a visitor opens the catalogue | Its tag isn't suggested |
| `test_tag_limits` | Adds 16 tags, then one 41-character tag | "Use at most 15 tags."; "Keep each tag under 40 characters" |
| `test_removing_tags_on_edit` | Edits tags from "ceremonial, gift" to "gift" | Only "gift" remains |

## 6. Units, profiles and password reset · `test_units_profiles.py` (15)
Feedback FB-04 units; stories US-04 Profile, US-03 Password reset.

| Test | What it does | Expected result |
|---|---|---|
| `test_metric_size_converts_to_inches` | Size 24 × 18 × 9 cm | "≈ 9.4 × 7.1 × 3.5 in", axes "H × W × D" |
| `test_imperial_size_converts_to_cm_and_skips_missing_axes` | Size with no height, 2 × 1.5 ft | "2 × 1.5 ft", axes "W × D", "≈ 61 × 45.7 cm" |
| `test_no_size_without_values_or_unit` | No values, or a value without a unit | Nothing shown |
| `test_weight` (×4) | 250 g, 2 kg, 3 lb, 4 oz | ≈ 8.8 oz, ≈ 4.4 lb, ≈ 1.4 kg, ≈ 113 g |
| `test_fmt_trims_zeros` | Formats 24.00 and 1.50 | "24" and "1.5" |
| `test_public_profile_lists_published_crafts` | Opens a maker's profile | Name, bio, community and published craft shown; draft not |
| `test_edit_profile` | Saves a new name, bio, community and location | Saved; back to the profile |
| `test_edit_profile_requires_login` | A visitor opens Edit profile | Sent to log in |
| `test_added_by_links_to_profile` | Opens a craft | "Added by" links to the author's profile |
| `test_login_page_links_to_reset` | Opens the login page | Has a "Forgot your password?" link |
| `test_reset_email_is_sent_and_link_works` | Requests a reset and opens the e-mailed link | One e-mail sent; the link opens the new-password form |
| `test_unknown_email_gives_no_hint` | Requests a reset for a known and an unknown email | Same response both times, so it doesn't reveal who has an account |

## 7. Search, filters and sorting · `test_search.py` (19)
Stories US-15 Search, US-16 Filter and sort. Catalogue: a Pomo basket (US, 1900), a Yörük kilim (Türkiye, 1950, wool, slit tapestry), a water pot (Peru), and a restricted "Hidden basket".

| Test | What it does | Expected result |
|---|---|---|
| `test_finds_by_any_field` (×8) | Searches "basket" (title), "feathers" (description), "sedge" (material), "tapestry" (technique), "pomoan basket" (community's other name + title), "türkiye" (country), "coils" (how it's made), "basket wool" | The right craft each time; "basket wool" finds nothing, because every word must match the same craft |
| `test_restricted_records_never_found` | Visitor and member search "hidden" | Restricted craft never appears |
| `test_empty_state_helps` | Searches "zzz" | "No crafts match “zzz”" with a "clear all filters" link |
| `test_title_matches_rank_first` | Searches "basket" when another craft mentions it only in its description | Title match listed first |
| `test_material_technique_country_filters` | Filters by wool, by Slit tapestry, by Peru | Kilim, kilim, water pot |
| `test_filters_combine_with_search` | "basket" + Peru; Basketry + United States | Nothing; the Pomo basket |
| `test_sorting` (×4) | Sorts by name, oldest made, newest made, recently added | Correct order each time |
| `test_filters_are_kept_in_page_links` | Searches with sorting on a two-page result | The page-2 link keeps the search and sort |
| `test_options_only_from_visible_crafts` | A restricted craft has a material; a visitor opens the catalogue | That material isn't offered as a filter |

## 8. Search by location · `test_location.py` (10)
Feedback FB-11. Crafts in Antalya, Konya, a hidden place near Antalya, an approximate place near Antalya, Lima, and one with no coordinates.

| Test | What it does | Expected result |
|---|---|---|
| `test_distance` | Distance Antalya → Konya | 191 km |
| `test_within_distance_nearest_first` | Near Antalya within 50 km, then 250 km | Antalya, approximate pot; then also Konya, nearest first |
| `test_hidden_places_never_found_by_location` | Searches 25 km around the hidden place | Not found |
| `test_approximate_places_use_the_rounded_point` | Searches right next to the approximate pot's real point | Distance measured to the rounded, published point; marked "(approximate)" |
| `test_cards_show_distance_and_map_data` | Near Antalya within 250 km | Cards show "≈ 191 km away"; heading names the place; map data excludes the hidden place |
| `test_place_text_without_coordinates_matches_names` | Place "Antalya", then "Peru", without coordinates (the lookup failed) | Matched by place, region and country names |
| `test_location_combines_with_other_filters` | Within 1,000 km of Antalya + search "felt" | Konya felt only |
| `test_bad_coordinates_are_ignored` (×2) | Latitude "abc"; latitude 95 | All 6 crafts listed, no error |
| `test_unknown_distance_falls_back_to_default` | Distance "7 km" (not an option) | Default distance used |

## 9. Consent, review and reports · `test_review.py` (22)
Stories US-23 Consent, US-24 Steward review, US-25 Reports. People: a maker, a steward of the craft's community, a steward of another community, and an admin.

| Test | What it does | Expected result |
|---|---|---|
| `test_needed_to_submit` | Submits without who agreed and when | "Needed before the craft can be submitted or published."; nothing saved |
| `test_optional_for_drafts` | Saves a draft with no consent | Draft saved, no consent record |
| `test_partial_consent_on_a_draft_is_checked` | Saves a draft with consent filled in except the date | Not saved (half a record isn't accepted) |
| `test_visible_to_stewards_and_admins_only` | Opens the craft as maker, steward, admin, visitor and the other steward | Consent details shown only to the community's steward and the admin |
| `test_maker_submission_waits_for_review` | A maker submits | Status "pending review"; the steward is e-mailed; visitors get 404; the maker can open it |
| `test_queue_lists_only_my_communities` | Opens the review queue as steward, admin, other steward and maker | Listed for steward and admin; not for the other steward; maker gets 403; header shows "1 waiting" |
| `test_decisions` (×3) | Steward approves; requests changes with a note; rejects with a note | Published / back to draft / unpublished; decision recorded; maker e-mailed; the note appears in the e-mail, on the craft page and in My crafts |
| `test_changes_and_rejection_need_a_comment` | Rejects with a blank note | Nothing changes |
| `test_only_this_communitys_reviewers_decide` | Maker and other steward try to approve | 404; still pending |
| `test_maker_edits_go_back_to_review` | Maker edits their published craft | Change saved; status back to pending |
| `test_stewards_publish_directly` | The community's steward submits a craft | Published immediately |
| `test_form_button_matches_role` | Opens Add a craft as maker, then steward | "Submit for review" vs "Publish" |
| `test_anyone_can_report_without_logging_in` | A visitor opens the report form from a craft page and sends it | Report saved as open with no reporter; steward e-mailed |
| `test_spam_trap` | Sends a report with the hidden "website" field filled in (as bots do) | Discarded |
| `test_cannot_report_what_you_cannot_see` | A visitor opens the report form of a restricted craft | 404 |
| `test_reports_in_queue_and_unpublish_now` | Steward sees a report in the queue and clicks "Unpublish now" | Only their community's steward sees and handles it; craft unpublished; report resolved; logged as a decision; visitors get 404 |
| `test_mark_resolved_keeps_the_record` | Admin marks a report resolved with a note | Report resolved; craft stays published |
| `test_stewards_cannot_see_edit_or_decide_on_others_drafts` | Steward opens, edits and approves a maker's unsubmitted draft | 404 for all; still a draft |
| `test_stewards_unpublish_but_do_not_delete` | Steward, then admin, tries to delete a craft | Steward gets 404; admin deletes it |
| `test_no_approval_without_consent` | Steward approves a pending craft with no consent record | Nothing changes |

## 10. Community pages · `test_communities.py` (7)
Story US-17. Community: Diné, also known as Navajo.

| Test | What it does | Expected result |
|---|---|---|
| `test_page_shows_own_name_first_and_crafts` | A visitor opens the page | "Diné" before "Also known as Navajo"; public craft listed, members-only not; no edit button |
| `test_craft_pages_link_to_the_community_page` | Opens one of its crafts | Links to the community page |
| `test_stewards_edit_the_description` | Its steward edits region and description | Saved; the community's name can't be changed this way |
| `test_others_cannot_edit` (×2) | A maker, and a steward of another community, open and submit the edit form | 404 |
| `test_admins_can_edit` | An admin opens the edit form | Opens |
| `test_non_ascii_community_names_have_pages` | Community "Yörük" | Its page and its craft's page open (this was a bug) |

## 11. Members' stories · `test_stories.py` (6)
Feedback FB-10.

| Test | What it does | Expected result |
|---|---|---|
| `test_members_can_share_stories` | A browse-only member shares a family story | Saved; page jumps to it; the craft's author is e-mailed; visitors see the story and the writer's name, plus "Log in or…" instead of the form |
| `test_visitors_cannot_post` | A visitor submits a story | Sent to log in; nothing saved |
| `test_not_on_crafts_you_cannot_see` | A member posts on a restricted craft | 404 |
| `test_story_needs_text_and_connection` | Posts with blank text and no connection | Nothing saved |
| `test_authors_edit_and_delete_only_their_own` | Someone else, then the writer, edits and deletes a story | Someone else gets 404; the writer can edit, then delete |
| `test_stewards_hide_and_show_stories` | A steward of another community tries to hide a story; the right steward hides it with a reason, then shows it again | Outsider 404. Once hidden: listed in the queue, gone for visitors, still visible to its writer with the reason. Then visible again |

## 12. Pages · `test_views.py` (14)

| Test | What it does | Expected result |
|---|---|---|
| `test_health_check` | Opens `/healthz` (Render checks this) | "ok" |
| `test_home_lists_public_crafts` | Opens the home page | Shows a public craft |
| `test_lists_only_visible_crafts` | A visitor opens the catalogue | Public craft listed; members-only and draft not |
| `test_member_sees_members_only_records` | A member opens the catalogue | Members-only craft listed |
| `test_filter_by_craft_type` | Filters by Pottery | Only the pot |
| `test_pagination_24_per_page` | 30 crafts | 24 on page 1, 6 on page 2 |
| `test_no_status_remarks_on_cards_or_footer` | Opens the catalogue | No "Sample data" or "Members only" labels |
| `test_shows_credits_and_report_link` | Opens a craft | Maker, community and "Report or request removal" shown |
| `test_hidden_records_are_not_found_for_visitors` (×3) | A visitor opens members-only, community-only and restricted crafts | 404 each |
| `test_members_only_visible_after_login` | A member opens a members-only craft | Opens |
| `test_unknown_slug_is_404` | Opens `/crafts/nope/` | 404 |
| `test_referrer_policy_allows_map_services` | Reads the home page's Referrer-Policy | `strict-origin-when-cross-origin` (OpenStreetMap refuses requests without one; this was a map bug) |

## 13. Data model and sample data · `test_models.py` (8)

| Test | What it does | Expected result |
|---|---|---|
| `test_anonymous_sees_only_published_public` | Applies the visibility rule for a visitor | Public craft only |
| `test_member_also_sees_members_only` | Same for a member | Public + members-only |
| `test_staff_sees_everything` | Same for staff | All five, including the draft |
| `test_rows_use_definition_labels_units_and_skip_empty` | Craft with height 30, empty glaze, watertight yes | Shows "Height: 30 cm" and "Watertight: Yes"; empty glaze hidden |
| `test_retired_definition_is_hidden_but_data_kept` | A type field is switched off | Not shown, but the stored value is kept |
| `test_multi_choice_is_joined` | Multiple choice ["Glass", "Shell"] | "Glass, Shell" |
| `test_seed_is_idempotent_and_labelled` | Loads the fictional samples twice | Same counts the second time; at least 10 crafts over 4 types, all marked as samples |
| `test_every_sample_credits_maker_and_has_alt_text` | Loads the samples | Every craft credits a maker; every photo has alt text |

## 14. Real examples · `test_reference.py` (8)
The 22 real crafts from public sources (`crafts/reference_data.py`).

| Test | What it does | Expected result |
|---|---|---|
| `test_seed_creates_published_public_reference_crafts` | Loads the real examples | All 22 published and public, each with maker credit, https sources, photos with alt text and a Commons file, materials, techniques and its tags |
| `test_seed_is_idempotent` | Loads them twice | No duplicates |
| `test_replace_samples_keeps_user_records` | Loads samples, a user adds a craft to a sample community, then real examples replace the samples | Samples gone; the user's craft and the community it uses kept |
| `test_commons_urls_are_encoded` | Builds the photo address for "Kuksa, Inari åå.jpg" | Commas, spaces and å encoded correctly |
| `test_craft_page_shows_sources_and_credits` | Opens the Pomo basket by Jenny Hughes | Maker, Wikipedia source, Commons photo, photo credit and licence link shown; no remark badges |
| `test_public_domain_credit_is_static` | Opens the Diné rug | "U.S. National Archives (NARA), 1933 · Public domain", with no online credit lookup |
| `test_catalogue_cards_have_no_remark_badges` | Opens the catalogue | No "Real example" or "Sample data" labels |
| `test_old_start_command_now_loads_real_examples` | Runs the old start-up command `seed_sample_data` | Real examples loaded instead of placeholders |

## 15. In a real browser · `test_e2e.py` (4)
Run in Chromium with Playwright against a running copy of the site loaded with the sample crafts.

| Test | What it does | Expected result |
|---|---|---|
| `test_demo_flow` | Home → Browse crafts → open a craft → sign up → catalogue again → log out | Home text shown; at least 8 cards; "Made by" on the craft; "Signed in as" after sign-up; more cards once signed in (members-only records); "Log in" link after logging out |
| `test_no_horizontal_scroll_on_phone` | Opens 5 pages (home, catalogue, location search, a craft, login) at phone width (360 px) | No page scrolls sideways (this was a bug) |
| `test_add_craft_in_browser` | Signs up, opens Add a craft, picks Basketry, waits for its fields, fills in materials (adding a second row with "+ Add material"), size and consent, publishes | Craft page shows the maker, "Spruce root, Bark", 2001, "30 cm" with "11.8 in", the material origin and an Edit link |
| `test_other_choices_and_tags_in_browser` | Checks the "Other" box is hidden at first, then types a new craft type and community, a tag, a typed unit "karış" and an own detail, and publishes | The note about new types appears; the page shows "Felt making", "Yörük", "3 karış", "Madder root" and a "#nomadic" tag link |
