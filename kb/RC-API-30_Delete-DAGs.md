RC-API-30

**Delete DAGs API**

| **Article ID** | RC-API-30 |
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

The Delete DAGs API method removes Data Access Groups from your project. You provide a list of DAG unique group names (the `unique_group_name` values) to delete. This method deletes the DAG definition itself. Users and records assigned to that DAG are not deleted, but they lose the DAG association. Use this method to clean up unused DAGs, automate DAG lifecycle management, or remove groups after consolidation.

Caution: Deleting a DAG is a significant operation. Users in deleted DAGs may lose their data isolation context. Ensure this is intended before deletion.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and User Rights rights. |
| `content` | Required | Always `'dag'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `format` | Optional | Response format: `'json'` (default) or `'csv'`. |
| `dags[0]`, `dags[1]`, ... | Required | Array of DAG unique group names to delete. Pass as `dags[0]=group_1&dags[1]=group_2`, etc. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'dag',
    'action': 'delete',
    'format': 'json',
    'dags[0]': 'group_api'
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
    action='delete',
    'dags[0]'='group_api'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=dag&action=delete&format=json&dags[0]=group_api"

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
	'action'  => 'delete',
	'format'  => 'json',
	'dags'  => array('group_api'),
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

On success, the API returns a count of DAGs deleted. For example: `1` means one DAG was removed from the project. If a DAG name does not exist in the project, it is ignored and does not affect the response.

Example response: `1`

---

# 5. Common Questions

**Q: What happens to data records assigned to a deleted DAG?**

**A:** The records are not deleted. However, they lose their DAG assignment. In most cases, they become accessible to users with all-DAG view permissions. If your project uses strict data isolation, ensure you reassign records or users before deleting a DAG.

**Q: What is the `unique_group_name`?**

**A:** It's the system-generated identifier assigned to the DAG (e.g., `'group_1'`, `'boston_site'`). To find this ID, export existing DAGs using the Export DAGs method (RC-API-28).

**Q: What if I try to delete a DAG that doesn't exist?**

**A:** The API ignores the DAG name and does not report an error. If you delete a DAG and the API returns 0, it means the DAG was not found in the project.

**Q: Can I delete multiple DAGs at once?**

**A:** Yes. Pass multiple unique group names using array syntax: `dags[0]=group_1&dags[1]=group_2`. All DAGs in the array will be deleted in a single call.

**Q: Can I undo a DAG deletion?**

**A:** No. DAG deletion is permanent. To restore a DAG, you must import it again using the Import DAGs method (RC-API-29) with the same or similar definition. Records that lost their DAG assignment cannot automatically regain it.

**Q: What permissions do I need?**

**A:** Your API token must have both API Import and User Rights permissions enabled at the project level.

---

# 6. Common Mistakes & Gotchas

**Deleting a DAG without reassigning its users or records.** Users and records assigned to a deleted DAG will lose the DAG association. Before deleting a DAG in production, export users and records to identify what is affected. If users need to retain data isolation, reassign them to alternative DAGs or adjust record assignments.

**Confusing DAG display names with unique group names.** The `unique_group_name` is the system ID (e.g., `'boston_site'`), not the human-readable label (e.g., `'Boston Site'`). Use the ID, not the label, in the delete request.

**Expecting an error when deleting a non-existent DAG.** The API does not return an error if a DAG is not found; it simply returns 0. Check the response count to verify the expected number of DAGs were deleted.

**Forgetting the User Rights permission.** This method requires both API Import and User Rights rights. If your token lacks User Rights, the deletion will fail.

**Inadvertently deleting the wrong DAG.** DAG names are easy to mistype. Always verify the correct unique group name by exporting existing DAGs before deletion.

**Deleting a DAG that users are currently active in.** If a user is actively viewing or entering data in a DAG you delete, their session context may become inconsistent. Notify users before deleting DAGs or ensure they switch to another DAG first.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-DAG-01 — Data Access Groups (explains DAG concepts, structure, and configuration)
- RC-DE-09 — Data Entry with Data Access Groups (covers data entry constraints in DAG-enabled projects)
- RC-API-28 — Export DAGs (retrieve existing DAG definitions and their unique names)
- RC-API-29 — Import DAGs (create or update DAG definitions)
- RC-API-31 — Export User-DAG Assignments (identify which users are assigned to DAGs)
- RC-API-32 — Import User-DAG Assignments (assign users to DAGs)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for permission types)
