RC-OPS-01

**Using REDCap as an Operational Request Management System**

| **Article ID** | RC-OPS-01 |
|---|---|
| **Domain** | Operational & Administrative Project Design |
| **Applies To** | Classic (non-longitudinal) projects; institutions using REDCap for internal administrative workflows |
| **Prerequisite** | RC-FD-01 — Form Design Overview; RC-LONG-02 — Repeated Instruments and Events Setup; RC-SURV-04 — Survey Link Types and Access Methods |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-LONG-02 — Repeated Instruments and Events Setup; RC-SURV-04 — Survey Link Types and Access Methods; RC-USER-02 — User Rights; Style Guide §4.1–4.3, §5.1 |

---

# 1. Overview

REDCap is primarily designed for research data collection, but its form builder, survey engine, branching logic, and repeating instruments also make it an effective platform for internal administrative workflows — particularly **request management** and **account administration**.

This article describes a proven project design pattern for building a request intake and review system inside REDCap. Common use cases include:

- REDCap account request management (study accounts, user access, new projects)
- Service request or consultation intake and tracking
- Internal approval workflows with structured review steps

This pattern is appropriate when:
- Requesters submit information via a survey or form and do not have REDCap accounts of their own
- Staff need to review, annotate, and track status internally without the requester seeing those fields
- Requests have multiple types (e.g., new account vs. new user vs. new project) that each need distinct fields
- Some requests generate sub-requests over time (e.g., a study account that later has multiple user additions)

---

# 2. Project Configuration

## 2.1 Project type

Use a **classic (non-longitudinal)** project. Each request (or each study account) is a record. The different request types are modeled as separate instruments, not as events.

Longitudinal mode is not necessary here and adds overhead — event setup, event-scoped branching logic, and a more complex record status dashboard — without any functional benefit for a workflow that has no time-point structure.

## 2.2 Repeating instruments

Enable repeating instruments (not repeating events) for request types that may occur multiple times per record. For example, if a study account can accumulate multiple user addition requests over time, the user request instrument repeats and each addition is a separate instance.

Set a **custom form label** on each repeating instrument to surface the key identifier for that instance. Without a label, the dashboard shows only "Instance 1", "Instance 2", etc., which is not useful when a record has many instances.

Example custom labels:

```
[institutional_id], [user_name]
```

```
[projectname] ([server_label]), pid: [pid]
```

See the Style Guide (Section 5.1) for detailed guidance on configuring custom form labels.

## 2.3 Surveys

Enable surveys so that requesters can complete intake forms without needing a REDCap account. The typical intake workflow is:

1. Staff create a new record (with auto-numbering enabled) or the record is created on survey submission.
2. Staff send the appropriate survey link to the requester.
3. Requester completes the intake form externally.
4. Staff complete the admin-only review section in data entry mode.

Review fields should not be part of the survey — they are staff-only and should only appear in data entry mode.

## 2.4 Record auto-numbering and custom record label

Enable **record auto-numbering** so records are assigned IDs without manual intervention.

Set the **project-level custom record label** to a meaningful identifier so the record list is easy to scan. For an account administration project, the PI name works well:

```
PI: [pi_lname], [pi_fname]
```

This is configured under Project Setup → Additional Customizations → "Custom Record Label."

---

# 3. Instrument Design

## 3.1 Instrument 1 — Request Intake (root instrument)

The first instrument on every record captures minimal information about the initial contact and routes the request. Keep it short — its purpose is to open the record and track overall status, not to collect all details.

Typical fields:

| Field | Type | Notes |
|---|---|---|
| `requester_fname` | Text | Requester first name |
| `requester_lname` | Text | Requester last name |
| `requester_email` | Text (email validation) | Requester contact email |
| `date_request` | Text (date\_mdy validation) | Date of initial request |
| `send_survey_link` | Radio (Yes/No) | Staff flag: has the intake survey link been sent? |
| `request_status` | Radio | Overall status: In-process / Active / Declined |
| `request_notes` | Notes | Free-text log of communications and actions taken |

## 3.2 Instrument 2 — Study / Account Request (survey)

The primary intake instrument, sent to the requester as a survey. It collects structured information about the study or project. Organize it into clearly labeled sections.

**Section: PI or Primary Contact**

Collect PI identity first. Then conditionally show a separate primary contact section using a single radio to gate it:

```
[pi_is_primary_contact] = '2'   → show primary contact fields
```

Typical PI fields: last name, first name, institutional identifier (e.g., username or staff ID), department, section, email (with email validation), phone (with phone validation).

Typical primary contact fields: same as PI fields, plus a role dropdown (e.g., Administrator, Biostatistician, Data Coordinator/Manager, Faculty Advisor, Investigator, Nurse Research Coordinator, Post Doc, Study Coordinator, Other).

Use `@PLACEHOLDER` on email fields to show the expected format (e.g., `@PLACEHOLDER='firstname.lastname@example.edu'`).

**Section: Study Information**

Collect the full study title and a short display title. These become the identifier visible in the record dashboard and in reports.

**Section: Human Subject Research**

Gate IRB-related fields behind a Yes/No radio:

```
[human_subject] = '1'   → show IRB/protocol number, study registry reference, research type, study type
[human_subject] = '2'   → show free-text explanation field (e.g., animal research, QI, exempt)
```

**Section: Funding**

Use a checkbox field for funding type (e.g., Federal, State, Non-profit, Industry, Department, Other). Gate a free-text "specify" field on the "Other" checkbox value:

```
[fund_type(99)] = '1'   → show fundtype_other field
```

**Section: Access Dates**

Collect start date, an optional end date, and a radio for "no end date / keep access ongoing." Add a conditional warning descriptive field for the case where ongoing access is declined but no end date is provided:

```
[ongoing] = '2' and [enddate] = ''
```

Display the warning with styled HTML to make it visually prominent:

```html
<span style="color:red;font-weight:bold;">
No end date was entered. Please enter an end date above or change your selection to ongoing access.
</span>
```

See Style Guide Section 4.2 for general guidance on this conditional warning pattern.

**Section: Billing Contact**

Collect billing contact name, email, phone, and any relevant billing codes. If your institution has multiple billing paths (e.g., standard vs. government agency billing), gate each section on a radio field:

```
[gov_billing] = '1'   → show government agency billing fields (institution name, billing contact, full address)
[gov_billing] <> '1' → show standard billing contact fields and cost center codes
```

**Section: Admin-Only Review**

See Section 4 below. This section appears at the end of the instrument but is hidden from the requester via branching logic.

## 3.3 Instrument 3 — User Request (repeating)

Captures requests to add individual users to an existing study account. This instrument repeats so that a single record can accumulate multiple user additions over time.

Typical fields:

| Field | Type | Notes |
|---|---|---|
| `user_institutional_id` | Text | Institutional identifier (e.g., username or staff ID) |
| `user_name` | Text | Display name |
| `user_email` | Text (email validation) | User's email |
| `user_type` | Radio | Staff vs. affiliate/external |
| `role` | Radio | Primary role (see role list below) |
| `role_other` | Text | Specify if role = Other; branched: `[role] = '99'` |
| `requester_id` | Text | Who submitted this request |
| `date_request` | Text (date\_mdy, @TODAY @READONLY) | Auto-stamped request date |

**Role list:** Administrator, Biostatistician, Data Coordinator/Manager, Faculty Advisor, Investigator, Nurse Research Coordinator, Post Doc, Study Coordinator, Other.

Use `@TODAY @READONLY` on the date field to auto-populate it when the form is first opened and prevent subsequent editing. This captures the submission timestamp without requiring staff to enter it manually.

## 3.4 Instrument 4 — Project Request (repeating)

Captures requests to create new projects (or sub-projects) under an existing study account. Also repeats.

Typical fields: project name, project type (main study / operational / testing/dev / quality improvement / ancillary), research type, brief description, requester name and institutional identifier.

Optionally track: which server the project was created on, the project ID assigned, and whether default user roles were set up and the requester was added.

## 3.5 Instrument 5 — Communications Log (optional, repeating)

A lightweight log for tracking batch communications sent to accounts. Useful if staff periodically send status emails to study PIs.

Typical fields: batch email status (not selected / selected / processed), date of last email sent, email log (notes field), and a linking project ID field if the record is tied to a specific system project.

---

# 4. Admin-Only Review Sections

Each main instrument should have an admin-only review block that is **hidden from requesters** but visible to staff in data entry mode.

## 4.1 Implementation

1. Add a **reviewer identity field** near the top of the review block. The reviewer types their own identifier (username, staff ID, or role name) when they begin the review.
2. Gate all review fields on that identity field being non-empty:

```
[reviewer_field] <> ''
```

Or, if using a role-based approach:

```
[reviewer_role] = 'admin'
```

3. Do **not** hardcode individual staff usernames or identifiers in branching logic expressions. Hardcoded identifiers are fragile (they break when staff change), hard to audit, and embed personnel information in the data dictionary. See Style Guide Section 4.1 for the rationale and preferred alternatives.

> **Note:** Branching logic provides visual hiding — it prevents the review fields from appearing on the form. To prevent unauthorized editing, also configure user rights so that requesters (if they have REDCap accounts) do not have edit access to the review fields. The two controls work together: user rights protect the data; branching logic provides the clean visual separation.

## 4.2 Typical admin review fields

| Field | Type | Notes |
|---|---|---|
| `review_date` | Text (date\_mdy) | Date staff reviewed the submission |
| `requester_matched` | Radio (Yes/No) | Requester identity confirmed against PI/contact on file |
| `notification_date` | Text (date\_mdy) | Date outcome communicated to requester |
| `admin_note` | Notes | Internal notes |
| `account_status` | Radio | Active / Pending / Closed |
| `account_status_date` | Text (date\_mdy) | Date the status was set |

## 4.3 Descriptive cross-reference fields

In repeating instruments (user request, project request), add a **descriptive field** that pipes in the study's PI and primary contact from the study account instrument. This saves the reviewer from navigating away to look up who the PI is.

Example field label (using piping):

```html
<span style="color:#1A6496;">
  <strong>Study PI:</strong> [pi_fname] [pi_lname] &nbsp;|&nbsp;
  <strong>Primary Contact:</strong> [primary_contact_fname] [primary_contact_lname]
</span>
```

Gate this descriptive field on the same reviewer identity condition so it only appears during staff review.

---

# 5. Funding Detail Instrument

If detailed funding tracking is a core need, consider a dedicated funding instrument rather than embedding funding fields in the study account instrument.

**Option A — Fixed slots:** Create a fixed set of funding source groups (e.g., fundsource1/awardnum1/awardamount1 through fundsource5). Simple to implement, but users must scroll through all five slots even if only one applies, and the empty slots add noise to exports.

**Option B — Repeating instrument:** Make the funding instrument itself repeating, with one instance per funding source. Each instance collects: funding source description, award number (or "NA" if none), and award amount. This is cleaner in exports and scales to any number of sources, but adds instance management complexity.

For new projects, Option B (repeating) is recommended. Option A may be acceptable for existing projects where changing to a repeating structure would require data migration.

---

# 6. Design Decisions and Trade-offs

**Classic vs. longitudinal:** Use classic mode. Each record is a study account. The different request types (user, project) are repeating instruments within that record — not events. Adding longitudinal mode here provides no functional benefit and increases configuration overhead.

**Survey vs. data entry form:** The intake instrument works well as a survey because requesters typically do not have REDCap accounts. Staff create the record (or it is auto-created on survey submission) and send the survey link; the requester completes it externally. Review fields are staff-only and must not be part of the survey instrument.

**Branching logic vs. required fields:** Use branching logic to hide irrelevant sections (e.g., government billing fields when that payment path is not applicable) rather than leaving all fields visible and requiring users to enter "N/A." Hidden fields produce cleaner exports and a less cluttered form experience.

**Admin visibility via branching vs. user rights:** These are complementary, not alternatives. Branching logic hides review fields visually from the form — including on surveys, where user rights do not apply. User rights prevent editing by users who do have project access. Both should be configured.

---

# 7. Common Questions

**Q: Can the requester fill in the intake form without a REDCap account?**

**A:** Yes — if the intake instrument is enabled as a survey and the requester is sent a survey link, they complete it without logging in. Staff create the record and distribute the link; the requester never needs REDCap credentials.

**Q: How do I prevent requesters from seeing the admin review fields if they do have a REDCap account?**

**A:** Use branching logic on a reviewer identity field (Section 4.1) to hide review fields unless the reviewer has identified themselves. Additionally, configure user rights so that requesters have limited or no edit access to the review instrument.

**Q: Can I pipe values from the study account instrument into the repeating user request instrument?**

**A:** Yes. Piping between non-repeating and repeating instruments in a classic project works when the source variable is in a non-repeating instrument and the target is a field label or descriptive field in the repeating one. Use this to surface PI and contact info in the review section without requiring navigation. Note that piping from a repeating instrument *into* a non-repeating one is not reliably supported.

**Q: How do I handle multiple funding sources?**

**A:** See Section 5. A repeating funding instrument (one instance per source) is the recommended approach for new projects. A fixed multi-slot design works but produces noisy exports when most records have fewer funding sources than the number of slots.

**Q: Should the communications log instrument be repeating or a single notes field?**

**A:** A repeating instrument gives each communication a discrete, timestamped record that can be filtered in reports. A notes field in the root instrument is simpler but conflates all communications into a single text blob. Use the repeating instrument approach if you need to report on communication activity; use a notes field if you only need an informal running log.

---

# 8. Common Mistakes and Gotchas

**Hardcoding staff identifiers in branching logic.** This is the most common design mistake in admin-only review sections. Hardcoded usernames or staff IDs break when personnel change and embed personal identifiers in the data dictionary. Use a role value or a non-empty check instead. See Style Guide Section 4.1.

**Including review fields in the survey instrument.** If the same instrument is used both as a survey (for the requester) and for data entry (for staff), any fields visible on the survey will be visible to the requester — regardless of user rights. Move review fields behind branching logic that only activates when a reviewer has identified themselves, or place them in a separate non-survey instrument.

**Using a fixed funding slot design when the number of sources varies widely.** Fixed slots produce export rows with many empty columns for records with fewer sources than the maximum. If the number of funding sources per record varies significantly, use a repeating funding instrument.

**Forgetting to set custom form labels on repeating instruments.** Without custom labels, the record status dashboard shows only "Instance 1", "Instance 2", etc. When a record has many instances, this makes it very difficult to locate a specific user or project request. Set custom labels during initial setup — it is much harder to retrofit once data exists.

**Relying on branching logic alone for access control.** Branching logic hides fields visually but does not prevent API access or direct URL manipulation by users with edit rights. Always pair branching logic with appropriate user rights configuration.

---

# 9. Related Articles

- RC-LONG-02 — Repeated Instruments and Events Setup
- RC-SURV-04 — Survey Link Types and Access Methods
- RC-SURV-06 — Automated Survey Invitations (for sending recurring links to requesters)
- RC-USER-02 — User Rights: Adding Users and Managing Roles
- RC-USER-03 — User Rights: Configuring User Privileges
- RC-PROJ-04 — Project Setup: Additional Customizations (custom record label configuration)
- Style Guide §4.1 — Anti-pattern: hardcoded user identifiers in branching logic
- Style Guide §4.2 — Conditional warning via descriptive field
- Style Guide §4.3 — Admin-only review sections
- Style Guide §5.1 — Custom form labels for repeating instruments
