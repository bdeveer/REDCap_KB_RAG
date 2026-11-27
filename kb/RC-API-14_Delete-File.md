

**Delete File API**

| **Article ID** | [RC-API-14 — Delete File API](RC-API-14_Delete-File.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with file upload fields |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Delete File behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-12 — Export File API](RC-API-12_Export-File.md); [RC-API-13 — Import File API](RC-API-13_Import-File.md)|
| **Synonyms** | how do i delete a file via the api; delete file api call; remove an uploaded file from a record through the api; api method to clear a file-upload field; delete a signature field file via api; programmatically remove files from redcap; api endpoint to delete a record file; automate file removal with the api |

---

## 1. Overview

The Delete File API method removes a file from a file-upload field in REDCap. This method is useful for automating file removal when records are updated or when files are no longer needed.

This method also works for **Signature fields** (i.e. file-upload fields with the `signature` validation type).

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** REDCap 17.3 and later add an enhanced signature field type. It is deleted through this method exactly like any other file-upload field. On 16.0.x LTS only the classic signature field exists, so check which signature type your project uses before scripting against it.

To use this method, you must specify the record, the file-upload field variable name, and (for longitudinal projects) the event. After deletion, the field will be empty.

**Rights and project status.** The API user needs a valid API token for the project **and** the **Delete Records** user right. An API right on its own is not enough: without Delete Records the call fails with HTTP 403 "You do not have Delete Record privileges", even if the user has API Import/Update. The method works in Development and Production, but is blocked in **Analysis/Cleanup** status (HTTP 403, "...cannot be deleted because the project is in Analysis/Cleanup status"), even when the project's data is still editable in that status.

**Other limits.** The same protections as data entry apply:

| Situation | Result |
|---|---|
| The record, or the instrument holding the field, is locked (including an e-signed instrument) | HTTP 400; the error says the data "could not be saved". Unlock the instrument (and remove the e-signature) first. |
| The user is in a Data Access Group and the record belongs to another DAG (or none) | HTTP 403. Users only reach records in their own DAG. |
| Double Data Entry project and the user is data entry person 1 or 2 | The user can only delete files in their own copy of the record. |
| The record has no data in the given event | Error; the record must exist in that event. |

---

## 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. The token's user needs the **Delete Records** user right (see Section 1). |
| `content` | Required | Always `'file'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `record` | Required | The value of the primary key (record ID) for the record from which the file will be deleted. |
| `field` | Required | The variable name of the file-upload field from which to delete the file. |
| `event` | Conditional | The unique event name. Required for every request in a longitudinal project, and must be a valid event; ignored in classic projects. |
| `repeat_instance` | Conditional | For projects with repeating instruments or events: the repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default value is `1`. |
| `returnFormat` | Optional | `csv`, `json`, or `xml` — specifies the format of **error messages only**. Does not affect the success response. If omitted, REDCap uses the value of `format` if you sent one, otherwise `xml`. |

---

## 3. Request Examples

### 3.1 Python

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

### 3.2 R

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

### 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=file&action=delete&record=f21a3ffd37fc0b3c&field=file_upload&event=event_1_arm_1"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

### 3.4 PHP

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

## 4. Response

On success, the method returns HTTP status **200 with an empty response body**, whatever `returnFormat` you set. Check the status code, not the body. The file is no longer accessible from that field, and the project's Logging shows a "Delete uploaded document (API)" entry naming the field (and instance, for repeating data).

Errors come back as a non-200 status (400 or 403) with a message in the `returnFormat` format. For example, if the field holds no file for that record, event and instance, the response is HTTP 400 "There is no file to delete for this record".

---

## 5. Common Questions

**Q: Can I delete a file without knowing the record ID?**

**A:** No. The `record` parameter is required. You must know the record ID of the record from which you want to delete the file.

**Q: What happens if the field is already empty or the file does not exist?**

**A:** The API returns HTTP 400 "There is no file to delete for this record". The call is not idempotent: a second delete of the same file fails. Nothing is changed, so in a script either treat this specific error as "already empty" or check first with [RC-API-12 — Export File API](RC-API-12_Export-File.md).

**Q: Is there an undo function if I accidentally delete a file?**

**A:** No. The file is permanently deleted. If you need to keep the file, export it (using [RC-API-12 — Export File API](RC-API-12_Export-File.md)) before deleting it. REDCap logs the deletion, but deleted files cannot be undeleted via the API or by users; the server purges the file after a retention period (about 30 days).

**Q: Do I need the `event` parameter for classic projects?**

**A:** No. For classic (non-longitudinal) projects, omit the `event` parameter; it is ignored if sent.

**Q: My token has API Import/Update rights but I get "You do not have Delete Record privileges". Why?**

**A:** Delete File also needs the **Delete Records** user right; API Import/Update alone is not enough. Ask a project user with User Rights access to give the API user Delete Records (or a role that includes it).

**Q: Can I delete a file from a specific instance of a repeating instrument?**

**A:** Yes. Include the `repeat_instance` parameter set to the instance number you want to target. If you omit `repeat_instance`, the API defaults to instance 1. Because deletion is permanent, confirm the correct instance number before calling the method.

---

## 6. Common Mistakes & Gotchas

**Forgetting the `event` parameter in longitudinal projects.** In longitudinal projects the `event` parameter is required on every request and must be a valid unique event name. Omitting it will result in an error.

**Granting only API rights.** API Import/Update alone does not allow file deletion; the API user also needs the **Delete Records** right.

**Treating "no file" as success.** Deleting from an empty field returns HTTP 400, not 200. Scripts that retry or re-run deletions should handle "There is no file to delete for this record" explicitly.

**Running against a project in Analysis/Cleanup.** Deletion is blocked in that status even if data editing is still allowed. Finish file deletions before the status change, or ask your REDCap administrators to return the project to Production.

**Locked or e-signed instruments.** A locked record or instrument, including an e-signed one, makes the call fail with HTTP 400. Unlock it first.

**Assuming the file can be recovered.** Delete File permanently removes the file from REDCap. There is no recycle bin or recovery option via the API. If you need to preserve files, back them up before deletion.

**Attempting to delete a file from a non-file-upload field.** If you specify a field that is not a file-upload field, the API will return an error. Double-check that the `field` parameter points to a file-upload field in your data dictionary.

---

## 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-12 — Export File API](RC-API-12_Export-File.md) (download files from file-upload fields)
- [RC-API-13 — Import File API](RC-API-13_Import-File.md) (upload files to file-upload fields)
