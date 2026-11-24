

**Online Designer**

| **Article ID** | [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured. Online Designer behaviour checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md); [RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md); [RC-FD-07 — Field Embedding](RC-FD-07_Field-Embedding.md); [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md); [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md); [RC-FD-05 — Codebook](RC-FD-05_Codebook.md); [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md); [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) |
| **Synonyms** | what is the online designer; build instruments point and click; create fields one at a time; drag and drop form builder; online designer in development vs production mode; add a field using the designer interface; guided instrument building tool; how to use redcap online designer |

---

## 1. Overview

The Online Designer is REDCap's guided, point-and-click instrument
building tool. It allows users to create instruments and variables one
at a time through an interactive interface, with built-in validation
that prevents common configuration errors. This article explains what
the Online Designer does, when to use it, and how its behavior differs
between Development and Production modes.

---

## 2. Key Concepts & Definitions

**Online Designer**

A web-based, wizard-style interface for creating and editing REDCap
instruments and variables. Changes made in the Online Designer are
validated in real time — REDCap checks that field configurations are
internally consistent (e.g., that branching logic references valid
variable names) before saving them. Branching logic and calculations
are checked again by the server when you save.

**Development Mode vs. Production Mode (Design Context)**

In Development mode, Online Designer changes are applied immediately and
are visible in data entry right away. In Production mode, you must first
select **Enter Draft Mode**; your field and instrument changes then
collect in a draft. The draft must be submitted and approved before it
takes effect — either automatically or by a REDCap administrator,
depending on institutional policy.

**Draft Mode (Production Mode)**

The single set of drafted edits to fields and instruments that has not
yet been applied to the live project. It is not a queue of separate
changes: there is one draft per project, and saving a field again simply
updates the draft. While you are still drafting, you can undo a change by
re-editing it, or discard the whole draft. Once you submit the draft for
review you can no longer edit it; only a REDCap administrator can reject
or reset it. Once approved, changes cannot be rolled back through the
interface (see Section 7 for the recovery path).

Only field and instrument design goes through Draft Mode. Survey
settings, enabling an instrument as a survey, the Survey Queue,
Automated Invitations, Survey Login, survey notifications and similar
project options take effect immediately, even in Production.

**Guardrails**

The Online Designer's built-in validation checks. They catch
configuration errors — for example, branching logic that references a
variable that doesn't exist — before the change is saved. The Online
Designer does not validate whether your instrument design is
scientifically appropriate for your study goals; that judgment belongs
to the research team.

---

## 3. Accessing the Online Designer

- From the Project Setup page (Development mode): select the Online
    Designer button in the Design Your Data Collection Instruments
    section.

- From any project page (Production mode or alternate path):
    select **Designer** in the left-hand menu. This opens the Online
    Designer directly.

- The Online Designer opens to a list of all existing instruments in
    the project. From here you can add a new instrument, open an
    existing one to edit it, or reorder instruments.

---

## 4. What the Online Designer Can Do

### 4.1 Instrument-Level Actions

- Create a new instrument. REDCap builds the instrument's unique name
    from the label you type: lowercase letters, digits and underscores
    only, starting with a letter, not ending in an underscore, at most 50
    characters, and unique in the project (a random suffix is added if
    needed). In Development mode, all existing users get full rights to a
    new instrument; review User Rights afterwards if access should be
    restricted.

- Rename an existing instrument. In Production mode only the
    instrument's display label can change; the unique instrument name of
    a live instrument stays fixed.

- Copy an instrument (see [RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md)).

- Reorder instruments within the project.

- Delete an instrument. REDCap asks you to confirm, but deletion is
    allowed whether or not the instrument contains saved data. You
    cannot delete a project's only instrument. See the warning below for
    what is lost.

> **Warning — deleting an instrument or field:** The saved values stop
> being accessible: they disappear from data entry forms, reports and
> exports. REDCap does not purge them, and they can reappear if a field
> with the same variable name is created again. So deleting a field or
> instrument is **not** a way to remove sensitive data, and you should
> avoid reusing old variable names for new questions. Some things tied to
> the instrument are permanently lost when it is deleted (or its unique
> instrument name changes): locking records, e-signatures, event
> designations, repeating instrument settings, MyCap tasks and
> instrument-level user rights. Files in deleted File Upload fields are
> marked for deletion once the change takes effect. Download a Data
> Dictionary and a data export as a backup before deleting anything.

- Export an instrument as a zip file for backup or reuse (see
    [RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md)).

- Import an instrument from a zip file (see [RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md)).

### 4.2 Variable-Level Actions

- Add a new variable (field) to an instrument.

- Edit an existing variable's field type, label, choices, validation,
    branching logic, and other attributes.

- Reorder variables within an instrument by dragging.

- Move fields to another instrument or to a new instrument with
    **Move field(s)** — this is how you split an instrument in the Online
    Designer.

- Select several fields on one instrument and apply one change to all
    of them (for example alignment, identifier, required, branching
    logic, action tags, question numbers or choices), or move, copy or
    delete them together (see [RC-FD-11 — Online Designer – Advanced Options: Quick-Modify, Field Navigator, and Custom CSS](RC-FD-11_Advanced-Online-Designer-Options.md)).

- Delete a variable. This is allowed in Development mode and, through
    Draft Mode, in Production mode — even when the field contains data.
    The exceptions are fields used by randomization (including strata)
    and a MyCap baseline date field. In Production, deleting a field that
    has data prevents the draft from being auto-approved under most
    policies. See the warning in Section 4.1 for what happens to the data.

- Flag a variable as an identifier.

- Open the branching logic editor for a specific variable.

Variable names are reduced to lowercase letters, digits and underscores,
and REDCap blocks duplicate and reserved names. In Production mode, the
variable name of a field that is already live cannot be changed in the
Online Designer.

For field types, matrix rules and field embedding, see
[RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md)
(Sections 8 and 10), [RC-FD-07 — Field Embedding](RC-FD-07_Field-Embedding.md),
and the column rules in [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md).

In Production, **Draft Preview Mode** lets you try your drafted changes on
data entry forms before submitting them (see [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md), Section 6.5).

### 4.3 Survey-Level Options

When surveys are enabled for the project, a **Survey options** section appears at the top of the Online Designer instrument list. These are project-wide controls — they apply across all surveys, not to a single instrument. The section contains the following buttons:

- **e-Consent** — Enable and configure the e-Consent Framework (see [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md)).
- **Survey Queue** — Configure the Survey Queue, which controls the order and conditions under which surveys are presented to participants after completing a prior survey. Includes a dropdown for bulk import/export of Survey Queue settings via CSV (see [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md)).
- **Auto Invitation options** — Bulk upload or download Automated Invitation settings across all surveys as a CSV file.
- **Survey Login** — Configure survey login (password protection) for the project (see [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md)).
- **Survey Notifications** — Select a project user to receive a notification email each time each survey is completed. Settings apply per survey. See [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) for details.
- **Survey Settings** — Bulk import or export Survey Settings for all instruments at once via CSV.

These project-level buttons are distinct from the per-instrument buttons that appear in the instrument row when an instrument has been enabled as a survey. Each instrument row has its own **Survey settings** button (which opens the Survey Settings page for that instrument) and an **Automated Invitations** button (which configures the ASI for that specific instrument).

> **Important:** None of these survey options go through Draft Mode. In a
> Production project, a change to survey settings, the Survey Queue,
> Automated Invitations, Survey Login or survey notifications takes effect
> as soon as you save it.

The Online Designer also gives access to other project-wide form options,
depending on your REDCap version and what your administrators have
enabled — for example PDF Snapshots, Form Display Logic, downloading a
PDF of all instruments, Descriptive Popups and Instance Embedding. Like
the survey options, these are not part of Draft Mode.

### 4.4 What the Online Designer Cannot Do

- Edit variables across many instruments at once, or rename dozens of
    variables in one step — multi-field edits work on one instrument at a
    time. Use the Data Dictionary for bulk edits
    ([RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)).

- Bypass Draft Mode in Production — every field and instrument change
    in Production goes through a draft that must be approved
    (automatically or by an administrator).

---

## 5. Behavior in Development vs. Production Mode

| **Action** | **Development Mode** | **Production Mode** |
| --- | --- | --- |
| Making a change | Applied immediately | Select **Enter Draft Mode** first; field and instrument changes are saved to the project's draft |
| Seeing the change | Visible in data entry right away | Not visible until the draft is approved (use Draft Preview Mode to try it first) |
| Cancelling a change | Edit and re-save or delete the field | Before submitting: re-edit the field in the draft, or discard the whole draft. After submitting: only an administrator can reject or reset the draft |
| Deleting a field with data | Allowed after a confirmation prompt | Allowed in the draft (except randomization and MyCap baseline date fields); counts against auto-approval |
| Approval required | No | Yes — automatic or administrator, per institutional policy |
| Rollback | Re-edit or re-upload a saved Data Dictionary | No rollback after approval; make the reverse change in a new draft |


> **Institution-specific:** The level of automatic approval in Production mode is set by your REDCap administrators. Options range from never auto-approving, to auto-approving drafts that only add new fields, to auto-approving changes that carry no critical risk flags. Deleting fields that contain data typically needs administrator review. For this installation's specific policy, see **[RC-INST-01 — Institution-Specific Settings & Policies](RC-INST-01_Institution-Specific-Settings-and-Policies.md)**.

> **Note:** Survey settings and other survey options (Section 4.3) are not part of this workflow; in Production they take effect immediately.


---

## 6. When to Use the Online Designer

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

Consider switching to the Data Dictionary ([RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)) when:

- You need to define a large number of variables at once.

- You need to restructure many instruments at once. (Moving a few
    fields to another or new instrument works fine in the Online Designer
    with **Move field(s)**.)

- You are comfortable with REDCap's variable definition schema and
    want faster bulk editing.

---

## 7. Common Questions

**Q: I saved a change in the Online Designer but it isn't showing up in
my data entry forms. Why?**

**A:** Your project is in Production mode. Field changes are saved to a
draft and do not take effect until the draft is submitted and approved.
Depending on your institution's policy, approval may be automatic or may
require a REDCap administrator. Check the Online Designer to see whether
your draft is still being edited or has been submitted for review.

**Q: Can I delete a variable that already has data in it?**

**A:** Yes, in both modes — in Production through Draft Mode, where the
deletion usually needs administrator review. Fields used by randomization
and a MyCap baseline date field cannot be deleted. After deletion the
data is no longer accessible in forms, reports or exports. REDCap does not
purge it, and it can reappear if a field with the same variable name is
created again — so deleting a field is not a way to remove sensitive
data, and avoid reusing old variable names. Download a backup (Data
Dictionary and data export) before deleting.

**Q: Does the Online Designer check whether my branching logic is
correct?**

**A:** It checks that the logic is syntactically valid and references
existing variables — these are the guardrails. It does not verify
whether the logic achieves your intended study behavior. Test branching
logic thoroughly in Development mode before collecting real data.

**Q: Can I reorder instruments after they've been created?**

**A:** Yes. The Online Designer's instrument list supports drag-and-drop
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
be rolled back through the interface. The recovery path is to enter Draft
Mode again and reverse the change, or to re-upload a Data Dictionary that
predates the erroneous change. **Project Revision History** lets you
download the Data Dictionary as it stood at each earlier approved
revision, and also lists the automatic snapshots REDCap takes before every
Data Dictionary upload and API metadata import. If a field was deleted,
re-creating it with the same variable name brings its data back. Saving
your own Data Dictionary backup before any significant change is still
the safest habit.

---

## 8. Common Mistakes & Gotchas

- Expecting field changes in Production to appear immediately: they
    stay in the draft until it is submitted and approved. If a change
    isn't visible, check whether the draft has been submitted. Re-saving
    a field only updates the same draft; it does not create a second
    pending change. Once the draft is submitted, it is locked for
    editing until an administrator approves or rejects it.

- Assuming survey changes in Production wait for approval: survey
    settings, the Survey Queue, Automated Invitations, Survey Login and
    notifications are not part of Draft Mode and go live as soon as you
    save them.

- Assuming the Online Designer validates study design: the guardrails
    catch technical errors (invalid logic syntax, duplicate variable
    names), not scientific ones. The appropriateness of your instrument
    for your study goals is not validated by REDCap.

- Deleting a variable without checking for data: the confirmation
    prompt (**"Are you sure you wish to delete the field(s)..."**) does
    not tell you whether the field has data. Afterwards REDCap lists any
    calculations or branching logic that referenced the field — fix those
    next. Check the field's data before deleting.

- Treating deletion as data removal, or reusing an old variable name:
    deleted fields' values are hidden, not purged, and they come back if
    a new field gets the same variable name. Give new questions new
    variable names.

- Not using the Data Dictionary for large restructuring jobs: the
    Online Designer is not efficient for renaming dozens of variables or
    reorganising many instruments at once. Switch to the Data Dictionary
    for those tasks.

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)** — retrieve the full data dictionary that the Online Designer manages
- **[RC-API-08 — Import Metadata (Data Dictionary) API](RC-API-08_Import-Metadata.md)** — push a new or updated data dictionary programmatically, bypassing the Online Designer
- **[RC-API-09 — Export Instruments API](RC-API-09_Export-Instruments.md)** — retrieve the list of instrument names and labels programmatically

---


## 9. Related Articles

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (prerequisite — covers
    navigation and tool selection)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (the alternative tool for bulk and
    advanced changes)

- [RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) (field types, Edit Field menu, matrix of fields)

- [RC-FD-07 — Field Embedding](RC-FD-07_Field-Embedding.md) (placing fields inside other fields' labels)

- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) (Draft Mode, change risk flags and Draft Preview Mode)

- [RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md) (importing and exporting
    instruments from within the Online Designer)

- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) (read-only reference companion to the Online
    Designer)

- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (enabling surveys and the survey setup workflow)

- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) (Survey Settings page and Survey Notifications)
