---
id: RC-SURV-08
title: 'e-Consent Framework: Setup & Management'
domain: Surveys
applies_to:
- Projects with surveys enabled
- setting up e-Consent requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — e-Consent
  behaviour checked against source code; pages not re-captured
prerequisites:
- RC-SURV-01 — Surveys – Basics
- 'RC-SURV-02 — Survey Settings: Basic Options & Design'
version: '1.4'
last_updated: 2026-11
related:
- id: RC-SURV-09
  title: PDF Snapshots of Records
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-FD-02
  title: Online Designer
- id: RC-AT-01
  title: 'Action Tags: Overview'
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
tags:
- surveys
synonyms:
- how do i set up electronic consent in redcap
- e-consent framework setup
- collect signed consent forms online
- generate a signed consent pdf
- manage consent versions over time
- participant signature and consent workflow
- electronic informed consent configuration
- immutable consent pdf record
---

# 1. Overview

This article covers REDCap's e-Consent Framework — a feature that enables electronic consent collection by allowing a participant to review a document, sign it, and generate a PDF record of that consent that project users cannot edit or delete (see Section 7.3 for when archived PDFs are removed). It covers the conceptual model behind e-Consent, everything that must be prepared before configuration, step-by-step setup of the e-Consent Framework, and how to manage consent versions over time. PDF Snapshots, which are related but independently usable, are covered in [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

> **Note:** This article covers how to use the e-Consent feature in REDCap. It does not constitute legal guidance on compliant e-consent practice. Requirements vary widely by jurisdiction and institution. Always consult your local compliance office or Institutional Review Board (IRB) to confirm what is required.

---

# 2. Key Concepts & Definitions

**e-Consent**

REDCap's built-in feature for collecting electronic consent. A participant reviews a consent document, enters their name (and optionally a signature and date of birth), and confirms their consent. REDCap then generates a PDF capturing that event, which users cannot edit or delete in the File Repository.

**e-Consent Framework**

The administrative interface in REDCap where e-Consent settings are configured and consent versions are managed. Accessed via the Online Designer by clicking the "e-Consent" button.

**Consent Version**

A specific instance of consent content (text or PDF) assigned to an e-Consent entry. Versions can be differentiated by language, Data Access Group (DAG), or revision. REDCap tracks which version each record consented on.

**PDF Snapshot**

A REDCap-generated PDF of instrument data at a specific point in time. e-Consent always produces a snapshot. Snapshots can also be generated independently of e-Consent — see [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

**Verification / Attestation**

The process by which a study team member confirms the identity of the person providing consent. Common procedural patterns are pre-validation (before signing), post-validation (after signing), and no validation. These are workflow choices, not REDCap settings. Attestations by staff are captured separately via a PDF Snapshot of a verification instrument.

**Versioning**

The e-Consent 2.0 mechanism that allows multiple concurrent versions of a consent to exist simultaneously — differentiated by language, DAG, or revision number. Without versioning, changes to consent content must be made directly in the Online Designer and are not tracked automatically.

**Descriptive Field Placeholder**

A field of the "Descriptive" field type added to the e-Consent instrument to serve as the insertion point for versioned consent content. The e-Consent Framework injects the chosen consent version's text or PDF into this field at runtime.

**Multi-Language Management (MLM)**

REDCap's module for defining and managing multiple languages in a project. When two or more languages are defined, the e-Consent Framework can assign different consent versions per language.

**Data Access Group (DAG)**

A mechanism for segmenting records into site-specific groups. The e-Consent Framework can assign different consent versions per DAG, enabling multi-site projects to maintain site-specific consent content within a single instrument.

**File Repository**

A project-level file storage area in REDCap. e-Consent PDFs are automatically saved here in a folder called "PDF Snapshot Archive."

---

# 3. How e-Consent Works

When a participant completes an e-Consent survey, REDCap executes the following sequence:

1. The participant reviews the consent content (text or inline PDF) injected into the descriptive field placeholder.
2. The participant fills in required fields (name, and optionally date of birth and signature).
3. REDCap automatically adds a certification page as the last page of the survey, where the participant reviews a PDF of their responses and explicitly agrees to the consent. You do not build this page.
4. If the participant clicks "Previous" on the certification page, REDCap warns them and then clears any defined signature fields. If the survey hides the Previous button, there is no way back and nothing is cleared.
5. Upon confirmation, REDCap generates the consent PDF and always stores it in the File Repository, plus in a specified file upload field if one is configured. The consent version recorded is the one active at the moment the participant completes the survey.

Fields tagged `@HIDDEN` or `@HIDDEN-SURVEY` are left out of the e-Consent PDF.

**What REDCap records for each consent**

| Where | What is recorded |
|---|---|
| PDF footer (every page) | The participant's name and date of birth (if those fields are set), "Version: x" with the consent version, and the custom tag, if set |
| PDF header | The custom label, if set |
| File Repository archive entry | Identifier (name and date of birth), consent version, type (e-Consent), and the participant's IP address if your administrator has IP capture on |
| Logging | An "e-Consent Certification" entry listing the participant's email or phone (if known), language, DAG, consent version, file name and the certification statement |

**What the e-Consent protection covers**

Once a participant completes an e-Consent survey, REDCap protects the response:

- The completed response is read-only on the data entry form (unless editing is allowed — see Section 5.2).
- Data Import Tool and API imports cannot change it.
- Bulk deletion of instrument data skips it.
- Staff cannot use "mark survey as complete" on an e-Consent survey.
- The participant can never return to modify a completed e-Consent response. REDCap forces the survey's "return and modify" option off.

These protections apply only while e-Consent is active for the survey (see the warning in Section 6.3).

**Signing options**

REDCap does not perform automatic identity verification (e.g., background checks). Verification is handled procedurally through one of three approaches:

| Verification Type | Description |
|---|---|
| Pre-validation | A staff member attests they verified the participant's identity *before* the participant signs. |
| Post-validation | A staff member attests they verified the participant's identity *after* the participant has signed. |
| No validation | No manual identity check is performed. Acceptable when consent is sent to a known, curated list of recipients. |

Attestations by staff are captured separately via a PDF Snapshot triggered on a verification instrument — not through the e-Consent Framework itself. See Section 5.3 for instrument design guidance, and [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md) for snapshot configuration.

**Versioning matrix**

The number of concurrent consent versions equals the product of active DAGs (plus one default) and active languages (plus one default):

> *Example: 4 DAGs × 3 languages = 5 DAG slots (4 + default) × 4 language slots (3 + default) = 20 concurrent versions*

---

# 4. Preparation Checklist

e-Consent pulls configuration from several other areas of REDCap. Setting these up before opening the e-Consent Framework page prevents errors and missing options during setup.

## 4.1 e-Consent Instrument

Create a dedicated instrument in the Online Designer to serve as the e-Consent survey. A typical design includes the following fields:

| Field | Field Type | Notes |
|---|---|---|
| First name | Text (no validation) | Recommended. Best practice: use separate first and last name fields. |
| Last name | Text (no validation) | Recommended if using the two-field name approach. |
| Date of birth | Text (date validation) | Optional. Use only if your consent process needs it. |
| Signature | Signature field type | Optional but strongly recommended. To be cleared on back-navigation it must be marked **Required** (see Section 5.2). |
| Descriptive placeholder | Descriptive | Required for versioning. This field receives the injected consent content at runtime. |

The name and date of birth fields do not have to be on the e-Consent instrument. The e-Consent settings can use fields from any instrument (and, in longitudinal projects, any event), for example names already collected on an earlier screening form. Signature fields, by contrast, must be on the e-Consent instrument itself.

> **Important:** The descriptive field placeholder does not need any content entered in the Online Designer — it serves purely as a target for the e-Consent Framework's content injection. Without it, you cannot use versioning, DAG-specific content, or language-specific content.

Once the instrument is created, enable it as a survey. Adjust the **Survey Instructions** and **Survey Completion Text** to reflect that participants are completing a consent form, not a generic survey. For detailed survey configuration guidance, see [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md).

> **Tip:** Include a note in the Survey Instructions that there will be a second screen after the form. Without this, participants may think they are done after filling in their information and abandon the process before the confirmation step. Example:
>
> *Survey Instructions:* "Please complete the e-Consent survey below. Note: There will be a second screen after this page. Thank you!"
>
> *Survey Completion Text:* "Thank you for completing our e-Consent."

## 4.2 Languages (if applicable)

If the consent will be offered in multiple languages, define at least two languages in the **Multi-Language Management (MLM)** module before configuring e-Consent. Once two or more languages are defined, the e-Consent Framework will display a language assignment option when adding consent versions. Any active MLM language appears in that option; languages that are not active are not offered.

## 4.3 Data Access Groups (if applicable)

If the project uses DAGs (e.g., for a multi-site study), ensure DAGs are configured before setting up e-Consent. The e-Consent Framework will display a DAG assignment option when adding consent versions, allowing site-specific consent content. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) for DAG setup.

## 4.4 Verification Instrument (if using attestation)

If your protocol requires a staff member to attest to identity verification, build a separate instrument to capture that attestation. At minimum, include:

- **User name field** — to record who performed the verification. Add `@READONLY @USERNAME` action tags to auto-populate this from the logged-in user's account and prevent manual editing.
- **Date/time field** — to record when verification occurred.
- **Attestation trigger field** — a checkbox or signature field that signals the attestation is complete. This field will be used as the PDF Snapshot trigger in [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

## 4.5 File Upload Fields (optional)

By default, e-Consent PDFs are saved only to the File Repository. If you want PDFs accessible directly from individual records, create a **File Upload** field for each PDF you want to store per-record. These fields can live in any instrument — consider a dedicated "Documentation" instrument to keep them organized.

| Field description | Variable name | Field type |
|---|---|---|
| e-Consent PDF | pdf_consent | File upload |
| Verification attestation PDF | pdf_attestation | File upload |

File upload fields also enable attaching PDFs to Alerts (e.g., a confirmation email) or displaying them inline elsewhere in REDCap.

---

# 5. e-Consent Framework Setup

## 5.1 Accessing the e-Consent Framework

Navigate to **Project Setup → Online Designer**, then click the **"e-Consent"** button. This opens the e-Consent Framework page.

> **Indicator:** Once at least one e-Consent is active, the "e-Consent" button in the Online Designer gains a green checkmark, and the corresponding survey row gains a person-with-pen icon in the "Enable as Survey" column. Hovering over it shows "This survey has the e-Consent Framework enabled."

The main page has two tabs:
- **e-Consent Framework** — where e-Consents are configured and versions managed
- **PDF Snapshots of Records** — for configuring standalone PDF snapshots (covered in [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md))

## 5.2 Creating a New e-Consent Entry

Click **"Enable the e-Consent Framework for a survey"** and select the instrument to use as the e-Consent survey. REDCap will display an error if no eligible survey exists.

This opens the e-Consent settings popup, organized into four sections:

**Primary Settings**

- **First/last name fields** — Map to the name variable(s). The fields can be on any instrument (and any event in longitudinal projects). REDCap does not force you to choose one, but select at least one, or the PDF footer and the File Repository archive carry no name. Best practice is to use separate first and last name fields for easier piping elsewhere in REDCap.
- **Allow e-Consent responses to be edited by users?** — Off by default. Leave it off unless there is a specific protocol reason to allow post-submission edits by staff. Turning it on does not regenerate or alter the PDF generated at the time of consent. Even when it is on, a user can edit a completed e-Consent response only if all of the following also hold:
  - A REDCap administrator has not turned off e-Consent editing for the project. This project-level administrator setting is on by default; if it is off, the option appears disabled in the popup.
  - The user has the **Edit survey responses** right for that instrument.
  - The system allows survey responses to be edited.

  Participants can never modify a completed e-Consent response, whatever this setting says.

**Additional Settings**

- **Date of birth** — Optional. Select a date variable if your consent process requires it. Note: REDCap does not validate that the selected variable has date formatting — verify this yourself.
- **Custom tag/category for PDF footer** — Optional static text appended to the PDF footer (e.g., "Pediatric," "LAR," "Standard").
- **Custom label for PDF header** — Optional. Supports piped values (e.g., `[record_id] -- [last_name]`). Use the "Codebook" and "Smart Variables" buttons in the popup for reference.
- **Signature fields** — Define up to five fields that will be cleared if the participant clicks "Previous" on the certification page (after a warning). Click "Select another signature field" to add more (up to five total). Only fields that are on the e-Consent instrument, marked **Required**, and of type Notes, Text (no validation, or integer/number validation) or Signature can be chosen. If the survey hides the Previous button, the participant cannot go back, so nothing is cleared.

> **Version caveat (16.0.x LTS):** Enhanced signature fields exist on 17.x only. On 16.0 LTS, build signature fields with the standard Signature field type; if a protocol or template assumes enhanced signatures, confirm your instance is on 17.x before relying on it.

**Location(s) to Save the Signed Consent Snapshot**

- **File Repository** — Always active; all e-Consent PDFs are saved here automatically. Users cannot edit or delete them there (see Section 7.3 for when they are removed).
- **Specified field** — Optional. Select a file upload field to also save a copy directly in the record. In longitudinal projects, an event dropdown appears; it defaults to "Current event" (the event in which the survey is completed), so choosing a specific event is optional. The copy in the file upload field is ordinary field data — it is not protected like the File Repository copy.
- **Store the translated version of the PDF** — Always on for e-Consent; this is not a checkbox you can change. When MLM is in use, the PDF is generated in the language the participant selected (e.g., a Spanish consent produces a Spanish PDF).

**Snapshot File Name**

Customize the PDF filename using static text and piped values. In the piped prefix, spaces and any characters other than letters, digits, hyphens and underscores are removed. REDCap always appends a timestamp to prevent duplicates. Examples:

```
pid[project-id]_form[instrument-label]_id[record-name]
→ pid1234_formdemo_consent_id56789_2025-12-12_121534.pdf

[last_name]-[first_name]-record_[record_id]
→ Doe-John-record_56789_2025-12-12_121534.pdf
```

> **Version caveat (16.0.x LTS):** On 16.0 LTS, the File Repository copy's file name gets an extra random suffix after the timestamp; the copy saved to a file upload field does not. If you match archived PDFs to records by file name (for example in an audit script), allow for the suffix, or match on the archive's Record column instead.

An optional **Notes** field is available for internal documentation. It is not used anywhere in the consent workflow.

> **Institution-specific:** Local policies on e-consent file storage location, naming conventions, or required document content (such as footer or header language) vary by institution. Contact your REDCap administrator or IRB office to confirm any applicable requirements.

Click **"Save Settings"** to finalize. Click **Cancel** to discard all entries.

---

# 5a. Version Caveats Affecting Consent Integrity

Three defects affected e-Consent in ways that matter for a compliance-relevant workflow.

> **Critical — the "erase signature on Previous Page" setting did nothing (below 15.5.17 Standard).** Where **"Force signature field(s) to be erased if participant clicks Previous Page button while on the certification page?"** was enabled, the signature fields were **not** erased. The control was configured, displayed as enabled, and silently had no effect — so a participant could amend responses after signing while the signature remained in place. Fixed in 15.5.17.

> **Critical — concurrent editing could bypass the edit-prevention setting (below 16.0.28 Standard).** Where a survey had e-Consent enabled *and* the option to prevent users editing e-Consent responses, a user sitting on the data entry form **at the same time as a respondent was consenting via the survey** could edit responses the setting was meant to protect. Fixed in 16.0.28.

> **Version caveat (below 15.0.16 Standard):** An inline PDF rendered into a REDCap-generated PDF — for example a consent form attached to a Descriptive field at the end of an e-Consent survey — could display with **horizontal artefacts** where the source PDF used a particular alpha-channel type, producing a corrupted archived consent document. Fixed in 15.0.16. Related inline-PDF display issues were addressed in 15.0.29 (`.mjs` MIME type) and 16.0.36 (PDF viewer toolbar buttons disabled).

If consents were captured on any of these versions, the archived PDFs and the signature fields are worth spot-checking against what the workflow was configured to produce.

---

# 6. Adding and Managing Consent Versions

## 6.1 Adding a Version

After saving the e-Consent entry, click **"Add consent form"** in the Survey column of the e-Consent table. The popup contains:

- **Consent form version** — A required identifier for this version. Use a consistent scheme (e.g., incrementing integers: 1, 2, 3; or dates: 2025-01-15). The scheme is yours to define — pick one and stick to it. The label must be unique for the same consent, DAG and language, and that includes inactive versions — so bringing back an older text needs a new label.
- **Placement of consent form** — Select the descriptive field placeholder in the e-Consent instrument. Only valid descriptive fields are shown. The descriptive field **must not be the only field on the instrument** — if it is, the PDF on the survey certification page does not generate correctly. Put at least the signature or name fields on the same instrument.

> **Version caveat (17.3 LTS and 16.0 LTS):** The dialog note warning that the descriptive field must not be the only field on the instrument appears on recent Standard releases (from 17.4.3) but not on 17.3 LTS or 16.0 LTS. The advice still applies there: always put the name or signature fields on the same instrument as the descriptive field.

- **Display for specific DAG** — If DAGs are defined, assign this version to a specific DAG or to the default ("When record is not assigned to a DAG"). Always create a default version. Without one, a record that is not in a DAG (including new records created through a public survey link) may be shown — and certified against — another DAG's active version rather than a blank consent, so the wrong site's consent can end up in the archived PDF. A record that is in a DAG with no version of its own gets no consent content at all if there is no default.
- **Display for specific Language** — If MLM languages are defined, assign this version to a specific language or to the default ("When participant has no language selected"). Only active MLM languages are offered. Always create a default version so every participant has consent content in a known language.
- **Consent form content** — Two options:
  - *Rich Text* — Enter or paste consent text directly. Supports rich formatting, HTML import, and (if enabled) AI-generated draft text. Piping and field embedding do not work in rich-text consent content, and images in it do not appear in exported or snapshot PDFs — if the consent needs logos or diagrams in the archived PDF, use Inline PDF.
  - *Inline PDF* — Upload a pre-prepared consent PDF. It will be displayed inline within the survey. In the stored e-Consent PDF, the inline PDF is rendered as page images; if the server cannot render it, an attachment placeholder appears in its place. This option needs the **Imagick PHP extension** on the REDCap web server. If Imagick is not installed, the Inline PDF tab is hidden and only Rich Text is offered. Ask your REDCap administrator; the Control Center Configuration Check page shows whether Imagick is installed and able to render PDFs (it also needs Ghostscript and a security policy that allows reading PDFs).

> **Important:** When you click "Add new consent form," the new version goes live **immediately** — even in Production mode. It replaces any prior version for the same DAG/language combination. Verify your content carefully before submitting.

> **Note:** If the consent form is for a specific language, write or upload the content in that language. The consent text is not routed through the MLM module for translation.

## 6.2 Managing Versions

Click **"View all versions"** in the e-Consent table to see a full history of all versions for a given consent. The version table shows:

| Column | Description |
|---|---|
| Active? | Whether this version is currently active |
| Version | The version identifier you assigned |
| Time Added | Timestamp of when the version was added |
| Uploaded By | The REDCap user who added the version |
| Number of Records Consented | Count of archived e-Consent PDFs on this version |
| Data Access Group | DAG assignment (blank if default or no DAGs) |
| MLM Language | Language assignment (blank if default or no languages) |
| Consent Form Text or File | Preview of text or link to the PDF |

To deactivate a version without replacing it, click **"Set as inactive."** REDCap will ask for confirmation. To reactivate a deactivated version, you must add it as a new version with a new version label — there is no direct reactivation, and the old label cannot be reused.

## 6.3 Managing the e-Consent Table

The main e-Consent Framework table provides the following controls per row:

- **Active?** toggle — Enable or disable the entire e-Consent entry
- **Pencil icon** — Edit the e-Consent settings
- **Survey column** — Manage consent versions for that entry

> **Important:** Turning **Active?** off for a survey removes the e-Consent protections (Section 3) from responses already completed, not just from future ones — those responses become editable and importable like any other survey data (PDFs already archived stay in the File Repository). Any user with Project Design and Setup rights can do this, including in Production. The change is logged. Control who may switch e-Consent off through your SOPs, and review Logging for these changes during audits.

Above the table:
- Add another consent entry (green button)
- Toggle to hide inactive consents
- Search box for locating a specific consent

---

# 7. Finding e-Consent PDFs

## 7.1 File Repository

All e-Consent PDFs are stored in the **File Repository** under a folder named **"PDF Snapshot Archive."** Access the File Repository from the left-hand Applications menu. Access depends on user rights:

- Seeing the archive requires the **File Repository** right.
- A download link for a PDF, and its inclusion in the ZIP download, require full data export rights on the instrument concerned.
- Users in a DAG see only their own DAG's records.

The archive table includes the following columns:

| Column | Description |
|---|---|
| Name | PDF filename — a well-chosen filename during setup pays off here |
| PDF utilized e-Consent Framework | Flags any PDF that contains a completed e-Consent response |
| Record | Direct link to the record and instrument that generated the PDF |
| Survey Completed | Which survey was completed to generate the PDF |
| File Storage Time | Timestamp of PDF generation |
| Identifier | Name and date of birth from the e-Consent settings |
| IP Address | IP of the consenting party, if IP capture is on (it is on by default). The IP address is kept in this archive entry; it is not printed on the PDF or saved in the record's data |
| Version | The consent version used |
| Type | Whether this was an e-Consent or standard snapshot |
| Size | File size |

The page also supports bulk download of all files as a ZIP archive (only files you have rights to download are included). Note that large projects can produce very large ZIP files.

## 7.2 File Upload Fields

If you configured per-record file upload fields (Section 4.5), each record's PDF is accessible directly from within the record. These files can be piped, displayed inline, or downloaded in bulk via reports. The copy in a file upload field is ordinary field data: it follows that field's normal rights and can be replaced or deleted like any other uploaded file. Treat the File Repository archive as the reference copy.

## 7.3 When Archived PDFs Are Removed

Users cannot edit or delete individual PDFs in the PDF Snapshot Archive, but the archive is not permanent in every case:

- **Deleting a record** removes that record's PDFs from the archive.
- **Erase all data** and **moving to Production with the option to delete all data** delete the archived PDFs as well.
- If your administrator has configured an **external storage server** for e-Consent, every e-Consent PDF is also copied there. That external copy survives record deletion.

Before deleting records or erasing data in a project that holds signed consents, export the PDFs you must retain, and check with your administrator whether an external copy exists.

> **Institution-specific:** Whether an external storage copy of e-Consent PDFs is configured, and your retention requirements for signed consents, vary by institution. Check with your REDCap administrators and IRB office.

---

# 8. Common Questions

**Q: Does REDCap automatically verify the identity of the person signing the consent?**
**A:** No. REDCap does not perform automated identity verification (such as background checks or account-based identity confirmation). Verification is a procedural step performed by a staff member, captured through a separate attestation instrument and PDF Snapshot.

**Q: Can I use e-Consent without the versioning system?**
**A:** Yes. If you do not add a descriptive field placeholder, you can still configure an e-Consent — but consent content must be managed directly in the Online Designer, REDCap will not track versions automatically, and you cannot assign different content by DAG or language.

**Q: What happens if a record is not assigned to a DAG and I have no default consent version?**
**A:** Always create a version assigned to the default DAG option ("When record is not assigned to a DAG"). Without one, a record that is not in a DAG — including a new record created through a public survey link — may be shown, and certified against, another DAG's active version rather than a blank consent. A record that is in a DAG with no version of its own gets no consent content if there is no default.

**Q: Can I edit a submitted consent response?**
**A:** By default, no. Staff can edit a completed e-Consent response only if **"Allow e-Consent responses to be edited by users?"** is turned on in Primary Settings, the administrator's project-level setting allows it (on by default), the user has the Edit survey responses right, and the system allows survey responses to be edited. Participants can never modify a completed e-Consent response. Editing does not regenerate or alter the PDF already generated at the time of original consent.

**Q: How many concurrent consent versions can I have?**
**A:** The maximum is (number of DAGs + 1) × (number of languages + 1). The +1 accounts for the default slot in each dimension. Example: 4 DAGs and 3 languages = 5 × 4 = 20 concurrent versions.

**Q: When does a new consent version go live?**
**A:** Immediately upon clicking "Add new consent form" — including in Production mode. There is no staging or preview step. Review content carefully before submitting.

**Q: Where is the consent PDF stored?**
**A:** Always in the File Repository under "PDF Snapshot Archive," where users cannot edit or delete it. Optionally also in a per-record file upload field if configured (that copy is ordinary field data). Deleting the record, Erase all data, or moving to Production with data deletion removes the archived PDFs; only an external storage copy, if your administrator configured one, survives record deletion. See Section 7.3.

**Q: Can I use the same e-Consent instrument for multiple e-Consent entries?**
**A:** No. Each e-Consent entry is linked to exactly one survey instrument. To run multiple distinct consent processes, create separate instruments and configure each as its own e-Consent entry.

**Q: What happens when a participant clicks "Previous" during the consent flow?**
**A:** If the participant clicks "Previous" on the certification page, REDCap warns them, then clears any fields defined as signature fields in the e-Consent settings. The participant must re-enter them before proceeding. If the survey hides the Previous button, the participant cannot go back and nothing is cleared.

**Q: Can I use the AI writing tool to draft consent content?**
**A:** Yes, if AI tools are enabled on your REDCap instance. The rich text editor in the "Add consent form" popup includes an AI draft option. Always have any AI-generated text reviewed by the relevant compliance office or IRB before going live.

---

# 9. Common Mistakes & Gotchas

**Missing descriptive field placeholder — blank consent content at runtime.** If the e-Consent instrument does not have a descriptive field, the e-Consent Framework cannot inject content into the survey. Participants see a form with name and signature fields but no consent text. Add a descriptive field to the instrument before setting up the e-Consent Framework.

**No default DAG or language version — wrong or missing consent.** Always configure a default version as a fallback. If you create versions only for specific DAGs but not for the default option, a record that is not in a DAG (including new public-survey records) may be shown — and certified against — another DAG's active version, so the archived PDF may carry the wrong site's consent. A record in a DAG that has no version of its own gets no consent content.

**New consent version goes live immediately in Production.** There is no staging environment for consent versions. The moment you click "Add new consent form," the new content is active for all new consents. Prepare and review content before opening the popup, not during.

**Date of birth field not validated.** The e-Consent Framework's DOB dropdown does not filter for fields with date validation — it shows all eligible fields. Selecting a non-date field will cause unexpected behavior. Verify that the selected DOB variable has proper date formatting.

**Reactivating a deactivated version requires re-adding it.** There is no "reactivate" button. If you deactivate a consent version and later need it again, you must re-enter it as a new version with a new version label — labels must be unique per consent, DAG and language, including inactive versions. Keep a copy of the consent text in an external document if there is any chance you will need it again.

**Attestation PDFs are not generated by the e-Consent Framework.** Staff verification attestations are captured via PDF Snapshots, not through e-Consent settings. If your protocol requires an attestation PDF, configure a separate PDF Snapshot trigger on the verification instrument. See [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

---

# Administrator Configuration

The e-Consent Framework is controlled at system level by a REDCap administrator. Administrators configure this in the Control Center under System Configuration → Modules/Services Configuration (see **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)**):

- **Display 'e-Consent Framework' Option for All Surveys** — Must be enabled for the e-Consent configuration button to appear in the Online Designer and survey settings. It is on by default.
- **Capture IP Address of Participants** — Stores the participant's IP address in the File Repository archive entry for each e-Consent PDF (not on the PDF or in the record's data). It is on by default.
- **Custom Message for e-Consent Framework Settings** — Administrators can add institution-specific guidance (e.g., links to IRB requirements or compliance checklists) that appears to project administrators when configuring e-Consent.

If the e-Consent option is not visible in your project's Online Designer, contact your REDCap administrator.

> **See also:** [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)

---

# 10. Related Articles

- [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md)
- [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)
- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (system-level e-Consent Framework enablement)
