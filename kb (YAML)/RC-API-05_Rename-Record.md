---
id: RC-API-05
title: Rename Record API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.5.6 (Standard) — §2, §4–§6 live-tested via the API on
  a sandbox project (2026-10); LTS line last reviewed against the v17.3.7 (LTS) changelog
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-10
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-02
  title: Export Records API
- id: RC-API-03
  title: Import Records API
- id: RC-API-04
  title: Delete Records API
tags:
- api
synonyms:
- how do i rename a record via the api
- rename record api call
- change a record id programmatically
- api method to update a record identifier
- renumber records using the api
- correct a mistaken record id with the api
- change primary key value of a record via api
- api endpoint to rename a record id
- rename record api returns 200 on error
---

# 1. Overview

The Rename Record API method allows you to change the record ID of an existing record in a REDCap project. This is useful when you need to update record identifiers programmatically, such as when consolidating projects, renumbering records, or correcting mistaken IDs.

When to use this method: When you need to rename a record ID to a new value, and you want to maintain all the data and structure associated with that record. The method updates the record ID while preserving all associated data.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires **Rename Record** user privilege in the project. |
| `content` | Required | Always `'record'` for this method. |
| `action` | Required | Always `'rename'` for this method. |
| `record` | Required | The current record ID (the one to be renamed). |
| `new_record_name` | Required | The new record ID to assign. |
| `arm` | Optional | The arm number (for multi-arm projects). If omitted, all records with the same name across all arms are renamed to the new record name. If specified, only the record in that arm is renamed. |
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `false` for compatibility. Set it to `true` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for why SSL certificate validation matters.

---

# 4. Response

On success, the API returns `1`. Most failures are **also HTTP 200**, with a plain-text message instead of `1` (not a JSON error, whatever `returnFormat` says):

| Case | Response body (HTTP 200) |
|---|---|
| New name already exists | `Study ID "1" could not be changed to "2" because that record already exists! Please try again.` |
| Record doesn't exist | `Current Record does not exists.` |
| `new_record_name` missing | `New record name must be provided.` |

A missing Rename Record privilege is a real error (non-200). Check that the body is exactly `1`.

---

# 5. Common Questions

**Q: Can I rename a record to a record ID that already exists?**

**A:** No. The new record name must be unique within the project. If you try to rename a record to an ID that already exists, the API returns an error.

**Q: Does renaming a record delete the old record?**

**A:** No. The rename operation changes the ID of the existing record. All associated data, history, and relationships are preserved and moved to the new record ID.

**Q: In a multi-arm project, does the arm parameter matter?**

**A:** Yes. If you specify an arm number, only the record in that arm is renamed. If you omit the `arm` parameter, REDCap renames all records with the matching name across every arm the record exists in.

**Q: Can I rename a record that has already been locked?**

**A:** This depends on your project's locking configuration. If records are locked, you may not be able to rename them. Check your project settings and user permissions.

**Q: What format should the new record name be in?**

**A:** Any unique string. The API doesn't restrict the characters: renaming to `a b` (space) and `x.y` (dot) both succeeded on 17.5.6. Stick to letters, numbers, underscores and hyphens anyway — spaces and dots cause trouble in URLs, file names and piping.

---

# 6. Common Mistakes & Gotchas

**Using 'record' instead of 'action'.** The `action` parameter must be set to `'rename'`. A common mistake is omitting this parameter or setting it to an incorrect value.

**Forgetting the new_record_name.** The new record ID is a required parameter. If you omit it, the API returns an error.

**Checking the status code instead of the body.** Renaming a record that doesn't exist, renaming to a name that's taken, or leaving out `new_record_name` all return HTTP 200 with an explanatory message. Treat anything other than a body of `1` as a failure.

**Not handling non-existent records.** If you attempt to rename a record that doesn't exist, the API returns a message instead of `1`. Your code must verify that the record exists before attempting to rename it.

**Duplicate new_record_name.** If the new record name already exists in the project, the rename operation fails. Always check for uniqueness first.

**Arm mismatch in multi-arm projects.** In a multi-arm project, specifying the wrong arm number will cause the operation to fail or rename the wrong record. Be explicit about arm assignment.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) (reading record data)
- [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) (creating and updating records)
- [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md) (removing records)
- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) (how record IDs are assigned and what auto-numbering means)
