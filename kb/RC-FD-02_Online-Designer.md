RC-FD-02

**Online Designer**

| **Article ID** | RC-FD-02 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-01 — Form Design Overview |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-FD-03 — Data Dictionary; RC-FD-05 — Codebook; RC-SURV-01 — Surveys – Basics; RC-SURV-02 — Survey Settings: Basic Options & Design |

---

# 1. Overview

The Online Designer is REDCap\'s guided, point-and-click instrument
building tool. It allows users to create instruments and variables one
at a time through an interactive interface, with built-in validation
that prevents common configuration errors. This article explains what
the Online Designer does, when to use it, and how its behavior differs
between Development and Production modes.

---

# 2. Key Concepts & Definitions

**Online Designer**

A web-based, wizard-style interface for creating and editing REDCap
instruments and variables. Changes made in the Online Designer are
validated in real time — REDCap checks that field configurations are
internally consistent (e.g., that branching logic references valid
variable names) before saving them.

**Development Mode vs. Production Mode (Design Context)**

In Development mode, Online Designer changes are applied immediately and
are visible in data entry right away. In Production mode, changes are
queued as a pending draft. The draft must be reviewed and approved
before it takes effect — either automatically or by a REDCap
administrator, depending on institutional policy.

**Change Queue (Production Mode)**

The set of pending Online Designer edits that have been submitted but
not yet applied to the live project. The change queue can be reviewed
and, if necessary, cancelled before approval. Once approved, changes
cannot be rolled back through the interface.

**Guardrails**

The Online Designer\'s built-in validation checks. They catch
configuration errors — for example, branching logic that references a
variable that doesn\'t exist — before the change is saved. The Online
Designer does not validate whether your instrument design is
scientifically appropriate for your study goals; that judgment belongs
to the research team.

---

# 3. Accessing the Online Designer

- From the Project Setup page (Development mode): click the Online
    Designer button in the Design Your Data Collection Instruments
    section.

- From the Project Home page (Production mode or alternate path):
    click Designer in the left-hand menu, then select Online Designer.

- The Online Designer opens to a list of all existing instruments in
    the project. From here you can add a new instrument, open an
    existing one to edit it, or reorder instruments.

---

# 4. What the Online Designer Can Do

## 4.1 Instrument-Level Actions

- Create a new instrument.

- Rename an existing instrument.

- Reorder instruments within the project.

- Delete an instrument (only if it contains no data).

- Export an instrument as a zip file for backup or reuse (see
    RC-FD-04).

- Import an instrument from a zip file (see RC-FD-04).

## 4.2 Variable-Level Actions

- Add a new variable (field) to an instrument.

- Edit an existing variable\'s field type, label, choices, validation,
    branching logic, and other attributes.

- Reorder variables within an instrument by dragging.

- Delete a variable (only if the project is in Development mode, or if
    the field contains no data).

- Flag a variable as an identifier.

- Open the branching logic editor for a specific variable.

## 4.3 Survey-Level Options

When surveys are enabled for the project, a **Survey options** section appears at the top of the Online Designer instrument list. These are project-wide controls — they apply across all surveys, not to a single instrument. The section contains the following buttons:

- **e-Consent** — Enable and configure the e-Consent Framework (see RC-SURV-08).
- **Survey Queue** — Configure the Survey Queue, which controls the order and conditions under which surveys are presented to participants after completing a prior survey. Includes a dropdown for bulk import/export of Survey Queue settings via CSV (see RC-SURV-07).
- **Auto Invitation options** — Bulk upload or download Automated Invitation settings across all surveys as a CSV file.
- **Survey Login** — Configure survey login (password protection) for the project (see RC-SURV-10).
- **Survey Notifications** — Select a project user to receive a notification email each time each survey is completed. Settings apply per survey. See RC-SURV-02 for details.
- **Survey Settings** — Bulk import or export Survey Settings for all instruments at once via CSV.

These project-level buttons are distinct from the per-instrument buttons that appear in the instrument row when an instrument has been enabled as a survey. Each instrument row has its own **Survey settings** button (which opens the Survey Settings page for that instrument) and an **Automated Invitations** button (which configures the ASI for that specific instrument).

## 4.4 What the Online Designer Cannot Do

- Split one instrument into two or more instruments — use the Data
    Dictionary for this (RC-FD-03).

- Edit many variables at once — use the Data Dictionary for bulk
    edits (RC-FD-03).

- Bypass the Production mode change queue — all changes in
    Production require review.

---

# 5. Behavior in Development vs. Production Mode

| **Action** | **Development Mode** | **Production Mode** |
| --- | --- | --- |
| Making a change | Applied immediately | Added to the pending change queue |
| Seeing the change | Visible in data entry right away | Not visible until the change is approved |
| Cancelling a change | Edit and re-save or delete the field | Cancel the pending change from the change queue before approval |
| Approval required | No | Yes — automatic or administrator, per institutional policy |
| Rollback | Re-edit or re-upload a saved Data Dictionary | Cancel before approval; no rollback after approval |

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** The level of automatic approvals in Production mode is set centrally by your institution\'s REDCap support team. Some institutions allow minor changes (adding a new field) to be auto-approved, while others require administrator review for any change. For this installation\'s specific policy, see **RC-INST-01 — Institution-Specific Settings & Policies, Section 4: Draft Mode Approval Policy**.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

# 6. When to Use the Online Designer

The Online Designer is the right tool in these situations:

- You are new to REDCap *and want guided, validated instrument
    building with guardrails.*

- You are making a small number of changes *--- adding or editing a
    handful of variables — and want to see the result immediately.*

- You are building a simple instrument *with a limited number of
    variables where a spreadsheet would be overkill.*

- You want to preview what your instrument will look like *as you
    build it — the Online Designer shows a live rendering of the
    form.*

Consider switching to the Data Dictionary (RC-FD-03) when:

- You need to define a large number of variables at once.

- You need to split, merge, or restructure instruments.

- You are comfortable with REDCap\'s variable definition schema and
    want faster bulk editing.

---

# 7. Common Questions

**Q: I saved a change in the Online Designer but it isn\'t showing up in
my data entry forms. Why?**

**A:** Your project is in Production mode. Changes do not take effect until
they pass through the change queue review process. Depending on your
institution\'s policy, approval may be automatic or may require a REDCap
administrator. Check the pending change queue to confirm your change was
submitted.

**Q: Can I delete a variable that already has data in it?**

**A:** In Production mode, variables with data cannot be deleted through the
Online Designer. In Development mode, deleting a variable with test data
is allowed, but the data is permanently lost. Always confirm whether a
variable contains real or test data before attempting deletion.

**Q: Does the Online Designer check whether my branching logic is
correct?**

**A:** It checks that the logic is syntactically valid and references
existing variables — these are the guardrails. It does not verify
whether the logic achieves your intended study behavior. Test branching
logic thoroughly in Development mode before collecting real data.

**Q: Can I reorder instruments after they\'ve been created?**

**A:** Yes. The Online Designer\'s instrument list supports drag-and-drop
reordering. In longitudinal projects, instrument order also affects how
they appear in the Record Home Page and Record Status Dashboard.

**Q: Can I use the Online Designer and the Data Dictionary on the same
project?**

**A:** Yes. They operate on the same underlying instrument and variable
definitions. Changes made in one tool are reflected in the other. It is
common to use the Online Designer for small edits and the Data
Dictionary for bulk restructuring on the same project.

**Q: What happens if I make a mistake in Production mode and the change
is auto-approved before I catch it?**

**A:** Once an Online Designer change is approved in Production, it cannot
be rolled back through the interface. The recovery path is to re-edit
the variable manually in the Online Designer, or to re-upload a
previously saved Data Dictionary snapshot that predates the erroneous
change. This reinforces why saving a Data Dictionary backup before any
significant change is critical.

---

# 8. Common Mistakes & Gotchas

- Expecting changes in Production to appear immediately: changes in
    Production mode go through a review queue. If a change isn\'t
    visible after saving, check the pending change queue rather than
    saving it again.

- Submitting the same change multiple times in Production: if the
    change appears to do nothing, it may be in the queue waiting for
    approval. Submitting again creates a duplicate pending change. Check
    the queue first.

- Assuming the Online Designer validates study design: the guardrails
    catch technical errors (invalid logic syntax, duplicate variable
    names), not scientific ones. The appropriateness of your instrument
    for your study goals is not validated by REDCap.

- Deleting a variable in Development without realizing it has test
    data: deleting a variable permanently removes its data. In
    Development mode this is allowed without warning. Always check
    whether the field contains data you intend to keep before deleting.

- Not using the Data Dictionary for large restructuring jobs: the
    Online Designer is not efficient for moving many variables between
    instruments or renaming dozens of variables at once. Switch to the
    Data Dictionary for those tasks.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-07 — Export Metadata (Data Dictionary) API** — retrieve the full data dictionary that the Online Designer manages
- **RC-API-08 — Import Metadata (Data Dictionary) API** — push a new or updated data dictionary programmatically, bypassing the Online Designer
- **RC-API-09 — Export Instruments API** — retrieve the list of instrument names and labels programmatically

---


# 9. Related Articles

- RC-FD-01 — Form Design Overview (prerequisite — covers
    navigation and tool selection)

- RC-FD-03 — Data Dictionary (the alternative tool for bulk and
    advanced changes)

- RC-FD-04 — Instrument Library & Zip Files (importing and exporting
    instruments from within the Online Designer)

- RC-FD-05 — Codebook (read-only reference companion to the Online
    Designer)

- RC-SURV-01 — Surveys – Basics (enabling surveys and the survey setup workflow)

- RC-SURV-02 — Survey Settings: Basic Options & Design (Survey Settings page and Survey Notifications)
