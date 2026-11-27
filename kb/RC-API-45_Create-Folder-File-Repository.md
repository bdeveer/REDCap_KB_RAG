

**Create Folder (File Repository) API**

| **Article ID** | [RC-API-45 — Create Folder (File Repository) API](RC-API-45_Create-Folder-File-Repository.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — folder creation behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-12 — Export File API](RC-API-12_Export-File.md); [RC-API-13 — Import File API](RC-API-13_Import-File.md); [RC-API-14 — Delete File API](RC-API-14_Delete-File.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Synonyms** | create folder in file repository api method; how do i make a file repository folder via the api; api call to create a new folder in the file repository; add a subfolder to the file repository through the api; programmatically create file repository folders with the api; api method to organize the file repository into folders; create file repository folder assigned to a dag via api |

---

## 1. Overview

The Create Folder (File Repository) API method creates a new folder inside the project's **File Repository** — the project-level file storage area that holds shared documents, auto-generated files (e.g., e-consent PDFs, data export archives), and any files uploaded through the File Repository page. The data export archives are visible on the File Repository page only; the API's File Repository methods do not expose them.

Unlike the Import File / Export File / Delete File methods ([RC-API-12 — Export File API](RC-API-12_Export-File.md), [RC-API-13 — Import File API](RC-API-13_Import-File.md), [RC-API-14 — Delete File API](RC-API-14_Delete-File.md)), which operate on **file-upload fields attached to individual records**, this method operates on the **project-wide File Repository** and only creates directory structure (no file content). The method returns the `folder_id` of the newly created folder, which can then be used as a parent reference for subsequent nested folders or for uploading files into that folder.

The method optionally supports creating the new folder as a **sub-folder** of an existing folder, and optionally restricting access to a specific **Data Access Group (DAG)** or **User Role**.

---

## 2. Key Concepts & Definitions

#### File Repository
The project-level file storage area in REDCap, separate from record-level file-upload fields. It holds shared documents, generated files (e.g., e-consent PDFs, data exports — the latter shown in the UI only, not through the API), and any files uploaded through the File Repository interface. Access is controlled by folder-level permissions.

#### Folder ID
A numeric identifier that uniquely identifies a folder in the File Repository. Used as the parent reference when creating sub-folders or uploading files into specific locations.

#### Data Access Group (DAG)
A logical division of project users and records that enforces row-level access control. When a folder is restricted to a DAG, users in that DAG and users not assigned to any DAG can access it; users in other DAGs cannot.

#### User Role
A template of permissions that can be assigned to users as a group. When a folder is restricted to a role, users assigned to that role and users with no role can access it; users in other roles cannot.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Import/Update privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'createFolder'` for this method. |
| `name` | Required | The desired name of the folder to be created. Must be unique among the folders directly under the same parent. Maximum length = **150 characters**; longer names are shortened, not rejected. Avoid the characters `/ \ : * ? " < > \|` (see the version caveat below). |
| `format` | Optional | Response format: `csv`, `json`, or `xml`. Defaults to `xml` if omitted. |
| `folder_id` | Optional | The `folder_id` of the parent folder under which the new folder should be created. If omitted, the folder is created at the **top level** of the File Repository. |
| `dag_id` | Optional | The numeric `dag_id` of a DAG to restrict access to. If omitted, the folder is accessible to users in all DAGs and users in no DAGs. |
| `role_id` | Optional | The numeric `role_id` of a User Role to restrict access to. If omitted, the folder is accessible to users in all User Roles and users in no User Roles. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. If omitted, defaults to the value of `format` (or `xml` if neither is provided). |

> **Version caveat (16.0.61 LTS vs 17.3.31 LTS / 17.6):** REDCap cleans special characters out of folder names, and the two lines do it differently. On 16.0.61 LTS, characters such as `/ \ : * ? " < > |` are removed and accented letters are converted to plain ones (`É` becomes `E`). On 17.3.31 LTS and 17.6, accents are kept, `< > : " | ? *` are replaced with `_`, and only the part after the last `/` or `\` is kept — so `Site A/Visits` becomes `Visits` on 17 but `Site AVisits` on 16. Avoid `/ \ : * ? " < > |` in folder names so the result is the same on every version.

---

## 4. Permissions Required

To call this method, the API token's owner must have **both** of the following in the project:

- **API Import/Update** privilege
- **File Repository** privilege

Calls from tokens lacking either privilege will fail with a permissions error (HTTP 403). In projects using Double Data Entry, users designated as Data Entry Person #1 or #2 also receive a 403.

---

## 5. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

## 6. Request Examples

### 6.1 Python

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'fileRepository',
    'action': 'createFolder',
    'name': 'Study Protocols',
    'format': 'json',
    'returnFormat': 'json'
}

r = requests.post(config['api_url'], data=fields)

print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

To create a sub-folder under an existing folder (for example, `folder_id=45`):

```python
fields = {
    'token': config['api_token'],
    'content': 'fileRepository',
    'action': 'createFolder',
    'name': 'Version 2',
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
    action='createFolder',
    name='Study Protocols',
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
      -d "action=createFolder" \
      -d "name=Study Protocols" \
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
    'action'       => 'createFolder',
    'name'         => 'Study Protocols',
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

On success, the API returns the `folder_id` of the newly created folder in the requested format.

Example success response (JSON, `format=json`):

```json
[{"folder_id":45}]
```

Example success response (XML, default):

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<items>
    <item>
        <folder_id>45</folder_id>
    </item>
</items>
```

The `backgroundProcess` parameter has no effect on this method; the normal `folder_id` response is always returned.

### 7.1 Errors

| Situation | HTTP status | Message / behaviour |
|---|---|---|
| `name` missing or empty | 400 | Error stating the folder name is missing |
| A folder with the same name already exists directly under the same parent | 400 | Error stating a folder with that same name already exists in this directory |
| `folder_id` is not numeric | 400 | `folder_id is not valid` |
| Parent `folder_id` does not exist, was deleted, or is DAG/role-restricted away from you | 400 | `The File Repository folder folder_id=N does not exist or else you do not have permission to that folder because it is DAG-restricted or Role-restricted.` |
| Token user lacks API Import/Update or File Repository rights, or is a Double Data Entry person | 403 | Permissions error |
| `dag_id` or `role_id` is not a valid ID in the project | — | No error; the folder is created **without** that restriction |

---

## 8. Common Questions

**Q: What's the difference between this method and Import File ([RC-API-13 — Import File API](RC-API-13_Import-File.md))?**

**A:** Import File uploads a file to a **file-upload field on a record** (record-level data). Create Folder operates on the **File Repository**, which is a separate project-level file storage area accessed from the project's left-hand menu. They use different `content` values (`file` vs `fileRepository`) and serve different purposes.

**Q: Where do I find the `folder_id` of an existing parent folder so I can nest a new folder inside it?**

**A:** REDCap provides a separate File Repository "list" API method (not covered in this article) that returns the folder hierarchy with each folder's `folder_id`. You can also capture the `folder_id` returned by a previous `createFolder` call and reuse it as the `folder_id` parameter for nested folders.

**Q: Can I restrict a folder to both a DAG and a User Role at the same time?**

**A:** Yes. If you provide both `dag_id` and `role_id`, a user must pass both checks: they must be in that DAG (or in no DAG) **and** assigned to that User Role (or to no role). Omitting either parameter means no restriction on that dimension.

**Q: What happens if I create a folder with a name that already exists at the same level?**

**A:** The call is rejected with HTTP 400 and a message saying a folder with that same name already exists in this directory. Folder names must be unique among the folders directly under the same parent; the same name can be reused under a different parent. If your script may run more than once, list the parent folder's contents first and reuse the existing `folder_id` instead of creating a new folder.

**Q: Is the folder name limited in length?**

**A:** Yes — maximum 150 characters. Longer names are not rejected; REDCap silently shortens them to 150. The limit is counted in bytes, so names with accented or non-Latin characters keep fewer than 150 characters. Keep names well under the limit so the stored name matches what you sent.

**Q: Does this method support calling through a background process?**

**A:** No. The `backgroundProcess` parameter has no effect on this method; the folder is created immediately and the normal `folder_id` response is returned.

---

## 9. Common Mistakes & Gotchas

**Confusing the File Repository with record-level file uploads.** Create Folder only affects the project-level File Repository — it has no connection to file-upload fields attached to records. If you need to store a file against a specific record, use Import File ([RC-API-13 — Import File API](RC-API-13_Import-File.md)) instead. Files stored in the File Repository are not linked to any particular record.

**Forgetting the File Repository privilege.** The API token's owner must have **both** API Import/Update and File Repository privileges assigned in User Rights. Tokens issued to users with API rights but no File Repository access will fail this call with a permissions error. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) for how to grant File Repository access.

**Assuming DAG/Role restriction is inherited from the parent folder.** Access restrictions must be set explicitly on each folder via `dag_id` and/or `role_id`. A new sub-folder does **not** copy its parent's DAG or role setting. In practice, REDCap checks every parent folder on the path, so users blocked from a parent folder cannot reach its sub-folders anyway. Still, set restrictions explicitly on each folder so that each folder's own setting matches who should see it.

**Passing the DAG name instead of the `dag_id`.** The `dag_id` parameter is the numeric internal ID of the DAG, not its unique name or display label (the same applies to `role_id`). An invalid value — such as a unique DAG name — is ignored without any error, and the folder is created **unrestricted**. Call the Export DAGs API ([RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md)) or Export User Roles API ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)) first to retrieve the numeric IDs, and after creating a restricted folder, check it with the File Repository list method to confirm the restriction was applied.

**Creating duplicate folders when a script re-runs.** A second `createFolder` call with the same name under the same parent fails with HTTP 400. Build scripts to look up existing folders first rather than treating that error as unexpected.

**Using path separators or special characters in the name.** A name like `Site A/Visits` does not create nested folders, and REDCap 16 and 17 clean it differently (see the version caveat in Section 3). Create nested folders with separate calls using `folder_id`, and avoid `/ \ : * ? " < > |` in names.

**Leaving `dag_id` and `role_id` unset when you want the folder to be generally accessible.** When both are omitted, the folder is accessible to users in all DAGs and all User Roles — including users assigned to no DAG and no User Role. This is almost always the desired behavior, but be aware that "unrestricted" means exactly that.

---

## 10. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-12 — Export File API](RC-API-12_Export-File.md) (download files from record-level file-upload fields)
- [RC-API-13 — Import File API](RC-API-13_Import-File.md) (upload files to record-level file-upload fields)
- [RC-API-14 — Delete File API](RC-API-14_Delete-File.md) (remove files from record-level file-upload fields)
- [RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md) (look up `dag_id` values for folder access restriction)
- [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) (look up `role_id` values for folder access restriction)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (concept reference for `dag_id`)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (granting API and File Repository privileges)
