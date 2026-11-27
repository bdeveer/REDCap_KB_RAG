---
id: RC-CC-12
title: User Activity Log
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — User Activity
  Log behaviour checked against source code; page not re-captured
prerequisites:
- REDCap administrator access, including the right to access Control Center dashboards
version: '1.1'
last_updated: 2026-11
related:
- id: RC-CC-11
  title: 'Control Center: System Statistics'
- id: RC-CC-13
  title: 'Control Center: User Activity Graphs'
- id: RC-CC-01
  title: 'Control Center: Notifications & Reporting (Dashboard)'
tags:
- control center (admin)
synonyms:
- control center user activity log
- view user actions across all projects
- system-wide audit log for admins
- real-time log of redcap user activity
- track what users did instance-wide
- difference between activity log and project logging
- see data changes and admin actions across projects
- admin activity monitoring log
---

# 1. Overview

The User Activity Log provides a real-time, system-wide view of data-changing and administrative events occurring across every project on the REDCap instance. Logins and logouts are not listed here (see Section 5). It is accessible under "Dashboards & Activity" in the Control Center sidebar. This is distinct from the per-project audit log (Logging module within a project) — the Activity Log shows actions across ALL projects simultaneously.

---

# 2. Default View

By default, the page loads all user activity for the current day, with a count of total events shown in the header (e.g., "All User Activity for Today (X events)"). Events are displayed in reverse-chronological order, with the most recent actions appearing first.

---

# 3. Filtering

The only filter is the date range: **Start Date** and **End Date** pickers and a **Display** button, used to view historical activity beyond the current day. There is no filter by project or by user. To narrow what you see, shorten the date range or click a column header to sort the table (for example, sort by **User** to group one person's actions together). To find out which project an entry belongs to, use the gear icon described in Section 8.

---

# 4. Log Entry Fields

The table has these columns:

- **Gear icon** (super users only; see Section 8)
- **Time**: the date and time the action occurred
- **User**: the username of the user who performed the action. Actions with no logged-in user are attributed to a placeholder instead: `[survey respondent]` (survey participants), `SYSTEM` (automated system processes) or `[non-user]`
- **Event**: a description of what was done

---

# 5. Action Types

The log captures a broad range of actions across the REDCap system. Common examples include:

- Create survey response / Update survey response
- Export data (API)
- Download data dictionary (API)
- Download all data entry forms as PDF
- Create record / Update record / Delete record
- Rename data collection instrument / Delete data collection instrument
- Send survey confirmation email to participant
- And many others covering data changes and administrative actions

> **Note:** User logins and logouts do not appear in this log. To see login volume, use the **Daily User Logins** chart in [RC-CC-13 — Control Center: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md).

---

# 6. Survey Respondents

Actions performed by unauthenticated survey participants are attributed to `[survey respondent]` rather than a named user. This includes creating and updating survey responses. This allows administrators to track survey activity while maintaining respondent privacy.

Activity by MyCap participants is labelled `[mycap respondent]` in the User column. This label is present in 17.6.

> **Version caveat (REDCap 16.0.x LTS and 17.3.x LTS):** the `[mycap respondent]` label is not used on these versions, so MyCap participant activity is not labelled that way. If you are tracing MyCap activity on an LTS instance, do not search for that label; check the project's own Logging page instead.

---

# 7. Volume Considerations

On active REDCap instances, the number of daily events can be very high (tens of thousands or more). The page renders all results which may cause slow load times for large date ranges. To improve performance:

- Narrow the date range to focus on a specific time period
- Check system performance during off-peak hours if investigating a historical time range with high activity

There is no row limit, so every matching event is rendered.

---

# 8. Finding the Project for an Entry

The table has no project column and entries do not link to individual records. Instead, super users see a **gear icon** at the start of each row that belongs to a project. Hover over the gear to see the project title; click it to open that project's home page in a new window. Rows with no project (for example, deleted projects or system events) have no gear icon. Administrators who only have the dashboards right, and are not super users, do not see the gear icon.

---

# 9. Aggregate Counts Table

Below the main table, a second table titled **Aggregate Counts for Activity for <date>** shows how many times each event type occurred, with the most frequent first. It combines all projects and non-project events. Automatic calculation entries are excluded from these counts. Use it to see at a glance what dominated a day's activity, for example a spike in record updates or API exports.

---

# 10. Common Questions

**Q: What is the difference between the User Activity Log and the per-project Logging module?**
The User Activity Log (in the Control Center) shows all activity across all projects on the instance in one centralized view. The Logging module within a single project shows only the activity within that specific project. Use the User Activity Log for instance-wide monitoring and the project Logging module for project-specific audit trails.

**Q: Can I filter the User Activity Log by username or project?**
No. The only filter is the date range. To find one user's activity, shorten the date range and click the **User** column header to sort, so that user's rows sit together. To find one project's activity, use the project's own Logging page, or hover over the gear icon on a row to see which project it belongs to.

**Q: How do I export the User Activity Log for further analysis?**
There is no export button. The page displays all entries for the selected dates, and you can select and copy the table data from the browser into a spreadsheet, or save the page content. For large exports, consider narrowing your date range to improve performance and reduce the amount of data to copy.

**Q: What does "[survey respondent]" mean in the User column?**
Actions performed by unauthenticated survey participants (respondents who are not REDCap users) are attributed to "[survey respondent]" rather than a specific username. This protects respondent privacy while allowing you to track survey activity at the instance level.

**Q: If I see high API call volumes in the User Activity Log, what should I investigate?**
High API call volumes could indicate active integrations, automated data pulls, or malicious activity. Check which project the calls are coming from (hover over the gear icon on the rows, or look at the project's Logging page), review the API documentation for that project, and contact the project administrator to understand if the activity is expected and legitimate.

**Q: Why is the page loading slowly when I request a large date range?**
The User Activity Log displays all events matching your filters in the current view. Large date ranges and active instances can result in tens of thousands of log entries, which requires the browser to render a large table. To improve performance, narrow your date range or wait for the page to fully load before scrolling.

---

# 11. Common Mistakes & Gotchas

**Confusing survey respondent activity with authenticated user activity.** When viewing the User Activity Log, remember that "[survey respondent]" entries represent actions by unauthenticated survey participants, not staff members or project administrators. Do not assume that survey respondents have user accounts or login credentials.

**Not checking the date range when investigating activity.** If you are looking for activity during a specific time period and don't set the date range filters, you may be viewing only today's activity. Always confirm that your date range matches the period you are investigating to avoid missing relevant log entries.

**Forgetting that deleted actions are still logged.** If a user or administrator deletes data or a record, the deletion itself is logged (e.g., "Delete data entry record"). However, the original data creation may have occurred on a different date. If you are investigating a missing record, review the log for both creation and deletion entries spanning a wider date range.

**Looking for logins in this log.** Logins and logouts are not listed. Use the Daily User Logins chart on the User Activity Graphs page instead.

**Ignoring the performance warning for large result sets.** When requesting a very large date range on an active instance, the page may become unresponsive. Always start with a narrower date range and widen it only if needed. Do not expect instant results when querying months or years of data.

---

# 12. Related Articles

- [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md)
- [RC-CC-13 — Control Center: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md)
- [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md)
