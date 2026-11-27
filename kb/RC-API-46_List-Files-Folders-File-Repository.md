

**List Files and Folders (File Repository) API**

| **Article ID** | [RC-API-46 — List Files and Folders (File Repository) API](RC-API-46_List-Files-Folders-File-Repository.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — listing behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md); [RC-API-12 — Export File API](RC-API-12_Export-File.md); [RC-API-13 — Import File API](RC-API-13_Import-File.md); [RC-API-14 — Delete File API](RC-API-14_Delete-File.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Synonyms** | list files and folders in file repository api method; how do i list the file repository contents via the api; api call to get files and folders in the file repository; retrieve file repository listing through the api; get doc ids of file repository files using the api; api method to browse file repository folder contents; programmatically list file repository items with the api |

---

## 1. Overview

The List Files and Folders (File Repository) API method returns a listing of everything inside a folder of the project's **File Repository** — both sub-folders and files. Each sub-folder is returned with its own `folder_id`, and each file is returned with its own `doc_id`. These IDs are the handles you use to act on that item with other File Repository API methods (e.g., to list a sub-folder's contents, export a specific file, or delete it).

By default the method lists the **top-level** of the File Repository. Pass a `folder_id` to list the contents of a specific sub-folder instead. The response also surfaces any access restrictions on listed folders: a folder restricted to a User Role returns that role's unique name under `role`, and a folder restricted to a Data Access Group returns the DAG's unique name under `dag`.

This method is the entry point for programmatic navigation of the File Repository — use it first to discover what is in a folder before acting on individual items.

---

## 2. Key Concepts & Definitions

#### Doc ID
A numeric identifier that uniquely identifies a file in the File Repository. Used to export, delete, or reference specific files.

#### Folder ID
A numeric identifier that uniquely identifies a folder in the File Repository. Used to list contents of a specific folder or as a parent reference when creating sub-folders.

#### Access Restrictions
Folder-level permissions that limit access to specific users based on their Data Access Group or User Role assignment. Restricted folders include `role` and/or `dag` fields in the response.

> **Admin-restricted folders are excluded from the response.** The File Repository supports folders visible only to administrators with access to all projects (15.5.0+). These are **not** returned by this method — up to 16.0.7 they were mistakenly included, corrected from 16.0.8. They are left out even when the token belongs to an administrator who can see them in the web interface. Do not treat this listing as a complete inventory of the File Repository: apart from admin-only folders, it reflects what the calling user may see (see Section 7 for everything that is not returned). See [RC-FILE-01 — File Repository](RC-FILE-01_File-Repository.md).

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Export privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'list'` for this method. |
| `format` | Optional | Response format: `csv`, `json`, or `xml`. Defaults to `xml` if omitted. |
| `folder_id` | Optional | The `folder_id` of the folder whose contents you want listed. If omitted, the method lists the **top-level directory** of the File Repository. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. If omitted, defaults to the value of `format` (or `xml` if neither is provided). |

---

## 4. Permissions Required

REDCap's API documentation lists **both** of the following as requirements for the API token's owner in the project. Set the token up this way:

- **API Export** privilege
- **File Repository** privilege

A user without the **File Repository** privilege receives an HTTP 403 error. Users assigned as a Double Data Entry person in a Double Data Entry project also receive 403.

If the requested `folder_id` does not exist, or the user cannot access it because of a DAG or User Role restriction, the call returns HTTP 400 with:

```
The File Repository folder folder_id=N does not exist or else you do not have permission to that folder because it is DAG-restricted or Role-restricted.
```

---

## 5. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

## 6. Request Examples

### 6.1 Python

List the top-level of the File Repository:

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'fileRepository',
    'action': 'list',
    'format': 'json',
    'returnFormat': 'json'
}

r = requests.post(config['api_url'], data=fields)

print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

List a specific sub-folder (for example, `folder_id=45`):

```python
fields = {
    'token': config['api_token'],
    'content': 'fileRepository',
    'action': 'list',
    'folder_id': 45,
    'format': 'json',
    'returnFormat': 'json'
}
```

### 6.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='fileRepository',
    action='list',
    format='json',
    returnFormat='json'
)
print(result)
```

### 6.3 cURL

```sh
. ./config

$CURL -H "Accept: application/json" \
      -d "token=$API_TOKEN" \
      -d "content=fileRepository" \
      -d "action=list" \
      -d "format=json" \
      -d "returnFormat=json" \
      $API_URL
```

### 6.4 PHP

```php
<?php

include 'config.php';

$fields = array(
    'token'        => $GLOBALS['api_token'],
    'content'      => 'fileRepository',
    'action'       => 'list',
    'format'       => 'json',
    'returnFormat' => 'json'
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $GLOBALS['api_url']);
curl_setopt($ch, CURLOPT_POSTFIELDS, $fields);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE); // Set to TRUE for production use
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);

$output = curl_exec($ch);
print $output;
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

## 7. Response

The API returns the list of files and sub-folders inside the requested folder. Each sub-folder entry has a `folder_id` and each file entry has a `doc_id` — the ID that the File Repository Export a File and Delete a File methods expect ([RC-API-47 — Export a File (File Repository) API](RC-API-47_Export-File-File-Repository.md), [RC-API-49 — Delete a File (File Repository) API](RC-API-49_Delete-File-File-Repository.md)). Names are returned with any HTML tags removed.

**Order.** Sub-folders come first, then files. Each group is sorted by name in natural, case-insensitive order (so `file2` sorts before `File10`).

**`role` and `dag` by format.** In JSON and XML, a folder restricted to a User Role includes `role` (the role's unique name) and a folder restricted to a Data Access Group includes `dag` (the DAG's unique name); unrestricted folders and files omit these fields. CSV always has the same five columns — `folder_id`, `doc_id`, `name`, `role`, `dag` — with blank values where a column does not apply. A restriction to a DAG or role that has since been deleted is treated as no restriction, so the field is omitted (blank in CSV).

**Not returned:**

- Deleted folders, and files in the File Repository's Recycle Bin
- Data export archive files
- Admin-only folders — not listed even for administrators, who can see them in the web interface
- Folders restricted to a DAG or User Role the calling user is not in (see Section 8)

Example response (JSON, `format=json`) for a folder containing one sub-folder and two files:

```json
[
  {
    "folder_id": 45,
    "name": "Study Protocols"
  },
  {
    "folder_id": 46,
    "name": "Restricted Documents",
    "role": "site_coordinator",
    "dag": "site_a"
  },
  {
    "doc_id": 201,
    "name": "consent_form_v3.pdf"
  },
  {
    "doc_id": 202,
    "name": "data_dictionary_v2.csv"
  }
]
```

The `backgroundProcess` parameter has no effect on this method: the normal list is returned.

---

## 8. Common Questions

**Q: How do I list the contents of the entire File Repository?**

**A:** The API only lists one folder at a time. Call the method without a `folder_id` to get the top-level, then recursively call it for each sub-folder's `folder_id` in the response to walk the full tree. There is no single "list everything" call.

**Q: What's the difference between `folder_id` and `doc_id` in the response?**

**A:** `folder_id` identifies a sub-folder — you can pass it back into this method to list **its** contents, or use it as the parent in Create Folder ([RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md)). `doc_id` identifies an individual file in the File Repository — you can use it with other File Repository API methods (export, delete) to act on that file.

**Q: I see `role` and `dag` on some folder entries but not others. Why?**

**A:** In JSON and XML, those fields only appear on folders that have an access restriction. A folder restricted to a specific User Role returns that role's unique name under `role`; a folder restricted to a Data Access Group returns the DAG's unique name under `dag`. Unrestricted folders (accessible to all users in the project) omit these fields entirely, as do folders whose restricting DAG or role has since been deleted. In CSV, every row has all five columns (`folder_id`, `doc_id`, `name`, `role`, `dag`), left blank where they do not apply.

**Q: Does this method list the contents of sub-folders recursively?**

**A:** No. One call returns only the **immediate children** of the requested folder — sub-folders and files one level deep. To build a recursive listing, call the method once per folder and assemble the tree client-side.

**Q: If a folder is DAG-restricted to a DAG I am not in, will it appear in my results?**

**A:** No. A user assigned to a DAG does not see folders restricted to other DAGs, and a user assigned to a User Role does not see folders restricted to other roles. A user not assigned to any DAG sees all DAG-restricted folders; a user not assigned to any role sees all role-restricted folders. Asking for a hidden folder directly by `folder_id` returns the HTTP 400 "does not exist or else you do not have permission" error (see Section 4). Make sure the token belongs to a user with appropriate DAG and User Role assignments before relying on this method for an audit.

**Q: How can I find the `folder_id` of a folder I just created with [RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md)?**

**A:** The Create Folder method returns the `folder_id` directly in its response. You can also call List (this method) on the parent folder after creation to confirm the new folder appears and to capture its `folder_id`.

---

## 9. Common Mistakes & Gotchas

**Expecting a recursive tree from one call.** The response lists the direct children of the requested folder only. If you need a full File Repository tree, you must walk it yourself by re-calling the method for each nested `folder_id`.

**Confusing `folder_id` and `doc_id`.** These are distinct identifier spaces. Passing a `doc_id` as `folder_id` (or vice versa) will either error or return the wrong thing. Check which field your target entry came from in the response.

**Using the wrong permission type.** REDCap's API documentation lists this as an **Export** method requiring API Export privileges — unlike Create Folder ([RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md)), which needs API Import/Update. Give the token owner API Export plus the File Repository privilege; without File Repository the call returns 403.

**Assuming `role` and `dag` fields always appear.** In JSON and XML, treat these fields as **optional** in each folder entry: only restricted folders include them. Looking them up unconditionally (e.g., `folder['role']`) will raise a KeyError on unrestricted folders. In CSV the columns are always present but blank when unused, so test for an empty value instead.

**Not accounting for access restrictions when auditing.** A token owner assigned to a DAG or User Role will not see folders restricted to other DAGs or roles; they are silently excluded from the listing. A user with no DAG and no role assignment sees all DAG- and role-restricted folders. Admin-only folders, deleted items and data export archive files are never listed. For the most complete inventory, use a token belonging to a user with full project access and no DAG or role assignment.

---

## 10. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md) (creates folders whose contents this method can list)
- [RC-API-12 — Export File API](RC-API-12_Export-File.md) (download files from record-level file-upload fields — distinct from File Repository files)
- [RC-API-13 — Import File API](RC-API-13_Import-File.md) (upload files to record-level file-upload fields)
- [RC-API-14 — Delete File API](RC-API-14_Delete-File.md) (remove files from record-level file-upload fields)
- [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) (look up `role_id` values referenced by File Repository restrictions)
- [RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md) (look up `dag_id` values referenced by File Repository restrictions)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (concept reference for DAG-based folder restriction)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (granting API Export and File Repository privileges)
