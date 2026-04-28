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

# 1. Overview

Publication Matching helps research institutions track and document scholarly output from REDCap projects by automatically discovering publications associated with project Principal Investigators. The system scans PubMed nightly, identifies potential matches, and can notify investigators about publications linked to their research. This is particularly useful for institutions that need to report research productivity or maintain publication records for regulatory and grant compliance purposes.

---

# 2. Eligibility Requirements

Not all projects participate in Publication Matching. A project must meet **both** of the following criteria:

1. **Project purpose is set to "Research"** — set in project settings at the project level
2. **Project is in Production status** — development-mode projects are excluded

Additionally, REDCap uses the **project's creation date** as the lower date boundary when searching for publications. The module assumes the project was created before any associated publication was submitted, so publications dated before the project creation date are excluded from search results.

---

# 3. Principal Investigator (PI) Data

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

# 4. Module Tabs

The Publication Matching page is organized into five tabs:

## 4.1 Setup

General configuration for the module. Key settings include:

- **Enable/disable Publication Matching** — toggles the entire module
- **P.I. Emailing** — controls whether PIs receive email notifications about matched publications. PIs are **not** emailed until this setting is explicitly enabled, even if the module is running

## 4.2 To-Do List

Displays projects whose PI records are incomplete and therefore excluded from nightly searches. The count of items requiring attention is shown in parentheses next to the tab label (e.g., *To-Do List (349)*).

Administrators use this tab to:
- Identify which projects are missing PI data
- Fill in or correct PI information before the next nightly run
- Copy PI data from an existing PI record using the autocomplete search

## 4.3 Manage Projects

Allows administrators to review and edit PI associations for individual projects. Provides:
- A project selector to navigate between qualifying projects
- PI name and contact fields, with validation highlighting for missing or malformed entries
- An autocomplete search field to copy data from an existing PI record to avoid re-entry

## 4.4 P.I.-Pub Matches

Displays matched publications organized by PI. Use this tab to review which publications have been associated with specific investigators.

## 4.5 Project-Pub Matches

Displays matched publications organized by REDCap project. Use this tab to review which publications have been associated with specific projects.

---

# 5. Nightly Search Process

REDCap runs the PubMed search automatically each night. The search uses:
- The PI's last name and first name (and alias, if provided)
- The PI's affiliated institution (derived from the REDCap instance configuration)
- The project creation date as the earliest allowable publication date

Results are added to the P.I.-Pub Matches and Project-Pub Matches tabs for review. The module does not automatically confirm or reject matches — administrator review is always required.

---

# 6. PI Email Notifications

When **P.I. Emailing** is enabled in the Setup tab, matched PIs receive email notifications about publications that REDCap has identified as potentially associated with their projects. Emails are sent from the REDCap system and include information about the matched publication for the PI to review.

> **Important:** PI emailing is disabled by default and must be explicitly turned on. Enabling it before PI records are complete and verified may result in incorrect or premature notifications.

---

# 7. Common Questions

**Q: Why do some of my research projects not appear in the Publication Matching module?**
Projects must meet two eligibility criteria: (1) the project's purpose must be set to "Research" in project settings, and (2) the project must be in Production status. Development-mode projects and projects with other purposes (e.g., QA, Training) are excluded. Check each project's settings to confirm it meets both requirements.

**Q: Does the search use the date the project was created?**
Yes. The project creation date is used as the lower boundary for the publication search. REDCap assumes that publications associated with a project could not have been submitted or published before the project existed. Publications dated earlier than the project creation date are excluded from results.

**Q: Can the system search for publications by multiple Principal Investigators?**
Yes. Each project can have multiple PIs associated with it. The nightly search uses the name and institution of each PI to look for matching publications in PubMed. Each PI record must have a first name, last name, and valid email address to be included in the search.

**Q: What happens if a PI's name is very common (like "John Smith")?**
Publication Matching uses the PI's name and affiliated institution to narrow results. The institution affiliation helps filter for the correct person. However, very common names may still return false positives (publications by a different "John Smith"). Always review matched publications to confirm they are actually associated with the correct investigator.

**Q: Can I manually review and reject publication matches before they are shown to PIs?**
Yes. All matched publications are surfaced for administrator review in the P.I.-Pub Matches and Project-Pub Matches tabs. Administrator review is always required before matches are considered confirmed. You can review, accept, or discard matches. Matches are not automatically sent to PIs — you control which ones are communicated via email.

---

# 8. Common Mistakes & Gotchas

**Enabling PI emailing before completing PI records.** PI emailing is disabled by default. If you enable it before ensuring that all PI records are complete (first name, last name, valid email), PIs may receive emails with incomplete or incorrect information about publication matches. Always complete and verify PI data in the To-Do List and Manage Projects tabs before enabling PI emailing.

**Assuming all PubMed matches are correct matches.** Publication Matching uses automated search, which can produce false positives. A publication matched to a PI may have been written by a different author with the same name, or may be only tangentially related to the research project. Always review matched publications critically. Administrators and PIs should verify that a matched publication is genuinely associated with the project before claiming it as output.

**Not updating PI information when investigators change or leave.** If a PI leaves the institution or is replaced, their record in Publication Matching should be updated or removed from active searches. Failing to update PI information can result in continued searches for publications by investigators who are no longer with the institution, and may create confusion about project ownership and authorship.

---

# 9. Related Articles

- RC-CC-21 — Control Center Overview
- RC-CC-06 — Modules & Services Configuration
- RC-PROJ-01 — Project Lifecycle
