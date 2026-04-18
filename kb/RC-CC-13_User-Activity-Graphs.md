RC-CC-13

**User Activity Graphs**

| **Article ID** | RC-CC-13 |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-11 (System Statistics); RC-CC-12 (User Activity Log); RC-CC-14 (Map of Users); RC-CC-15 (Top Usage Report) |

---

## 1. Overview

The User Activity Graphs page displays visual charts summarizing REDCap system usage over time. It is accessible under "Dashboards & Activity" in the Control Center sidebar. The charts provide at-a-glance trend views that complement the raw data available in the User Activity Log (RC-CC-12) and System Statistics (RC-CC-11).

## 2. Time Range Selection

All charts can be filtered by time range using the navigation at the top of the page. The available options are:

- **Past Day**: last 24 hours
- **Past Week** (default): last 7 days
- **Past Month**: last 30 days
- **Past 3 Months**: last 90 days
- **Past 6 Months**: last 180 days
- **Past Year**: last 365 days
- **All**: entire history of the REDCap instance

Switching between time ranges reloads all charts for the selected period.

## 3. Available Charts

Charts are loaded dynamically. Based on REDCap v16.x, the charts include (but may not be limited to):

- **Concurrent Users/Respondents**: the number of users simultaneously active in REDCap, including survey respondents
- **Projects Moved to Production**: the count of projects transitioning from Development to Production status over the selected period
- **First-Time Visitors**: new unique users logging into REDCap for the first time during the period
- Additional charts covering logins, data entry activity, survey submissions, and other system metrics

Charts show "Loading chart..." until the data query completes. The exact set of charts may vary by REDCap version.

## 4. Chart Interaction

Most charts display:

- **X-axis**: time (days, weeks, or months depending on the time range selected)
- **Y-axis**: count or number of occurrences
- **Trend line or bar graph**: visual representation of activity over time

Charts can often be hovered over to view exact values for specific time points.

## 5. Relationship to Other Monitoring Tools

Activity Graphs provide trend visualization, complementing:

- **User Activity Log** (RC-CC-12) — for raw event-level detail and filtering by project or date
- **System Statistics** (RC-CC-11) — for aggregate counts and high-level metrics
- **Map of Users** (RC-CC-14) — for geographic distribution of users
- **Top Usage Report** (RC-CC-15) — for identifying the most active projects and users

## 6. Performance and Caching

The charts may take several seconds to load, especially for longer time ranges (Past Year or All). Results are typically cached to improve subsequent load times. If data appears outdated, administrators may need to wait for the cache to refresh or contact system administrators.

## Related Resources

- [RC-CC-11: System Statistics](RC-CC-11_System-Statistics.md)
- [RC-CC-12: User Activity Log](RC-CC-12_User-Activity-Log.md)
- [RC-CC-14: Map of Users](RC-CC-14_Map-of-Users.md)
- [RC-CC-15: Top Usage Report](RC-CC-15_Top-Usage-Report.md)
