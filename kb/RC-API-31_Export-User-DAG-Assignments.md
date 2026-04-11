RC-API-31

**Export User-DAG Assignments API**

| **Article ID** | RC-API-31 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects with Data Access Groups enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-DAG-01 — Data Access Groups; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Export User-DAG Assignments API method retrieves the mapping of users to Data Access Groups (DAGs) in your project. Each record pairs a username with the unique group name of the DAG assigned to that user. Use this method to audit user-DAG assignments, validate your user access structure, identify unassigned users, or export assignments for backup or migration.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export or User Rights rights. |
| `content` | Required | Always `'userDagMapping'` for this method. |
| `format` | Optional | Response format: `'json'` (default) or `'csv'`. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'userDagMapping',
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
    content='userDagMapping',
    format='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=userDagMapping&format=json"

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
	'content' => 'userDagMapping',
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

The API returns a JSON or CSV array of user-DAG mappings. Each record contains:

- `username`: The user account name (e.g., `'john.doe'`, `'jane.smith'`).
- `redcap_data_access_group`: The unique group name of the assigned DAG (e.g., `'group_1'`, `'boston_site'`). An empty string indicates the user is not assigned to any DAG.

Example JSON response:
```json
[
  {
    "username": "john.doe",
    "redcap_data_access_group": "group_1"
  },
  {
    "username": "jane.smith",
    "redcap_data_access_group": "group_2"
  },
  {
    "username": "admin.user",
    "redcap_data_access_group": ""
  }
]
```

If the project has no users, an empty array `[]` is returned. Users with an empty `redcap_data_access_group` are not assigned to any specific DAG (they typically have all-DAG view permissions).

---

# 5. Common Questions

**Q: What does an empty `redcap_data_access_group` mean?**

**A:** An empty value means the user is not assigned to any specific DAG. This user typically has all-DAG view permissions and can see data across all groups in the project. This is common for administrators or managers.

**Q: How do I identify users without a DAG assignment?**

**A:** Export the user-DAG mappings and filter for records where `redcap_data_access_group` is empty. These users have project-wide access.

**Q: Can a user be assigned to multiple DAGs?**

**A:** No. Each user can be assigned to at most one DAG. If a user needs multi-DAG access, they must be assigned no DAG (empty value) to gain all-DAG view permissions.

**Q: How do I use this export to audit user access?**

**A:** Export the user-DAG mappings and combine it with the Export Users export (RC-API-22) to correlate user roles with DAG assignments. This helps verify that users have appropriate data isolation.

**Q: What permissions do I need?**

**A:** Your API token must have API Export or User Rights permissions enabled at the project level.

**Q: What if DAGs are not enabled in the project?**

**A:** If DAGs are not enabled, the export will return an empty array `[]` or an error, depending on the REDCap version.

---

# 6. Common Mistakes & Gotchas

**Confusing user-DAG mappings with user roles.** This export shows DAG assignments only, not roles or permissions. To see what a user can do, also export user roles (RC-API-25) or users (RC-API-22) and cross-reference with their permissions.

**Assuming all users are assigned to a DAG.** Many users may have empty DAG assignments, meaning they have all-DAG access. Do not assume every user is restricted to a single group.

**Not checking the unique group name format.** The `redcap_data_access_group` field contains the unique group name (e.g., `'group_1'`), not the display label (e.g., `'Boston Site'`). Use these values if you plan to delete DAGs or modify assignments.

**Forgetting to export DAGs first.** If you want to understand what each DAG is called, export DAGs (RC-API-28) first to map unique group names to display names.

**Not handling users assigned to deleted DAGs.** If a DAG is deleted but users are still assigned to it, they will appear in this export with the deleted DAG's unique group name. Their access may become inconsistent. Clean up assignments before deleting DAGs.

**Expecting all project users in the export.** This export only includes users who have been explicitly assigned (or not assigned) to DAGs. Users may be exported here even if they lack certain permissions.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-DAG-01 — Data Access Groups (explains DAG concepts, structure, and configuration)
- RC-DE-09 — Data Entry with Data Access Groups (covers data entry constraints in DAG-enabled projects)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for user permission types)
- RC-API-22 — Export Users (retrieve user account details and permissions)
- RC-API-25 — Export User Roles (retrieve role definitions and assignments)
- RC-API-28 — Export DAGs (retrieve DAG definitions and unique names)
- RC-API-32 — Import User-DAG Assignments (assign users to DAGs)
- RC-API-33 — Switch DAG (allow users to change their active DAG context)
