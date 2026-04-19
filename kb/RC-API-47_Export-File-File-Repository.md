RC-API-47

**Export a File (File Repository) API**

| **Article ID** | RC-API-47 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects (all types) |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-45 — Create Folder (File Repository) API; RC-API-46 — List Files and Folders (File Repository) API; RC-API-12 — Export File; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Export a File (File Repository) API method downloads a single file stored in the project's **File Repository** by its `doc_id`. The method returns the **raw file content** (the bytes of the file itself) — not JSON, CSV, or XML data. Callers must write the response to disk (or a byte stream) rather than treating it as text.

Because this method acts on a specific file by `doc_id`, you normally discover the `doc_id` first by calling List Files and Folders (RC-API-46), which enumerates the files in a given folder and returns each file's `doc_id`. Export a File is the File Repository analogue of Export File (RC-API-12), which downloads a file from a record-level file-upload field. The two methods look similar but operate on different storage areas of the project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | The API token specific to your REDCap project and username. Each token is unique per user per project. Requires API Export privileges **and** File Repository privileges in the project. |
| `content` | Required | Always `'fileRepository'` for this method. |
| `action` | Required | Always `'export'` for this method. |
| `doc_id` | Required | The `doc_id` of the specific file in the File Repository to download. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the returned file content. If omitted, defaults to `xml`. Does not apply to background process calls — in that case, the response is `success:true` or `success:false` in the response format. |

Note: this method has **no `format` parameter**, because the body of a successful response is binary file content rather than a structured data format. `returnFormat` only controls how error messages are serialized.

---

# 3. Permissions Required

To call this method, the API token's owner must have **both** of the following in the project:

- **API Export** privilege
- **File Repository** privilege

In addition, the user's DAG and User Role assignments must grant access to the folder containing the target file. Attempting to export a file that sits in a DAG- or Role-restricted folder the user cannot see will fail.

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
    'action': 'export',
    'doc_id': 201,
    'returnFormat': 'json'
}

r = requests.post(config['api_url'], data=fields)

print('HTTP Status: ' + str(r.status_code))

# Write the binary response to disk
with open('/tmp/exported_file.bin', 'wb') as f:
    f.write(r.content)
```

> **Tip:** The filename and MIME type can be recovered from the response's `Content-Disposition` and `Content-Type` headers when present.

## 5.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='fileRepository',
    action='export',
    doc_id='201',
    returnFormat='json',
    binary=TRUE
)
writeBin(result, '/tmp/exported_file.bin')
```

## 5.3 cURL

```sh
. ./config

$CURL -d "token=$API_TOKEN" \
      -d "content=fileRepository" \
      -d "action=export" \
      -d "doc_id=201" \
      -d "returnFormat=json" \
      -o /tmp/exported_file.bin \
      $API_URL
```

The `-o` flag writes the raw response body to a file, which is what you want for binary content.

## 5.4 PHP

```php
<?php

include 'config.php';

$fields = array(
    'token'        => $GLOBALS['api_token'],
    'content'      => 'fileRepository',
    'action'       => 'export',
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
file_put_contents('/tmp/exported_file.bin', $output);
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 6. Response

On success, the response **body is the raw contents of the file** (binary data). The HTTP status code will be 200. Filename and MIME type information is typically provided via response headers (e.g., `Content-Disposition: attachment; filename="consent_form_v3.pdf"` and `Content-Type: application/pdf`).

On error, the response body is an error message serialized in the format specified by `returnFormat` (or `xml` by default).

When called as a background process (`backgroundProcess=true`), the response is `success:true` or `success:false` in the appropriate format instead of the file contents.

---

# 7. Common Questions

**Q: How do I find the `doc_id` of the file I want to export?**

**A:** Call List Files and Folders (RC-API-46) on the folder that contains the file. Each file entry in the response includes a `doc_id`. If the file is nested under a sub-folder, call List on the parent folder first to get the sub-folder's `folder_id`, then call List again on that sub-folder to find the file's `doc_id`.

**Q: Why can't I see the exported file in my terminal or browser when I run the request?**

**A:** The response body is raw binary content, not text. Printing it to a terminal can garble non-text bytes. Always write the response to a file (using `-o` in cURL, `r.content` with `wb` in Python, `writeBin` in R, etc.) and open it with a viewer appropriate to the file type (PDF viewer, image viewer, spreadsheet app, etc.).

**Q: How do I recover the original filename and extension?**

**A:** The original filename is provided in the `Content-Disposition` response header, and the MIME type is provided in `Content-Type`. If your HTTP client exposes response headers, you can use those to save the file with its original name and detect its type.

**Q: What's the difference between this method and Export File (RC-API-12)?**

**A:** RC-API-12 exports a file from a **record-level file-upload field** — the file is attached to a specific record through a field on an instrument. RC-API-47 exports a file from the **project-level File Repository**, which is a shared, project-wide file store separate from record data. They use different `content` values (`file` vs `fileRepository`) and different parameters (RC-API-12 takes `record`/`field`/`event`, RC-API-47 takes `doc_id`).

**Q: Is there a file size limit?**

**A:** The API respects the same file size limits the File Repository imposes in the web UI. Very large files may require increased timeouts on your HTTP client.

**Q: Can I export a whole folder's worth of files in one call?**

**A:** No. This method exports one file per call, identified by `doc_id`. To bulk-download a folder, first call List (RC-API-46) to enumerate the `doc_id`s, then iterate and call Export a File for each.

---

# 8. Common Mistakes & Gotchas

**Treating the response as JSON or text.** The body on success is raw file bytes. Parsing it as JSON or decoding it as UTF-8 will corrupt binary files (PDFs, images, Office docs, zip archives). Write the response directly to disk in binary mode and then open it as the appropriate file type.

**Confusing `doc_id` with `folder_id` or `record_id`.** `doc_id` uniquely identifies a file in the File Repository. Passing a `folder_id` (from a list response) or a record's primary key will not work — you will get a not-found or permissions error. Confirm you are passing the identifier that came from the `doc_id` field of a List response.

**Assuming the caller sees every file in the project.** If the target file lives inside a folder restricted to a DAG or User Role that the API token owner is not part of, the export will fail. For an audit or full-backup use case, use a token owned by a user with unrestricted access across the project's folders.

**Forgetting that `returnFormat` only shapes errors.** Setting `returnFormat=json` does not wrap the file contents in JSON. On success, the response body remains the raw file. `returnFormat` only affects how errors are returned when something goes wrong.

**Using this method to download files from record file-upload fields.** Record-attached files are not in the File Repository — use RC-API-12 (Export File) for those. The two endpoints look superficially similar but pull from different storage areas.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-45 — Create Folder (File Repository) API (create folders that this method's files live in)
- RC-API-46 — List Files and Folders (File Repository) API (discover `doc_id`s for files to export)
- RC-API-12 — Export File (download files from record-level file-upload fields — distinct from File Repository files)
- RC-API-13 — Import File (upload files to record-level file-upload fields)
- RC-API-14 — Delete File (remove files from record-level file-upload fields)
- RC-USER-03 — User Rights: Configuring User Privileges (granting API Export and File Repository privileges)
