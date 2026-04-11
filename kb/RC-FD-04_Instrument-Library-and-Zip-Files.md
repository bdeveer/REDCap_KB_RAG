RC-FD-04

**Instrument Library & Zip Files**

| **Article ID** | RC-FD-04 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-01 — Form Design Overview |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary |

# 1. Overview

This article covers two mechanisms for importing and exporting REDCap
instruments: the REDCap Instrument Library and the Zip File feature.
Both allow instruments to move into or out of a project without building
them from scratch, but they serve different use cases and draw from
different sources.

# 2. Key Concepts & Definitions

**REDCap Instrument Library**

A centrally maintained collection of instruments provided by Vanderbilt
University (the developer of REDCap) and curated by the REDCap
consortium. Instruments in the library have been reviewed by a dedicated
committee before being made available. The library includes validated
clinical and research scales as well as community-contributed
instruments.

**Zip File (Instrument Export/Import)**

A file format used to export and import individual REDCap instruments. A
zip file captures the instrument\'s metadata — its variable
definitions, field types, labels, choices, and branching logic — but
not any data collected using that instrument. Zip files are
project-agnostic and can be imported into any REDCap project.

**Variable Name Collision**

A conflict that occurs when an imported instrument contains a variable
name that already exists in the destination project. REDCap detects
collisions automatically on import and prompts you to resolve them
before the import is completed.

**Instrument Name Collision**

A conflict that occurs when an imported instrument has the same internal
name (form\_name) as an existing instrument in the destination project.
REDCap handles this similarly to variable name collisions — it flags
the conflict and suggests an alternative name.

# 3. REDCap Instrument Library

## 3.1 What It Contains

- Validated clinical and research instruments (e.g., PHQ-9, GAD-7,
    PROMIS scales).

- Community-contributed instruments submitted by REDCap consortium
    members and approved by the curation committee.

- A mix of free and fee-based instruments. The library clearly
    indicates which instruments require a license or fee before import.

## 3.2 Accessing the Library

- From the Project Setup page or Designer page, click REDCap Shared
    Library in the Design Your Data Collection Instruments section.

- Alternatively, access it from the Online Designer via the shared
    library button.

- The library interface allows browsing and searching by instrument
    name, category, and keyword.

## 3.3 Importing from the Library

- Find the instrument you want. Review its description, field count,
    and licensing status.

- Click Import to begin. REDCap checks for variable and instrument
    name collisions before completing the import.

- After import, open the instrument in the Online Designer to review
    the variables and confirm nothing conflicts with your existing
    setup.

- If the imported instrument uses variable names that conflict with
    existing ones, REDCap will flag them. Resolve all conflicts before
    using the instrument.

## 3.4 Contributing to the Library

If you want to contribute one of your instruments to the shared global
library, contact your local REDCap support team. The submission process
involves committee review by the REDCap consortium before the instrument
is made publicly available.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** Always review imported instruments in the Online Designer after import. Variable names from the library may conflict with names already in your project, or the instrument\'s branching logic may reference variables that don\'t exist in your project context.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4. Zip File Feature

## 4.1 What Zip Files Contain

- The complete metadata of a single instrument: variable names, field
    types, field labels, choices, validation rules, branching logic, and
    field annotations.

- What zip files do NOT contain: any data collected using the
    instrument. Zip files are metadata-only.

## 4.2 Accessing Zip File Export and Import

- Zip file export and import are accessed from within the Online
    Designer — not from the Project Setup page directly.

- In the Online Designer\'s instrument list, each instrument has an
    Export as zip option.

- The import option (Upload a zip file) is also in the Online Designer
    instrument list.

## 4.3 Exporting an Instrument as a Zip File

- In the Online Designer, locate the instrument you want to export.

- Click the export/download option for that instrument and select zip
    file format.

- Save the file. The zip file contains the instrument definition only
    — no participant data.

- The exported zip file can be stored as a backup, shared with
    collaborators, or imported into another REDCap project.

## 4.4 Importing a Zip File

- In the Online Designer, click the Upload a zip file option.

- Select the zip file and upload it. REDCap automatically checks for
    variable and instrument name collisions.

- If collisions are found, REDCap suggests alternative names. You can
    accept the suggestions or modify them — as long as the proposed
    names do not themselves cause new collisions.

- Confirm the import. The new instrument appears in the Online
    Designer\'s instrument list.

- Review the imported instrument in the Online Designer to verify the
    import is correct.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Zip file import does not overwrite existing instruments — it adds the imported instrument as a new one. If you want to replace an existing instrument with a zip file version, you must delete the existing instrument first (only possible if it contains no data).
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5. Library vs. Zip File: When to Use Each

  -------------------- ------------------------------------------------- ----------------------------------------------------------
  **Factor**           **Instrument Library**                            **Zip File**
  Source               Centrally curated, Vanderbilt-hosted              Any REDCap user or project
  Curation             Committee-reviewed before publication             Not curated — quality varies
  Licensing            Some instruments require a fee                    No licensing constraints
  Use case             Validated clinical scales; community tools        Reusing your own instruments; sharing with collaborators
  Backup use           Not applicable                                    Yes — export for safekeeping
  Access point         Project Setup page or Online Designer             Online Designer only
  Collision handling   Automatic detection; must resolve before import   Automatic detection with suggested alternatives
  -------------------- ------------------------------------------------- ----------------------------------------------------------

# 6. Common Questions

**Q: Does importing from the Instrument Library add the instrument to my
project permanently?**

A: Yes. Once imported, the instrument is part of your project and can be
modified, deleted (if no data), or exported like any other instrument.
The library copy is unaffected.

**Q: Can I export an instrument that already has data collected in it?**

A: Yes. The zip file export captures the instrument\'s metadata only ---
it does not include any collected data. The export is safe to perform at
any time regardless of data collection status.

**Q: What should I do if REDCap flags a variable name collision during
import?**

A: Accept REDCap\'s suggested alternative name, or type your own
alternative — as long as it is unique across the project. After
import, update any branching logic or other references that used the
original variable name, since they will now reference the renamed
variable.

**Q: Can I share a zip file with someone at a different institution
using a different REDCap instance?**

A: Yes. Zip files are portable across REDCap instances as long as both
instances are running compatible REDCap versions. Variable name and
instrument name collisions are handled at import time by the destination
project.

**Q: Are copyrighted instruments from the library restricted in how I
can use them?**

A: Yes. Fee-based or copyrighted instruments in the library come with
license terms that govern their use. The library indicates which
instruments have licensing requirements. Do not import a fee-based
instrument without verifying your institution has the appropriate
license.

**Q: Can I contribute my instrument to the Instrument Library?**

A: Yes, through your local REDCap support team. The submission goes
through a committee review process before being published. Contact your
institution\'s REDCap administrator to start the process.

# 7. Common Mistakes & Gotchas

- Not reviewing imported instruments after import: variable name
    conflicts may have been silently renamed, or branching logic may
    reference variables that don\'t exist in your project. Always open
    the imported instrument in the Online Designer to verify it.

- Expecting zip file import to replace an existing instrument: zip
    imports add a new instrument — they do not overwrite an existing
    one. Delete the old instrument first if replacement is intended
    (only if no data has been collected).

- Importing a fee-based library instrument without a license: some
    instruments require your institution to hold a license. Using them
    without the appropriate license may have legal implications. Check
    the instrument\'s licensing status before importing.

- Losing the zip file and assuming the project is a backup: a zip file
    contains only the instrument metadata. Collected data is not
    included. Use the Data Dictionary download or a project snapshot for
    full backups.

- Overlooking that zip file features are in the Online Designer, not
    the Project Setup page: users often look for import/export on the
    setup page and miss it. The feature is accessed from within the
    Online Designer\'s instrument list.

# 8. Related Articles

- RC-FD-01 — Form Design Overview (prerequisite)

- RC-FD-02 — Online Designer (the access point for zip file import
    and export)

- RC-FD-03 — Data Dictionary (alternative approach for bulk
    instrument management)
