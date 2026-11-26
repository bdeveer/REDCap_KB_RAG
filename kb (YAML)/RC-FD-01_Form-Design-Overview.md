---
id: RC-FD-01
title: Form Design Overview
domain: Form Design
applies_to:
- All REDCap project types
- the Project Design and Setup right is needed for Project Setup, the Online Designer,
  the Data Dictionary, instrument zip files and Check for Identifiers (the Codebook
  and the PDF of instruments are available to all project users)
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — design
  area navigation and tools checked against source code; pages not re-captured
prerequisites:
- User is logged in to the project. Project Design and Setup rights are needed to
  change instruments
- the Codebook and the PDF of instruments need no design rights
version: '1.1'
last_updated: 2026-11
related:
- id: RC-FD-02
  title: Online Designer
- id: RC-FD-03
  title: Data Dictionary
- id: RC-FD-04
  title: Instrument Library & Zip Files
- id: RC-FD-05
  title: Codebook
- id: RC-NAV-UI-01
  title: Project Navigation UI
- id: RC-NAV-UI-02
  title: Project Menu Reference
tags:
- form design
- instruments
synonyms:
- how do i design forms in redcap
- where do i build instruments
- intro to form and instrument design
- what is an instrument in redcap
- tools for designing data collection forms
- getting started with form design
- design your data collection instruments area
- online designer vs data dictionary vs codebook
---

# 1. Overview

This article orients users to REDCap's instrument design area. It
explains what an instrument is, describes the three primary design
tools, and covers the supporting features in the Design Your Data
Collection Instruments section. It is the entry point for the Form
Design knowledge base series.

---

# 2. Key Concepts & Definitions

**Instrument**

The primary term in REDCap for any data collection form, survey, or
grouping of variables. REDCap uses 'instrument' consistently across
its interface. The terms form, survey, and instrument are often used
interchangeably in practice, but instrument is the canonical REDCap term
and is used throughout this knowledge base series to prevent confusion.

**Variable**

A single data-collection field within an instrument. Each variable has a
unique name (variable name), a field type, and optional attributes such
as validation rules, branching logic, and field labels. Variable names
are REDCap's internal identifiers and appear in data exports.

**Project Setup Page**

The landing page for projects in Development mode. It provides
structured access to all configuration areas, including the instrument
design section. Projects in Production mode open on the Project Home
page instead, but the Project Setup page is still reachable through the
**Setup** link in the left-hand menu.

**Development Mode vs. Production Mode**

These are the two project statuses that matter for design work (a third,
Analysis/Cleanup, is for projects that have finished data collection;
see [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)).
In Development mode, all design changes take effect immediately and no
approval is required. In Production mode, you must first enter **Draft
Mode**, make your changes (in the Online Designer or by Data Dictionary
upload), and then submit them for review. Submitted changes are either
approved automatically by REDCap or held for administrator approval.

> **Institution-specific:** Whether production changes can be approved
> automatically is set by your REDCap administrators. They choose the
> rules, for example based on whether the project has records, whether
> fields that hold data are being deleted, or whether REDCap flags
> critical issues. Some installations also stop automatic approval when
> a newly added field looks like an identifier but is not flagged as
> one. Check with your REDCap administrators for the local policy.

---

# 3. Navigating to the Instrument Design Area

## 3.1 From the Project Setup Page (Development Mode)

- Log in and open your project from the My Projects page.

- If the project is in Development mode, it opens directly on the
    Project Setup page.

- Locate the Design Your Data Collection Instruments section — it is
    prominently displayed in the setup workflow.

## 3.2 From the Left-Hand Menu (Production Mode or Alternate Path)

- If the project is in Production mode, it opens on the Project Home
    page.

- In the left-hand menu, find the **Project Home and Design** panel.
    It holds the links **Home**, **Setup** and **Codebook** on one line
    and **Designer** and **Dictionary** on the next.

- **Designer** opens the Online Designer directly. **Dictionary** opens
    the Data Dictionary upload page. **Setup** opens the Project Setup
    page, where the Design Your Data Collection Instruments section is
    available in every project status.

- Users without Project Design and Setup rights see only **Home** and
    **Codebook** in this panel.

---

# 4. The Three Main Instrument Design Tools

The Design Your Data Collection Instruments section surfaces three
distinct tools for creating and modifying instruments. Each serves
different use cases and skill levels. Dedicated articles in this series
cover each tool in detail.

| **Tool** | **Best For** | **Article** |
| --- | --- | --- |
| Online Designer | Beginners; making a small number of changes; wanting immediate visual feedback | [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) |
| Data Dictionary | Advanced users; defining many variables at once; splitting or restructuring instruments | [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) |
| REDCap Instrument Library | Importing validated or community-contributed instruments (e.g., PHQ-9) | [RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md) |

> **Note:** The Instrument Library button appears only if your REDCap
> administrators have enabled the library on your installation.

---

# 5. Supporting Features in the Design Area

## 5.1 Download PDF of All Instruments

Generates a PDF of every instrument in the project as blank forms, laid
out much as they appear during data entry. Useful for documentation,
IRB submissions, and offline review of your project's structure. The
same PDF is available from the **PDF (all instruments)** option in the
Online Designer, and any project user can download it without design
rights.

## 5.2 Download the Current Data Dictionary

Downloads the project's current instrument and variable definitions as
a CSV file. This is the same format used by the Data Dictionary upload
tool ([RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)). The
file uses the CSV delimiter set in your user profile preferences. While
a production project is in Draft Mode, a second link, **Download Data
Dictionary with drafted changes**, gives you the draft version.

Downloading the current Data Dictionary before every upload or bulk
change is best practice: it gives you a copy you control that can be
re-uploaded to undo a bad import. REDCap also keeps its own safety net.
It saves a Data Dictionary snapshot automatically each time a Data
Dictionary upload is committed, and you can take a manual snapshot at
any time. Snapshots are listed and downloadable on the **Project
Revision History** page, which in production also lists every approved
revision of the design.

## 5.3 Check for Identifiers

Opens a page for reviewing and setting identifier flags. It does not
list every variable. It shows only likely identifiers: variables whose
name or label matches common identifier keywords (e.g., name, date of
birth, medical record number), variables already flagged as
identifiers, and text fields validated as a date, phone number, email
address or zip code. Identifier flags control how data is handled in
exports and reports. Any variable can also be flagged as an identifier
within the Online Designer.

In production, this page is available only while the project is in
Draft Mode, and changes you make here go into the draft like any other
design change. A newly added field that looks like an identifier but is
not flagged can stop the draft from being approved automatically on
installations that use that check.

## 5.4 Zip File Upload and Download

Instruments can be exported as zip files and re-imported into the same
or a different REDCap project. Both are in the Online Designer: download
an instrument zip from the instrument's **Choose action** menu, and
upload one with the import button above the instrument list. See [RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md) for full details.

> **Version caveat (v17.3 LTS and v17.6 Standard):** On v17.3 and v17.6 the Codebook
> also shows a **Download instrument ZIP** icon next to each instrument
> for users with design rights. It is absent on v16.0.61 LTS. On any
> version, use the Online Designer's **Choose action** menu, which works
> everywhere.

## 5.5 Codebook

A read-only, human-readable summary of all instruments and variables in
the project. Useful as a reference while designing instruments or
writing logic. Open it from the **Codebook** link in the **Project Home
and Design** panel of the left-hand menu; all project users can view it,
with or without design rights. See [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) for full
details.

## 5.6 Project Setup Progress Indicators

Each step in the Design Your Data Collection Instruments section shows
a status of **Not started**, **In progress** or **Complete!**, and an
**I'm done!** button that only users with Project Design and Setup
rights see. These are visual progress trackers for the project setup
workflow only — ticking a step as done has no functional effect on the
project and does not lock or unlock any features.

## 5.7 Advanced Feature Reference Buttons

Five **Learn how to use** buttons at the bottom of the design section
open pop-up reference guides for advanced features: Smart Variables,
Piping, \@Action Tags, Field Embedding, and Special Functions. These
features extend what instruments can do but require a solid grasp of
basic instrument design before use. This knowledge base series does not
cover them in depth.

## 5.8 Who Can Use What

| **Feature** | **Who can use it** |
| --- | --- |
| Project Setup page, Online Designer, Data Dictionary, instrument zip files, Check for Identifiers | Users with Project Design and Setup rights |
| Codebook, PDF of all instruments | All project users |
| Instrument Library | Users with design rights, once an administrator has enabled the library |


> **Note:** Not every tool appears in every project. The text and layout of the Design Your Data Collection Instruments section vary with the project features enabled (e.g., Surveys mode). The Instrument Library button needs administrator enablement. In production, the Instrument Library and Check for Identifiers are hidden, and the Online Designer's instrument-level actions are unavailable, until you enter Draft Mode.


---

# 6. Choosing the Right Tool

Use this guide to select the appropriate tool for your task. For full
details on each tool, see the linked articles.

| **Task** | **Recommended Tool** |
| --- | --- |
| Create your first instrument or add a few fields | Online Designer ([RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)) |
| Build or restructure many variables or instruments at once | Data Dictionary ([RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)) |
| Split one instrument into two | Data Dictionary ([RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)) |
| Import a validated clinical scale (e.g., PHQ-9, GAD-7) | Instrument Library ([RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md)) |
| Reuse an instrument from another project | Zip File import ([RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md)) |
| Back up your instrument definitions before a major change | Download Data Dictionary or Zip File export ([RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md)) |
| Review all variables and their attributes in a readable format | Codebook ([RC-FD-05 — Codebook](RC-FD-05_Codebook.md)) |
| Check or update which variables are flagged as identifiers | Check for Identifiers (this article, Section 5.3) |
| Generate a PDF of all instruments for documentation or IRB submission | Download PDF of All Instruments (this article, Section 5.1) |

---

# 7. Common Questions

**Q: What is the difference between an instrument, a form, and a survey
in REDCap?**

**A:** They refer to the same structural object. REDCap uses 'instrument'
as the canonical term. A form is an instrument used for staff data
entry. A survey is the same instrument configured to be filled out by a
participant. The underlying data structure is identical.

**Q: I made a change in the Online Designer but it hasn't appeared in
my project yet. Why?**

**A:** Your project is likely in Production mode. There, changes are made
in Draft Mode and only take effect once you submit them and they are
approved. Depending on the rules your REDCap administrators have set,
approval may be automatic or may need an administrator, for example
when fields with data are deleted or a new field looks like an
unflagged identifier. Check whether you still need to submit the draft,
and check with your local REDCap support team about review times.

**Q: Can I undo a change I made to an instrument?**

**A:** Not through an undo button. Best practice is to download the Data
Dictionary before making significant changes — this gives you a copy
you can re-upload to restore the previous state. REDCap also saves a
snapshot automatically each time a Data Dictionary upload is committed;
you can download these, and in production every approved revision,
from **Project Revision History**. For Production projects, you can
discard drafted changes yourself only before you submit them; after
submission, only a REDCap administrator can reject or reset them.

**Q: Where do I find the Online Designer if my project is already in
Production?**

**A:** In Production mode, the project opens on the Project Home page. Click
**Designer** in the **Project Home and Design** panel of the left-hand
menu to open the Online Designer directly. You need Project Design and
Setup rights, and you must enter Draft Mode before you can change
instruments.

**Q: Do the 'Not started' and 'I'm done!' status indicators affect
my project?**

**A:** No. They are visual progress indicators for the project setup
workflow only. Marking a step as done or not done has no functional
effect on any REDCap feature.

**Q: Are the advanced feature buttons (Smart Variables, Piping, \@Action
Tags, etc.) tools or links?**

**A:** They are **Learn how to use** buttons that open pop-up reference
guides within REDCap, not tools themselves. The features they describe
— piping values into fields, conditional action tags, etc. — are
applied within the Online Designer or Data Dictionary, not through
those buttons directly.

---

# 8. Common Mistakes & Gotchas

- **Making changes in Production without expecting a review step.** Design
    changes in Production mode are made in Draft Mode and are not
    applied until you submit them and they are approved. If your changes
    aren't showing up, check whether the draft has been submitted and is
    still awaiting review. Data Dictionary uploads in production also
    need Draft Mode.

- **Using inconsistent terminology (form, survey, instrument).** REDCap treats these as one object type.
    Using inconsistent terminology in documentation or training creates
    confusion. Standardize on 'instrument' throughout.

- **Skipping the Data Dictionary download before making bulk changes.** Downloading the current Data Dictionary before every upload is the
    simplest, most reliable way to recover from a bad import. REDCap's
    automatic snapshots on **Project Revision History** are a backup,
    not a substitute for this habit.

- **Confusing advanced feature buttons with tools.** They open
    reference pop-ups, not editors. The actual features (Piping,
    \@Action Tags, etc.) are configured within the Online Designer or
    Data Dictionary.

- **Expecting Check for Identifiers to list every variable.** It shows
    only likely identifiers. Flag any other sensitive variable in the
    Online Designer or the Data Dictionary.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)** — retrieve the full project data dictionary programmatically
- **[RC-API-08 — Import Metadata (Data Dictionary) API](RC-API-08_Import-Metadata.md)** — push a new or updated data dictionary to a project programmatically; works only while the project is in Development mode
- **[RC-API-09 — Export Instruments API](RC-API-09_Export-Instruments.md)** — retrieve the list of instruments (forms) in a project programmatically
- **[RC-API-15 — Export Instruments PDF API](RC-API-15_Export-Instruments-PDF.md)** — download the PDF of one or all instruments programmatically

---


# 9. Related Articles

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)

- [RC-FD-04 — Instrument Library & Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md)

- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md)

- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) (Draft Mode and production change review)

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (the Designer, Dictionary, and Codebook links are in the Project Home and Design menu section)

- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (full reference for the Project Home and Design menu items that lead to these form design tools)
