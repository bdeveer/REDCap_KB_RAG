---
id: RC-API-06
title: Export Field Names API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.1'
last_updated: '2026'
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-02
  title: Export Records API
- id: RC-API-07
  title: Export Metadata (Data Dictionary) API
tags:
- api
synonyms:
- how do i export field names via the api
- export field names api call
- get checkbox export field names through the api
- api method to list export import variable names
- find the field___value names for checkboxes via api
- retrieve export-specific field names with the api
- map field names for export and import using api
- api endpoint for field name list
---

# 1. Overview

The Export Field Names API method returns the export/import-specific version of field names for all fields (or a single field) in a project. Its primary purpose is to handle **checkbox fields**, which use a different variable name during exports and imports than the one defined in the Online Designer or Data Dictionary. Each checkbox option is represented as its own export field name in this format: `field_name___coded_value` (field name + triple underscore + the coded value for that choice).

For non-checkbox fields, the export field name is identical to the original field name.

**Note:** The following field types are automatically excluded from the returned list because they cannot be used during data import: `calc`, `file`, and `descriptive`.

When to use this method: When you need to construct correct field name references for checkbox fields during data exports or imports, or when you want a lightweight list of importable field names without pulling the full data dictionary.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'exportFieldNames'` for this method. |
| `format` | Required | Response format: `'csv'`, `'json'`, or `'xml'` [default]. |
| `field` | Optional | A single field's variable name. If provided, returns export field name(s) for that field only. If the field name is invalid, an error is returned. If omitted, all fields are returned. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not specified, or `'xml'` if neither is set. |

---

# 3. Request Examples

## 3.1 Python

```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'exportFieldNames',
    'format': 'json',
    'field': 'first_name'
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
    content='exportFieldNames',
    format='json',
    field='first_name'
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=exportFieldNames&format=json&field=first_name"

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
	'content' => 'exportFieldNames',
	'format'  => 'json',
	'field'   => 'first_name'
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for production use. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for why SSL certificate validation matters.

---

# 4. Response

The method returns a list ordered by field order. Each entry contains three attributes:

| Attribute | Description |
|---|---|
| `original_field_name` | The variable name as defined in the Online Designer / Data Dictionary. |
| `choice_value` | For checkbox fields: the raw coded value for that specific choice. For all other field types: always blank. |
| `export_field_name` | The export/import-specific field name. For checkboxes: `field_name___coded_value`. For all other types: same as `original_field_name`. |

**JSON format — checkbox field example** (`symptoms` field with choices `1`, `2`, `3`):
```json
[
  {
    "original_field_name": "symptoms",
    "choice_value": "1",
    "export_field_name": "symptoms___1"
  },
  {
    "original_field_name": "symptoms",
    "choice_value": "2",
    "export_field_name": "symptoms___2"
  },
  {
    "original_field_name": "symptoms",
    "choice_value": "3",
    "export_field_name": "symptoms___3"
  }
]
```

**JSON format — non-checkbox field example:**
```json
[
  {
    "original_field_name": "first_name",
    "choice_value": "",
    "export_field_name": "first_name"
  }
]
```

**CSV format:** Returns the same three columns (`original_field_name`, `choice_value`, `export_field_name`) with a header row, one row per field/choice combination.

---

# 5. Common Questions

**Q: What's the difference between export_field_name and other field identifiers?**

**A:** The `export_field_name` is the internal field name used in API calls, data exports, and calculations. It is the same as the "Variable Name" shown in the Data Dictionary. Other identifiers like field label (the descriptive name shown to users) are different.

**Q: Can I query multiple fields at once?**

**A:** No, the `field` parameter only accepts a single field name. To get information about multiple fields, either omit the parameter to export all fields, or make separate API calls for each field.

**Q: Why would I use this instead of exporting the full data dictionary?**

**A:** This method is lightweight and fast when you only need field names. Exporting the full data dictionary ([RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)) returns more information (field labels, validation rules, etc.) but is heavier. Use this method when you only need the list of available fields.

**Q: Does the field parameter perform validation?**

**A:** Yes. If you provide a field name that doesn't exist in the project, the API returns an error (not an empty result). Always ensure the field name is valid before calling this method with the `field` parameter.

**Q: Are calculated fields included in the field list?**

**A:** No. The method automatically excludes `calc`, `file`, and `descriptive` field types from the returned list because these fields cannot be used during data import. If you need to see those field names, use Export Metadata ([RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)) instead.

---

# 6. Common Mistakes & Gotchas

**Querying a non-existent field returns an error, not empty results.** If you pass an invalid field name via the `field` parameter, the API returns an error response. Validate field names against the project's data dictionary before calling this method with a specific field.

**Assuming field parameters are case-insensitive.** Field names are case-sensitive in the API. If you query `'First_Name'` but the field is actually `'first_name'`, the query returns empty results.

**Forgetting to specify format.** The `format` parameter controls the output format. Always explicitly set it to `'json'`, `'csv'`, or `'xml'` based on your needs.

**Expecting calc, file, or descriptive fields in the response.** These three field types are automatically excluded from the returned list. If your code relies on finding a calculated field's name here, it won't appear — use Export Metadata ([RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)) if you need those field names.

**Using the response for data export.** This method returns only field names, not field data. To export actual record data, use [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) (Export Records).

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md)(reading record data)
- [RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)(reading the complete data dictionary)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (the source of field definitions returned by this method)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (detailed field attribute reference)
