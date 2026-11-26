

**Record Status Dashboard and Links**

| **Article ID** | [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) |
|---|---|
| **Domain** | Record Navigation |
| **Applies To** | All project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Record Status Dashboard, custom dashboards and record links behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md), [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md), [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md)[RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md), [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md), [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)[RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md)[RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md), [RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md), [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md)[RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md)[RC-DE-08 — Field Comment Log](RC-DE-08_Field-Comment-Log.md), [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md), [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) |
| **Synonyms** | what is the record status dashboard; how to create a custom record dashboard; where to see all records and their completion status; how to make a custom dashboard filtered by criteria; clicking links to open records from the dashboard; view of all records as rows and instruments as columns; how to find record links throughout redcap; record status dashboard colored dots |

---

## 1. Overview

This article covers the Record Status Dashboard in detail — including
custom dashboards — and describes all other locations in REDCap where
you can find clickable links to records or specific instruments.

---

## 2. Key Concepts & Definitions

**Record Status Dashboard**

A project-level view that displays all records as rows and all
instruments (and events) as columns. Each cell contains a colored status
dot. The default dashboard shows everything you have access to.

**Custom Dashboard**

A user-configured version of the Record Status Dashboard. Custom
dashboards filter, sort, or group the default view to make large
projects more manageable. Only users with Project Design and Setup
rights can create, modify or delete them; all project users can view
them once created.

**Record ID Link**

Whenever REDCap displays a Record ID (the primary identifier for any
record), it is almost always a clickable link to that record. Depending
on the page, it opens the Record Home Page or a specific instrument for
the record (see section 5.1).

**Variable Link**

In certain data quality and data resolution tools, REDCap can link
directly to a specific instrument and even highlight a specific variable
within that instrument.

---

## 3. The Record Status Dashboard

### 3.1 Default Dashboard

- Access it from the left-hand menu under Data Collection \> Record
    Status Dashboard.

- Shows all records, events, arms (if applicable), repeated
    instruments, and repeated events you have access to.

- Click any dot to go directly to that instrument for that record.

- In longitudinal projects with more than one arm, tabs appear at the
    top — one per arm. Click a tab to switch arms.

- Records are shown 100 per page by default. Use the records-per-page
    selector (10, 25, 50, 100, 250, 500, 1000 or ALL) and the page
    selector to move through large projects.

- If you are not assigned to a Data Access Group, a **Displaying Data
    Access Group** dropdown lets you limit the view to one DAG.

- Lock and e-signature icons are shown over the status dots of locked
    or e-signed instruments. A lock icon next to the record name means
    the whole record is locked.

- The page has an **Add new record** button (if you have record
    creation rights) and a **+** button for adding a new instance of a
    repeating instrument or event.

- If Bulk Record Delete is enabled and you have that user right, it is
    available from the multi-record actions on the dashboard.

### 3.2 Access Restrictions

REDCap automatically filters the dashboard based on your access level:

- Instrument-level access restrictions: instruments you do not have
    permission to view are hidden from the dashboard.

- Data Access Group (DAG) membership: if you are in a DAG, you only
    see records that belong to your DAG.


> **Troubleshooting:** If instruments seem to be missing from the dashboard, the most likely cause is either a custom dashboard filter or your access level. Check whether you are viewing a custom dashboard vs. the default dashboard.


---

## 4. Custom Dashboards

### 4.1 What Custom Dashboards Can Do

A user with Project Design and Setup rights can create custom dashboards
with the following options:

| **Customization Option** | **What It Does** |
| --- | --- |
| Title | The dashboard name shown in the **Dashboard displayed:** dropdown. |
| Description / instructions | Optional text shown at the top of the dashboard (see the smart-variable note below). |
| Select instruments (classic) / Select instruments/events (longitudinal) | Shows only the chosen columns, condensing the view. |
| Group columns by instrument or event | Longitudinal projects only (not offered in classic projects). Changes how the column headers are nested: instruments under events, or events under instruments. It does not affect repeating instances. |
| Header orientation | **Horizontal** (default) or **Vertical**. Vertical text narrows columns when instrument or event names are long. |
| Filter logic | Applies a REDCap logic expression to show only matching records (e.g., only consented participants). |
| Filter by arm | Only shown when the project has more than one arm. Choosing one arm shows only that arm and hides the arm tabs. |
| Sort by | Sorts records by a field (plus an event in longitudinal projects), ascending or descending, instead of by Record ID (e.g., by visit date). |

**Description and instructions** — from **15.7.2**, the description/instructions text on a Custom Record Status Dashboard supports **aggregate smart variables** and miscellaneous **project-level smart variables**. This allows a dashboard to open with a live summary — a record count, a project status, or a computed total — rather than static prose. See [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md) and [RC-PIPE-17 — Smart Variables: Miscellaneous](RC-PIPE-17_Smart-Variables-Miscellaneous.md).

From **16.1.1**, rows on the Record Status Dashboard highlight on hover and on keyboard focus, which makes tracking a row across a wide grid considerably easier.

> **Version caveat (16.0 LTS):** Rows do not highlight on hover or focus. To keep track of rows on a wide grid, use a custom dashboard that shows fewer columns.

> **Version caveat (below 15.6.1 Standard):** Filter logic on a report **or** a Custom Record Status Dashboard that tested a form status field against a blank value — `[form1_complete] = ""` — could return **incorrect filtered results**. The underlying inconsistency in how blank and incomplete form statuses were compared was addressed across 15.5.1 and 15.6.1. Dashboards built on this pattern before then should be re-checked, because the failure was silent: a plausible-looking but wrong record set.

> **Version caveat (below 15.0.3 Standard):** A custom dashboard sorted by the record ID field in **descending** order displayed records in the wrong order where the project's first instrument was a repeating instrument or sat on a repeating event.

### 4.2 Accessing Custom Dashboards

- Custom dashboards do **not** appear as links in the left-hand menu.
    Open the Record Status Dashboard, then pick the dashboard from the
    **Dashboard displayed:** dropdown at the top of the page.

- If you want a direct menu link to a custom dashboard, open it, copy
    its URL, and add it as a Project Bookmark.

- All project users can view all custom dashboards once created — no
    setup is required per user. Instrument-level rights and DAG
    membership still restrict what each user sees on them.

### 4.3 Managing Custom Dashboards *(17.5.3+)*

From 17.5.3 (Standard), users with Project Design and Setup rights see a
**Manage** link next to the **Record Status Dashboard** link on the
left-hand project menu. It opens a dedicated page that lists every
custom dashboard in the project and lets you create new ones and edit
or delete existing ones, without first opening each dashboard.

The same release changed the buttons on the Record Status Dashboard
page itself: it now shows **Dashboard actions: Modify / Manage /
Create**.

> **Version caveat (below 17.5.3 Standard, and the 17.3 and 16.0 LTS lines):**
> There is no Manage link or Manage page. On the Record Status Dashboard
> page, use **Create custom dashboard** to add one, and select a
> dashboard in the dropdown and click **Modify** to edit or delete it.
> Written instructions that mention **Dashboard actions** or **Manage**
> do not apply to your version.

---

## 5. Other Locations with Record Links

### 5.1 Record ID Links

In the following locations, a displayed Record ID is a clickable link.
Where it leads depends on the page:

| **Location** | **Where the link goes** |
| --- | --- |
| Reports (My Reports & Exports) | Longitudinal projects, non-repeating rows: the Record Home Page. Classic projects: the record's first instrument. Repeating rows: that instrument and event instance. Reports viewed in Data Analysis/Cleanup (Stats & Charts) have no record links. |
| Field comment log, Data Resolution Workflow | The record (and, with a variable link, the instrument and field — see 5.2). |
| Notification log (Alerts & Notifications) | The instrument the alert relates to when it is known; otherwise the Record Home Page. |
| Survey invitation log | That survey's data entry form for the record (only when the survey is in identified mode). |
| Participant list | That survey's data entry form for the record (same identified-mode restriction). |
| Calendar | The Record Home Page. |


> **Important:** Survey invitation logs and the participant list only contain working Record ID links when the survey is in identified mode. In anonymous mode, the links are deactivated to protect respondent anonymity.


### 5.2 Variable Links (to a Specific Instrument and Field)

In a few locations, REDCap links directly to a specific instrument and
highlights a specific variable. This is most common in data quality and
data cleaning tools:

- Data Quality tool

- Field comment log

- Data Resolution Workflow

E-Signature and Locking Management also links to the record and
instrument, but it opens the instrument without highlighting a field.

---

## 6. Common Questions

**Q: Why are some instruments missing from my Record Status Dashboard?**

**A:** The two most common reasons are: (1) you are viewing a custom
dashboard that filters certain events or instruments, or (2) your user
access level restricts which instruments you can see. Switch to the
default dashboard to see everything you have permission to access.

**Q: Who can create a custom dashboard?**

**A:** Only users with Project Design and Setup rights can create, modify
or delete custom dashboards. Once created, all project users can view
them from the **Dashboard displayed:** dropdown; their instrument rights
and DAG still limit what they see.

**Q: Why do Record ID links not work in the survey invitation log?**

**A:** When a survey is configured in anonymous mode, REDCap deactivates
Record ID links in the invitation log and participant list to preserve
respondent anonymity.

**Q: What is the difference between a Record ID link and a variable
link?**

**A:** A Record ID link takes you to the record — usually the Record Home
Page, or on some pages a specific instrument for that record. A
variable link takes you directly to a specific instrument and highlights
a specific field — this level of precision is only available in data
quality and resolution tools.

**Q: Can I sort the dashboard by something other than Record ID?**

**A:** Yes, but only in a custom dashboard. A user with Project Design
and Setup rights can configure the custom dashboard to sort by any field
in the project (plus an event in longitudinal projects), ascending or
descending.

---

## 7. Common Mistakes & Gotchas

- Viewing a custom dashboard and not realizing it: if the dashboard
    appears filtered, check the **Dashboard displayed:** dropdown at the
    top of the page to see if you are on the default dashboard or a
    named custom dashboard.

- Looking for custom dashboards in the left-hand menu: they are not
    listed there. Use the **Dashboard displayed:** dropdown, or add a
    Project Bookmark to the dashboard's URL.

- Expecting Record ID links to work in anonymous surveys: links in
    invitation logs and participant lists are intentionally broken in
    anonymous mode. This is by design, not a bug.

- Expecting variable links everywhere: deep variable linking is only
    available in a handful of data quality tools. Most other locations
    link to the Record Home Page or to an instrument without highlighting
    a field.

- Overlooking DAG filtering: if you are in a Data Access Group, you
    will not see records outside your group — even on the default
    dashboard. This is an access control feature, not a dashboard
    filter.

---

## 8. Related Articles

- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) — foundational article
    covering Add/Edit Records, the Record Home Page, and dot color
    meanings

- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) — how arm tabs and
    event columns appear on the dashboard in longitudinal projects

- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) — stacked
    dot indicators shown on the dashboard for repeated instruments

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) — the two-panel layout
    and how to reach the Record Status Dashboard from the menu

- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) — full reference for the
    Data Collection menu section where the dashboard lives

- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) — how
    user permissions control which instruments appear on the dashboard

- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) — instrument-
    level access settings that filter dashboard visibility

- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md)
    records appear on the dashboard; key troubleshooting context

- [RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md) — creating custom dashboards that
    filter, sort, or group the default dashboard view

- [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md)
    Record IDs are clickable links to the record; custom
    dashboards and reports are complementary tools

- [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md)
    invitation logs contain Record ID links, but only in identified
    (non-anonymous) survey mode

- [RC-DE-08 — Field Comment Log](RC-DE-08_Field-Comment-Log.md)
    to the Record Home Page; variable-level links also available

- [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md) — deep variable links to
    specific instruments are available from this tool

- [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) — variable-level links to specific
    instruments and fields are available from data quality results
