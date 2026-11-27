

**Export Reports API**

| **Article ID** | [RC-API-38 — Export Reports API](RC-API-38_Export-Reports.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with custom reports configured |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — export rights, required rights, report access, DAG filtering, record ID hashing and `csvDelimiter` handling checked against source code; §1, §3, §5–§7 (report created for the test) live-tested via the API on a sandbox project on v17.5.6 (2026-10); pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.4 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-02 — Export Records API](RC-API-02_Export-Records.md)|
| **Synonyms** | export reports api method; how do i pull a report via the api; api call to export data from a custom report; get report data by report id through the api; export redcap report results using the api; api method to retrieve a saved report; download custom report output via api; programmatically extract a report with the api; export report csv tab delimiter error |

---

## 1. Overview

The Export Reports API retrieves data from a custom report created in the REDCap interface. Reports are flexible data filters that allow users to define which records, fields, and events are displayed. This API endpoint exports data exactly as configured in the report's definition, making it ideal for programmatic access to pre-built report views without needing to understand the underlying project structure.

This is particularly useful for recurring report generation, integration with downstream analytics systems, and scheduled data extracts.

> **Rights required.** The API token's user needs the **API Export** right; without it the request fails with HTTP 403. Users in a Double Data Entry project who are assigned as data entry person 1 or 2 cannot use this method.

> **Data export rights apply to API report exports.** Export rights are set per instrument. If your account has *No Access* export rights, the request fails with HTTP 403 and a message saying you have "No Access" data export rights. If you have *De-Identified* or *Remove All Identifier Fields* rights, some fields are filtered out of the response (see Data Export Rights in Section 2). To ensure no data is excluded, the API token's user should have *Full Data Set* export rights on every instrument in the report.

> **The `type` parameter is not supported.** Unlike the Export Records method, Export Reports does not accept a `type` (flat/eav) parameter. All data is always returned in flat format. If you pass `type` in your request, it will be silently ignored.

---

## 2. Key Concepts & Definitions

#### Custom Report
A user-defined view of project data created in the REDCap interface that filters records, fields, and events according to specified criteria. Each report has a unique numeric ID.

#### Report ID
The numeric identifier of a custom report, visible in the URL or report management table. Required to export a specific report via API.

#### Data Export Rights
User permissions, set per instrument, that control which fields an export includes. These rights are enforced on API exports:

| Level | Effect on the report export |
|---|---|
| Full Data Set | No restrictions |
| Remove All Identifier Fields | Removes only fields tagged as identifiers |
| De-Identified | The stricter level: removes identifier-tagged fields **and** unvalidated free-text fields, notes fields and date/datetime fields |
| No Access | Blocks the export (HTTP 403) |

If the record ID field is tagged as an identifier and the user's export right is anything other than Full Data Set, record IDs are exported hashed rather than as the real values.

#### Flat Format
The standard tabular data structure (one row per record/event) with columns for each field. All data exported via the Export Reports API is in flat format regardless of the project structure.

#### rawOrLabel Parameter
Determines whether exported values are raw coded values (e.g., `'1'`, `'0'`) or human-readable labels (e.g., `'Yes'`, `'No'`). Applies to field values, not column headers.

#### CSV Delimiter
The character used to separate fields in CSV output. Options include comma (default), tab, semicolon, pipe, or caret, allowing flexibility for downstream systems.

---

## 3. Parameters

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
| `csvDelimiter` | Optional | CSV delimiter: `','` (default), `'tab'`, `';'`, `'\|'`, or `'^'`. See the version caveat below for `'tab'` on older versions. |
| `decimalCharacter` | Optional | Force decimal format: `'.'` or `','`. If blank, uses each field's native format. Applies to calc fields and number-validated text fields. |

> **Version caveat (below 17.5.7 Standard / 17.3.21 LTS, including all 16.x LTS):** `csvDelimiter=tab` makes CSV **exports** fail with HTTP 400 and an HTML error page instead of data. On these versions, send a literal tab character instead (URL-encoded `%09`) or use another delimiter. Fixed in 17.5.7 Standard / 17.3.21 LTS; present in 17.3.31 LTS and 17.6, not in 16.0.61 LTS.

---

## 4. Request Examples

### 4.1 Python
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

### 4.2 R
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

### 4.3 cURL
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

### 4.4 PHP
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) Section 3.5.

---

## 5. Response

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

## 6. Common Questions

**Q: How do I find my report's ID?**
**A:** In the REDCap interface, go to "Manage" > "Custom reports." The report ID appears in the URL bar (e.g., `...?pid=123&report_id=1`) or is listed in the report management table.

**Q: What happens if a user doesn't have access to a report?**
**A:** If the report's "who can view" setting excludes the API token's user, the request fails with HTTP 403 and a message that you do not have access to the report. Users with the **Add/Edit Reports** right, and administrators, can export any report in the project regardless of that setting.

**Q: Can I export all reports at once?**
**A:** No. You must call the API separately for each report ID. Loop through your report IDs and call the API for each one.

**Q: Are the results filtered by Data Access Groups (DAGs)?**
**A:** Yes. If your API token user is restricted to a DAG, the report respects that restriction and only returns records the user can access.

**Q: What is the difference between rawOrLabel and rawOrLabelHeaders?**
**A:** `rawOrLabel` controls field values (e.g., coded values vs. display text). `rawOrLabelHeaders` controls column headers (e.g., `age` vs. `Age (years)`).

---

## 7. Common Mistakes & Gotchas

**`csvDelimiter=tab` fails on older versions:** Below 17.5.7 Standard / 17.3.21 LTS (including 16.x LTS), `'tab'` makes CSV **exports** fail with HTTP 400 and an HTML page. Send a literal tab character instead (URL-encoded `%09`) or use another delimiter. Fixed in 17.5.7 Standard / 17.3.21 LTS.

**Incorrect report_id format:** Report IDs are numeric. Passing a string like `"my_report"`, or the ID of a report in a different project, fails with HTTP 403 and a message that the report does not belong to this project. Always use the numeric ID from the URL or report list of the same project the token belongs to.

**Ignoring report permissions:** Reports respect the report's "who can view" setting, DAG assignments, and export rights. Verify your API token user can view the report before automating exports. Users with the **Add/Edit Reports** right, and administrators, can export any report in the project regardless of its "who can view" setting.

**Missing parameter defaults:** If you don't specify `rawOrLabel`, the API defaults to `'raw'` (coded values). If you need human-readable labels, explicitly set `rawOrLabel='label'`.

**Assuming `type=flat` is required:** Export Reports always returns flat format. There is no `type` parameter — unlike Export Records, passing `type` here does nothing. Don't copy it from an Export Records call and expect it to have any effect.

**Data export rights silently filter results:** If the API token's user has Remove All Identifier Fields export rights on an instrument, identifier-tagged fields are stripped from the response without any error or warning. De-Identified is stricter: it also strips unvalidated free-text fields, notes fields and date/datetime fields. If the record ID field is tagged as an identifier, record IDs come back hashed for any right other than Full Data Set. If your export is missing expected fields or shows unfamiliar record IDs, check the user's per-instrument data export rights in User Rights, not the report definition.

**Wrong `format` default assumption:** The default format for Export Reports is `xml`, not `json`. Always pass `format='json'` or `format='csv'` explicitly in your requests if you don't want XML.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (manual report export workflow)
- [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) (how to build the reports exported by this method)
- [RC-EXPRT-07 — Custom Reports: Filtering & Ordering](RC-EXPRT-07_Custom-Reports-Filtering-and-Ordering.md) (how report filters affect exported data)
- [RC-EXPRT-08 — Custom Reports: Management & Organization](RC-EXPRT-08_Custom-Reports-Management-and-Organization.md) (report IDs and organization)
