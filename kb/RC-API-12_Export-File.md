RC-API-12

**Export File API**

| **Article ID** | RC-API-12 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with file upload fields |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-13 — Import File; RC-API-14 — Delete File |

---

# 1. Overview

The Export File API method retrieves a file that has been uploaded to a file-upload field in REDCap. This method returns the raw file content as a binary file, not JSON or CSV data. The method is useful when you need to download files attached to specific records programmatically from an external system.

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
| `returnFormat` | Optional | Set to `'json'` to return a JSON response with file metadata instead of raw file bytes. Default returns raw binary file. |

---

# 3. Request Examples

## 3.1 Python

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

## 3.2 R

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

## 3.3 cURL

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

## 3.4 PHP

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

# 4. Response

The method returns the raw binary file content (e.g., a PDF, image, Word document) directly. The file should be written to disk using a binary write operation. The HTTP status code will be 200 on success.

If you set `returnFormat='json'`, the response will be JSON containing file metadata instead of the raw file bytes.

---

# 5. Common Questions

**Q: My export returns a file, but when I try to open it, it says the file is corrupted. What went wrong?**

**A:** You likely wrote the file in text mode rather than binary mode. Always use binary write operations (`'wb'` in Python, `writeBin()` in R, `fopen(..., 'wb')` in PHP). Text mode can corrupt binary file formats like images and PDFs.

**Q: Do I need to include the `event` parameter for classic (non-longitudinal) projects?**

**A:** No. For classic projects, omit the `event` parameter entirely. If a file-upload field is not event-specific, the API call will work without it.

**Q: What happens if the field I request is not a file-upload field or does not exist?**

**A:** The API will return an error response, typically with HTTP status 400 or a JSON error message. Check that the field variable name is correct and that the field type in your data dictionary is set to "File" upload.

**Q: Can I export a file that was uploaded to a repeating instrument?**

**A:** Yes. For repeating instruments, include the `field` parameter as the instrument name (not the repeat instance), and the API will retrieve the file from the specified record and event.

---

# 6. Common Mistakes & Gotchas

**Writing to a file in text mode instead of binary mode.** The most common mistake is opening the file for writing in text mode (`'w'` or `'wt'`). This corrupts binary files. Always use binary mode: `'wb'` in Python, `writeBin()` in R, or `fopen($filename, 'wb')` in PHP.

**Forgetting the `event` parameter in longitudinal projects.** In longitudinal projects, if the file-upload field is associated with a specific event, the `event` parameter is required. Omitting it will result in an error. Check your instrument-to-event mapping to confirm which event the field belongs to.

**Assuming the response is JSON.** By default, Export File returns raw binary data, not JSON. Do not attempt to parse the response as JSON unless you explicitly set `returnFormat='json'`. Binary data parsed as JSON will produce garbage.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-13 — Import File (upload files to file-upload fields)
- RC-API-14 — Delete File (remove files from file-upload fields)
