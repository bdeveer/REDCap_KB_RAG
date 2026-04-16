RC-API-45

**Create Folder (File Repository) API**

| **Article ID** | RC-API-45 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-12 — Export File; RC-API-13 — Import File; RC-API-14 — Delete File; RC-DAG-01 — Data Access Groups; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Create Folder (File Repository) API method creates a new folder inside the project's **File Repository** — the project-level file storage area that holds shared documents, auto-generated files (e.g., e-consent PDFs, data export archives), and any files uploaded through the File Repository page.

Unlike the Import File / Export File / Delete File methods (RC-API-12, RC-API-13, RC-API-14), which operate on **file-upload fields attached to individual records**, this method operates on the **project-wide File Repository** and only creates directory structure (no file content). The method returns the `folder_id` of the newly created folder, which can then be used as a parent reference for subsequent nested folders or for uploading files into that folder.

The method optionally supports creating the new folder as a **sub-folder** of an existing folder, and optionally restricting access to a specific **Data Access Group (DAG)** or **User Role**.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Import/Update privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'createFolder'` for this method. |
| `name` | Required | The desired name of the folder to be created. Maximum length = **150 characters**. |
| `format` | Optional | Response format: `csv`, `json`, or `xml`. Defaults to `xml` if omitted. |
| `folder_id` | Optional | The `folder_id` of the parent folder under which the new folder should be created. If omitted, the folder is created at the **top level** of the File Repository. |
| `dag_id` | Optional | The `dag_id` of a DAG to restrict access to. If omitted, the folder is accessible to users in all DAGs and users in no DAGs. |
| `role_id` | Optional | The `role_id` of a User Role to restrict access to. If omitted, the folder is accessible to users in all User Roles and users in no User Roles. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. If omitted, defaults to the value of `format` (or `xml` if neither is provided). Does not apply to background process calls — in that case, the response is `success:true` or `success:false` in the response format. |

---

# 3. Permissions Required

To call this method, the API token's owner must have **both** of the following in the project:

- **API Import/Update** privilege
- **File Repository** privilege

Calls from tokens lacking either privilege will fail with a permissions error.

---

# 4. Endpoint

```
POST https://redcap.school.wakehealth.edu/api/
```

Only `POST` is supported.

---

# 5. Request Examples

## 5.1 Python

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

## 5.2 R

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

## 5.3 cURL

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

## 5.4 PHP

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 6. Response

On success, the API returns the `folder_id` of the newly created folder in the requested format.

Example success response (JSON, `format=json`):

```json
[{"folder_id":45}]
```

Example success response (XML, default):

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<folders>
    <folder>
        <folder_id>45</folder_id>
    </folder>
</folders>
```

When called as a background process (`backgroundProcess=true`), the response is `success:true` or `success:false` in the appropriate format instead of the `folder_id`.

---

# 7. Common Questions

**Q: What's the difference between this method and Import File (RC-API-13)?**

**A:** Import File uploads a file to a **file-upload field on a record** (record-level data). Create Folder operates on the **File Repository**, which is a separate project-level file storage area accessed from the project's left-hand menu. They use different `content` values (`file` vs `fileRepository`) and serve different purposes.

**Q: Where do I find the `folder_id` of an existing parent folder so I can nest a new folder inside it?**

**A:** REDCap provides a separate File Repository "list" API method (not covered in this article) that returns the folder hierarchy with each folder's `folder_id`. You can also capture the `folder_id` returned by a previous `createFolder` call and reuse it as the `folder_id` parameter for nested folders.

**Q: Can I restrict a folder to both a DAG and a User Role at the same time?**

**A:** Yes. If you provide both `dag_id` and `role_id`, access to the folder is restricted to users who are in that DAG **and** assigned to that User Role. Omitting either parameter means no restriction on that dimension.

**Q: What happens if I create a folder with a name that already exists at the same level?**

**A:** REDCap does not enforce unique folder names within the File Repository — you can end up with two folders at the same level with identical `name` values but different `folder_id`s. To avoid confusion, check for existing folders before creating a new one.

**Q: Is the folder name limited in length?**

**A:** Yes — maximum 150 characters. Names longer than that will be rejected by the API.

**Q: Does this method support calling through a background process?**

**A:** Yes. When `backgroundProcess=true`, the response format changes to `success:true` / `success:false` instead of returning the `folder_id`, and the `returnFormat` parameter does not apply.

---

# 8. Common Mistakes & Gotchas

**Confusing the File Repository with record-level file uploads.** Create Folder only affects the project-level File Repository — it has no connection to file-upload fields attached to records. If you need to store a file against a specific record, use Import File (RC-API-13) instead. Files stored in the File Repository are not linked to any particular record.

**Forgetting the File Repository privilege.** The API token's owner must have **both** API Import/Update and File Repository privileges assigned in User Rights. Tokens issued to users with API rights but no File Repository access will fail this call with a permissions error. See RC-USER-03 — User Rights: Configuring User Privileges for how to grant File Repository access.

**Assuming DAG/Role restriction is inherited from the parent folder.** Access restrictions must be set explicitly on each folder via `dag_id` and/or `role_id`. A sub-folder does **not** automatically inherit the restrictions of its parent — each folder's access is evaluated independently.

**Passing the DAG name instead of the `dag_id`.** The `dag_id` parameter is the numeric internal ID of the DAG, not its unique name or display label. Call the Export DAGs API (RC-API-28) first to retrieve the `dag_id` values if you do not already know them.

**Leaving `dag_id` and `role_id` unset when you want the folder to be generally accessible.** When both are omitted, the folder is accessible to users in all DAGs and all User Roles — including users assigned to no DAG and no User Role. This is almost always the desired behavior, but be aware that "unrestricted" means exactly that.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-12 — Export File (download files from record-level file-upload fields)
- RC-API-13 — Import File (upload files to record-level file-upload fields)
- RC-API-14 — Delete File (remove files from record-level file-upload fields)
- RC-API-28 — Export DAGs API (look up `dag_id` values for folder access restriction)
- RC-API-25 — Export User Roles API (look up `role_id` values for folder access restriction)
- RC-DAG-01 — Data Access Groups (concept reference for `dag_id`)
- RC-USER-03 — User Rights: Configuring User Privileges (granting API and File Repository privileges)
