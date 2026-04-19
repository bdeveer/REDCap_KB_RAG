RC-CC-20

**Control Center: Multi-Language Management**

| **Article ID** | RC-CC-20 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-MLM-01 — Multi-Language Management; RC-CC-06 — Modules & Services Configuration; RC-AI-03 — AI Translations; RC-AT-10 — Action Tags: Language |

---

**Multi-Language Management (MLM)** (**Control Center → Miscellaneous Modules → Multi-Language Management**) is where administrators define system-level languages that projects can use to translate their user interfaces. When a project adopts a system language, the translations are copied into the project and can be freely customized there.

MLM can be turned on or off system-wide. When off, surveys and data entry forms are not translated in any project, and the MLM menu is not visible to project users.

> **Note:** This page does not auto-translate text. It provides tools so that translations can be entered and managed manually (or optionally using the AI translation feature).

A PDF manual for MLM is available from the REDCap Language Library (linked from the Control Center sidebar under Administrator Resources).

---

# What MLM Does (and Doesn't Do)

| Behavior | Detail |
| --- | --- |
| **Scope** | Languages defined here are available for **UI translations only** — field labels, survey button text, validation error messages, etc. Data values are not translated. |
| **Applies to projects** | Translations are copied into a project when the project adopts the language. Changes to system languages do **not** retroactively affect existing projects. |
| **Per-project customization** | After importing a system language, project managers can freely customize translations within their project. |
| **Base language** | The language shown to a user when no language preference has been set. Only one language can be designated as the base language. |

---

# 1. Page Tabs

## 1.1 Languages Tab

The main tab where system languages are listed and managed. Each language entry shows:

| Column | Notes |
| --- | --- |
| **ID** | ISO language code (e.g., `en-US`, `es-ES`) |
| **Display Name** | Name shown in language selectors — should be written in the target language (e.g., "Deutsch" for German) |
| **%** | Approximate percentage of UI items that have been translated |
| **Active** | Whether the language is active for use in projects |
| **Visible** | Whether the language appears in language selectors |
| **Base Language** | Whether this is the fallback language |
| **Initial** | Language used to initialize new project languages |
| **RTL** | Whether this is a right-to-left language |
| **Actions** | Edit, export, delete |

**Adding a new language** can be done in three ways:
1. From an available system language (using the built-in library)
2. From a file (JSON, CSV, or INI)
3. From scratch (manual entry)

**Language ID format:** Use ISO 639-1 codes for language and ISO 3166-1 for country (e.g., `en-US` for American English, `de-DE` for German). Only letters and hyphens are allowed (optionally numbers at the end). The Language ID is case-insensitive.

**Available system language library** includes languages such as: en-US, it-IT, zh-CN, hi-IN, es-ES, ar-SA, fr-FR, bn-BD, pt-BR, ur-PK, ja-JP, pa-IN, de-DE, ko-KR, fil-PH, vi-VN, ht-HT, and uk-UA (among others).

**Language Notes:** An optional free-text field for documenting the source of translations, context, or other relevant information. Notes are exported on demand only and never imported.

**Deleting a language** removes all associated UI translations permanently. It does not affect any existing projects that had already imported that language.

---

## 1.2 User Interface Tab

This tab is where the actual translation strings are entered and managed for each language.

**What can be translated:** REDCap's stock UI elements that appear on forms and surveys, including:
- Field validation error messages
- Survey navigation buttons (Next Page, Previous Page, Submit)
- Common UI labels (Close, Cancel, Confirm, Print, etc.)
- Branching logic/calculation error messages
- Cookie policy dialog text
- Field type-specific messages (sliders, checkboxes, dropdowns, etc.)
- reCAPTCHA and Protected Email module strings

**Translation categories:** All | Common | Field Types | Data Entry | Survey | Validation | Protected Email | reCAPTCHA

**Filtering and tools:**
- **Hide translated items** — filter to show only untranslated items, making it easier to find gaps.
- **Highlight untranslated text** — enabled from the Settings tab; highlights untranslated items across the page as a visual audit tool.
- **Translate using AI** — available per category; uses the AI translation feature to auto-fill untranslated strings (requires the AI features to be enabled; see RC-AI-03).

**Subscribed system languages:** If a language is designated as a "subscribed" system language, its UI items cannot be edited directly. However, administrators can still provide **selective overrides** for individual items while leaving the rest managed by the subscription.

**Saving:** Use **Save Changes** or the keyboard shortcut **CTRL-S**. The page does not auto-save.

**Reviewing changed items:** If the original REDCap text for a UI element changes (e.g., after a REDCap upgrade), translations that may be outdated are flagged. Administrators can review flagged items and either update the translation or accept the existing translation as still valid.

---

## 1.3 Usage Tab

Provides an overview of MLM usage across all projects on the instance.

- Click a **project name link** to open that project in a new browser tab.
- Click a **PID** to navigate to that project's settings page.
- Hover over usage **counts** to see more detail; click to navigate to that project's MLM setup page.

**Status icons:**

| Icon | Meaning |
| --- | --- |
| Deactivated by user | The project user has deactivated MLM for that project |
| Enabled by admin | An administrator has enabled MLM for that project |
| Deactivated by admin | An administrator has deactivated MLM for that project |
| Debug mode on | Translation debug mode is active for that project |
| Highlight translation fallbacks | Translation fallback highlighting is enabled |

The table supports **search by project language or status icon label**. An **Export** button is available to download the usage data.

---

## 1.4 Settings Tab

System-level controls that apply to how projects can use MLM.

| Setting | Notes |
| --- | --- |
| **Disable multi-language support for all projects** | Turns off MLM system-wide immediately. **WARNING: affects all projects.** |
| **Require admin activation in projects** | When enabled, an administrator must explicitly enable MLM in each project before it can be used. Projects that already have MLM enabled are unaffected. |
| **Disable project language initialization from a file** | Prevents project managers from importing a new language from a file. |
| **Disable project language initialization from scratch** | Prevents project managers from creating a new language manually. |
| **Force subscription to system language updates** | Locks project languages to receive and stay in sync with system language updates. |
| **Disable UI overrides in subscribed system languages** | Prevents project managers from overriding individual UI strings in subscribed system languages. |
| **Debug mode** | Outputs translation status messages to the browser console (F12). Useful for diagnosing unexpected translation behavior. |

These settings can be overridden on a per-project basis within that project's own MLM settings page.

---

# 2. MyCap Integration

Languages can be marked as **active for MyCap** (the mobile companion app). This is configured separately from the forms/surveys activation — MyCap language support is **all-or-nothing** per language: a language is either fully active for MyCap or not available at all.

> **Note:** MyCap requires that the Language ID follow the ISO format list. Using a non-standard ID may result in the language not appearing in the MyCap app.

---

# 3. Exporting and Importing Languages

**Export options:**
- Optionally include translation prompts, default values, and language notes
- Formats: **JSON**, **CSV** (comma, semicolon, or tab delimited)
- Export reflects the currently saved state only — unsaved changes are not included

**Import/update options:**
- Keep existing translations (only fill in gaps)
- Overwrite existing translations
- Allow blank values to overwrite existing translations

**Export/Import General Settings:** The export/import for general settings (tab-level configuration) is separate from language export/import and uses JSON format.

# 4. Common Questions

**Q: If I disable Multi-Language Management system-wide, what happens to projects that already use it?**
If you disable MLM in the Settings tab, surveys and data entry forms will stop being translated across all projects immediately. Projects that had MLM enabled will revert to the base/default language. The translations are not deleted, but they are not active. If you re-enable MLM later, translations will be available again, but the change is disruptive to active projects.

**Q: Does Multi-Language Management translate the data that users enter?**
No. MLM only translates the user interface — field labels, button text, validation error messages, and other UI elements. The actual data values that users enter (e.g., survey responses, data entry) are not translated. MLM makes surveys accessible in multiple languages, but the data collected remains in the original format entered by users.

**Q: Can a project that imported a system language keep using it even if I delete the system language?**
Yes. Deleting a system language from the Control Center does not remove translations from projects that already imported it. Projects that have already adopted a system language will continue to use those translations. Deletion only prevents new projects from importing that language going forward.

**Q: What is the difference between "Active" and "Visible" language settings?**
"Active" means the language is available for use within projects (projects can import and use it). "Visible" means the language appears in the language selector dropdown presented to users. A language can be active but not visible (users cannot see it to select), or visible but not active (users can select it but it will not work). Typically both are enabled together.

**Q: Can I set a base language that is different from English?**
Yes. The base language is the fallback language shown to users who have not selected a language preference. Only one language can be designated as the base language at a time. Many institutions set English as the base language, but you can choose any language you have configured. Changing the base language affects the default display for all users.

# 5. Common Mistakes & Gotchas

**Disabling MLM system-wide without notifying projects that depend on it.** If you disable Multi-Language Management globally, all projects immediately lose their active translations and revert to the base language. This can disrupt surveys and forms for end users without warning. Always plan ahead and communicate changes to project managers before disabling MLM.

**Changing the base language without ensuring the new base language is fully translated.** The base language is the fallback when a user has no language preference or when a language has missing translations. If you designate a language with incomplete translations as the base, users will see blank or missing text. Always verify that your chosen base language has good translation coverage (>90%) before making it the base.

**Assuming "Force subscription to system language updates" means projects can never customize translations.** When force subscription is enabled, projects receive updates to system language strings automatically. However, administrators can still provide "selective overrides" for individual items while staying subscribed to the base language. Projects are not locked in completely — they have some flexibility even under forced subscriptions.

# 6. Related Articles

- RC-MLM-01 — Multi-Language Management
- RC-CC-06 — Modules & Services Configuration
- RC-AI-03 — AI Translations
- RC-AT-10 — Action Tags: Language
