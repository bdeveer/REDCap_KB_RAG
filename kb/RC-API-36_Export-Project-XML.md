RC-API-36

**Export Project XML API**

| **Article ID** | RC-API-36 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-34 — Export Project Info; RC-API-37 — Import Project (Create Project) |

---

# 1. Overview

The Export Project XML API returns the complete project structure as XML, including all instruments, fields, calculated fields, data access group assignments, event definitions, and branching logic. This comprehensive export captures the entire project design and can be used to recreate or clone the project via the Import Project API (RC-API-37).

This method is essential for project backups, migrations between REDCap instances, version control of project designs, and programmatic project cloning workflows.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'project_xml'` |
| `returnFormat` | Optional | Response format: `'json'` (default), `'xml'`, or `'csv'` |
| `returnMetadataOnly` | Optional | `'true'` to return only metadata (field definitions); `'false'` (default) for complete structure |
| `exportSurveyFields` | Optional | `'true'` to include survey-specific fields; `'false'` (default) to omit |
| `exportDataAccessGroups` | Optional | `'true'` to include DAG assignments; `'false'` (default) to omit |
| `filterLogic` | Optional | Branching logic filter to export only matching fields |
| `exportFiles` | Optional | `'true'` to include file attachments; `'false'` (default) to omit |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'project_xml',
    'returnMetadataOnly': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
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
    content='project_xml',
    returnMetadataOnly='false',
    exportSurveyFields='false',
    exportDataAccessGroups='false',
    returnFormat='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=project_xml&returnMetadataOnly=false&exportSurveyFields=false&exportDataAccessGroups=false&returnFormat=json"

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
    'content' => 'project_xml',
    'returnMetadataOnly' => 'false',
    'exportSurveyFields' => 'false',
    'exportDataAccessGroups' => 'false',
    'returnFormat' => 'json'
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

The API returns the full project definition in your chosen format (JSON, XML, or CSV). A typical JSON response contains a data structure with metadata, events, instruments, and field definitions:

```json
{
  "project_id": 123,
  "project_title": "My Research Project",
  "creation_time": "2024-01-15 10:30:45",
  "production_time": "2024-02-01 14:22:18",
  "is_longitudinal": 0,
  "surveys_enabled": 1,
  "metadata": [
    {
      "field_name": "record_id",
      "form_name": "demographics",
      "field_type": "text",
      "field_label": "Record ID",
      ...
    },
    ...
  ]
}
```

---

# 5. Common Questions

**Q: Can I use the exported XML to create a new project?**
A: Yes. Use the Export Project XML API to download your project design, then use RC-API-37 (Import Project / Create Project) with that XML to clone the project.

**Q: What is the difference between `returnMetadataOnly` true and false?**
A: `'true'` returns only field definitions (metadata). `'false'` returns the complete project structure including all instruments, events, and configuration. For cloning, use `'false'`.

**Q: Will my exported XML include data records?**
A: No. Export Project XML returns only the project design structure, not the data. Use RC-API-02 (Export Records) to export data separately.

**Q: How large can the exported XML be?**
A: Export size depends on project complexity (number of instruments, fields, branching logic). REDCap has default upload/download limits; consult your instance settings if you encounter size errors.

**Q: Can I export only specific instruments?**
A: Not directly. Use `filterLogic` to filter fields by branching logic conditions, but to export specific instruments you would need to manually construct the XML or export the entire project and parse it.

---

# 6. Common Mistakes & Gotchas

**Large exports timing out:** Projects with hundreds of instruments and thousands of fields may exceed request timeout limits. Consider exporting metadata only first with `returnMetadataOnly='true'`.

**Format parameter mismatches:** The parameter is `returnFormat`, not `format`. Using `format` alone will not control the output format and may default unexpectedly.

**Incomplete exports without all flags:** If you need data access groups, survey fields, or other settings included in your cloned project, explicitly set those optional parameters to `'true'` before exporting.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-34 — Export Project Info
- RC-API-37 — Import Project (Create Project)
- RC-FD-01 — Form Design Overview (instrument structure captured in the project XML)
- RC-FD-03 — Data Dictionary (the metadata embedded in the exported XML)
