

**Record Locking & E-Signatures**

| **Article ID** | [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md) |
|---|---|
| **Domain** | Record Locking |
| **Applies To** | All REDCap project types; requires the Record Locking Customization and/or Lock/Unlock user rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — locking and e-signature behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md); [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md); [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) |
| **Synonyms** | how do i lock a record or instrument; prevent further edits to a completed form; set up e-signatures in redcap; unlock a locked form; who can lock and unlock records; e-signature and locking management page; make a finalized instrument read-only; review and sign workflow for regulated studies |

---

## 1. Overview

This article covers REDCap's record locking feature — what it does, how to configure it per instrument, how to lock and unlock records, how the optional e-signature layer works, and how to use the Locking Management page to monitor lock and e-signature status across all records.

Record locking prevents further edits to a completed form. Once an instrument is locked for a record, all fields on that form become read-only for all users until someone with Lock/Unlock privileges unlocks it. This is useful for protecting finalized data against further changes, supporting audit requirements, or enforcing a review-and-sign workflow in regulated studies. The e-signature option adds an attestation step on top of locking: e-signing a form also locks it, and unlocking an e-signed form removes the e-signature.

Locking is configured and managed through a dedicated application in the left-hand project menu: **Customize & Manage Locking/E-signatures**. This application has two tabs — Record Locking Customization (settings) and E-signature and Locking Management (status overview). If your administrator has switched e-signatures off for the whole REDCap instance, the application is shown as **Customize & Manage Locking** and only the locking features are available.

---

## 2. Key Concepts & Definitions

**Record Locking**

A state applied to a specific instrument within a specific record (or to all instruments in a record at once) that makes all fields on that form read-only. A locked form cannot be edited by any user, regardless of their other data entry privileges, until someone with Lock/Unlock privileges unlocks it. The lock state, locking timestamp, and locking user are displayed on the form for all users.

**Instrument-Level Locking**

Locking applied to one instrument at a time for a given record. The user navigates to the instrument, scrolls to the bottom, and locks or unlocks that specific form. This is the default locking scope.

**Record-Level Locking**

Locking all instruments in a record simultaneously with a single action. This is controlled by a separate user right, **Lock/Unlock Entire Records** (see Section 3.1). Record-level locks also appear in the Locking Management table.

**E-Signature**

An optional attestation step that can be enabled per instrument. When enabled, an authorized user can "sign" the form electronically, indicating they have reviewed and affirm the data. The e-signature records who signed and when. E-signing and locking are linked: e-signing a form locks it automatically if it is not already locked, and unlocking an e-signed form negates (removes) the e-signature, so the form must be signed again. A form therefore cannot be e-signed but unlocked. Locking does not require e-signing — an instrument can allow locking without the e-signature option.

**Record Locking Customization Page**

The settings tab of the Locking/E-signatures application. Used to configure, per instrument, whether the Lock option is displayed, whether the E-signature option is displayed, and what custom text (if any) appears at the Lock option. Changes here are optional — the defaults make locking available on all instruments for users with appropriate rights. The e-signature option is off by default for every instrument.

**E-signature and Locking Management Page**

The status-overview tab of the Locking/E-signatures application. Displays a table of all existing records with their current locked and e-signed status for each instrument. Supports filtering, timestamp/user display, and CSV export.

**Lock/Unlock Privileges**

The user rights that control locking. There are three separate rights: **Record Locking Customization** (access to the setup page), instrument-level **Lock/Unlock Records** (with an optional e-signature authority level), and **Lock/Unlock Entire Records** (record level). Users without instrument-level Lock/Unlock rights cannot lock or unlock individual instruments, and the Lock option is invisible to them. See Section 3.

---

> **Note (16.0.7):** The locking and e-signature settings configured on the **Record Locking Customization** page can now be **exported and imported via a Project XML file**, so they travel with the project rather than needing to be reconstructed by hand in a copy or a migrated instance.

---

## 3. User Rights for Locking

#### 3.1 The Lock/Unlock Privileges

Locking is controlled through standard user rights or user roles. There are three separate rights, each granted on its own:

| Right | What the User Can Do |
|---|---|
| **Record Locking Customization** | Open the **Record Locking Customization** tab and change the per-instrument locking and e-signature settings. This right does not by itself let the user lock or unlock anything. |
| **Lock/Unlock Records** (instrument level) | Three levels: **No Access**; **Locking / Unlocking** — lock and unlock individual instruments; **Locking / Unlocking with E-signature authority** — the same, plus e-sign. Only users at the e-signature authority level are shown the e-signature option on a form. |
| **Lock/Unlock Entire Records** (record level) | Lock or unlock all instruments in a record at once. This is an independent checkbox, not a higher tier of the instrument-level right. |

When you set instrument-level Lock/Unlock to **No Access** in the user rights dialog, REDCap also clears the **Lock/Unlock Entire Records** checkbox.

Assign lock/unlock rights through **User Rights** or via a **User Role**. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) for how to set these.

> **Important:** Anyone with instrument-level Lock/Unlock rights can unlock an e-signed form, and unlocking removes the e-signature. This is by design. If your study treats e-signatures as formal attestations, grant Lock/Unlock only to people who are allowed to withdraw signatures, and write this into your SOP.

#### 3.2 Who Can See Locked Forms

Once a form is locked, the lock indicator (timestamp and locking user's name) is visible to **all users**, regardless of their Lock/Unlock privileges. The fields themselves are read-only for all users. However, only users with Lock/Unlock privileges can see the unlock control and actually remove the lock.

---

## 4. Record Locking Customization

The **Record Locking Customization** tab controls which instruments show the Lock option and whether the E-signature option appears. These settings are optional — if you make no changes, locking is available on all instruments by default.

#### 4.1 Accessing the Customization Page

1. From the left-hand project menu, navigate to **Customize & Manage Locking/E-signatures** (under Applications).
2. Click the **Record Locking Customization** tab.

Only users with the **Record Locking Customization** right can access this page.

#### 4.2 Per-Instrument Settings

The customization table has one row per instrument with the following columns:

| Column | What It Controls |
|---|---|
| Display the Lock option for this instrument? | Checkbox — when unchecked, the Lock option is hidden for this instrument for all users, including those with Lock/Unlock rights. The instrument will also not appear in the Locking Management table. |
| Data Collection Instrument | The instrument name (read-only) |
| Also display E-signature option on instrument? | Checkbox, unchecked by default — when unchecked, the e-signature option is hidden for this instrument. It is greyed out unless **Display the Lock option for this instrument?** is checked. If locking is still enabled, the Locking Management table will show 'N/A' for this instrument's e-signature status. |
| Lock Record Custom Text | Optional. Text entered here replaces the default lock prompt text displayed at the bottom of the instrument. |
| Edit / Remove Custom Text | Controls to modify or clear any previously saved custom text. |

Changes are saved per row. The help text on the Customization page describes what the Lock option does:

> *Lock this record for this form? If locked, no user will be able to edit this record on this form until someone with Lock/Unlock privileges unlocks it.*

On the instrument itself, users with Lock/Unlock rights see the prompt **Lock this instrument?** at the bottom of the form, followed by any custom text you have entered.

#### 4.3 Custom Lock Text

Custom text appears with the lock prompt for a specific instrument. Use this to provide study-specific instructions, regulatory language, or a more descriptive prompt for your team — for example, a statement of what an e-signature on this instrument means (see Section 6.3). Custom text can be edited or removed at any time without affecting the lock state of any existing records.

---

## 5. Locking and Unlocking Records

#### 5.1 Locking an Instrument

Users with Lock/Unlock privileges lock a form directly from the data entry view:

1. Navigate to the record and open the instrument you want to lock.
2. Scroll to the bottom of the form. The Lock option appears below the save buttons (visible only to users with Lock/Unlock privileges).
3. Check the lock checkbox (or click the lock control) and save.

Once locked, the form immediately becomes read-only. All users, including those without Lock/Unlock rights, will see a banner or indicator showing the lock timestamp and the name of the user who locked it.

#### 5.2 Unlocking an Instrument

Only users with instrument-level Lock/Unlock rights (either level) can unlock a form.

1. Navigate to the locked instrument.
2. The unlock control appears at the bottom of the form (visible only to users with Lock/Unlock privileges).
3. Confirm the unlock action.

After unlocking, all fields return to their normal editable state. If the form was e-signed, unlocking negates the e-signature; the form must be e-signed again after it is re-locked. The unlock (and any negated e-signature) is recorded in the project audit trail.

#### 5.3 Record-Level Locking (All Instruments at Once)

Users with the **Lock/Unlock Entire Records** right can lock or unlock all instruments in a record simultaneously. This action is available from the Record Home Page or from within an instrument. Record-level locks appear in the Locking Management table and are noted distinctly from instrument-level locks.

- **Per arm.** In a project with multiple arms, a record-level lock applies to the record within one arm.
- **Overrides instrument controls.** While a record-level lock is in place, individual instruments in that record cannot be locked, unlocked or e-signed. Unlock the entire record first.
- **Optional PDF copy.** When locking an entire record, REDCap can optionally store a PDF of the record. This depends on your administrator having configured an external storage location for these PDFs.

> **Institution-specific:** Whether a PDF is stored when an entire record is locked, and where, is set by your REDCap administrators. Check with them if your study relies on that copy.

#### 5.4 What Locking Blocks — and What It Does Not

| Action | Behaviour on a locked form |
|---|---|
| Editing on the data entry form | Fields are read-only for all users |
| Data Import Tool and API record imports | Data for the locked form is refused with an error |
| Calculated fields | Calculations on the locked form are not updated |
| Survey submissions | Refused for the locked form |
| Deleting all data in an event for the record (from the Record Home Page) | Refused while any form in that event is locked |
| Deleting the whole record | **Not blocked** — a user with Delete Records rights can delete a record that contains locked or e-signed forms |

Locking protects data against editing. Do not rely on it to protect data against deletion: control deletion through the Delete Records user right and your SOP.

---

## 6. E-Signature Workflow

When the E-signature option is enabled for an instrument (via the Customization page), an e-signature control appears at the bottom of the instrument alongside the lock option.

#### 6.1 Signing a Form

1. Open the instrument for the target record.
2. Scroll to the bottom. The e-signature control appears below the lock option (visible only to users with the **Locking / Unlocking with E-signature authority** level of the Lock/Unlock right).
3. Activate the e-signature and confirm your identity when prompted (see Section 6.4). REDCap records who signed and when.

Three failed attempts to confirm your identity while e-signing log you out of REDCap.

#### 6.2 E-Signature and Lock Interaction

E-signing and locking are linked:

- **E-signing locks the form.** If the form is not already locked, e-signing it locks it at the same time.
- **Unlocking negates the e-signature.** When anyone with Lock/Unlock rights unlocks an e-signed form, the e-signature is removed. After any correction, the form must be locked and e-signed again.
- **Locking does not require e-signing.** A form can be locked without being e-signed, but it cannot be e-signed and unlocked.

A common workflow is:

1. Data entry is completed.
2. A data entry user or monitor locks the form to prevent further edits while it is reviewed (optional).
3. An authorized signer reviews the form and e-signs it to attest accuracy, which also locks it if it is not already locked.

#### 6.3 E-Signature Display and What Is Recorded

Once a form has been e-signed, a signature line is displayed on the form for all users, reading **E-signed by** *username* (*First Last*) **on** *date/time*.

REDCap stores who signed and when. It does not store a meaning for the signature (such as "reviewed", "approved" or "author"). If your study must record what a signature means, cover it in your SOP — for example, by stating the meaning in the instrument's custom lock text on the Customization page (see Section 4.3) so signers see it at the point of signing.

#### 6.4 E-Signature and Authentication Compatibility

REDCap's e-signature feature requires users to confirm their identity at the moment of signing. How they do this depends on the instance's authentication method and administrator settings:

| Authentication | How users e-sign |
|---|---|
| Table-based (REDCap-managed accounts) or LDAP | Re-enter their username and password, or the two-factor authentication 6-digit PIN if the administrator has enabled the PIN option for e-signatures |
| Single sign-on (Shibboleth, OpenID Connect, Microsoft Entra ID and similar) | Enter the two-factor authentication 6-digit PIN, **if** the administrator has enabled the option to use the 2FA PIN for e-signatures (or, for Shibboleth, has installed an e-signature add-on). Otherwise the e-signature authority level of the Lock/Unlock right is not offered |

With single sign-on, REDCap does not see the user's password, so it cannot ask for it at signing; the 2FA PIN option gives it a local way to confirm identity instead.

> **Version caveat (16.0.x LTS):** Approving a Duo push as the e-signature confirmation is available only on the 17.x release lines (checked on 17.3.31 LTS and 17.6.5 Standard). On 16.0.x LTS, two-factor users e-sign with the 6-digit PIN. If your signers rely on Duo, confirm your instance's version with your administrator and train them to use the PIN on 16.0.x.

An optional two-factor setting lets users enter the PIN only once per session: later e-signatures in the same session are saved without asking for the PIN again, and are logged as signed without a PIN. Administrators can override this setting for individual projects.

> **Institution-specific:** Which e-signature methods are available (password, 2FA PIN, Duo, once-per-session PIN entry) and whether e-signatures are enabled at all are set by your REDCap administrators. If your study requires electronic attestation and the e-signature option is not offered, contact them to discuss the options, and consult the applicable regulatory guidance for your study type.

---

## 7. E-Signature and Locking Management Page

The **E-signature and Locking Management** tab provides a project-wide view of lock and e-signature status across all records and instruments.

#### 7.1 Accessing the Page

1. Navigate to **Customize & Manage Locking/E-signatures** from the left-hand project menu.
2. Click the **E-signature and Locking Management** tab.

#### 7.2 The Status Table

The table displays one row per record-instrument combination (or per record-event-instrument combination in longitudinal projects). For repeating instruments, a Repeat Instance column is shown. Columns:

| Column | Description |
|---|---|
| Record | The record ID |
| Event Name | The event the instrument belongs to (longitudinal projects only) |
| Form Name | The instrument name |
| Repeat Instance | The repeat instance number (repeating instruments only) |
| Locked? | Whether the form is currently locked; can show the locking timestamp and user when enabled via Actions |
| E-signed? | Whether the form has been e-signed; shows 'N/A' if the e-signature option is disabled for this instrument |

Instruments on which the Lock option has been disabled (via the Customization page) do not appear in this table. Records locked as a whole (record-level locks) appear as separate rows marked **(entire record)**.

If you are assigned to a Data Access Group, the table shows only records in your group.

#### 7.3 Filtering the Table

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

#### 7.4 Exporting and Viewing Records

- **Export all (CSV):** Downloads the full status table as a CSV file.
- **View record:** Opens the specific record-instrument (or record-event-instrument) combination in a new window, allowing direct review without navigating away from the management table.

---

## 8. Locking in Longitudinal Projects

In longitudinal projects, locking operates at the instrument-within-event level. Each instance of an instrument in each event can be locked or unlocked independently. The Locking Management table includes an Event Name column to distinguish between the same instrument appearing across multiple events.

For repeating instruments and repeating events, each instance has its own lock state, and the Repeat Instance column in the management table identifies which instance is locked or signed.

---

## 9. Audit Trail Behavior

Every lock, unlock, and e-signature action is recorded automatically in the project audit trail (Logging). The log entry includes:

- The action type
- The record ID and instrument name
- The user who performed the action
- The timestamp

The action appears in Logging under these descriptions:

| Logging description | Recorded when |
|---|---|
| Lock instrument | An instrument is locked |
| Unlock instrument | An instrument is unlocked |
| Save e-signature | An instrument is e-signed |
| Negate e-signature | An e-signature is removed by unlocking the instrument |
| Lock entire record | A record-level lock is applied |
| Unlock entire record | A record-level lock is removed |
| Customize record locking | Settings on the Record Locking Customization page are changed |

To see only these events on the Logging page, use the filter **Record locking & e-signatures**.

See [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) for details on filtering and exporting audit log entries. See [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md) for information on the field-level audit trail.

---

## 10. Common Questions

**Q: Can a user without Lock/Unlock rights see that a form is locked?**
Yes. Once a form is locked, the lock indicator (timestamp and locking user) is visible to all users. The fields are also read-only for everyone. Only the lock/unlock controls are hidden from users without the Lock/Unlock privilege.

**Q: Does locking a form prevent survey respondents from editing their submission?**
Yes. If a form is locked, REDCap refuses survey submissions for it, even if a survey link or return code would otherwise allow the respondent to make changes.

**Q: Can I lock a record before data collection is complete?**
Yes — locking is not tied to form completion status. However, once locked, no further edits can be made until the form is unlocked. Lock only forms where data entry is finalized unless your workflow requires otherwise.

**Q: What happens to a lock if the instrument is modified in the Online Designer?**
The lock state is not automatically cleared when an instrument is modified. The form will remain locked after a design change. This can cause confusion if new required fields are added to a locked form — the record cannot be updated until the form is unlocked. Renaming an instrument keeps its existing locks and e-signatures. Deleting an instrument in the Online Designer deletes its lock and e-signature records along with it.

**Q: Can I export lock and e-signature status via the API?**
There is no API method that returns the current lock or e-signature status. The Locking Management CSV export is the primary method for extracting current status. For history, exporting Logging through the API filtered to record locking events returns the lock, unlock and e-signature events.

**Q: Can a locked or e-signed record still be deleted?**
Yes. Locking does not prevent a user with Delete Records rights from deleting the whole record. Restrict the Delete Records right and cover deletion in your SOP. See Section 5.4.

**Q: Is locking available in all project types?**
Yes. Locking is available in classic (single-event) and longitudinal projects alike. In longitudinal projects, locking is per-instrument-per-event.

---

## 11. Common Mistakes & Gotchas

**Locking before data entry is complete.** A locked form is entirely read-only until unlocked. If you lock a form prematurely and then discover missing data, you must unlock it, make the correction, and re-lock it. Each lock/unlock cycle is logged.

**Disabling locking for an instrument partway through a study.** If you uncheck "Display the Lock option for this instrument?" on the Customization page after some records have already been locked, the lock controls disappear from the instrument UI but previously locked records remain locked. The locked records will also no longer appear in the Locking Management table. Restore the setting to regain visibility and the ability to unlock those records.

**Unlocking to make a correction and forgetting the e-signature is gone.** E-signing locks the form, and unlocking an e-signed form negates the e-signature. After any correction, the form must be e-signed again — re-locking alone does not restore the signature. Use the Locking Management page's **Show locked but not e-signed** filter to find forms that need re-signing.

**Giving Lock/Unlock rights too widely.** Anyone with instrument-level Lock/Unlock rights can remove an e-signature by unlocking the form. Grant Lock/Unlock only to people who may withdraw signatures.

**Forgetting record-level locking requires a separate privilege.** The instrument-level Lock/Unlock right only enables instrument-level locking. If your workflow requires locking all forms in a record at once, grant **Lock/Unlock Entire Records** in User Rights. It is an independent checkbox, and setting instrument-level Lock/Unlock to No Access clears it.

**Expecting the e-signature option without the right level.** Only users at the **Locking / Unlocking with E-signature authority** level see the e-signature option. Users with plain **Locking / Unlocking** can lock and unlock but not e-sign.

**Custom lock text not saving.** Custom text must be entered and saved per instrument. After typing text, click Save for that row — navigating away without saving discards the text.

**Assuming e-signature is available on all instances.** E-signing requires REDCap to confirm the signer's identity. On single sign-on instances (Shibboleth, OpenID Connect, Entra ID and similar) this works only if the administrator has enabled the 2FA PIN option for e-signatures (or a Shibboleth e-signature add-on); otherwise the e-signature level of the Lock/Unlock right is not offered. Administrators can also switch e-signatures off for the whole instance. If the e-signature option is not visible despite being enabled on the Customization page, check the user's Lock/Unlock level first, then ask your administrator. See Section 6.4 for details.

**E-signature checkbox greyed out on the Customization page.** **Also display E-signature option on instrument?** can be ticked only when **Display the Lock option for this instrument?** is ticked for that instrument.

---

## 12. Related Articles

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md)
- [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md)
- [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md)
- [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md)
