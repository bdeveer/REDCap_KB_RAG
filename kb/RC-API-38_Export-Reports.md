RC-API-38

**Export Reports API**

| **Article ID** | RC-API-38 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with custom reports configured |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-02 — Export Records |

---

# 1. Overview

The Export Reports API retrieves data from a custom report created in the REDCap interface. Reports are flexible data filters that allow users to define which records, fields, and events are displayed. This API endpoint exports data exactly as configured in the report's definition, making it ideal for programmatic access to pre-built report views without needing to understand the underlying project structure.

This is particularly useful for recurring report generation, integration with downstream analytics systems, and scheduled data extracts.

> **Data export rights apply to API report exports.** If your account has *No Access* export rights, the request will fail with an error. If you have *De-Identified* or *Remove All Identifier Fields* rights, some fields may be filtered out of the response. To ensure no data is excluded, the API token's user should have *Full Data Set* export rights in the project.

> **The `type` parameter is not supported.** Unlike the Export Records method, Export Reports does not accept a `type` (flat/eav) parameter. All data is always returned in flat format. If you pass `type` in your request, it will be silently ignored.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'report'` |
| `report_id` | Required | Numeric ID of the report (visible in URL or report list) |
| `format` | Required | Response format: `'csv'`, `'json'`, `'xml'` (default), or `'odm'` (CDISC ODM XML v1.3.1) |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, `'xml'`. Defaults to match `format` if not specified. Not used when importing as a background process. |
| `rawOrLabel` | Optional | `'raw'` (default) for raw coded values, `'label'` for display labels |
| `rawOrLabelHeaders` | Optional | For CSV flat format only: `'raw'` (default) for field variable names, `'label'` for field labels in headers |
| `exportCheckboxLabel` | Optional | `'true'` to export checkbox option labels when checked (blank if unchecked); `'false'` (default) exports `'Checked'`/`'Unchecked'`. Only applies when `rawOrLabel=label`. |
| `csvDelimiter` | Optional | CSV delimiter: `','` (default), `'tab'`, `';'`, `'\|'`, or `'^'` |
| `decimalCharacter` | Optional | Force decimal format: `'.'` or `','`. If blank, uses each field's native format. Applies to calc fields and number-validated text fields. |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'report',
    'format': 'json',
    'report_id': '1'
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
    content='report',
    format='json',
    report_id='1'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=report&format=json&report_id=1"

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
	'content'   => 'report',
	'format'    => 'json',
	'report_id' => 1
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

The API returns data rows as configured in the report, ordered first by record (the project's primary key) and then by event ID. Results are always in flat format regardless of project structure.

```json
[
  {
    "record_id": "1",
    "redcap_repeat_instrument": "",
    "redcap_repeat_instance": "",
    "demographics_timestamp": "2024-06-15 14:23:45",
    "first_name": "John",
    "last_name": "Doe",
    "dob": "1985-03-22"
  },
  {
    "record_id": "2",
    "redcap_repeat_instrument": "",
    "redcap_repeat_instance": "",
    "demographics_timestamp": "2024-06-16 09:17:30",
    "first_name": "Jane",
    "last_name": "Smith",
    "dob": "1990-07-08"
  }
]
```

---

# 5. Common Questions

**Q: How do I find my report's ID?**
A: In the REDCap interface, go to "Manage" > "Custom reports." The report ID appears in the URL bar (e.g., `...?pid=123&report_id=1`) or is listed in the report management table.

**Q: What happens if a user doesn't have access to a report?**
A: If the report is restricted to specific users, your API token must belong to a user with permission to view that report. Otherwise, you receive an access denied error.

**Q: Can I export all reports at once?**
A: No. You must call the API separately for each report ID. Loop through your report IDs and call the API for each one.

**Q: Are the results filtered by Data Access Groups (DAGs)?**
A: Yes. If your API token user is restricted to a DAG, the report respects that restriction and only returns records the user can access.

**Q: What is the difference between rawOrLabel and rawOrLabelHeaders?**
A: `rawOrLabel` controls field values (e.g., coded values vs. display text). `rawOrLabelHeaders` controls column headers (e.g., `age` vs. `Age (years)`).

---

# 6. Common Mistakes & Gotchas

**Incorrect report_id format:** Report IDs are numeric. Passing a string like `"my_report"` will fail. Always use the numeric ID from the URL or report list.

**Ignoring report permissions:** Reports respect user-level restrictions, DAG assignments, and role-based access control. Verify your API token user has permission to the report before automating exports.

**Missing parameter defaults:** If you don't specify `rawOrLabel`, the API defaults to `'raw'` (coded values). If you need human-readable labels, explicitly set `rawOrLabel='label'`.

**Assuming `type=flat` is required:** Export Reports always returns flat format. There is no `type` parameter — unlike Export Records, passing `type` here does nothing. Don't copy it from an Export Records call and expect it to have any effect.

**Data export rights silently filter results:** If the API token's user has De-Identified or Remove All Identifier Fields export rights, identifier fields will be stripped from the response without any error or warning. If your export is missing expected fields, check the user's data export rights in User Rights, not the report definition.

**Wrong `format` default assumption:** The default format for Export Reports is `xml`, not `json`. Always pass `format='json'` or `format='csv'` explicitly in your requests if you don't want XML.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-02 — Export Records
- RC-EXPRT-01 — Data Export: Overview & Workflow (manual report export workflow)
- RC-EXPRT-06 — Custom Reports: Setup & Field Selection (how to build the reports exported by this method)
- RC-EXPRT-07 — Custom Reports: Filtering & Ordering (how report filters affect exported data)
- RC-EXPRT-08 — Custom Reports: Management & Organization (report IDs and organization)
