RC-PROJ-04

**Project Setup: Additional Customizations**

| **Article ID** | RC-PROJ-04 |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects; requires Project Design and Setup rights |
| **Prerequisite** | RC-PROJ-01 — Project Lifecycle: Status and Settings |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PROJ-01 — Project Lifecycle: Status and Settings; RC-PROJ-02 — Project Setup Checklist; RC-DE-08 — Field Comment Log; RC-DE-12 — Data Resolution Workflow; RC-BL-01 — Branching Logic: Overview & Scope; RC-AT-01 — Action Tags: Overview; RC-ALERT-01 — Alerts & Notifications: Setup; RC-INTG-01 — Data Entry Trigger |

---

# 1. Overview

The **Additional Customizations** section of the Project Setup page contains a collection of project-level settings that control how records are displayed, how data quality annotation works, how PDFs are formatted, how missing data is handled, and how various data entry behaviors are enforced. These settings are independent of one another and can be configured in any order. Most take effect immediately upon saving; none require Draft Mode.

This article covers all settings available in that section. For settings related to project status, moving to Production, or design changes via Draft Mode, see RC-PROJ-01.

---

# 2. Custom Record Label

By default, records are identified in REDCap drop-down lists and instrument headers only by their record ID (e.g., "1", "2", "102"). The **Custom Record Label** setting lets you append additional text — including live field values — to that identifier everywhere a record name is displayed.

**How it works:** Enter a label template in the text box. Wrap any field variable name in square brackets to include that field's value for the current record. Static text can be mixed freely with variable references.

**Example:** If you enter `([last_name], [first_name])`, then record 102 whose subject is "Doe, Jane" would display as:

```
102 (Doe, Jane)
```

**Where labels appear:** The custom label is displayed in the record drop-down lists on data entry forms and in the header at the top of a form page after a record is selected. It does not replace the record ID — it appends to it.

**Constraints and notes:**
- Only field variables from the current project can be referenced.
- Piping modifiers (e.g., `:value`) are not supported in the Custom Record Label.
- If a referenced field is blank for a given record, that portion of the label will appear empty.
- In longitudinal projects, the label draws field values from the first event the variable appears in.
- The label is displayed for usability purposes only; it does not affect how data is stored, exported, or addressed via the API.

---

# 3. Secondary Unique Field

REDCap's record ID is always unique, but a project may need a second field — such as a participant ID, MRN, or email address — to also be unique across all records. The **Secondary Unique Field** setting designates any existing text field in the project as a unique constraint.

**Behavior when enabled:**
- When a user enters or imports a value for the designated field, REDCap checks in real time whether that value already exists in another record.
- If a duplicate is detected, REDCap prompts the user to enter a different value before saving.
- This check applies both to data entry via the UI and to data imports.

**Display options:** Two additional toggles control how the secondary unique field value is shown alongside record names throughout the project interface:

- **Display the value of the Secondary Unique Field next to each record name displayed?** — When enabled, the secondary field's value is appended to the record name in drop-down lists and elsewhere, similar to the Custom Record Label.
- **Display the field label of the Secondary Unique Field when displaying the value?** — When enabled, the field's label (not just the value) is also shown next to the record name for additional context.

**Notes:**
- Only one field can be designated as the Secondary Unique Field per project.
- The field must be a text field; calculated fields, notes fields, and other field types cannot be designated.
- Existing records are not retroactively validated when the setting is first enabled. Only new or edited values are checked going forward.
- The Secondary Unique Field value also appears at the top right of PDF exports (see Section 6).

---

# 4. Order Records by Another Field

By default, REDCap sorts records in drop-down lists by their record ID in ascending order. The **Order records by another field** setting allows the project to sort drop-down lists by the values of a different field instead — for example, sorting by last name or by visit date.

Select the desired field from the drop-down menu. REDCap will use that field's values to sort records wherever the record drop-down appears on data entry forms.

**Notes:**
- The sort is applied to the displayed list only; stored record IDs and data are not affected.
- Sorting is alphabetical/lexicographic. For date fields, this produces chronological order if ISO format dates are used.
- If the selected field has no value for a given record, that record will appear at the top or bottom of the list depending on how empty strings sort relative to the chosen field's values.

---

# 5. Field Comment Log and Data Resolution Workflow

REDCap provides two mutually exclusive annotation modes for tracking data questions and issues at the field level. This setting controls which mode is active for the project.

**None** — Annotation is disabled. The balloon icon does not appear next to fields on data entry forms.

**Field Comment Log** — The default mode. Users can click the balloon icon next to any field to leave a free-text comment. Comments are timestamped and attributed to the user who wrote them. All comments across the project can be viewed, searched, and downloaded from the Field Comment Log page. See RC-DE-08 for full details.

**Data Resolution Workflow** — A structured query management system suited for clinical trials and studies with formal data quality requirements. Each annotation becomes a tracked query with an open/closed status and a full audit trail. Queries can be opened, responded to, and closed by users with appropriate privileges, and are accessible from both the data entry form and the Data Quality module. See RC-DE-12 for full details.

**Additional options for Field Comments:**
- **Allow users to edit or delete Field Comments** — When enabled, users who posted a comment may edit or delete it. This option is not available for Data Resolution Workflow comments, which are always immutable once posted.

**Additional options for Data Resolution Workflow:**
- **Hide closed/verified data queries from Data Quality results** — When enabled, queries that have been closed or verified no longer appear in the Data Quality module results. This reduces visual noise for teams that have already resolved flagged issues.
- **Prevent calc/CALCTEXT fields with closed/verified queries from being fixed by DQ rule H** — Data Quality rule H automatically fixes calculated and @CALCTEXT fields with outdated values. When this option is enabled, fields that have a closed or verified query will be exempt from rule H auto-fixes, preserving the existing value even if REDCap would otherwise correct it.

> **Switching modes:** Switching between Field Comment Log and Data Resolution Workflow is possible at any point. However, existing comments or queries created under the previous mode remain in the system and may not be fully visible under the new mode. Consult your local support team before switching modes on a project that already has annotation data.

---

# 6. PDF Customizations

PDFs generated from REDCap data entry forms and surveys can be customized using four project-level options. All options apply to every instrument in the project; per-instrument overrides are not supported.

**1. Custom header text**

Text entered here appears at the top left of every PDF page. Only static text is supported — piping and variable references are not rendered. If left blank, REDCap displays "Confidential" by default.

This text is suppressed from PDFs that are emailed to, viewed by, or downloaded by survey participants.

**2. REDCap logo and website URL**

Controls what appears at the bottom right of every PDF page.

- **Display REDCap logo and website URL (default)** — Shows the standard REDCap logo and the system URL.
- **Hide REDCap logo/URL and instead display the following text** — Replaces the logo and URL with custom text. The default replacement text is "Powered by REDCap," but this can be changed to any static string.

**3. Secondary Unique Field in PDF header**

If the Secondary Unique Field is enabled and set to display (see Section 3), this option controls whether its value appears at the top right corner of every PDF page.

- **Keep it displayed** (default)
- **Hide it**

**4. Hide Record ID from PDF header**

By default, the record ID appears in the header of every PDF page. This option removes the record ID from the header entirely.

- **Keep it displayed** (default)
- **Hide it** — Useful when printing PDFs for participants where the internal record ID should not be visible.

---

# 7. Missing Data Codes

REDCap's **Missing Data Codes** feature allows users to mark a blank field with a coded reason explaining why no value was entered — for example, "Not asked," "Unknown," or "Not applicable." This provides richer information than a simple blank and supports analysis workflows that need to distinguish between different types of missingness.

## 7.1 Setup

To enable the feature, enter one or more codes and their labels in the configuration box. Each code follows the same format as a multiple-choice field choice: `code, label`. Codes may contain only letters, numbers, dots, dashes, and underscores.

**Examples:** `-999, Not asked` | `UNK, Unknown` | `NA, Not applicable` | `NASK, Not asked`

REDCap provides an optional list of standardized codes (drawn from international health data standards) that can be added with a single click. These are suggestions only — use whatever codes are appropriate for your project.

If no codes are entered, the feature remains disabled and no M icon will appear on forms.

## 7.2 Data Entry Usage

Once codes are configured, an **M** icon appears next to every field on data entry forms. Clicking the icon opens a picker showing all defined codes. Selecting a code saves it as the literal data value for the field — the same way a text value would be saved.

Missing data codes can be applied to any field type, including dates, sliders, and file upload fields.

## 7.3 Choosing Safe Codes

Because a missing code is stored as a literal field value, it must never overlap with a real, expected value in any field in the project.

**Example:** If a project has an integer field where `-999` could legitimately represent a measurement, using `-999` as a missing data code would make it impossible to distinguish the real value from the missingness indicator. Choose codes that cannot plausibly appear as real data.

## 7.4 Behavior with Branching Logic

If a field hidden by branching logic has a missing data code saved for it, REDCap will hide the field but will not delete the missing data code. The field can remain "blank" with a missing code while being invisible on the form.

## 7.5 Using Missing Codes in Logic

Because codes are stored as literal field values, they can be referenced directly in branching logic, report filters, Data Quality rules, Survey Queue conditions, and Automated Survey Invitation logic.

**Example:** To show a follow-up field only when a previous field is blank or marked with the code "NASK":

```
[field_name] = "" OR [field_name] = "NASK"
```

A special function **`isblankormissingcode()`** acts as a catch-all: it returns TRUE if a field's value is either truly blank or matches any defined missing data code for the project.

```
isblankormissingcode([age])
```

This returns TRUE if `age` is empty or if it contains any configured missing data code (such as `UNK`). It returns FALSE if the field contains any non-blank value that is not a missing data code.

## 7.6 Disabling per Field: @NOMISSING

The missing data code feature is enabled for all fields by default. To disable it on a specific field — hiding the M icon for that field and preventing missing code entry — add the `@NOMISSING` action tag to that field's action tags column. See RC-AT-01 — Action Tags: Overview.

## 7.7 Export Considerations

Missing data codes are exported as literal string values in the data export. When importing data into statistical packages (SAS, SPSS, Stata, R), the syntax file may need to be manually adjusted before loading, because the package may not recognize a string like "UNK" or "NA" as a valid value for a numeric or date field. Consider this when designing your analysis workflow. If needed, you can export data without missing codes by unchecking the corresponding option on the data export page.

---

# 8. Data History Popup

When enabled, a clock icon appears next to every field on every data collection instrument. Clicking the icon displays a chronological history of all values that field has held for that record — including the previous value, who made each change, and the timestamp of each change.

This feature is particularly useful for audit trail review and for studies that need to demonstrate a complete change history for regulatory purposes.

The Data History popup must be enabled for the File Version History feature (Section 9) to function.

---

# 9. File Version History

The **File Version History** feature applies to File Upload fields. When enabled, uploading a new file to a File Upload field does not replace the existing file — instead, the new file is saved as the latest version while all prior versions are preserved. Previous versions remain accessible via the Data History popup for that field.

This eliminates the need to delete an old file before uploading a replacement and ensures that older versions remain available for review or download.

**Important constraints:**
- The Data History popup (Section 8) must be enabled for File Version History to work.
- Previous file versions are accessible only through the Data History popup. They do not appear in other areas of the project, such as the bulk file download zip for a record or a project-wide file export.

---

# 10. Today/Now Button for Date and Time Fields

When enabled, a **Today** button appears to the right of all date fields, and a **Now** button appears to the right of all time, datetime, and datetime_seconds fields on both forms and surveys. Clicking the button automatically populates the field with the current date or time.

This setting applies project-wide. There is no per-field toggle for this button from Project Setup; to suppress the button on a specific field, use the `@HIDEBUTTON` action tag if available at your institution.

---

# 11. Prevent Branching Logic from Hiding Fields That Have Values

By default, when a field is hidden by branching logic on a data entry form, REDCap prompts the user with "Erase the value of the field?" before hiding it. On survey pages, the field is hidden and its value erased automatically without a prompt.

When this setting is **enabled**, the behavior changes: any field that currently contains a value will not be hidden by branching logic at all. Instead of asking the user whether to erase the value, the field stays visible even if its branching logic condition is no longer met. Fields with no value continue to hide normally.

**Effect:** Data already entered is preserved. Fields with values are effectively exempt from branching logic.

**Scope:** This setting affects both data entry forms and survey pages.

**When to use:** Enable this setting if your workflow requires that previously entered data never be erased by branching logic — for example, in projects where data is collected in stages and earlier entries must remain visible even if later entries would otherwise trigger the field to hide.

**Caution:** With this setting enabled, users may see fields that the branching logic was intended to hide. This can cause visual inconsistency if the logic was designed to progressively show only relevant fields. Test carefully before enabling on an active project.

---

# 12. Require a Reason When Making Changes to Existing Records

When enabled, REDCap prompts the user to enter a reason (up to 200 characters) in a text box whenever they click Save on an instrument that already has data saved for one or more fields.

The reason text is stored in the project's Logging and can be reviewed on the Logging page at any time.

**Trigger conditions:**
- The prompt appears only when there is at least one field on the instrument with a previously saved value.
- It does not appear when entering data for the first time on an instrument (i.e., when all fields are blank for that instrument and record).
- It applies to data entry via the user interface only. Data imported via the Data Import Tool or API does not trigger the reason prompt.

**Use cases:** This setting is commonly used in studies with regulatory requirements for audit trails, or in any project where a change log with explanations is required for data quality or compliance purposes.

---

# 13. Protected Email Mode

**Protected Email Mode** prevents sensitive identifying data (PHI/PII) from being sent in plain text within outgoing emails generated by REDCap — specifically, alerts, survey invitations, and survey confirmation emails.

When triggered, REDCap does not send the full email content to the recipient. Instead, it sends a surrogate email containing a link to a secure REDCap page where the recipient can read the original message. If the recipient is accessing this page for the first time on a given device (or has not accessed it within the past 30 days), REDCap sends a security code to their inbox to authenticate before the protected message is displayed. Once authenticated, the recipient can view protected emails for up to 30 days on that device without needing to re-authenticate.

**Important limitation:** Protected Email Mode does not apply to alerts that use SendGrid template emails, because those emails cannot be fully rendered within the REDCap web application.

## 13.1 Scope Setting

**All alerts, survey invitations, and survey confirmation emails** — Every outgoing email generated by the project is routed through Protected Email Mode, regardless of whether it contains piped data.

**Only those with data piped from Identifier fields** — Only emails whose body pipes data from fields that are marked as Identifier fields in the project are affected. Emails that do not pipe identifier data are sent normally.

## 13.2 Custom Branding

Two optional customizations control the appearance of the secure viewing page and surrogate email header presented to recipients:

**Custom text** — Static or HTML text displayed in the email header and on the secure viewing page. HTML may be used to include images, links, or styled text. Default text: *REDCap Secure Messaging.*

**Custom logo** — An image displayed above the custom text in the email header and on the secure viewing page.

These branding options are useful for maintaining a consistent organizational identity in participant-facing communications.

---

# 14. Data Entry Trigger

The **Data Entry Trigger (DET)** field allows a project to notify an external system every time a record is saved in REDCap. Enter a URL in this field and REDCap will send an HTTP POST request to that URL each time data is submitted via a data entry form or survey page — in real time.

The DET is an advanced integration feature intended for technical users or developers who need to connect REDCap to an external application or script. Full documentation on the POST parameters sent, trigger conditions, and implementation guidance is covered in RC-INTG-01 — Data Entry Trigger.

**Key points:**
- Only one URL can be configured per project.
- The DET fires on interactive data entry and survey submissions only. CSV imports, API imports, and Mobile App imports do not trigger it.
- The URL must be accessible from the REDCap server and capable of receiving HTTP POST requests.

---

# 15. Common Questions

**Q: Can I use a calculated field as the Custom Record Label?**

**A:** Yes — calculated fields are regular fields in REDCap and can be referenced in the custom record label using bracket notation. Note that the label displays the current stored value of the field, so if the calculated field has not yet been evaluated for a record (e.g., the record is new), the label will appear blank for that portion.

---

**Q: If I set a Secondary Unique Field and then import records via the Data Import Tool, will duplicates be rejected?**

**A:** Yes. The uniqueness check applies to data imported through the user interface Data Import Tool. Attempts to import a value that is already used by another record will be flagged. However, the API does not enforce the Secondary Unique Field constraint by default — check with your local support team or the API documentation for the current behavior.

---

**Q: Can I use missing data codes in branching logic to show a follow-up field?**

**A:** Yes. Missing data codes are stored as literal field values, so they can be referenced directly in branching logic. For example: `[field] = 'NASK'` will show a follow-up field only if the code "NASK" (Not Asked) is selected. You can also use `isblankormissingcode([field])` as a broader check that returns TRUE whether the field is empty or has any missing code applied to it.

---

**Q: Does the "Prevent branching logic from hiding fields with values" setting affect surveys?**

**A:** Yes. This setting affects both data entry forms and survey pages. On surveys, the default behavior is to auto-erase and hide any field hidden by branching logic without prompting. With this setting enabled, survey fields with saved values will also stay visible rather than being erased.

---

**Q: The Data History popup is enabled but I don't see previous versions of a file in a File Upload field. Why?**

**A:** File Version History must also be explicitly enabled under Additional Customizations (Section 9). Enabling the Data History popup alone does not activate version tracking for file uploads. Enable both settings, then upload a new file using the "Upload new version" link — older versions will then be preserved and accessible through the Data History popup.

---

**Q: Can I apply Protected Email Mode to only some alerts, not all?**

**A:** Not on a per-alert basis. The setting is project-wide and offers two levels of scope: all outgoing emails, or only those that pipe data from Identifier fields. If you need finer-grained control, consider using the "Only those with data piped from Identifier fields" option and marking only the fields whose piped values are sensitive as Identifiers.

---

**Q: Will enabling "Require a reason when making changes" affect data imported via the API?**

**A:** No. The reason prompt is triggered only when a user saves data through the REDCap data entry interface. API imports and the Data Import Tool bypass this prompt and do not require a reason to be entered.

---

# 16. Related Articles

- RC-PROJ-01 — Project Lifecycle: Status and Settings (project statuses, moving to Production, Draft Mode)
- RC-PROJ-02 — Project Setup Checklist (dependency-ordered walkthrough of full project configuration)
- RC-DE-08 — Field Comment Log (full documentation for the FCL annotation mode)
- RC-DE-12 — Data Resolution Workflow (full documentation for the DRW query management mode)
- RC-DQ-01 — Data Quality Module (data quality rules; includes the Resolve Issues tab when DRW is enabled)
- RC-AT-01 — Action Tags: Overview (action tags including @NOMISSING)
- RC-BL-01 — Branching Logic: Overview & Scope (branching logic fundamentals relevant to the field-hiding behavior setting)
- RC-ALERT-01 — Alerts & Notifications: Setup (alert configuration relevant to Protected Email Mode)
- RC-CALC-01 — Special Functions Reference (includes isblankormissingcode() function documentation)
- RC-INTG-01 — Data Entry Trigger (full documentation for the DET feature configured from this page)
