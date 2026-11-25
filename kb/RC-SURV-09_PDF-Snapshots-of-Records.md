

**PDF Snapshots of Records**

| **Article ID** | [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All project types; surveys not required for logic-triggered snapshots |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — PDF Snapshot behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md); [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md); [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md); [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) |
| **Synonyms** | how do i auto-generate a pdf of a record; create a pdf snapshot when a survey is completed; save instrument pdfs to the file repository; trigger a pdf based on logic; capture a pdf copy of completed forms; automatically store a record pdf; pdf snapshot setup; generate pdfs of records at a trigger point |

---

## 1. Overview

This article covers REDCap's **PDF Snapshots of Records** feature — a mechanism for automatically generating a PDF of one or more instruments at a defined trigger point. Snapshots can be triggered by survey completion or by custom logic, and can capture a single instrument, multiple selected instruments, or all instruments in a record. Each trigger saves its PDF to the project's File Repository (the "PDF Snapshot Archive" folder), to a file upload field in the record, or both — you choose at least one location per trigger.

PDF Snapshots are independent of the e-Consent Framework — they do not require surveys or consent processes to function. However, they are also the mechanism used to capture verification attestations in an e-Consent workflow. For e-Consent setup, see [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md).

---

## 2. Key Concepts & Definitions

**PDF Snapshot**

A REDCap-generated PDF of one or more instruments for a given record, captured at the moment a trigger condition is met. The snapshot reflects the data in the record at that point in time.

**Trigger**

The condition that causes REDCap to generate a snapshot. Two types are supported: survey completion and custom logic. These cannot be combined in a single snapshot trigger (unlike Alerts or ASIs, which support both).

**Scope**

The set of instruments included in the snapshot. Options are: a single survey response, all instruments, or a selected subset of instruments. In longitudinal projects, scope can be defined per event.

**Compact PDF**

A snapshot option, shown as **"Save as Compact PDF (includes only fields with saved data)"**, that leaves out every field without a saved value and any instrument with no data. It is on by default. It is not related to branching logic: empty fields hidden by branching are left out of all record PDFs anyway, and fields with saved data always print, even if branching would currently hide them.

**PDF Snapshot Archive**

A folder in the project's File Repository that holds the snapshot PDFs of every trigger with **Save to File Repository** ticked (and all e-Consent PDFs).

**Logic-based Trigger**

A trigger that fires when a custom logic expression is true at the time the record is saved. Uses the same logic syntax as branching logic, calculated fields, and alerts. Fires only once per record — once across all events and repeating instances.

**Survey Completion Trigger**

A trigger that fires every time a specific survey is completed. Does not support additional logic conditions.

---

## 3. Accessing PDF Snapshots

Navigate to **Project Setup → Online Designer** and click the **"PDF Snapshots"** button (in the Form Options area above the instrument list). This button is always available, whether or not the project uses surveys.

If surveys are enabled and your administrator has enabled the e-Consent Framework, the Online Designer also shows an **"e-Consent"** button. Both buttons open the same page, which has two tabs: **"e-Consent Framework"** and **"PDF Snapshots of Records"**. Select the **"PDF Snapshots of Records"** tab.

Creating and editing snapshot triggers requires the **Project Design and Setup** user right.

The main feature of this page is the **"Triggers for PDF Snapshots"** table, which displays all active snapshot triggers — including those generated automatically by the e-Consent Framework and any manually defined triggers.

> **Note:** You do not need to use the e-Consent Framework to use PDF Snapshots. The two features share this interface but operate independently.

---

## 4. The Snapshot Triggers Table

The table lists all snapshot triggers with the following columns:

| Column | Description |
|---|---|
| Active? | Toggle to enable or disable a trigger. Manual triggers only — e-Consent triggers must be deactivated from the e-Consent Framework tab. Triggers cannot be deleted; disabling is the only way to retire one. |
| Edit Settings | Pencil icon = edit settings; Double-paper icon = duplicate the trigger. Both are available only on active triggers — re-enable an inactive trigger before editing or copying it. e-Consent triggers cannot be edited here. |
| Name | Title of the manually defined snapshot. Blank for e-Consent-generated triggers. Shown in this table only, not in the File Repository. |
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

## 5. Creating a Snapshot Trigger

Click **"Add new trigger"** to open the snapshot configuration popup. The popup has four sections:

### 5.1 Name of Trigger

Enter a descriptive name for the trigger. The name appears in the triggers table only — it is **not** shown in the File Repository archive. A clear, specific name (e.g., "Attestation — Site A Verification") makes managing triggers easier; to make the PDFs themselves easy to find, put identifying text in the file-name prefix (see 5.5 Snapshot File Name).

### 5.2 Trigger Conditions

Select one of two trigger types — they cannot be combined:

**Survey Completion**

Select a survey from the dropdown under "Every time the following survey is completed." The snapshot fires each time a participant completes that survey. It also fires when a staff member opens the survey as a data entry form and uses **"Save & Mark Survey as Complete"**. It never fires when a survey is marked complete through the Data Import Tool or the API. In longitudinal projects, you can tie the trigger to one specific event or to any event.

**Logic Based**

Enter a logic expression in the box under "When the following logic becomes true (only once per record)." Clicking the box opens REDCap's Logic Editor popup — the same editor used in branching logic, alerts, and ASIs. A logic checker is included.

The logic is checked every time the record is saved — on a data entry form, on a survey, through the Data Import Tool, or through the API — until the trigger has fired for that record. It is evaluated in the event and repeating instance that was just saved. Logic is not evaluated when a project is created or a project XML file is imported, and nothing runs on a schedule: logic that uses dates (for example, `datediff([enroll_date], "today", "d") >= 30`) fires only when the record is next saved after the condition becomes true.

> **Important:** Logic-based triggers fire *once per record* — once across all events and repeating instances. In repeating contexts, only the first instance that makes the logic true gets a PDF. If you need a trigger that fires multiple times (e.g., each time a survey is completed), use the survey completion trigger type instead.

**Workaround: Combining survey completion with additional logic**

PDF Snapshot triggers cannot use both survey completion and custom logic simultaneously. If you need to check whether a survey is completed *and* apply additional conditions, use the form completion variable in your logic:

```
[instrument_name_complete] = "2"
```

Each instrument in REDCap has a `[instrument_name_complete]` variable that is set to "2" when the instrument is marked complete. Note that users can manually set this status — factor this in when using the workaround.

### 5.3 Scope of the Snapshot

Configure three items:

**Instrument Selection**

Click the pencil icon in the note box to open the instrument selector. Choose which instruments to include in the snapshot. In longitudinal projects, you can specify instruments per event. The selector is generated dynamically based on your project's current instruments and events.

**Save as a Compact PDF**

The checkbox reads **"Save as Compact PDF (includes only fields with saved data)"** and is ticked by default. When enabled, REDCap leaves out every field that has no saved value, and leaves out instruments with no data at all. The result is shorter, but unanswered questions disappear from the PDF.

This option has nothing to do with branching logic. In every record PDF, compact or not, empty fields hidden by branching are left out, and fields that have saved data always print — even if branching would currently hide them.

Untick it if the PDF needs to show everything that was asked, including questions left blank (for example, a consent or attestation document reviewed by an auditor).

**Store the Translated Version of the PDF**

Available when Multi-Language Management (MLM) is configured. When enabled, the PDF is generated in the language the participant used to fill out the instrument(s). For example, if a participant completed a form in Spanish, the snapshot PDF will be in Spanish.

### 5.4 Location

At least one save location is required.

**Save to File Repository** — An ordinary checkbox. When ticked, the PDF is saved to the File Repository under the "PDF Snapshot Archive" folder. It is pre-ticked only when the project has no file upload fields; otherwise you must tick it yourself if you want archive copies. (For e-Consent snapshots the File Repository copy is mandatory.)

**Specified field** — To save a copy directly in the record, select a **File Upload** field from the dropdown. This field can be in any instrument. In longitudinal projects, you also choose the event containing the field; the default is **"Current event"** (the event in which the trigger fired). If the field is on a repeating instrument or event, the PDF goes into the instance that triggered the snapshot.

> **Important:** Saving to a file upload field replaces any file already in that field. The previous file is lost unless File Version History is enabled for the project. Tick **Save to File Repository** as well if you need to keep every snapshot.

If managing many records, per-record file upload fields are recommended for easier access. They also enable attaching PDFs to Alerts (e.g., confirmation emails) or displaying them inline. See Section 4.5 of [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) for guidance on setting up a "Documentation" instrument to house these fields.

### 5.5 Snapshot File Name

Customize the PDF filename prefix using static text and piped values. REDCap always appends a timestamp to prevent filename conflicts.

After piping, REDCap removes spaces and every character other than letters (a–z, A–Z), digits, hyphens and underscores from the prefix — they are deleted, not converted to underscores. Accented letters disappear too (e.g. "José" becomes "Jos"). `[instrument-label]` pipes the instrument's label, not its variable name.

Examples (instrument label "Demo Attestation"):

```
pid[project-id]_form[instrument-label]_id[record-name]
→ pid1234_formDemoAttestation_id56789_2025-12-12_121534.pdf

[last_name]-[first_name]-record_[record_id]
→ Doe-John-record_56789_2025-12-12_121534.pdf
```

> **Version caveat (LTS 16.0.x, checked on 16.0.61):** On the 16.0 LTS line, File Repository copies of a snapshot get an extra random string after the timestamp (the copy saved to a file upload field does not), and snapshots always render in survey style without the project's PDF customizations. On 17.x, file names follow the pattern shown above, and the PDF follows the style of the form that triggered it and applies the project's PDF customizations. If you are on LTS 16, do not build any process that relies on exact snapshot file names — match on the prefix instead.

### 5.6 Saving the Trigger

Click **"Save"** to finalize the trigger. The trigger appears in the snapshot table and is active from that moment forward: it is checked on each subsequent save of a record. Records that already meet the logic fire the next time they are saved (or when triggered manually — see 5.7).

Editing a trigger does not re-arm records that have already fired; those records will not produce another PDF from that trigger. Creating, editing, enabling and disabling triggers is recorded in the project Logging, as is each saved snapshot PDF.

### 5.7 Triggering Snapshots Manually

On a record's data entry form, the **"Trigger PDF Snapshots"** option opens a dialog listing the project's snapshot triggers, so you can generate a snapshot for that record immediately without waiting for the next save:

- **Logic-based triggers** can be fired, or re-fired, even if the logic is currently false for the record.
- **Survey-completion triggers** can only be re-fired, and only when the record has a completed response to that survey.

---

## 6. Using PDF Snapshots for Verification Attestations

A common use of PDF Snapshots in e-Consent workflows is capturing staff attestations of identity verification. The setup follows the same steps as any other snapshot trigger, applied to a verification instrument:

1. Build a verification instrument with a user name field (using `@READONLY @USERNAME`), a date/time field, and an attestation field (checkbox or signature) — as described in [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md), Section 4.4.
2. In the PDF Snapshots tab, create a new trigger.
3. Set the trigger condition to fire when the attestation field is set (e.g., `[attestation_checkbox___1] = "1"`) or when the verification instrument is marked complete.
4. Set the scope to include the verification instrument.
5. Set the file location to the verification PDF file upload field (if configured) and tick **Save to File Repository**.

This produces a timestamped PDF of the staff member's attestation, stored alongside the e-Consent PDF. Users cannot edit or delete files in the PDF Snapshot Archive. The archive is not permanent storage, though: deleting the record removes its snapshots from the archive, and **Erase all data** deletes them. REDCap does not apply hashing or a digital signature to snapshot PDFs.

> **Institution-specific:** If you need permanent retention of snapshot PDFs, ask your REDCap administrators whether your installation has external PDF storage configured.

---

## 7. Finding Snapshot PDFs

### 7.1 File Repository

Snapshot PDFs from triggers with **Save to File Repository** ticked are stored in the File Repository under **"PDF Snapshot Archive."** Access via the left-hand Applications menu.

What you can see and do depends on your user rights:

- **Seeing the archive** requires the **File Repository** user right.
- **Downloading files**, individually or as a ZIP, requires data export rights. For PDFs triggered by a survey, you need full data export rights on that instrument.
- **Data Access Group** members see only the snapshots of records in their own DAG.
- **No one can delete archive files** from the File Repository. Files leave the archive only when the record is deleted, or when the project's data is erased (**Erase all data**, or moving to production with the option to delete all data).

The archive table includes:

| Column | Description |
|---|---|
| Name | PDF filename |
| PDF utilized e-Consent Framework | Flags any PDF that contains a completed e-Consent response — including a standalone snapshot whose scope includes an e-Consent survey |
| Record | Direct link to the record and instrument |
| Survey Completed | Which survey triggered the PDF (if survey-based) |
| File Storage Time | Timestamp of generation |
| Identifier | Participant name and DOB (populated from e-Consent settings, if applicable) |
| IP Address | IP address recorded with the e-Consent response — filled only for e-Consent surveys, and only when your administrator has turned on IP address capture. Blank for other snapshots. |
| Version | Consent version (e-Consent PDFs only) |
| Type | Whether this was an e-Consent or a standalone snapshot |
| Size | File size |

Bulk download is available — all files download as a single ZIP archive. Large projects can produce very large archives.

### 7.2 Per-Record File Upload Fields

If you configured file upload fields for your snapshots, the PDFs are accessible directly from each record. Per-record storage is recommended for high-volume projects where the archive becomes difficult to navigate.

---

## 8. Common Questions

**Q: Do I need the e-Consent Framework to use PDF Snapshots?**
**A:** No. PDF Snapshots are a standalone feature. You can use them without any e-Consent configuration — for example, to capture a staff member's attestation form, or a summary of a completed assessment. Note that snapshots never run on a schedule — a trigger is only checked when a record is saved (or triggered manually from the data entry form).

**Q: Can a PDF Snapshot trigger fire more than once per record?**
**A:** Yes, if configured as a survey completion trigger — it fires each time the survey is completed. Logic-based triggers fire only once per record (across all events and instances), on the first save at which the logic is true. You can re-fire a logic-based trigger for a single record with **"Trigger PDF Snapshots"** on the data entry form.

**Q: Can I combine survey completion and custom logic in a single trigger?**
**A:** No. Each trigger supports one condition type. To approximate combined logic, use the `[instrument_name_complete] = "2"` variable in a logic-based trigger as a workaround.

**Q: What is the difference between an e-Consent PDF and a standalone snapshot PDF?**
**A:** An e-Consent PDF is generated by the e-Consent Framework upon a participant confirming their consent. A standalone snapshot PDF is triggered by any condition you define and can include any instruments. e-Consent PDFs always contain only the single consent instrument; snapshots can include one or many instruments.

**Q: What does "Compact PDF" do exactly?**
**A:** "Save as Compact PDF (includes only fields with saved data)" leaves out every field that has no saved value, and any instrument with no data. It is on by default. It is unrelated to branching logic: empty branching-hidden fields are omitted from all record PDFs, and fields with saved data always print even if branching would hide them. The trade-off is that unanswered questions disappear, so untick it when the PDF must show everything that was asked.

**Q: Can I edit a snapshot trigger after creating it?**
**A:** Yes, using the pencil icon in the trigger table (active triggers only). Changes take effect immediately for all future triggers. Previously generated PDFs are not affected, and records that already fired the trigger are not re-armed.

**Q: Can I delete a snapshot trigger?**
**A:** No. Triggers can only be disabled with the **Active?** toggle.

**Q: Where are snapshot PDFs stored?**
**A:** In the File Repository under "PDF Snapshot Archive" if **Save to File Repository** is ticked, and/or in a per-record file upload field if one is selected. Each trigger must have at least one location.

**Q: Are snapshot settings and PDFs kept when I copy a project?**
**A:** Copy Project and the project XML export carry the trigger settings, but not the archived PDF files.

**Q: Can I duplicate a snapshot trigger?**
**A:** Yes. The double-paper icon in the trigger table duplicates the trigger, which you can then modify. Useful when setting up similar triggers for multiple DAGs or instruments.

**Q: Can a snapshot include instruments from multiple events in a longitudinal project?**
**A:** Yes. When configuring the instrument scope, the selector allows you to choose instruments per event.

**Q: What happens if the file upload field I selected for storage already contains a file?**
**A:** REDCap replaces the existing file in that field with the newly generated PDF. The old file is lost unless File Version History is enabled for the project. If you need to retain multiple PDFs per record, either tick **Save to File Repository** or set up separate file upload fields for each snapshot.

**Q: What happens to snapshots when a record is deleted?**
**A:** Deleting a record removes its snapshots from the PDF Snapshot Archive and clears its "already fired" status, so a new record with the same name can fire the triggers again. **Erase all data**, and moving to production with the option to delete all data, also delete snapshot files.

---

## 9. Common Mistakes & Gotchas

**Logic-based trigger does not fire until the record is saved.** Logic triggers are evaluated on every save of the record — data entry form, survey, Data Import Tool or API — until they fire. A record that already met the logic before the trigger was created fires on its next save, not when the trigger is created. To generate the PDF right away, use **"Trigger PDF Snapshots"** on the record's data entry form. The same applies to date-based logic: nothing runs on a schedule.

**Survey completion trigger fires for every completion — including staff test submissions.** If staff test the consent or verification survey during setup, those completions will generate PDFs. Clean up test records before going live, or expect test PDFs in the archive.

**Compact PDF (on by default) drops unanswered questions.** Compact mode leaves out every field without saved data, so blank or skipped questions do not appear in the PDF at all. If the snapshot must show what was asked — not just what was answered — untick **"Save as Compact PDF"**. Data that was saved always prints, even if branching would hide the field. Test with a real or realistic record to confirm the PDF captures what you expect.

**e-Consent triggers cannot be managed from the PDF Snapshots tab.** To deactivate or edit an e-Consent trigger, you must go to the e-Consent Framework tab. The pencil and toggle icons in the PDF Snapshots table are disabled for e-Consent rows.

**File upload field is overwritten on each trigger.** If a logic-based trigger fires and then the same condition becomes false and true again, a new PDF is generated only once (logic triggers fire once per record). For survey completion triggers, each completion overwrites the previous PDF in the file upload field — only the most recent snapshot is retained in the field (earlier files are lost unless File Version History is enabled). The File Repository retains all versions only if **Save to File Repository** is ticked for the trigger.

---

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-15 — Export Instruments PDF API](RC-API-15_Export-Instruments-PDF.md)** — programmatically export a blank or completed instrument PDF for any record or event

---


## 10. Related Articles

- [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)
- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)
