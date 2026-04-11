RC-API-02

**Export Records API**

| **Article ID** | RC-API-02 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-03 — Import Records; RC-API-06 — Export Field Names; RC-API-07 — Export Metadata |

---

# 1. Overview

The Export Records API method retrieves record data from a REDCap project. This is the primary way to programmatically read data that has been entered into your project. The method returns a list of records with the values for all or a subset of fields, instruments, events, and forms. You can export data in JSON, CSV, or XML format, and you can export raw values or user-friendly labels.

When to use this method: When you need to read record data from REDCap in an automated workflow, generate a report, sync data to an external system, or perform analysis on exported data.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'record'` for this method. |
| `format` | Required | Response format: `'json'`, `'csv'`, or `'xml'`. |
| `type` | Optional | Data structure: `'flat'` (default; one row per record) or `'eav'` (entity-attribute-value; one row per field value). Ignored for CSV format. |
| `records` | Optional | Array of record IDs to export. If omitted, all records are exported. |
| `fields` | Optional | Array of field/variable names to export. If omitted, all fields are exported. |
| `forms` | Optional | Array of instrument (form) names to export. If omitted, all forms are exported. |
| `events` | Optional | Array of event names to export. Only applicable in longitudinal projects. If omitted, all events are exported. |
| `rawOrLabel` | Optional | `'raw'` (default) to export raw values, `'label'` to export choice labels and checkbox labels. |
| `rawOrLabelHeaders` | Optional | `'raw'` (default) to show variable names in headers, `'label'` to show field labels. Applicable to CSV format only. |
| `exportDataAccessGroups` | Optional | `true` or `false` (default). If `true`, includes a column for the Data Access Group assignment for each record. |
| `exportSurveyFields` | Optional | `true` or `false` (default). If `true`, includes survey timestamp and survey identifier fields. |
| `returnFormat` | Optional | Response format (alternative to `format` parameter): `'json'`, `'csv'`, or `'xml'`. |

---

# 3. Request Examples

## 3.1 Python

```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'record',
    'format': 'json',
    'type': 'flat'
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
    content='record',
    format='json',
    type='flat'
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=record&format=json&type=flat"

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
	'content' => 'record',
	'format'  => 'json',
	'type'    => 'flat'
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
?>
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 for why SSL certificate validation matters.

---

# 4. Response

The method returns records in the requested format (JSON, CSV, or XML). Each record contains values for the requested fields and events.

**JSON format (flat type):** An array of objects, where each object is one record:
```json
[
  {
    "record_id": "1",
    "first_name": "John",
    "last_name": "Doe",
    "demographics_complete": "2"
  },
  {
    "record_id": "2",
    "first_name": "Jane",
    "last_name": "Smith",
    "demographics_complete": "1"
  }
]
```

**CSV format:** A table with headers and one row per record.

**Flat vs. EAV (Entity-Attribute-Value):** In flat structure, each row is a complete record. In EAV structure, repeating instruments and longitudinal data are represented as multiple rows, one per field value per event per instance.

---

# 5. Common Questions

**Q: How do I export only specific records?**

**A:** Use the `records` parameter and pass an array of record IDs. For example, to export records with IDs 1, 3, and 5, include `'records': ['1', '3', '5']` in your request (or equivalent syntax in your language).

**Q: Can I export only certain fields from each record?**

**A:** Yes. Use the `fields` parameter and pass an array of variable names. For example, `'fields': ['first_name', 'email', 'age']` will export only those three fields plus the record ID.

**Q: What's the difference between raw and label format?**

**A:** Raw format returns the actual values stored in the database — for choice fields, this is the numeric code. Label format returns the text label displayed to users. For example, a sex field might store `1` (raw) but display as `'Male'` (label).

**Q: In a longitudinal project, how do I export a specific event?**

**A:** Use the `events` parameter. For example, `'events': ['visit_1_arm_1', 'visit_2_arm_1']` exports only those events. Omitting `events` exports all events.

**Q: What happens if I request a field that doesn't exist?**

**A:** The field is silently ignored. The API will not return an error; it simply will not include that field in the response.

**Q: Can I export survey metadata like completion timestamps?**

**A:** Yes. Set `exportSurveyFields` to `true`. This adds fields like the survey completion timestamp and survey identifier for records created via survey.

---

# 6. Common Mistakes & Gotchas

**Using the wrong content value.** The `content` parameter must always be `'record'` for this method. A common mistake is using `'records'` (plural) instead of `'record'` (singular), which will result in an API error.

**Not handling empty results.** If you export records with criteria that match no data (e.g., a non-existent record ID), the API returns an empty array or empty CSV, not an error. Your code must check for empty responses.

**Forgetting to set the format.** If you don't specify a `format` parameter, the API may use a default format you didn't expect. Always explicitly set `format` to `'json'`, `'csv'`, or `'xml'` based on what your application requires.

**Mixing up type and format parameters.** The `type` parameter controls data structure (flat vs. eav) and only applies to JSON and XML. The `format` parameter controls the output format (json, csv, xml). These are different parameters for different purposes.

**Exporting label format without understanding encoded values.** When you set `rawOrLabel` to `'label'`, choice fields are converted to their text labels. If your downstream system expects numeric codes, you must decode the labels back to raw values or export in raw format instead.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-03 — Import Records (writing data to REDCap)
- RC-API-04 — Delete Records (removing records)
- RC-API-06 — Export Field Names (get metadata about fields)
- RC-API-07 — Export Metadata (get the data dictionary)
- RC-EXPRT-01 — Data Export: Overview & Workflow (manual export workflows and format options)
- RC-EXPRT-02 — Data Export: Export Formats (format reference for CSV, SPSS, SAS, R, Stata)
- RC-DAG-01 — Data Access Groups (how DAGs filter exported data)
- RC-LONG-02 — Repeated Instruments & Events Setup (repeat instance handling in exports)
