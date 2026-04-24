RC-PROJ-05

**Project Migration: Moving a Project Between REDCap Installations**

| **Article ID** | RC-PROJ-05 |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-PROJ-01 — Project Lifecycle: Status and Settings |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PROJ-01 — Project Lifecycle: Status and Settings; RC-FD-03 — Data Dictionary; RC-IMP-01 — Data Import Overview; RC-EXPRT-01 — Data Export: Overview & Workflow; RC-SURV-01 — Surveys – Basics; RC-USER-01 — User Rights: Overview & Three-Tier Access |

> **Note on REDCap+:** This article covers the standard project migration workflow available in all REDCap installations using the built-in backup and restore feature. REDCap+ includes a revamped Project Migration tool with expanded capabilities. If your installation has REDCap+, check the dedicated REDCap+ documentation for that tool.

---

# 1. Overview

There are many reasons to move a REDCap project from one installation to another: changing institutions, consolidating multiple REDCap installations, or sharing a project design with a colleague at a different site. Whatever the reason, REDCap provides a built-in mechanism to export a full project backup and re-import it elsewhere.

This article covers:

- What to check before migrating
- How to export a project using the Backup feature
- What is and is not included in the export
- How to import a project into a new installation
- Common pitfalls and how to handle them
- Alternative migration approaches when a full backup/restore is not feasible

> **Prerequisite rights:** You need **Project Design and Setup** rights in the source project to access the backup feature. You need the ability to create projects in the destination installation to complete the import. If you are unsure whether you can create projects at the destination, contact that installation's REDCap support team before starting.

---

# 2. Pre-Migration Checks

Before exporting anything, review the differences between your source and destination REDCap installations. Migrating without checking first is the most common cause of post-migration problems.

## 2.1 Version Differences

If there is a significant version gap between the two installations, pay attention to the direction of migration:

- **Migrating to a newer version** generally works without issues.
- **Migrating to an older version** can cause problems. Features introduced after the older version will either be silently dropped or cause import errors.

Examples of features that may not be available in older versions: Form Display Logic, Multi-Language Management, Alerts & Notifications, MyCap.

## 2.2 Feature Differences

REDCap is highly configurable at the administrator level. Features that are active in your source installation may be disabled at the destination — due to cost, security policy, or support capacity. Check whether the following are available at the destination before migrating a project that relies on them:

- Texting (Twilio or Mosio)
- Bioportal biomedical ontology lookups
- MyCap / REDCap Mobile App
- External Modules (and specifically the modules your project uses)

Contact the destination installation's REDCap support team if you are unsure about any of these.

## 2.3 Policy Differences

Every organization runs REDCap differently. The destination installation may have:

- Restrictions on who can create new projects
- A project request/approval workflow instead of self-service project creation
- Different API access, survey, or export policies

Reviewing these policies before you start will prevent surprises at import time.

---

# 3. Exporting a Project (Backup)

## 3.1 Accessing the Backup Feature

1. Navigate to the source project's **Project Home** or **Project Setup** page.
2. Click the **"Other Functionality"** tab.
3. Locate the **"Back Up the Project"** section.

You will see two export options.

## 3.2 Export Options

### Option A: Download Metadata Only (XML)

Exports all project structure, configuration, and settings — but **no data records**. Use this when:

- You want to recreate the project design at the destination without bringing data
- You are sharing a project template with another site
- You only need to set up the instrument structure

### Option B: Download Metadata & Data (XML)

Exports the full project including all structure and all data records. Use this when:

- You are doing a full project relocation and need all existing data at the destination
- You want to archive a complete project snapshot

Both options produce a single XML file in the **CDISC-ODM format** — a standardized electronic data capture interchange format. Other EDC tools may be able to import this file, though the best results are always REDCap-to-REDCap.

> **File type note:** The export file has an `.xml` extension. Some organizational cybersecurity policies block downloading XML files. If the download fails or is blocked, contact your organization's IT or cybersecurity team.

## 3.3 Optional Inclusions

Before downloading, REDCap presents a checklist of optional components to include in the backup. Items only appear on the list if they are actively in use in the source project:

- User roles
- Custom record status dashboards
- Reports and report folders
- Project dashboards
- Data quality rules
- Alerts & Notifications
- Project bookmarks
- Survey Queue and Automated Survey Invitation settings
- Form Display Logic settings
- Multi-Language Management translations
- MyCap Mobile App configuration

If you exclude any of these, you will need to configure them manually in the destination project (or start with a clean slate for those features).

## 3.4 Data Export Options (Metadata & Data Only)

When exporting metadata and data together, REDCap offers additional options to control the data included:

**Include uploaded files and signatures** — Adds all file-type field contents and signature images to the export. If the project contains many files, this may produce a very large archive and in rare cases can cause the export to fail. If that happens, export files separately.

**De-identification options:**

- *Remove all Identifier Fields* — Strips any field flagged as an identifier during instrument design.
- *Hash the Record ID Field* — Scrambles the record ID. Use this only if your record ID field contains an actual identifier (e.g., MRN, phone number).
- *Remove unvalidated text fields* — Strips text fields with no validation rule defined.
- *Remove Notes/Essay box fields* — Strips all Notes fields due to the difficulty of verifying their contents.
- *Remove all date and datetime fields* — Strips all date/datetime-validated fields.
- *Shift all dates by 0–364 days* — Adds a random offset to all dates, preserving relative date relationships while obscuring absolute values.

**Advanced formatting options:**

- *Export blank values for gray Form Status* — Controls whether forms with no data show as "0" or blank. The default is sufficient for most purposes.
- *Set CSV delimiter character* — Relevant only if you plan to use the exported data as a CSV import elsewhere.
- *Force decimal format* — Sets the numeric punctuation convention (e.g., European vs. American format).

## 3.5 What Is NOT Included in the Backup

Certain items are excluded by design because they are tied to the source installation and cannot be meaningfully transferred:

| Excluded Item | Why |
|---|---|
| **Logging** | Logging can be downloaded separately but cannot be imported into a different installation |
| **Individual users and their rights** | User accounts exist per-installation; users must be re-added manually at the destination |
| **Project folders** | Folder organization is user- and installation-specific |
| **External Module configurations** | Module settings are per-installation and per-project; must be reconfigured at destination |
| **Survey links** | Links are composed of the source installation's base URL plus a unique token — neither transfers |
| **API tokens** | Tokens are per-project, per-user, and per-installation; must be regenerated at the destination |

---

# 4. Importing a Project

## 4.1 Standard Import Steps

1. Navigate to the **My Projects** page or the REDCap home page of the destination installation.
2. Click **"+ New Project"** (or **"Request New Project"** if your institution requires administrator approval).
3. Enter a project title and select a project purpose.
4. Optionally, assign the project to a folder and add project notes.
5. Under **"Project creation option"**, select **"Upload a REDCap project XML file (CDISC ODM format)"**.
6. Use the **"Choose File"** button to select your backup XML file.
7. Click **"Create Project"**.
8. Once created, open the new project and verify that all settings, instruments, and configurations transferred correctly.
9. Add users to the new project. (They did not transfer — see Section 3.5.)

## 4.2 Policy Variations at the Destination

REDCap administrators can configure the project creation experience in different ways. Common variations you may encounter:

- An informational popup from the local support team appears before or after creation.
- An additional project creation survey is required.
- The button reads **"Request Project"** instead of "Create Project," meaning an administrator must approve the request before the project is created.

If you are unsure about the process at your destination installation, contact their REDCap support team before starting.

---

# 5. Migration Pitfalls

## 5.1 Import Timeouts on Large Projects

The XML import process runs synchronously — the server must process the entire file in a single request before returning a response. On very large projects (high record counts, many uploaded files, or both), this can exceed the server's request time limit. Most web servers implement health-check timeouts to cut off long-running processes and keep the server responsive, and an oversized import will hit that ceiling before it completes.

If you encounter a timeout during import, options include:

- Export metadata only (no data), import that first, then import data separately via CSV (see Section 7).
- Export without files/signatures, then handle file-type fields separately.
- Contact the destination REDCap support team — an administrator may be able to run the import in a context with a higher timeout, or assist with a database-level transfer.

> **REDCap+ note:** The revamped Project Migration tool in REDCap+ does not have this limitation. It runs the migration in the background through a series of API calls rather than a single synchronous request, making it suitable for large-scale migrations that would otherwise time out.

## 5.2 Feature Availability

As covered in Section 2, a feature present in the source project may not be available at the destination. Items to check proactively:

- **Texting (Twilio / Mosio):** Requires a separate vendor contract. Not universally available.
- **Bioportal lookups:** Can be disabled by strict outbound-connection security policies.
- **MyCap and the Mobile App:** Some organizations have not enabled these due to support or security considerations.
- **External Modules:** Availability varies significantly by installation. Ask the destination support team whether specific modules are available or can be enabled.

## 5.2 Migrating an Active Project

The most significant risk in project migration arises when the project is **actively collecting data** — particularly when participants are being invited via survey links, email, or text.

All of the following are tied to the source installation and will break on migration:

| Element | What Breaks |
|---|---|
| **Survey invitations** | Outstanding invitations still point to the source installation |
| **Survey links** | Public and individualized links change; participants following old links reach the wrong project or an error |
| **Custom survey links** | Custom links are globally unique across all REDCap installations. You cannot simply duplicate one in the new project — it will almost certainly show as "already taken." Releasing a custom link from the old project is possible, but processing can take considerable time. If your custom link is embedded in printed materials, this is a strong reason to reconsider migrating. |
| **Texting** | The sending phone number is tied to the source installation's Twilio/Mosio account. A new number at the destination may confuse participants. |
| **Email sender address** | If the "from" address changes, some email providers will treat messages as spoofing attempts and block delivery. Verify SPF/DKIM configuration at the destination before switching. |

Note that any alerts, text messages, or survey invitations that were already sent before the migration will still contain links pointing to the old installation. Participants who follow those links will reach the old project — not the new one.

**For this reason, it is strongly recommended to shut down the old project immediately after migration** by moving it to Analysis/Cleanup status or marking it as Completed (see RC-PROJ-01). Leaving the old project open and accepting data after the new project is live creates a split-data situation: records may be updated in both projects simultaneously, resulting in conflicting versions of the same record. Resolving these data collisions is time-consuming and error-prone, and in some cases may not be fully recoverable.

---

# 6. Strategies for Active Projects

## 6.1 Option 1 — Avoidance

If active data collection is expected to end soon, the cleanest approach is to wait until the collection period is complete before migrating. The more limited the remaining collection window, the stronger the case for simply waiting.

## 6.2 Option 2 — Parallel Collection

Run both projects simultaneously for a period:

- Existing participants continue in the old project.
- New participants are enrolled directly in the new project.
- Once the old project's data collection is complete, export and import that data into the new project.

**Critical requirement:** The instrument design and variable names must be kept in sync between both projects throughout the parallel phase. Any design changes must be applied to both projects simultaneously.

## 6.3 Option 3 — Big Bang (Hard Cutover)

When a staged migration is not possible, a full hard cutover is the only option. To minimize disruption:

- Have the new project fully configured and tested before the cutover date.
- Set definitive expiration dates on all outstanding survey invitations in the old project before switching over.
- Communicate the change to study participants in advance.
- Choose a cutover time that minimizes participant impact (e.g., overnight or during a low-activity period).
- Be prepared to troubleshoot broken links and confused participants immediately after the switch.

The Big Bang approach carries the highest risk of data collection gaps and participant confusion. It should be used only when no other option is feasible.

---

# 7. Alternative Migration Methods

The full XML backup/restore approach moves the entire project in one step. When that is not possible — for example, when migrating to an older REDCap version, or when you only need to move part of a project — the following piece-by-piece alternatives are available.

Note that some features depend on others being in place first. For example, you cannot assign instruments to events until the data dictionary and event definitions are already imported.

## 7.1 Data Dictionary

The Data Dictionary (CSV) defines all instruments and fields in a project. Importing a data dictionary into a new project recreates the full instrument structure.

See **RC-FD-03 — Data Dictionary** for full documentation.

## 7.2 Data Export and Import

If the destination project already has the same instruments and variable definitions, you can export data as CSV from the source project and import it into the destination project.

See **RC-EXPRT-01 — Data Export: Overview & Workflow** and **RC-IMP-01 — Data Import Overview** for details.

## 7.3 Other Feature-Specific Exports

Several REDCap features support their own export/import CSV workflows, which can be used to selectively transfer settings:

- Arms and events (longitudinal projects)
- Instrument-to-event mappings
- User roles and user-role assignments
- Data Access Groups and DAG assignments
- Repeating instruments and events configuration

Use these targeted exports when you only need to transfer specific components, or as a fallback when a full XML migration is not an option.

---

# 8. Common Questions

**Q: I'm moving to a new institution. Do I need to do anything special before exporting?**

**A:** Check the three areas in Section 2: version compatibility, feature availability, and creation policies at the destination. If the destination runs a significantly older version of REDCap, review which features your project uses that may not be available there. Contact the destination support team if you're unsure.

---

**Q: Will the backup include my data?**

**A:** Only if you choose "Download metadata & data (XML)." The "Download metadata only (XML)" option exports the project structure but not any records.

---

**Q: Why aren't my users showing up in the migrated project?**

**A:** Individual user accounts and their rights are never included in the backup — this is by design. Users exist per-installation and must be added manually (or via user roles) in the destination project. The only user with automatic access to the new project is the person who created it.

---

**Q: My custom survey link is in use in printed materials. Can I transfer it?**

**A:** Not reliably. Custom survey links are globally unique across all REDCap installations worldwide. You cannot simply reuse the same link in a new project. Releasing a custom link from the old project is technically possible, but processing takes time and is not guaranteed. If your custom link is embedded in printed materials that cannot be updated, this is a strong reason to reconsider migration entirely.

---

**Q: Can I import the backup XML into a different electronic data capture tool?**

**A:** Possibly. The export uses the CDISC-ODM format, which is a recognized EDC interchange standard. Other tools that support CDISC-ODM may be able to import the file, but the results will vary. REDCap-to-REDCap migration will always produce the most complete and reliable transfer.

---

**Q: Can I use the backup feature to clone a project within the same installation?**

**A:** Yes, that works fine. However, for cloning within the same installation, the dedicated **"Copy the Project"** function (Project Setup → Other Functionality) is generally easier — see **RC-PROJ-01** for details on that feature.

---

**Q: What if my export fails due to file size?**

**A:** This can happen when "Include uploaded files and signatures" is checked on a project with many large attachments. Try exporting without that option first, then handle the files separately via the file export tools.

---

**Q: Do I lose my survey links when I migrate?**

**A:** Yes. Both public survey links and individualized participant survey links are tied to the source installation. After migration, new links are generated by the destination installation, and you will need to redistribute them to participants.

---

# 9. Related Articles

- RC-PROJ-01 — Project Lifecycle: Status and Settings (project statuses, copy/delete features)
- RC-PROJ-02 — Project Setup Checklist (post-import checklist for setting up your new project)
- RC-FD-03 — Data Dictionary (piece-by-piece alternative: instrument/field structure transfer)
- RC-EXPRT-01 — Data Export: Overview & Workflow (exporting data for partial migration)
- RC-IMP-01 — Data Import Overview (importing data into the destination project)
- RC-SURV-01 — Surveys – Basics (survey links, custom links, and survey access after migration)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (re-adding users to the migrated project)
