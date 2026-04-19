RC-NAV-REC-01

**Record Navigation Overview**

| **Article ID** | RC-NAV-REC-01 |
| --- | --- |
| **Domain** | Navigation |
| **Applies To** | All REDCap project types |
| **Prerequisite** | User is logged into a REDCap instance |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | See KB-SOURCE-ATTESTATION.md |

# 1. Overview

This article explains how to navigate to records and locate data within
a REDCap project. It covers the primary navigation paths available to
any REDCap user and explains how to interpret instrument status
indicators (colored dots).

# 2. Key Concepts & Definitions

**Record**

The fundamental unit of data in REDCap. Each record corresponds to one
participant, patient, or subject. Every record has a Record ID — the
primary identifier used throughout the system.

**Instrument**

A data-entry form within a REDCap project. Instruments contain fields
(variables) where data is entered. Each instrument has a status dot that
reflects its completion state.

**Record Home Page**

A per-record landing page that displays all instruments associated with
that record. It is the central hub for viewing and navigating to any
instrument for a single record.

**Record Status Dashboard**

A project-level view displaying all records and their instrument
statuses in a grid. Useful for monitoring progress across an entire
study.

**Add/Edit Records Page**

A data-collection menu page that provides lookup tools for finding and
opening individual records.

# 3. Step-by-Step: Primary Navigation Paths

## 3.1 Navigating to a Project

- Log in to your REDCap instance.

- On the My Projects page, click the name of the project you want to
    open.

- You are now on the project home page, with the left-hand menu
    available.

## 3.2 Add/Edit Records (Quickest Path to a Single Record)

- In the left-hand menu, find the Data Collection section and click
    Add / Edit Records.

- To find a record by ID: use the Choose an existing record dropdown
    — it lists all record IDs in the project.

- To search by value: use the Data Search feature.

- Search across all variables — useful when you only know a value
    but not which field contains it.

- Search within a specific variable — faster in large projects
    (e.g., search only the Date of Birth field).

- Selecting a result takes you directly to the Record Home Page or to
    the specific instrument where the value was found.

## 3.3 Record Status Dashboard

- In the left-hand menu, click Record Status Dashboard under Data
    Collection.

- The default dashboard shows all records, events, and instruments you
    have access to.

- Click any colored dot to open the corresponding instrument for that
    record.

## 3.4 Reports

- In the left-hand menu, click Data Exports, Reports, and Stats, then
    select a report.

- Any Record ID displayed in a report is a clickable link that opens
    the Record Home Page for that record.

## 3.5 Using the Record Home Page

- Once on the Record Home Page, you see all instruments for that
    record displayed as colored dots.

- Click any dot to open the corresponding instrument.

- After opening an instrument, the left-hand menu displays a list of
    all instruments for quick switching.

# 4. Instrument Status Dot Colors

Every instrument in REDCap is represented by a colored dot. The color
encodes the completion status of that instrument for a given record.

  ----------------------------- -----------------------------------------------------------------------------------------------------------------------
  **Dot Appearance**            **Meaning**
  Grey                          Incomplete — no data has been entered. This is the default state.
  Red                           Data has been saved, but the Form Status field is still set to Incomplete.
  Yellow                        Form Status field is set to Unverified by a user.
  Green                         Form Status field is set to Complete by a user.
  Orange with white checkmark   The instrument was opened as a survey but only partially completed (e.g., participant closed the browser mid-survey).
  Green with white checkmark    The instrument was completed in full as a survey.
  ----------------------------- -----------------------------------------------------------------------------------------------------------------------

**Important distinctions:**

- REDCap automatically enforces grey (no data) and red (data present,
    incomplete) statuses.

- Yellow and green statuses are set manually by the study team ---
    they are optional but recommended for projects with many
    instruments.

- Survey statuses (orange and green with checkmarks) are set
    automatically when a survey is submitted or partially completed.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Technical Note:** Instrument status values are stored as part of the project dataset and can be manipulated in bulk via data import. Grey and red are both coded as 0; yellow = 1; green = 2. Survey statuses (orange checkmark = 1, green checkmark = 2) only appear when the instrument is used as a survey.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5. Common Questions

**Q: What is the fastest way to find a specific record in a large
project?**

A: Use Add/Edit Records and the Data Search feature. Searching within a
specific variable (such as Record ID or email) is faster than searching
across all variables.

**Q: Can I navigate to an instrument directly without going through the
Record Home Page?**

A: Yes. Clicking any colored dot in the Record Status Dashboard or in a
report takes you directly to the corresponding instrument without
visiting the Record Home Page first.

**Q: What does a red dot mean — is something wrong?**

A: No. A red dot simply means data has been entered but the Form Status
field has not been changed from its default value of Incomplete. It does
not indicate an error.

**Q: Can I change instrument statuses for many records at once?**

A: Yes. Instrument statuses are stored in the dataset and can be set in
bulk using REDCap\'s data import tools. Use coded values: 0 =
incomplete, 1 = unverified, 2 = complete.

**Q: What happens to the dot color if I enter a single data point but
leave everything else blank?**

A: The dot turns red. Any data saved to an instrument — even a single
field — changes the dot from grey to red.

# 6. Common Mistakes & Gotchas

- Confusing grey and red: grey means no data at all; red means data is
    present but the form status has not been updated. They are both
    coded as 0 in the dataset, but have different visual meanings.

- Ignoring optional statuses: teams that skip yellow/green statuses on
    large projects often lose track of which instruments have been
    reviewed vs. just filled in.

- Searching all variables in a large project: this can be slow. Always
    prefer variable-specific search when you know which field to look
    in.

- Expecting survey statuses on non-survey instruments: orange and
    green-checkmark dots only appear on instruments that are enabled as
    surveys.

# 7. Related Articles

- RC-NAV-REC-02 — Longitudinal Mode & Arms

- RC-NAV-REC-03 — Repeated Instruments & Repeated Events

- RC-NAV-REC-04 — Record Status Dashboard & Other Record Links
