---
id: RC-API-29
title: Import DAGs API
domain: API
applies_to:
- All REDCap projects with Data Access Groups enabled
prerequisites:
- RC-API-01 — REDCap API
version: '1.1'
last_updated: '2026'
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
- how do i import dags via the api
- import data access groups api call
- create or update dags through the api
- api method to add data access group names
- bulk create dags with the api
- migrate data access groups programmatically
- api endpoint to import data access groups
- add data access groups to a project via api
---

# 1. Overview

The Import DAGs API method creates new Data Access Groups or updates existing ones in your project. You provide a JSON or CSV payload containing DAG definitions: a human-readable display name and an optional unique group name. If the `unique_group_name` is omitted or empty, REDCap auto-generates it. Use this method to automate DAG creation, migrate DAGs between projects, or bulk-import DAG structures from external systems.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update **and** Data Access Groups privileges at the project level. |
| `content` | Required | Always `'dag'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `format` | Required | Format of the `data` payload and response: `'csv'`, `'json'`, or `'xml'` (default). |
| `data` | Required | Array of DAG records in the specified format. Each record must contain `data_access_group_name` and `unique_group_name`. Set `unique_group_name` to blank to create a new DAG; provide an existing value to update it. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value passed in `format`. Not applicable when using a background process. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests, json

record = {
    'data_access_group_name': 'Group API',
    'unique_group_name': ''
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'dag',
    'action': 'import',
    'format': 'json',
    'data': data,
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
library(jsonlite)

record <- c(
	data_access_group_name='Group API',
	unique_group_name=''
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='dag',
	action='import',
    format='json',
    data=data
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=dag&action=import&format=json&data=[{\"data_access_group_name\":\"Group%20API\",\"unique_group_name\":\"\"}]"

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

$data = array(
	array(
		'data_access_group_name' => 'Group API 1',
		'unique_group_name'    => 'group_api'
	),
	array(
		'data_access_group_name' => 'Group API 2',
		'unique_group_name'    => ''
	),
);

$data = json_encode($data);

$fields = array(
	'token'    => $GLOBALS['api_token'],
	'content'  => 'dag',
	'action'   => 'import',
	'format'   => 'json',
	'data'     => $data,
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

On success, the API returns the count of DAGs created or updated. For example: `2` means two DAGs were imported. If a `unique_group_name` is provided and already exists, that DAG is updated; otherwise, a new DAG is created.

Example response: `2`

---

# 5. CSV Format

When submitting the `data` payload as CSV (`format='csv'`), the file uses the following structure.

**Columns:** `data_access_group_name`, `unique_group_name`

| **Column** | **Type** | **Required** | **Notes** |
|---|---|---|---|
| `data_access_group_name` | Free text | Required | Human-readable display name for the DAG (e.g., `Boston Site`). Shown in the REDCap UI. Values containing spaces or commas must be enclosed in double quotes. |
| `unique_group_name` | Alphanumeric/underscore | Optional | System identifier used in all API calls and data entry. Leave blank to let REDCap auto-generate it from the display name (lowercase, spaces converted to underscores — e.g., `"New Haven"` → `new_haven`). If provided, must be unique within the project. |

Example CSV (two new DAGs, auto-generated unique names):
```
data_access_group_name,unique_group_name
"New Haven",
Seattle,
```

Example CSV (two DAGs with explicit unique names):
```
data_access_group_name,unique_group_name
"New Haven",new_haven
Seattle,seattle
```

> **Note:** The `data_access_group_id` column appears as a third column in DAG **exports** (e.g., `data_access_group_name,unique_group_name,data_access_group_id`). This is a read-only internal ID assigned by REDCap and is ignored on import — you do not need to include it when building an import file, but it is harmless to leave it in if you are re-uploading an exported file.

---

# 6. Common Questions

**Q: Do I have to provide a `unique_group_name` when importing?**

**A:** No. If you omit the field or leave it empty, REDCap auto-generates a unique ID based on the display name. If you provide a `unique_group_name`, it will be used; if one with that name already exists, the DAG will be updated.

**Q: Can I import multiple DAGs in a single call?**

**A:** Yes. Pass an array of DAG records in the `data` field. Each record will be created or updated.

**Q: What happens if a DAG with the same `unique_group_name` already exists?**

**A:** The existing DAG is updated with the new `data_access_group_name`. Users assigned to that DAG are not affected.

**Q: What format should the `unique_group_name` have?**

**A:** It should be alphanumeric and lowercase, typically without spaces (e.g., `'boston_site'`, `'group_1'`). Avoid special characters.

**Q: What permissions are required?**

**A:** Your API token must have both API Import/Update **and** Data Access Groups privileges enabled at the project level. Having only one of the two is not sufficient.

---

# 7. Common Mistakes & Gotchas

**Using spaces or special characters in `unique_group_name`.** While REDCap may accept them, stick to alphanumeric characters and underscores for consistency and to avoid downstream issues. If you provide a complex name, it may not work properly in data entry or other operations.

**Forgetting to provide `data_access_group_name`.** This field is required and must be a non-empty string. Each DAG must have a human-readable display name.

**Attempting to import without the correct permissions.** This method requires both API Import/Update **and** Data Access Groups privileges. Having only API Import is not sufficient — the token must also have Data Access Groups access enabled at the project level.

**Not URL-encoding the `data` field in cURL.** In shell scripts, ensure special characters in JSON (like `"` and spaces) are properly encoded or escaped.

**Misunderstanding what `format` controls.** The `format` parameter governs both the format of the `data` payload you send **and** the response format. You can submit `data` as JSON, CSV, or XML — just ensure the `format` parameter matches the format of your payload.

**Trying to update a DAG by display name alone.** You must use the `unique_group_name` to target an existing DAG for updates. If you omit it, a new DAG is created instead.

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (explains DAG concepts, structure, and configuration)
- [RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md) (covers data entry constraints in DAG-enabled projects)
- [RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md)(retrieve existing DAG definitions)
- [RC-API-30 — Delete DAGs API](RC-API-30_Delete-DAGs.md)(remove DAG definitions)
- [RC-API-31 — Export User-DAG Assignments API](RC-API-31_Export-User-DAG-Assignments.md)(retrieve user-to-DAG mappings)
- [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md)(assign users to DAGs)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (reference for permission types)
