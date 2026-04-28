RC-API-37

**Import Project (Create Project) API**

| **Article ID** | RC-API-37 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap instances (requires Super API Token) |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-34 — Export Project Info; RC-API-36 — Export Project XML |

---

# 1. Overview

The Import Project API creates new projects from scratch or imports a complete project design (including instruments, fields, and events) from exported XML. This method **requires a Super API Token**, not a regular project API token. Super tokens are high-privilege credentials issued to administrators for instance-wide operations.

This API is essential for programmatic project creation workflows, bulk project provisioning, project cloning across instances, and automated project setup pipelines.

When a project is created via this method, REDCap automatically seeds it with defaults identical to creating a new empty project through the UI: a single data collection instrument with a Record ID field and Form Status field, and (for longitudinal projects) one arm with one event. The user who issued the request is automatically added to the new project with full user privileges and receives a project-level API token, which can immediately be used for subsequent project-level API calls.

---

# 2. Key Concepts & Definitions

### Super API Token
A high-privilege administrative credential (64 characters) issued by REDCap administrators for instance-wide operations. Required for project creation; distinct from regular project-level API tokens with limited scope.

### Project Purpose Code
A numeric classification (0-4) indicating the project's intent: Practice, Other, Research, Quality Improvement, or Operational Support. This field is required when creating a project.

### CDISC ODM XML
A standardized XML format (Operational Data Model) containing project metadata and optionally data. Can be provided to import complete project designs from exported projects or external systems.

### Auto-numbered Record ID
A system feature that automatically assigns sequential numeric or alphanumeric identifiers to new records. Can be enabled via the `record_autonumbering_enabled` field.

### Longitudinal Configuration
A project structure supporting multiple time points (events) and study arms. Requires `is_longitudinal: 1` and can include event and arm definitions.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | **Super API Token** (64-character admin token, NOT a regular project token) |
| `content` | Required | Always `'project'` |
| `format` | Optional | Data format: `'json'` (default), `'xml'`, or `'csv'` |
| `data` | Required | Project definition: JSON object or XML with project settings and structure |
| `returnFormat` | Optional | Format for error messages: `csv`, `json`, or `xml`. Defaults to the value of `format` if not specified. Not used when `backgroundProcess=true`. |
| `odm` | Optional | An XML string in CDISC ODM format containing project metadata (fields, forms, events, arms) and optionally record data. When provided, REDCap imports the XML contents into the newly created project — allowing fields, forms, project attributes, events, arms, and records to all be imported in a single API call. The XML can come from a REDCap Project XML export (RC-API-36) or any system that exports in CDISC ODM format. |

**Data Field Options (for new project creation):**

| Field | Type | Required | Description |
|---|---|---|---|
| `project_title` | String | Required | Project name (1–255 characters) |
| `purpose` | Integer | Required | Project purpose: `0` (Practice/just for fun), `1` (Other), `2` (Research), `3` (Quality Improvement), `4` (Operational Support) |
| `purpose_other` | String | Optional | Required text description if `purpose` is `1` (Other) |
| `project_notes` | String | Optional | Additional project notes |
| `is_longitudinal` | Integer | Optional | `0` (classic, default) or `1` (longitudinal) |
| `surveys_enabled` | Integer | Optional | `0` (disabled, default) or `1` (enabled) |
| `record_autonumbering_enabled` | Integer | Optional | `0` (disabled) or `1` (enabled, default) |

---

# 4. Request Examples

## 4.1 Python
```python
#!/usr/bin/env python

from config import config
import requests, json

record = {
    'project_title': 'Project ABC',
    'purpose': 0,
    'purpose_other': '',
    'project_notes': 'Some notes about the project'
}

data = json.dumps(record)

fields = {
    'token': config['api_super_token'],
    'content': 'project',
    'format': 'json',
    'data': data,
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 4.2 R
```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)
library(jsonlite)

record <- c(
	project_title='Project ABC',
	purpose=0,
	purpose_other='',
	project_notes='Some notes about the project'
)

#data <- toJSON(list(as.list(record)), auto_unbox=TRUE)
data <- toJSON(as.list(record), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_super_token,
    content='project',
    format='json',
    data=data
)
print(result)
```

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_SUPER_TOKEN&content=project&format=json&data=[{\"project_title\":\"New%20Project%20via%20API\",\"purpose\":0,\"purpose_other\":\"\",\"project_note\":\"Some%20notes%20about%20the%20project\"}]"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

## 4.4 PHP
```php
<?php

include 'config.php';

$record = array(
	'project_title' => 'New Project via API',
	'purpose'       => 0,
	'purpose_other' => '',
	'project_note'  => 'Some notes about the project',
);

$data = json_encode($record);

/* xml
$data = <<<EOF
<?xml version="1.0" encoding="UTF-8" ?>
<items>
<project>
<project_title><![CDATA[New Project via API]]></project_title>
<purpose>0</purpose>
<purpose_other></purpose_other>
<project_note><![CDATA[Some notes about the project]]></project_note>
</project>
</items>
EOF;
*/

/* csv
$data = <<<EOF
project_title,purpose,purpose_other,project_notes
"Project ABC","",0,"Some notes about the project"
EOF;
*/

$fields = array(
	'token'   => $GLOBALS['super_api_token'],
	'content' => 'project',
	'data'    => $data,
	'format'  => 'json'
	//'format'  => 'xml'
	//'format'  => 'csv'
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

# 5. Response

On success, the API returns the newly created project's API token:

```json
{
  "token": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6"
}
```

On error, you receive an error message:

```json
{
  "error": "Project title is required"
}
```

---

# 6. Common Questions

**Q: What is a Super API Token and where do I get one?**
**A:** A Super API Token is a 64-character administrative credential issued by your REDCap administrator. It grants instance-wide permissions for operations like creating projects. Request it from your REDCap admins through secure channels. Never share it publicly.

**Q: Can I use a regular project API token for this method?**
**A:** No. Regular project tokens are project-specific and have limited scope. Import Project requires a Super API Token with admin-level privileges.

**Q: How do I clone an entire project with all its instruments?**
**A:** (1) Export the source project using RC-API-36 (Export Project XML), (2) Use this API (RC-API-37) to create a new project with the exported XML data.

**Q: What purpose code should I use for my research study?**
**A:** Use `2` for Research. Full mapping: `0` = Practice/just for fun, `1` = Other (requires `purpose_other` text), `2` = Research, `3` = Quality Improvement, `4` = Operational Support.

**Q: Can I create a longitudinal project with arms and events via API?**
**A:** Yes, if you include a complete XML export with arm and event definitions. Use `is_longitudinal: 1` and provide the full XML structure from RC-API-36.

---

# 7. Common Mistakes & Gotchas

**Super token confusion:** Many developers attempt this with regular project tokens and receive authentication errors. Verify you are using a Super API Token, not a project-specific token.

**Missing purpose field:** The `purpose` field is required. Requests without it will fail. Always include `purpose` as an integer (0–4).

**Project title length limits:** Project titles cannot exceed 255 characters. Validation will fail silently if you exceed this length.

**Importing complete XML vs. minimal fields:** To clone a project, provide complete XML from Export Project XML (RC-API-36). To create a simple project quickly, provide only basic fields like `project_title` and `purpose`.

**Default arm/event not removed when you add your own:** When you create a longitudinal project and then immediately call Import Arms or Import Events, the default arm/event created at project creation is still there. Use `override=1` in the Import Arms or Import Events call to replace the defaults entirely rather than appending to them. Failing to do this results in a stale default arm or event alongside your intended structure.

---

# 8. Related Articles

- RC-API-01 — REDCap API
- RC-API-34 — Export Project Info
- RC-API-36 — Export Project XML
