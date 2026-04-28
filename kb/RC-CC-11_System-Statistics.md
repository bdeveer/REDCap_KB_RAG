RC-CC-11

**System Statistics**

| **Article ID** | RC-CC-11 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-01 — Notifications & Reporting; RC-CC-12 — User Activity Log; RC-CC-13 — User Activity Graphs |

---

# 1. Overview

The System Statistics page provides a comprehensive snapshot of the REDCap instance's usage, configuration, and infrastructure. It is accessible under "Dashboards & Activity" in the Control Center sidebar. Statistics are displayed in a table format and can be exported as a CSV file for further analysis or trend tracking.

---

# 2. Statistics Categories

The System Statistics page displays statistics across multiple categories:

## Projects by Status

- **Development**: Count of projects in development status (not yet in production)
- **Production**: Count of active production projects
- **Analysis/Cleanup**: Count of projects in analysis or cleanup phase
- **Archived**: Count of archived projects
- **Total**: Overall count of all projects on the instance

## User Activity

- **Total registered users**: Count of all user accounts registered on the instance
- **Active users** (by time period): Count of users active within a specified recent time interval (e.g., last 30 days, last 90 days, depending on configuration)
- **Recently logged in users**: Count of users with recent login activity

## Records and Data

- **Total records**: Cumulative count of all records across all projects
- **Data entry records**: Count of records created through standard data entry (not survey responses)
- **Survey responses**: Count of records or responses completed via survey interface

## Survey Usage

- **Survey-enabled projects**: Count of projects with at least one survey instrument
- **Total survey invitations sent**: Count of all survey invitations distributed (across all time)

## API Activity

- **API-enabled projects**: Count of projects with API access enabled
- **API call volume**: Count or frequency of API requests made to the instance

## External Modules

- **Installed modules**: Count of external modules installed on the instance
- **Enabled projects per module**: Breakdown of how many projects have each installed module enabled

## REDCap Features

Statistics on instance-wide feature adoption, including:
- Projects using randomization
- Projects using double data entry (DDV/DDE)
- Projects with alerts or notifications enabled
- Projects with multi-language management enabled
- Projects using MyCap (mobile app integration)
- Projects with eConsent enabled
- Any other feature-specific adoption metrics

## Infrastructure

- **REDCap version**: Current version number of the REDCap installation
- **PHP version**: Version of PHP running on the server
- **Database version**: Version of MySQL, MariaDB, or other database backend in use

## Dynamic Data Pull (DDP)

- **Projects using DDP**: Count of projects with Dynamic Data Pull configured
- **Values pulled**: Count or total number of individual data pulls performed
- **Records imported (loaded dynamically)**: Count of records populated via DDP

## Logged Events

- **Total count of logged events**: Cumulative count of audit log entries across the system (all user actions, data modifications, system changes, etc.)

---

# 3. Dynamic Loading

Some statistics on the System Statistics page are loaded asynchronously after the page renders. These statistics require time-consuming database queries and may not be available immediately:

- **Logged events**: Total count of audit log entries
- **Dynamic Data Pull (DDP)** statistics: Values pulled, records imported

When the page initially loads, these fields display "Loading..." or a similar placeholder. Once the asynchronous query completes (typically within seconds to minutes, depending on database size and server performance), the actual values are populated. Avoid closing or navigating away from the page until all statistics have loaded if you need complete data.

---

# 4. Exporting Statistics

A "Download as CSV" button located on the System Statistics page exports all visible statistics to a CSV file. Key features:

- The exported file includes all statistics currently displayed on the page
- The filename includes the current timestamp (e.g., `system_stats_2026-04-17_14-30-45.csv`)
- The CSV format is suitable for import into spreadsheet applications or data analysis tools
- Exporting is useful for tracking usage trends over time by comparing exported snapshots from different dates

To export:
1. Navigate to the System Statistics page
2. Ensure all statistics have finished loading (no "Loading..." placeholders)
3. Click the "Download as CSV" button
4. Save the file to your local computer
5. Open in your spreadsheet application or data analysis tool as needed

---

# 5. Reporting to the Consortium

The statistics displayed on the System Statistics page overlap with (but are not identical to) metrics reported to the REDCap Consortium. For details on consortium reporting, including which statistics are reported, frequency, and any privacy considerations, see RC-CC-01 — Notifications & Reporting.

---

# 6. FHIR Statistics

A separate System Statistics page is available for FHIR (Fast Healthcare Interoperability Resources) reporting on instances with FHIR integration or Dynamic Data Pull enabled. This page, accessible at `ControlCenter/fhir_stats.php`, displays FHIR-specific metrics and is typically linked in the Control Center sidebar adjacent to the main System Statistics page.

For more information on FHIR integration and statistics, consult your institution's FHIR administrator or the REDCap documentation on FHIR support.

---

# 7. Common Questions

**Q: Why do some statistics show "Loading..." on the System Statistics page?**
Some statistics require time-consuming database queries (such as total logged events and Dynamic Data Pull metrics). These statistics are loaded asynchronously after the page renders to keep the page responsive. Wait a few seconds to a few minutes depending on your database size and server performance.

**Q: Can I export the statistics for use in reports or trend analysis?**
Yes. The "Download as CSV" button exports all visible statistics to a CSV file. The filename includes the current timestamp. You can then import the CSV into spreadsheet applications or data analysis tools to track trends over time by comparing exports from different dates.

**Q: What counts as an "active user" for the purposes of System Statistics?**
Active users are typically counted based on login activity within a specified recent time interval (e.g., last 30 or 90 days, depending on your configuration). The exact definition may vary by REDCap version. Contact your system administrator if you need clarity on the definition used at your institution.

**Q: How do survey responses differ from data entry records in the statistics?**
Data entry records are created by authenticated users entering data manually on forms. Survey responses are created by unauthenticated respondents completing survey instruments. Both count toward the "Total records" metric, but the breakdown allows you to understand the balance between staff data entry and survey-based data collection.

**Q: Are the statistics real-time or is there a delay?**
Most statistics are near real-time, reflecting activity that occurred within the last few minutes. However, asynchronously loaded statistics (like total logged events) may take longer to compute and may reflect data from a few minutes or hours ago, depending on database performance. Plan important statistical reports accordingly.

**Q: Where can I find the REDCap version number on the System Statistics page?**
The REDCap version is listed under the Infrastructure section of the System Statistics page. It shows the current version number of the REDCap installation on your server.

---

# 8. Common Mistakes & Gotchas

**Assuming all statistics are loaded immediately.** Administrators sometimes screenshot or export the System Statistics page before asynchronous statistics have finished loading, capturing incomplete data. Always wait for all "Loading..." placeholders to be replaced with actual values before exporting or relying on the statistics.

**Using old statistics snapshots without verifying current data.** If you export System Statistics regularly for trend tracking, ensure you are comparing apples to apples. The definition of "active users" or counting methodology may change between REDCap versions, making historical comparisons less meaningful. Document the REDCap version and date of each snapshot.

**Not accounting for how DDP and Dynamic Data Pull affect record counts.** If you use Dynamic Data Pull to import records from external systems, these imported records are counted in the "Total records" metric. Be aware that record counts reflect both natively created records and those pulled from external sources. Understanding this helps interpret the statistics correctly.

**Misinterpreting API-enabled projects as projects actually using the API.** The "API-enabled projects" statistic shows how many projects have API access turned on, not how many projects actively use the API. Many projects may be API-enabled but rarely or never use it. Use the User Activity Log or API call volume metrics for actual usage.

**Forgetting that FHIR statistics are separate from main statistics.** If your instance has FHIR integration, remember that FHIR-specific metrics are on a different page (`ControlCenter/fhir_stats.php`). The main System Statistics page may not include all FHIR-related metrics you need for compliance or reporting.

---

# 9. Related Articles

- RC-CC-01 — Notifications & Reporting
- RC-CC-12 — User Activity Log
- RC-CC-13 — User Activity Graphs
