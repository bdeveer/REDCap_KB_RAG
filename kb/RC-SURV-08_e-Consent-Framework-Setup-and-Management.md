| **Article ID** | RC-SURV-08 |
|---|---|
| **Domain** | Surveys |
| **Applies To** | Projects with surveys enabled; requires Project Design and Setup, User Rights, and Data Access Groups rights |
| **Prerequisite** | RC-SURV-01 — Surveys – Basics; RC-SURV-02 — Survey Settings: Basic Options & Design |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-09 — PDF Snapshots of Records; RC-DAG-01 — Data Access Groups; RC-USER-01 — User Rights: Overview & Three-Tier Access; RC-FD-02 — Online Designer; RC-AT-01 — Action Tags: Overview |

---

# 1. Overview

This article covers REDCap's e-Consent Framework — a feature that enables electronic consent collection by allowing a participant to review a document, sign it, and generate a permanent, immutable PDF record of that consent. It covers the conceptual model behind e-Consent, everything that must be prepared before configuration, step-by-step setup of the e-Consent Framework, and how to manage consent versions over time. PDF Snapshots, which are related but independently usable, are covered in RC-SURV-09 — PDF Snapshots of Records.

> **Note:** This article covers how to use the e-Consent feature in REDCap. It does not constitute legal guidance on compliant e-consent practice. Requirements vary widely by jurisdiction and institution. Always consult your local compliance office or Institutional Review Board (IRB) to confirm what is required.

---

# 2. Key Concepts & Definitions

**e-Consent**

REDCap's built-in feature for collecting electronic consent. A participant reviews a consent document, enters their name (and optionally a signature and date of birth), and confirms their consent. REDCap then generates an immutable PDF capturing that event.

**e-Consent Framework**

The administrative interface in REDCap where e-Consent settings are configured and consent versions are managed. Accessed via the Online Designer by clicking the "e-Consent" button.

**Consent Version**

A specific instance of consent content (text or PDF) assigned to an e-Consent entry. Versions can be differentiated by language, Data Access Group (DAG), or revision. REDCap tracks which version each record consented on.

**PDF Snapshot**

A REDCap-generated PDF of instrument data at a specific point in time. e-Consent always produces a snapshot. Snapshots can also be generated independently of e-Consent — see RC-SURV-09.

**Verification / Attestation**

The process by which a study team member confirms the identity of the person providing consent. REDCap supports pre-validation (before signing), post-validation (after signing), and no validation. Attestations by staff are captured separately via a PDF Snapshot of a verification instrument.

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
3. REDCap presents a confirmation screen where the participant explicitly agrees to the consent.
4. If the participant clicks "Previous" before confirming, any defined signature fields are automatically cleared.
5. Upon confirmation, REDCap generates an immutable PDF and stores it in the File Repository and/or a specified file upload field.

**Signing options**

REDCap does not perform automatic identity verification (e.g., background checks). Verification is handled procedurally through one of three approaches:

| Verification Type | Description |
|---|---|
| Pre-validation | A staff member attests they verified the participant's identity *before* the participant signs. |
| Post-validation | A staff member attests they verified the participant's identity *after* the participant has signed. |
| No validation | No manual identity check is performed. Acceptable when consent is sent to a known, curated list of recipients. |

Attestations by staff are captured separately via a PDF Snapshot triggered on a verification instrument — not through the e-Consent Framework itself. See Section 5.3 for instrument design guidance, and RC-SURV-09 for snapshot configuration.

**Versioning matrix**

The number of concurrent consent versions equals the product of active DAGs (plus one default) and active languages (plus one default):

> *Example: 4 DAGs × 3 languages = 5 DAG slots (4 + default) × 4 language slots (3 + default) = 20 concurrent versions*

---

# 4. Preparation Checklist

e-Consent pulls configuration from several other areas of REDCap. Setting these up before opening the e-Consent Framework page prevents errors and missing options during setup.

## 4.1 e-Consent Instrument

Create a dedicated instrument in the Online Designer to serve as the e-Consent survey. Include the following fields:

| Field | Field Type | Notes |
|---|---|---|
| First name | Text (no validation) | Required. Best practice: use separate first and last name fields. |
| Last name | Text (no validation) | Required if using two-field name approach. |
| Date of birth | Text (date validation) | Optional. Required only if your consent process needs it. |
| Signature | Signature field type | Optional but strongly recommended. Enables automatic clearing on back-navigation. |
| Descriptive placeholder | Descriptive | Required for versioning. This field receives the injected consent content at runtime. |

> **Important:** The descriptive field placeholder does not need any content entered in the Online Designer — it serves purely as a target for the e-Consent Framework's content injection. Without it, you cannot use versioning, DAG-specific content, or language-specific content.

Once the instrument is created, enable it as a survey. Adjust the **Survey Instructions** and **Survey Completion Text** to reflect that participants are completing a consent form, not a generic survey. For detailed survey configuration guidance, see RC-SURV-02.

> **Tip:** Include a note in the Survey Instructions that there will be a second screen after the form. Without this, participants may think they are done after filling in their information and abandon the process before the confirmation step. Example:
>
> *Survey Instructions:* "Please complete the e-Consent survey below. Note: There will be a second screen after this page. Thank you!"
>
> *Survey Completion Text:* "Thank you for completing our e-Consent."

## 4.2 Languages (if applicable)

If the consent will be offered in multiple languages, define at least two languages in the **Multi-Language Management (MLM)** module before configuring e-Consent. Once two or more languages are defined, the e-Consent Framework will display a language assignment option when adding consent versions.

## 4.3 Data Access Groups (if applicable)

If the project uses DAGs (e.g., for a multi-site study), ensure DAGs are configured before setting up e-Consent. The e-Consent Framework will display a DAG assignment option when adding consent versions, allowing site-specific consent content. See RC-DAG-01 for DAG setup.

## 4.4 Verification Instrument (if using attestation)

If your protocol requires a staff member to attest to identity verification, build a separate instrument to capture that attestation. At minimum, include:

- **User name field** — to record who performed the verification. Add `@READONLY @USERNAME` action tags to auto-populate this from the logged-in user's account and prevent manual editing.
- **Date/time field** — to record when verification occurred.
- **Attestation trigger field** — a checkbox or signature field that signals the attestation is complete. This field will be used as the PDF Snapshot trigger in RC-SURV-09.

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

> **Indicator:** Once at least one e-Consent is active, the "e-Consent" button in the Online Designer gains a green checkmark, and the corresponding survey row gains a blue person-with-checkmark icon in the "Enable as Survey" column.

The main page has two tabs:
- **e-Consent Framework** — where e-Consents are configured and versions managed
- **PDF Snapshots of Records** — for configuring standalone PDF snapshots (covered in RC-SURV-09)

## 5.2 Creating a New e-Consent Entry

Click **"Enable the e-Consent Framework for a survey"** and select the instrument to use as the e-Consent survey. REDCap will display an error if no eligible survey exists.

This opens the e-Consent settings popup, organized into four sections:

**Primary Settings**

- **First/last name fields** — Map to the name variable(s) in the instrument. At least one must be selected. Best practice is to use separate first and last name fields for easier piping elsewhere in REDCap.
- **Allow editing after submission** — Unchecked by default. Leave unchecked unless there is a specific protocol reason to allow post-submission edits. Enabling this does not alter the PDF generated at the time of consent.

**Additional Settings**

- **Date of birth** — Optional. Select a date variable if your consent process requires it. Note: REDCap does not validate that the selected variable has date formatting — verify this yourself.
- **Custom tag/category for PDF footer** — Optional static text appended to the PDF footer (e.g., "Pediatric," "LAR," "Standard").
- **Custom label for PDF header** — Optional. Supports piped values (e.g., `[record_id] -- [last_name]`). Use the "Codebook" and "Smart Variables" buttons in the popup for reference.
- **Signature fields** — Define up to five fields that will be automatically cleared if the participant clicks "Previous" during the consent flow. Click "Select another signature field" to add more (up to five total).

**Location(s) to Save the Signed Consent Snapshot**

- **File Repository** — Always active; all e-Consent PDFs are saved here automatically.
- **Specified field** — Optional. Select a file upload field to also save a copy directly in the record. In longitudinal projects, you must also specify the event.
- **Translated version** — Checked by default when MLM languages are defined. When active, the PDF is generated in the language the participant selected (e.g., a Spanish consent produces a Spanish PDF).

**Snapshot File Name**

Customize the PDF filename using static text and piped values. REDCap always appends a timestamp to prevent duplicates. Examples:

```
pid[project-id]_form[instrument-label]_id[record-name]
→ pid1234_formdemo_consent_id56789_2025-12-12_121534.pdf

[last_name]-[first_name]-record_[record_id]
→ Doe-John-record_56789_2025-12-12_121534.pdf
```

An optional **Notes** field is available for internal documentation. It is not used anywhere in the consent workflow.

> **Yale-specific:** [Describe any local policy on file storage location, naming conventions, or required footer/header content — leave blank until confirmed with Yale REDCap support team]

Click **"Save Settings"** to finalize. Click **Cancel** to discard all entries.

---

# 6. Adding and Managing Consent Versions

## 6.1 Adding a Version

After saving the e-Consent entry, click **"Add consent form"** in the Survey column of the e-Consent table. The popup contains:

- **Consent form version** — A required identifier for this version. Use a consistent scheme (e.g., incrementing integers: 1, 2, 3; or dates: 2025-01-15). The scheme is yours to define — pick one and stick to it.
- **Placement of consent form** — Select the descriptive field placeholder in the e-Consent instrument. Only valid descriptive fields are shown.
- **Display for specific DAG** — If DAGs are defined, assign this version to a specific DAG or to the default ("When record is not assigned to a DAG"). Always create a default version — records without a DAG assignment will show a blank consent if no default exists.
- **Display for specific Language** — If MLM languages are defined, assign this version to a specific language or to the default ("When participant has no language selected"). Always create a default version for the same reason.
- **Consent form content** — Two options:
  - *Rich Text* — Enter or paste consent text directly. Supports rich formatting, HTML import, and (if enabled) AI-generated draft text.
  - *Inline PDF* — Upload a pre-prepared consent PDF. It will be displayed inline within the survey.

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
| Number of Records Consented | Count of records consented on this version |
| Data Access Group | DAG assignment (blank if default or no DAGs) |
| MLM Language | Language assignment (blank if default or no languages) |
| Consent Form Text or File | Preview of text or link to the PDF |

To deactivate a version without replacing it, click **"Set as inactive."** REDCap will ask for confirmation. To reactivate a deactivated version, you must add it as a new version — there is no direct reactivation.

## 6.3 Managing the e-Consent Table

The main e-Consent Framework table provides the following controls per row:

- **Active?** toggle — Enable or disable the entire e-Consent entry
- **Pencil icon** — Edit the e-Consent settings
- **Survey column** — Manage consent versions for that entry

Above the table:
- Add another consent entry (green button)
- Toggle to hide inactive consents
- Search box for locating a specific consent

---

# 7. Finding e-Consent PDFs

## 7.1 File Repository

All e-Consent PDFs are stored in the **File Repository** under a folder named **"PDF Snapshot Archive."** Access the File Repository from the left-hand Applications menu (requires appropriate user rights).

The archive table includes the following columns:

| Column | Description |
|---|---|
| Name | PDF filename — a well-chosen filename during setup pays off here |
| PDF utilized e-Consent Framework | Flags whether the PDF was generated by an e-Consent |
| Record | Direct link to the record and instrument that generated the PDF |
| Survey Completed | Which survey was completed to generate the PDF |
| File Storage Time | Timestamp of PDF generation |
| Identifier | Name and date of birth from the e-Consent settings |
| IP Address | IP of the consenting party, if your administrator has enabled capture |
| Version | The consent version used |
| Type | Whether this was an e-Consent or standard snapshot |
| Size | File size |

The page also supports bulk download of all files as a ZIP archive. Note that large projects can produce very large ZIP files.

## 7.2 File Upload Fields

If you configured per-record file upload fields (Section 4.5), each record's PDF is accessible directly from within the record. These files can be piped, displayed inline, or downloaded in bulk via reports.

---

# 8. Common Questions

**Q: Does REDCap automatically verify the identity of the person signing the consent?**
A: No. REDCap does not perform automated identity verification (such as background checks or account-based identity confirmation). Verification is a procedural step performed by a staff member, captured through a separate attestation instrument and PDF Snapshot.

**Q: Can I use e-Consent without the versioning system?**
A: Yes. If you do not add a descriptive field placeholder, you can still configure an e-Consent — but consent content must be managed directly in the Online Designer, REDCap will not track versions automatically, and you cannot assign different content by DAG or language.

**Q: What happens if a record is not assigned to a DAG and I have no default consent version?**
A: The participant will see a blank consent form — no content will be displayed. Always create a version assigned to the default DAG option ("When record is not assigned to a DAG") to prevent this.

**Q: Can I edit a submitted consent response?**
A: By default, no. The "Allow editing after submission" option in Primary Settings must be explicitly enabled. Note that enabling this does not alter the PDF already generated at the time of original consent.

**Q: How many concurrent consent versions can I have?**
A: The maximum is (number of DAGs + 1) × (number of languages + 1). The +1 accounts for the default slot in each dimension. Example: 4 DAGs and 3 languages = 5 × 4 = 20 concurrent versions.

**Q: When does a new consent version go live?**
A: Immediately upon clicking "Add new consent form" — including in Production mode. There is no staging or preview step. Review content carefully before submitting.

**Q: Where is the consent PDF stored?**
A: Always in the File Repository under "PDF Snapshot Archive." Optionally also in a per-record file upload field if configured.

**Q: Can I use the same e-Consent instrument for multiple e-Consent entries?**
A: No. Each e-Consent entry is linked to exactly one survey instrument. To run multiple distinct consent processes, create separate instruments and configure each as its own e-Consent entry.

**Q: What happens when a participant clicks "Previous" during the consent flow?**
A: Any fields defined as signature fields in the e-Consent settings are automatically cleared. The participant must re-enter them before proceeding.

**Q: Can I use the AI writing tool to draft consent content?**
A: Yes, if AI tools are enabled on your REDCap instance. The rich text editor in the "Add consent form" popup includes an AI draft option. Always have any AI-generated text reviewed by the relevant compliance office or IRB before going live.

---

# 9. Common Mistakes & Gotchas

**Missing descriptive field placeholder — blank consent content at runtime.** If the e-Consent instrument does not have a descriptive field, the e-Consent Framework cannot inject content into the survey. Participants see a form with name and signature fields but no consent text. Add a descriptive field to the instrument before setting up the e-Consent Framework.

**No default DAG or language version — blank consent for unassigned records.** If you create versions only for specific DAGs or languages but not for the default option, any record that falls outside those assignments will receive a blank consent form. Always configure a default version as a fallback.

**New consent version goes live immediately in Production.** There is no staging environment for consent versions. The moment you click "Add new consent form," the new content is active for all new consents. Prepare and review content before opening the popup, not during.

**Date of birth field not validated.** The e-Consent Framework's DOB dropdown does not filter for fields with date validation — it shows all eligible fields. Selecting a non-date field will cause unexpected behavior. Verify that the selected DOB variable has proper date formatting.

**Reactivating a deactivated version requires re-adding it.** There is no "reactivate" button. If you deactivate a consent version and later need it again, you must re-enter it as a new version. Keep a copy of the consent text in an external document if there is any chance you will need it again.

**Attestation PDFs are not generated by the e-Consent Framework.** Staff verification attestations are captured via PDF Snapshots, not through e-Consent settings. If your protocol requires an attestation PDF, configure a separate PDF Snapshot trigger on the verification instrument. See RC-SURV-09.

---

# Related Articles

- RC-SURV-09 — PDF Snapshots of Records
- RC-SURV-01 — Surveys – Basics
- RC-SURV-02 — Survey Settings: Basic Options & Design
- RC-SURV-04 — Survey Link Types & Access Methods
- RC-DAG-01 — Data Access Groups
- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-FD-02 — Online Designer
- RC-AT-01 — Action Tags: Overview
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types
- RC-ALERT-01 — Alerts & Notifications: Setup
