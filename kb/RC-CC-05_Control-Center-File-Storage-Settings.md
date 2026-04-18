RC-CC-05

**Control Center: File Storage & Upload Settings**

| **Article ID** | RC-CC-05 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-01 — Notifications & Reporting; RC-CC-06 — Modules & Services Configuration; RC-DE-12 — Data Resolution Workflow; RC-INST-01 — Institution-Specific Settings & Policies |

---

The **File Upload Settings** page (under **System Configuration**) controls where REDCap stores uploaded files and what file upload behaviors are allowed across the system. Configuration here applies to all projects on the instance.

---

# File Storage Methods

REDCap supports several file storage backends. Only one method should be active at a time. All uploaded files are stored on your web server or an external server — REDCap itself does not retain them in the database.

**Local (on REDCap web server)**
Files are stored in a directory on the REDCap web server (or a mapped network share such as NFS/NAS). The default storage path is the `edocs` folder. For security, the storage directory should not be web-accessible. An alternative local path can be specified.

**External server using WebDAV (SSL supported)**
Files are stored on a separate server via WebDAV protocol. Configuration is done in `/webtools2/webdav/` on the REDCap server.

**Amazon S3**
Files are stored in an AWS S3 bucket. Required configuration: AWS Access Key, AWS Secret Key, bucket name, and AWS Region/Location Constraint (e.g., `ap-northeast-2`). Leaving the region blank defaults to `us-east-1`. An optional custom S3 endpoint can be provided for non-standard deployments.

**Google Cloud Storage (for Google App Engine hosting only)**
For REDCap instances hosted on Google Cloud Platform. Requires two GCS buckets: one for permanent file storage and one for temporary file storage (they must be different buckets). The subfolder-by-project-ID option (see below) also applies to this storage type.

**Google Cloud Storage using API Service Account**
For non-App Engine GCP hosting. Requires a GCP Project ID, bucket name, and service account secret key. Includes an independent setting for organizing files into subfolders by project ID.

**Microsoft Azure Blob Storage**
Files are stored in a Microsoft Azure Blob Storage container. Required configuration: storage account name, storage account key, and container name.

Setup steps:
1. Log in to the Azure portal (`https://portal.azure.com/`)
2. Go to *Storage Accounts* and create or identify your storage account
3. Under the storage account, navigate to *Access keys* and copy a Key value
4. Under the storage account, navigate to *Blobs* and create a container

The Azure environment can be set to either *Azure Commercial/Global* (default) or *Azure U.S. Government*. The U.S. Government option is only for Microsoft-authorized government and CSP partners serving US federal, state, and local government entities.

> **Recommendation:** For cloud-hosted REDCap instances, using the same cloud provider's native storage service simplifies access control, reduces egress costs, and aligns with institutional cloud governance policies.

---

# Storage Configuration Settings

## Local Server File Storage

**Set Local File Storage Location**
An alternative directory path can be specified for local file storage. If left blank, REDCap uses the default `edocs` folder. For security, this path should not be accessible over the web (i.e., not under the web root).

**Organize Stored Files into Subfolders by Project ID**
When enabled, each new project's files are stored in a dedicated subfolder named by its REDCap project ID. This applies only to projects created after the setting is enabled — existing projects are not moved. If REDCap cannot create the subfolder due to permissions, it falls back to storing files in the main storage directory.

Options: *Disabled* / *Enabled*

> This setting also applies to Google Cloud Storage for App Engine hosting.

---

# Restricted File Types for Uploaded Files

A system-level blocklist of file extensions prevents users from uploading potentially dangerous file types into REDCap. This applies to all upload locations across the system (File Repository, file upload fields, Send-It, etc.).

Extensions are specified as a comma-, semicolon-, or line-break-delimited list. Case-insensitive — no need to list both `.EXE` and `.exe`.

The default REDCap blocklist includes:

```
ade, adp, apk, appx, appxbundle, bat, cab, chm, cmd, com, cpl, diagcab, diagcfg, diagpack,
dll, dmg, ex, exe, hta, img, ins, iso, isp, jar, jnlp, js, jse, lib, lnk, mde, msc, msi,
msix, msixbundle, msp, mst, nsh, php, pif, ps1, scr, sct, shb, sys, vb, vbe, vbs, vhd,
vxd, wsc, wsf, wsh, xll
```

This list covers executables, scripts, system files, and installer formats that could be used to execute malicious code.

---

# Configuration Options for Various Types of Stored Files

Upload limits and enable/disable controls are set independently for each file upload context in REDCap.

> **Server default:** The web server's maximum file upload size is determined by two values in `PHP.INI`: `upload_max_filesize` and `post_max_size`. The lower of the two applies. To change the server default, modify these values and restart the web server. The server default is typically 1024 MB unless changed. Per-context limits in REDCap can only be set *lower* than the server default.

## File Repository

**Enable File Uploading for the File Repository Module**
Globally enables or disables user-initiated file uploads to the File Repository. Even when disabled, REDCap still stores automatically generated files in the File Repository (e.g., data export files, eConsent PDFs).

Options: *Disabled* / *Enabled*

**File Repository Upload Max File Size**
Maximum size (in MB) for a single file uploaded by a user to the File Repository. If left blank, the server default applies.

**File Repository: File Storage Limit Per Project (in MB)**
Sets a cap on total storage per project within the File Repository, counting only user-uploaded files (not system-generated files like exports or eConsent PDFs). Set to blank or `0` to disable the limit. This value can be overridden per project via the 'Edit Project Settings' page.

**File Repository: Allow Users to Share Files via Public Links**
When enabled, project users can generate a unique public URL for any file in the File Repository. Anyone with the link can download the file without authenticating to REDCap.

Options: *Disabled* / *Enabled*

> Disable this setting if your institution's data security policy requires authenticated access to all files stored in REDCap.

## 'File Upload' Fields

**Enable 'File Upload' Field Types**
Globally enables or disables the File Upload field type on data entry forms and surveys. When disabled, the field type is hidden in the Online Designer and any existing File Upload fields become non-functional (though their configuration is retained).

Options: *Disabled* / *Enabled*

**Upload Max File Size for 'File' Field Types on Forms/Surveys**
Maximum size (in MB) for a file uploaded via a File Upload field on a data entry form or survey. If left blank, the server default applies.

## Send-It

**Enable Send-It**
Send-It allows users to securely transfer files to other recipients via a temporary expiring link. It can be enabled for all REDCap locations, or restricted to specific areas. Files are deleted from the server when their link expires.

Options:
- *Disabled*
- *Enabled for all locations* — Available from the REDCap home page, File Repository, and form-level File Upload fields
- *Enabled only for REDCap home page*
- *Enabled only for project file repository and forms*

**Send-It Upload Max File Size**
Maximum size (in MB) for a file sent via Send-It. If left blank, the server default applies.

## File Attachments (General)

**Upload Max File Size for General File Attachments**
Applies to miscellaneous file attachment contexts not covered above, including attachments to Descriptive fields and files uploaded in the Data Resolution Workflow.

## Data Resolution Workflow

**Allow File Attachments for Data Queries**
When enabled, users can attach files to open data queries in the Data Resolution Workflow (e.g., uploading source documentation to support a query response). When disabled, this option does not appear within the DRW.

Options: *Disabled* / *Enabled*

> See RC-DE-12 for more on the Data Resolution Workflow.
