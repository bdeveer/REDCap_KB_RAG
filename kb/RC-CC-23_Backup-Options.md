RC-CC-23

**Backup Options**

| **Article ID** | RC-CC-23 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators and project managers |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-API-36 — Export Project XML API; RC-API-37 — Import Project (Create Project) API; RC-CC-21 — Control Center: Overview & Navigation |

---

# 1. Overview

REDCap does not include a built-in scheduled backup system accessible to end users. Instead, backup coverage comes from two distinct layers: **project-level backups** that any authorized project user or administrator can trigger manually, and **infrastructure-level backups** that are configured and managed by the institution's IT or database administration team outside of the REDCap application. This article explains both layers, walks through the project XML export as the primary user-accessible backup mechanism, and clarifies what is and is not captured by each approach.

---

# 2. Key Concepts & Definitions

### Project XML Export
The primary user-accessible backup mechanism. A project XML export produces a single file in **CDISC ODM format** (Operational Data Model version 1.3.1) that encodes the project's structure — all instruments, fields, events, arms, branching logic, and validation settings — and optionally includes all data records. This file can be used to recreate the project on any REDCap instance.

### Metadata-Only Export
A project XML export that includes only the project's structure (instruments, fields, events, arms, logic) with no data records. Useful for backing up the project design before making structural changes, or for cloning an empty project template.

### Full Export (Metadata + Data)
A project XML export that includes both the project structure and all data records. This is the closest equivalent to a complete project backup that REDCap provides at the application level.

### Project Copy
A separate REDCap function that creates a new project with the same structure as an existing project, but contains no data. A project copy is a design clone, not a backup — it cannot be used to restore data.

### Infrastructure-Level Backup
A server- or database-level backup of the REDCap MySQL/MariaDB database, configured and managed by the hosting institution's IT team. This captures the entire REDCap instance — all projects, all data, all user accounts — and is independent of any action taken within the REDCap application.

### CDISC ODM Format
A standardized XML format used for clinical trial data and metadata. REDCap exports project XML in ODM version 1.3.1, which enables portability across REDCap instances and to other ODM-compatible systems.

---

# 3. Project-Level Backup via XML Export

## 3.1 Accessing the Export from the Project UI

The project XML export is available from the **Project Setup** page under the **Other Functionality** tab. Look for the option labeled **Download a backup of the entire project (as a .zip archive)**. Clicking this generates and downloads a ZIP file containing the ODM XML of the project.

By default, the ZIP export includes both metadata and all data records. A metadata-only option is available if you only need to back up the project structure.

> **Note:** This option requires the user to have appropriate project access. A project-level administrator or a user with Data Export rights can perform this action. Check with your REDCap administrator if the option is not visible.

## 3.2 Accessing the Export via API

For automated or programmatic backups, the same export is available via the **Export Project XML API** (see **RC-API-36 — Export Project XML API**). The API provides additional control over what is included:

- Set `returnMetadataOnly=true` to export structure only (no data)
- Use `records`, `fields`, `events`, or `filterLogic` parameters to limit which data records are exported
- Set `exportFiles=true` to embed file upload attachments in the XML (note: this can produce very large exports)

The API approach is the recommended method for scheduled or recurring backups, as it can be automated using a scripted process running on a schedule.

## 3.3 What Is Included in the XML Export

| Element | Included |
| --- | --- |
| All instruments and field definitions | ✓ |
| Field labels, validation rules, choice lists | ✓ |
| Branching logic | ✓ |
| Calculated field expressions | ✓ |
| Events and arms (longitudinal projects) | ✓ |
| Instrument-event mappings | ✓ |
| Repeating instruments and events configuration | ✓ |
| Survey settings (enabled surveys, survey options) | ✓ |
| All data records (when not metadata-only) | ✓ |
| Data Access Group assignments per record | ✓ (with `exportDataAccessGroups=true` via API) |
| Survey field identifiers and timestamps | ✓ (with `exportSurveyFields=true` via API) |
| File upload field attachments | ✓ (with `exportFiles=true` via API only) |

## 3.4 What Is NOT Included in the XML Export

| Element | Not Included | Notes |
| --- | --- | --- |
| User accounts and user rights | ✗ | Must be re-configured after restore |
| Data Access Group definitions | ✗ | DAG names and assignments must be recreated |
| Custom reports | ✗ | Reports must be recreated manually |
| Audit log / logging history | ✗ | Log data is not exportable as part of a backup |
| Survey invitation queue and history | ✗ | Invitation records are not preserved |
| External module configurations | ✗ | Module settings must be reconfigured |
| Randomization setup | ✗ | Randomization tables must be rebuilt |
| Scheduled alerts | ✗ | Alerts must be recreated after restore |
| File attachments (File Repository) | ✗ | Repository files are not included in project XML |
| API tokens | ✗ | Tokens are tied to user accounts, not the project |

> **Important:** For critical projects with file uploads, randomization, or complex user rights, a project-level XML backup alone may not be sufficient for full recovery. Coordinate with your institution's IT team to ensure infrastructure-level backups capture these elements.

---

# 4. Restoring from a Project XML Backup

Restoring from a project XML backup means creating a new REDCap project using the exported file. REDCap does not support overwriting an existing project with an XML restore — the process always produces a new project.

## 4.1 Restore via the REDCap UI

1. Go to the REDCap home page and click **New Project**.
2. On the Create Project page, select the option to **Upload a REDCap project XML file** (or equivalent wording — the upload option appears alongside the blank project and template options).
3. Upload the `.xml` file (or the `.zip` containing it) from your backup.
4. Complete the project creation form (title, purpose, etc.) and submit.
5. The new project will be created with the structure and data from the backup.

> **Note:** After restore, user rights, Data Access Groups, custom reports, and other non-exported elements must be reconfigured manually.

## 4.2 Restore via API

Use **RC-API-37 — Import Project (Create Project) API** to programmatically create a new project from an ODM XML string. This is equivalent to the UI upload but scriptable. The API requires a super API token (a special token that allows project creation) provided by a REDCap administrator.

## 4.3 Cross-Instance Restores

An ODM XML export from one REDCap instance can be imported into a different REDCap instance, provided both instances are running compatible REDCap versions. This makes the project XML export useful for migrating projects between institutions or between development and production environments.

> **Note:** External module configurations, institution-specific settings, and features not present on the destination instance will not carry over.

---

# 5. Infrastructure-Level Backups

Infrastructure-level backups are the responsibility of the institution hosting the REDCap server, not of individual REDCap administrators or project managers working within the application.

## 5.1 What Is Covered

A server- or database-level backup captures the entire REDCap MySQL/MariaDB database, which includes everything that the project XML export does not: user accounts and rights, audit logs, file repository contents, randomization tables, custom reports, survey invitation history, and all project data across every project on the instance.

## 5.2 Configuring Database Backups

Database backup scheduling and configuration is handled by your institution's IT infrastructure team, not through the REDCap Control Center. REDCap does not provide a built-in database backup scheduler or configuration interface within the application itself.

Administrators who need to verify backup schedules or recovery procedures should contact their institution's IT team or database administrators.

## 5.3 What Administrators Can Monitor

Within the Control Center, the **Cron Jobs** page (under System Configuration) shows the status of REDCap's scheduled background processes. This is not a backup configuration interface, but it confirms that REDCap's internal maintenance tasks are running. See **RC-CC-21 — Control Center: Overview & Navigation** for the Cron Jobs location.

---

# 6. Backup vs. Project Copy

These two features are sometimes confused:

| | **Project XML Export (Backup)** | **Copy Project** |
| --- | --- | --- |
| **Data included** | Yes (full export) or No (metadata-only) | Never |
| **Restores to a new project** | Yes | Yes |
| **Preserves record data** | Yes (full export) | No |
| **Preserves user rights** | No | No |
| **Use case** | Disaster recovery, archiving | Creating a blank copy of a project design |

Use **Project XML Export** when you need to preserve or restore actual data. Use **Copy Project** when you want to reuse a project design for a new study or new cohort without carrying over any existing records.

---

# 7. Automated Backup Approaches

REDCap does not provide a native scheduled backup feature accessible from the project interface. Teams that need recurring automated backups have two practical options:

**API-based scripted backups:** Use the Export Project XML API (RC-API-36) in a scheduled script (cron job, task scheduler, etc.) to automatically export the project XML on a defined interval — for example, nightly or weekly. The script can save the resulting XML file to a secure network location with a timestamped filename. This is the most reliable way to achieve project-level automated backups without involving IT infrastructure.

**Infrastructure-level backup:** As described in Section 5, the institution's IT team can configure server-level database backups on a scheduled basis. This is the most comprehensive option, but it requires coordination outside of REDCap and recovery requires IT assistance.

---

# 8. Common Questions

**Q: How do I back up my REDCap project?**
**A:** Go to Project Setup → Other Functionality and download the project ZIP archive. This produces an ODM XML file containing your project structure and data. For recurring backups, use the Export Project XML API (RC-API-36) in an automated script.

**Q: Can I restore a project from a backup without losing the original?**
**A:** Yes. Restoring always creates a new project — REDCap does not overwrite an existing project. Your original project remains unchanged, and the restored backup becomes a separate project that you can compare or rename.

**Q: Does the project XML export include file uploads from File Upload fields?**
**A:** Not by default. File attachments are excluded from the standard project XML download in the UI. Via the API, you can set `exportFiles=true` to embed file attachments, but this can make the export very large. File Repository contents are not included in any project XML export.

**Q: Does the project XML export include user rights?**
**A:** No. User accounts, user rights, and user-role assignments are not included in the project XML. After restoring from backup, you must reconfigure user access manually.

**Q: Can I use my backup to move my project to a different institution's REDCap?**
**A:** Yes, with limitations. The ODM XML file can be imported on any REDCap instance. However, features specific to the source instance (external modules, institutional integrations, field validation types not enabled on the destination) may not carry over. Test the import in a development environment before relying on it for a critical migration.

**Q: Who is responsible for making sure my REDCap data is backed up?**
**A:** Responsibility is shared. Project managers and administrators are responsible for maintaining project-level XML backups. The institution's IT team is responsible for infrastructure-level database backups. For critical studies, both layers of backup are recommended.

**Q: Is there a way to schedule automatic backups within REDCap?**
**A:** Not natively. REDCap does not include a built-in scheduled backup feature. Automation requires using the API in an external script or relying on IT-managed infrastructure backups.

**Q: What is the difference between a backup and a project copy?**
**A:** A project copy duplicates the project design (instruments, fields, logic) with no data. A backup (full XML export) preserves both the project design and all data records. Use project copy for reusing a design; use a backup for disaster recovery or archiving.

**Q: Can I restore just a subset of records from a backup?**
**A:** Not directly via the restore process. The project XML import always creates a new project with everything in the file. To restore only a subset of records, import the full backup into a new project, then re-export just the records you need and import them into your production project using the data import process.

---

# 9. Common Mistakes & Gotchas

**Assuming the UI export always includes all data.** The standard project ZIP download from Project Setup → Other Functionality includes data by default, but if you accidentally choose a metadata-only export, data records will not be in the file. Always verify that the ZIP file contains a reasonably sized XML file — a very small file is likely metadata-only.

**Forgetting that user rights are not backed up.** This is the most common oversight after a restore. After creating a new project from an XML backup, the project has no users assigned. You must re-add all users and configure their rights before the project is usable. Consider keeping a separate record (screenshot or export from Users → User Rights) of your user rights configuration.

**Thinking a project copy is a backup.** The Copy Project function is frequently mistaken for a backup because it creates what looks like a duplicate project. However, it copies only the design — no data. If you later need to recover records, a project copy is useless. Always use the XML download for backup purposes.

**Not testing the restore before you need it.** An XML backup file that cannot be imported successfully is worthless in an emergency. Periodically test your backup by importing it into a development environment and confirming that the data and structure appear correct.

**Relying solely on project-level backups for compliance-critical data.** Project XML exports do not capture the audit log, randomization tables, or file attachments by default. If your project is subject to regulatory requirements, coordinate with IT to confirm infrastructure-level backups are covering these elements, and document your backup strategy.

**Exporting with `exportFiles=true` without checking project size.** Including file attachments in the API export can produce extremely large XML files that may time out or fail to complete on projects with many or large files. Test with a small record subset first before running a full file-inclusive export.

---

# 10. Related Articles

- RC-API-36 — Export Project XML API
- RC-API-37 — Import Project (Create Project) API
- RC-CC-21 — Control Center: Overview & Navigation
- RC-EXPRT-01 — Data Export: Overview & Workflow
- RC-EXPRT-02 — Data Export: Export Formats
