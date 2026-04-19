RC-API-04

**Delete Records API**

| **Article ID** | RC-API-04 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-02 — Export Records; RC-API-03 — Import Records |

---

# 1. Overview

The Delete Records API method removes records or data from a REDCap project. You can use it to delete entire records, delete specific instruments (forms) for a record, delete data for a specific event in a longitudinal project, or delete data from specific arms in a multi-arm project. Use this method with caution — deletion is permanent and cannot be undone.

When to use this method: When you need to remove records from the project, clean up test data, delete an instrument's data for a record while preserving other data, or manage which records and events are active in the project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires Delete Record user privilege in the project. |
| `content` | Required | Always `'record'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `records` | Required | Array of record names specifying the records to delete. |
| `arm` | Optional | The arm number to delete records from. Only applicable in longitudinal projects with more than one arm. If omitted, specified records are deleted from all arms in which they exist. If provided, records are deleted from that arm only. |
| `instrument` | Optional | The unique instrument name (column B in the Data Dictionary) to delete data for. If specified, only that instrument's data is deleted for the specified records — the record itself is not removed. For longitudinal projects, `event` is mandatory when `instrument` is provided. |
| `event` | Optional | The unique event name — longitudinal projects only. If provided, only data for that event is deleted. If `instrument` is also provided, only that instrument's data for that event is deleted. |
| `repeat_instance` | Optional | The repeating instance number for a repeating instrument or repeating event. If provided, only the data for that specific instance is removed. |
| `delete_logging` | Optional | `'0'` (keep logging) or `'1'` (delete logging). Only available in projects where an administrator has enabled the "Delete a record's logging activity when deleting the record?" setting on Edit Project Settings. When that setting is enabled, the default is `'1'` (logging deleted with the record); pass `'0'` to preserve the log. If the setting is not enabled in the project, this parameter has no effect and defaults to `'0'`. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. |

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 for why SSL certificate validation matters.

---

# 4. Response

On success, the API returns:

- The **number of records deleted** — when no `instrument`, `event`, or `repeat_instance` is specified.
- The **number of items deleted over the total records specified** — when `instrument`, `event`, and/or `repeat_instance` is provided (e.g., partial record deletion).

On error, the API returns an error message describing the problem (e.g., invalid record ID, missing required parameter, insufficient permissions).

---

# 5. Common Questions

**Q: Can I delete only the data in a specific instrument without deleting the entire record?**

**A:** Yes. Specify the `instrument` parameter with the form variable name. This deletes only that instrument's data for the specified records, leaving other instruments untouched.

**Q: In a longitudinal project, can I delete data for only one event?**

**A:** Yes. Specify the `event` parameter with the event name. This deletes data for that event only, leaving other events intact.

**Q: Can I delete multiple records at once?**

**A:** Yes. Pass an array of record IDs in the `records` parameter. For example, `'records[0]'='1'` and `'records[1]'='2'` deletes both records 1 and 2.

**Q: What happens if I specify a record ID that doesn't exist?**

**A:** The API will skip it and continue with other records. No error is returned for non-existent records.

**Q: Can I delete only a specific repeating instance without removing the whole instrument?**

**A:** Yes. Provide the `instrument`, `event` (if longitudinal), and `repeat_instance` parameters together. Only that one instance will be removed; other instances and the record itself remain intact.

**Q: Will the audit log be deleted when I delete a record?**

**A:** By default, no — logging is preserved. However, if an administrator has enabled the "Delete a record's logging activity when deleting the record?" setting on Edit Project Settings, then logging is deleted with the record by default. Pass `delete_logging='0'` to override and keep the log even when that setting is enabled.

**Q: Can I undo a deletion?**

**A:** No. Deletion is permanent. If you need to recover deleted data, you must restore from a backup or re-import the data from another source.

---

# 6. Common Mistakes & Gotchas

**Deleting entire records when you meant to delete one instrument.** Always check whether you want to delete the whole record or just one instrument's data. If you omit the `instrument` parameter, the entire record (all instruments and events) is deleted.

**Forgetting to specify arm in a multi-arm project.** In a multi-arm project, if you specify the `arm` parameter, only records in that arm are deleted. If you omit it, records from all arms matching the record IDs are deleted. Be explicit about which arm you're targeting.

**Assuming deletion respects event filters in longitudinal projects.** If you specify an `event` parameter, deletion is limited to that event. But if you also specify an `instrument`, the instrument data is deleted for that event only. Always be clear about the scope of your deletion.

**Not having the right permissions.** Deleting records requires the **Delete Record** user privilege in the project — this is a separate permission from API Import or API Export. A user can have full API import/export rights but still be blocked from deletions if Delete Record is not granted.

**Event is mandatory when instrument is specified in a longitudinal project.** If you provide `instrument` in a longitudinal project, you must also provide `event`. Omitting `event` in that scenario will result in an API error.

**`delete_logging` behavior depends on an admin-level project setting.** The parameter only has effect when an administrator has enabled the logging deletion setting for the project. If that setting is off, `delete_logging='1'` does nothing — it won't delete logging regardless of what you pass.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-02 — Export Records (reading records)
- RC-API-03 — Import Records (creating and updating records)
- RC-DAG-01 — Data Access Groups (DAG membership controls which records a token can delete)
