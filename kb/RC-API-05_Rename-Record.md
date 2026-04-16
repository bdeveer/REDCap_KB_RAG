RC-API-05

**Rename Record API**

| **Article ID** | RC-API-05 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-02 — Export Records; RC-API-03 — Import Records; RC-API-04 — Delete Records |

---

# 1. Overview

The Rename Record API method allows you to change the record ID of an existing record in a REDCap project. This is useful when you need to update record identifiers programmatically, such as when consolidating projects, renumbering records, or correcting mistaken IDs.

When to use this method: When you need to rename a record ID to a new value, and you want to maintain all the data and structure associated with that record. The method updates the record ID while preserving all associated data.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Edit right. |
| `content` | Required | Always `'record'` for this method. |
| `action` | Required | Always `'rename'` for this method. |
| `record` | Required | The current record ID (the one to be renamed). |
| `new_record_name` | Required | The new record ID to assign. |
| `arm` | Optional | The arm number (for multi-arm projects). If omitted, the first arm is assumed. |
| `returnFormat` | Optional | Response format: `'json'` (default) or `'xml'`. |

---

# 3. Request Examples

## 3.1 Python

```python
#!/usr/bin/env python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'action': 'rename',
    'content': 'record',
    'record': '1',
    'new_record_name': 'record_1',
    'arm': '1',
    'returnFormat': 'json'
}
r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 3.2 R

```r
#!/usr/bin/env Rscript
source('config.R')
library(RCurl)
result <- postForm(
    api_url,
    token=api_token,
    action='rename',
    content='record',
    record='1',
    new_record_name='record_1',
    arm='1',
    returnFormat='json'
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&action=rename&content=record&record=1&new_record_name=record_1&arm=1&returnFormat=json"

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

$data = array(
    'token' => $GLOBALS['api_token'],
    'action' => 'rename',
    'content' => 'record',
    'record' => '1',
    'new_record_name' => 'record_1',
    'arm' => '1',
    'returnFormat' => 'json'
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $GLOBALS['api_url']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data, '', '&'));
$output = curl_exec($ch);
print $output;
?>
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `false` for compatibility. Set it to `true` in production. See RC-API-01 for why SSL certificate validation matters.

---

# 4. Response

The API returns a success message in the requested format. On success, the response typically contains a message confirming the rename operation:

```json
{
  "success": true,
  "message": "Record renamed successfully"
}
```

If an error occurs, the response includes an error message. Common errors include:
- The record ID does not exist
- The new record name already exists
- You lack API Edit permission

---

# 5. Common Questions

**Q: Can I rename a record to a record ID that already exists?**

**A:** No. The new record name must be unique within the project. If you try to rename a record to an ID that already exists, the API returns an error.

**Q: Does renaming a record delete the old record?**

**A:** No. The rename operation changes the ID of the existing record. All associated data, history, and relationships are preserved and moved to the new record ID.

**Q: In a multi-arm project, does the arm parameter matter?**

**A:** Yes, the `arm` parameter specifies which arm's record is being renamed. If you omit it, the API assumes arm 1. You can only rename a record within a single arm.

**Q: Can I rename a record that has already been locked?**

**A:** This depends on your project's locking configuration. If records are locked, you may not be able to rename them. Check your project settings and user permissions.

**Q: What format should the new record name be in?**

**A:** The new record name must be a valid string. It can contain letters, numbers, and special characters, but it must be unique and follow any naming conventions your project enforces. REDCap allows alphanumeric values, underscores, and hyphens.

---

# 6. Common Mistakes & Gotchas

**Using 'record' instead of 'action'.** The `action` parameter must be set to `'rename'`. A common mistake is omitting this parameter or setting it to an incorrect value.

**Forgetting the new_record_name.** The new record ID is a required parameter. If you omit it, the API returns an error.

**Not handling non-existent records.** If you attempt to rename a record that doesn't exist, the API returns an error. Your code must verify that the record exists before attempting to rename it.

**Duplicate new_record_name.** If the new record name already exists in the project, the rename operation fails. Always check for uniqueness first.

**Arm mismatch in multi-arm projects.** In a multi-arm project, specifying the wrong arm number will cause the operation to fail or rename the wrong record. Be explicit about arm assignment.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-02 — Export Records (reading record data)
- RC-API-03 — Import Records (creating and updating records)
- RC-API-04 — Delete Records (removing records)
- RC-DE-01 — Record Creation & the Record Home Page (how record IDs are assigned and what auto-numbering means)
