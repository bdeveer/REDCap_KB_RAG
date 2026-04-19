RC-FD-01

**Form Design Overview**

| **Article ID** | RC-FD-01 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | User is logged in and has Project Design and Setup rights |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary; RC-FD-04 — Instrument Library & Zip Files; RC-FD-05 — Codebook |

# 1. Overview

This article orients users to REDCap\'s instrument design area. It
explains what an instrument is, describes the three primary design
tools, and covers the supporting features in the Design Your Data
Collection Instruments section. It is the entry point for the Form
Design knowledge base series.

# 2. Key Concepts & Definitions

**Instrument**

The primary term in REDCap for any data collection form, survey, or
grouping of variables. REDCap uses \'instrument\' consistently across
its interface. The terms form, survey, and instrument are often used
interchangeably in practice, but instrument is the canonical REDCap term
and is used throughout this knowledge base series to prevent confusion.

**Variable**

A single data-collection field within an instrument. Each variable has a
unique name (variable name), a field type, and optional attributes such
as validation rules, branching logic, and field labels. Variable names
are REDCap\'s internal identifiers and appear in data exports.

**Project Setup Page**

The landing page for projects in Development mode. It provides
structured access to all configuration areas, including the instrument
design section. Projects in Production mode open on the Project Home
page instead, but the design area remains accessible from the left-hand
menu.

**Development Mode vs. Production Mode**

REDCap projects exist in one of two states. In Development mode, all
design changes take effect immediately and no approval is required. In
Production mode, design changes made in the Online Designer are queued
for review before being applied — either automatically by REDCap or
after administrator approval, depending on local policy.

# 3. Navigating to the Instrument Design Area

## 3.1 From the Project Setup Page (Development Mode)

- Log in and open your project from the My Projects page.

- If the project is in Development mode, it opens directly on the
    Project Setup page.

- Locate the Design Your Data Collection Instruments section — it is
    prominently displayed in the setup workflow.

## 3.2 From the Project Home Page (Production Mode or Alternate Path)

- If the project is in Production mode, it opens on the Project Home
    page.

- In the left-hand menu, click Designer under the Data Collection
    section to reach the instrument design area.

- The same Design Your Data Collection Instruments section is
    available from both entry points.

# 4. The Three Main Instrument Design Tools

The Design Your Data Collection Instruments section surfaces three
distinct tools for creating and modifying instruments. Each serves
different use cases and skill levels. Dedicated articles in this series
cover each tool in detail.

  --------------------------- ----------------------------------------------------------------------------------------- -------------
  **Tool**                    **Best For**                                                                              **Article**
  Online Designer             Beginners; making a small number of changes; wanting immediate visual feedback            RC-FD-02
  Data Dictionary             Advanced users; defining many variables at once; splitting or restructuring instruments   RC-FD-03
  REDCap Instrument Library   Importing validated or community-contributed instruments (e.g., PHQ-9)                    RC-FD-04
  --------------------------- ----------------------------------------------------------------------------------------- -------------

# 5. Supporting Features in the Design Area

## 5.1 Download PDF of All Instruments

Generates a PDF document containing the definitions of every variable
across all instruments in the project. Useful for documentation, IRB
submissions, and offline review of your project\'s structure.

## 5.2 Download the Current Data Dictionary

Downloads the project\'s current instrument and variable definitions as
a CSV file. This is the same format used by the Data Dictionary upload
tool (RC-FD-03). Downloading the current Data Dictionary before making
bulk changes is a critical safety practice — it serves as a snapshot
that can be re-uploaded to undo a bad import.

## 5.3 Check for Identifiers

Opens a page that lets you review all variables in the project and
designate which ones are identifiers (e.g., name, date of birth, medical
record number). Identifier flags control how data is handled in exports
and reports. Individual variables can also be flagged as identifiers
within the Online Designer.

## 5.4 Zip File Upload and Download

Instruments can be exported as zip files and re-imported into the same
or a different REDCap project. This feature is accessed from within the
Online Designer. See RC-FD-04 for full details.

## 5.5 Codebook

A read-only, human-readable summary of all instruments and variables in
the project. Useful as a reference while designing instruments or
writing logic. Accessible from the left-hand menu. See RC-FD-05 for full
details.

## 5.6 Project Setup Progress Indicators

The Design Your Data Collection Instruments section includes a \'Not
Started\' status indicator and an \'I\'m done!\' button. These are
visual progress trackers for the project setup workflow only — they
have no functional effect on the project and do not lock or unlock any
features.

## 5.7 Advanced Feature Reference Buttons

Five buttons at the bottom of the design section link to REDCap\'s
built-in reference guides for advanced features: Smart Variables,
Piping, \@Action Tags, Field Embedding, and Special Functions. These
features extend what instruments can do but require a solid grasp of
basic instrument design before use. This knowledge base series does not
cover them in depth.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** The text and layout of the Design Your Data Collection Instruments section may vary slightly depending on which project features are enabled (e.g., Surveys mode). The core tools and links described here are present in all configurations.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 6. Choosing the Right Tool

Use this guide to select the appropriate tool for your task. For full
details on each tool, see the linked articles.

  ----------------------------------------------------------------------- -------------------------------------------------------------
  **Task**                                                                **Recommended Tool**
  Create your first instrument or add a few fields                        Online Designer (RC-FD-02)
  Build or restructure many variables or instruments at once              Data Dictionary (RC-FD-03)
  Split one instrument into two                                           Data Dictionary (RC-FD-03)
  Import a validated clinical scale (e.g., PHQ-9, GAD-7)                  Instrument Library (RC-FD-04)
  Reuse an instrument from another project                                Zip File import (RC-FD-04)
  Back up your instrument definitions before a major change               Download Data Dictionary or Zip File export (RC-FD-04)
  Review all variables and their attributes in a readable format          Codebook (RC-FD-05)
  Check or update which variables are flagged as identifiers              Check for Identifiers (this article, Section 5.3)
  Generate a PDF of all instruments for documentation or IRB submission   Download PDF of All Instruments (this article, Section 5.1)
  ----------------------------------------------------------------------- -------------------------------------------------------------

# 7. Common Questions

**Q: What is the difference between an instrument, a form, and a survey
in REDCap?**

A: They refer to the same structural object. REDCap uses \'instrument\'
as the canonical term. A form is an instrument used for staff data
entry. A survey is the same instrument configured to be filled out by a
participant. The underlying data structure is identical.

**Q: I made a change in the Online Designer but it hasn\'t appeared in
my project yet. Why?**

A: Your project is likely in Production mode. In Production, Online
Designer changes are queued for review before being applied. Depending
on your institution\'s REDCap policy, the review may be automatic or may
require administrator approval. Check with your local REDCap support
team.

**Q: Can I undo a change I made to an instrument?**

A: Not through an undo button. The safest recovery path is to download
the Data Dictionary before making significant changes — this gives you
a snapshot you can re-upload to restore the previous state. For
Production projects, pending changes can be cancelled before they are
approved.

**Q: Where do I find the Online Designer if my project is already in
Production?**

A: In Production mode, the project opens on the Project Home page. Click
Designer in the left-hand menu under Data Collection to reach the
instrument design area, which includes access to the Online Designer.

**Q: Do the \'Not Started\' and \'I\'m done!\' status indicators affect
my project?**

A: No. They are visual progress indicators for the project setup
workflow only. Marking a step as done or not done has no functional
effect on any REDCap feature.

**Q: Are the advanced feature buttons (Smart Variables, Piping, \@Action
Tags, etc.) tools or links?**

A: They are links to built-in REDCap reference guides, not tools
themselves. They open documentation pages within REDCap. The features
they describe — piping values into fields, conditional action tags,
etc. — are applied within the Online Designer or Data Dictionary, not
through those buttons directly.

# 8. Common Mistakes & Gotchas

- Making changes in Production without expecting a review step: design
    changes in Production mode are not applied immediately. If your
    changes aren\'t showing up, check whether they are pending review in
    the Online Designer\'s change queue.

- Using \'form\' and \'survey\' and \'instrument\' interchangeably in
    logic and variable names: REDCap treats these as one object type.
    Using inconsistent terminology in documentation or training creates
    confusion. Standardize on \'instrument\' throughout.

- Skipping the Data Dictionary download before making bulk changes:
    downloading the current Data Dictionary before a major edit is the
    only reliable way to recover from a bad import. Build this habit
    before every bulk change.

- Assuming the advanced feature buttons open tools: they open
    reference documentation, not editors. The actual features (Piping,
    \@Action Tags, etc.) are configured within the Online Designer or
    Data Dictionary.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-07 — Export Metadata (Data Dictionary) API** — retrieve the full project data dictionary programmatically
- **RC-API-08 — Import Metadata (Data Dictionary) API** — push a new or updated data dictionary to a project programmatically
- **RC-API-09 — Export Instruments API** — retrieve the list of instruments (forms) in a project programmatically

---


# 9. Related Articles

- RC-FD-02 — Online Designer

- RC-FD-03 — Data Dictionary

- RC-FD-04 — Instrument Library & Zip Files

- RC-FD-05 — Codebook
