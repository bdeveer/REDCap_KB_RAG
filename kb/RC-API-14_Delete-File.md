RC-API-14

**Delete File API**

| Article ID | RC-API-14 |
|---|---|
| Domain | API |
| Applies To | REDCap projects with file upload fields |
| Prerequisite | RC-API-01 — REDCap API |
| Version | 1.1 |
| Last Updated | 2026 |
| Author | See KB-SOURCE-ATTESTATION.md |
| Source | REDCap API v16.1.3 official documentation examples |
| Related Topics | RC-API-01 — REDCap API; RC-API-12 — Export File; RC-API-13 — Import File |

---

# 1. Overview

The Delete File API method removes a file from a file-upload field in REDCap. This method is useful for automating file removal when records are updated or when files are no longer needed.

This method also works for **Signature fields** (i.e. file-upload fields with the `signature` validation type).

To use this method, you must specify the record, the file-upload field variable name, and (for longitudinal projects) the event. After deletion, the field will be empty.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update right. |
| `content` | Required | Always `'file'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `record` | Required | The value of the primary key (record ID) for the record from which the file will be deleted. |
| `field` | Required | The variable name of the file-upload field from which to delete the file. |
| `event` | Conditional | The unique event name (longitudinal projects only). Required only if the file-upload field is associated with a specific event. |
| `repeat_instance` | Conditional | For projects with repeating instruments or events: the repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default value is `1`. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the success response. Defaults to `xml` if omitted. Note: does not apply when using a background process. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'file',
    'action': 'delete',
    'record': 'f21a3ffd37fc0b3c',
    'field': 'file_upload',
    'event': 'event_1_arm_1',
}

fields['returnFormat'] = 'json'

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 3.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='file',
    action='delete',
    record='f21a3ffd37fc0b3c',
    field='file_upload',
    event='event_1_arm_1'
)
print(result)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=file&action=delete&record=f21a3ffd37fc0b3c&field=file_upload&event=event_1_arm_1"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

## 3.4 PHP

```php
<?php

include 'config.php';

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'file',
	'action'  => 'delete',
	'record'  => 'f21a3ffd37fc0b3c',
	'field'   => 'file_upload',
	'event'   => 'event_1_arm_1',
);

$fields['returnFormat'] = 'json';

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

On success, the method returns a success message or JSON response (if `returnFormat='json'` is set). The HTTP status code will be 200. The file will no longer be accessible from that field.

Example success response (JSON):
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

---

# 5. Common Questions

**Q: Can I delete a file without knowing the record ID?**

**A:** No. The `record` parameter is required. You must know the record ID of the record from which you want to delete the file.

**Q: What happens if the field is already empty or the file does not exist?**

**A:** Depending on your REDCap version, the API may return success or an error. It is safe to attempt deletion on an empty field; the operation is idempotent.

**Q: Is there an undo function if I accidentally delete a file?**

**A:** No. The file is permanently deleted. If you need to keep the file, export it (using RC-API-12) before deleting it. REDCap maintains an audit trail, but deleted files cannot be undeleted via the API.

**Q: Do I need the `event` parameter for classic projects?**

**A:** No. For classic (non-longitudinal) projects, omit the `event` parameter if the file-upload field is not event-specific.

**Q: Can I delete a file from a specific instance of a repeating instrument?**

**A:** Yes. Include the `repeat_instance` parameter set to the instance number you want to target. If you omit `repeat_instance`, the API defaults to instance 1. Because deletion is permanent, confirm the correct instance number before calling the method.

---

# 6. Common Mistakes & Gotchas

**Forgetting the `event` parameter in longitudinal projects.** For longitudinal projects, if the file-upload field belongs to a specific event, the `event` parameter is required. Omitting it will result in an error.

**Assuming the file can be recovered.** Delete File permanently removes the file from REDCap. There is no recycle bin or recovery option via the API. If you need to preserve files, back them up before deletion.

**Attempting to delete a file from a non-file-upload field.** If you specify a field that is not a file-upload field, the API will return an error. Double-check that the `field` parameter points to a file-upload field in your data dictionary.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-12 — Export File (download files from file-upload fields)
- RC-API-13 — Import File (upload files to file-upload fields)
