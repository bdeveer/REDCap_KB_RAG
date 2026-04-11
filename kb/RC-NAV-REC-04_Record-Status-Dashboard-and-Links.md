RC-NAV-REC-04

**Record Status Dashboard & Other Record Links**

| **Article ID** | RC-NAV-REC-04 |
| --- | --- |
| **Domain** | Navigation |
| **Applies To** | All REDCap project types |
| **Prerequisite** | RC-NAV-REC-01 — Record Navigation Overview |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | REDCap Support |

# 1. Overview

This article covers the Record Status Dashboard in detail — including
custom dashboards — and describes all other locations in REDCap where
you can find clickable links to records or specific instruments.

# 2. Key Concepts & Definitions

**Record Status Dashboard**

A project-level view that displays all records as rows and all
instruments (and events) as columns. Each cell contains a colored status
dot. The default dashboard shows everything you have access to.

**Custom Dashboard**

A user-configured version of the Record Status Dashboard. Custom
dashboards filter, sort, or group the default view to make large
projects more manageable. They are created by users with Project Design
rights and are available to all project users once created.

**Record ID Link**

Whenever REDCap displays a Record ID (the primary identifier for any
record), it is almost always a clickable link that opens the Record Home
Page for that record.

**Variable Link**

In certain data quality and data resolution tools, REDCap can link
directly to a specific instrument and even highlight a specific variable
within that instrument.

# 3. The Record Status Dashboard

## 3.1 Default Dashboard

- Access it from the left-hand menu under Data Collection \> Record
    Status Dashboard.

- Shows all records, events, arms (if applicable), repeated
    instruments, and repeated events you have access to.

- Click any dot to go directly to that instrument for that record.

- In projects with arms, tabs appear at the top — one per arm. Click
    a tab to switch arms.

## 3.2 Access Restrictions

REDCap automatically filters the dashboard based on your access level:

- Instrument-level access restrictions: instruments you do not have
    permission to view are hidden from the dashboard.

- Data Access Group (DAG) membership: if you are in a DAG, you only
    see records that belong to your DAG.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Troubleshooting:** If instruments seem to be missing from the dashboard, the most likely cause is either a custom dashboard filter or your access level. Check whether you are viewing a custom dashboard vs. the default dashboard.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4. Custom Dashboards

## 4.1 What Custom Dashboards Can Do

A user with Project Design rights can create custom dashboards with the
following options:

  ------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------
  **Customization Option**       **What It Does**
  Show a selection of events     Hides unused or less-relevant events to condense the view.
  Filter by arm                  Shows records from one specific arm, or all arms.
  Filter by logic                Applies a REDCap logic expression to show only matching records (e.g., only consented participants).
  Group by event or instrument   Reorganizes the grid to group all instances of one instrument or event together — useful for reviewing adverse events across all timepoints.
  Vertical header orientation    Rotates column headers to vertical text, narrowing columns when instrument or event names are long.
  Custom sorting                 Sorts records by a variable other than Record ID (e.g., by date of birth or visit date).
  ------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------

## 4.2 Accessing Custom Dashboards

- Custom dashboards appear as additional named links in the left-hand
    menu, below the default Record Status Dashboard link.

- They are automatically available to all project users once created
    — no additional setup is required per user.

# 5. Other Locations with Record Links

## 5.1 Record ID Links (to Record Home Page)

In the following locations, any displayed Record ID is a clickable link
to the Record Home Page:

- Reports

- Field comment logs

- Data resolution workflow

- Notification logs

- Survey invitation logs (only when surveys are in identified mode ---
    links are deactivated in anonymous mode)

- Participant list (same anonymous-mode restriction as above)

- Calendars

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** Survey invitation logs and the participant list only contain working Record ID links when the survey is in identified mode. In anonymous mode, the links are deactivated to protect respondent anonymity.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 5.2 Variable Links (to a Specific Instrument and Field)

In a few locations, REDCap links directly to a specific instrument and
highlights a specific variable. This is most common in data quality and
data cleaning tools:

- Data Quality tool

- Field comment log

- Data Resolution Workflow

- E-Signature and Locking Management

# 6. Common Questions

**Q: Why are some instruments missing from my Record Status Dashboard?**

A: The two most common reasons are: (1) you are viewing a custom
dashboard that filters certain events or instruments, or (2) your user
access level restricts which instruments you can see. Switch to the
default dashboard to see everything you have permission to access.

**Q: Who can create a custom dashboard?**

A: Only users with Project Design rights can create custom dashboards.
Once created, they are visible to all project users automatically.

**Q: Why do Record ID links not work in the survey invitation log?**

A: When a survey is configured in anonymous mode, REDCap deactivates
Record ID links in the invitation log and participant list to preserve
respondent anonymity.

**Q: What is the difference between a Record ID link and a variable
link?**

A: A Record ID link takes you to the Record Home Page for that record. A
variable link takes you directly to a specific instrument and highlights
a specific field — this level of precision is only available in data
quality and resolution tools.

**Q: Can I sort the dashboard by something other than Record ID?**

A: Yes, but only in a custom dashboard. A user with Project Design
rights can configure the custom dashboard to sort by any variable in the
project.

# 7. Common Mistakes & Gotchas

- Viewing a custom dashboard and not realizing it: if the dashboard
    appears filtered, check the left-hand menu to see if you are on the
    default dashboard or a named custom dashboard.

- Expecting Record ID links to work in anonymous surveys: links in
    invitation logs and participant lists are intentionally broken in
    anonymous mode. This is by design, not a bug.

- Expecting variable links everywhere: deep variable linking is only
    available in a handful of data quality tools. Most other locations
    only link to the Record Home Page.

- Overlooking DAG filtering: if you are in a Data Access Group, you
    will not see records outside your group — even on the default
    dashboard. This is an access control feature, not a dashboard
    filter.

# 8. Related Articles

- RC-NAV-REC-01 — Record Navigation Overview

- RC-NAV-REC-02 — Longitudinal Mode & Arms

- RC-NAV-REC-03 — Repeated Instruments & Repeated Events
