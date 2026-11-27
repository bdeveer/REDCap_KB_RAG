---
id: RC-API-12
title: Export File API
domain: API
applies_to:
- REDCap projects with file upload fields
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured. Export File behaviour checked against source code of v17.6.5 (Standard)
  / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-13
  title: Import File API
- id: RC-API-14
  title: Delete File API
tags:
- api
synonyms:
- how do i download a file via the api
- export file api call
- retrieve an uploaded file from a record through the api
- api method to get a file-upload field attachment
- download signature field file via api
- pull binary file content with the api
- api endpoint to export a record file
- get a file attached to a record programmatically
---

# 1. Overview

The Export File API method retrieves a file that has been uploaded to a file-upload field in REDCap. This method returns the raw file content as a binary file, not JSON or CSV data. The method is useful when you need to download files attached to specific records programmatically from an external system.

This method also works for **Signature fields** (i.e. file-upload fields with the `signature` validation type).

To use this method, you must specify the record, the file-upload field variable name, and (for longitudinal projects) the event. The API returns the actual file bytes, which must be written to a file on disk rather than displayed as text.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'file'` for this method. |
| `action` | Required | Always `'export'` for this method. |
| `record` | Required | The value of the primary key (record ID) for the record from which to export the file. |
| `field` | Required | The variable name of the file-upload field containing the file to export. |
| `event` | Conditional | The unique event name. Required in longitudinal projects: a missing or invalid event returns HTTP 400. Ignored in classic projects. |
| `repeat_instance` | Conditional | For projects with repeating instruments or events: the repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default value is `1`. Ignored (treated as `1`) when the field's instrument or event is not repeating. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the returned file content. Defaults to `xml` if omitted. Note: does not apply when using a background process. |

Export File works in any project status (Development, Production, Analysis/Cleanup). Each download is recorded in the project Logging as "Download file (API)".

---

# 3. Data Export Rights

Data Export user rights apply to this API request. What counts is the token owner's Data Export right for the instrument that contains the file-upload field. The following table summarises what happens for each rights level (a refused export returns HTTP 403):

| Export Rights Level | File Upload field tagged as Identifier? | Result |
|---|---|---|
| Full Data Set | Either | ✅ Export succeeds |
| De-Identified | No | ✅ Export succeeds |
| De-Identified | Yes | ❌ Export fails with error |
| Remove All Identifier Fields | No | ✅ Export succeeds |
| Remove All Identifier Fields | Yes | ❌ Export fails with error |
| No Access | Either | ❌ Export always fails with error |

To guarantee that the export will not return an error regardless of field tagging, the API token owner must have **Full Data Set** export rights for that instrument.

Two other rights settings also block the export with HTTP 403:

- **Data Access Groups:** if the token owner is in a DAG, files on records outside their DAG cannot be exported.
- **Double Data Entry:** users designated as DDE person 1 or 2 cannot use this method.

---

# 4. Request Examples

## 4.1 Python

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'file',
    'action': 'export',
    'record': 'f21a3ffd37fc0b3c',
    'field': 'file_upload',
    'event': 'event_1_arm_1'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))

f = open('/tmp/export.raw.txt', 'wb')
f.write(r.content)
f.close()
```

## 4.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='file',
    action='export',
    record='f21a3ffd37fc0b3c',
    field='file_upload',
    event='event_1_arm_1'
)
print(result)
```

## 4.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=file&action=export&record=f21a3ffd37fc0b3c&field=file_upload&event=event_1_arm_1"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      -o /tmp/file.raw \
      $API_URL
```

## 4.4 PHP

```php
<?php

include 'config.php';

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'file',
	'action'  => 'export',
	'record'  => 'f21a3ffd37fc0b3c',
	'field'   => 'file_upload',
	'event'   => 'event_1_arm_1'
);

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $GLOBALS['api_url']);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($fields, '', '&'));
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

# 5. Response

The method returns the raw binary file content (e.g., a PDF, image, Word document) directly. The file should be written to disk using a binary write operation. The HTTP status code will be 200 on success.

**Getting the filename from the response header.** The filename, file extension, and MIME type are not embedded in the response body — they are in the response header. To determine these attributes, parse the `content-type` header of the response. Example:

```
content-type: application/vnd.openxmlformats-officedocument.wordprocessingml.document; name="FILE_NAME.docx"
```

The filename is in double quotes. There is no `Content-Disposition` header, so libraries or tools that look only there for a filename will not find one; read it from `Content-Type` instead.

The `returnFormat` parameter controls the format of error messages only and does not affect the returned file content.

**Common error responses (HTTP 400)** include: the record does not exist in the given event, the field is not a file-upload field, and "no file to download" when the field is empty for that record, event and instance.

---

# 6. Common Questions

**Q: My export returns a file, but when I try to open it, it says the file is corrupted. What went wrong?**

**A:** You likely wrote the file in text mode rather than binary mode. Always use binary write operations (`'wb'` in Python, `writeBin()` in R, `fopen(..., 'wb')` in PHP). Text mode can corrupt binary file formats like images and PDFs.

**Q: Do I need to include the `event` parameter for classic (non-longitudinal) projects?**

**A:** No. For classic projects, omit the `event` parameter; if you send it, it is ignored. In longitudinal projects it is always required.

**Q: What happens if the field I request is not a file-upload field or does not exist?**

**A:** The API returns HTTP 400 with an error message, formatted according to your `returnFormat` (XML if omitted). Check that the field variable name is correct and that the field type in your data dictionary is set to "File" upload.

**Q: Can I export a file that was uploaded to a repeating instrument?**

**A:** Yes. Include the `repeat_instance` parameter with the instance number you want to retrieve. The `field` parameter should still be the variable name of the file-upload field. If you omit `repeat_instance`, the API defaults to instance 1. If the instrument or event is not repeating, `repeat_instance` is ignored.

**Q: Can I export a file stored in a Signature field using this method?**

**A:** Yes. Export File works for both standard file-upload fields and Signature fields. Use the Signature field's variable name as the `field` parameter. The signature image is returned as a PNG file and should be written to disk in binary mode like any other file download.

---

# 7. Common Mistakes & Gotchas

**Writing to a file in text mode instead of binary mode.** The most common mistake is opening the file for writing in text mode (`'w'` or `'wt'`). This corrupts binary files. Always use binary mode: `'wb'` in Python, `writeBin()` in R, or `fopen($filename, 'wb')` in PHP.

**Forgetting the `event` parameter in longitudinal projects.** In longitudinal projects the `event` parameter is required; omitting it returns HTTP 400. Check your instrument-to-event mapping to confirm which event the field belongs to.

**Assuming the response is JSON.** A successful Export File always returns raw binary data, even if you set `returnFormat='json'`; `returnFormat` only changes how error messages are formatted. Check the HTTP status code first: write the body to disk on 200, and parse it as an error message otherwise.

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-13 — Import File API](RC-API-13_Import-File.md) (upload files to file-upload fields)
- [RC-API-14 — Delete File API](RC-API-14_Delete-File.md) (remove files from file-upload fields)
