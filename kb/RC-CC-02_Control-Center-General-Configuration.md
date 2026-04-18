RC-CC-02

**Control Center: General System Configuration**

| **Article ID** | RC-CC-02 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-01 — Notifications & Reporting; RC-CC-03 — Security & Authentication; RC-CC-04 — User Settings & Defaults; RC-CC-07 — Users & Access Management; RC-INST-01 — Institution-Specific Settings & Policies; RC-PROJ-01 — Project Lifecycle |

---

The **General Configuration** page contains the core technical and operational settings that govern how REDCap runs at the instance level. It is organized into three sub-sections: **Server Configuration Settings**, **Configuration for Outgoing Emails**, and **Other System Settings**. A separate **Configuration Check** tool also lives under System Configuration.

---

# Configuration Check

The **Configuration Check** tool (Control Center → System Configuration → Configuration Check) tests the current REDCap installation for errors that might prevent the system from functioning correctly. It is a diagnostic read-out only — there are no configurable settings here. Run it after any significant system change, upgrade, or PHP/MySQL configuration edit.

## Basic Tests

Six tests run automatically when the page loads. All six must pass for REDCap to function correctly:

1. **File structure** — Verifies all required REDCap files and folders are present in the web root directory.
2. **Database connection** — Connects to the `redcap_config` table in the MySQL/MariaDB database.
3. **Database table structure** — Confirms the full database schema matches what REDCap expects.
4. **PHP cURL extension** — Required for many REDCap HTTP calls; must be installed and active.
5. **REDCap Consortium server communication** — Tests outbound connectivity to the Consortium server (`redcap.vumc.org/consortium/`), used for weekly site statistics reporting and access to the Shared Library. Failure here does not break core REDCap functionality but will prevent stats reporting and Shared Library use.
6. **Cron job** — Confirms the REDCap Cron Job is running. The cron job handles automated surveys, alerts, scheduled tasks, data quality checks, and other background processes. A failed cron job will silently break many time-dependent features.

## Secondary Tests

These are passive indicator checks shown as pass/warn/fail icons. They do not stop REDCap from loading but indicate configuration gaps:

- **SSL** — REDCap should always be served over HTTPS.
- **PHP 8.1.0 or higher** — Minimum supported PHP version.
- **MySQL/MariaDB 5.5.5 or higher** — Minimum supported database version.
- **GD library (version 2+)** — Required for image processing features.
- **Imagick PHP extension** *(Recommended, not required)* — If not installed, inline PDF attachments on **Descriptive Text** fields will not display inside PDF exports of forms or surveys. Recommended for full PDF functionality.
- **PHP Fileinfo extension** — Required for file-type detection on uploads.
- **REDCap can send emails** — Confirms the mail subsystem is functional.

## MySQL / MariaDB Configuration Recommendations

If REDCap detects suboptimal database server settings, a recommendations block appears. Common recommendation:

> **Too many sorts are causing temporary tables.** Consider increasing `sort_buffer_size` and/or `read_rnd_buffer_size`.

Changes should be made in `my.cnf` (Linux/Unix) or `my.ini` (Windows). Restart the MySQL/MariaDB service after any edit. Always test on a staging environment first — improvements in one area can negatively affect performance in another.

## Directory Writability

The page confirms that the following directories are writable by the web server process:

- **Web server temp directory** (e.g., `/tmp`) — Used by PHP for temporary file operations.
- **REDCap `temp/` directory** — Located inside the REDCap web root; used for temporary exports and processing.
- **`modules/` directory** — Required for External Module installation and updates.

If any directory is not writable, the relevant feature will fail (e.g., module installs, file exports).

## Internal Service Check

Tests that the REDCap server can communicate with its own survey end-point. Failure here means surveys cannot be accessed by participants, even if the main REDCap interface is reachable.

## External Service Checks

Tests outbound connectivity to third-party services. Failures do not break core REDCap but will disable the corresponding feature:

| Service | Purpose |
| --- | --- |
| Twilio | SMS/voice survey invitations and reminders |
| Mosio | SMS messaging service integration |
| PROMIS | NIH PROMIS assessment API (Computer Adaptive Tests) |
| BioPortal | Biomedical ontology lookups in field design |
| REDCAP.LINK | Built-in URL shortener for survey links |
| Field Bank (NLM) | NLM Field Bank for importing standard measures |

## Optional: Add Primary Keys for Clustering / Replication

If the database is configured for clustering or replication (where every table must have an auto-incremented Primary Key), the Configuration Check page provides a block of `ALTER TABLE` SQL statements that adds a `pk_id` primary key to any REDCap tables that lack one. This SQL is only needed in replication setups and should not be run on standard single-server installations. The queries may take minutes to hours to complete on large databases.

---

# MyCap Configuration Check

The **MyCap Configuration Check** (Control Center → System Configuration → MyCap Configuration Check) performs the equivalent health check for the MyCap mobile app module. It is only relevant on instances where MyCap is enabled.

## Basic Tests

Three tests run automatically:

1. **Internal API calls** — Verifies that REDCap can make the internal API calls that MyCap depends on. The page also displays the API endpoint URL (`{your-redcap-base-url}/api/?content=mycap&action=testEndpoint`) that administrators can enter on a mobile device to confirm the endpoint is reachable from outside the network.
2. **TLS 1.2 support** — Confirms the server supports TLS 1.2, required for secure MyCap communication.
3. **MyCap Central communication** — Tests that the REDCap server can reach MyCap Central, the hosted service that facilitates app distribution and participant joining.

All three must pass for MyCap to function.

## Secondary Tests (API Tests)

To run the secondary API tests, select a MyCap-enabled project (one with at least one record) from the dropdown and choose a participant, then click **Execute API Tests**. These tests exercise the full MyCap API call chain and are useful for diagnosing connectivity or configuration issues after a system change.

> The secondary tests require an existing MyCap-enabled project with at least one record. If no eligible projects exist, the secondary tests cannot be run.

---

# Server Configuration Settings

## System Status

Controls whether REDCap is accessible to normal users. Options: **SYSTEM ONLINE** (default) or **SYSTEM OFFLINE**.

When set to Offline, all normal (non-admin) users are denied access to all pages. Administrators can still log in.

An optional **custom offline message** can be set — the text shown to users when they try to access REDCap while it is offline. HTML is supported in this message, allowing you to include formatted text, links to a status page, or estimated downtime information.

## Language Displayed for Global Pages

Sets the default language for system-level pages (login page, home page, and other non-project pages). English is the standard default. Language files can be downloaded from the REDCap Community Language Library or created using the built-in Language File Creator/Updater tool.

> Changing the global language does not automatically change the default language for existing or new projects. That default is set separately on the Default Project Settings page.

## Read Replica Database

Optionally connects REDCap to a read-only MySQL/MariaDB replica database to offload read-heavy operations and improve performance under load. When enabled, the replica handles: viewing reports, data exports (including API exports), record status dashboards, logging, data search, scheduling, data quality rule execution, project dashboards, and the Control Center's System Statistics and User Activity Log pages.

The replica is only used when its lag time behind the primary is 3 seconds or less, preventing stale data from being displayed.

**Setup requires:**
1. A replica database server running MySQL/MariaDB replication from the primary
2. Connection variables added to `database.php` on the REDCap web server
3. The feature enabled on this page

> This setting is only recommended if routine performance issues have already been investigated and other improvements (hardware, indexing) have not resolved them. Setup should be performed by a database administrator.

## Automatically Send Basic Statistics to REDCap Consortium

Controls whether REDCap automatically sends anonymized usage statistics to the REDCap Consortium (projectredcap.org). Statistics include user counts, project purpose counts, REDCap version, authentication method, and module usage. No project data is sent. If set to manual, the administrator must click a button on the Notifications & Reporting page to send stats.

## REDCap Base URL

The public-facing root URL of the REDCap installation (e.g., `https://redcap.[your-institution].edu/`). REDCap uses this to construct all internal links and survey invitation URLs. This value is typically set during initial installation and should match the actual URL through which users access the system.

> A warning is displayed on this page if the saved Base URL does not match the URL from which the administrator is currently accessing REDCap.

## Survey Base URL (optional)

An alternative base URL used only when constructing survey links. Leave blank if survey URLs should use the same base as the main REDCap URL. Useful when a reverse proxy or separate web server hosts the surveys on a different domain than where users log in.

## Proxy Server

If the REDCap web server must route outbound HTTP calls through a proxy, enter the proxy hostname and port here. Optionally add `username:password` credentials in the second field if the proxy requires authentication. These settings apply only to outbound requests originating from the REDCap server (e.g., API calls, third-party integrations).

## Is This a Development/Test/Staging Server?

When set to Yes, PHP error reporting is enabled on all pages to aid with debugging. This should only be set to Yes on non-production servers. Production instances should always be set to No.

## Can REDCap Server Access the Web?

Controls whether REDCap attempts to make outbound HTTP calls. If the server has no internet connectivity and this is left as Yes, some pages or services can become extremely slow or fail to load entirely. Set to No for air-gapped or restricted-network installations.

## REDCap Hooks

Specifies the full file path to a PHP file on the REDCap web server that contains REDCap hook functions. Hooks allow administrators to inject custom PHP code into specific points in REDCap's execution. Leave blank if hooks are not in use. See Plugin, Hook, & External Module Documentation (accessible from the Administrator Resources menu) for guidance.

---

# Configuration for Outgoing Emails

## Universal FROM Email Address (optional)

Sets a single email address used as the "From" sender for **all** outgoing emails from REDCap, regardless of who triggered the email. All emails will still carry a "Reply-To" value reflecting the actual sender.

This setting is primarily needed when the REDCap server's SMTP configuration rejects emails whose "From" address does not match the server's sending domain — a common issue when users have external email addresses (Gmail, Yahoo, etc.) configured in their REDCap profiles.

Leave blank to allow each email to show the actual sender's address as "From."

## Universal DO-NOT-REPLY Email Address (optional)

A separate address used as the sender for system-generated emails (User Access Dashboard reminders, admin notifications, Messenger notifications). This address is not monitored and users are not expected to reply to it. When a Universal FROM address is set, it takes precedence as the visible "From" address, while the DO-NOT-REPLY address functions as the Reply-To.

## Suppress Universal FROM for Specific Email Domains

A domain-level exception list for the Universal FROM address. Enter one domain per line (e.g., `yourinstitution.edu`). Emails where the original sender's address matches one of these domains will be sent with the sender's own address as "From," bypassing the Universal FROM override. Useful when most system emails need the universal address, but emails from certain internal senders should preserve their own identity.

## Utilize Display Name in All Outgoing Emails

Controls whether REDCap includes the sender's display name alongside their email address in outgoing mail (e.g., `Jane Smith <jane.smith@example.edu>`). When disabled, recipients only see the raw email address. Hiding the display name is occasionally necessary when an institution's email servers are blocking or filtering messages due to display name format issues.

---

# Third-Party Email Service Configuration (optional)

REDCap can route outgoing emails through an external email delivery API instead of the server's default PHPMailer. The following services are supported. Only one should be configured at a time; leave others blank.

> **Note:** The Modules/Services Configuration page has a separate SendGrid setting specifically for enabling SendGrid *template-based* emails within Alerts & Notifications. The SendGrid API key entered here in General Configuration is for using SendGrid as the general email delivery provider for all outgoing REDCap emails.

## Mandrill (MailChimp)
Enter the Mandrill API key from your MailChimp/Mandrill account. See [mandrillapp.com/api/docs/](https://mandrillapp.com/api/docs/) for setup.

## SendGrid
Enter the SendGrid API key from your SendGrid account. See [app.sendgrid.com/guide](https://app.sendgrid.com/guide) for setup.

## Mailgun
Enter the Mailgun API key, the Mailgun domain name, and optionally a custom base URL (defaults to `https://api.mailgun.net`; use `https://api.eu.mailgun.net` for EU-region accounts). See [app.mailgun.com/app/domains](https://app.mailgun.com/app/domains) for setup.

## Azure Communication Services
Enter the Azure Communication Services API key and endpoint URL (e.g., `https://[your-resource].communication.azure.com/`). See [Microsoft Azure documentation](https://learn.microsoft.com/en-us/rest/api/communication/email) for setup.

> **Limitations:** Due to Microsoft API constraints, inline images in email bodies are converted to attachments when sent via Azure Communication Services. Additionally, the true sender's display name and email address cannot be shown to recipients — only the Universal FROM address will appear.

---

# Other System Settings

## Administrator Contact Information

- **Name of REDCap Administrator** — Displayed on the REDCap home page and in system messages as the support contact. Use a team name rather than an individual's name for continuity (e.g., "REDCap Support Team").
- **Email Address of REDCap Administrator** — The contact email for administrator support inquiries.
- **Alternate URL for "Contact REDCap Admin" links** — By default, the "Contact REDCap Admin" link in each project opens a pre-formatted email to the admin address. Entering a URL here overrides this behavior: clicking the link navigates to the specified URL in a new tab. Useful for routing support requests through a ticketing system or help desk portal.

## Institutional Identity

- **Name of Institution** — The official name of the institution, shown in the REDCap header and on project pages.
- **Name of Organization at Institution** — An optional sub-unit name (e.g., a research center or core facility) shown alongside the institution name.
- **Grant Name to be Cited** — If the REDCap instance is supported by a grant, the grant award number or name can be entered here. It is displayed when users export data. Leave blank if not applicable.

## Custom Logo

Enter a URL pointing to an institutional logo image (max 650 pixels wide). This logo is displayed at the top of project pages across the instance. The logo can be hosted on the REDCap server itself (e.g., in the File Repository of a designated admin project) or at any publicly accessible URL.

## Field Comment Log Default

Controls whether the Field Comment Log is enabled by default for all newly created projects. When enabled, every new project starts with the Field Comment Log turned on; project administrators can disable it per-project if needed from the Project Setup page.

## Record Limit for Development Projects

Sets a maximum number of records that can be created in a project while it is in Development status. A value of `0` means no limit. When the limit is exceeded, users see a warning and cannot create additional records until the project moves to Production. A project-level override is available on the Edit Project Settings page.

> This setting is useful for preventing development projects from accumulating large amounts of test data, but use with care — teams occasionally need many test records for complex projects.

## Cron Jobs: Maximum Concurrent Jobs

Sets the maximum number of REDCap cron jobs that may run simultaneously across the entire system. Allowed range: 1–50; default: 10. Increasing this value allows more background jobs to run in parallel but increases server load. Monitor system resources for a few days after any increase.

## Rate Limiter: Page Hit Threshold

Sets the maximum number of web requests per minute allowed from a single IP address before that IP is **permanently banned**. The default is 600 requests/minute. When an IP is banned, an administrator email notification is sent and the IP appears on the Banned IP Addresses page. Set to `0` to disable the rate limiter entirely.

**IP Address Exceptions:** IP addresses or ranges can be excluded from the rate limiter (e.g., for security scanning tools or trusted automated processes). Enter IPv4 addresses, wildcard ranges (e.g., `1.2.3.*`), hyphen ranges (e.g., `1.2.3.0-1.2.3.255`), or IPv6 subnet masks, separated by commas.

## HTTP Compression

When enabled (default), REDCap compresses HTML output using gzip, making pages load 2–5× faster. Should be left enabled unless the web server or a proxy is already handling compression upstream.

## Project Deletion Lag

The number of days between when a user requests project deletion and when REDCap permanently purges it from the database. Default: 30 days. During the lag period the project is hidden from its users but still exists in the database, and an administrator can restore it. After the lag period expires, restoration would require disaster recovery backups.

## MySQL/MariaDB `binlog_format`

An advanced database setting that manually overrides the `binlog_format` for REDCap's database connection. **Leave at the default system setting** unless instructed otherwise by a DBA. Changing this incorrectly can cause serious database issues.

## Check for Identifiers — Keywords

A comma- or line-separated list of keywords used by REDCap's "Check for Identifiers" feature to detect fields that may contain personally identifiable information (PII). REDCap scans field labels and variable names against this list and flags potential identifiers. The default list includes common terms such as: `name, street, address, city, zip, postal, date, phone, fax, mail, ssn, social security, mrn, dob, medical, record, id, age`. Add institution-specific terms as needed.

---

# Custom Text Areas

Four rich-text (HTML) areas can be customized to provide institution-specific messaging to users at key points in the REDCap interface. All four support full HTML.

**Custom text at the top of the Help & FAQ page**
Displayed to all users on the Help & FAQ page. A good location for links to institutional training resources, office hours, support channels, and help documentation.

**Custom text at the top of the Create New Project page**
Displayed when a user begins the project creation process. Use this to provide guidance on naming conventions, institutional requirements, or links to training materials for new project builders.

**Custom popup dialog when creating or copying a project**
A certification/notice dialog that users must dismiss before completing project creation or copy. Use for formal acknowledgment of institutional data policies, terms of use, or data governance requirements.

**Custom popup dialog when moving a project to Production**
A certification/notice dialog displayed at the production move step. Should be concise and include direct links to relevant checklists, policies, or review processes. Avoid walls of text — users will skip it.

---

# Cron Jobs Setup

The dedicated **Cron Jobs** page (Control Center → System Configuration → Cron Jobs) provides setup instructions, diagnostics, and run history for the REDCap background job scheduler.

REDCap requires a cron job on the web server that fires every minute. The cron triggers asynchronous background processes for: automated survey invitations, alert delivery, scheduled data quality checks, and other time-dependent features. A missing or broken cron job silently disables all of these.

## Diagnostic Check

When the page loads, REDCap reports:

| Item | What it shows |
| --- | --- |
| Server type | Windows or Linux/Unix |
| Last cron job ran at | Timestamp of the most recent successful cron execution |
| Cron job status | **Good** if the cron ran recently; a warning or error if overdue |
| Max concurrent cron jobs | The limit set on General Configuration (default: 10) |
| Active cron processes | How many cron workers are currently running |
| Available memory | RAM available to the cron worker (cron runs with a higher memory limit than normal pages) |

## Setup on Linux/Unix (CronTab)

Open a terminal/SSH session and edit the crontab with `crontab -e` (use `sudo crontab -e` if you get a permission denied error). Add the following two lines:

```
# REDCap Cron Job (runs every minute)
* * * * * /usr/local/bin/php /path/to/redcap/cron.php > /dev/null
```

Replace `/usr/local/bin/php` with the actual path to PHP on your server if it differs. Replace `/path/to/redcap/` with the REDCap web root path.

To verify existing cron entries: `crontab -l`

## Setup on Windows (Task Scheduler)

Run the following command in a Windows command prompt to create a scheduled task that fires every minute:

```
schtasks /create /tn "REDCap Cron Job" /tr "/usr/local/bin/php /path/to/redcap/cron.php" /sc MINUTE /ru SYSTEM
```

To run the task under a specific Windows user account, additionally pass:
```
/u [domain\]user /p password /ru {[Domain\]User | "System"} /rp Password
```

## Browser-Based Trigger (Fallback)

If the server-side cron cannot be configured immediately, the cron job can also be triggered manually by navigating to `{your-redcap-base-url}/cron.php` in a web browser. This URL is publicly accessible — anyone who knows it can trigger the cron. This is generally not a security concern on production servers but is worth noting on test/staging servers, where triggering the cron might send unintended emails (copies of those intended for the production instance).

## Cron History

The bottom of the Cron Jobs page shows a log of recent cron executions with timestamps, useful for confirming the scheduler is firing consistently and diagnosing gaps.
