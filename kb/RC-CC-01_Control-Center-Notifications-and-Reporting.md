RC-CC-01

**Control Center Notifications & Reporting**

| **Article ID** | RC-CC-01 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-03 — Security & Authentication; RC-CC-09 — To-Do List; RC-CC-11 — System Statistics |

---

# 1. Overview

The Control Center Notifications & Reporting page is the main dashboard administrators land on when accessing the Control Center. Located at `ControlCenter/index.php` and labeled "Notifications & Reporting" in the sidebar, this page displays critical system health information, update alerts, and consortium reporting tools. It serves as the central hub for monitoring REDCap server status and administrative tasks.

# 2. System Notifications & Warnings

The Notifications & Warnings section displays alerts about server configuration issues that may impact REDCap functionality and security. Common alerts include:

- **Temp directory access restrictions**: REDCap recommends configuring web servers to restrict public access to temporary directories. This prevents unauthorized access to sensitive files.
- **Web server configuration recommendations**: Alerts specific to your server environment and configuration.

The system provides configuration instructions tailored to common web servers, including NGINX and Apache, to help administrators remediate these issues.

# 3. External Module Update Alerts

When installed external modules have updates available in the REDCap Repository, an update banner is displayed on this page. This allows administrators to:

- **Upgrade all modules at once** for convenience
- **Upgrade individual modules** selectively

Each alert displays:
- Module name
- Currently installed version
- Available version
- Links to Release Notes for reviewing changes before upgrading

# 4. Easy Upgrade

The Easy Upgrade feature allows administrators to upgrade REDCap to a newer version directly through the browser interface, without requiring direct server access. 

**Requirements:**
- REDCap Community credentials
- Valid internet connectivity

**Important Limitation:** Easy Upgrade cannot be used in load-balanced environments where the REDCap web server uses multiple application servers. In these environments, the downloaded source code would only be deployed to a single server, leaving other servers running outdated code. Load-balanced installations require manual upgrade procedures or coordination with server administrators.

# 5. Reporting Stats to the Consortium

REDCap administrators are expected to report usage statistics to the REDCap Consortium to support the continued development and maintenance of the REDCap platform. Two reporting methods are available:

**Automatic Reporting (Recommended)**
- Statistics are sent automatically once per week
- Configuration is managed in the Control Center configuration settings
- Requires outbound internet connectivity to the Consortium server

**Manual Reporting**
- A "Report my stats" button allows on-demand submission
- Useful for immediate reporting or testing

**Firewall-Restricted Alternative**
- For organizations with firewalls that prevent outbound connections to the Consortium server, an email-based alternative reporting method is available
- Contact your REDCap administrator for setup

**Status & Information**
- The page displays the date statistics were last successfully reported
- The current reporting method is shown
- A link to "What stats are sent?" explains which data elements are shared with the Consortium

# 6. Other System Information

The Notifications & Reporting page displays additional system configuration information at the bottom of the notifications section:

- **Date of last REDCap upgrade**: Indicates when the server was last updated
- **REDCap server current time**: Displays the server's local time and timezone
- **PHP.INI path**: Full path to the web server's PHP configuration file
- **PHP error log path**: Full path to the PHP error log file

This information is useful for troubleshooting, audit purposes, and verifying server configuration details.

---

# 7. Common Questions

**Q: What should I do if I see an alert about temp directory access restrictions?**
REDCap recommends that web servers restrict public access to temporary directories to prevent unauthorized access to sensitive files. The alert provides configuration instructions for your specific web server (NGINX or Apache). If you see this alert, follow the provided instructions to configure your web server's access controls, then verify the change by checking the Notifications & Reporting page again.

**Q: How often are external module updates checked?**
The system checks for available module updates automatically, and the update banners appear on the Notifications & Reporting page whenever new versions are available in the REDCap Repository. You can review the Release Notes before upgrading to understand what changes are included in each version.

**Q: Can I upgrade REDCap using Easy Upgrade if my system is load-balanced?**
No. Easy Upgrade cannot be used in load-balanced environments because the downloaded code would only be deployed to a single application server, leaving other servers running outdated code. Load-balanced installations require manual upgrade procedures or coordination with your server administrators to upgrade all servers simultaneously.

**Q: Why do I need to report statistics to the REDCap Consortium?**
REDCap is community-driven software maintained by Vanderbilt University. Reporting usage statistics to the Consortium helps support REDCap's continued development and improvement. The statistics sent are anonymized and do not include any project data. If your firewall prevents outbound connections, contact your REDCap administrator about using the email-based alternative reporting method.

**Q: How do I know if automatic reporting to the Consortium is working?**
The Notifications & Reporting page displays the date statistics were last successfully reported. If you are using automatic reporting, verify that this date is recent (within the last week). If reporting appears to have stopped, check your outbound internet connectivity to the Consortium server or consider the email-based alternative reporting method.

---

# 8. Common Mistakes & Gotchas

**Not monitoring temp directory warnings.** Temp directory access restrictions are a common security misconfiguration that can expose sensitive files. Check the Notifications & Reporting page regularly for these alerts and follow the provided remediation steps promptly. Delaying action on this warning leaves your instance vulnerable.

**Forgetting to review module Release Notes before upgrading.** Upgrading all external modules at once without reviewing their Release Notes can introduce unexpected changes or dependencies. Always review the Release Notes for any updates and test them in a staging environment before deploying to production.

**Neglecting to configure the Easy Upgrade alternative for load-balanced systems.** If your instance uses load balancing, attempting to use Easy Upgrade will result in only one server being updated. This creates version mismatch issues and unpredictable behavior. Plan ahead for manual or coordinated upgrade procedures on load-balanced systems.

---

# 9. Related Articles

- RC-CC-02 — Control Center: General System Configuration (Consortium reporting settings, Easy Upgrade configuration)
- RC-CC-03 — Control Center: Security & Authentication (server security recommendations)
- RC-CC-06 — Control Center: Modules & Services (external module management overview)
- RC-EM-01 — External Modules Overview (external module concepts and management)
