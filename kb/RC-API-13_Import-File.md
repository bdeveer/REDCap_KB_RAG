RC-API-13

**Import File API**

| **Article ID** | RC-API-13 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with file upload fields |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-12 — Export File; RC-API-14 — Delete File |

---

# 1. Overview

The Import File API method uploads a file to a file-upload field in REDCap. This method accepts a file from your local system and attaches it to a specific record in a file-upload field. This is useful for automating file uploads from external systems or workflows.

To use this method, you must specify the record, the file-upload field variable name, the actual file to upload, and (for longitudinal projects) the event. The file is sent as multipart form data, not as a JSON string.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import right. |
| `content` | Required | Always `'file'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `record` | Required | The value of the primary key (record ID) for the record to which the file will be uploaded. |
| `field` | Required | The variable name of the file-upload field where the file will be stored. |
| `event` | Conditional | The unique event name (longitudinal projects only). Required only if the file-upload field is associated with a specific event. |
| `file` | Required | The actual file to upload. Sent as a file upload (multipart form data), not as a string. |
| `returnFormat` | Optional | Set to `'json'` to return a JSON response. Default returns text. |

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

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

---

# 6. Common Mistakes & Gotchas

**Sending the file as a string instead of a file upload.** A common error is trying to send the file content as a JSON field or as a base64-encoded string. Import File expects an actual file upload using the multipart form data encoding. Use your HTTP library's file upload mechanism, not a text field.

**Forgetting the `event` parameter in longitudinal projects.** If the file-upload field belongs to a specific event in a longitudinal project, you must include the `event` parameter. Omitting it will result in an error.

**Not closing the file handle after upload.** In languages like Python, always close the file handle after the upload completes to avoid resource leaks. Use a context manager (`with` statement) or explicitly call `close()`.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-12 — Export File (download files from file-upload fields)
- RC-API-14 — Delete File (remove files from file-upload fields)
