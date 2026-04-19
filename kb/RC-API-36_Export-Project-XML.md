RC-API-36

**Export Project XML API**

| **Article ID** | RC-API-36 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-34 — Export Project Info; RC-API-37 — Import Project (Create Project) |

---

# 1. Overview

The Export Project XML API exports the entire project — all records, events, arms, instruments, fields, and project attributes — as a single XML file in **CDISC ODM format (ODM version 1.3.1)**. This XML can be used to clone the project on the same REDCap server or another REDCap server (by uploading it on the Create New Project page), or to import it into any other ODM-compatible system.

By default, the export includes both metadata and data. Setting `returnMetadataOnly=true` returns only the project structure without any records.

**Important — data export rights apply:** When `returnMetadataOnly` is `false` (the default), your Data Export user rights are enforced. If you have De-Identified or Remove All Identifier Fields export rights, some fields may be stripped from the returned data. Use Full Data Set export rights to ensure no data is filtered out.

This method requires only the API Export right.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'project_xml'` |
| `returnMetadataOnly` | Optional | `'true'` returns only metadata (all fields, forms, events, arms); `'false'` (default) returns metadata and data |
| `records` | Optional | Array of record names to pull; by default all records are returned |
| `fields` | Optional | Array of field names to pull; by default all fields are returned |
| `events` | Optional | Array of unique event names to pull records for (longitudinal projects only) |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`). The response itself is always CDISC ODM XML. |
| `exportSurveyFields` | Optional | `'true'` to include survey identifier and timestamp fields; `'false'` (default) to omit. Note: if imported via API, these pseudo-fields are ignored. |
| `exportDataAccessGroups` | Optional | `'true'` to include the `redcap_data_access_group` field; `'false'` (default) to omit. Only applies when the API user is **not** in a data access group — if the user is in a DAG, this flag is ignored and reverts to `'false'`. |
| `filterLogic` | Optional | Logic string (e.g., `[age] > 30`) to filter which records are returned. Only records where the logic evaluates as TRUE are included. Invalid syntax returns an error. |
| `exportFiles` | Optional | `'true'` to embed uploaded File Upload and Signature field files in the XML; `'false'` (default) to omit. Setting to `'true'` can produce very large exports that may fail to complete on file-heavy projects. |

> **Note:** All optional filtering parameters (`records`, `fields`, `events`, `filterLogic`, `exportSurveyFields`, `exportDataAccessGroups`, `exportFiles`) only apply to data. All metadata is always exported regardless.

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

The API always returns a single XML string in **CDISC ODM format (ODM version 1.3.1)**, regardless of any format parameters. The `returnFormat` parameter controls only error message formatting, not the response itself.

The ODM XML includes all metadata (fields, forms, events, arms) and, unless `returnMetadataOnly=true`, all records filtered according to any optional parameters supplied. This XML can be uploaded directly on the REDCap Create New Project page to clone the project.

---

# 5. Common Questions

**Q: Can I use the exported XML to create a new project?**
A: Yes. Use the Export Project XML API to download your project design, then use RC-API-37 (Import Project / Create Project) with that XML to clone the project.

**Q: What is the difference between `returnMetadataOnly` true and false?**
A: `'true'` returns only the project structure — all fields, forms, events, and arms — with no data records. `'false'` (the default) returns both metadata and data, optionally filtered by `records`, `fields`, `events`, or `filterLogic`.

**Q: Will the exported XML include data records?**
A: Yes, by default. `returnMetadataOnly` defaults to `'false'`, so data is included unless you explicitly set it to `'true'`.

**Q: Can I export only specific records or fields?**
A: Yes. Use the `records` parameter to specify an array of record names, the `fields` parameter for specific field names, or `filterLogic` to return only records matching a logic expression. These filters apply only to data — all metadata is always exported.

**Q: How large can the exported XML be?**
A: Export size depends on project complexity and the amount of data. Setting `exportFiles=true` can make the export extremely large if the project contains many or large file uploads. REDCap has default request limits; use `returnMetadataOnly=true` or filter parameters to reduce export size if you hit errors.

**Q: Can I use this export to clone a project?**
A: Yes. The ODM XML can be uploaded on the REDCap Create New Project page to recreate the project on the same instance or another REDCap server.

---

# 6. Common Mistakes & Gotchas

**Data included by default:** `returnMetadataOnly` defaults to `'false'`, meaning data is exported unless you explicitly opt out. If you only want the project structure, always pass `returnMetadataOnly='true'`.

**Data export rights apply to returned data:** If your account has De-Identified or Remove All Identifier Fields export rights, those restrictions are enforced on any data returned by this method. Use Full Data Set rights to avoid unexpected field omissions.

**`returnFormat` controls errors, not the response:** The response is always CDISC ODM XML. `returnFormat` only affects the format of any error messages returned. Don't confuse it with a general format selector.

**DAG flag ignored for DAG members:** `exportDataAccessGroups=true` only works if the API token belongs to a user who is not in a data access group. If the user is in a DAG, the flag silently reverts to `'false'`.

**`exportFiles=true` can break large exports:** Including file attachments significantly increases export size and may cause the request to fail or time out on projects with many or large files.

**Incomplete exports without all flags:** If you need data access groups, survey fields, or file attachments in your cloned project, explicitly set the relevant optional parameters to `'true'` before exporting.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-34 — Export Project Info
- RC-API-37 — Import Project (Create Project)
- RC-FD-01 — Form Design Overview (instrument structure captured in the project XML)
- RC-FD-03 — Data Dictionary (the metadata embedded in the exported XML)
