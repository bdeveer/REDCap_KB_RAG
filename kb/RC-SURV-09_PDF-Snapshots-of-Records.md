RC-SURV-09

**PDF Snapshots of Records**

| **Article ID** | RC-SURV-09 |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All project types; surveys not required for logic-triggered snapshots |
| **Prerequisite** | RC-SURV-01 — Surveys – Basics |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-08 — e-Consent Framework: Setup & Management; RC-BL-01 — Branching Logic: Overview & Scope; RC-SURV-06 — Automated Survey Invitations (ASI); RC-ALERT-01 — Alerts & Notifications: Setup |

---

# 1. Overview

This article covers REDCap's **PDF Snapshots of Records** feature — a mechanism for automatically generating a PDF of one or more instruments at a defined trigger point. Snapshots can be triggered by survey completion or by custom logic, and can capture a single instrument, multiple selected instruments, or all instruments in a record. They are stored in the project's File Repository and optionally in per-record file upload fields.

PDF Snapshots are independent of the e-Consent Framework — they do not require surveys or consent processes to function. However, they are also the mechanism used to capture verification attestations in an e-Consent workflow. For e-Consent setup, see RC-SURV-08 — e-Consent Framework: Setup & Management.

---

# 2. Key Concepts & Definitions

**PDF Snapshot**

A REDCap-generated PDF of one or more instruments for a given record, captured at the moment a trigger condition is met. The snapshot reflects the data in the record at that point in time.

**Trigger**

The condition that causes REDCap to generate a snapshot. Two types are supported: survey completion and custom logic. These cannot be combined in a single snapshot trigger (unlike Alerts or ASIs, which support both).

**Scope**

The set of instruments included in the snapshot. Options are: a single survey response, all instruments, or a selected subset of instruments. In longitudinal projects, scope can be defined per event.

**Compact PDF**

A snapshot option that strips fields hidden by branching logic for that specific record. The result is a shorter, cleaner PDF showing only the data that was actually visible and entered. Recommended for instruments with many conditionally shown fields.

**PDF Snapshot Archive**

A folder in the project's File Repository where all generated snapshot PDFs are automatically stored.

**Logic-based Trigger**

A trigger that fires when a custom logic expression becomes true. Uses the same logic syntax as branching logic, calculated fields, and alerts. Fires once per record when the condition first evaluates to true.

**Survey Completion Trigger**

A trigger that fires every time a specific survey is completed. Does not support additional logic conditions.

---

# 3. Accessing PDF Snapshots

Navigate to **Project Setup → Online Designer → e-Consent** button, then select the **"PDF Snapshots of Records"** tab.

The main feature of this page is the **"Triggers for PDF Snapshots"** table, which displays all active snapshot triggers — including those generated automatically by the e-Consent Framework and any manually defined triggers.

> **Note:** You do not need to use the e-Consent Framework to use PDF Snapshots. The two features share this interface but operate independently.

---

# 4. The Snapshot Triggers Table

The table lists all snapshot triggers with the following columns:

| Column | Description |
|---|---|
| Active? | Toggle to enable or disable a trigger. Manual triggers only — e-Consent triggers must be deactivated from the e-Consent Framework tab. |
| Edit Settings | Pencil icon = edit settings; Double-paper icon = duplicate the trigger. e-Consent triggers cannot be edited here. |
| Name | Title of the manually defined snapshot. Blank for e-Consent-generated triggers. |
| Type of Trigger | "Logic based" or "Survey completion" |
| Save snapshot when... | The exact condition that fires the trigger |
| Scope of the Snapshot | "Single survey response," "All instruments," or "Selected instruments" |
| Location(s) to Save the Snapshot | Where the PDF is stored |
| Snapshot ID | A REDCap-assigned identifier. Cannot be modified. |

Above the table:
- **"Add new trigger"** button — creates a new manual snapshot trigger
- **Hide inactive triggers** toggle — filters the table to active triggers only
- **Search box** — find a specific trigger by name or setting

---

# 5. Creating a Snapshot Trigger

Click **"Add new trigger"** to open the snapshot configuration popup. The popup has four sections:

## 5.1 Name of Trigger

Enter a descriptive name for the trigger. This appears in the table and in the File Repository alongside generated PDFs. A clear, specific name (e.g., "Attestation — Site A Verification") makes managing triggers and finding PDFs significantly easier.

## 5.2 Trigger Conditions

Select one of two trigger types — they cannot be combined:

**Survey Completion**

Select a survey from the dropdown under "Every time the following survey is completed." The snapshot fires each time a participant completes that survey.

**Logic Based**

Enter a logic expression in the box under "When the following logic becomes true (only once per record)." Clicking the box opens REDCap's Logic Editor popup — the same editor used in branching logic, alerts, and ASIs. A logic checker is included.

> **Important:** Logic-based triggers fire *once per record*, the first time the condition evaluates to true. If you need a trigger that fires multiple times (e.g., each time a survey is completed), use the survey completion trigger type instead.

**Workaround: Combining survey completion with additional logic**

PDF Snapshot triggers cannot use both survey completion and custom logic simultaneously. If you need to check whether a survey is completed *and* apply additional conditions, use the form completion variable in your logic:

```
[instrument_name_complete] = "2"
```

Each instrument in REDCap has a `[instrument_name_complete]` variable that is set to "2" when the instrument is marked complete. Note that users can manually set this status — factor this in when using the workaround.

## 5.3 Scope of the Snapshot

Configure three items:

**Instrument Selection**

Click the pencil icon in the note box to open the instrument selector. Choose which instruments to include in the snapshot. In longitudinal projects, you can specify instruments per event. The selector is generated dynamically based on your project's current instruments and events.

**Save as a Compact PDF**

When enabled, REDCap strips fields hidden by branching logic for that record from the PDF. This produces a shorter, more readable document that reflects only the data the participant actually saw and entered. Recommended for instruments with conditional fields.

**Store the Translated Version of the PDF**

Available when Multi-Language Management (MLM) is configured. When enabled, the PDF is generated in the language the participant used to fill out the instrument(s). For example, if a participant completed a form in Spanish, the snapshot PDF will be in Spanish.

## 5.4 Location

**File Repository** — All snapshot PDFs are automatically saved to the File Repository under the "PDF Snapshot Archive" folder. This is always active and cannot be disabled.

**Specified field** — To also save a copy directly in the record, select a **File Upload** field from the dropdown. This field can be in any instrument. In longitudinal projects, you must also specify the event containing the field.

If managing many records, per-record file upload fields are recommended for easier access. They also enable attaching PDFs to Alerts (e.g., confirmation emails) or displaying them inline. See Section 4.5 of RC-SURV-08 for guidance on setting up a "Documentation" instrument to house these fields.

## 5.5 Snapshot File Name

Customize the PDF filename using static text and piped values. REDCap always appends a timestamp to prevent filename conflicts.

Examples:

```
pid[project-id]_form[instrument-label]_id[record-name]
→ pid1234_formdemo_attestation_id56789_2025-12-12_121534.pdf

[last_name]-[first_name]-record_[record_id]
→ Doe-John-record_56789_2025-12-12_121534.pdf
```

## 5.6 Saving the Trigger

Click **"Save"** to finalize the trigger. REDCap immediately begins monitoring the project for the defined conditions. The trigger will appear in the snapshot table and is active from that moment forward.

---

# 6. Using PDF Snapshots for Verification Attestations

A common use of PDF Snapshots in e-Consent workflows is capturing staff attestations of identity verification. The setup follows the same steps as any other snapshot trigger, applied to a verification instrument:

1. Build a verification instrument with a user name field (using `@READONLY @USERNAME`), a date/time field, and an attestation field (checkbox or signature) — as described in RC-SURV-08, Section 4.4.
2. In the PDF Snapshots tab, create a new trigger.
3. Set the trigger condition to fire when the attestation field is set (e.g., `[attestation_checkbox___1] = "1"`) or when the verification instrument is marked complete.
4. Set the scope to include the verification instrument.
5. Set the file location to the verification PDF file upload field (if configured) and the File Repository.

This produces a timestamped, immutable PDF of the staff member's attestation, stored alongside the e-Consent PDF.

---

# 7. Finding Snapshot PDFs

## 7.1 File Repository

All snapshot PDFs are stored in the File Repository under **"PDF Snapshot Archive."** Access via the left-hand Applications menu (requires appropriate user rights).

The archive table includes:

| Column | Description |
|---|---|
| Name | PDF filename |
| PDF utilized e-Consent Framework | Whether this PDF came from an e-Consent trigger |
| Record | Direct link to the record and instrument |
| Survey Completed | Which survey triggered the PDF (if survey-based) |
| File Storage Time | Timestamp of generation |
| Identifier | Participant name and DOB (populated from e-Consent settings, if applicable) |
| IP Address | IP of the person who triggered the snapshot, if capture is enabled by your administrator |
| Version | Consent version (e-Consent PDFs only) |
| Type | Whether this was an e-Consent or a standalone snapshot |
| Size | File size |

Bulk download is available — all files download as a single ZIP archive. Large projects can produce very large archives.

## 7.2 Per-Record File Upload Fields

If you configured file upload fields for your snapshots, the PDFs are accessible directly from each record. Per-record storage is recommended for high-volume projects where the archive becomes difficult to navigate.

---

# 8. Common Questions

**Q: Do I need the e-Consent Framework to use PDF Snapshots?**
A: No. PDF Snapshots are a standalone feature. You can use them without any e-Consent configuration — for example, to capture a staff member's attestation form, a summary of a completed assessment, or a scheduled monthly data extract.

**Q: Can a PDF Snapshot trigger fire more than once per record?**
A: Yes, if configured as a survey completion trigger — it fires each time the survey is completed. Logic-based triggers fire only once per record, the first time the logic evaluates to true.

**Q: Can I combine survey completion and custom logic in a single trigger?**
A: No. Each trigger supports one condition type. To approximate combined logic, use the `[instrument_name_complete] = "2"` variable in a logic-based trigger as a workaround.

**Q: What is the difference between an e-Consent PDF and a standalone snapshot PDF?**
A: An e-Consent PDF is generated by the e-Consent Framework upon a participant confirming their consent. A standalone snapshot PDF is triggered by any condition you define and can include any instruments. e-Consent PDFs always contain only the single consent instrument; snapshots can include one or many instruments.

**Q: What does "Compact PDF" do exactly?**
A: It removes fields that were hidden by branching logic for that specific record at the time of snapshot. This produces a document showing only the data the user actually entered, without blank rows for fields that were never shown.

**Q: Can I edit a snapshot trigger after creating it?**
A: Yes, using the pencil icon in the trigger table. Changes take effect immediately for all future triggers. Previously generated PDFs are not affected.

**Q: Where are snapshot PDFs stored?**
A: Always in the File Repository under "PDF Snapshot Archive." Optionally in a per-record file upload field if configured.

**Q: Can I duplicate a snapshot trigger?**
A: Yes. The double-paper icon in the trigger table duplicates the trigger, which you can then modify. Useful when setting up similar triggers for multiple DAGs or instruments.

**Q: Can a snapshot include instruments from multiple events in a longitudinal project?**
A: Yes. When configuring the instrument scope, the selector allows you to choose instruments per event.

**Q: What happens if the file upload field I selected for storage already contains a file?**
A: REDCap will overwrite the existing file in that field with the newly generated PDF. If you need to retain multiple PDFs per record, either use the File Repository or set up separate file upload fields for each snapshot.

---

# 9. Common Mistakes & Gotchas

**Logic-based trigger fires only once — missed if conditions were met before trigger was created.** Logic triggers evaluate from the moment they are saved and fire the first time the condition becomes true for each record. Records where the condition was already true before the trigger was created will not produce a PDF. If you need retroactive snapshots, consider duplicating the relevant records' data manually or using a report.

**Survey completion trigger fires for every completion — including staff test submissions.** If staff test the consent or verification survey during setup, those completions will generate PDFs. Clean up test records before going live, or expect test PDFs in the archive.

**Compact PDF strips hidden fields permanently — review branching logic carefully.** If branching logic hides fields containing relevant data at the moment of snapshot, that data will not appear in the compact PDF. Test with a real or realistic record to confirm the compact version captures what you expect.

**e-Consent triggers cannot be managed from the PDF Snapshots tab.** To deactivate or edit an e-Consent trigger, you must go to the e-Consent Framework tab. The pencil and toggle icons in the PDF Snapshots table are disabled for e-Consent rows.

**File upload field is overwritten on each trigger.** If a logic-based trigger fires and then the same condition becomes false and true again, a new PDF is generated only once (logic triggers fire once per record). For survey completion triggers, each completion overwrites the previous PDF in the file upload field — only the most recent snapshot is retained in the field. The File Repository retains all versions.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-15 — Export Instruments PDF API** — programmatically export a blank or completed instrument PDF for any record or event

---


# Related Articles

- RC-SURV-08 — e-Consent Framework: Setup & Management
- RC-SURV-01 — Surveys – Basics
- RC-SURV-06 — Automated Survey Invitations (ASI)
- RC-BL-01 — Branching Logic: Overview & Scope
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements
- RC-ALERT-01 — Alerts & Notifications: Setup
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types
- RC-FD-02 — Online Designer
