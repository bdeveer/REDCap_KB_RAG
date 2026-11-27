---
id: RC-API-28
title: Export DAGs API
domain: API
applies_to:
- All REDCap projects with Data Access Groups enabled
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Export
  DAGs behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-DE-09
  title: Data Entry with Data Access Groups
tags:
- api
synonyms:
- how do i export dags via the api
- export data access groups api call
- get the list of dags through the api
- api method to retrieve dag names and unique group names
- pull data access group structure with the api
- audit dags programmatically
- api endpoint to export data access groups
- list data access groups in a project via api
---

# 1. Overview

The Export DAGs API method retrieves all Data Access Groups (DAGs) defined in your project. Each DAG is returned with its display name, unique group name and numeric group ID. Use this method to automate DAG discovery, audit your DAG structure, or retrieve the list of available groups for downstream operations like user-DAG assignment or DAG deletion.

Data Access Groups enable role-based data segregation within a single project. This method is read-only and does not modify any project data.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export **and** Data Access Groups privileges at the project level, and the token's user must not be assigned to a DAG. |
| `content` | Required | Always `'dag'` for this method. |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'`. Defaults to `'xml'` if omitted. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value passed in `format`. Not applicable when using a background process. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'dag',
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
    content='dag',
    format='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=dag&format=json"

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
	'content' => 'dag',
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
```

> **Note:** CURLOPT_SSL_VERIFYPEER should be TRUE in production.

---

# 4. Response

The API returns all DAGs in the project in the requested format (JSON, CSV or XML). Each row contains:

- `data_access_group_name`: The human-readable display name of the DAG (e.g., `'Boston Site'`, `'New York Site'`).
- `unique_group_name`: The unique identifier REDCap generates from the label (e.g., label `Boston Site` becomes `boston_site`). Used in API calls, DAG operations, and data imports.
- `data_access_group_id`: The numeric ID of the DAG within REDCap.

Example JSON response:
```json
[
  {
    "data_access_group_name": "Boston Site",
    "unique_group_name": "boston_site",
    "data_access_group_id": "1205"
  },
  {
    "data_access_group_name": "New York Site",
    "unique_group_name": "new_york_site",
    "data_access_group_id": "1206"
  }
]
```

If the project has no DAGs defined, the call still succeeds and returns an empty result: `[]` in JSON, only the header row in CSV, and an empty document in XML.

**Unique names follow the current labels.** REDCap derives each `unique_group_name` from the DAG's current label. Renaming a DAG changes its unique name, and adding or deleting a DAG whose label clashes with another can change the letter suffix (for example `b` or `c`) REDCap adds to tell the clashing names apart. Re-export the DAGs before any script relies on stored unique names, especially after DAGs have been renamed, added or deleted.

> **Version caveat (17.3 and later):** projects have an optional setting to convert accented letters (for example `é` to `e`) before the unique name is built. On 16.0, and on newer versions with the setting off, accented letters are dropped from the unique name instead. Check the exported `unique_group_name` values rather than predicting them from labels that contain accented characters.

---

# 5. Common Questions

**Q: What is the difference between `data_access_group_name` and `unique_group_name`?**

**A:** The `data_access_group_name` is the human-readable label for users (e.g., `'Boston Site'`). The `unique_group_name` is the identifier REDCap generates from that label (e.g., `'boston_site'`), used in API calls and data operations. Always use the `unique_group_name` in API operations. The export also includes `data_access_group_id`, the DAG's numeric ID.

**Q: How do I use this to get the list of DAGs before assigning users?**

**A:** Export the DAGs, then store the `unique_group_name` values. Use these values in the Import User-DAG Assignments method ([RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md)) to assign users to specific groups.

**Q: What permissions do I need to export DAGs?**

**A:** Your API token must have both API Export **and** Data Access Groups privileges enabled at the project level. Having only one of the two is not sufficient. The token's user must also not be assigned to a DAG: a DAG-assigned user gets HTTP 403 `You do not have permission to export/import/delete Data Access Groups because you have been assigned to a Data Access Group.` even with both rights. Use a token belonging to a user who is not in any DAG.

**Q: Can I filter DAGs by name in the export?**

**A:** No. The export returns all DAGs in the project. You must filter the results in your code if needed.

**Q: What if the project has DAGs disabled?**

**A:** A project with no DAGs returns an empty result, not an error: `[]` in JSON, only the header row in CSV, and an empty document in XML.

---

# 6. Common Mistakes & Gotchas

**Using `data_access_group_name` in API calls instead of `unique_group_name`.** The human-readable label will not work in API operations. Always use the `unique_group_name` value (e.g., `'boston_site'`, not `'Boston Site'`) in Delete DAGs, Import User-DAG Assignments, and Switch DAG methods.

**Assuming DAGs are enabled in all projects.** Not all projects use Data Access Groups. Check that the export returns a non-empty array before assuming the project is DAG-enabled.

**Relying on stale unique_group_name values.** Unique names are rebuilt from the current labels, so renaming, adding or deleting DAGs can change them. Re-export the DAGs before assigning users, importing records or deleting DAGs rather than reusing values cached from an earlier run.

**Confusing DAG exports with user-DAG mapping exports.** This method exports the DAG definitions themselves. To export user-DAG assignments, use the Export User-DAG Assignments method ([RC-API-31 — Export User-DAG Assignments API](RC-API-31_Export-User-DAG-Assignments.md)).

**Forgetting to check API permissions.** If your token lacks either API Export or Data Access Groups privileges, the export will fail. Both permissions are required — ensure both are enabled for the token at the project level.

**Using the token of a DAG-assigned user.** A user who is assigned to a DAG cannot export DAGs through the API, even with both rights; the call returns HTTP 403 saying they have been assigned to a Data Access Group. Use the token of a user who is not assigned to any DAG.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (explains DAG concepts, structure, and configuration)
- [RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md) (covers data entry constraints in DAG-enabled projects)
- [RC-API-29 — Import DAGs API](RC-API-29_Import-DAGs.md) (create or update DAG definitions)
- [RC-API-30 — Delete DAGs API](RC-API-30_Delete-DAGs.md) (remove DAG definitions)
- [RC-API-31 — Export User-DAG Assignments API](RC-API-31_Export-User-DAG-Assignments.md) (retrieve user-to-DAG mappings)
- [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md) (assign users to DAGs)
- [RC-API-33 — Switch DAG API](RC-API-33_Switch-DAG.md) (change a user's active DAG context)
