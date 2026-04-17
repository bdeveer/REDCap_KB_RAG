RC-API-46

**List Files and Folders (File Repository) API**

| **Article ID** | RC-API-46 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-45 — Create Folder (File Repository) API; RC-API-12 — Export File; RC-API-13 — Import File; RC-API-14 — Delete File; RC-DAG-01 — Data Access Groups; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The List Files and Folders (File Repository) API method returns a listing of everything inside a folder of the project's **File Repository** — both sub-folders and files. Each sub-folder is returned with its own `folder_id`, and each file is returned with its own `doc_id`. These IDs are the handles you use to act on that item with other File Repository API methods (e.g., to list a sub-folder's contents, export a specific file, or delete it).

By default the method lists the **top-level** of the File Repository. Pass a `folder_id` to list the contents of a specific sub-folder instead. The response also surfaces any access restrictions on listed folders: a folder restricted to a User Role returns that role's unique name under `role`, and a folder restricted to a Data Access Group returns the DAG's unique name under `dag`.

This method is the entry point for programmatic navigation of the File Repository — use it first to discover what is in a folder before acting on individual items.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Export privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'list'` for this method. |
| `format` | Optional | Response format: `csv`, `json`, or `xml`. Defaults to `xml` if omitted. |
| `folder_id` | Optional | The `folder_id` of the folder whose contents you want listed. If omitted, the method lists the **top-level directory** of the File Repository. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. If omitted, defaults to the value of `format` (or `xml` if neither is provided). Does not apply to background process calls — in that case, the response is `success:true` or `success:false` in the response format. |

---

# 3. Permissions Required

To call this method, the API token's owner must have **both** of the following in the project:

- **API Export** privilege
- **File Repository** privilege

Calls from tokens lacking either privilege will fail with a permissions error.

---

# 4. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

# 5. Request Examples

## 5.1 Python

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

## 5.2 R

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

## 5.3 cURL

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

## 5.4 PHP

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 6. Response

The API returns the list of files and sub-folders inside the requested folder. Each sub-folder entry has a `folder_id` and each file entry has a `doc_id`. Restricted folders also include a `role` (unique User Role name) and/or `dag` (unique Data Access Group name).

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

When called as a background process (`backgroundProcess=true`), the response is `success:true` or `success:false` in the appropriate format instead of the list itself.

---

# 7. Common Questions

**Q: How do I list the contents of the entire File Repository?**

**A:** The API only lists one folder at a time. Call the method without a `folder_id` to get the top-level, then recursively call it for each sub-folder's `folder_id` in the response to walk the full tree. There is no single "list everything" call.

**Q: What's the difference between `folder_id` and `doc_id` in the response?**

**A:** `folder_id` identifies a sub-folder — you can pass it back into this method to list **its** contents, or use it as the parent in Create Folder (RC-API-45). `doc_id` identifies an individual file in the File Repository — you can use it with other File Repository API methods (export, delete) to act on that file.

**Q: I see `role` and `dag` on some folder entries but not others. Why?**

**A:** Those fields only appear on folders that have an access restriction. A folder restricted to a specific User Role returns that role's unique name under `role`; a folder restricted to a Data Access Group returns the DAG's unique name under `dag`. Unrestricted folders (accessible to all users in the project) omit these fields entirely.

**Q: Does this method list the contents of sub-folders recursively?**

**A:** No. One call returns only the **immediate children** of the requested folder — sub-folders and files one level deep. To build a recursive listing, call the method once per folder and assemble the tree client-side.

**Q: If a folder is DAG-restricted to a DAG I am not in, will it appear in my results?**

**A:** Folder visibility in the API respects the same access rules as the web interface. If your API token's owner does not have access to a restricted folder, that folder will not appear in the listing. Make sure the token belongs to a user with appropriate DAG and User Role assignments before relying on this method for an audit.

**Q: How can I find the `folder_id` of a folder I just created with RC-API-45?**

**A:** The Create Folder method returns the `folder_id` directly in its response. You can also call List (this method) on the parent folder after creation to confirm the new folder appears and to capture its `folder_id`.

---

# 8. Common Mistakes & Gotchas

**Expecting a recursive tree from one call.** The response lists the direct children of the requested folder only. If you need a full File Repository tree, you must walk it yourself by re-calling the method for each nested `folder_id`.

**Confusing `folder_id` and `doc_id`.** These are distinct identifier spaces. Passing a `doc_id` as `folder_id` (or vice versa) will either error or return the wrong thing. Check which field your target entry came from in the response.

**Using the wrong permission type.** This is an **Export** method and requires API Export privileges — unlike Create Folder (RC-API-45), which needs API Import/Update. Tokens with Import/Update rights but not Export rights will be denied, even if the user owning the token can view the File Repository in the web UI.

**Assuming `role` and `dag` fields always appear.** Your code should treat these fields as **optional** in each folder entry. Only restricted folders include them. Looking them up unconditionally (e.g., `folder['role']`) will raise a KeyError on unrestricted folders.

**Not accounting for access restrictions when auditing.** If the token belongs to a user who lacks access to certain DAG- or Role-restricted folders, those folders will be silently excluded from the listing. For a comprehensive inventory, use a token belonging to a user with full project access.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-45 — Create Folder (File Repository) API (creates folders whose contents this method can list)
- RC-API-12 — Export File (download files from record-level file-upload fields — distinct from File Repository files)
- RC-API-13 — Import File (upload files to record-level file-upload fields)
- RC-API-14 — Delete File (remove files from record-level file-upload fields)
- RC-API-25 — Export User Roles API (look up `role_id` values referenced by File Repository restrictions)
- RC-API-28 — Export DAGs API (look up `dag_id` values referenced by File Repository restrictions)
- RC-DAG-01 — Data Access Groups (concept reference for DAG-based folder restriction)
- RC-USER-03 — User Rights: Configuring User Privileges (granting API Export and File Repository privileges)
