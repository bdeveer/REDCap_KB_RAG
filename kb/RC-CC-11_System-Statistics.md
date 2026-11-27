

**System Statistics**

| **Article ID** | [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — System Statistics behaviour checked against source code; checked live on v17.5.6 (read-only): project status rows and the practice-project wording |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md); [RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md); [RC-CC-13 — Control Center: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md)|
| **Synonyms** | control center system statistics page; how many projects and users on the instance; redcap usage and infrastructure snapshot; export system statistics to csv; instance configuration and usage counts; where do i see total project and user account counts; system-wide statistics dashboard admin; redcap server stats overview |

---

## 1. Overview

The System Statistics page provides a comprehensive snapshot of the REDCap instance's usage, configuration, and infrastructure. It is accessible under "Dashboards & Activity" in the Control Center sidebar. Statistics are displayed in a table format and can be exported as a CSV file for further analysis or trend tracking. Every value is calculated live when the page loads (or when you click a **fetch** link); nothing is cached, and the page has no date filters.

---

## 2. Statistics Categories

The page is one long table, grouped into the sections below. This is a summary of what each section covers, not a list of every row; rows for features that are switched off on your instance may be hidden.

### Projects by Status

- **Production**: Count of active production projects
- **Development**: Count of projects in development status (not yet in production)
- **Analysis/Cleanup**: Count of projects in analysis or cleanup phase
- **Completed**: Count of projects marked Completed. A project with a completed date is counted here whatever its earlier status was
- **Total projects**: Count of projects on the instance, **excluding 'practice' projects**. The Modules utilized counts exclude them too

Deleted projects and REDCap's own internal projects are also left out of these totals and of **Modules utilized**. The **Project attributes (all projects)** section, as its name says, counts every project. Each status row has a **view types** link that breaks the count down further.

> **Note:** On 17.5.6 the page lists Production, Development, Analysis/Cleanup and Completed. Older documentation may say Archived.

### Project Types and Purpose

- **Project types**: **Projects containing surveys** (surveys enabled) and **Projects not containing surveys**
- **Project purpose**: Research (with a **view subcategories** link for the research types), Operational Support, Quality Improvement and Other

### Project Attributes (all projects)

Counts across every project, including practice projects:

- **Data collection instruments** and **Fields on all data collection instruments**
- **Survey responses**: responses where at least the first survey page was submitted, so partial responses are included
- **Survey participants (in participants list)**: participants with an email address in a participant list
- **Survey invitations sent**, split into **Responded** and **Not responded**. This counts distinct participants invited, not individual emails, so reminders do not raise it
- **Calendar events** and **Schedules generated**
- **Projects created from a project template**
- **Surveys using Text-to-Speech functionality**

> **Note:** The page has no total record count. There is no row for records created by data entry versus surveys; **Survey responses** is the closest survey measure.

### Modules Utilized

Project counts for feature adoption (practice projects excluded), including:

- Longitudinal (using multiple events) and repeating instruments/events
- Alerts & Notifications (alert count and projects with one or more alerts)
- Double Data Entry
- Randomization
- Data Transfer Service (DTS)
- Dynamic Data Pull (DDP), shown when DDP Custom is enabled, and Clinical Data Pull
- Mobile App (users and projects using the REDCap mobile app)
- MyCap Mobile App (projects, joined participants, tasks created)
- Announcements and messages, Twilio telephony, Mosio SMS and SendGrid email
- REDCap Messenger (conversations and messages sent)
- e-Consent (projects with e-Consent surveys and stored consent PDFs)
- AI Services (projects that have used an AI feature and the number of requests made to the AI service), when AI is enabled

There is no row for Multi-Language Management, no row for External Modules, and no count of API requests.

### Additional 17.x Sections

These blocks appear on REDCap 17.x. Some show only where the feature or a REDCap+ subscription is active:

| Section | What it counts | Shown when |
| --- | --- | --- |
| **Rewards** | Projects using REDCap Rewards, participants compensated, compensation actions and amounts by currency | Feature in use |
| **Project Migration Tool** | Projects migrated off of and to this instance | Always (17.x) |
| **Project Administrator Groups (PAGs)** | Total PAGs, and projects and users assigned to a PAG | Active REDCap+ subscription (changelog: from 17.3.3) |
| **REDCap SHARE** | Projects using SHARE, records and project participants with SHARE data pulled, and EHR systems used | SHARE in use (changelog: from 17.3.1) |
| **Email Verification and Email Unsubscribe Features** | Projects and participants that verified or unsubscribed | Active REDCap+ subscription (changelog: from 17.3.3) |

> **Note:** The distinction drawn in the SHARE totals matters when interpreting them — project participants and EHR-specific REDCap records are counted separately, so the two should not be added together as if they were the same population.

> **Version caveat (REDCap 16.0.x LTS):** The 16.0.x LTS line does not have the SHARE, Project Administrator Groups, Email Verification, Rewards or Project Migration rows (or the Mobile Toolbox rows under MyCap). If you compare CSV exports from a 16.0.x instance with a 17.x instance, expect these rows to be missing on 16.0.x rather than zero. To see them, upgrade to a 17.x release.

### Clinical Data Sections

- **DDP Custom**: four rows (data values pulled, and values, records and projects adjudicated by users). Each value loads only when you click its **fetch** link
- **Clinical Data Pull** and **Clinical Data Mart**: values, records and projects adjudicated or imported. These fill in on their own

### Space Usage

- **MySQL database server**: size of the REDCap database
- **Web server**: space used on the web server
- **External space usage**: shown when files are stored on external storage
- **Total files sent using Send-It**, with past 7 days and past 30 days

The page does not show the REDCap, PHP or database version numbers.

### Logged Events

- **Total logged events**: the all-time total is a **fetch** link you must click; counts for the **Past 30 minutes**, **Today**, **Past 7 days** and **Past 30 days** appear on their own

### User Statistics

- **Users currently logged in**: users active within the auto-logout window, split into **Project users** and **Survey participants** (survey sessions in the last 60 minutes)
- **Total user accounts**
- **Active users**: accounts that have ever performed an action REDCap logged (for example, created a project or entered data), excluding suspended users. There is no time window
- **Non-active users (excluding suspended users)**: accounts with no logged action
- **Suspended users**
- **Median # users per project (prod/analysis-cleanup)** and **Avg/mdn # projects a user can access**
- **Users (table-based authentication)**

### Login Activity

From REDCap **16.0.1**, two counts appear at the bottom of the page, under **Unique user logins (authenticated users)**:

- **Unique users that logged in (past month)**: last login within the past 30 days
- **Unique users that logged in (past 6 months)**: last login within the past 183 days

These measure *distinct users who actually logged in*, which is a different question from how many accounts exist. The gap between total accounts and either figure is the usual starting point for an account cleanup. When the user allowlist is on, only allowlisted and table-based users are counted.

---

## 3. Dynamic Loading

Some rows show "Loading" when the page first opens and fill in on their own a few seconds later, for example the instrument and field counts and the Clinical Data Pull and Data Mart rows.

Two kinds of value never load by themselves. You must click their **fetch** link:

- **Total logged events** (the all-time total)
- The four **DDP Custom** rows

These queries can be slow on a large database. A value you have not fetched is exported blank in the CSV.

---

## 4. Exporting Statistics

A **Download** button on the System Statistics page exports the statistics to a CSV file. Key features:

- The file has two columns, Label and Value, and contains only the rows visible on the page
- The filename includes the date and time the page was loaded, to the minute (e.g., `redcap_system_statistics_2026-04-17_1430.csv`)
- The CSV format is suitable for import into spreadsheet applications or data analysis tools
- Exporting is useful for tracking usage trends over time by comparing exported snapshots from different dates

To export:
1. Navigate to the System Statistics page
2. Wait for the "Loading" placeholders to fill in, and click any **fetch** links whose values you need
3. Click the **Download** button
4. Save the file to your local computer
5. Open in your spreadsheet application or data analysis tool as needed

---

## 5. Reporting to the Consortium

The statistics displayed on the System Statistics page overlap with (but are not identical to) metrics reported to the REDCap Consortium. For details on consortium reporting, including which statistics are reported, frequency, and any privacy considerations, see [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md) — Notifications & Reporting.

---

## 6. FHIR Statistics

A separate **FHIR Statistics** page reports FHIR (Fast Healthcare Interoperability Resources) activity, such as FHIR endpoint requests and resources fetched. Its link appears in the Control Center sidebar only when Clinical Data Interoperability Services (CDIS) are enabled on the instance.

For more information on FHIR integration and statistics, consult your institution's FHIR administrator or the REDCap documentation on FHIR support.

---

## 7. Common Questions

**Q: Why do some statistics show "Loading..." or a "fetch" link on the System Statistics page?**
Some statistics require time-consuming database queries. Rows showing "Loading" fill in on their own after the page renders. The all-time **Total logged events** and the **DDP Custom** rows show a **fetch** link instead; click it to run the query.

**Q: Can I export the statistics for use in reports or trend analysis?**
Yes. The **Download** button exports the visible rows to a CSV file named with the date and time the page was loaded. Fetch any click-to-load values first, or they export blank. You can then compare exports from different dates to track trends.

**Q: What counts as an "active user" for the purposes of System Statistics?**
An account that has ever performed an action REDCap logged, such as creating a project or entering data, and is not suspended. There is no time window. For recent activity, use **Users currently logged in** or the **Unique users that logged in (past month / past 6 months)** rows.

**Q: What does the "Survey responses" count include?**
Survey responses where at least the first page was submitted, across all projects, so partial responses count. The page has no total record count and does not split records by data entry versus survey.

---

## 8. Common Mistakes & Gotchas

**Exporting before click-to-load values are fetched.** Administrators sometimes screenshot or export the System Statistics page before the "Loading" rows have filled in, or without clicking the **fetch** links, capturing incomplete data. Unfetched values export blank. Wait for the placeholders to clear and fetch what you need before exporting.

**Using old statistics snapshots without verifying current data.** If you export System Statistics regularly for trend tracking, ensure you are comparing apples to apples. Rows and counting methods can change between REDCap versions, making historical comparisons less meaningful. Document the REDCap version and date of each snapshot.

**Reading "Active users" as recently active.** **Active users** counts every non-suspended account that has ever done something logged, so it only grows. Use the unique-login rows to see who has logged in recently.

**Forgetting that FHIR statistics are separate from main statistics.** If your instance has FHIR integration, FHIR-specific metrics are on the separate **FHIR Statistics** page in the Control Center sidebar. The main System Statistics page does not include all FHIR-related metrics you may need for compliance or reporting.

---

## 9. Related Articles

- [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md)
- [RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)
- [RC-CC-13 — Control Center: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md)
