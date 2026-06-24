---
id: RC-IMP-07
title: Survey Settings CSV — Column Reference and Format Guide
domain: Data Import
applies_to:
- REDCap projects with at least one survey-enabled instrument
prerequisites:
- 'RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap'
- 'RC-SURV-02 — Survey Settings: Basic Options & Design'
version: '1.0'
last_updated: '2026-05-07'
related:
- id: RC-IMP-03
  title: 'CSV Upload Reference: All Bulk Upload Options in REDCap'
- id: RC-SURV-02
  title: 'Survey Settings: Basic Options & Design'
- id: RC-SURV-03
  title: 'Survey Settings: Behavior, Access & Termination'
tags:
- data import
- data
synonyms:
- how do i import survey settings via csv
- bulk edit survey settings in a spreadsheet
- copy survey configuration across projects
- upload survey settings csv for all instruments
- replicate completion text and confirmation emails
- 62-column survey settings file structure
- export and re-import survey settings
- change response limits for many surveys at once
---

# 1. Overview

The Survey Settings CSV allows bulk export and re-import of survey configuration across all survey-enabled instruments in a project. This is useful for replicating settings (e.g., response limits, completion text, confirmation emails) across projects without reconfiguring each instrument manually.

**Location:** Online Designer → download icon next to "Survey Settings" (project-level download of all survey-enabled instruments).

**Upload behavior — Additive/update:** Imported rows overwrite the current settings for the instruments named in the file. Instruments not listed in the file are left untouched.

**Rights required:** Project Design and Setup (at least one instrument must be survey-enabled in the project).

**Always download first.** The full 62-column header must be exact. Always start from a file downloaded from REDCap rather than building the header from memory.

For full coverage of survey settings through the REDCap UI, see [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) and [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md).

---

# 2. File Structure

One row per survey-enabled instrument. The header row lists all 62 columns exactly as exported — do not rename or reorder them. Instruments that are not survey-enabled are excluded from the file; there is no way to enable a survey for the first time via this upload (the instrument must already be enabled in the Online Designer).

HTML content (survey instructions, acknowledgement text, confirmation email body, etc.) is valid in the relevant columns and will be rendered in the survey interface. When HTML contains literal newlines (e.g., `<p>` tags split across lines), standard CSV quoting rules apply — wrap the entire cell value in double quotes. REDCap's own download always quotes these cells correctly; files built from scratch must do the same.

The file exports default values for some columns (e.g., `response_limit_include_partials`, `repeat_survey_btn_location`) even when the parent feature is disabled. On re-import, REDCap reads all columns, so these orphaned defaults are harmless.

---

# 3. Column Reference

Columns are grouped below by functional area, in the order they appear in the file.

## Row identifier

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `form_name` | Yes | Instrument variable name (e.g., `demographics`). Must match an existing instrument in the target project exactly. Case-sensitive. |
| `survey_enabled` | Yes | `Y` = instrument is active as a survey. `N` = survey is offline (participants cannot access it; logged-in users can still fill it in as a regular form). Changing this column on import toggles the survey status. |

## Survey title and instructions

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `offline_instructions` | No | Text displayed to participants who attempt to access the survey when it is offline. Supports HTML. Leave blank to use the REDCap default offline message. |
| `title` | No | Survey title shown to participants in the browser header and at the top of the survey page. Defaults to the instrument name when blank. Supports a limited subset of HTML tags. |
| `instructions` | No | Introductory text block shown between the title and the first question. Supports full rich-text HTML. When this field contains embedded newlines, the cell must be quoted. |

## Survey design and appearance

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `survey_width_percent` | No | Integer (e.g., `75`). Controls the width of the survey content area as a percentage of the browser window. Leave blank for the REDCap default (approximately 80%). |
| `enhanced_choices` | No | `Y` = use large enhanced radio/checkbox buttons (pill-style). `N` = standard compact radio/checkbox inputs. |
| `text_size` | No | Controls base font size. Known values: `SMALL`, `MEDIUM`, `LARGE`, `X-LARGE`. Leave blank for the site default. |
| `font_family` | No | Numeric code representing the selected font. REDCap stores fonts as an internal index rather than a font name string (e.g., `16`). Download an existing survey's settings to see available codes; leave blank for the default font. |
| `custom_css` | No | Raw CSS string applied to the survey page. Leave blank for no custom styling. |
| `theme` | No | Name of a saved survey theme. Leave blank to use no theme (default REDCap colors). |
| `theme_bg_page` | No | Hex color code for the survey page background (e.g., `#FFFFFF`). Only applied when `theme` is set. |
| `theme_text_buttons` | No | Hex color for navigation button text. |
| `theme_text_title` | No | Hex color for the survey title text. |
| `theme_bg_title` | No | Hex color for the survey title background band. |
| `theme_text_sectionheader` | No | Hex color for section header text. |
| `theme_bg_sectionheader` | No | Hex color for section header background. |
| `theme_text_question` | No | Hex color for question label text. |
| `theme_bg_question` | No | Hex color for the question row background. |

## Display behavior

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `promis_skip_question` | No | `Y` = enable the PROMIS skip-question feature (used with computer adaptive tests). Leave blank or `N` for standard surveys. |
| `question_auto_numbering` | No | `Y` / `N`. When `Y`, REDCap automatically numbers each question in sequence (1, 2, 3…). |
| `question_by_section` | No | `Y` / `N`. When `Y`, the survey shows one section per page (each section header creates a new page break). |
| `display_page_number` | No | `Y` / `N`. Show "Page X of Y" at the bottom of multi-page surveys. |
| `hide_back_button` | No | `Y` / `N`. When `Y`, the "Previous Page" button is hidden — participants cannot navigate backward. |
| `end_of_survey_pdf_download` | No | `Y` / `N`. Show a "Download PDF" link on the survey completion page. |
| `email_participant_field` | No | Variable name of a field that holds the participant's email address. REDCap uses this to send the confirmation email without a Participant List entry. Leave blank if using the Participant List or no confirmation email. |
| `show_required_field_text` | No | `Y` / `N`. Show the "* must provide value" legend at the top of the survey. |
| `survey_show_font_resize` | No | `Y` / `N`. Show the font-size resize control on the survey toolbar. |

## Results sharing

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `view_results` | No | `Y` / `N`. Allow participants to view an aggregate summary of all survey responses after completing the survey. |
| `min_responses_view_results` | No | Integer. Minimum number of completed responses required before the results summary is shown to any participant. Prevents disclosure when only a few responses exist. |
| `check_diversity_view_results` | No | `Y` / `N`. Require response diversity before showing aggregate results (reduces risk of reverse-engineering individual answers). |

## Accessibility

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `text_to_speech` | No | `Y` / `N`. Enable text-to-speech for the survey (reads questions aloud). Requires site-level TTS configuration. |
| `text_to_speech_language` | No | Language/locale string for TTS (e.g., `en-US`). Leave blank when TTS is disabled. |

## Navigation buttons

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `survey_btn_hide_submit` | No | `Y` / `N`. Hide the final Submit button on the last page (uncommon; typically used when an action tag or custom logic handles submission). |
| `survey_btn_text_prev_page` | No | Custom label for the "Previous Page" button. Leave blank for the REDCap default label. |
| `survey_btn_text_next_page` | No | Custom label for the "Next Page" button. Leave blank for the REDCap default label. |
| `survey_btn_text_submit` | No | Custom label for the final "Submit" button. Leave blank for the REDCap default label. |

## Response limits

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `response_limit` | No | Integer. Maximum number of completed responses allowed. Leave blank for no limit. Once the limit is reached, new participants see the `response_limit_custom_text` message instead of the survey. |
| `response_limit_include_partials` | No | `Y` / `N`. When `Y`, in-progress (partial/incomplete) responses count toward the limit. |
| `response_limit_custom_text` | No | HTML message shown to participants who try to access the survey after the response limit is reached. **Note:** REDCap exports a default message here even when no response limit is set — this is normal and harmless. |

## Survey time window

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `survey_time_limit_days` | No | Integer. Days component of the time-limited access window. All three time-limit columns must be specified together (use `0` for unused units). Leave all three blank to disable the time limit. |
| `survey_time_limit_hours` | No | Integer. Hours component of the time-limited access window. |
| `survey_time_limit_minutes` | No | Integer. Minutes component of the time-limited access window. |
| `survey_expiration` | No | Specific date/time after which the survey closes to all participants. Format: `YYYY-MM-DD HH:MM` in server time. Leave blank for no expiration date. |

## Access and session controls

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `survey_auth_enabled_single` | No | `Y` / `N`. Enable Survey Login for this survey. When active, participants must enter a per-participant login code (configured in the Online Designer under Survey Settings) before they can view the survey. This is a password-like gate tied to the individual record — distinct from the Survey Access Code, which is a shorthand alternative to the public survey URL and is unrelated to this setting. |
| `save_and_return` | No | `Y` / `N`. Allow participants to save a partially completed survey and return later to finish it. |
| `save_and_return_code_bypass` | No | `Y` / `N`. When `Y`, participants can return to a saved survey without entering a return code (uses a browser cookie instead). |
| `edit_completed_response` | No | `Y` / `N`. Allow participants to re-open and edit a survey they have already submitted. |

## Post-completion behavior

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `end_survey_redirect_next_survey` | No | `Y` / `N`. Automatically redirect participants to the next survey in the Survey Queue upon completion. |
| `end_survey_redirect_next_survey_logic` | No | Logic expression string. When populated, the redirect to the next survey only occurs if this expression evaluates to true. Leave blank for unconditional redirect. |
| `end_survey_redirect_url` | No | URL to redirect participants to after completing the survey (instead of the default completion page). Leave blank to show the default REDCap completion page. |
| `repeat_survey_enabled` | No | `Y` / `N`. Show a "Take Survey Again" button on the completion page, allowing participants to submit additional responses. |
| `repeat_survey_btn_text` | No | Custom label for the "Take Survey Again" button. Leave blank for the default label. |
| `repeat_survey_btn_location` | No | Where the repeat button appears. `BEFORE_SUBMIT` = shown above the Submit button on the last page. `AFTER_SUBMIT` = shown on the completion page. **Note:** REDCap exports `BEFORE_SUBMIT` as a default even when `repeat_survey_enabled` is `N`. |
| `acknowledgement` | No | HTML content of the survey completion page shown to participants after submission. This is the "end of survey" message — distinct from the confirmation email. Supports full rich text. |

## Stop actions (e-Consent)

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `stop_action_delete_response` | No | `Y` / `N`. In e-Consent surveys, when a participant triggers the stop action (e.g., declines consent), delete their response record entirely rather than saving a partial record. |
| `stop_action_acknowledgement` | No | HTML message shown to a participant after the stop action is triggered. Leave blank for no message. |

## Confirmation email

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `confirmation_email_from_display` | No | Display name for the confirmation email from-address (e.g., `Study Team`). Leave blank to use the raw email address as the display name. |
| `confirmation_email_from` | No | From-address for the confirmation email. Must be a valid email associated with a REDCap user in the project. Leave blank to disable the confirmation email entirely. |
| `confirmation_email_subject` | No | Subject line for the confirmation email. |
| `confirmation_email_content` | No | HTML body of the confirmation email. Supports piping (`[field_name]`) to personalize content with participant data. |
| `confirmation_email_attach_pdf` | No | `Y` / `N`. Attach a PDF snapshot of the participant's completed survey responses to the confirmation email. |

---

# 4. Annotated Example

The table below shows values from a real export. Only key columns are shown — the full file contains all 62.

| `form_name` | `survey_enabled` | `title` | `text_size` | `show_required_field_text` | `response_limit` | `response_limit_custom_text` | `repeat_survey_btn_location` | `acknowledgement` | `confirmation_email_attach_pdf` |
|---|---|---|---|---|---|---|---|---|---|
| `screening` | `Y` | `Form 1` | `LARGE` | `Y` | *(empty)* | `<p>Thank you for your interest; the survey is closed...</p>` | `BEFORE_SUBMIT` | `<p><strong>Thank you for taking the survey.</strong></p>` | `N` |
| `demographics` | `Y` | `Demographics` | `LARGE` | `Y` | *(empty)* | `Thank you for your interest; the survey is closed...` | `BEFORE_SUBMIT` | `<p><strong>Thank you for taking the survey.</strong></p>` | `N` |
| `phq9` | `Y` | `Phq9` | `LARGE` | `Y` | *(empty)* | `<p>Thank you for your interest; the survey is closed...</p>` | `BEFORE_SUBMIT` | `<p><strong>Thank you for taking the survey.</strong></p>` | `N` |

Key observations from this example:

- **`response_limit_custom_text` is populated even when `response_limit` is blank.** REDCap exports a default fallback message regardless of whether a limit is active. This value is stored but only shown to participants when a limit is actually configured.
- **`response_limit_custom_text` may or may not include HTML tags** — the `demographics` row uses plain text while `screening` uses `<p>` tags. Both are accepted; plain text is rendered without formatting.
- **`repeat_survey_btn_location` exports as `BEFORE_SUBMIT` even when `repeat_survey_enabled` is `N`.** This is an export default — harmless on re-import.
- **HTML in `instructions` and `acknowledgement` must be quoted** (standard CSV) when it contains commas or newlines. When copying values from a REDCap export, this quoting is already applied correctly.

---

# 5. Common Mistakes

**Using the instrument display label instead of the variable name** in `form_name`. The variable name is lowercase and underscored (e.g., `social_history`, not `Social History`).

**Attempting to enable a survey for the first time via this file.** Setting `survey_enabled = Y` for an instrument that has never been configured as a survey will not work — the instrument must first be enabled in the Online Designer.

**Building the header row from memory.** The full 62-column header must be exact. Always start from a file downloaded from REDCap.

**Omitting CSV quoting around HTML with newlines.** Instructions or acknowledgement text that contains literal newlines (from `<p>` tags on separate lines) will break CSV parsing if not enclosed in double quotes.

**Setting `response_limit` without setting `response_limit_custom_text`.** Participants who hit the limit will see either a blank page or the REDCap default — always provide a clear, friendly message.

---

# 6. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) (full UI reference)
- [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md)
- [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) — e-Consent Framework Setup and Management (stop action columns)
- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)(ASI CSV format — [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md))
