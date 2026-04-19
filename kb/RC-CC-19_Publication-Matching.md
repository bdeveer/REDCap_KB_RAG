RC-CC-19

**Control Center: Publication Matching**

| **Article ID** | RC-CC-19 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-21 — Control Center Overview; RC-CC-06 — Modules & Services Configuration; RC-PROJ-01 — Project Lifecycle |

---

**Publication Matching** (found at **Control Center → Miscellaneous Modules → Publication Matching**) is a module that automatically searches online publication databases to find publications associated with REDCap research projects. As of REDCap 16.x, the only supported database is **PubMed**.

When enabled, REDCap runs a nightly search using the Principal Investigators (PIs) and their affiliated institutions linked to each qualifying project. Potential matches are surfaced for administrator review, and optionally, PIs can be emailed about their matched publications.

---

# Eligibility Requirements

Not all projects participate in Publication Matching. A project must meet **both** of the following criteria:

1. **Project purpose is set to "Research"** — set in project settings at the project level
2. **Project is in Production status** — development-mode projects are excluded

Additionally, REDCap uses the **project's creation date** as the lower date boundary when searching for publications. The module assumes the project was created before any associated publication was submitted, so publications dated before the project creation date are excluded from search results.

---

# Principal Investigator (PI) Data

Each qualifying project should have PI information associated with it. The following fields are tracked per PI:

| Field | Notes |
| --- | --- |
| **Last name** | Required for a PI to be marked as "Ready" |
| **First name** | Required for a PI to be marked as "Ready" |
| **Middle initial** | Optional |
| **Alias** | Optional; use for alternative author name formats (e.g., maiden name, preferred abbreviation) |
| **Email** | Required (must be valid) for a PI to be marked as "Ready"; used for PI email notifications |

A PI is only included in nightly PubMed searches when their record is complete (last name, first name, and a valid email are all present). Incomplete records appear in the **To-Do List** tab.

---

# Module Tabs

The Publication Matching page is organized into five tabs:

## Setup

General configuration for the module. Key settings include:

- **Enable/disable Publication Matching** — toggles the entire module
- **P.I. Emailing** — controls whether PIs receive email notifications about matched publications. PIs are **not** emailed until this setting is explicitly enabled, even if the module is running

## To-Do List

Displays projects whose PI records are incomplete and therefore excluded from nightly searches. The count of items requiring attention is shown in parentheses next to the tab label (e.g., *To-Do List (349)*).

Administrators use this tab to:
- Identify which projects are missing PI data
- Fill in or correct PI information before the next nightly run
- Copy PI data from an existing PI record using the autocomplete search

## Manage Projects

Allows administrators to review and edit PI associations for individual projects. Provides:
- A project selector to navigate between qualifying projects
- PI name and contact fields, with validation highlighting for missing or malformed entries
- An autocomplete search field to copy data from an existing PI record to avoid re-entry

## P.I.-Pub Matches

Displays matched publications organized by PI. Use this tab to review which publications have been associated with specific investigators.

## Project-Pub Matches

Displays matched publications organized by REDCap project. Use this tab to review which publications have been associated with specific projects.

---

# Nightly Search Process

REDCap runs the PubMed search automatically each night. The search uses:
- The PI's last name and first name (and alias, if provided)
- The PI's affiliated institution (derived from the REDCap instance configuration)
- The project creation date as the earliest allowable publication date

Results are added to the P.I.-Pub Matches and Project-Pub Matches tabs for review. The module does not automatically confirm or reject matches — administrator review is always required.

---

# PI Email Notifications

When **P.I. Emailing** is enabled in the Setup tab, matched PIs receive email notifications about publications that REDCap has identified as potentially associated with their projects. Emails are sent from the REDCap system and include information about the matched publication for the PI to review.

> **Important:** PI emailing is disabled by default and must be explicitly turned on. Enabling it before PI records are complete and verified may result in incorrect or premature notifications.
