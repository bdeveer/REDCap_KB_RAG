RC-API-49

**Delete a File (File Repository) API**

| **Article ID** | RC-API-49 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-45 — Create Folder (File Repository) API; RC-API-46 — List Files and Folders (File Repository) API; RC-API-47 — Export a File (File Repository) API; RC-API-48 — Import a File (File Repository) API; RC-API-14 — Delete File; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Delete a File (File Repository) API method removes a single file from the project's **File Repository** by its `doc_id`. The deletion is a **soft delete** — the file is moved to the project's File Repository Recycle Bin, where it remains for up to **30 days** before being permanently purged. During that retention window the file can be restored from the Recycle Bin through the web interface.

This method is the File Repository counterpart to Delete File (RC-API-14), which removes a file attached to a record-level file-upload field. The two endpoints look similar but act on different storage areas.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Import/Update privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `doc_id` | Required | The `doc_id` of the file to delete. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. If omitted, defaults to `xml`. Does not apply to background process calls — in that case, the response is `success:true` or `success:false` in the response format. |

Note: this method has **no `format` parameter** because a successful response does not include a structured data payload (see Section 6). `returnFormat` only controls how errors are serialized.

---

# 3. Permissions Required

To call this method, the API token's owner must have **both** of the following in the project:

- **API Import/Update** privilege
- **File Repository** privilege

The user must also have access to the folder containing the target file. Files in folders restricted to a DAG or User Role the user is not part of cannot be deleted through this method.

---

# 4. Endpoint

```
POST https://your-redcap-instance.edu/api/
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
    'action': 'delete',
    'doc_id': 201,
    'returnFormat': 'json'
}

r = requests.post(config['api_url'], data=fields)

print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 5.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='fileRepository',
    action='delete',
    doc_id='201',
    returnFormat='json'
)
print(result)
```

## 5.3 cURL

```sh
. ./config

$CURL -d "token=$API_TOKEN" \
      -d "content=fileRepository" \
      -d "action=delete" \
      -d "doc_id=201" \
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
    'action'       => 'delete',
    'doc_id'       => 201,
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

A successful delete returns an **HTTP 200** response with no structured data payload — no JSON, XML, CSV, or confirmation object. The empty body plus a 200 status is the sole indicator of success, matching the pattern of Import a File (RC-API-48).

On error, the response body is an error message serialized in the format specified by `returnFormat` (or `xml` by default).

When called as a background process (`backgroundProcess=true`), the response is `success:true` or `success:false` in the appropriate format instead of an empty body.

> **Note:** If your institution runs a different REDCap version, confirm the response shape via the API Playground.

---

# 7. Common Questions

**Q: What happens to the file after I delete it?**

**A:** The file is moved to the project's File Repository **Recycle Bin**, where it remains for up to **30 days**. During that retention window, a user with File Repository access can restore the file through the web interface. After 30 days the file is permanently purged and cannot be recovered.

**Q: How do I find the `doc_id` of the file I want to delete?**

**A:** Call List Files and Folders (RC-API-46) on the folder that contains the file. Each file entry in the response includes a `doc_id`. Once you have the right `doc_id`, pass it to this method.

**Q: What's the difference between this method and Delete File (RC-API-14)?**

**A:** RC-API-14 deletes a file attached to a **record-level file-upload field** — the file lives on an instrument's file field for a specific record. RC-API-49 deletes a file from the **project-level File Repository**, which is a shared, project-wide file store. They use different `content` values (`file` vs `fileRepository`) and different required parameters (RC-API-14 takes `record`/`field`/`event`, RC-API-49 takes `doc_id`).

**Q: Can I delete multiple files in one call?**

**A:** No. This method deletes one file per call. To bulk-delete, iterate in your client code and call the endpoint once per `doc_id`.

**Q: Can I restore a file I deleted through the API?**

**A:** Yes — within the 30-day retention window. The API does not currently expose a "restore" action, but a user with File Repository access can restore files from the Recycle Bin through the web interface.

**Q: What happens if I try to delete a file I do not have access to?**

**A:** The call will fail with a permissions error. Access is governed by the same DAG and User Role rules that apply to the web interface — a file inside a folder restricted to a DAG or User Role you are not part of is not visible or deletable via the API.

---

# 8. Common Mistakes & Gotchas

**Passing a `folder_id` instead of a `doc_id`.** These are distinct identifier spaces. A `folder_id` targets a folder; a `doc_id` targets a file. Confirm the value you are passing came from the `doc_id` field of a List response (RC-API-46), not the `folder_id` field.

**Assuming deletion is immediate and permanent.** Files are **soft-deleted**, not immediately destroyed. They remain in the Recycle Bin for up to 30 days. If your use case is a compliance-driven hard delete (e.g., immediate purge of PHI), the API alone does not achieve that — coordinate with your REDCap administrator for immediate purge from the Recycle Bin.

**Using this method to delete files from record file-upload fields.** Record-attached files are not in the File Repository — use RC-API-14 (Delete File) for those. The two endpoints look superficially similar but act on different storage areas.

**Deleting files inside restricted folders without appropriate access.** If the containing folder is DAG- or Role-restricted and the API token's owner does not have access, the call will error. For auditing or full-cleanup workflows, use a token belonging to a user with access across the relevant folders.

**Deleting a file without keeping a record of its metadata.** Once deleted, the file's metadata may be difficult to reconstruct if it's purged after 30 days. If you need an audit trail of what was deleted, capture the file's `doc_id`, filename, and containing `folder_id` from List (RC-API-46) *before* calling delete.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-45 — Create Folder (File Repository) API (create folders in the File Repository)
- RC-API-46 — List Files and Folders (File Repository) API (discover `doc_id`s before deleting)
- RC-API-47 — Export a File (File Repository) API (download a file — e.g., as a backup before deletion)
- RC-API-48 — Import a File (File Repository) API (upload files into the File Repository)
- RC-API-14 — Delete File (remove files from record-level file-upload fields — distinct from File Repository deletes)
- RC-API-12 — Export File (download files from record-level file-upload fields)
- RC-API-13 — Import File (upload files to record-level file-upload fields)
- RC-USER-03 — User Rights: Configuring User Privileges (granting API Import/Update and File Repository privileges)
