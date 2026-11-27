---
id: RC-CC-20
title: 'Control Center: Multi-Language Management'
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Control
  Center multi-language behaviour checked against source code; earlier live check
  (v17.5.6) of Settings tab labels and page tabs kept; pages not re-captured
prerequisites:
- REDCap administrator access
version: '1.4'
last_updated: 2026-11
related:
- id: RC-MLM-01
  title: Multi-Language Management
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-AI-03
  title: AI Translations
- id: RC-AT-10
  title: 'Action Tags: Language Action Tags'
tags:
- control center (admin)
synonyms:
- control center multi-language management
- define system-level languages for projects
- mlm administrator settings instance-wide
- add a new ui language for redcap projects
- manage available languages admin
- system language management for translations
- enable languages projects can adopt
- instance-wide multi-language configuration
- reset a ui translation override to the system value
---

# 1. Overview

**Multi-Language Management (MLM)** (**Control Center → Miscellaneous Modules → Multi-Language Management**) is where administrators define system-level languages that projects can import for UI translation, and where the non-project pages (such as the Enter Survey Access Code page) get their languages. This article covers the administrator view — system language management, page tabs, and instance-wide settings.

For a full explanation of what MLM is, how translations work, and the project-level workflow, see **[RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md)**.

MLM can be turned on or off system-wide. When off, surveys and data entry forms are not translated in any project, and the MLM menu is not visible to project users.

> **Note — MLM manuals.** A PDF manual for MLM is available from the REDCap Language Library (linked from the Control Center sidebar under Administrator Resources). **From 15.5.1** separate PDF manuals for administrators and for end users also ship with REDCap and can be downloaded directly, without going to the Language Library.

---

# 2. Page Tabs

## 2.1 Languages Tab

The main tab where system languages are listed and managed. Each language entry shows:

| Column | Notes |
| --- | --- |
| **ID** | ISO language code (e.g., `en-US`, `es-ES`) |
| **Display Name** | Name shown in language selectors — should be written in the target language (e.g., "Deutsch" for German) |
| **%** | Approximate percentage of UI items that have been translated |
| **Active** | Whether the language is offered on non-project MLM pages (for example, the Enter Survey Access Code page). It does not control whether projects can use it. |
| **Visible** | Whether the language is available for projects to import as one of their languages. Independent of **Active**. |
| **Base Language** | The language REDCap's interface text is written in on this instance. It must match the language set for the instance in General Configuration, and it does not need to be active. |
| **Initial** | The language shown first on non-project pages to visitors who have not yet chosen a language |
| **RTL** | Whether this is a right-to-left language |
| **Actions** | Edit, export, delete |

A typical setup for a language you want projects to use, but not offer on non-project pages, is **Visible** on and **Active** off. Turn both on if you also want it on the non-project pages.

**Adding a new language** can be done in three ways:
1. Based on a system language already defined on this instance
2. From a file (JSON, CSV, or INI)
3. From scratch (manual entry)

REDCap does not ship a built-in library of translations: the "available system languages" offered when adding a language are the ones already defined on your instance. To start from a community translation, download it from the REDCap Language Library and add it from a file.

**Language ID format:** Use ISO 639-1 codes for language and ISO 3166-1 for country (e.g., `en-US` for American English, `de-DE` for German). Only letters and hyphens are allowed (optionally numbers at the end). The Language ID is case-insensitive.

**Language Notes:** An optional free-text field for documenting the source of translations, context, or other relevant information. Notes are exported on demand only and never imported.

**Deleting a language** removes all of its UI translations from the system permanently. Projects that use that system language — especially projects subscribed to its updates — may be affected. Check the **Usage** tab for projects using the language, and export it first, before deleting.

---

## 2.2 User Interface Tab

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
- **Highlight translation fallbacks** — enabled from the Settings tab as **Highlight translation fallbacks on non-project pages**; a visual audit tool for finding untranslated items.
- **Translate using AI** — available per category; uses the AI translation feature to auto-fill untranslated strings. On the Control Center page this needs AI to be configured for non-project pages with the multi-language translation feature turned on (see [RC-AI-03 — AI Translations](RC-AI-03_AI-Translations.md)).

> **Version caveat (16.0 LTS):** On 16 LTS, Control Center AI translation depends on the system-level AI translation toggle rather than the non-project AI configuration. If **Translate using AI** does not appear on 16 LTS, check that toggle.

**Saving:** Use **Save Changes** or the keyboard shortcut **CTRL-S**. The page does not auto-save.

**Reviewing changed items:** If the original REDCap text for a UI element changes (e.g., after a REDCap upgrade), translations that may be outdated are flagged. Administrators can review flagged items and either update the translation or accept the existing translation as still valid.

---

## 2.3 Usage Tab

Provides an overview of MLM usage across projects on the instance. A **Show all projects** toggle widens the list to every project, and a **Refresh** button reloads the data.

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

The table supports **search by project language or status icon label**. An **Export** button is available to download the usage data.

---

## 2.4 Settings Tab

System-level controls that apply to how projects can use MLM.

| Setting | Notes |
| --- | --- |
| **Highlight translation fallbacks on non-project pages** | Visual audit tool for untranslated items on non-project pages. |
| **Disable multi-language support for all projects** | Turns off MLM system-wide immediately. **WARNING: affects all projects.** |
| **Require admin activation in projects** | When enabled, an administrator must explicitly enable MLM in each project before it can be used. Projects that already have MLM enabled are unaffected. |
| **Disable project language initialization from a file** | Prevents project managers from importing a new language from a file. |
| **Disable project language initialization from scratch** | Prevents project managers from creating a new language manually. |
| **Force subscription to system language updates** | Locks project languages to receive and stay in sync with system language updates. |
| **Disable UI overrides in subscribed system languages** | Prevents project designers from overriding individual UI strings in subscribed system languages. |
| **Debug mode** | Outputs translation status messages to the browser console (F12). Useful for diagnosing unexpected translation behavior. |

**Per-project exceptions:** an administrator can override some of these settings for a single project, from that project's own MLM Settings tab (the override options are shown to administrators only). The settings that can be overridden per project are file initialization, initialization from scratch, forced subscription, UI overrides in subscribed languages, and admin activation (enable or disable MLM for that project). **Disable multi-language support for all projects** and **Highlight translation fallbacks on non-project pages** cannot be overridden per project. See [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) for the project-level Settings tab.

---

# 3. In Projects: Subscriptions, Overrides and MyCap

Several MLM features that the Control Center settings influence are used on the **project-level** MLM page by project designers, not on the Control Center page. They are documented in [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md):

- **Subscribing to a system language and selective UI overrides.** A project language imported from a system language can subscribe to its updates. Project designers can still override individual UI items on the project's User Interface tab (unless you turn on **Disable UI overrides in subscribed system languages**). Each item shows whether it is inherited from the system language or a project override, and a **Use system value** button resets an override.

> **Version caveat (16.0 LTS):** The **Use system value** button and the inherited / project override labels exist in 17.3 LTS and current Standard releases, but not in 16 LTS. On 16 LTS, note the system text before overriding an item so it can be restored by hand, or upgrade to 17.3 LTS or later.

- **Translation fallback.** When a project language has no translation for an item, the project's fallback settings decide what is shown. The fallback chain and advice on translation coverage are project-level topics.
- **MyCap.** Within a project, a language can be marked as **active for MyCap** (the mobile companion app). This is separate from the forms/surveys activation and is **all-or-nothing** per language: a language is either fully active for MyCap or not available at all.

> **Note:** MyCap only supports languages whose Language ID is on its supported list: en-US, it-IT, zh-CN, hi-IN, es-ES, ar-SA, fr-FR, bn-BD, pt-BR, ur-PK, ja-JP, pa-IN, de-DE, ko-KR, fil-PH, vi-VN, ht-HT and uk-UA. A system language with a non-standard ID will not be usable in the MyCap app, so give system languages a matching ID if projects will use them with MyCap.

> **Version caveat (17.x):** REDCap 17.x adds zu-ZA, af-ZA and cs-CZ to the MyCap list (21 codes). On 16 LTS these three are not supported for MyCap; if a project needs them in MyCap, it needs 17.x.

- **Export/Import General Settings** (the JSON export of MLM configuration) is available on the project MLM page only, not in the Control Center.

---

# 4. Exporting and Importing Languages

**Export options:**
- Optionally include translation prompts, default values, and language notes
- Formats: **JSON**, **CSV** (comma, semicolon, or tab delimited)
- Export reflects the currently saved state only — unsaved changes are not included

**Import/update options:**
- Keep existing translations (only fill in gaps)
- Overwrite existing translations
- Allow blank values to overwrite existing translations

---

# 5. Common Questions

**Q: If I disable Multi-Language Management system-wide, what happens to projects that already use it?**
If you disable MLM in the Settings tab, surveys and data entry forms will stop being translated across all projects immediately. Projects that had MLM enabled will revert to the base/default language. The translations are not deleted, but they are not active. If you re-enable MLM later, translations will be available again, but the change is disruptive to active projects.

**Q: Does Multi-Language Management translate the data that users enter?**
No. MLM only translates the user interface — field labels, button text, validation error messages, and other UI elements. The actual data values that users enter (e.g., survey responses, data entry) are not translated. MLM makes surveys accessible in multiple languages, but the data collected remains in the original format entered by users.

**Q: Can a project that imported a system language keep using it even if I delete the system language?**
Projects that use a system language may be affected when you delete it, particularly projects subscribed to its updates. Deleting it also stops any project from importing it in future. Before deleting, check the **Usage** tab for projects that use the language, export the language as a backup, and tell those projects' owners.

**Q: What is the difference between "Active" and "Visible" language settings?**
They control different things and are independent. "Visible" means projects can import the language as one of their own languages. "Active" means the language is offered on non-project MLM pages, such as the Enter Survey Access Code page. A language can be visible but not active (projects can use it, but it is not offered on non-project pages), or active but not visible (offered on non-project pages, but projects cannot import it).

**Q: Can I set a base language that is different from English?**
Yes, but the base language must match the language set for the instance in General Configuration — it describes the language REDCap's interface text is actually written in on your instance. Only one language can be the base language at a time, and it does not need to be active. How projects fall back to other languages when a translation is missing is configured per project; see [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md).

---

# 6. Common Mistakes & Gotchas

**Disabling MLM system-wide without notifying projects that depend on it.** If you disable Multi-Language Management globally, all projects immediately lose their active translations and revert to the base language. This can disrupt surveys and forms for end users without warning. Always plan ahead and communicate changes to project managers before disabling MLM.

**Marking a base language that doesn't match the instance's language.** The **Base Language** flag tells MLM which language REDCap's own interface text is in. It must match the language set in General Configuration. If you change the instance's language there, move the **Base Language** flag to match — don't change one without the other.

**Turning on "Active" expecting projects to get the language.** **Active** only affects non-project pages. For projects to import a language, turn on **Visible**.

**Assuming "Force subscription to system language updates" means projects can never customize translations.** When force subscription is enabled, projects receive updates to system language strings automatically. Project designers can still override individual UI items on their project's MLM page while staying subscribed. To prevent that too, also turn on **Disable UI overrides in subscribed system languages**.

---

# 7. Related Articles

- [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)
- [RC-AI-03 — AI Translations](RC-AI-03_AI-Translations.md)
- [RC-AT-10 — Action Tags: Language Action Tags](RC-AT-10_Action-Tags-Language.md)
