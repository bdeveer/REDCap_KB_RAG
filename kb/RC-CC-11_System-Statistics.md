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

# 3. Dynamic Loading

Some statistics on the System Statistics page are loaded asynchronously after the page renders. These statistics require time-consuming database queries and may not be available immediately:

- **Logged events**: Total count of audit log entries
- **Dynamic Data Pull (DDP)** statistics: Values pulled, records imported

When the page initially loads, these fields display "Loading..." or a similar placeholder. Once the asynchronous query completes (typically within seconds to minutes, depending on database size and server performance), the actual values are populated. Avoid closing or navigating away from the page until all statistics have loaded if you need complete data.

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

# 5. Reporting to the Consortium

The statistics displayed on the System Statistics page overlap with (but are not identical to) metrics reported to the REDCap Consortium. For details on consortium reporting, including which statistics are reported, frequency, and any privacy considerations, see RC-CC-01 — Notifications & Reporting.

# 6. FHIR Statistics

A separate System Statistics page is available for FHIR (Fast Healthcare Interoperability Resources) reporting on instances with FHIR integration or Dynamic Data Pull enabled. This page, accessible at `ControlCenter/fhir_stats.php`, displays FHIR-specific metrics and is typically linked in the Control Center sidebar adjacent to the main System Statistics page.

For more information on FHIR integration and statistics, consult your institution's FHIR administrator or the REDCap documentation on FHIR support.
