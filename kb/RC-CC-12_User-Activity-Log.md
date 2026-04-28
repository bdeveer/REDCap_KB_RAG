RC-CC-12

**User Activity Log**

| **Article ID** | RC-CC-12 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-11 — System Statistics; RC-CC-13 — User Activity Graphs; RC-CC-01 — Notifications & Reporting |

---

# 1. Overview

The User Activity Log provides a real-time, system-wide view of all user actions occurring across every project on the REDCap instance. It is accessible under "Dashboards & Activity" in the Control Center sidebar. This is distinct from the per-project audit log (Logging module within a project) — the Activity Log shows actions across ALL projects simultaneously.

---

# 2. Default View

By default, the page loads all user activity for the current day, with a count of total events shown in the header (e.g., "All User Activity for Today (X events)"). Events are displayed in reverse-chronological order, with the most recent actions appearing first.

---

# 3. Filtering

Administrators can filter the log by:

- **Project title**: search or select a specific project to view activity for only that project
- **Date range**: Start Date and End Date pickers to view historical activity beyond the current day

---

# 4. Log Entry Fields

Each log entry displays the following information:

- **Timestamp**: the date and time the action occurred
- **User**: the username or email of the user who performed the action (or `[survey respondent]` for actions by unauthenticated survey participants)
- **Action type**: a description of what was done

---

# 5. Action Types

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

---

# 6. Survey Respondents

Actions performed by unauthenticated survey participants are attributed to `[survey respondent]` rather than a named user. This includes creating and updating survey responses. This allows administrators to track survey activity while maintaining respondent privacy.

---

# 7. Volume Considerations

On active REDCap instances, the number of daily events can be very high (tens of thousands or more). The page renders all results which may cause slow load times for large date ranges. To improve performance:

- Filter by a specific project to reduce the result set
- Narrow the date range to focus on a specific time period
- Check system performance during off-peak hours if investigating a historical time range with high activity

---

# 8. Opening Individual Records

Some log entries may be clickable and link directly to the associated project or record for further investigation. This allows quick navigation from a system-wide activity view to a specific project context.

---

# 9. Common Questions

**Q: What is the difference between the User Activity Log and the per-project Logging module?**
The User Activity Log (in the Control Center) shows all activity across all projects on the instance in one centralized view. The Logging module within a single project shows only the activity within that specific project. Use the User Activity Log for instance-wide monitoring and the project Logging module for project-specific audit trails.

**Q: Can I filter the User Activity Log by username?**
The User Activity Log can be filtered by project title and date range. If you need to find activity by a specific user, enter their username or email in the Project title search field if they are associated with a particular project, or review the User field column for each entry. Advanced filtering by user may require exporting the data and analyzing it externally.

**Q: How do I export the User Activity Log for further analysis?**
The page displays all entries matching your filters, and you can copy them to your clipboard or right-click to save the page content. Most browsers allow you to select and copy table data. For large exports, consider narrowing your date range to improve performance and reduce the amount of data to copy.

**Q: What does "[survey respondent]" mean in the User column?**
Actions performed by unauthenticated survey participants (respondents who are not REDCap users) are attributed to "[survey respondent]" rather than a specific username. This protects respondent privacy while allowing you to track survey activity at the instance level.

**Q: If I see high API call volumes in the User Activity Log, what should I investigate?**
High API call volumes could indicate active integrations, automated data pulls, or malicious activity. Check which project the calls are coming from (via filtering), review the API documentation for that project, and contact the project administrator to understand if the activity is expected and legitimate.

**Q: Why is the page loading slowly when I request a large date range?**
The User Activity Log displays all events matching your filters in the current view. Large date ranges and active instances can result in tens of thousands of log entries, which requires the browser to render a large table. To improve performance, narrow your date range, filter by a specific project, or wait for the page to fully load before scrolling.

---

# 10. Common Mistakes & Gotchas

**Confusing survey respondent activity with authenticated user activity.** When viewing the User Activity Log, remember that "[survey respondent]" entries represent actions by unauthenticated survey participants, not staff members or project administrators. Do not assume that survey respondents have user accounts or login credentials.

**Not checking the date range when investigating activity.** If you are looking for activity during a specific time period and don't set the date range filters, you may be viewing only today's activity. Always confirm that your date range matches the period you are investigating to avoid missing relevant log entries.

**Forgetting that deleted actions are still logged.** If a user or administrator deletes data or a record, the deletion itself is logged (e.g., "Delete data entry record"). However, the original data creation may have occurred on a different date. If you are investigating a missing record, review the log for both creation and deletion entries spanning a wider date range.

**Assuming User Activity Log filtering is case-sensitive.** Test whether project title filtering is case-sensitive at your institution. Some systems may require exact case matching while others do not. If a filter returns no results, try variations in capitalization.

**Ignoring the performance warning for large result sets.** When requesting a very large date range on an active instance, the page may become unresponsive. Always start with a narrower date range and widen it only if needed. Do not expect instant results when querying months or years of data.

---

# 11. Related Articles

- RC-CC-11 — System Statistics
- RC-CC-13 — User Activity Graphs
- RC-CC-01 — Notifications & Reporting
