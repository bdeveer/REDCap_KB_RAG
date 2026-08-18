---
id: RC-API-13
title: Import File API
domain: API
applies_to:
- REDCap projects with file upload fields
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-08
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-12
  title: Export File API
- id: RC-API-14
  title: Delete File API
tags:
- api
synonyms:
- how do i upload a file via the api
- import file api call
- attach a file to a record through the api
- api method to upload to a file-upload field
- send a file as multipart form data via api
- programmatically upload files to redcap
- api endpoint to import a record file
- automate file uploads with the api
---

# 1. Overview

The Import File API method uploads a file to a file-upload field in REDCap. This method accepts a file from your local system and attaches it to a specific record in a file-upload field. This is useful for automating file uploads from external systems or workflows.

This method **cannot** be used for **Signature fields** (i.e. file-upload fields with the `signature` validation type). Signatures can only be captured and stored through the web interface.

To use this method, you must specify the record, the file-upload field variable name, the actual file to upload, and (for longitudinal projects) the event. The file is sent as multipart form data, not as a JSON string.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update right. |
| `content` | Required | Always `'file'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `record` | Required | The value of the primary key (record ID) for the record to which the file will be uploaded. |
| `field` | Required | The variable name of the file-upload field where the file will be stored. |
| `event` | Conditional | The unique event name (longitudinal projects only). Required only if the file-upload field is associated with a specific event. |
| `repeat_instance` | Conditional | For projects with repeating instruments or events: the repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default value is `1`. If the repeating instance does not yet exist, it will be created. **From 17.4.0 the literal value `new` is also accepted** — see below. |

> **Using `repeat_instance=new` (17.4.0+).** Passing the literal string `new` creates a new repeating instance and uploads the file to it, without you having to determine the next instance number first. The same support was added to the developer method `REDCap::addFileToField`.
>
> This removes a race condition as much as a convenience: previously, uploading to a new instance meant querying the current highest instance number and adding one, which two concurrent processes could get wrong and collide on. It also mirrors the `new` value already accepted by the Import Records method — see [RC-API-03 — Import Records API](RC-API-03_Import-Records.md).
>
> On versions below 17.4.0, `new` is not recognised; you must supply an explicit instance number.
| `file` | Required | The actual file to upload. Sent as a file upload (multipart form data), not as a string. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the success response. Defaults to `xml` if omitted. Note: does not apply when using a background process. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests

file = '/tmp/test_file.txt'

fields = {
    'token': config['api_token'],
    'content': 'file',
    'action': 'import',
    'record': 'f21a3ffd37fc0b3c',
    'field': 'file_upload',
    'event': 'event_1_arm_1',
    'returnFormat': 'json'
}

file_obj = open(file, 'rb')
r = requests.post(config['api_url'],data=fields,files={'file':file_obj})
file_obj.close()

print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 3.2 R

```r
source('config.R')
library(RCurl)

file = '/tmp/test_file.txt'

result <- postForm(
    api_url,
    token=api_token,
    content='file',
    action='import',
    record='f21a3ffd37fc0b3c',
    field='file_upload',
    event='event_1_arm_1',
    returnFormat='json',
    file=httr::upload_file(file)
)
print(result)
```

## 3.3 cURL

```sh
. ./config

$CURL -H "Accept: application/json" \
      -F "token=$API_TOKEN" \
      -F "content=file" \
      -F "action=import" \
      -F "record=f21a3ffd37fc0b3c" \
      -F "field=file_upload" \
      -F "event=event_1_arm_1" \
      -F "filename=export.pdf" \
      -F "file=@/tmp/test_file.txt" \
      $API_URL
```

## 3.4 PHP

```php
<?php

include 'config.php';

$file = '/tmp/test_file.txt';
$file = (function_exists('curl_file_create') ? curl_file_create($file, 'text/plain', 'test_file.txt') : "@$file");

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'file',
	'action'  => 'import',
	'record'  => 'f21a3ffd37fc0b3c',
	'field'   => 'file_upload',
	'event'   => 'event_1_arm_1',
	'file'    => $file
);

$fields['returnFormat'] = 'json';

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

# 4. Response

On success, the method returns a success message or JSON response (if `returnFormat='json'` is set). The HTTP status code will be 200.

Example success response (JSON):
```json
{
  "success": true,
  "message": "File uploaded successfully"
}
```

---

# 5. Common Questions

**Q: I'm getting an error about multipart form data. What does that mean?**

**A:** The Import File method requires the file to be sent as multipart form data (a file upload), not as a JSON string or base64-encoded data. Use the file upload features of your HTTP library: `files={'file': file_obj}` in Python's requests, `httr::upload_file()` in R, or `-F "file=@filename"` in cURL.

**Q: Can I upload a file larger than REDCap's file upload limit?**

**A:** No. The API respects the same file size limits as the manual upload interface. If your file exceeds the limit set in Project Setup → Additional Customizations, the upload will fail.

**Q: What happens if I try to upload a file to a non-file-upload field?**

**A:** The API will return an error. Verify that the `field` parameter points to a field with type "File" in your data dictionary.

**Q: Do I need the `event` parameter for classic projects?**

**A:** No. For classic (non-longitudinal) projects, omit the `event` parameter if the file-upload field is not event-specific.

**Q: What happens if a file already exists in the target field? Will it be overwritten?**

**A:** Yes. If a file already exists in the target file-upload field, importing a new file replaces it. The previous file is permanently removed. If you need to preserve the original, export it first using [RC-API-12 — Export File API](RC-API-12_Export-File.md) before importing the replacement.

---

# 6. Common Mistakes & Gotchas

**Sending the file as a string instead of a file upload.** A common error is trying to send the file content as a JSON field or as a base64-encoded string. Import File expects an actual file upload using the multipart form data encoding. Use your HTTP library's file upload mechanism, not a text field.

**Forgetting the `event` parameter in longitudinal projects.** If the file-upload field belongs to a specific event in a longitudinal project, you must include the `event` parameter. Omitting it will result in an error.

**Not closing the file handle after upload.** In languages like Python, always close the file handle after the upload completes to avoid resource leaks. Use a context manager (`with` statement) or explicitly call `close()`.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-12 — Export File API](RC-API-12_Export-File.md)(download files from file-upload fields)
- [RC-API-14 — Delete File API](RC-API-14_Delete-File.md)(remove files from file-upload fields)
