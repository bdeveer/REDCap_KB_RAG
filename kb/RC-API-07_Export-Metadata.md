RC-API-07

**Export Metadata (Data Dictionary) API**

| **Article ID** | RC-API-07 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-06 — Export Field Names; RC-API-08 — Import Metadata |

---

# 1. Overview

The Export Metadata API method retrieves the complete data dictionary (metadata) for a REDCap project. The data dictionary defines the structure of your project — all fields, instruments, field types, validation rules, branching logic, and other configuration details. This is the most comprehensive way to programmatically understand your project's structure.

When to use this method: When you need to understand the complete structure of a project, document the data dictionary, migrate a project, validate field configurations, or programmatically access field labels, validation rules, and other metadata attributes.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'metadata'` for this method. |
| `format` | Required | Response format: `'json'` (default), `'csv'`, or `'xml'`. |
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
    'content': 'metadata',
    'format': 'json'
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
    content='metadata',
    format='json'
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=metadata&format=json"

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
	'content' => 'metadata',
	'format'  => 'json'
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

The method returns the complete data dictionary in the requested format. Each row represents one field definition. The response includes all Data Dictionary columns such as field name, form name, field type, field label, validation rules, branching logic, and more.

**JSON format (excerpt):**
```json
[
  {
    "field_name": "record_id",
    "form_name": "demographics",
    "section_header": "",
    "field_type": "text",
    "field_label": "Record ID",
    "select_choices_or_calculations": "",
    "field_note": "",
    "text_validation_type_or_show_slider_number": "",
    "text_validation_min": "",
    "text_validation_max": "",
    "identifier": "y",
    "branching_logic": "",
    "required_field": "y",
    "custom_alignment": "",
    "question_number": "",
    "matrix_group_name": "",
    "matrix_ranking": "",
    "field_annotation": ""
  },
  {
    "field_name": "first_name",
    "form_name": "demographics",
    "section_header": "",
    "field_type": "text",
    "field_label": "First Name",
    "select_choices_or_calculations": "",
    "field_note": "",
    "text_validation_type_or_show_slider_number": "",
    "text_validation_min": "",
    "text_validation_max": "",
    "identifier": "",
    "branching_logic": "",
    "required_field": "",
    "custom_alignment": "",
    "question_number": "",
    "matrix_group_name": "",
    "matrix_ranking": "",
    "field_annotation": ""
  }
]
```

**CSV format:** The response is the raw data dictionary CSV with all standard columns.

---

# 5. Common Questions

**Q: What's included in the metadata response?**

**A:** The response includes all columns from the Data Dictionary: field_name, form_name, section_header, field_type, field_label, select_choices_or_calculations, field_note, text_validation rules, identifier, branching_logic, required_field, custom_alignment, question_number, matrix settings, and field_annotation.

**Q: Can I export metadata for only certain instruments?**

**A:** No, this method exports the entire data dictionary. If you only need specific instruments, you can filter the response in your code after receiving it.

**Q: What format is best for metadata export?**

**A:** JSON is easiest to parse programmatically and preserves structure. CSV is the native REDCap format and can be imported back (see RC-API-08). XML works but is more verbose.

**Q: Does the metadata include calculated fields and matrices?**

**A:** Yes, all field types are included: text, choice, calculated, checkbox, radio, matrix, file upload, and custom fields. All field properties are returned.

**Q: Can I use this to audit project structure changes?**

**A:** Yes. By periodically exporting metadata and comparing versions, you can track when fields, forms, or validation rules change. This is useful for data governance and compliance auditing.

**Q: Does the metadata include project-level settings?**

**A:** No. This method returns only field and instrument definitions. To get project settings (title, purpose, etc.), use other metadata endpoints. See RC-API-01 for additional project-level API methods.

---

# 6. Common Mistakes & Gotchas

**Assuming metadata is lightweight.** For large projects with hundreds of fields and instruments, the metadata response can be large (megabytes). Plan accordingly in your code, especially for network-constrained environments.

**Not properly handling the JSON structure.** The JSON response is an array of objects, not a single object. Each field is a separate object in the array. Always iterate through the array.

**Missing field properties.** Some optional field properties may be empty strings in the response. Don't assume all fields have values for all columns. Use defensive programming to check for empty values.

**Forgetting to update on project changes.** Metadata is static at the time you request it. If fields are added or modified after you export, your local copy is outdated. If you need fresh data, re-export.

**Using metadata for data validation without refreshing.** If you use exported metadata to validate incoming data (e.g., checking which fields are required), be aware that project structure may change. Refresh metadata periodically in production systems.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-06 — Export Field Names (get a lightweight list of field names only)
- RC-API-08 — Import Metadata (create or update the data dictionary)
- RC-FD-02 — Online Designer (the GUI for building the data dictionary)
- RC-FD-03 — Data Dictionary (the full data dictionary format exported by this method)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (detailed column reference)
