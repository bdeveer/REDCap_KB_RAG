

**Backup Options**

| **Article ID** | [RC-CC-23 — Backup Options](RC-CC-23_Backup-Options.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators and project managers |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — project XML, copy and backup behaviour checked against source code; earlier live check (v17.5.6) of the Other Functionality button labels kept; pages not re-captured |
| **Prerequisite** | None |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md); [RC-API-37 — Import Project (Create Project) API](RC-API-37_Import-Project-Create-Project.md); [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md); [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md) |
| **Synonyms** | how do i back up my redcap project; export project as xml backup; does redcap have automatic backups; restore a project from a backup file; save project structure before making changes; metadata only vs full project export; recreate a project on another redcap instance; what is and isn't captured in a backup; cdisc odm xml export |

---

## 1. Overview

REDCap does not include a built-in scheduled backup system accessible to end users. Instead, backup coverage comes from two distinct layers: **project-level backups** that an authorized project user or administrator can trigger manually, and **infrastructure-level backups** that are configured and managed by the institution's IT or database administration team outside of the REDCap application. This article explains both layers, walks through the project XML export as the primary user-accessible backup mechanism, and clarifies what is and is not captured by each approach.

---

## 2. Key Concepts & Definitions

#### Project XML Export
The primary user-accessible backup mechanism. A project XML export produces a single `.xml` file in **CDISC ODM format** (Operational Data Model version 1.3.1) that encodes the project's structure — all instruments, fields, events, arms, branching logic, and validation settings — plus, if you choose, many project settings and the data records. This file can be used to create a new project from it, on the same or another REDCap instance.

#### Metadata-Only Export
A project XML export that includes only the project's structure and settings, with no data records. Useful for backing up the project design before making structural changes, or for reusing an empty project template.

#### Full Export (Metadata + Data)
A project XML export that includes both the project structure and the data records. This is the closest equivalent to a complete project backup that REDCap provides at the application level, but it still leaves out some things (see §3.4).

#### Project Copy
A separate REDCap function (**Copy the project**) that creates a new project on the same server from an existing one. You choose what comes along: the records (optional), the users, roles, reports, alerts and other settings, each with its own checkbox. A project copy is useful, but it is not a backup — it never copies the logging history, and it lives on the same server as the original rather than in an offline file you can keep elsewhere.

#### Infrastructure-Level Backup
A server- or database-level backup of the REDCap MySQL/MariaDB database, configured and managed by the hosting institution's IT team. This captures the entire REDCap instance — all projects, all data, all user accounts — and is independent of any action taken within the REDCap application.

#### CDISC ODM Format
A standardized XML format used for clinical trial data and metadata. REDCap exports project XML in ODM version 1.3.1, which enables portability across REDCap instances and to other ODM-compatible systems.

---

## 3. Project-Level Backup via XML Export

### 3.1 Accessing the Export from the Project UI

The project XML export is available from the **Project Setup** page under the **Other Functionality** tab, in the **Copy or Back Up the Project** section. On 17.5.6 there are two buttons:

- **Download metadata only (XML)** — the project structure and settings, with no data records
- **Download metadata & data (XML)** — the structure, settings and the data records

Neither button is a default; they are separate choices. Each opens a dialog where you pick what to include, and the download is a single `.xml` file.

> **Version caveat:** Older versions of this article described a single **Download a backup of the entire project (as a .zip archive)** option. That does not match current versions: there is no ZIP, the download is one `.xml` file, and metadata and data are separate buttons. The 17.5.6 labels above were read from the page.

> **Note:** You need **Project Design & Setup** rights to see this section. The **Download metadata & data (XML)** button also needs Data Export rights — without them it appears greyed out. Administrators can turn the project XML export off for the whole server, in which case the buttons do not appear at all. Check with your REDCap administrator if the option is not visible.

> **Important:** A data backup made from the UI applies the export rights of the person who downloads it. If your export rights are restricted (de-identified export, removal of identifiers, or a Data Access Group limit), the backup contains only what you are allowed to export, and it is incomplete. Make backups with an account that has full export rights to all instruments and is not in a Data Access Group.

> **Version caveat (17.x):** On 17.x the Other Functionality page may also show **Migrate the project to another REDCap server** (the Project Migration Tool, which needs REDCap+ on the destination and is shown only when the administrator allows it). Unlike the XML export, it moves data, uploaded files, logging, File Repository contents and External Module settings. It is not shown on 16 LTS. See [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md).

### 3.2 Accessing the Export via API

For automated or programmatic backups, the same export is available via the **Export Project XML API** (see **[RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md)**). The API provides additional control over what is included:

- Set `returnMetadataOnly=true` to export structure only (no data)
- Use `records`, `fields`, `events`, or `filterLogic` parameters to limit which data records are exported
- Set `exportFiles=true` to embed uploaded files in the XML (note: this can produce very large exports)
- Set `exportSurveyFields=true` to include survey identifiers and timestamps

Via the API, all the optional project settings are included by default. Exporting data through the API needs full export rights to all instruments.

The API approach is the recommended method for scheduled or recurring backups, as it can be automated using a scripted process running on a schedule.

### 3.3 What Is Included in the XML Export

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
| Optional project settings (see §3.4) | ✓ (ticked by default in the UI) |
| All data records (when not metadata-only) | ✓ |
| Data Access Group assignments per record | ✓ (with `exportDataAccessGroups=true` via API) |
| Survey identifiers and timestamps | API only, with `exportSurveyFields=true` |
| Files uploaded to File Upload and signature fields | ✓ (tick **Include all uploaded files and signatures?** in the data dialog, unticked by default; `exportFiles=true` via API) |

### 3.4 Optional Settings and What Is Never Included

When you download the XML from the UI, the dialog lists the optional parts under **Include the following in the XML file:**. Each is a checkbox, ticked by default, and a checkbox appears only if the project actually uses that feature. Via the API, all of them are included by default.

**Can be included (optional checkboxes):**

| Element | Notes |
| --- | --- |
| User roles | Role definitions only — not which users hold them |
| Data Access Groups | Group names |
| Reports and report folders | |
| Alerts & Notifications | Arrive switched off after restore unless **leave enabled** is ticked; always off when restored via the API |
| Automated survey invitations (ASIs) | Same as alerts: switched off unless **leave enabled** is ticked; always off via the API |
| Survey Queue | |
| Data Quality rules | |
| Project dashboards | |
| Multi-Language Management settings | |
| Form display logic | |
| Randomization settings | The setup only, not the allocation table |
| MyCap, record locking, e-Consent and PDF snapshot settings | |

> **Version caveat (16 LTS vs 17.x):** Newer versions can include more in the XML: 17.3 LTS and later offer Rewards and REDCap SHARE options that 16 LTS lacks, and AI chatbot settings are present in 17.6. If you restore such a file on an older server, those parts may be ignored — check them after restore.

**Never included:**

| Element | Notes |
| --- | --- |
| User accounts and their rights assignments | Only roles travel; after restore, re-add users and assign them to roles |
| Logging history | Download it separately from the **Logging** page (see [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md)) |
| Survey invitation history and participant lists | Invitation records are not preserved |
| Randomization allocation tables | The allocation table must be uploaded again |
| File Repository files | Download them separately |
| External Module settings | Module settings must be reconfigured |
| API tokens | Tokens are tied to user accounts and must be requested again |

> **Important:** For critical projects with file uploads, randomization, or complex user rights, a project-level XML backup alone may not be sufficient for full recovery. Coordinate with your institution's IT team to ensure infrastructure-level backups capture these elements.

---

## 4. Restoring from a Project XML Backup

Restoring from a project XML backup means creating a new REDCap project using the exported file. REDCap does not support overwriting an existing project with an XML restore — the process always produces a new project.

### 4.1 Restore via the REDCap UI

1. Go to the REDCap home page and click **New Project**.
2. On the Create Project page, select the option to **Upload a REDCap project XML file** (or equivalent wording — the upload option appears alongside the blank project and template options).
3. Upload the `.xml` file from your backup.
4. Complete the project creation form (title, purpose, etc.) and submit.
5. The new project will be created with the structure, the settings included in the file, and the data.

> **Note:** The upload is limited by the server's maximum upload size. A large XML file — especially one with embedded uploaded files — may be too big to restore through the UI. Use the API, or ask your administrator.

> **Note:** After restore you are a user of the new project and the roles from the file exist, but no other users are added. Re-add the other users and assign them to roles. Alerts and ASIs need switching on again unless you ticked **leave enabled**, and anything listed as never included in §3.4 must be reconfigured manually.

### 4.2 Restore via API

Use **[RC-API-37 — Import Project (Create Project) API](RC-API-37_Import-Project-Create-Project.md)** to programmatically create a new project from an ODM XML string. This is equivalent to the UI upload but scriptable. The API requires a super API token (a special token that allows project creation) provided by a REDCap administrator.

### 4.3 Cross-Instance Restores

An ODM XML export from one REDCap instance can be imported into a different REDCap instance. This makes the project XML export useful for migrating projects between institutions or between development and production environments. It is safest when the destination runs the same or a newer REDCap version than the source; a file from a newer version may contain settings the older server does not recognise. Test the import before relying on it.

> **Note:** External Module settings, institution-specific settings, and features not present on the destination instance will not carry over.

---

## 5. Infrastructure-Level Backups

Infrastructure-level backups are the responsibility of the institution hosting the REDCap server, not of individual REDCap administrators or project managers working within the application.

### 5.1 What Is Covered

A server- or database-level backup captures the entire REDCap MySQL/MariaDB database, which includes everything that the project XML export does not: user accounts and rights, audit logs, randomization allocation tables, survey invitation history, External Module settings, and all project data across every project on the instance. Uploaded files and File Repository contents are covered only if the server's file storage is backed up too.

### 5.2 Configuring Database Backups

Database backup scheduling and configuration is handled by your institution's IT infrastructure team, not through the REDCap Control Center. REDCap does not provide a built-in database backup scheduler or configuration interface within the application itself.

Administrators who need to verify backup schedules or recovery procedures should contact their institution's IT team or database administrators.

### 5.3 What Administrators Can Monitor

Within the Control Center, the **Cron Jobs** page (under System Configuration) shows the status of REDCap's scheduled background processes. This is not a backup configuration interface, but it confirms that REDCap's internal maintenance tasks are running. See **[RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md)** for the Cron Jobs location.

---

## 6. Backup vs. Project Copy

These two features are sometimes confused:

| | **Project XML Export (Backup)** | **Copy Project** |
| --- | --- | --- |
| **Data included** | Yes (metadata & data) or No (metadata only) | Optional — tick the records checkbox (may be greyed out for non-admins if the project is over the development record limit) |
| **Result** | An offline `.xml` file you can store anywhere and restore to a new project | A new project on the same server, straight away |
| **Preserves user rights** | Roles only — users must be re-added | Users (ticked by default) and roles can be copied |
| **Logging history** | Never | Never |
| **Use case** | Disaster recovery, archiving, moving between servers | Reusing a project design, with or without its records, on the same server |

Use **Project XML Export** when you need a backup you can keep outside REDCap and restore later. Use **Copy Project** when you want to reuse a project on the same server for a new study or cohort, with or without its records.

> **Note:** On 17.x, Access Control Groups can grey out the copy button for some users. See [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md).

---

## 7. Automated Backup Approaches

REDCap does not provide a native scheduled backup feature accessible from the project interface. Teams that need recurring automated backups have two practical options:

**API-based scripted backups:** Use the Export Project XML API ([RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md)) in a scheduled script (cron job, task scheduler, etc.) to automatically export the project XML on a defined interval — for example, nightly or weekly. The script can save the resulting XML file to a secure network location with a timestamped filename. This is the most reliable way to achieve project-level automated backups without involving IT infrastructure.

**Infrastructure-level backup:** As described in Section 5, the institution's IT team can configure server-level database backups on a scheduled basis. This is the most comprehensive option, but it requires coordination outside of REDCap and recovery requires IT assistance.

---

## 8. Common Questions

**Q: How do I back up my REDCap project?**
**A:** Go to Project Setup → Other Functionality → **Copy or Back Up the Project** and click **Download metadata & data (XML)**. This produces an ODM XML file containing your project structure, settings and data. Use an account with full export rights so nothing is left out. For recurring backups, use the Export Project XML API ([RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md)) in an automated script.

**Q: Can I restore a project from a backup without losing the original?**
**A:** Yes. Restoring always creates a new project — REDCap does not overwrite an existing project. Your original project remains unchanged, and the restored backup becomes a separate project that you can compare or rename.

**Q: Does the project XML export include file uploads from File Upload fields?**
**A:** Only if you ask for it. In the **Download metadata & data (XML)** dialog, tick **Include all uploaded files and signatures?** (unticked by default). Via the API, set `exportFiles=true`. Either way, this can make the file very large. File Repository contents are not included in any project XML export.

**Q: Does the project XML export include user rights?**
**A:** Partly. User roles can be included, but user accounts and which user holds which role are not. After restoring from backup you are a user of the new project and the roles exist; re-add the other users and assign them to roles.

**Q: Can I use my backup to move my project to a different institution's REDCap?**
**A:** Yes, with limitations. The ODM XML file can be imported on another REDCap instance, ideally one running the same or a newer version. However, features specific to the source instance (External Modules, institutional integrations, field validation types not enabled on the destination) may not carry over. Test the import in a development environment before relying on it for a critical migration. On 17.x, the Project Migration Tool may be an alternative (see [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md)).

**Q: Who is responsible for making sure my REDCap data is backed up?**
**A:** Responsibility is shared. Project managers and administrators are responsible for maintaining project-level XML backups. The institution's IT team is responsible for infrastructure-level database backups. For critical studies, both layers of backup are recommended.

**Q: Is there a way to schedule automatic backups within REDCap?**
**A:** Not natively. REDCap does not include a built-in scheduled backup feature. Automation requires using the API in an external script or relying on IT-managed infrastructure backups.

**Q: What is the difference between a backup and a project copy?**
**A:** A project copy creates a new project on the same server, and can bring the records, users, roles, reports, alerts and other settings along. A backup (XML export) is a file you keep outside REDCap and can restore later, even on another server. Neither keeps the logging history. Because a copy lives on the same server as the original, it does not protect you the way an offline backup does.

**Q: Can I restore just a subset of records from a backup?**
**A:** Not directly via the restore process. The project XML import always creates a new project with everything in the file. To restore only a subset of records, import the full backup into a new project, then re-export just the records you need and import them into your production project using the data import process.

**Q: Is the logging history in the backup?**
**A:** No. Download the logging separately from the project's **Logging** page if you need to keep it (see [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md)).

---

## 9. Common Mistakes & Gotchas

**Downloading the wrong button.** **Download metadata only (XML)** and **Download metadata & data (XML)** are separate buttons and neither is a default. If you click the metadata-only one, no records are in the file. Check the file size — a very small file is likely metadata only.

**Backing up with restricted export rights.** The UI export applies your own export rights. If you have de-identified export rights or are in a Data Access Group, the backup silently leaves data out. Use an account with full export rights.

**Forgetting that users are not backed up.** This is the most common oversight after a restore. The new project has you as a user and the roles from the file, but nobody else. You must re-add the other users and assign them to roles before the project is usable. Consider keeping a separate record (an export from User Rights) of who holds which role.

**Forgetting to switch alerts and ASIs back on.** Restored alerts and automated survey invitations are switched off unless you ticked **leave enabled** (and always off when restored via the API). Review and re-enable them after a restore.

**Thinking a project copy is a backup.** Copy Project can bring records, users and settings along, so the copy can look complete. But it never copies the logging history, and it sits on the same server as the original — if the server or the database is lost, the copy goes with it. Use the XML download (or the API) for backups.

**Not testing the restore before you need it.** An XML backup file that cannot be imported successfully is worthless in an emergency. Periodically test your backup by importing it into a development environment and confirming that the data and structure appear correct. Remember that a very large file may exceed the maximum upload size in the UI.

**Relying solely on project-level backups for compliance-critical data.** Project XML exports never capture the logging history, randomization allocation tables or File Repository files, and leave out uploaded files unless you ask for them. If your project is subject to regulatory requirements, coordinate with IT to confirm infrastructure-level backups are covering these elements, and document your backup strategy.

**Including uploaded files without checking project size.** Including uploaded files (the UI checkbox or `exportFiles=true` in the API) can produce extremely large XML files that may time out or fail to complete on projects with many or large files. Test with a small record subset first before running a full file-inclusive export.

---

## 10. Related Articles

- [RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md)
- [RC-API-37 — Import Project (Create Project) API](RC-API-37_Import-Project-Create-Project.md)
- [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md)
- [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md)
- [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md)
- [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md)
