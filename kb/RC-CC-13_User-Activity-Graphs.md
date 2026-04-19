RC-CC-13

**User Activity Graphs**

| **Article ID** | RC-CC-13 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-11 — System Statistics; RC-CC-12 — User Activity Log; RC-CC-14 — Map of Users; RC-CC-15 — Top Usage Report |

---

# 1. Overview

The User Activity Graphs page displays visual charts summarizing REDCap system usage over time. It is accessible under "Dashboards & Activity" in the Control Center sidebar. The charts provide at-a-glance trend views that complement the raw data available in the User Activity Log (RC-CC-12) and System Statistics (RC-CC-11).

# 2. Time Range Selection

All charts can be filtered by time range using the navigation at the top of the page. The available options are:

- **Past Day**: last 24 hours
- **Past Week** (default): last 7 days
- **Past Month**: last 30 days
- **Past 3 Months**: last 90 days
- **Past 6 Months**: last 180 days
- **Past Year**: last 365 days
- **All**: entire history of the REDCap instance

Switching between time ranges reloads all charts for the selected period.

# 3. Available Charts

Charts are loaded dynamically. Based on REDCap v16.x, the charts include (but may not be limited to):

- **Concurrent Users/Respondents**: the number of users simultaneously active in REDCap, including survey respondents
- **Projects Moved to Production**: the count of projects transitioning from Development to Production status over the selected period
- **First-Time Visitors**: new unique users logging into REDCap for the first time during the period
- Additional charts covering logins, data entry activity, survey submissions, and other system metrics

Charts show "Loading chart..." until the data query completes. The exact set of charts may vary by REDCap version.

# 4. Chart Interaction

Most charts display:

- **X-axis**: time (days, weeks, or months depending on the time range selected)
- **Y-axis**: count or number of occurrences
- **Trend line or bar graph**: visual representation of activity over time

Charts can often be hovered over to view exact values for specific time points.

# 5. Relationship to Other Monitoring Tools

Activity Graphs provide trend visualization, complementing:

- **User Activity Log** (RC-CC-12) — for raw event-level detail and filtering by project or date
- **System Statistics** (RC-CC-11) — for aggregate counts and high-level metrics
- **Map of Users** (RC-CC-14) — for geographic distribution of users
- **Top Usage Report** (RC-CC-15) — for identifying the most active projects and users

# 6. Performance and Caching

The charts may take several seconds to load, especially for longer time ranges (Past Year or All). Results are typically cached to improve subsequent load times. If data appears outdated, administrators may need to wait for the cache to refresh or contact system administrators.

# 7. Common Questions

**Q: What is the default time range shown when I first load the User Activity Graphs page?**
The default time range is "Past Week" (last 7 days). This provides a reasonable balance between showing recent trends and avoiding excessive amounts of historical data. You can change the time range using the navigation buttons at the top of the page.

**Q: Can I zoom in or interact with individual data points on the charts?**
Most charts support hovering to view exact values for specific time points. The exact level of interactivity depends on the charting library and REDCap version. Try hovering over or clicking on chart elements to see if additional details are revealed.

**Q: What does "Concurrent Users/Respondents" measure?**
This metric shows the number of users and survey respondents simultaneously active in REDCap during the selected time period. A high peak may indicate a scheduled event, a major launch, or unusual activity. Use this chart to identify periods of highest system load.

**Q: Why would the "First-Time Visitors" chart show spikes at certain times?**
Spikes in new user registrations may correspond to planned onboarding events, the launch of major research studies, or institutional training sessions. If you see unexpected spikes, it may indicate that many new users were added at once, which could be related to project creation or user provisioning.

**Q: How do the User Activity Graphs differ from the User Activity Log?**
User Activity Graphs display trends and summaries over time, providing a high-level overview of usage patterns. The User Activity Log provides detailed, event-by-event information with filtering capabilities. Use graphs for trend analysis and the log for detailed investigations.

**Q: Is the data in the charts real-time, or is there a delay?**
Charts are typically near real-time, but may have a slight delay (minutes to hours depending on server performance and caching). Very recent activity may not appear until the next cache refresh. For the most current information, use the User Activity Log instead.

# 8. Common Mistakes & Gotchas

**Waiting too long for charts to load on "Past Year" or "All" views.** Querying charts for very long time periods can take considerable time, especially on active instances with years of historical data. Be patient and allow several seconds or minutes for results to load. Switching to a shorter time range will load much faster.

**Misinterpreting chart axes and unit scales.** Different charts may use different units (days vs. weeks, counts vs. percentages). Always read the axis labels and legend carefully to understand what is being measured. A sharp-looking spike might represent only a small absolute change if the Y-axis scale is zoomed in.

**Confusing "Concurrent Users" with "Total Active Users."** Concurrent Users shows how many people are using REDCap at the same moment. It is different from total active users over the period, which would count each active person once regardless of when they logged in. These are complementary but distinct metrics.

**Assuming cached data represents the current moment.** Charts may be cached to improve performance, which means they may represent data from several minutes or hours ago, not the exact current moment. If you need up-to-the-minute information, refresh the page or check the User Activity Log for the latest entries.

**Ignoring seasonal or scheduled patterns.** Usage graphs often show predictable patterns (e.g., lower activity on weekends, higher activity during academic terms, spikes around deadlines). Do not be alarmed by regular cycles; instead, use them to establish baselines for detecting truly anomalous activity.

# 9. Related Articles

- RC-CC-11 — System Statistics
- RC-CC-12 — User Activity Log
- RC-CC-14 — Map of Users
