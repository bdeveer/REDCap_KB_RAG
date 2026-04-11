RC-API-06

**Export Field Names API**

| **Article ID** | RC-API-06 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-02 — Export Records; RC-API-07 — Export Metadata |

---

# 1. Overview

The Export Field Names API method retrieves the internal field names (variable names) for a project. This is the most lightweight way to discover which field names exist in your project without downloading the entire data dictionary. Field names are the unique identifiers used to reference fields in API calls, exports, and analyses.

When to use this method: When you need to query which fields exist in a project, validate field names before making API calls, or generate a list of available variables for documentation or code generation.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'exportFieldNames'` for this method. |
| `format` | Required | Response format: `'json'` (default), `'csv'`, or `'xml'`. |
| `field` | Optional | A single field name to query. If provided, returns information about only that field. If omitted, returns all fields. |
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for production use. Set it to `TRUE` in production. See RC-API-01 for why SSL certificate validation matters.

---

# 4. Response

The method returns a list of field names. When querying a single field (using the `field` parameter), the response includes information about that field. When querying all fields, it returns a JSON array or CSV with all variable names.

**JSON format (all fields):**
```json
[
  {
    "export_field_name": "first_name"
  },
  {
    "export_field_name": "last_name"
  },
  {
    "export_field_name": "age"
  },
  {
    "export_field_name": "record_id"
  }
]
```

**JSON format (single field):**
```json
[
  {
    "export_field_name": "first_name"
  }
]
```

**CSV format:** A simple list with a header row and one field name per row.

---

# 5. Common Questions

**Q: What's the difference between export_field_name and other field identifiers?**

**A:** The `export_field_name` is the internal field name used in API calls, data exports, and calculations. It is the same as the "Variable Name" shown in the Data Dictionary. Other identifiers like field label (the descriptive name shown to users) are different.

**Q: Can I query multiple fields at once?**

**A:** No, the `field` parameter only accepts a single field name. To get information about multiple fields, either omit the parameter to export all fields, or make separate API calls for each field.

**Q: Why would I use this instead of exporting the full data dictionary?**

**A:** This method is lightweight and fast when you only need field names. Exporting the full data dictionary (RC-API-07) returns more information (field labels, validation rules, etc.) but is heavier. Use this method when you only need the list of available fields.

**Q: Does the field parameter perform validation?**

**A:** No, if you query a field name that doesn't exist, the API returns an empty result, not an error. You need to check for empty results in your code.

**Q: Are calculated fields included in the field list?**

**A:** Yes, calculated fields are included in the field list. They appear with their variable names just like regular fields.

---

# 6. Common Mistakes & Gotchas

**Querying non-existent fields silently returns empty results.** Unlike other API methods that return an error, querying a field that doesn't exist returns an empty array or empty CSV. Always validate that your results are not empty.

**Assuming field parameters are case-insensitive.** Field names are case-sensitive in the API. If you query `'First_Name'` but the field is actually `'first_name'`, the query returns empty results.

**Forgetting to specify format.** The `format` parameter controls the output format. Always explicitly set it to `'json'`, `'csv'`, or `'xml'` based on your needs.

**Using the response for data export.** This method returns only field names, not field data. To export actual record data, use RC-API-02 (Export Records).

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-02 — Export Records (reading record data)
- RC-API-07 — Export Metadata (reading the complete data dictionary)
- RC-FD-03 — Data Dictionary (the source of field definitions returned by this method)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (detailed field attribute reference)
