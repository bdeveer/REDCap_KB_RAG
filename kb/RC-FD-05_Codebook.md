RC-FD-05

**Codebook**

| **Article ID** | RC-FD-05 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-01 — Form Design Overview |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary |

# 1. Overview

The Codebook is a read-only, human-readable view of every instrument and
variable in a REDCap project. It provides a comprehensive, always
up-to-date reference of the project\'s structure without requiring the
user to navigate the Online Designer or parse a CSV file. This article
explains what the Codebook shows, where to find it, and when to use it.

# 2. Key Concepts & Definitions

**Codebook**

A project-level reference view that displays all instruments and their
variables in a structured, human-readable format. The Codebook always
reflects the current live state of the project. It is read-only — it
cannot be used to make changes to instruments or variables directly.

**Read-Only Reference Tool**

The Codebook is not a design tool. You cannot add, edit, delete, or
reorder instruments or variables from the Codebook view. Its purpose is
inspection and reference, not modification.

**Inline Edit Links**

Despite being read-only, the Codebook contains direct links that open
the edit interface for individual variables in the Online Designer, and
links that open the branching logic editor for specific variables. These
links are shortcuts — they take you to the appropriate design tool,
not to an editable state within the Codebook itself.

# 3. Accessing the Codebook

- From the Project Setup page: click Codebook in the Design Your Data
    Collection Instruments section.

- From the left-hand menu: click Codebook under the Data Collection
    section (available in both Development and Production modes).

- The Codebook opens to a full listing of all instruments and their
    variables, organized by instrument.

# 4. What the Codebook Shows

For each variable, the Codebook displays:

- Variable name (the internal REDCap identifier).

- Field label (the human-readable question or prompt shown to users).

- Field type (e.g., text, radio button, checkbox, dropdown, notes).

- Choices or options (for radio buttons, checkboxes, and dropdowns).

- Validation type and range (for text fields with validation).

- Branching logic (the condition under which the field is shown or
    hidden).

- Field annotations (\@Action Tags and other annotations applied to
    the field).

- Required status and identifier flag.

- Inline links to the Online Designer edit view and branching logic
    editor for that variable.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** The Codebook always reflects the currently applied state of the project. In Production mode, pending (unapproved) Online Designer changes are not shown — the Codebook shows only what is live.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5. When to Use the Codebook

The Codebook is the right tool in these situations:

- You need a reference while writing or debugging branching logic *---
    the Codebook lets you look up variable names and their choices
    without switching to the Online Designer or opening the Data
    Dictionary.*

- You want a human-readable overview of your entire project structure
    *--- the Codebook is easier to read than the raw Data Dictionary CSV
    and more navigable than the Online Designer for purely reviewing
    content.*

- You need to verify what choices are coded as in a radio or dropdown
    field *--- especially useful when writing branching logic or
    checking data export values.*

- You want to quickly navigate to a specific variable\'s edit
    interface *--- use the inline edit link rather than scrolling
    through the Online Designer.*

- You are onboarding to a project you didn\'t design *--- the Codebook
    gives a rapid, readable summary of what the project collects and how
    it is structured.*

# 6. Codebook vs. Other Reference Options

  ---------------------------------- ----------------------------------------- ------------------------------- ------------------------------------------------------------------
  **Reference Tool**                 **Format**                                **Editable?**                   **Best For**
  Codebook                           Web view, organized by instrument         No (links to editors)           Human-readable review; looking up variable names while designing
  Data Dictionary (downloaded CSV)   Spreadsheet                               Yes (upload to apply changes)   Bulk editing; offline reference; version control
  Download PDF of All Instruments    PDF                                       No                              Documentation; IRB submissions; stakeholder review
  Online Designer                    Web interface, one instrument at a time   Yes                             Making edits; previewing form appearance
  ---------------------------------- ----------------------------------------- ------------------------------- ------------------------------------------------------------------

# 7. Common Questions

**Q: Can I edit variables directly from the Codebook?**

A: No. The Codebook is read-only. It contains inline links that open the
Online Designer\'s edit interface or branching logic editor for
individual variables, but the editing itself happens in those tools ---
not in the Codebook.

**Q: Does the Codebook update in real time as I make changes?**

A: Yes, for applied changes. In Development mode, changes made in the
Online Designer or via Data Dictionary upload are reflected immediately.
In Production mode, pending (unapproved) changes are not shown — the
Codebook reflects only the live project state.

**Q: Is the Codebook the same as the Data Dictionary?**

A: No. The Data Dictionary is a CSV file that defines your project\'s
variables and can be uploaded to modify them. The Codebook is a
read-only web view of the same information in a more readable format.
They present similar content but serve entirely different purposes.

**Q: Can I export the Codebook as a file?**

A: Not directly as a Codebook export. For a portable version of your
project\'s variable definitions, use Download the current Data
Dictionary (CSV) or Download PDF of All Instruments, both available from
the Design Your Data Collection Instruments section.

**Q: I\'m new to a project and need to understand its structure quickly.
Is the Codebook the best starting point?**

A: Yes. The Codebook gives you a structured, human-readable view of all
instruments and variables without requiring you to interpret a CSV or
navigate the Online Designer instrument by instrument. It\'s the fastest
way to understand what a project collects and how it is organized.

# 8. Common Mistakes & Gotchas

- Expecting to edit from the Codebook: the Codebook is read-only. Use
    the inline links to jump to the Online Designer if you need to make
    a change, but the edit happens there.

- Treating the Codebook as an export: the Codebook is a live web view,
    not a downloadable file. Use the Data Dictionary download or the PDF
    export for portable versions of your project structure.

- Relying on the Codebook in Production when changes are pending: the
    Codebook only reflects the live, approved project state. Pending
    Online Designer changes in Production are not visible until
    approved. If you recently made a change and don\'t see it in the
    Codebook, check whether it is still in the approval queue.

- Overlooking the inline edit links: the Codebook\'s inline links to
    the Online Designer and branching logic editor are easy to miss but
    save significant time. They let you jump directly to a specific
    variable\'s edit interface without scrolling through the full Online
    Designer.

# 9. Related Articles

- RC-FD-01 — Form Design Overview (prerequisite)

- RC-FD-02 — Online Designer (the editing tool linked from the
    Codebook\'s inline edit links)

- RC-FD-03 — Data Dictionary (the CSV-format alternative reference
    and design tool)
