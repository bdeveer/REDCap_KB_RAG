RC-CC-12

**User Activity Log**

| **Article ID** | RC-CC-12 |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-11 (System Statistics); RC-CC-13 (User Activity Graphs); RC-CC-01 (Notifications & Reporting) |

---

## 1. Overview

The User Activity Log provides a real-time, system-wide view of all user actions occurring across every project on the REDCap instance. It is accessible under "Dashboards & Activity" in the Control Center sidebar. This is distinct from the per-project audit log (Logging module within a project) — the Activity Log shows actions across ALL projects simultaneously.

## 2. Default View

By default, the page loads all user activity for the current day, with a count of total events shown in the header (e.g., "All User Activity for Today (X events)"). Events are displayed in reverse-chronological order, with the most recent actions appearing first.

## 3. Filtering

Administrators can filter the log by:

- **Project title**: search or select a specific project to view activity for only that project
- **Date range**: Start Date and End Date pickers to view historical activity beyond the current day

## 4. Log Entry Fields

Each log entry displays the following information:

- **Timestamp**: the date and time the action occurred
- **User**: the username or email of the user who performed the action (or `[survey respondent]` for actions by unauthenticated survey participants)
- **Action type**: a description of what was done

## 5. Action Types

The log captures a broad range of actions across the REDCap system. Common examples include:

- Create survey response / Update survey response
- Export data (API)
- Download data dictionary (API)
- Download all data entry forms as PDF
- Create/update/delete data entry record
- Rename data collection instrument / Delete data collection instrument
- Send survey confirmation email to participant
- User login / logout
- And many others covering the full range of REDCap operations

## 6. Survey Respondents

Actions performed by unauthenticated survey participants are attributed to `[survey respondent]` rather than a named user. This includes creating and updating survey responses. This allows administrators to track survey activity while maintaining respondent privacy.

## 7. Volume Considerations

On active REDCap instances, the number of daily events can be very high (tens of thousands or more). The page renders all results which may cause slow load times for large date ranges. To improve performance:

- Filter by a specific project to reduce the result set
- Narrow the date range to focus on a specific time period
- Check system performance during off-peak hours if investigating a historical time range with high activity

## 8. Opening Individual Records

Some log entries may be clickable and link directly to the associated project or record for further investigation. This allows quick navigation from a system-wide activity view to a specific project context.

## Related Resources

- [RC-CC-11: System Statistics](RC-CC-11_System-Statistics.md)
- [RC-CC-13: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md)
- [RC-CC-01: Notifications & Reporting](RC-CC-01_Notifications-and-Reporting.md)
