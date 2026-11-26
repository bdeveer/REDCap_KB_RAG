

**File Repository**

| **Article ID** | [RC-FILE-01 — File Repository](RC-FILE-01_File-Repository.md) |
|---|---|
| **Domain** | File Repository |
| **Applies To** | All REDCap project types; requires File Repository user right |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — File Repository behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) |
| **Version** | 1.4 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md); [RC-SENDIT-01 — Send-It: Secure File Transfer](RC-SENDIT-01_Send-It-Secure-File-Transfer.md); [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md); [RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md) through [RC-API-49 — Delete a File (File Repository) API](RC-API-49_Delete-File-File-Repository.md)|
| **Synonyms** | where do i store project files in redcap; upload and share files with my team; create folders in the file repository; restrict file access by dag or role; recover a deleted file from the recycle bin; file repository vs file upload field; find exported data files and econsent pdfs; how to use the file repository |

---

## 1. Overview

The File Repository is a project-level storage area where team members can upload, organize, and share files related to a REDCap project. It supports unlimited folders and subfolders, optional per-folder access restrictions (by DAG, user role, or administrators only), bulk file operations, and a Recycle Bin with 30-day recovery. Several system folders are automatically maintained by REDCap to hold data export files, e-consent PDFs, and rich-text editor attachments. The File Repository is accessible from the left-hand Applications menu in any project and is distinct from file-upload fields on instruments, which store files at the individual record level.

---

## 2. Key Concepts & Definitions

**File Repository**

A per-project file storage area for documents, shared resources, and any files the team needs to access collectively. All project users with the File Repository user right can access it; folder-level restrictions can narrow access further.

**User-Created Folders**

Folders and subfolders created manually by project users or administrators to organize files. There is no limit on the number of folders or the depth of nesting. Each folder can optionally be restricted by Data Access Group, user role, or to administrators only.

**System Folders (Starred Folders)**

A set of automatically managed folders that REDCap maintains for its own purposes. Files in these folders do not count against the project's storage quota:

- **Data Export Files** — Every export run from the Export Data dialog on the Data Exports, Reports, and Stats page is saved here automatically (API exports and the ZIP of uploaded files are not). Users can re-download a previous export without re-running it, if their export rights allow: the folder is empty for users whose export rights are De-identified or Remove Identifiers on every instrument, a file can only be downloaded with Full Data Set rights on every instrument it contains, and users in a DAG see only exports made by users in their DAG. An administrator can set a project to delete these files automatically after a number of days. See [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md).
- **PDF Snapshot Archive** — Signed e-Consent PDFs, and any PDF Snapshot set to save to the File Repository, are stored here automatically. See [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) and [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).
- **Miscellaneous File Attachments** — Files uploaded via the rich text editor anywhere in the project (field labels, survey invitations, project dashboards, etc.) are auto-stored here with publicly accessible download links. Anyone with the link can download these files without logging in to REDCap — PHI or other sensitive content should never be uploaded through the rich text editor.
- **Recycle Bin** — Deleted files are held here for up to 30 days, after which they are permanently deleted. Files can be restored during this window.
- **Record locking PDFs** — If the project archives PDFs when records are locked (record-level locking with PDF archiving), those PDFs are kept in their own system folder.

**Duplicate File Names (No Versioning)**

The File Repository does not keep file versions. Uploading a file with the same name as one already in the folder does not overwrite it or create a version — REDCap saves the new file under an automatically adjusted name, such as `report (1).pdf`. Renaming a file to a name already used in the folder is refused. To keep a clear history, put a date or version number in the file name yourself.

**Storage Quota**

Projects may have a maximum total storage limit set by administrators. The storage meter reflects only user-uploaded files; system folder contents (exports, PDF Snapshot Archive files, miscellaneous attachments) and the Recycle Bin do not count toward the quota.

---

## 3. Accessing the File Repository

Navigate to the project and select **File Repository** from the left-hand Applications menu. Users must have the **File Repository** user right to see this item — users without it cannot access the module at all.

> **See also:** [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) — Configuring User Privileges for details on granting the File Repository right.

---

## 4. Uploading and Managing Files

### 4.1 Uploading Files

Drag files into the upload zone at the top of the page, or click the upload area to browse. You can select any number of files at once; REDCap uploads them one at a time. Navigate into a subfolder before uploading to place files in that location.

- **Maximum file size** is set by your server and REDCap administrator, so it differs between installations. If a file is refused as too large, ask your administrator what the limit is.
- **Blocked file types:** administrators maintain a list of blocked file extensions (typically executables such as .exe, .dll and .bat), and REDCap always blocks certain server-script file types regardless of that list. Files with no extension are rejected. If a file is blocked, compress it into a ZIP or ask your administrator.

> **Institution-specific:** Upload size limits, blocked file types, project storage limits and whether File Repository uploads are switched on at all are set by your REDCap administrators. Check with them if an upload is refused.

### 4.2 File Operations

The following actions are available per file:

| Action | Description |
|---|---|
| **Download** | Click the filename or download icon. |
| **Rename** | Change the filename. The file extension cannot be changed after upload, and the new name cannot match another file in the same folder. |
| **Edit comment** | Add or update a free-text comment visible in the file listing. |
| **Move** | Relocate the file to a different folder — individually or in bulk. |
| **Share** | Depending on what your installation allows, get a public download link for the file and/or send it through Send-It. A public link works for anyone who has it, without logging in; it does not expire and cannot be withdrawn — it stops working only if the file is deleted (or an administrator switches public links off). See [RC-SENDIT-01 — Send-It: Secure File Transfer](RC-SENDIT-01_Send-It-Secure-File-Transfer.md). |
| **Delete** | Moves the file to the Recycle Bin after a general confirmation. REDCap does not check whether the file is linked elsewhere in the project (field label, survey invitation, dashboard); any such link stops working. |

> **Tip:** Share public links carefully. Never create one for a file containing PHI or other sensitive data, and if a link reaches the wrong person, delete the file (re-upload it if you still need it) to stop the link working.

**Bulk operations:** Use checkboxes to select multiple files and delete, move, or download them together (multiple files download as a ZIP). Folders cannot be bulk-deleted — they must be deleted individually.

**Search:** A search box filters the listing within the currently open folder.

### 4.3 Folder Management

**Creating a folder:** Click **Create folder**, enter a name, and optionally configure access restrictions (see Section 4.4). Navigate into the folder before uploading to place files there.

**Renaming a folder:** Click the rename icon next to the folder name.

**Moving a folder:** Folders can be moved into another folder, like files.

**Deleting a folder:** Click the X next to the folder name. Folders that still contain files cannot be deleted — all contents must be removed or moved first.

### 4.4 Folder Access Restrictions

Restrictions are set **only when the folder is created** — they cannot be added, changed or removed later. If you need different restrictions, create a new folder with the right settings and move the files into it.

Three optional restrictions are available:

- **Limit by Data Access Group** — Users in other DAGs cannot see this folder. Users who are not assigned to any DAG see all folders, including DAG-restricted ones — this is normal, since unassigned users see all DAGs' data too. Useful for multi-site studies where sites should not see each other's files. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).
- **Limit by User Role** — Users in other roles cannot see this folder. Users who are not assigned to any role also see role-restricted folders. See [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) and [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md).
- **Limit to administrators only** — The folder is hidden from all project users and accessible only to REDCap administrators. This option cannot be combined with DAG or role restrictions.

A DAG restriction and a role restriction can be combined on the same folder. Users who are themselves in a DAG or role can only pick their own DAG or role. Restrictions carry down to subfolders created inside a restricted folder.

> **Tip:** To keep a role-restricted folder private, make sure every project user is assigned to a role — users with no role see it. Likewise, a DAG restriction only hides a folder from users in other DAGs, not from users outside all DAGs.

> **Important:** Deleting a DAG or a user role removes that restriction from any folder that used it, so the folder becomes visible to everyone who can see the File Repository. Check restricted folders before deleting a DAG or role.

---

### 4a. Admin-Restricted Folders *(15.5.0+)*

Administrators with access to all projects can create folders in a project's File Repository that are **visible only to administrators**. Project users do not see them at all.

The intended use is project-level material that belongs with the project but not in the hands of its users — administrative correspondence, review documentation, or configuration notes.

Two consequences worth knowing:

- **They are excluded from the API listing.** The Export a List of Files/Folders method does not return admin-restricted folders, so an API-driven inventory of the File Repository is not a complete one. See [RC-API-46 — List Files and Folders (File Repository) API](RC-API-46_List-Files-Folders-File-Repository.md).
- **Visibility depends on all-project access**, not merely on being an administrator with some elevated rights.

> **Project-level upload size override (17.x — 17.3 LTS and 17.6 Standard; not in 16.0 LTS).** The Edit Project Settings page carries a project-level override for the system-wide "File Repository upload max file size", so one project can be allowed larger uploads without raising the limit everywhere. The server's own upload limit still applies on top. See [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md).

> **Version caveat (16.1.0–16.1.3 Standard):** That project-level limit was **not respected when files were imported through the API** — it applied correctly in the interface only. Fixed in 16.1.4. On affected versions the API could accept files the project's own setting should have rejected.

---

## 5. Recycle Bin and PDF Snapshot Archive

### 5.1 Recycle Bin

Deleted files land in the Recycle Bin and remain recoverable for up to 30 days. The Recycle Bin is a single flat list (it does not show which folder a file came from), with the columns **Name**, **Size**, **Time Uploaded**, **Comments**, **Time Deleted**, **Time until permanent deletion** and **Restore**. Click **Restore** to recover a file; it goes back to its original folder, and if that folder was also deleted, REDCap recreates it and any required parent folders. A restore is refused if it would take the project over its storage limit. Administrators can permanently delete Recycle Bin files immediately — this is irreversible.

### 5.2 PDF Snapshot Archive

When the e-Consent Framework is enabled on a survey instrument, REDCap automatically stores a signed PDF of each completed consent here. PDF Snapshots whose trigger has "Save to File Repository" ticked are stored here too. For e-Consent PDFs the listing shows the respondent identifier (name/DOB), IP address (if the administrator has IP capture on), version and type, along with survey completion and file storage times.

Project users cannot edit or delete files in this folder. Downloading a file needs data export rights; for PDFs created by a survey, full export rights on that instrument. Users in a Data Access Group see only their group's records. Deleting a record removes its PDFs from the archive, and Erase all data deletes them, so the archive is not a permanent record on its own.

> **See also:** [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md).

---

## 6. Common Questions

| Question | Answer |
|---|---|
| *Who can access the File Repository?* | Any project user with the File Repository user right. Users without this right see no menu item and cannot access the module. Folder-level restrictions (DAG, role, admin-only) further limit which folders a user can see within it. |
| *Do files in the system folders count toward the project storage limit?* | No. Data Export Files, the PDF Snapshot Archive, Miscellaneous File Attachments, and the Recycle Bin are excluded from the storage quota. Only user-uploaded files in user-created folders count. |
| *Can I recover a file I accidentally deleted?* | Yes, if within 30 days. Open the Recycle Bin, find the file, and click Restore. After 30 days the file is permanently deleted and cannot be recovered. |
| *I deleted a file that was linked in a field label — is the link broken?* | Yes. Deleting a file that is embedded elsewhere makes its download link a dead link. REDCap does not detect such links when you delete, so check before deleting. If this has already happened, restore the file from the Recycle Bin, or re-upload it and update any links that referenced it. |
| *Can I restrict a folder so only one DAG can see it?* | Yes, but only when you create the folder — restrictions cannot be added to an existing folder. Use the DAG restriction option to hide it from users in other DAGs. Users not assigned to any DAG still see it. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md). |
| *What happens if I upload a file with the same name as an existing one?* | Nothing is overwritten and no version is created. REDCap saves the new file under an adjusted name such as `report (1).pdf`. Put dates or version numbers in file names if you need a history. |
| *Do public share links expire?* | No. A public link keeps working until the file is deleted (or an administrator switches public links off), and it cannot be withdrawn on its own. Only share files you are comfortable being reachable by anyone with the link. |
| *Where do files I upload in the rich text editor go?* | They are auto-stored in the Miscellaneous File Attachments system folder. These files receive publicly accessible download links — anyone with the link can download them without logging in. Do not upload PHI or sensitive content through the rich text editor. |
| *Can I access the File Repository via the API?* | Yes. See [RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md) through [RC-API-49 — Delete a File (File Repository) API](RC-API-49_Delete-File-File-Repository.md) for creating folders, listing contents, uploading, downloading, and deleting files programmatically. |

---

## 7. Common Mistakes & Gotchas

**Rich text editor uploads are public.** Files uploaded through REDCap's rich text editor (field labels, survey invitations, dashboards) land in the Miscellaneous File Attachments folder with publicly accessible links — no login required to download. Never use this path for PHI, PII, or sensitive documents.

**Deleting embedded files breaks links.** If a file in the File Repository is referenced in a field label, survey invitation, or project dashboard, deleting it turns that reference into a dead link. The delete confirmation is a general one — REDCap does not tell you the file is linked — so check before deleting files in active projects.

**Folder restrictions cannot be changed later.** DAG, role and admin-only restrictions are set when the folder is created. Plan restrictions up front; to change them, create a new folder and move the files.

**Unassigned users see restricted folders.** Users with no role see role-restricted folders, and users in no DAG see DAG-restricted folders. Deleting a DAG or role also lifts the restriction from its folders.

**Public share links are permanent.** They do not expire and cannot be revoked except by deleting the file.

**Folder delete requires an empty folder.** Folders cannot be deleted while they still contain files. Move or delete all contents first.

**File extension is locked after upload.** The file extension cannot be changed via the rename function. If a different extension is needed, delete the file and re-upload under the correct name.

**Admin-only and DAG/role restrictions are mutually exclusive.** A folder restricted to administrators only cannot also be restricted by DAG or user role. DAG and role restrictions can be combined with each other.

### API Access

> **Note:** The following REDCap API methods provide programmatic access to File Repository operations. API usage requires an API token and familiarity with the REDCap API. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication and setup.

- **[RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md)** — Create Folder
- **[RC-API-46 — List Files and Folders (File Repository) API](RC-API-46_List-Files-Folders-File-Repository.md)** — List Files and Folders
- **[RC-API-47 — Export a File (File Repository) API](RC-API-47_Export-File-File-Repository.md)** — Export (Download) a File
- **[RC-API-48 — Import a File (File Repository) API](RC-API-48_Import-File-File-Repository.md)** — Import (Upload) a File
- **[RC-API-49 — Delete a File (File Repository) API](RC-API-49_Delete-File-File-Repository.md)** — Delete a File

---

## 8. Related Articles

- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (the right required to access the File Repository)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (how to grant File Repository access)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG-restricted folder setup)
- [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) (the PDF Snapshot Archive system folder)
- [RC-SENDIT-01 — Send-It: Secure File Transfer](RC-SENDIT-01_Send-It-Secure-File-Transfer.md) (sharing files via secure link from the File Repository)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (Data Export Files system folder; how exports are stored)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (prerequisite — left-hand menu and application access)
