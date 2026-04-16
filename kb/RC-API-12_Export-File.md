RC-API-12

**Export File API**

| **Article ID** | RC-API-12 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with file upload fields |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-13 — Import File; RC-API-14 — Delete File |

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
| `event` | Conditional | The unique event name (longitudinal projects only). Required only if the file-upload field is associated with a specific event. |
| `repeat_instance` | Conditional | For projects with repeating instruments or events: the repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default value is `1`. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the returned file content. Defaults to `xml` if omitted. Note: does not apply when using a background process. |

---

# 3. Data Export Rights

Data Export user rights apply to this API request. The following table summarises what happens for each rights level:

| Export Rights Level | File Upload field tagged as Identifier? | Result |
|---|---|---|
| Full Data Set | Either | ✅ Export succeeds |
| De-Identified | No | ✅ Export succeeds |
| De-Identified | Yes | ❌ Export fails with error |
| Remove All Identifier Fields | No | ✅ Export succeeds |
| Remove All Identifier Fields | Yes | ❌ Export fails with error |
| No Access | Either | ❌ Export always fails with error |

To guarantee that the export will not return an error regardless of field tagging, the API token owner must have **Full Data Set** export rights in the project.

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 5. Response

The method returns the raw binary file content (e.g., a PDF, image, Word document) directly. The file should be written to disk using a binary write operation. The HTTP status code will be 200 on success.

**Getting the filename from the response header.** The filename, file extension, and MIME type are not embedded in the response body — they are in the response header. To determine these attributes, parse the `content-type` header of the response. Example:

```
content-type: application/vnd.openxmlformats-officedocument.wordprocessingml.document; name='FILE_NAME.docx'
```

The `returnFormat` parameter controls the format of error messages only and does not affect the returned file content.

---

# 6. Common Questions

**Q: My export returns a file, but when I try to open it, it says the file is corrupted. What went wrong?**

**A:** You likely wrote the file in text mode rather than binary mode. Always use binary write operations (`'wb'` in Python, `writeBin()` in R, `fopen(..., 'wb')` in PHP). Text mode can corrupt binary file formats like images and PDFs.

**Q: Do I need to include the `event` parameter for classic (non-longitudinal) projects?**

**A:** No. For classic projects, omit the `event` parameter entirely. If a file-upload field is not event-specific, the API call will work without it.

**Q: What happens if the field I request is not a file-upload field or does not exist?**

**A:** The API will return an error response, typically with HTTP status 400 or a JSON error message. Check that the field variable name is correct and that the field type in your data dictionary is set to "File" upload.

**Q: Can I export a file that was uploaded to a repeating instrument?**

**A:** Yes. Include the `repeat_instance` parameter with the instance number you want to retrieve. The `field` parameter should still be the variable name of the file-upload field. If you omit `repeat_instance`, the API defaults to instance 1.

---

# 7. Common Mistakes & Gotchas

**Writing to a file in text mode instead of binary mode.** The most common mistake is opening the file for writing in text mode (`'w'` or `'wt'`). This corrupts binary files. Always use binary mode: `'wb'` in Python, `writeBin()` in R, or `fopen($filename, 'wb')` in PHP.

**Forgetting the `event` parameter in longitudinal projects.** In longitudinal projects, if the file-upload field is associated with a specific event, the `event` parameter is required. Omitting it will result in an error. Check your instrument-to-event mapping to confirm which event the field belongs to.

**Assuming the response is JSON.** By default, Export File returns raw binary data, not JSON. Do not attempt to parse the response as JSON unless you explicitly set `returnFormat='json'`. Binary data parsed as JSON will produce garbage.

---

# 8. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-13 — Import File (upload files to file-upload fields)
- RC-API-14 — Delete File (remove files from file-upload fields)
