

**Control Center: Publication Matching**

| **Article ID** | [RC-CC-19 — Control Center: Publication Matching](RC-CC-19_Publication-Matching.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Publication Matching behaviour checked against source code; earlier live check (v17.5.6) of tabs and Setup settings kept; pages not re-captured |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md); [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md); [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)|
| **Synonyms** | control center publication matching; find pubmed publications linked to projects; automatically match papers to redcap projects; nightly publication search by principal investigator; email pis about matched publications; pubmed matching for research projects; track publications associated with projects; publication matching module admin |

---

**Publication Matching** (found at **Control Center → Miscellaneous Modules → Publication Matching**) is a module that automatically searches online publication databases to find publications associated with REDCap research projects. As of REDCap 16.x, the only supported database is **PubMed**.

When enabled, REDCap runs a nightly search using the Principal Investigators (PIs) and the institution names linked to each qualifying project. Potential matches are not reviewed by administrators: if PI emailing is turned on, REDCap emails each PI a link where the PI confirms which publications are theirs and which projects they relate to.

---

## 1. Overview

Publication Matching helps research institutions track and document scholarly output from REDCap projects by automatically discovering publications associated with project Principal Investigators. The system scans PubMed nightly, identifies potential matches, and asks the investigators themselves to confirm them. This is particularly useful for institutions that need to report research productivity or maintain publication records for regulatory and grant compliance purposes.

---

## 2. Eligibility Requirements

Not all projects participate in Publication Matching. A project must meet **all** of the following criteria:

1. **Project purpose is set to "Research"** — set in project settings at the project level
2. **Project is out of Development status** — Production and Analysis/Cleanup projects qualify; development-mode projects are excluded
3. **Project is marked "Ready for use"** — an administrator sets this on the To-Do List or Manage Projects tab once the PI data is in order (see §3)

Additionally, REDCap uses the **project's creation date** as the lower date boundary when searching for publications. The module assumes the project was created before any associated publication was submitted, so matches from before the year the project was created are dropped.

---

## 3. Principal Investigator (PI) Data

Each qualifying project should have PI information associated with it. The following fields are tracked per PI:

| Field | Notes |
| --- | --- |
| **Last name** | Required; used in the search |
| **First name** | Required; only its first letter is used in the search |
| **Middle initial** | Optional; not used in the search |
| **Alias** | Optional; an alternative author name in PubMed's "last name + initials" style (e.g. `Harris PA`), useful for a maiden name or a middle initial the PI publishes under |
| **Email** | Required (must be valid); this is where match emails go |

Complete PI fields are not enough on their own. Each project also has a status that an administrator chooses:

| Status | Effect |
| --- | --- |
| **Decide later** | Not yet decided; the project stays on the To-Do List tab and is not searched |
| **Ready for use** | The project's PIs are included in the nightly search |
| **Exclude from use** | The project is left out of Publication Matching |

PI data you enter or correct in this module is written into the project's own PI fields (the ones in the project settings), so it is the same information, not a separate copy.

---

## 4. Module Tabs

The Publication Matching page is organized into five tabs:

### 4.1 Setup

General configuration for the module. Key settings include:

- **Enable/disable Publication Matching** — toggles the entire module
- **P.I. Emailing** — controls whether PIs receive email notifications about matched publications. PIs are **not** emailed until this setting is explicitly enabled, even if the module is running
- **Days between emails** — install value `7`; the minimum gap between emails to the same PI
- **Email Limit** — install value `3`; how many times a PI is emailed about the same match before REDCap stops asking
- **Email Subject** — a 17.5.6 test instance showed *[REDCap] Action Requested - Confirm REDCap Supported Publication*
- **Email Text** — the opening paragraph of the message sent to PIs. REDCap adds the greeting ("Dr." and the PI's last name), the number of matches, the link and the closing itself
- **Institution Keywords** — institution names used in the search. The install value is `Vanderbilt` and `Meharry`, so **replace these with your own institution's names** before enabling the module

### 4.2 To-Do List

Displays projects that have not yet been marked **Ready for use** or **Exclude from use**, usually because their PI data is incomplete or nobody has reviewed it. These projects are not searched. The count in parentheses next to the tab label (e.g., *To-Do List (349)*) counts groups of projects that share the same PI, not individual projects.

Administrators use this tab to:
- Identify which projects are missing PI data
- Fill in or correct PI information before the next nightly run
- Copy PI data from an existing PI record using the autocomplete search
- Mark each project **Ready for use** or **Exclude from use**

### 4.3 Manage Projects

Allows administrators to review and edit PI associations for individual projects. Provides:
- A project selector to navigate between qualifying projects
- PI name and contact fields, with validation highlighting for missing or malformed entries
- An autocomplete search field to copy data from an existing PI record to avoid re-entry
- The project's status (Decide later, Ready for use, Exclude from use), so a project can be excluded or brought back later

### 4.4 P.I.-Pub Matches

Lists the PIs who will be emailed about matches: how many matches are pending for each, a warning where a PI has reached the email limit, and a sample of the email. A PI-view button opens the page the PI sees from the email link, so an administrator can see exactly what the PI will be asked.

### 4.5 Project-Pub Matches

Displays the publications that PIs have **confirmed**, organised by REDCap project, with a CSV export. Unconfirmed matches do not appear here.

---

## 5. Nightly Search Process

REDCap runs the PubMed search automatically once every 24 hours, as part of its scheduled jobs (the REDCap cron job must be running on the server). For each PI on a project marked **Ready for use**, the search uses:
- The PI's last name and first initial, in PubMed's author style (e.g. "Smith J"), plus the alias if one is entered
- The institution names in the **Institution Keywords** setting on the Setup tab, plus any extra institution names entered for that project
- The project creation year as the earliest allowable publication date

Each search returns at most 100 results. Because only the first initial is used, the institution names do most of the work of telling one "Smith J" from another.

New matches are queued for the PI to confirm; they are not shown to administrators for approval. Publications that PIs confirm appear on the Project-Pub Matches tab. Once a week REDCap also sends the confirmed PubMed IDs, with summary statistics, to the REDCap Consortium.

---

## 6. PI Email Notifications

When **P.I. Emailing** is enabled in the Setup tab, REDCap emails each PI who has pending matches. The email contains the **Email Text** paragraph, the number of matches and a personal link. The link opens a page without a REDCap login, where the PI answers whether each publication is theirs and picks which of their projects it relates to. Those answers are what fill the Project-Pub Matches tab.

REDCap waits at least the **Days between emails** before emailing the same PI again, and stops asking about a match once the **Email Limit** is reached.

> **Important:** PI emailing is disabled by default and must be explicitly turned on. Enabling it before PI records are complete and verified may result in incorrect or premature notifications.

The administrator's levers are therefore: turning emailing on or off, the interval and the limit, the institution keywords, and excluding a project. There is no step where an administrator approves or rejects individual matches.

---

## 7. Common Questions

**Q: Why do some of my research projects not appear in the Publication Matching module?**
Projects must meet these eligibility criteria: (1) the project's purpose must be set to "Research" in project settings, and (2) the project must be out of Development (Production or Analysis/Cleanup). Development-mode projects and projects with other purposes (e.g., QA, Training) are excluded. A qualifying project is only searched once an administrator marks it **Ready for use**; until then it sits on the To-Do List tab.

**Q: Does the search use the date the project was created?**
Yes. The project creation date is used as the lower boundary for the publication search. REDCap assumes that publications associated with a project could not have been submitted or published before the project existed, so matches from before the project's creation year are dropped.

**Q: Can the system search for publications by multiple Principal Investigators?**
Yes. Each project can have multiple PIs associated with it. The nightly search uses each PI's last name and first initial, plus the institution names, to look for matching publications in PubMed. Each PI record must have a first name, last name and valid email address, and the project must be marked **Ready for use**, to be included in the search.

**Q: What happens if a PI's name is very common (like "John Smith")?**
The search uses only the last name and first initial ("Smith J"), so the institution names are what narrow the results to the right person. Very common names may still return false positives (publications by a different "J Smith"). This is why each PI confirms their own matches: a publication only counts once the PI says it is theirs.

**Q: Can I manually review and reject publication matches before they are shown to PIs?**
No. Administrators do not review, accept or discard matches. REDCap emails each PI a link, and the PI confirms or rejects each match and picks the related projects. What you control is whether PIs are emailed at all (**P.I. Emailing**), how often (**Days between emails**, **Email Limit**), which projects take part (**Ready for use** / **Exclude from use**), and the institution keywords. The PI-view button on the P.I.-Pub Matches tab shows you what a PI will see.

---

## 8. Common Mistakes & Gotchas

**Leaving the default Institution Keywords in place.** The install values name other institutions, so searches would use them unless you replace them on the Setup tab.

**Enabling PI emailing before completing PI records.** PI emailing is disabled by default. If you enable it before ensuring that all PI records are complete (first name, last name, valid email) and the right projects are marked **Ready for use**, PIs may receive emails with incomplete or incorrect information about publication matches. Always complete and verify PI data in the To-Do List and Manage Projects tabs before enabling PI emailing.

**Expecting an administrator review queue.** The P.I.-Pub Matches tab is a list of PIs to be emailed, not a list of matches to approve. Confirmation is done by the PIs through the emailed link; only confirmed publications appear on the Project-Pub Matches tab.

**Assuming all PubMed matches are correct matches.** Publication Matching uses automated search on last name and first initial, which can produce false positives. A publication matched to a PI may have been written by a different author with the same name, or may be only tangentially related to the research project. Only publications the PI has confirmed should be claimed as output.

**Leaving projects on the To-Do List.** Complete PI data alone does not start the search. Projects nobody marks **Ready for use** are never searched, however complete their PI fields are.

**Not updating PI information when investigators change or leave.** If a PI leaves the institution or is replaced, their record in Publication Matching should be updated, or the project marked **Exclude from use**. Failing to update PI information can result in continued searches for publications by investigators who are no longer with the institution, and may create confusion about project ownership and authorship.

---

## 9. Related Articles

- [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)
