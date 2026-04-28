RC-CC-08

**Control Center: Home Page, Templates, Project Defaults & Field Validations**

| **Article ID** | RC-CC-08 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-02 — General Configuration; RC-CC-04 — User Settings & Defaults; RC-DE-05 — Field Validations; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers four related System Configuration pages that control the appearance and default behavior of REDCap projects: **Home Page Settings**, **Project Templates**, **Default Project Settings**, and **Footer Settings**. It also covers **Field Validation Types**, which determines what validation options are available to form designers across all projects. These settings apply instance-wide and affect all users and projects on the REDCap instance.

---

# 2. Home Page Settings

<!-- PLACEHOLDER: Insert annotated screenshot of Home Page Settings section -->

The Home Page Settings control what users see on the REDCap landing page (before and after login) and on the My Projects page.

**Contact Information**
- Contact name — Displayed on the Home page as the REDCap support contact (typically a team name, not an individual)
- Contact email — The email address linked to the support contact name
- Contact URL — An optional link (e.g., a help desk landing page) displayed alongside the contact information

**Grant Information**
- Grant name — If the REDCap instance is funded by a grant, the grant name or award number can be displayed on the Home page

**Announcement Text**
- Top-of-page announcement — Text displayed at the top of the Home page and My Projects page. Used for time-sensitive communications such as upcoming maintenance windows, policy changes, or new feature announcements. Should be part of your institution's communications plan.
- Display announcement on login page — Controls whether the same announcement text is shown on the login page. When SSO-based authentication is used, the login page may not be the standard REDCap login page, making this less relevant.

**Informational Text**
- Bottom-of-page text — Persistent informational text displayed at the bottom of the Home page (not the login page). A good location for standing guidance such as links to training resources, support policies, or institutional data governance information.

---

# 3. Project Templates

<!-- PLACEHOLDER: Insert annotated screenshot of Project Templates section -->

Project Templates are pre-configured projects made available to users when they create a new project. When a user creates a project and selects a template, the template's instruments (and optionally events and user roles) are copied into the new project.

Administrators can manage which templates are available, add new templates from existing projects, enable/disable individual templates, and remove outdated ones. Each template can be toggled enabled or disabled without deleting it.

**Default templates shipped with REDCap** (as of v16.x) include:

| Template | Description |
| --- | --- |
| Base Project with eConsent | Starter project incorporating the e-Consent framework |
| Basic Demography | Single instrument for capturing basic demographic information |
| Classic Database | Six forms: demography, baseline, three monthly follow-ups, and a completion form |
| Field Embedding Example Project | Demonstrates the Field Embedding feature |
| Human Cancer Tissue Biobank | Five forms for collecting and tracking cancer tissue information |
| Longitudinal Database (1 arm) | Nine forms over eight events, starting with demography |
| Longitudinal Database (2 arms) | Nine forms across two arms (e.g., Drug A / Drug B), each with eight events |
| Multiple Surveys (classic) | Pre-screening survey + two follow-up surveys + a staff data entry form (classic mode) |
| Multiple Surveys (longitudinal) | Pre-screening + weekly survey + follow-up + staff form (longitudinal mode) |
| MyCap Example Project | Sample MyCap tasks and active tasks for mobile data collection |
| Piping Example Project | Single survey demonstrating the Piping feature |
| Project Dashboards, Smart Functions, Smart Tables & Smart Charts | Dashboard examples with fifty sample records |
| Project Tracking Database | Fifteen forms for tracking attributes and progress of studies/projects |
| Randomized Clinical Trial | Seven forms including demographics, randomization, and follow-up; example randomization model pre-configured (allocation tables not yet created) |
| Repeating Instruments | Demonstrates the Repeating Instruments feature |
| Single Survey | Single survey showcasing all field types |

> **Tip:** Templates are most effective after your instance has been in use for a while and common project patterns have emerged. Over time, the default templates can be supplemented or replaced with institution-specific ones that incorporate standard fields, user role structures, and instrument configurations common at your organization.

---

# 4. Default Project Settings

<!-- PLACEHOLDER: Insert annotated screenshot of Default Project Settings section -->

These settings determine the system-wide defaults applied to all new projects when they are created.

**Language**
The default language for text displayed within projects (e.g., button labels, error messages). English is the standard default.

**Character Encoding for Exported Files**
The character encoding used for CSV exports from projects. UTF-8 is the standard default and handles special characters and international characters correctly.

**Display Custom Logo and Institution Name**
Controls whether the institutional logo (configured in General Configuration) and institution name appear in the project header on every page. Typically enabled to maintain consistent institutional branding.

**Display the Today/Now Button**
When enabled, a "Today" button (for date fields) and a "Now" button (for datetime fields) appears on all forms and surveys by default. Project administrators can override this per field if needed.

**Enable File Version History for 'File Upload' Fields**
When enabled, REDCap tracks version history for files uploaded to File Upload fields across all projects. Users can view previous file versions from the record. This setting can also be overridden at the project level via Additional Customizations on the Project Setup page.

**Custom Survey Footer Text**
A text block (with optional link) that appears at the bottom of all survey pages across all projects by default. Two sub-fields control its behavior:

- *Link text (optional)* — If provided, a link with this text appears at the bottom of every survey page; clicking it opens the custom text in a modal popup. If left blank, the custom text is displayed inline at the bottom of the page instead.
- *Custom survey footer text* — The actual text to display. HTML is supported, so you can include styled text, links, or images.

---

# 5. Footer Settings (All Projects)

<!-- PLACEHOLDER: Insert annotated screenshot of Footer Settings section -->

Configures links and text that appear in the footer of every REDCap project page.

**Footer Links**
Up to several URL + display name pairs can be added. These links appear in the footer across all projects and are typically used for institutional resources (e.g., institutional home page, IT help desk, data governance page).

**Footer Text**
A text block displayed in the footer alongside the links. Commonly contains the institution's official name, address, and contact phone number.

---

# 6. Field Validation Types

<!-- PLACEHOLDER: Insert annotated screenshot of Field Validation Types section -->

This page lists all available field validation types that form designers can assign to text fields in the Online Designer and Data Dictionary. Administrators can enable or disable individual validation types, and can add custom validations developed for the institution.

Administrators can enable or disable any validation type. Once enabled, it appears in the **Validation** drop-down in the Online Designer's Add/Edit Field dialog. Disabled types are hidden from the Online Designer but remain fully functional in any project that already uses them — and can still be entered directly in a Data Dictionary CSV upload (they work as an "Easter Egg" option even when not shown in the UI).

**Important:** Disabling a validation type that is already in use in a project does not break it; the validation continues to function. The disable only prevents new fields from selecting it via the Online Designer.

**Standard validation types shipped with REDCap** (internal Data Dictionary names in parentheses):

| Validation label | DD name |
| --- | --- |
| Date (D-M-Y) | `date_dmy` |
| Date (M-D-Y) | `date_mdy` |
| Date (Y-M-D) | `date_ymd` |
| Datetime (D-M-Y H:M) | `datetime_dmy` |
| Datetime (M-D-Y H:M) | `datetime_mdy` |
| Datetime (Y-M-D H:M) | `datetime_ymd` |
| Datetime w/ seconds (D-M-Y H:M:S) | `datetime_seconds_dmy` |
| Datetime w/ seconds (M-D-Y H:M:S) | `datetime_seconds_mdy` |
| Datetime w/ seconds (Y-M-D H:M:S) | `datetime_seconds_ymd` |
| Time (HH:MM) | `time` |
| Time (HH:MM:SS) | `time_hh_mm_ss` |
| Time (MM:SS) | `time_mm_ss` |
| Email | `email` |
| Integer | `integer` |
| Number | `number` |
| Number (1 decimal place) | `number_1dp` |
| Number (2 decimal places) | `number_2dp` |
| Number (3 decimal places) | `number_3dp` |
| Number (4 decimal places) | `number_4dp` |
| Number (comma as decimal) | `number_comma_decimal` |
| Number (1 decimal place — comma as decimal) | `number_1dp_comma_decimal` |
| Number (2 decimal places — comma as decimal) | `number_2dp_comma_decimal` |
| Number (3 decimal places — comma as decimal) | `number_3dp_comma_decimal` |
| Number (4 decimal places — comma as decimal) | `number_4dp_comma_decimal` |
| Letters only | `alpha_only` |
| Phone (North America) | `phone` |
| Phone (Australia) | `phone_australia` |
| Phone (France) | `phone_france` |
| Phone (UK) | `phone_uk` |
| Zipcode (U.S.) | `zipcode` |
| Postal Code (Australia) | `postalcode_australia` |
| Postal Code (Canada) | `postalcode_canada` |
| Postal Code (Germany) | `postalcode_germany` |
| Postal Code (UK) | `postalcode_uk` |
| Code Postal 5 caractères (France) | `postalcode_french` |
| Social Security Number (U.S.) | `ssn` |
| MRN (7 digits) | `mrn_7d` |
| MRN (10 digits) | `mrn_10d` |
| MRN (generic) | `mrn_generic` |
| Vanderbilt MRN | `vmrn` |

**Custom Validation Types**
REDCap administrators can develop and register custom validation types for institution-specific needs. Custom validations use JavaScript-based pattern matching or range checking. Once registered here, they become available in the validation type dropdown alongside standard types.

---

# 7. Common Questions

**Q: Can I customize the text shown on the login page and home page?**
Yes. The Top-of-page announcement displays on both the Home page and optionally on the login page. Use the Bottom-of-page text field to add persistent guidance below the main content on the Home page. For login page-specific customization when SSO is in use, consult your authentication configuration.

**Q: How do users see project templates when creating a new project?**
When a user clicks "Create New Project," they are offered the option to start from a template. Available templates appear in a selection list; only enabled templates are shown. Administrators can enable, disable, or remove templates from the Project Templates page.

**Q: If I disable a validation type, will existing projects using it break?**
No. Disabling a validation type hides it from the Online Designer dropdown (preventing new fields from selecting it), but existing fields with that validation type continue to function normally. The validation rules already applied to projects remain in effect. Users can still enter validation types directly via Data Dictionary CSV upload even if disabled.

**Q: What happens when I change the default survey footer text?**
The new footer text applies to all survey pages in all projects going forward. Existing surveys created before the change already have the footer text embedded; they do not retroactively update unless the project administrator manually changes the survey footer in that specific project.

**Q: Can I use HTML in the announcement text and footer text fields?**
Yes. The announcement text, bottom-of-page text, and custom survey footer text all support HTML. You can include styled text, hyperlinks, images, and other HTML elements. Test your HTML in a development project before deploying to production.

**Q: What is the purpose of creating institution-specific project templates?**
Institution-specific templates allow you to standardize data collection across projects. By creating templates that reflect your organization's common workflows (standard instruments, user roles, event structures), you reduce redundant work and ensure consistency in project setup. Over time, as common patterns emerge in your institution, custom templates become invaluable.

---

# 8. Common Mistakes & Gotchas

**Forgetting to enable newly created templates.** When you add a new template to the system, it is created in a disabled state by default. It will not appear in the template list for users creating new projects until you explicitly enable it on the Project Templates page. Administrators sometimes add a template and wonder why users cannot see it.

**Changing instance defaults does not affect already-created projects.** If you modify the Default Project Settings (e.g., character encoding, display of the Today button), these changes apply only to new projects created after the change. Existing projects retain their original settings. To update existing projects, project administrators must change those settings individually in each project's Additional Customizations.

**Disabling validation types without warning form designers.** If you disable a validation type that is in active use at your institution, form designers may be confused when they can no longer find it in the Online Designer dropdown. Communicate with your design team before disabling validation types, and consider removing only truly obsolete types.

**HTML injection in announcement text poses security risks.** While HTML is supported in announcement and footer text, malicious HTML (scripts, forms, etc.) could compromise security. Always vet HTML content carefully and limit who can edit these fields. Never allow untrusted users to edit announcement or footer text.

**Survey footer text applies instance-wide, affecting all surveys.** Custom survey footer text is a global setting. If you change it, the new footer appears on all survey pages across all projects. Consider your institution's branding and legal requirements before making changes, as the footer may include disclaimers or compliance notices.

---

# 9. Related Articles

- RC-CC-02 — General Configuration
- RC-CC-04 — User Settings & Defaults
- RC-DE-05 — Field Validations
- RC-FD-02 — Online Designer
- RC-PROJ-01 — Project Lifecycle: Status and Settings
