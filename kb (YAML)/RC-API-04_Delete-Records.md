---
id: RC-API-04
title: Delete Records API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.5.6 (Standard) — §2, §4–§6 and the case caveat (delete_logging
  not re-tested) live-tested via the API on a sandbox project (2026-10); LTS line
  last reviewed against the v17.3.7 (LTS) changelog. Delete Records behaviour checked
  against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- RC-API-01 — REDCap API
version: '1.3'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-02
  title: Export Records API
- id: RC-API-03
  title: Import Records API
tags:
- api
synonyms:
- how do i delete records via the api
- delete records api call
- remove records programmatically from redcap
- api method to delete a whole record
- delete data for a specific instrument or event via api
- bulk delete records using the api
- permanently remove record data through the api
- api to clear records in an arm
- delete records api non-existent record error
---

# 1. Overview

The Delete Records API method removes records or data from a REDCap project. You can use it to delete entire records, delete specific instruments (forms) for a record, delete data for a specific event in a longitudinal project, or delete data from specific arms in a multi-arm project. Use this method with caution — deletion is permanent and cannot be undone.

When to use this method: When you need to remove records from the project, clean up test data, delete an instrument's data for a record while preserving other data, or manage which records and events are active in the project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. The token's user needs both the **Delete Records** and the **API Import/Update** user privileges in the project. |
| `content` | Required | Always `'record'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `records` | Required | Array of record names specifying the records to delete, sent as `records[0]=...`, `records[1]=...`. A plain `records=1` string (not an array) is rejected with HTTP 400. |
| `arm` | Optional | The arm number to delete records from. Only applicable in longitudinal projects with more than one arm. If omitted, specified records are deleted from all arms in which they exist. If provided, records are deleted from that arm only. An arm number that doesn't exist returns HTTP 400. |
| `instrument` | Optional | The unique instrument name (column B in the Data Dictionary) to delete data for. If specified, only that instrument's data is deleted for the specified records — the record itself is not removed. For longitudinal projects, `event` is mandatory when `instrument` is provided. |
| `event` | Optional | The unique event name — longitudinal projects only. If provided, only data for that event is deleted. If `instrument` is also provided, only that instrument's data for that event is deleted. |
| `repeat_instance` | Optional | The repeating instance number for a repeating instrument or repeating event. Only applied **together with `event` and/or `instrument`**: with `instrument` (plus `event` if longitudinal) it removes that instance of a repeating instrument; with `event` alone it removes that instance of a repeating event. Sent on its own, it is ignored — see the warning below. |
| `delete_logging` | Optional | `'0'` (keep logging) or `'1'` (delete logging). Only available in projects where an administrator has enabled the "Delete a record's logging activity when deleting the record?" setting on Edit Project Settings. When that setting is enabled, the default is `'1'` (logging deleted with the record); pass `'0'` to preserve the log. If the setting is not enabled in the project, this parameter has no effect and defaults to `'0'`. Applies only to whole-record deletes. The log rows stay, but the logged data values (including logged outgoing emails and text messages) are replaced with `[*DATA REMOVED*]`. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. |

> **Critical — `repeat_instance` on its own deletes the whole record.** If you send `repeat_instance` without `event` or `instrument`, REDCap ignores it and performs a whole-record delete — in every arm, unless `arm` is given. To remove one instance, always include `instrument` (and `event` in a longitudinal project) or, for a repeating event, `event`. Deletion is irreversible: test the exact request on a copy of the project first.

> **Critical — match the stored case of the record name exactly (version caveat, below 16.0.0 Standard).** When deleting a specific instrument's data in a **longitudinal** project, supplying the record name in different case to how it is stored — `taylor-101` where the project holds `TAYLOR-101` — could cause **all data in the entire record to be deleted** rather than just the named instrument's data. Fixed in 16.0.0 (on 17.5.6, `taylor-101` deleted only the named instrument's data of `TAYLOR-101`). Deletion is irreversible, so on any earlier version match the stored case exactly, and test against a copy of the project first.

---

# 3. Request Examples

## 3.1 Python

```python
#!/usr/bin/env python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'action': 'delete',
    'content': 'record',
    'records[0]': '1',
    'arm': '1',
    'instrument': 'demographics',
    'event': 'visit_1_arm_1',
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
    action='delete',
    content='record',
    'records[0]'='1',
    arm='1',
    instrument='demographics',
    event='visit_1_arm_1',
    returnFormat='json'
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=7C3EEBE7B54F68807FF005DD37FE0DFA&action=delete&content=record&records[0]=1&arm=1&instrument=demographics&event=visit_1_arm_1&returnFormat=json"
CURL=`which curl`
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
    'action' => 'delete',
    'content' => 'record',
    'records' => array('1', '2'),
    'arm' => '1',
    'instrument' => 'demographics',
    'event' => 'visit_1_arm_1',
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for why SSL certificate validation matters.

---

# 4. Response

On success, the API returns:

- The **number of records deleted** — when neither `instrument` nor `event` is specified (a whole-record delete).
- For partial deletes (`instrument` and/or `event`, optionally with `repeat_instance`): also a plain number — the count of records whose data was deleted (records without data in that instrument aren't counted).

On error, the API returns an error message describing the problem (e.g., invalid record ID, missing required parameter, insufficient permissions).

The request is **all-or-nothing**: if any record in the batch can't be deleted, nothing is deleted and the API returns HTTP 400. Record access is enforced as in the user interface:

- A user in a Data Access Group gets HTTP 403 for a record outside their DAG, and nothing is deleted. Administrators are not limited by DAGs.
- In a double data entry project, a user designated as data entry person 1 or 2 can only delete their own `--1` or `--2` copies of records.

---

# 5. Common Questions

**Q: Can I delete only the data in a specific instrument without deleting the entire record?**

**A:** Yes. Specify the `instrument` parameter with the form variable name. This deletes only that instrument's data for the specified records, leaving other instruments untouched.

**Q: In a longitudinal project, can I delete data for only one event?**

**A:** Yes. Specify the `event` parameter with the event name. This deletes data for that event only, leaving other events intact.

**Q: Can I delete multiple records at once?**

**A:** Yes. Pass an array of record IDs in the `records` parameter. For example, `'records[0]'='1'` and `'records[1]'='2'` deletes both records 1 and 2.

**Q: What happens if I specify a record ID that doesn't exist?**

**A:** The whole request fails and **nothing is deleted**: HTTP 400 `One or more of the records provided cannot be deleted because they do not exist in the project. The following records do not exist: 999`. Remove unknown IDs from the list (check with Export Records) before deleting.

**Q: Can I delete only a specific repeating instance without removing the whole instrument?**

**A:** Yes. Provide the `instrument`, `event` (if longitudinal), and `repeat_instance` parameters together. Only that one instance will be removed; other instances and the record itself remain intact. For a repeating event, send `event` and `repeat_instance` without `instrument` to remove that event instance. Never send `repeat_instance` without `event` or `instrument`: it is then ignored and the whole record is deleted.

**Q: Will the audit log be deleted when I delete a record?**

**A:** By default, no — logging is preserved. However, if an administrator has enabled the "Delete a record's logging activity when deleting the record?" setting on Edit Project Settings, then logging is deleted with the record by default. Pass `delete_logging='0'` to override and keep the log even when that setting is enabled. "Deleted" here means the log entries remain but their data values are replaced with `[*DATA REMOVED*]`; it only happens on whole-record deletes.

**Q: Can I undo a deletion?**

**A:** No. Deletion is permanent. If you need to recover deleted data, you must restore from a backup or re-import the data from another source.

---

# 6. Common Mistakes & Gotchas

**Deleting entire records when you meant to delete one instrument.** Always check whether you want to delete the whole record or just one instrument's data. If you omit the `instrument` parameter, the entire record (all instruments and events) is deleted.

**Forgetting to specify arm in a multi-arm project.** In a multi-arm project, if you specify the `arm` parameter, only records in that arm are deleted. If you omit it, records from all arms matching the record IDs are deleted. Be explicit about which arm you're targeting.

**Assuming deletion respects event filters in longitudinal projects.** If you specify an `event` parameter, deletion is limited to that event. But if you also specify an `instrument`, the instrument data is deleted for that event only. Always be clear about the scope of your deletion.

**Sending `repeat_instance` on its own.** `repeat_instance` only narrows a delete that already names an `instrument` and/or `event`. On its own it is ignored and the entire record is deleted (across all arms if `arm` is omitted). Test on a copy of the project first.

**Not having the right permissions.** Deleting records via the API requires both the **Delete Records** user privilege and the **API Import/Update** privilege in the project. Delete Records is a separate permission: a user can have full API import/export rights but still be blocked from deletions if Delete Records is not granted.

**Event is mandatory when instrument is specified in a longitudinal project.** If you provide `instrument` in a longitudinal project, you must also provide `event`. Omitting `event` in that scenario will result in an API error.

**`delete_logging` behavior depends on an admin-level project setting.** The parameter only has effect when an administrator has enabled the logging deletion setting for the project. If that setting is off, `delete_logging='1'` does nothing — it won't delete logging regardless of what you pass.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) (reading records)
- [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) (creating and updating records)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG membership controls which records a token can delete)
