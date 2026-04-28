RC-CC-15

**Top Usage Report**

| **Article ID** | RC-CC-15 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-12 — User Activity Log; RC-CC-13 — User Activity Graphs; RC-CC-14 — Map of Users; RC-CC-16 — Database Activity Monitor |

---

# 1. Overview

The Top Usage Report identifies the most resource-intensive projects, users, pages, URLs, External Modules, and cron jobs over a specified time period. It is accessible under "Dashboards & Activity" in the Control Center sidebar. Its primary purpose is to help diagnose server performance issues by pinpointing where load is concentrated.

---

# 2. When to Use

This report is most useful when REDCap is experiencing performance issues such as slow response times or crash messages. It helps answer questions like "which projects or users are consuming the most server resources right now?" By identifying resource-heavy components, administrators can take targeted action to resolve bottlenecks or investigate unexpected spikes in usage.

---

# 3. Important Caveats

The Top Usage Report includes several important limitations and clarifications to understand before interpreting results:

- **High utilization does NOT necessarily indicate a problem** — Heavy usage is expected for active projects. A project appearing in the top report simply means it is being actively used, not that there is a malfunction.

- **Percentages can exceed 100%** — Hours and percentages shown are accurate portions of tracked totals, but may be duplicated between "Types." This means the percentages across different categories can add up to more than 100%.

- **Incomplete coverage of all requests** — The report tracks many, but not all, HTTP requests. For complete coverage, administrators should consult the web server's access logs.

- **External Module Timed Crons are excluded** — External Module Timed Crons are not included in these statistics.

---

# 4. Filters

Administrators can configure the report using the following parameters:

- **Begin time** — Sets the start of the analysis window. Only data collected since this time point is available for reporting.

- **CPU time percentage minimum threshold** — Filters out entries below a specified CPU contribution percentage. This reduces noise by excluding low-utilization items from the results, allowing focus on the most significant consumers of resources.

- **Include incomplete HTTP requests** — Optional toggle to include requests that did not complete normally. Incomplete requests may indicate errors or client disconnections.

---

# 5. Report Contents

The report surfaces the "top" entries across multiple categories:

- **Most active projects** — Ranked by request count or CPU time consumption, showing which projects are driving the most activity.

- **Most active users** — Identifies users generating the most requests or consuming the most CPU time.

- **Most frequently accessed pages and URLs** — Shows which pages within projects are being accessed most often, useful for understanding usage patterns.

- **External Modules** — Reports which External Modules are consuming the most resources.

- **Cron jobs** — Lists cron jobs with the highest execution time, helpful for identifying long-running scheduled tasks.

---

# 6. Relationship to Other Tools

The Top Usage Report is one of several tools available for performance monitoring:

- **Database Activity Monitor (RC-CC-16)** — For real-time database-level performance and query analysis
- **User Activity Log (RC-CC-12)** — For detailed system-wide user action logs and audit trails
- **User Activity Graphs (RC-CC-13)** — For visual trends in user activity over time
- **Map of Users (RC-CC-14)** — For geographic visualization of user access patterns

Together, these tools provide multiple perspectives on REDCap system performance and usage.

---

# 7. Common Questions

**Q: If a project shows up in the Top Usage Report with high CPU time, does that mean there is a bug?**
No. High usage simply means the project is being actively used. Many active research projects will appear in top usage reports because they legitimately have many users, records, and transactions. A project appearing in the top report is expected behavior for busy instances.

**Q: Can I filter the report to exclude certain projects or users?**
The report provides a CPU time percentage minimum threshold filter, which helps reduce noise by excluding low-utilization items. However, there is no explicit project or user exclusion filter. If you need to focus on a specific subset of data, consider the time window and threshold filters to narrow results.

**Q: Why do percentages in the report sometimes add up to more than 100%?**
Hours and percentages are accurate portions of tracked totals, but they may be duplicated between different categories (e.g., "Most active projects" and "Most active users"). The same request may be counted in multiple categories, so percentages across different types can exceed 100%.

**Q: What time period does the report cover by default?**
The report covers all data collected since the "Begin time" parameter you set. If you do not set a specific begin time, the report will include the earliest available data. Set a specific start time to limit results to a relevant window (e.g., the last 24 hours or last week).

**Q: Does the Top Usage Report track all HTTP requests to REDCap?**
No. The report tracks many HTTP requests but not all. For a complete record of all HTTP activity, consult your web server's access logs. The report is most useful for identifying trends and resource-heavy components rather than for complete request accounting.

---

# 8. Common Mistakes & Gotchas

**Interpreting high usage as a performance problem.** A project appearing in the "Most active projects" list does not indicate a malfunction or problem — it simply means that project is being actively used. High activity is normal and expected. Only investigate further if you are experiencing actual performance issues (slow response times, timeouts, crashes) and the report helps you pinpoint the source.

**Setting the CPU time threshold too high and missing important data.** If you set the minimum CPU time percentage threshold too aggressively, you may filter out entries that would be useful to analyze. If you are investigating a specific performance issue, use a lower threshold to see more entries, then sort or focus on the most resource-intensive ones.

**Assuming External Module Timed Crons are included in the statistics.** External Module Timed Crons are explicitly excluded from the Top Usage Report. If you are troubleshooting slow scheduled tasks from External Modules, use the Database Activity Monitor or check cron logs separately rather than relying on this report.

---

# 9. Related Articles

- RC-CC-12 — User Activity Log
- RC-CC-13 — User Activity Graphs
- RC-CC-14 — Map of Users
- RC-CC-16 — Database Activity Monitor
- RC-CC-21 — Control Center Overview
