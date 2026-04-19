RC-API-39

**Export Logging API**

| **Article ID** | RC-API-39 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API |

---

# 1. Overview

The Export Logging API retrieves audit trail entries from your project's activity log. Every action in REDCap—data exports, imports, record edits, user logins, and system changes—is logged. This API allows you to programmatically query these logs for compliance audits, user activity tracking, data lineage analysis, and security investigations.

Logging is essential for HIPAA compliance, data governance, and understanding what happened in your project at a specific time.

> **Permissions required:** The API token user must have both **API Export** privileges *and* **Logging** privileges in the project. Having only one of the two will result in an error.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'log'` |
| `format` | Optional | Response format: `'csv'`, `'json'`, `'xml'` (default: `'xml'`) |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, `'xml'`. Defaults to match `format` if omitted. Not applicable when using a background process. |
| `logtype` | Optional | Filter by event type: `'export'`, `'manage'`, `'user'`, `'record'`, `'record_add'`, `'record_edit'`, `'record_delete'`, `'lock_record'`, `'page_view'` (empty string = all types) |
| `user` | Optional | Filter by username (exact match). If not specified, returns events for all users. |
| `record` | Optional | Filter by record name (exact match). Only applicable for record-related events. If not specified, returns events for all records. |
| `dag` | Optional | Filter by DAG `group_id`. If not specified, returns events for all DAGs. |
| `beginTime` | Optional | Return only events logged *after* this date/time. Format: `YYYY-MM-DD HH:MM` (e.g., `2017-01-01 17:00`). Uses server time. If not specified, no begin cutoff is applied. |
| `endTime` | Optional | Return only events logged *before* this date/time. Format: `YYYY-MM-DD HH:MM` (e.g., `2017-01-01 17:00`). Uses server time. If not specified, uses current server time. |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'log',
    'format': 'json',
    'logtype': '',
    'user': '',
    'record': '',
    'beginTime': '2020-10-06 17:37',
    'endTime': '',
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
    content='log',
    format='json',
    logtype='',
    user='',
    record='',
    beginTime='2020-10-06 17:37',
    endTime=''
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=log&format=json&logtype=&user=&record=&beginTime=2020-10-06 17:37&endTime="

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
	'token'     => $GLOBALS['api_token'],
	'content'   => 'log',
	'format'    => 'json',
    'logtype' => '',
    'user' => '',
    'record' => '',
    'beginTime' => '2020-10-06 17:37',
    'endTime' => ''
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 4. Response

The API returns an array of log entries with action details:

```json
[
  {
    "timestamp": "2024-06-15 14:23:45",
    "username": "admin_user",
    "action": "Export records",
    "details": "Exported 150 records in JSON format",
    "pk": "record_id_123",
    "event": "event_1_arm_1",
    "record": "123",
    "data_values": ""
  },
  {
    "timestamp": "2024-06-15 14:20:12",
    "username": "data_coordinator",
    "action": "Create record",
    "details": "Created new record",
    "pk": "record_id_124",
    "event": "",
    "record": "124",
    "data_values": ""
  }
]
```

---

# 5. Common Questions

**Q: What is the time format for beginTime and endTime?**
A: Use `YYYY-MM-DD HH:MM` format (e.g., `2020-10-06 17:37`). All timestamps are in the REDCap server's local time. Omit `endTime` to include all entries up to the current server time.

**Q: Can I export logs for a specific date range?**
A: Yes. Set both `beginTime` and `endTime` to define the range. Timestamp is inclusive on both boundaries.

**Q: Which logtypes are most useful for compliance audits?**
A: `'export'` (data exports), `'record_edit'` (field modifications), `'record_delete'` (deleted records), and `'user'` (user access logs) are typically most relevant for compliance tracking.

**Q: How far back does the audit log go?**
A: REDCap retains logs according to your instance's data retention policy. Contact your administrator if you need historical log data beyond the default retention period.

**Q: Are filtered exports (by user, record, logtype) more efficient than exporting everything?**
A: Yes. Filtering reduces the result set significantly. Always filter on known criteria to improve query performance.

---

# 6. Common Mistakes & Gotchas

**Timestamp format errors:** The correct format for `beginTime` and `endTime` is `YYYY-MM-DD HH:MM` (e.g., `2020-10-06 17:37`). Using other formats such as `M/D/YYYY HH:MM` will cause the filter to fail silently and return unfiltered results.

**Empty filter strings vs. omitted parameters:** An empty string (`''`) for logtype, user, or record means "no filter on that field." Omitting the parameter entirely has the same effect, but always be explicit.

**Assuming local timezone:** Timestamps in logs are stored in the REDCap server's timezone. Verify your server timezone when comparing logs with external events.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-DE-04 — Editing Data & Audit Trail (the audit trail that this method exports programmatically)
