RC-API-48

**Import a File (File Repository) API**

| **Article ID** | RC-API-48 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-45 — Create Folder (File Repository) API; RC-API-46 — List Files and Folders (File Repository) API; RC-API-47 — Export a File (File Repository) API; RC-API-13 — Import File; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Import a File (File Repository) API method uploads a single file into the project's **File Repository** — the project-level file store. The file may be placed in any existing sub-folder by supplying that folder's `folder_id`; if no `folder_id` is provided, the file is placed at the **top level** of the File Repository.

The file is transmitted as **multipart form data** (a file upload), not as a JSON string or base64-encoded text. This is the File Repository counterpart to Import File (RC-API-13), which uploads to a record-level file-upload field. The two endpoints look similar but operate on different storage areas.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Import/Update privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `file` | Required | The actual file to upload. Sent as multipart form data, not as a string. |
| `folder_id` | Optional | The `folder_id` of the folder into which the file should be placed. If omitted, the file is placed at the top level of the File Repository. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the success response. If omitted, defaults to `xml`. Does not apply to background process calls — in that case, the response is `success:true` or `success:false` in the response format. |

Note: this method has **no `format` parameter**. The successful response is not a structured data payload (see Section 6), so there is no response format to choose. `returnFormat` only controls how error messages are serialized.

---

# 3. Permissions Required

To call this method, the API token's owner must have **both** of the following in the project:

- **API Import/Update** privilege
- **File Repository** privilege

If `folder_id` is provided and the target folder is restricted to a DAG or User Role the user is not part of, the call will fail.

---

# 4. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

# 5. Request Examples

## 5.1 Python

Import a file to the top level of the File Repository:

```python
from config import config
import requests

file = '/tmp/study_protocol_v3.pdf'

fields = {
    'token': config['api_token'],
    'content': 'fileRepository',
    'action': 'import',
    'returnFormat': 'json'
}

with open(file, 'rb') as file_obj:
    r = requests.post(
        config['api_url'],
        data=fields,
        files={'file': file_obj}
    )

print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

Place the file inside a specific sub-folder (for example, `folder_id=45`):

```python
fields = {
    'token': config['api_token'],
    'content': 'fileRepository',
    'action': 'import',
    'folder_id': 45,
    'returnFormat': 'json'
}
```

## 5.2 R

```r
source('config.R')
library(RCurl)

file = '/tmp/study_protocol_v3.pdf'

result <- postForm(
    api_url,
    token=api_token,
    content='fileRepository',
    action='import',
    returnFormat='json',
    file=httr::upload_file(file)
)
print(result)
```

## 5.3 cURL

```sh
. ./config

$CURL -H "Accept: application/json" \
      -F "token=$API_TOKEN" \
      -F "content=fileRepository" \
      -F "action=import" \
      -F "returnFormat=json" \
      -F "file=@/tmp/study_protocol_v3.pdf" \
      $API_URL
```

## 5.4 PHP

```php
<?php

include 'config.php';

$file = '/tmp/study_protocol_v3.pdf';
$file = (function_exists('curl_file_create')
    ? curl_file_create($file, 'application/pdf', 'study_protocol_v3.pdf')
    : "@$file");

$fields = array(
    'token'        => $GLOBALS['api_token'],
    'content'      => 'fileRepository',
    'action'       => 'import',
    'file'         => $file,
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

Unlike other File Repository API methods, Import a File does **not** return a structured payload in the response body. A successful upload is indicated solely by an **HTTP 200** response. No `doc_id`, JSON object, or XML document is returned.

If you need the `doc_id` of the file you just imported (e.g., to download, delete, or reference it later), call List Files and Folders (RC-API-46) on the target folder after the import completes — the newly uploaded file will appear in that listing with its `doc_id`.

On error, the response body is an error message serialized in the format specified by `returnFormat` (or `xml` by default).

When called as a background process (`backgroundProcess=true`), the response is `success:true` or `success:false` in the appropriate format instead of an empty body.

> **Note:** If your institution runs a different REDCap version, confirm the response shape via the API Playground.

---

# 7. Common Questions

**Q: How do I find out what `doc_id` was assigned to the file I just imported?**

**A:** The import response itself does not include a `doc_id`. Immediately after import, call List Files and Folders (RC-API-46) on the target folder — the new file will appear as an entry with a `doc_id`. Match it by filename (or by import order) to identify the newly uploaded file.

**Q: What's the difference between this method and Import File (RC-API-13)?**

**A:** RC-API-13 uploads a file to a **record-level file-upload field** — the file becomes attached to a specific record through a field on an instrument. RC-API-48 uploads to the **project-level File Repository**, which is a shared, project-wide file store separate from record data. They use different `content` values (`file` vs `fileRepository`) and different required parameters (RC-API-13 requires `record`/`field`; RC-API-48 requires only `file` and optionally `folder_id`).

**Q: How do I upload into a specific sub-folder instead of the top level?**

**A:** Pass the target folder's `folder_id` as a parameter. Discover the `folder_id` by calling List Files and Folders (RC-API-46) on the parent folder, or capture it from the response of Create Folder (RC-API-45) if the folder was created programmatically.

**Q: What file types and sizes are allowed?**

**A:** The File Repository respects the same file type and size limits configured for the project. The API does not bypass those limits — a file that would be rejected through the web interface will also be rejected through the API.

**Q: Can I upload a file to a folder that is restricted to a DAG or User Role I'm not in?**

**A:** No. If the target folder is DAG- or Role-restricted and the API token owner does not have access, the import will fail. Use a token belonging to a user with access to that folder, or upload to an unrestricted folder first and move it through the web UI if needed.

**Q: Can I upload multiple files in one call?**

**A:** No. This method uploads one file per call. To bulk-upload, loop in your client code and call the endpoint once per file.

---

# 8. Common Mistakes & Gotchas

**Sending the file as a string or base64-encoded blob.** The `file` parameter must be an actual file upload transmitted as multipart form data. Attempts to send file contents as a plain string, a JSON field, or base64 text will be rejected. Use your HTTP library's file upload mechanism (`files=` in Python requests, `httr::upload_file()` in R, `-F "file=@..."` in cURL).

**Expecting a `doc_id` in the response.** Import a File returns an empty HTTP 200 response on success — no `doc_id`, no JSON, no XML. Code that parses the response body for identifiers will break. Use List Files and Folders (RC-API-46) afterward to discover the new `doc_id`.

**Uploading to a non-existent or inaccessible `folder_id`.** If the `folder_id` does not exist in this project, or if it points to a folder restricted to a DAG or User Role the token owner is not part of, the call will error. List the File Repository first to confirm the `folder_id` is valid for your token before uploading.

**Assuming files with duplicate names are de-duplicated.** The File Repository does not enforce unique filenames within a folder. Uploading a file with the same name as an existing one creates a second entry, each with its own `doc_id`. If you want to "replace" a file, delete the old `doc_id` first (once the Delete File API is covered — see Section 9) and then import the new version.

**Using this method to attach a file to a record.** Record-attached files belong in file-upload fields, not the File Repository. Use RC-API-13 (Import File) for record-level uploads. The two endpoints look superficially similar but write to different storage areas.

**Closing the file handle too early in Python.** When using `requests.post(..., files={'file': file_obj})`, keep the file handle open until after the request returns. A `with open(...)` context manager (as shown in Section 5.1) is the safest pattern.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-45 — Create Folder (File Repository) API (create folders to import into)
- RC-API-46 — List Files and Folders (File Repository) API (discover `folder_id`s before import; discover the new file's `doc_id` after import)
- RC-API-47 — Export a File (File Repository) API (download a file from the File Repository)
- RC-API-13 — Import File (upload files to record-level file-upload fields — distinct from File Repository uploads)
- RC-API-12 — Export File (download files from record-level file-upload fields)
- RC-API-14 — Delete File (remove files from record-level file-upload fields)
- RC-USER-03 — User Rights: Configuring User Privileges (granting API Import/Update and File Repository privileges)
