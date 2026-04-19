RC-MLM-01

**Multi-Language Management**

| **Article ID** | RC-MLM-01 |
|---|---|
| **Domain** | Multi-Language Management |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | None |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-SURV-01 — Survey Setup; RC-ALERT-01 — Alerts and Notifications Setup; RC-AT-11 — Action Tags: Mobile App; RC-CC-20 — Control Center: Multi-Language Management |

---

# 1. Overview

Multi-Language Management (MLM) is a built-in REDCap feature that allows data entry forms and surveys to be displayed in multiple languages simultaneously. When MLM is enabled, respondents and data entry users see a language selector and can switch languages in real-time without losing or corrupting stored data. MLM covers field labels, choice labels, survey settings, alert messages, missing data code labels, PDF customizations, MyCap settings, and user interface text — but it does **not** translate content automatically. All translations must be provided by the project team. This article covers the full MLM workflow for project-level users: setting up languages, translating content, managing language selection behavior, and using MLM-specific action tags.

> **Note:** MLM must be enabled at the system level by a REDCap administrator before it is available to projects. This is configured in the Control Center under Miscellaneous Modules → Multi-Language Management (see **RC-CC-20**). Contact your REDCap administrator if Multi-Language Management does not appear in your Applications menu.

---

# 2. Key Concepts & Definitions

**Multi-Language Management (MLM)**
A REDCap feature that manages the display of multiple languages within a single project. MLM controls which translation to show for each piece of project content depending on the active language for a given user, survey respondent, or server-side process.

**Translation Domain**
The category of content being translated. MLM operates across two translation domains per language:
- **User interface (UI) translations** — strings that REDCap displays in the context of data entry or surveys (button labels, system messages, etc.). Default values are set by the REDCap administrator via system languages and may be overridden at the project level unless restricted by the administrator.
- **Project-specific translations** — all data dictionary items (field labels, choice labels, section headers), survey settings (title, instructions, completion text), survey queue custom messages, ASI and alert subjects and message bodies, missing data code labels, PDF customizations, and MyCap settings.

**System Language**
An administrator-configured library of UI translations for a given language. Think of system languages as the REDCap instance's shared pool of UI strings that projects can inherit from when setting up a new language. Projects can subscribe to a system language so that UI translations update automatically when the administrator updates the system language.

**Base Language**
The language that corresponds to the project's UI language — i.e., the language in which REDCap's own menus and dialog messages appear (set by the administrator). The base language tab in MLM shows the source text of all translatable items but does not allow editing those items there (edits happen in the Online Designer or Survey Settings). The base language is also typically the language used during project design (field labels written in the base language). A project can have the base language set to inactive — it does not need to be visible to survey respondents.

**Fallback Language**
A designated language used when a translation is missing in the language currently set as active. If the fallback translation is also missing, MLM falls back to the base language (i.e., the raw data dictionary text or the language.ini file configured for the project). Setting a fallback language prevents respondents from seeing untranslated text.

**Language ID**
A unique case-insensitive identifier assigned to each language in a project. The Language ID should correspond to an ISO 639-1 code (e.g., `en` for English, `de` for German, `es` for Spanish), optionally followed by an ISO 3166-1 country code (e.g., `en-US`, `de-DE`). Language IDs must use only letters and hyphens. Using standard ISO codes enables automatic browser language detection for survey respondents and is required for MyCap language matching.

**Active Language**
A language that has been turned on and is available for selection by users or survey respondents. Languages can be added to a project but remain inactive — only active languages appear in language selectors.

**Language Preference Field**
An optional project field (radio or dropdown type) whose value stores a participant's preferred language. REDCap uses the value of this field to determine which language to display in server-side processes (ASIs, scheduled alerts, PDF rendering) where no browser session is available. The field behaves like the designated email field — its value is synchronized across all events and repeat instances.

**Opt-in Model**
Everything in MLM is opt-in. Adding a language to a project does not automatically translate anything. Each item that should be translated must be explicitly provided with a translation. Items without a translation fall back through the fallback → base language chain.

**REDCap Language Files vs. MLM Languages**
These are two separate, easily confused systems. REDCap's own UI language files (`.ini` files, e.g., `English.ini`) contain all strings used to render REDCap's interface system-wide — over 14,000 unique strings covering every REDCap page. These files are managed by REDCap administrators via the Language File Creator/Updater and are set in General Configuration (or per-project via Edit Project's Settings). They are installed on the server's file system and apply globally.

MLM languages are distinct. MLM translates only the subset of REDCap UI strings that appear on data entry and survey pages (approximately 570 strings), plus all project-specific content (data dictionary, survey settings, alerts, etc.). MLM languages are configured per project or at the system level via the Control Center, and are selectable by individual users and survey respondents in real-time. Do not confuse a REDCap `.ini` language file with an MLM system language — they serve different purposes and are managed separately.

---

# 3. Setting Up Languages in a Project

## 3.1 Access and Prerequisites

The MLM setup page is accessed via **Applications → Multi-Language Management**. Project Design and Setup rights are required.

> **Important:** The MLM setup page is locked in **Production** projects. To add or modify languages, switch to Draft Mode first. Additionally, only one user may edit MLM settings at a time — if another user has the page open, the Save button will be unavailable.

## 3.2 Adding a New Language

1. Open the Multi-Language Management page from the Applications menu.
2. Click **+ Add a new language**.
3. Choose one of the three initialization methods (see 3.3 below). Click **Continue**.
4. Enter or confirm the **Language ID** (ISO 639-1 code recommended) and the **Language Display Name** (the name shown in the language selector — enter it in the language itself, e.g., "Deutsch" for German, not "German").
5. Optionally enter a **Sort Override** value to control the order languages appear in selectors.
6. Click **Add Language** to add the language to the project.
7. Click **Save Changes** (or use Ctrl+S) to commit all changes. The page does not auto-save — an orange save button or orange strip at the top signals unsaved changes.

## 3.3 Initialization Methods

| Method | When to Use |
|---|---|
| **From available system languages** (preferred) | A system language for the target language has been configured by the administrator. Optionally subscribe for automatic UI updates. |
| **From a file** (JSON, CSV, or INI) | A translation file is available from a previous project export, an external translator, or a shared library. Choose whether to import UI strings, project-specific items, or both. |
| **From scratch** (not recommended) | No system language or file is available. All translations must be entered manually. Error-prone and time-consuming. |

> **Note:** On some installations, administrators restrict project languages to centrally maintained system languages only. In that case, "Initialize from system languages" will be the only available option.

## 3.4 Managing Language Settings

After adding languages, the Languages tab shows a table with the following columns:

| Column | Purpose |
|---|---|
| **Active** | Toggle to enable or disable the language for selection by users and respondents. |
| **Base Language** | Radio button to designate which language matches the project's UI language. Only one language can be the base language. |
| **Fallback** | Radio button to designate which language serves as the fallback when a translation is missing. |
| **RTL** | Checkbox to enable right-to-left text rendering for languages such as Arabic or Hebrew. |
| **MyCap** | Checkbox to enable the language in the MyCap app. Only shown when MyCap is active in the project. Requires a Language ID matching one of MyCap's supported language codes. |

Use the **Edit** (pencil) button to change a language's ID, display name, notes, sort order, or subscription status.

Use the **Update** (sync/arrow) button to import updated translations — either by syncing from a system language or by uploading a translation file. File imports are additive by default (existing translations are preserved unless "Overwrite" is selected), so partial imports (e.g., a single instrument's export) are safe.

## 3.5 Snapshots

The **Create Snapshot** button saves a ZIP archive of all current language exports as a backup. Snapshots are created automatically when a project is first moved to Production and each time drafted changes are approved. Snapshots reflect the saved state — unsaved changes are not captured. In Production mode, snapshots do not include drafted (unapproved) changes. Individual files from a snapshot can be re-imported to restore a previous state.

## 3.6 Settings Tab

The Settings tab controls three project-level MLM behaviors:

1. **Highlight untranslated text** — Visually marks items missing a translation on data entry forms and survey pages. Useful during development. Recommended off in Production.
2. **Attempt to match the initially displayed language to the browser's preferred language** — When enabled, REDCap tries to match a first-time visitor's browser language setting to one of the project's active languages. Requires Language IDs to be valid ISO codes. Only triggers for users who have not yet selected a language.
3. **Disable multi-language support for this project** — Turns off MLM for the project. Useful for troubleshooting to rule out MLM as the cause of a display issue.

---

# 4. Understanding Base Language and Fallback

The **Base Language** should match the project's UI language — the language in which REDCap's system text (button labels, dialog messages) is displayed. It is also usually the language in which field labels were written in the Online Designer. If the project's data dictionary language does not match the system UI language, add a language entry that represents each and designate them appropriately.

The **Fallback Language** is displayed when a translation for the active language is missing. If the fallback translation is also missing, REDCap displays the base language content (the raw data dictionary text or the configured language.ini file).

A common setup for a two-language project (English UI, German translation):
- `en` — Base Language, also set as Fallback, Active
- `de-DE` — Active, subscribed to the German system language

> **Note:** The base language tab in the Forms/Surveys and MyCap sections shows a read-only view of source text with no translation inputs. Fields can be excluded from translation on the base language tab (they will not appear in other languages' translation screens). Clicking the base language button in the Alerts section opens the alert exclusion and Language Source settings, not a translation screen.

---

# 5. Translating Project Content

Translation is organized by content type. Navigate to each tab or use the action buttons in the Languages table to access the translation screens.

## 5.1 Enabling Instruments per Language

Before translating field content, each language must be enabled for each instrument separately — in data entry mode, survey mode, or both. This is done on the **Forms/Surveys** tab by selecting a language and toggling the Data Entry and Survey switches for each instrument.

> **Common pitfall:** Adding a language to the project and providing translations does not automatically make those translations visible. The language must also be toggled on for each instrument where it should appear.

## 5.2 Translating Fields

On the Forms/Surveys tab, select a non-base language and click **Translate** next to an instrument to open the field translation screen. For each field:

- The **default text** (base language content) is displayed for reference. A copy icon lets you copy it to the translation input for manual editing.
- Enter the translation in the input field below. A **Rich Text Editor** button is available for fields that support HTML.
- A green indicator means the translation is complete; a red indicator means it is missing.
- An **orange marker** on the default text means the underlying item changed after the translation was last saved — the translation may be outdated and should be reviewed.
- Use **"Hide translated items"** to focus only on items still needing translation.
- The **Go to field** dropdown (Ctrl+G) navigates directly to a specific field.

## 5.3 Translating Survey Settings

On the Forms/Surveys tab, click **Survey Settings** next to an instrument to translate the survey title, survey instructions, completion text, and other survey-level text. Use the Rich Text Editor for settings that support HTML formatting.

## 5.4 Translating ASIs (Automated Survey Invitations)

On the Forms/Surveys tab, click **ASIs** to translate the email subject, message body, and sender display name for each automated survey invitation. ASIs for each event in longitudinal projects must be translated separately. Faithfully replicate any piping expressions in translations — piping syntax must appear in the translated text exactly as in the original.

## 5.5 Translating Alerts

On the **Alerts** tab, translate the email subject, message body, and sender display name for each alert. Use the search box to quickly find a specific alert. Piping expressions must be replicated exactly in all translations.

On the **base language** tab for Alerts, configure two settings for each alert:
- **Excluded** — Check to prevent an alert from being translated (it will always fire in the base language).
- **Language Source** — Determines how REDCap identifies the language to use when triggering the alert. Choose **Language preference field** for alerts triggered by server-side processes (e.g., scheduled or condition-based alerts where no browser session exists), or **User's or survey respondent's active language** for alerts reliably triggered in the context of an active session.

## 5.6 Miscellaneous Items (Misc tab)

The Misc tab covers:
- **Missing Data Codes** — Translate the label for each missing data code defined in the project. The tab only appears if missing data codes are configured. New codes cannot be added through MLM — only existing codes can be translated.
- **PDF customizations** — Translate custom PDF header/footer text if configured.
- **Protected Email Mode customizations** — Translate custom text if Protected Email Mode is enabled.

For the base language, there is nothing to translate on the Misc tab.

## 5.7 Translating MyCap Settings

The **MyCap** tab (only shown when MyCap is active in the project) translates MyCap app settings: app title, baseline date task settings, about pages, contacts, and links. MyCap Tasks and their fields are translated via the **Forms/Surveys** tab, not the MyCap tab — task-specific items appear as fields in the instrument translation screen. Task fields that store sensor/task data (tagged with `@MC-TASK-...`) are hidden by default in the translation screen and generally do not need translation.

## 5.8 User Interface Overrides

The **User Interface** tab allows project-level overrides of UI strings (buttons, system messages) for a given language, unless the administrator has restricted this. If a language is subscribed to a system language, UI items cannot be edited and the tab displays a notice.

## 5.9 AI-Assisted Translation

When both REDCap AI Services and the "Auto-translate text on the MLM setup page" feature are enabled by an administrator, all MLM translation screens display an **Auto-translate** widget with a **Translate using AI** button.

Clicking the button sends all not-yet-translated items visible on the current page to the AI service, which fills in translations automatically. To limit the number of strings sent — and improve relevance — use the "Hide translated items" checkbox and the category tabs/filters to show only the items you want translated before clicking the button.

**Limitations to be aware of:**
- AI prompts cannot be modified — the system controls what instructions are sent to the service.
- Only the default (source) text for each item is sent; no surrounding context (field type, instrument purpose, etc.) is included.
- The AI service is instructed to translate into the language specified by the **Language Display Name**. A display name like "de" or "lang1" produces poor results — use a meaningful name such as "Deutsch" or "Español."
- AI-generated translations are a starting point, not a finished product. Always have a person sufficiently proficient in the target language review and correct any AI-generated translations before going live.
- For complex or high-volume projects, better results may be obtained by exporting the MLM JSON file and submitting it to an external AI translation service that supports structured JSON output, then importing the result.

---

# 6. How REDCap Determines the Active Language

## 6.1 The Language Determination Algorithm

The language displayed for a given page, email, or PDF depends on the context:

**Interactive (browser) sessions — surveys, data entry forms, MyCap:**
- The language stored in a browser cookie (surveys and unauthenticated users) or the user's saved setting (authenticated data entry users) is used.
- On first visit by a survey respondent, REDCap attempts to match the browser's preferred language to an active project language (if the browser-matching setting is enabled).
- The `@LANGUAGE-FORCE` action tag overrides the cookie/setting for the current page.

**Non-interactive (server-side) processes — ASIs, scheduled alerts, data import-triggered processes, PDF rendering:**
- The **Language Preference Field** value for the record is used.
- If no language preference field is set or its value is blank, REDCap falls back to the base language.

## 6.2 The Language Preference Field

Designate a language preference field on the MLM Languages tab (Settings section at the bottom of the page). The field must be a radio or dropdown type with choice codes matching active language IDs, or a plain text box field. Its value can be set by:
- Manual data entry on an intake form.
- The `@LANGUAGE-CURRENT-FORM` or `@LANGUAGE-CURRENT-SURVEY` action tag (captures the language selected during a session).
- Data import.

Like the designated email field, the language preference field's value is synchronized across all events and repeat instances — changing it in one location updates it everywhere.

## 6.3 Setting the Initially Displayed Survey Language

For survey respondents visiting for the first time, the initially displayed language can be controlled by:

1. **`@LANGUAGE-SET` on a radio field** populated with `@DEFAULT` containing the desired language ID — sets and synchronizes the language menu with the field value.
2. **The `__lang` URL parameter** (note: two underscores) appended to the survey URL — e.g., `https://redcap.server.tld/surveys/?s=ABCD1234&__lang=es`. This overrides both the cookie and the language preference field. The `@LANGUAGE-FORCE` action tag takes precedence over `__lang`.
3. **`@LANGUAGE-FORCE`** — forces a language and hides the language selector entirely.

> **Testing tip:** Always test language switching in a fresh private/incognito browser window to avoid "tainted" cookies from previous sessions affecting the displayed language.

## 6.4 Change Notifications

When a field label, survey setting, or other translatable item changes after a translation has been saved, MLM displays a **Review Changed Items** notification. Each changed item is listed with its old and new default text alongside the existing translation. Items should be reviewed and corrected as needed. If the existing translation is still valid despite the change, click **Accept** for that item (or **Accept all translations as still valid** to clear all at once).

---

# 7. Exporting and Importing Translations

## 7.1 Exporting a Language

Click the **Export** button in a language's row on the Languages tab (or the per-instrument export icon on the Forms/Surveys tab for a single instrument). Select:
- Which content types to include (UI strings, field translations, survey settings, ASIs, alerts, missing data codes, PDFs, Protected Email, MyCap).
- Whether to include **translation prompts** (default text) and **default values** — include these for offline translation by a professional translator; omit them for backup or transfer purposes.
- File format: JSON or CSV (CSV supports comma, semicolon, or tab delimiters).

Exports reflect the **saved** state only — unsaved changes are not included.

## 7.2 Importing Translations

Click the **Update** (sync) button for a language to import translations:
- **Sync from a system language** — pulls updated UI strings from the system language subscription.
- **Import from a file** (JSON, CSV, or INI) — choose what to import (UI strings, project-specific items, or both).
- **Import options**: "Keep existing translations" (default, additive) or "Overwrite existing translations." The "Allow blank values to overwrite" option erases existing translations where the import file contains a blank value — use with caution.

## 7.3 Exporting Translated Instrument PDFs

Download a translated blank instrument PDF directly from the Languages tab (PDF icon in the language's row, or the per-instrument PDF icon on the Forms/Surveys tab). Instruments without translations will render in the default language. On-the-fly language switching is not supported during eConsent PDF review — the language is locked to the language used on the preceding survey page.

---

# 8. MLM Action Tags

MLM provides a set of action tags that control language selection behavior during data entry and surveys. All MLM action tags are applied in the **Field Annotation** box of a field in the Online Designer.

## 8.1 Capturing the Active Language — @LANGUAGE-CURRENT-FORM / @LANGUAGE-CURRENT-SURVEY

| Tag | Scope |
|---|---|
| `@LANGUAGE-CURRENT-FORM` | Data entry forms only |
| `@LANGUAGE-CURRENT-SURVEY` | Survey pages only |

**Use case:** Record which language was active when a form or survey was completed.

**Field types:** Text box (no validation) or radio/dropdown field whose choice codes match active language IDs.

**Behavior:** Automatically updates the field's value to the currently active language whenever the form or survey page loads or the language changes. Has no effect on survey response review pages.

**Note:** For multi-page surveys, `@LANGUAGE-CURRENT-SURVEY` must be placed on a field on each page where language capture is needed.

## 8.2 Setting the Language from a Field — @LANGUAGE-SET / @LANGUAGE-SET-FORM / @LANGUAGE-SET-SURVEY

| Tag | Scope |
|---|---|
| `@LANGUAGE-SET` | Both forms and surveys |
| `@LANGUAGE-SET-FORM` | Data entry forms only |
| `@LANGUAGE-SET-SURVEY` | Survey pages only |

**Use case:** Allow the language selector to be controlled by a radio or dropdown field in real-time — selecting a choice in the field simultaneously switches the displayed language.

**Field types:** Radio or dropdown only. Choice codes must match active language IDs.

**Behavior:** Bidirectional — selecting a language from the selector updates the field value; selecting a choice in the field switches the displayed language. Combine with a matching `@LANGUAGE-CURRENT-X` tag to also capture and store the chosen language.

## 8.3 Forcing a Language — @LANGUAGE-FORCE / @LANGUAGE-FORCE-FORM / @LANGUAGE-FORCE-SURVEY

| Tag | Scope |
|---|---|
| `@LANGUAGE-FORCE` | Both forms and surveys |
| `@LANGUAGE-FORCE-FORM` | Data entry forms only |
| `@LANGUAGE-FORCE-SURVEY` | Survey pages only |

**Use case:** Force a specific language on a form or survey page and hide the language selector so respondents cannot change it.

**Syntax:** Takes a string parameter. Piping is supported. Example: `@LANGUAGE-FORCE-SURVEY="de"` or `@LANGUAGE-FORCE-SURVEY=[lang_pref:value]` (use `:value` when piping from a radio/dropdown field).

**Field types:** Can be applied to any field on an instrument.

**Scope limitation:** On multi-page surveys, the action tag only affects the page on which it appears. Apply it to a field on each page where the forced language effect is desired.

**Common pattern:** Collect language preference on page 1 with `@LANGUAGE-SET`, then lock the language on subsequent pages with `@LANGUAGE-FORCE-SURVEY=[lang_pref:value]`.

## 8.4 Keeping the Language Menu Expanded — @LANGUAGE-MENU-STATIC

**Use case:** Prevent the language selection menu from collapsing after a language has been chosen. By default the expanded button-style menu collapses to a compact globe icon after initial selection. This tag keeps the buttons visible at all times.

**Syntax:** No parameters — place `@LANGUAGE-MENU-STATIC` in any field's annotation on the survey page where the effect is desired.

**Scope limitation:** Like `@LANGUAGE-FORCE`, this tag only affects the page on which it appears in a multi-page survey.

## 8.5 Action Tag DOs and DON'Ts

- **Do** use the scope-specific variants (`@LANGUAGE-SET-SURVEY`, `@LANGUAGE-CURRENT-SURVEY`) rather than the generic forms when the project has both data entry and survey contexts — this prevents unintended language captures on data entry forms.
- **Do** include `:value` when piping from a radio or dropdown field into `@LANGUAGE-FORCE`: `@LANGUAGE-FORCE-SURVEY=[lang_pref:value]`.
- **Do** apply `@LANGUAGE-FORCE` (and `@LANGUAGE-MENU-STATIC`) to a field on every page of a multi-page survey where the effect is required.
- **Don't** apply both `@LANGUAGE-CURRENT-FORM` and `@LANGUAGE-CURRENT-SURVEY` to the same field when the project uses separate display modes — use the mode-specific variant.
- **Don't** use `@LANGUAGE-FORCE` or `@LANGUAGE-FORCE-FORM` unless there is a specific reason to force language on data entry forms — this is rarely necessary.

---

# 9. Common Questions

**Q: What is the difference between REDCap's language files (.ini files) and MLM languages?**
REDCap language files (e.g., `English.ini`) are server-side files that control the language of REDCap's entire user interface — every page, every button, every system message — across the whole installation. They are managed by administrators and set in General Configuration or per-project settings. MLM is a separate, project-level feature that translates a subset of REDCap's data entry and survey UI strings (approximately 570 strings) plus all project-specific content (field labels, alerts, survey settings, etc.), and allows individual respondents to choose their preferred language in real-time. You can have a REDCap instance running in English (via the `.ini` file) while an individual project offers English and Spanish via MLM.

**Q: Does MLM auto-translate my content?**
No. REDCap's MLM feature does not translate anything automatically. All translations must be provided by the project team, either by typing them directly into the MLM translation screens or by importing a translation file prepared by a professional translator.

**Q: I added a language and turned it on, but respondents still see English. Why?**
Two separate activations are required. First, the language must be set to Active on the Languages tab. Second, the language must be toggled on for each specific instrument (for data entry mode, survey mode, or both) on the Forms/Surveys tab. If either step is missing, the language will not appear.

**Q: My project is in Production. Can I still add or edit languages?**
The MLM setup page is locked in Production. Switch the project to Draft Mode first (Project Setup → Other Functionality → Switch to Draft Mode). After making your changes, submit them for approval to move the project back to Production.

**Q: What happens if a translation is missing for a given field?**
REDCap falls through a chain: it first tries the selected language's translation, then the fallback language's translation, then the base language (data dictionary text). If none of those are available, the field is rendered in the project's configured language.ini text.

**Q: Can I use MLM with the REDCap Mobile App?**
No. MLM is not compatible with the REDCap Mobile App for offline data collection. MLM is compatible with the MyCap app — enable MyCap for each language on the Languages tab and ensure language IDs match MyCap-supported language codes.

**Q: How do I get ASIs or alerts to fire in a respondent's preferred language?**
Set up a Language Preference Field in your project (a radio or dropdown field with choice codes matching your language IDs). Configure the Language Source for each alert to "Language preference field" on the Alerts base language tab. Populate the field using `@LANGUAGE-CURRENT-SURVEY` on your intake survey or through data import.

**Q: Can a language be active but invisible to respondents?**
Yes. The Base Language is often set to active but not necessarily offered to respondents — it serves as the source text. You can also create an inactive language (e.g., as a fallback-only language) that is set as Fallback but not Active, meaning it provides translations silently without appearing in the language selector.

**Q: Does switching languages mid-survey affect stored data?**
No. Switching languages in real-time only changes the display. Data already entered is preserved regardless of language switching. The language the respondent was using at submission is captured only if you have set up a `@LANGUAGE-CURRENT-SURVEY` field.

---

# 10. Common Mistakes & Gotchas

**Forgetting to enable the language per instrument.** Adding a language to the project and marking it Active is not enough. Each language must also be toggled on for each instrument (data entry and/or survey mode) individually on the Forms/Surveys tab. Translations exist but nothing changes for the respondent — this is the most common MLM setup error.

**Editing MLM in Production without switching to Draft Mode.** The Save button on the MLM page is disabled in Production. Many users click through the page and make edits without noticing nothing is being saved. Always switch to Draft Mode before making MLM changes in a Production project.

**Two users editing MLM at the same time.** Only one user can hold the MLM editing session at a time. If a second user opens the page while another is editing, they will not be able to save changes. Coordinate edits or check that no one else has the page open.

**Testing with a cached browser cookie.** Language selection is stored in a browser cookie for survey respondents. If you test language switching in a regular browser window, your previous language choice persists and may mask display issues. Always test in a fresh private/incognito window.

**Not replicating piping in translated alert or ASI messages.** Piping expressions such as `[first_name]` or `[survey-url]` must appear in the translated message body exactly as in the original. Omitting or altering piping syntax causes the translation to display broken text or missing values.

**Forgetting `:value` when piping into @LANGUAGE-FORCE from a radio field.** When a radio or dropdown field is the source for `@LANGUAGE-FORCE`, the piping syntax must include the `:value` modifier: `@LANGUAGE-FORCE-SURVEY=[lang_pref:value]`. Without `:value`, REDCap pipes the label (e.g., "German") rather than the code (e.g., "de"), and the language ID will not match any active language.

**Language preference field not set — ASIs and alerts fire in the wrong language.** Without a designated Language Preference Field, server-side processes (ASIs, scheduled alerts) cannot determine the respondent's language and default to the base language. Set up and designate a language preference field, and ensure it is populated before any ASIs or alerts fire.

**Applying @LANGUAGE-FORCE to only the first page of a multi-page survey.** The forced language effect is limited to the page where the action tag appears. On subsequent pages without the tag, the language selector re-appears and respondents can switch languages. Apply `@LANGUAGE-FORCE-SURVEY` to a field on every page where the language should be locked.

---

# Related Articles

- RC-SURV-01 — Survey Setup *(see for enabling instruments as surveys)*
- RC-ALERT-01 — Alerts and Notifications Setup *(see for alert configuration; MLM language source is set in the base language Alerts tab)*
- RC-AT-09 — Action Tags: Calculations *(see RC-AT series for general action tag guidance)*
- RC-AT-11 — Action Tags: Mobile App *(MyCap-specific action tags)*
- RC-AI-03 — AI Translations *(AI-assisted translation integrates with MLM language IDs and display names)*
- RC-CC-20 — Control Center: Multi-Language Management *(system-level MLM configuration: enabling MLM, managing system languages, setting access restrictions)*
