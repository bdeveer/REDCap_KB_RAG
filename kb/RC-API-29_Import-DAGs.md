RC-API-29

**Import DAGs API**

| **Article ID** | RC-API-29 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects with Data Access Groups enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-DAG-01 — Data Access Groups; RC-DE-09 — Data Entry with Data Access Groups |

---

# 1. Overview

The Import DAGs API method creates new Data Access Groups or updates existing ones in your project. You provide a JSON or CSV payload containing DAG definitions: a human-readable display name and an optional unique group name. If the `unique_group_name` is omitted or empty, REDCap auto-generates it. Use this method to automate DAG creation, migrate DAGs between projects, or bulk-import DAG structures from external systems.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and User Rights rights. |
| `content` | Required | Always `'dag'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `format` | Optional | Response format: `'json'` (default) or `'csv'`. |
| `data` | Required | JSON or CSV array of DAG records. Each record must contain `data_access_group_name` and may contain `unique_group_name`. |

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

# 5. Common Questions

**Q: Do I have to provide a `unique_group_name` when importing?**

**A:** No. If you omit the field or leave it empty, REDCap auto-generates a unique ID based on the display name. If you provide a `unique_group_name`, it will be used; if one with that name already exists, the DAG will be updated.

**Q: Can I import multiple DAGs in a single call?**

**A:** Yes. Pass an array of DAG records in the `data` field. Each record will be created or updated.

**Q: What happens if a DAG with the same `unique_group_name` already exists?**

**A:** The existing DAG is updated with the new `data_access_group_name`. Users assigned to that DAG are not affected.

**Q: What format should the `unique_group_name` have?**

**A:** It should be alphanumeric and lowercase, typically without spaces (e.g., `'boston_site'`, `'group_1'`). Avoid special characters.

**Q: What permissions are required?**

**A:** Your API token must have both API Import and User Rights permissions enabled at the project level.

---

# 6. Common Mistakes & Gotchas

**Using spaces or special characters in `unique_group_name`.** While REDCap may accept them, stick to alphanumeric characters and underscores for consistency and to avoid downstream issues. If you provide a complex name, it may not work properly in data entry or other operations.

**Forgetting to provide `data_access_group_name`.** This field is required and must be a non-empty string. Each DAG must have a human-readable display name.

**Attempting to import with API Export permission instead of API Import.** This method requires API Import rights, not Export. Check your token permissions at the project level.

**Not URL-encoding the `data` field in cURL.** In shell scripts, ensure special characters in JSON (like `"` and spaces) are properly encoded or escaped.

**Confusing the response format with the payload.** The `format` parameter controls the response, not the data format. You always submit data as JSON in the `data` field.

**Trying to update a DAG by display name alone.** You must use the `unique_group_name` to target an existing DAG for updates. If you omit it, a new DAG is created instead.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-DAG-01 — Data Access Groups (explains DAG concepts, structure, and configuration)
- RC-DE-09 — Data Entry with Data Access Groups (covers data entry constraints in DAG-enabled projects)
- RC-API-28 — Export DAGs (retrieve existing DAG definitions)
- RC-API-30 — Delete DAGs (remove DAG definitions)
- RC-API-31 — Export User-DAG Assignments (retrieve user-to-DAG mappings)
- RC-API-32 — Import User-DAG Assignments (assign users to DAGs)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for permission types)
