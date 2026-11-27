---
id: RC-CC-13
title: User Activity Graphs
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: 'REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — User
  Activity Graphs behaviour checked against source code; checked live on v17.5.6 (read-only):
  time ranges and chart titles'
prerequisites:
- REDCap administrator with the "Access to Control Center dashboards" right
version: '1.2'
last_updated: 2026-11
related:
- id: RC-CC-11
  title: 'Control Center: System Statistics'
- id: RC-CC-12
  title: 'Control Center: User Activity Log'
- id: RC-CC-14
  title: 'Control Center: Map of Users'
- id: RC-CC-15
  title: 'Control Center: Top Usage Report'
tags:
- control center (admin)
synonyms:
- control center user activity graphs
- visual charts of redcap usage over time
- usage trend graphs for administrators
- chart of logins and activity by date
- database usage and page hits graph
- system usage visualization control center
- graph of active users over time
- activity trend charts admin dashboard
- visualize redcap system usage
---

# 1. Overview

The User Activity Graphs page displays visual charts summarizing REDCap system usage over time. It is accessible under "Dashboards & Activity" in the Control Center sidebar, to administrators who hold the "Access to Control Center dashboards" right. The page is the same on REDCap 16.0.x LTS and 17.x. The charts provide at-a-glance trend views that complement the raw data available in the User Activity Log ([RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)) and System Statistics ([RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md)).

---

# 2. Time Range Selection

All charts can be filtered by time range using the navigation at the top of the page. The available options are:

- **Past Day**: last 24 hours
- **Past Week** (default): last 7 days
- **Past Month**: the past calendar month (same date last month to today)
- **Past 3 Months**: the past three calendar months
- **Past 6 Months**: the past six calendar months
- **Past Year**: the past twelve months
- **All**: entire history of the REDCap instance

Switching between time ranges reloads all charts for the selected period. The charts load one after another, so the lower charts finish last.

---

# 3. Available Charts

Charts are loaded dynamically. The page shows ten charts. Four show a value per day (or per 30 minutes); the other six are **running totals**.

**Per-period charts:**

- **Concurrent Users/Respondents**: the number of distinct sessions (users and survey respondents) that viewed at least one page in each 30-minute block
- **Database Usage (MB)**: size of REDCap's database tables (data plus indexes), taken as one snapshot per day
- **Usage by Uploaded Files (MB)**: total size of the files REDCap has recorded as uploaded, including active Send-It files, taken as one snapshot per day. This is what REDCap has on record, not a measurement of the disk or storage server
- **Daily User Logins**: the number of successful logins per day. A user who logs in three times counts three times; with two-factor authentication a login counts once the second factor is completed

**Running-total charts** (each point is the cumulative count up to that date, not the count for that day):

- **Projects Created**: total projects created
- **Projects Moved to Production**: total projects moved from Development to Production
- **Active Users**: total users who have ever had any logged activity, placed on the date of their first activity
- **First-Time Visitors**: total users who have logged in or visited REDCap at least once, placed on the date of their first visit. This tracks first use, not account creation
- **Logged Events**: total entries written to logging
- **Page Hits**: total page requests

To read a running-total chart, compare the first and last point of the range: the rise is the number that happened in the period. For example, if **Projects Created** goes from 12,400 to 12,460 over Past Month, 60 projects were created that month. A flat stretch means nothing new happened; the line never goes down.

Charts show "Loading chart..." until the data query completes.

---

# 4. Chart Interaction

All ten charts are line charts:

- **X-axis**: date. Each point is one day (Concurrent Users/Respondents: one 30-minute block) whatever range you pick; a longer range only changes how the date labels are spaced.
- **Y-axis**: a count, or megabytes for the two "(MB)" charts. There are no axis titles or legends; the chart title is the only label.
- **Missing days**: days with nothing to count are left out, so the line joins the points on either side instead of dropping to zero (for example across weekends with no logins).

Hover over a point to see its exact value.

---

# 5. Relationship to Other Monitoring Tools

Activity Graphs provide trend visualization, complementing:

- **User Activity Log** ([RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)) — for raw event-level detail and filtering by project or date
- **System Statistics** ([RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md)) — for aggregate counts and high-level metrics
- **Map of Users** ([RC-CC-14 — Control Center: Map of Users](RC-CC-14_Map-of-Users.md)) — for geographic distribution of users
- **Top Usage Report** ([RC-CC-15 — Control Center: Top Usage Report](RC-CC-15_Top-Usage-Report.md)) — for identifying the most active projects and users

---

# 6. Performance and Caching

The charts may take several seconds to load, especially for longer time ranges (Past Year or All). Results are not cached: each chart is calculated live when the page loads, so reloading the page shows current data. The exceptions are **Database Usage (MB)** and **Usage by Uploaded Files (MB)**, which plot one snapshot per day, so today's change shows up after the next daily snapshot.

---

# 7. Common Questions

**Q: What is the default time range shown when I first load the User Activity Graphs page?**
The default time range is "Past Week" (last 7 days). This provides a reasonable balance between showing recent trends and avoiding excessive amounts of historical data. You can change the time range using the navigation buttons at the top of the page.

**Q: Can I zoom in or interact with individual data points on the charts?**
Hovering over a point shows its exact value. To look at a shorter period in more detail, pick a shorter time range.

**Q: What does "Concurrent Users/Respondents" measure?**
For each 30-minute block, it counts the distinct sessions that viewed at least one REDCap page, including survey respondents' sessions. A high peak may indicate a scheduled event, a major launch, or unusual activity. Use this chart to identify periods of highest system load.

**Q: How many new projects (or new users) did we get this month?**
Select **Past Month** and read **Projects Created** (or **First-Time Visitors**). These are running totals, so subtract the value at the first point from the value at the last point. The difference is the number created (or first visiting) in that month.

**Q: Why would the "First-Time Visitors" chart climb steeply at certain times?**
A steep climb means many people used REDCap for the first time in that stretch, for example after an onboarding event, a training session or the launch of a large study. The chart counts a person's first login or visit, not the creation of their account, so users created in bulk only appear once they actually log in.

**Q: How do the User Activity Graphs differ from the User Activity Log?**
User Activity Graphs display trends and summaries over time, providing a high-level overview of usage patterns. The User Activity Log provides detailed, event-by-event information with filtering capabilities. Use graphs for trend analysis and the log for detailed investigations.

**Q: Is the data in the charts real-time, or is there a delay?**
Real-time. Charts are calculated when the page loads, so reload the page to include the latest activity. The two storage charts, **Database Usage (MB)** and **Usage by Uploaded Files (MB)**, are the exception: they show one snapshot per day.

---

# 8. Common Mistakes & Gotchas

**Waiting too long for charts to load on "Past Year" or "All" views.** Querying charts for very long time periods can take considerable time, especially on active instances with years of historical data. Be patient and allow several seconds or minutes for results to load. Switching to a shorter time range will load much faster.

**Reading a running total as a per-day count.** Projects Created, Projects Moved to Production, Active Users, First-Time Visitors, Logged Events and Page Hits are cumulative, so the line only ever rises and its height is the all-time total, not the activity in the period. Use the rise from the first to the last point of the range instead. The charts have no axis titles or legends, and the only units shown are the "(MB)" in two titles. Check the Y-axis values before reading a steep-looking stretch as a large change.

**Reading "Active Users" as the users active in the period.** Active Users is a running total of everyone who has ever had any logged activity, placed on the date of their first activity. Someone who was active every day this week but started using REDCap years ago adds nothing to this week's rise. The rise over the range is therefore the number of users whose first activity fell in that period. To count people who actually used REDCap in a period, use the User Activity Log ([RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)); for the load at any one moment, use Concurrent Users/Respondents.

**Expecting zero on quiet days.** Days with nothing to count are left out rather than plotted as zero, so the line joins straight across them. A smooth line through a weekend does not mean there was activity on Saturday and Sunday.

**Expecting the storage charts to update immediately.** Database Usage (MB) and Usage by Uploaded Files (MB) show one snapshot per day, so a large upload or a data purge today will only appear after the next daily snapshot. All the other charts are live and update when you reload the page.

**Ignoring seasonal or scheduled patterns.** Usage graphs often show predictable patterns (e.g., lower activity on weekends, higher activity during academic terms, spikes around deadlines). Do not be alarmed by regular cycles; instead, use them to establish baselines for detecting truly anomalous activity.

---

# 9. Related Articles

- [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md)
- [RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)
- [RC-CC-14 — Control Center: Map of Users](RC-CC-14_Map-of-Users.md)
