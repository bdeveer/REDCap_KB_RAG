RC-FILE-01

**File Repository**

| **Article ID** | RC-FILE-01 |
| --- | --- |
| **Domain** | File Repository |
| **Applies To** | All REDCap project types; requires File Repository user right |
| **Prerequisite** | RC-NAV-UI-01 — Project Navigation UI |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-USER-01 — User Rights Overview; RC-USER-03 — Configuring User Privileges; RC-DAG-01 — Data Access Groups; RC-SURV-08 — e-Consent Framework; RC-SENDIT-01 — Send-It Secure File Transfer; RC-EXPRT-01 — Data Export Overview; RC-API-45 through RC-API-49 — File Repository API |

---

# 1. Overview

The File Repository is a project-level storage area where team members can upload, organize, and share files related to a REDCap project. It supports unlimited folders and subfolders, optional per-folder access restrictions (by DAG, user role, or administrators only), bulk file operations, and a Recycle Bin with 30-day recovery. Several system folders are automatically maintained by REDCap to hold data export files, e-consent PDFs, and rich-text editor attachments. The File Repository is accessible from the left-hand Applications menu in any project and is distinct from file-upload fields on instruments, which store files at the individual record level.

---

# 2. Key Concepts & Definitions

**File Repository**

A per-project file storage area for documents, shared resources, and any files the team needs to access collectively. All project users with the File Repository user right can access it; folder-level restrictions can narrow access further.

**User-Created Folders**

Folders and subfolders created manually by project users or administrators to organize files. There is no limit on the number of folders or the depth of nesting. Each folder can optionally be restricted by Data Access Group, user role, or to administrators only.

**System Folders (Starred Folders)**

A set of automatically managed folders that REDCap maintains for its own purposes. Files in these folders do not count against the project's storage quota:

- **Data Export Files** — Every data export run from the project is saved here automatically. Users can re-download any previous export without re-running it. See RC-EXPRT-01.
- **e-Consent PDFs** — Signed consent documents are stored here automatically when the e-Consent Framework is in use. See RC-SURV-08.
- **Miscellaneous File Attachments** — Files uploaded via the rich text editor anywhere in the project (field labels, survey invitations, project dashboards, etc.) are auto-stored here with publicly accessible download links. Anyone with the link can download these files without logging in to REDCap — PHI or other sensitive content should never be uploaded through the rich text editor.
- **Recycle Bin** — Deleted files are held here for up to 30 days, after which they are permanently deleted. Files can be restored during this window.

**File Versioning**

When file versioning is enabled at the system level, uploading a file with the same name as an existing file in the same folder creates a new version rather than overwriting the original. Whether versioning is active depends on your institution's REDCap configuration.

**Storage Quota**

Projects may have a maximum storage limit set by administrators. The storage meter reflects only user-uploaded files; system folder contents (exports, e-consent PDFs, miscellaneous attachments) do not count toward the quota.

---

# 3. Accessing the File Repository

Navigate to the project and select **File Repository** from the left-hand Applications menu. Users must have the **File Repository** user right to see this item — users without it cannot access the module at all.

> **See also:** RC-USER-03 — Configuring User Privileges for details on granting the File Repository right.

---

# 4. Uploading and Managing Files

## 4.1 Uploading Files

Drag files into the upload zone at the top of the page, or click the upload area to browse. Up to 10 files can be uploaded per batch; the maximum file size is 512 MB per file. Certain executable and script file types are blocked for security (e.g., .exe, .dll, .sh, .js, .ps1, .bat, .jar). Navigate into a subfolder before uploading to place files in that location.

## 4.2 File Operations

The following actions are available per file:

| Action | Description |
|---|---|
| **Download** | Click the filename or download icon. |
| **Rename** | Change the filename. The file extension cannot be changed after upload. |
| **Edit comment** | Add or update a free-text comment visible in the file listing. |
| **Move** | Relocate the file to a different folder — individually or in bulk. |
| **Share** | Generate a secure download link via Send-It. See RC-SENDIT-01. |
| **Delete** | Moves the file to the Recycle Bin. If the file is linked elsewhere in the project (field label, survey invitation, dashboard), its download link becomes dead — REDCap warns before confirming. |

**Bulk operations:** Use checkboxes to select multiple files and delete, move, or download them together. Folders cannot be bulk-deleted — they must be deleted individually.

**Search:** A search box filters the listing within the currently open folder.

## 4.3 Folder Management

**Creating a folder:** Click **Create folder**, enter a name, and optionally configure access restrictions (see Section 4.4). Navigate into the folder before uploading to place files there.

**Renaming a folder:** Click the rename icon next to the folder name.

**Deleting a folder:** Click the X next to the folder name. Folders that still contain files cannot be deleted — all contents must be removed or moved first.

## 4.4 Folder Access Restrictions

When creating a folder, three optional restrictions can be applied:

- **Limit by Data Access Group** — Only users in the specified DAG can see this folder. Useful for multi-site studies where sites should not see each other's files. See RC-DAG-01.
- **Limit by User Role** — Only users assigned to the specified role can access the folder. Useful for restricting sensitive documents to specific team members. See RC-USER-01 and RC-USER-02.
- **Limit to administrators only** — The folder is hidden from all project users and accessible only to REDCap administrators. This option is mutually exclusive with DAG and role restrictions — only one type of restriction can be active at a time.

---

# 5. Recycle Bin and e-Consent PDFs Folder

## 5.1 Recycle Bin

Deleted files land in the Recycle Bin and remain recoverable for up to 30 days. The listing shows the original folder location, deletion time, and the deadline for permanent deletion. Click **Restore** to recover a file; if its original folder was also deleted, restoring the file automatically recreates the folder and any required parent folders. Administrators can permanently delete Recycle Bin files immediately — this is irreversible.

## 5.2 e-Consent PDFs Folder

When the e-Consent Framework is enabled on a survey instrument, REDCap automatically stores a signed PDF of each completed consent here. The listing shows respondent identifier (name/DOB), IP address, survey completion time, file storage time, version, and consent type. This folder is read-only for project users.

> **See also:** RC-SURV-08 — e-Consent Framework: Setup & Management.

---

# 6. Common Questions

| Question | Answer |
|---|---|
| *Who can access the File Repository?* | Any project user with the File Repository user right. Users without this right see no menu item and cannot access the module. Folder-level restrictions (DAG, role, admin-only) further limit which folders a user can see within it. |
| *Do files in the system folders count toward the project storage limit?* | No. Data Export Files, e-Consent PDFs, Miscellaneous File Attachments, and the Recycle Bin are excluded from the storage quota. Only user-uploaded files in user-created folders count. |
| *Can I recover a file I accidentally deleted?* | Yes, if within 30 days. Open the Recycle Bin, find the file, and click Restore. After 30 days the file is permanently deleted and cannot be recovered. |
| *I deleted a file that was linked in a field label — is the link broken?* | Yes. Deleting a file that is embedded elsewhere makes its download link a dead link. REDCap warns before deletion. If this has already happened, re-upload the file and update any links that referenced it. |
| *Can I restrict a folder so only one DAG can see it?* | Yes. When creating or editing a folder, use the DAG restriction option to limit visibility to users in a specific DAG. See RC-DAG-01. |
| *Where do files I upload in the rich text editor go?* | They are auto-stored in the Miscellaneous File Attachments system folder. These files receive publicly accessible download links — anyone with the link can download them without logging in. Do not upload PHI or sensitive content through the rich text editor. |
| *Can I access the File Repository via the API?* | Yes. See RC-API-45 through RC-API-49 for creating folders, listing contents, uploading, downloading, and deleting files programmatically. |

---

# 7. Common Mistakes & Gotchas

**Rich text editor uploads are public.** Files uploaded through REDCap's rich text editor (field labels, survey invitations, dashboards) land in the Miscellaneous File Attachments folder with publicly accessible links — no login required to download. Never use this path for PHI, PII, or sensitive documents.

**Deleting embedded files breaks links.** If a file in the File Repository is referenced in a field label, survey invitation, or project dashboard, deleting it turns that reference into a dead link. REDCap shows a warning, but the warning should be taken seriously in active projects.

**Folder delete requires an empty folder.** Folders cannot be deleted while they still contain files. Move or delete all contents first.

**File extension is locked after upload.** The file extension cannot be changed via the rename function. If a different extension is needed, delete the file and re-upload under the correct name.

**Admin-only and DAG/role restrictions are mutually exclusive.** A folder restricted to administrators only cannot simultaneously be restricted by DAG or user role. Choose one type of restriction.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to File Repository operations. API usage requires an API token and familiarity with the REDCap API. See RC-API-01 — REDCap API for authentication and setup.

- **RC-API-45** — Create Folder
- **RC-API-46** — List Files and Folders
- **RC-API-47** — Export (Download) a File
- **RC-API-48** — Import (Upload) a File
- **RC-API-49** — Delete a File

---

# 8. Related Articles

- RC-USER-01 — User Rights: Overview & Three-Tier Access (the right required to access the File Repository)
- RC-USER-03 — User Rights: Configuring User Privileges (how to grant File Repository access)
- RC-DAG-01 — Data Access Groups (DAG-restricted folder setup)
- RC-SURV-08 — e-Consent Framework: Setup & Management (the e-Consent PDFs system folder)
- RC-SENDIT-01 — Send-It: Secure File Transfer (sharing files via secure link from the File Repository)
- RC-EXPRT-01 — Data Export: Overview & Workflow (Data Export Files system folder; how exports are stored)
- RC-NAV-UI-01 — Project Navigation UI (prerequisite — left-hand menu and application access)
