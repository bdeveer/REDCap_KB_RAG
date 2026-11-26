---
id: RC-FD-04
title: Instrument Library & Zip Files
domain: Form Design
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Instrument
  Library and zip import/export checked against source code; pages not re-captured
prerequisites:
- RC-FD-01 — Form Design Overview
version: '1.2'
last_updated: 2026-11
related:
- id: RC-FD-01
  title: Form Design Overview
- id: RC-FD-02
  title: Online Designer
- id: RC-FD-03
  title: Data Dictionary
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
tags:
- form design
- instruments
synonyms:
- how to import an instrument from the library
- reuse a prebuilt instrument
- download an instrument as a zip file
- share an instrument between projects
- redcap shared instrument library
- import instrument zip into my project
- copy a form without rebuilding it
- validated instruments from vanderbilt library
---

# 1. Overview

This article covers two mechanisms for importing and exporting REDCap
instruments: the REDCap Instrument Library and the Zip File feature.
Both allow instruments to move into or out of a project without building
them from scratch, but they serve different use cases and draw from
different sources.

---

# 2. Key Concepts & Definitions

**REDCap Instrument Library**

A centrally maintained collection of instruments provided by Vanderbilt
University (the developer of REDCap) and curated by the REDCap
consortium. Instruments in the library have been reviewed before being
made available. The library includes validated clinical and research
scales as well as community-contributed instruments.

**Zip File (Instrument Export/Import)**

A file format used to export and import individual REDCap instruments. A
zip file captures the instrument's design — its variable definitions,
field types, labels, choices, branching logic and related settings (see
section 4.1) — but not any data collected using that instrument. Zip
files are project-agnostic and can be imported into any REDCap project,
subject to the version caveat in section 4.4.

**Variable Name Collision**

A conflict that occurs when an imported instrument contains a variable
name that already exists in the destination project. REDCap does not ask
you to resolve it: the colliding variable is renamed automatically (see
sections 3.3 and 4.4).

**Instrument Name Collision**

A conflict that occurs when an imported instrument has the same internal
name (form\_name) as an existing instrument in the destination project.
On a zip import REDCap renames the instrument automatically. On a
Library import you type the instrument name yourself.

---

# 3. REDCap Instrument Library

## 3.1 What It Contains

- Validated clinical and research instruments (e.g., PHQ-9, GAD-7,
    PROMIS scales).

- Community-contributed instruments submitted by REDCap users and
    reviewed before publication.

- A mix of free and fee-based instruments. The library clearly
    indicates which instruments require a license or fee before import.

- PROMIS, computer-adaptive (CAT) and auto-scoring instruments. These
    cannot be modified after import — you can only rename or delete
    them — and they are enabled as surveys automatically.

## 3.2 Accessing the Library

- On the Project Setup page, click **Explore the REDCap Instrument
    Library** in the Design your data collection instruments section.

- In the Online Designer, click **Import a new instrument from the
    official REDCap Instrument Library**.

- In a production project, both buttons are hidden unless the project
    is in Draft Mode.

- The library interface allows browsing and searching by instrument
    name, category, and keyword.

- Browsing the library sends your name, email address, institution,
    REDCap server and REDCap version to Vanderbilt.

## 3.3 Importing from the Library

- Find the instrument you want. Review its description, field count,
    and licensing status.

- Click Import and type the name the instrument should have in your
    project.

- Any variable names that clash with variables already in your project
    are renamed automatically with a short suffix. No list of renamed
    variables is shown, so check the variable names after import.

- REDCap updates references to the renamed variables in the imported
    instrument's calculations and branching logic.

- If the same library instrument is already in your project, REDCap
    warns you but still lets you import it again.

- After import, open the instrument in the Online Designer and check
    variable names, action tags and piping in labels, field notes and
    section headers.

## 3.4 Contributing to the Library

You can share your own instrument directly from REDCap:

1. Open the Online Designer of a **production** project that is not in
    Draft Mode.

2. Click **Share your instruments with others via the REDCap Shared
    Library** and pick the instrument.

3. Enter the submitter information and accept the Shared Content
    Agreement.

The instrument is reviewed before it appears in the library. You can
limit sharing to your own institution, and replace or remove a shared
instrument later. Only the copyright owner of an instrument may share
it. Your local REDCap support team can help if you have questions about
the process.

> **Important:** Always review imported instruments in the Online Designer after import. Variable names may have been renamed to avoid collisions, and the instrument may reference variables that don't exist in your project.

---

# 4. Zip File Feature

## 4.1 What Zip Files Contain

A zip file holds one instrument. It **contains**:

- The instrument's data dictionary rows (file **instrument.csv**):
    variable names, field types, labels, choices, validation, branching
    logic, calculations, field annotations and action tags.
- The name of the server it came from.
- Field attachments and embedded video URLs.
- Survey settings, including the survey logo and confirmation email
    attachment, if the instrument is enabled as a survey.
- Survey stop actions.
- MyCap task settings, if the instrument is a MyCap task.

It does **not contain**:

- Collected data.
- Event designations, repeating instrument setup, alerts, automated
    survey invitations, the survey queue, form display logic,
    multi-language translations or e-Consent settings.

## 4.2 Accessing Zip File Export and Import

- Zip file export and import are in the Online Designer — neither is on
    the Project Setup page.

- To export, open an instrument's **Choose action** menu in the
    instrument list and select **Download instrument ZIP**.

- The import button sits above the instrument list. Its dialog also
    lists external libraries that publish instrument zip files.

## 4.3 Exporting an Instrument as a Zip File

- In the Online Designer, open the **Choose action** menu for the
    instrument and select **Download instrument ZIP**.

- Save the file. It contains the instrument definition only — no
    participant data.

- An instrument that exists only in Draft Mode (not yet approved)
    cannot be downloaded.

- The exported zip file can be kept as a copy of the instrument's
    design, shared with collaborators, or imported into another REDCap
    project.

## 4.4 Importing a Zip File

- Imports are only possible in development, or in production while the
    project is in Draft Mode. In production the change is reviewed like
    any other draft change.

- The file must be a .zip with **instrument.csv** at its top level, and
    within your server's maximum upload size.

- The imported instrument is added as the last instrument in the
    project.

- If an instrument name, variable name or matrix group name collides
    with one already in the project, REDCap adds a short random suffix
    automatically. A list of renamed variables is shown after import.

- REDCap updates references to the renamed variables inside the
    imported instrument: calculations, branching logic, action tags and
    field annotations.

- The import is all or nothing. If the zip itself contains duplicate
    names, the import stops and nothing is added.

- Importing a survey-enabled instrument turns on surveys for the
    project. Importing a MyCap task makes the instrument repeating.

- Review the imported instrument in the Online Designer: check action
    tags and piping in labels, field notes and section headers, and any
    references to it from other instruments.

> **Version caveat (zip from v17 into v16.0.61):** a survey-enabled instrument zip exported from REDCap v17 is rejected by v16.0.61 with "Invalid survey settings in instrument ZIP". Zips move freely between v17.3 and v17.6, and non-survey zips work across all three versions. Export from the same or an older version than the target server.

> **Note:** Zip file import does not overwrite existing instruments — it adds the imported instrument as a new one. To replace an existing instrument, you must delete it first. REDCap does not block deleting an instrument that has data, but deleting it deletes its data. Treat this as data loss and delete and re-import only while the instrument has no data.

---

> **Note (15.3.1) — PROMIS batteries in longitudinal projects.** When a PROMIS battery of instruments is downloaded from the Shared Library and the **first** instrument in the battery has already been designated to an event, REDCap handles the remaining instruments' event designation correctly. On earlier versions the designation step behaved inconsistently for the rest of the battery.

---

# 5. Library vs. Zip File: When to Use Each

| **Factor** | **Instrument Library** | **Zip File** |
| --- | --- | --- |
| Source | Centrally curated, Vanderbilt-hosted | Any REDCap user or project |
| Curation | Reviewed before publication | Not curated — quality varies |
| Licensing | Some instruments require a fee | Copyright still applies; uploading one confirms it holds no third-party copyrighted content |
| Use case | Validated clinical scales; community tools | Reusing your own instruments; sharing with collaborators |
| Backup use | Not applicable | Copy of one instrument's design only — not a project backup |
| Access point | Project Setup page or Online Designer | Online Designer only |
| Collision handling | You type the instrument name; clashing variables renamed without a list | Clashing names renamed automatically; list of renamed variables shown |

---

# 6. Common Questions

**Q: Does importing from the Instrument Library add the instrument to my
project permanently?**

**A:** Yes. Once imported, the instrument is part of your project and can be
modified, deleted, or exported like any other instrument (PROMIS, CAT and
auto-scoring instruments can only be renamed or deleted). Deleting an
instrument deletes its data. The library copy is unaffected.

**Q: Can I export an instrument that already has data collected in it?**

**A:** Yes. The zip file export captures the instrument's design only —
it does not include any collected data. The export is safe to perform at
any time regardless of data collection status.

**Q: What should I do if variable names collide during import?**

**A:** Nothing at import time — REDCap renames colliding variables
automatically. A zip import shows a list of renamed variables; a Library
import does not, so compare the variable names yourself. REDCap updates
references inside the imported instrument, but check action tags, piping
in labels and notes, and any references from other instruments, and
rename variables in the Online Designer if you want different names.

**Q: Can I share a zip file with someone at a different institution
using a different REDCap instance?**

**A:** Yes. Zip files are portable across REDCap instances. A
survey-enabled zip from v17 cannot be imported into v16.0.61, so export
from the same or an older version than the destination server. Name
collisions are handled at import time by the destination project.

**Q: Are copyrighted instruments restricted in how I can use them?**

**A:** Yes. Fee-based or copyrighted instruments in the library come with
license terms that govern their use. The library indicates which
instruments have licensing requirements. Do not import a fee-based
instrument without verifying your institution has the appropriate
license. The same applies to zip files: a zip does not remove the
copyright of the instrument it carries.

**Q: Can I contribute my instrument to the Instrument Library?**

**A:** Yes, directly from the Online Designer of a production project that is
not in Draft Mode, if you own the instrument's copyright. See section 3.4.
The submission is reviewed before it is published. Your local REDCap
support team can help.

---

# 7. Common Mistakes & Gotchas

- Not reviewing imported instruments after import: variable names may
    have been renamed automatically — without a list on a Library
    import — and the instrument may reference variables that don't
    exist in your project. Always open the imported instrument in the
    Online Designer to verify it.

- Expecting zip file import to replace an existing instrument: zip
    imports add a new instrument — they do not overwrite an existing
    one. Deleting the old instrument is not blocked when it has data,
    but its data is deleted with it. Delete and re-import only while
    the instrument has no data.

- Importing a fee-based library instrument without a license: some
    instruments require your institution to hold a license. Using them
    without the appropriate license may have legal implications. Check
    the instrument's licensing status before importing.

- Treating a zip file, data dictionary or snapshot as a backup: they
    contain only design, never collected data. For a full backup, use a
    data export or the project XML export with data.

- Looking for zip import/export on the Project Setup page: the feature
    is only in the Online Designer's instrument list.

- Importing a v17 survey-enabled zip into a v16.0.61 server: it is
    rejected. Export from the same or an older version than the target.

---

# 8. Administrator Configuration

Access to the REDCap Shared Library (the consortium's instrument repository) requires a system-level setting to be enabled by a REDCap administrator. This is done in the Control Center under System Configuration → Modules/Services Configuration (see **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)**, "REDCap Shared Library" toggle). Administrators can also disable the Library for an individual project.

When the Shared Library is disabled, the Library buttons do not appear on the Project Setup page or in the Online Designer. The zip file import/export feature (Section 4) is a local operation and is unaffected by this setting — zip files work regardless of whether the Shared Library is enabled.

Outbound HTTP access to the Consortium's server (`redcap.vumc.org`) is also required for the Shared Library to function. In restricted-network environments, this connection may need to be allowed through a firewall.

> **See also:** [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)

---

# 9. Related Articles

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (prerequisite)

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (the access point for zip file import
    and export)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (alternative approach for bulk
    instrument management)

- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (system-level REDCap Shared Library enable/disable)
