

**Control Center Notifications & Reporting**

| **Article ID** | [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — notifications and stats-reporting behaviour checked against source code; page sections and actions checked live on v17.5.6 (read-only) |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-03 — Control Center: Security & Authentication](RC-CC-03_Control-Center-Security-and-Authentication.md); [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md); [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md)|
| **Synonyms** | control center notifications and reporting dashboard; redcap system health warnings page; control center server configuration alerts; where do i see redcap update alerts; consortium reporting tools in control center; main control center landing page; temp directory and web server warnings; admin notifications and warnings section |

---

## 1. Overview

The Control Center Notifications & Reporting page is the main dashboard administrators land on when accessing the Control Center. Labeled "Notifications & Reporting" in the sidebar, this page displays critical system health information, update alerts, and consortium reporting tools. It serves as the central hub for monitoring REDCap server status and administrative tasks.

---

## 2. System Notifications & Warnings

The Notifications & Warnings section displays alerts about server configuration issues that may impact REDCap functionality and security. Common alerts include:

- **Temp directory access restrictions**: REDCap recommends configuring web servers to restrict public access to temporary directories. This prevents unauthorized access to sensitive files.
- **Web server configuration recommendations**: Alerts specific to your server environment and configuration.

The system provides configuration instructions tailored to common web servers, including NGINX and Apache, to help administrators remediate these issues.

> **Version caveat (16.0 LTS):** the protection file REDCap places in the temp directory only carries the Apache 2.2 access rule, so on Apache 2.4 the temp-directory warning is more likely to appear even though REDCap tried to protect the folder. Apply the web server rule the warning shows you. 17.x releases cover all Apache versions.

Other warnings can appear in this section when the condition applies, for example: cron jobs not running, the Base URL not matching the address in use or using HTTP instead of HTTPS, a database structure that needs fixing, authentication set to "None", files on the server that don't belong to a REDCap version folder, a read replica problem, and an upcoming REDCap+ expiry. Each warning explains the fix or links to the page where you make it.

---

## 3. External Module Update Alerts

When installed external modules have updates available in the REDCap Repository, an update banner is displayed on this page. This allows administrators to:

- **Upgrade all modules at once** for convenience
- **Upgrade individual modules** selectively

Each alert displays:
- Module name
- Currently installed version
- Available version
- Links to Release Notes for reviewing changes before upgrading

On 17.x the alert also warns when an update is a new major version of the module. REDCap checks the REDCap Repository for module updates in a background job about every 3 hours.

> **Version caveat (16.0 LTS):** the alert lists each module's title, the new version and an **Update** button, but not the installed version or Release Notes links. Check the module's page in the REDCap Repository for its release notes before you update.

---

## 4. Easy Upgrade

The Easy Upgrade feature allows administrators to upgrade REDCap to a newer version directly through the browser interface, without requiring direct server access. 

**Requirements:**
- REDCap Community credentials
- Outbound internet access from the server to the Consortium server
- Write access for REDCap to its web root folder
- A database user with rights to create, alter and drop tables

**Important Limitation:** Easy Upgrade cannot be used in load-balanced environments where the REDCap web server uses multiple application servers. In these environments, the downloaded source code would only be deployed to a single server, leaving other servers running outdated code. Load-balanced installations require manual upgrade procedures or coordination with server administrators.

> **Easy Upgrade is not recommended on production servers (16.1.4+; also in 16.0 LTS).** It needs REDCap to be able to write to its own main directory, which the Configuration Check warns against. Read the warning in [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) before enabling it.

---

## 5. Reporting Stats to the Consortium

REDCap administrators are expected to report usage statistics to the REDCap Consortium to support the continued development and maintenance of the REDCap platform. Two reporting methods are available:

**Automatic Reporting (Recommended)**
- Statistics are sent when 7 or more days have passed since the last report and an administrator next opens a Control Center page. There is no fixed weekly schedule, so an instance whose Control Center is rarely visited reports less often.
- Configuration is managed in the Control Center configuration settings
- Requires outbound internet connectivity to the Consortium server
- The **Report my stats** button is greyed out in this mode

**Manual Reporting**
- A "Report my stats" button allows on-demand submission
- Useful for immediate reporting or testing
- A **Try auto-sending stats** option is also offered

**Firewall-Restricted Alternative**
- For organizations with firewalls that prevent outbound connections to the Consortium server, an email-based alternative reporting method is available
- Use the alternative reporting button on this page: it emails your stats to the Consortium, and they are usually posted within 24 hours

**Status & Information**
- The page displays the date statistics were last successfully reported. The date turns amber after 7 days and red after 30 days.
- The current reporting method is shown
- A link to "What stats are sent?" explains which data elements are shared with the Consortium

---

## 6. Other System Information

A **Server info** line at the top of the page shows the REDCap version, the PHP version and server operating system type, and the MySQL version.

The Notifications & Reporting page displays additional system configuration information at the bottom of the notifications section:

- **Date of last REDCap upgrade**: Indicates when the server was last updated
- **REDCap server current time**: Displays the server's local time and timezone
- **PHP.INI path**: Full path to the web server's PHP configuration file
- **PHP error log path**: Full path to the PHP error log file
- **Browser time**: Your computer's current time, for comparison with the server time
- A warning if the cron job uses a different PHP.INI file from the web server

A warning icon appears next to the PHP version when it falls outside the range REDCap supports (8.2 to 8.5 on current versions).

This information is useful for troubleshooting, audit purposes, and verifying server configuration details.

---

## 7. Common Questions

**Q: What should I do if I see an alert about temp directory access restrictions?**
REDCap recommends that web servers restrict public access to temporary directories to prevent unauthorized access to sensitive files. The alert provides configuration instructions for your specific web server (NGINX or Apache). If you see this alert, follow the provided instructions to configure your web server's access controls, then verify the change by checking the Notifications & Reporting page again.

**Q: How often are external module updates checked?**
REDCap checks the REDCap Repository in a background job about every 3 hours, and the update banners appear on the Notifications & Reporting page whenever new versions are available in the REDCap Repository. On 17.x you can review the Release Notes before upgrading to understand what changes are included in each version.

**Q: Can I upgrade REDCap using Easy Upgrade if my system is load-balanced?**
No. Easy Upgrade cannot be used in load-balanced environments because the downloaded code would only be deployed to a single application server, leaving other servers running outdated code. Load-balanced installations require manual upgrade procedures or coordination with your server administrators to upgrade all servers simultaneously.

**Q: Why do I need to report statistics to the REDCap Consortium?**
REDCap is community-driven software maintained by Vanderbilt University. Reporting usage statistics to the Consortium helps support REDCap's continued development and improvement. No project data is sent. The report does identify your institution and the contact name and email on file. If your firewall prevents outbound connections, use the email-based alternative reporting button on the same page.

**Q: How do I know if automatic reporting to the Consortium is working?**
The Notifications & Reporting page displays the date statistics were last successfully reported. If you are using automatic reporting, verify that this date is recent (within the last week; it turns amber after 7 days). Automatic reporting only fires when an administrator opens a Control Center page, so a quiet instance can go longer between reports. If reporting appears to have stopped, check your outbound internet connectivity to the Consortium server or consider the email-based alternative reporting method.

---

## 8. Common Mistakes & Gotchas

**Not monitoring temp directory warnings.** Temp directory access restrictions are a common security misconfiguration that can expose sensitive files. Check the Notifications & Reporting page regularly for these alerts and follow the provided remediation steps promptly. Delaying action on this warning leaves your instance vulnerable.

**Forgetting to review module Release Notes before upgrading.** Upgrading all external modules at once without reviewing their Release Notes can introduce unexpected changes or dependencies. Always review the Release Notes for any updates and test them in a staging environment before deploying to production.

**Neglecting to configure the Easy Upgrade alternative for load-balanced systems.** If your instance uses load balancing, attempting to use Easy Upgrade will result in only one server being updated. This creates version mismatch issues and unpredictable behavior. Plan ahead for manual or coordinated upgrade procedures on load-balanced systems.

---

## 9. Related Articles

- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) (Consortium reporting settings, Easy Upgrade configuration)
- [RC-CC-03 — Control Center: Security & Authentication](RC-CC-03_Control-Center-Security-and-Authentication.md) (server security recommendations)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (external module management overview)
- [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md) (external module concepts and management)
