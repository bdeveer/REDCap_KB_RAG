RC-API-28

**Export DAGs API**

| **Article ID** | RC-API-28 |
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

The Export DAGs API method retrieves all Data Access Groups (DAGs) defined in your project. Each DAG is returned with its display name and unique group name. Use this method to automate DAG discovery, audit your DAG structure, or retrieve the list of available groups for downstream operations like user-DAG assignment or DAG deletion.

Data Access Groups enable role-based data segregation within a single project. This method is read-only and does not modify any project data.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export or User Rights rights. |
| `content` | Required | Always `'dag'` for this method. |
| `format` | Optional | Response format: `'json'` (default) or `'csv'`. |

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

The API returns a JSON or CSV array of all DAGs in the project. Each record contains:

- `unique_group_name`: The system-generated unique identifier for the DAG (e.g., `'group_1'`, `'group_2'`). Used in API calls, DAG operations, and data entry.
- `data_access_group_name`: The human-readable display name of the DAG (e.g., `'Boston Site'`, `'New York Site'`).

Example JSON response:
```json
[
  {
    "unique_group_name": "group_1",
    "data_access_group_name": "Boston Site"
  },
  {
    "unique_group_name": "group_2",
    "data_access_group_name": "New York Site"
  }
]
```

If the project has no DAGs defined, an empty array `[]` is returned.

---

# 5. Common Questions

**Q: What is the difference between `data_access_group_name` and `unique_group_name`?**

**A:** The `data_access_group_name` is the human-readable label for users (e.g., `'Boston Site'`). The `unique_group_name` is the system-generated unique identifier (e.g., `'group_1'`), used in API calls and data operations. Always use the `unique_group_name` in API operations.

**Q: How do I use this to get the list of DAGs before assigning users?**

**A:** Export the DAGs, then store the `unique_group_name` values. Use these values in the Import User-DAG Assignments method (RC-API-32) to assign users to specific groups.

**Q: What permissions do I need to export DAGs?**

**A:** Your API token must have API Export or User Rights permissions enabled at the project level.

**Q: Can I filter DAGs by name in the export?**

**A:** No. The export returns all DAGs in the project. You must filter the results in your code if needed.

**Q: What if the project has DAGs disabled?**

**A:** If DAGs are not enabled in the project, the export will return an empty array `[]` or an error message, depending on the REDCap version.

---

# 6. Common Mistakes & Gotchas

**Using `data_access_group_name` in API calls instead of `unique_group_name`.** The human-readable label will not work in API operations. Always use the `unique_group_name` value (e.g., `'group_1'`, not `'Boston Site'`) in Delete DAGs, Import User-DAG Assignments, and Switch DAG methods.

**Assuming DAGs are enabled in all projects.** Not all projects use Data Access Groups. Check that the export returns a non-empty array before assuming the project is DAG-enabled.

**Not storing the unique_group_name values for later use.** If you plan to assign users or delete DAGs, cache the exported `unique_group_name` values to avoid repeated exports.

**Confusing DAG exports with user-DAG mapping exports.** This method exports the DAG definitions themselves. To export user-DAG assignments, use the Export User-DAG Assignments method (RC-API-31).

**Forgetting to check API permissions.** If your token lacks API Export or User Rights permissions, the export will fail. Ensure the token is configured correctly at the project level.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-DAG-01 — Data Access Groups (explains DAG concepts, structure, and configuration)
- RC-DE-09 — Data Entry with Data Access Groups (covers data entry constraints in DAG-enabled projects)
- RC-API-29 — Import DAGs (create or update DAG definitions)
- RC-API-30 — Delete DAGs (remove DAG definitions)
- RC-API-31 — Export User-DAG Assignments (retrieve user-to-DAG mappings)
- RC-API-32 — Import User-DAG Assignments (assign users to DAGs)
- RC-API-33 — Switch DAG (change a user's active DAG context)
