---
id: RC-LOCK-01
title: Record Locking & E-Signatures
domain: Record Locking
applies_to:
- All REDCap project types
- requires Lock/Unlock Records user privilege
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-DE-02 — Basic Data Entry
- 'RC-USER-03 — User Rights: Configuring User Privileges'
version: '1.1'
last_updated: 2026-08
related:
- id: RC-DE-04
  title: Editing Data & Audit Trail
- id: RC-LOG-01
  title: Logging — Project Audit Trail
- id: RC-DE-12
  title: Data Resolution Workflow
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
tags:
- record locking
synonyms:
- how do i lock a record or instrument
- prevent further edits to a completed form
- set up e-signatures in redcap
- unlock a locked form
- who can lock and unlock records
- e-signature and locking management page
- make a finalized instrument read-only
- review and sign workflow for regulated studies
---

# 1. Overview

This article covers REDCap's record locking feature — what it does, how to configure it per instrument, how to lock and unlock records, how the optional e-signature layer works, and how to use the Locking Management page to monitor lock and e-signature status across all records.

Record locking prevents further edits to a completed form. Once an instrument is locked for a record, all fields on that form become read-only for all users until someone with Lock/Unlock privileges unlocks it. This is useful for protecting finalized data, supporting audit requirements, or enforcing a review-and-sign workflow in regulated studies. The e-signature option adds an additional attestation step where an authorized user affirms the data is correct before or after locking.

Locking is configured and managed through a dedicated application in the left-hand project menu: **Customize & Manage Locking/E-signatures**. This application has two tabs — Record Locking Customization (settings) and E-signature and Locking Management (status overview).

---

# 2. Key Concepts & Definitions

**Record Locking**

A state applied to a specific instrument within a specific record (or to all instruments in a record at once) that makes all fields on that form read-only. A locked form cannot be edited by any user, regardless of their other data entry privileges, until someone with Lock/Unlock privileges unlocks it. The lock state, locking timestamp, and locking user are displayed on the form for all users.

**Instrument-Level Locking**

Locking applied to one instrument at a time for a given record. The user navigates to the instrument, scrolls to the bottom, and locks or unlocks that specific form. This is the default locking scope.

**Record-Level Locking**

Locking all instruments in a record simultaneously with a single action. This requires an additional user privilege beyond standard Lock/Unlock rights (see Section 3.2). Record-level locks also appear in the Locking Management table.

**E-Signature**

An optional attestation step that can be enabled per instrument. When enabled, an authorized user can "sign" the form electronically, indicating they have reviewed and affirm the data. The e-signature records the user's name and timestamp. E-signature is configured independently of locking — an instrument can allow locking without the e-signature option, or both.

**Record Locking Customization Page**

The settings tab of the Locking/E-signatures application. Used to configure, per instrument, whether the Lock option is displayed, whether the E-signature option is displayed, and what custom text (if any) appears at the Lock option. Changes here are optional — the defaults make locking available on all instruments for users with appropriate rights.

**E-signature and Locking Management Page**

The status-overview tab of the Locking/E-signatures application. Displays a table of all existing records with their current locked and e-signed status for each instrument. Supports filtering, timestamp/user display, and CSV export.

**Lock/Unlock Privileges**

A user right that controls who can see and use the Lock option on instruments, access the customization and management pages, and unlock locked forms. Without this right, users cannot lock, unlock, view the Lock option, or access the Locking/E-signatures application. The Lock option is invisible to users without this right.

---

> **Note (16.0.7):** The locking and e-signature settings configured on the **Record Locking Customization** page can now be **exported and imported via a Project XML file**, so they travel with the project rather than needing to be reconstructed by hand in a copy or a migrated instance.

---

# 3. User Rights for Locking

### 3.1 The Lock/Unlock Privilege

The Lock/Unlock Records privilege is controlled through standard user rights or user roles. Users without this privilege cannot see the Lock option at the bottom of any instrument, cannot access the Customize & Manage Locking/E-signatures application, and cannot lock or unlock any form.

There are two tiers of Lock/Unlock access:

| Privilege Level | What the User Can Do |
|---|---|
| Lock/Unlock Records | Lock and unlock individual instruments for a record; access the Customization and Management pages |
| Lock/Unlock Records *with record-level locking* | All of the above, plus lock or unlock all instruments in a record simultaneously |

Assign lock/unlock rights through **User Rights** or via a **User Role**. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) for how to set these.

### 3.2 Who Can See Locked Forms

Once a form is locked, the lock indicator (timestamp and locking user's name) is visible to **all users**, regardless of their Lock/Unlock privileges. The fields themselves are read-only for all users. However, only users with Lock/Unlock privileges can see the unlock control and actually remove the lock.

---

# 4. Record Locking Customization

The **Record Locking Customization** tab controls which instruments show the Lock option and whether the E-signature option appears. These settings are optional — if you make no changes, locking is available on all instruments by default.

### 4.1 Accessing the Customization Page

1. From the left-hand project menu, navigate to **Customize & Manage Locking/E-signatures** (under Applications).
2. Click the **Record Locking Customization** tab.

Only users with Lock/Unlock privileges can access this page.

### 4.2 Per-Instrument Settings

The customization table has one row per instrument with the following columns:

| Column | What It Controls |
|---|---|
| Display the Lock option for this instrument? | Checkbox — when unchecked, the Lock option is hidden for this instrument for all users, including those with Lock/Unlock rights. The instrument will also not appear in the Locking Management table. |
| Data Collection Instrument | The instrument name (read-only) |
| Also display E-signature option on instrument? | Checkbox — when unchecked, the e-signature option is hidden for this instrument. If locking is still enabled, the Locking Management table will show 'N/A' for this instrument's e-signature status. |
| Lock Record Custom Text | Optional. Text entered here replaces the default lock prompt text displayed at the bottom of the instrument. |
| Edit / Remove Custom Text | Controls to modify or clear any previously saved custom text. |

Changes are saved per row. If no custom text is entered, the following default prompt is displayed at the bottom of the instrument to users with Lock/Unlock rights:

> *Lock this record for this form? If locked, no user will be able to edit this record on this form until someone with Lock/Unlock privileges unlocks it.*

### 4.3 Custom Lock Text

Custom text replaces the default lock prompt for a specific instrument. Use this to provide study-specific instructions, regulatory language, or a more descriptive prompt for your team. Custom text can be edited or removed at any time without affecting the lock state of any existing records.

---

# 5. Locking and Unlocking Records

### 5.1 Locking an Instrument

Users with Lock/Unlock privileges lock a form directly from the data entry view:

1. Navigate to the record and open the instrument you want to lock.
2. Scroll to the bottom of the form. The Lock option appears below the save buttons (visible only to users with Lock/Unlock privileges).
3. Check the lock checkbox (or click the lock control) and save.

Once locked, the form immediately becomes read-only. All users, including those without Lock/Unlock rights, will see a banner or indicator showing the lock timestamp and the name of the user who locked it.

### 5.2 Unlocking an Instrument

Only users with Lock/Unlock privileges can unlock a form.

1. Navigate to the locked instrument.
2. The unlock control appears at the bottom of the form (visible only to users with Lock/Unlock privileges).
3. Confirm the unlock action.

After unlocking, all fields return to their normal editable state. The lock/unlock event is recorded in the project audit trail.

### 5.3 Record-Level Locking (All Instruments at Once)

Users with the additional record-level locking privilege can lock or unlock all instruments in a record simultaneously. This action is available from the Record Home Page or from within an instrument. Record-level locks appear in the Locking Management table and are noted distinctly from instrument-level locks.

---

# 6. E-Signature Workflow

When the E-signature option is enabled for an instrument (via the Customization page), an e-signature control appears at the bottom of the instrument alongside the lock option.

### 6.1 Signing a Form

1. Open the instrument for the target record.
2. Scroll to the bottom. The e-signature control appears below the lock option (visible to users with Lock/Unlock privileges).
3. Activate the e-signature. REDCap records the signing user's name and the timestamp.

### 6.2 E-Signature and Lock Interaction

E-signature and locking are independent controls, but they are typically used together. A common workflow is:

1. Data entry is completed.
2. An authorized user reviews the form, applies an e-signature to attest accuracy.
3. The same or a different authorized user then locks the form to prevent further edits.

An instrument can be locked without being e-signed, or e-signed without being locked — the combination depends on your study's workflow requirements.

### 6.3 E-Signature Display

Once a form has been e-signed, the signing user's name and timestamp are displayed on the form for all users.

### 6.4 E-Signature and Authentication Compatibility

REDCap's e-signature feature requires users to re-enter their REDCap credentials (username and password, or a 2FA PIN depending on your instance configuration) to confirm their identity at the moment of signing. This mechanism relies on locally managed REDCap credentials.

**Incompatibility with federated authentication:** E-signature is not compatible with institutions using Shibboleth (SAML) or OAuth2 as their REDCap authentication method. Because those methods delegate credential verification to an external identity provider, REDCap cannot perform the local credential re-entry that the e-signature step requires. If your institution uses Shibboleth or OAuth2 authentication, the e-signature option will not be available to your users.

If your study requires electronic attestation and your institution uses federated authentication, contact your REDCap administrator to discuss alternative approaches or consult the applicable regulatory guidance for your study type.

---

# 7. E-Signature and Locking Management Page

The **E-signature and Locking Management** tab provides a project-wide view of lock and e-signature status across all records and instruments.

### 7.1 Accessing the Page

1. Navigate to **Customize & Manage Locking/E-signatures** from the left-hand project menu.
2. Click the **E-signature and Locking Management** tab.

### 7.2 The Status Table

The table displays one row per record-instrument combination (or per record-event-instrument combination in longitudinal projects). For repeating instruments, a Repeat Instance column is shown. Columns:

| Column | Description |
|---|---|
| Record | The record ID |
| Event Name | The event the instrument belongs to (longitudinal projects only) |
| Form Name | The instrument name |
| Repeat Instance | The repeat instance number (repeating instruments only) |
| Locked? | Whether the form is currently locked; can show the locking timestamp and user when enabled via Actions |
| E-signed? | Whether the form has been e-signed; shows 'N/A' if the e-signature option is disabled for this instrument |

Instruments on which the Lock option has been disabled (via the Customization page) do not appear in this table.

### 7.3 Filtering the Table

Use the **Actions** links above the table to filter rows:

| Action | Effect |
|---|---|
| Show All Rows | Resets all filters |
| Show timestamp / user | Adds locking and e-signature timestamp and username to each row |
| Hide timestamp / user | Hides timestamp and username (default view) |
| Show locked | Shows only rows where the form is currently locked |
| Show not locked | Shows only rows where the form is not locked |
| Show e-signed | Shows only rows where the form has been e-signed |
| Show not e-signed (excludes N/A) | Shows rows where e-signature is enabled but the form has not been signed |
| Show both locked and e-signed | Shows only rows that are both locked and e-signed |
| Show neither locked nor e-signed (excludes N/A) | Shows rows that are neither locked nor e-signed, excluding instruments with no e-signature option |
| Show locked but not e-signed (excludes N/A) | Shows rows that are locked but have not been e-signed |

### 7.4 Exporting and Viewing Records

- **Export all (CSV):** Downloads the full status table as a CSV file.
- **View record:** Opens the specific record-instrument (or record-event-instrument) combination in a new window, allowing direct review without navigating away from the management table.

---

# 8. Locking in Longitudinal Projects

In longitudinal projects, locking operates at the instrument-within-event level. Each instance of an instrument in each event can be locked or unlocked independently. The Locking Management table includes an Event Name column to distinguish between the same instrument appearing across multiple events.

For repeating instruments and repeating events, each instance has its own lock state, and the Repeat Instance column in the management table identifies which instance is locked or signed.

---

# 9. Audit Trail Behavior

Every lock, unlock, and e-signature action is recorded automatically in the project audit trail (Logging). The log entry includes:

- The action type (locked, unlocked, e-signed)
- The record ID and instrument name
- The user who performed the action
- The timestamp

See [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) for details on filtering and exporting audit log entries. See [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md) for information on the field-level audit trail.

---

# 10. Common Questions

**Q: Can a user without Lock/Unlock rights see that a form is locked?**
Yes. Once a form is locked, the lock indicator (timestamp and locking user) is visible to all users. The fields are also read-only for everyone. Only the lock/unlock controls are hidden from users without the Lock/Unlock privilege.

**Q: Does locking a form prevent survey respondents from editing their submission?**
Yes. If a form is locked, survey submissions are also read-only. The survey interface will reflect the locked state and prevent further edits even if a survey edit link would otherwise allow changes.

**Q: Can I lock a record before data collection is complete?**
Yes — locking is not tied to form completion status. However, once locked, no further edits can be made until the form is unlocked. Lock only forms where data entry is finalized unless your workflow requires otherwise.

**Q: What happens to a lock if the instrument is modified in the Online Designer?**
The lock state is not automatically cleared when an instrument is modified. The form will remain locked after a design change. This can cause confusion if new required fields are added to a locked form — the record cannot be updated until the form is unlocked.

**Q: Can I export lock and e-signature status via the API?**
There is no dedicated API endpoint for lock/e-signature status. The Locking Management CSV export is the primary method for extracting this data.

**Q: Is locking available in all project types?**
Yes. Locking is available in classic (single-event) and longitudinal projects alike. In longitudinal projects, locking is per-instrument-per-event.

---

# 11. Common Mistakes & Gotchas

**Locking before data entry is complete.** A locked form is entirely read-only until unlocked. If you lock a form prematurely and then discover missing data, you must unlock it, make the correction, and re-lock it. Each lock/unlock cycle is logged.

**Disabling locking for an instrument partway through a study.** If you uncheck "Display the Lock option for this instrument?" on the Customization page after some records have already been locked, the lock controls disappear from the instrument UI but previously locked records remain locked. The locked records will also no longer appear in the Locking Management table. Restore the setting to regain visibility and the ability to unlock those records.

**Expecting e-signature to enforce locking.** Applying an e-signature does not automatically lock the form. If your workflow requires both, users must perform both actions explicitly. Build training or SOPs around this distinction.

**Forgetting record-level locking requires a separate privilege.** Standard Lock/Unlock rights only enable instrument-level locking. If your workflow requires locking all forms in a record at once, confirm the additional record-level privilege is granted in User Rights.

**Custom lock text not saving.** Custom text must be entered and saved per instrument. After typing text, click Save for that row — navigating away without saving discards the text.

**Assuming e-signature is available on all instances.** E-signature requires locally managed REDCap credentials for the re-entry step. Institutions using Shibboleth or OAuth2 authentication cannot use e-signature. If the e-signature option is not visible despite being enabled on the Customization page, confirm your instance's authentication method with your administrator. See Section 6.4 for details.

---

# 12. Related Articles

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md)
- [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md)
- [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md)
- [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md)
