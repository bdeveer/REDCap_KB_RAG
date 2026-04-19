RC-API-32

**Import User-DAG Assignments API**

| **Article ID** | RC-API-32 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects with Data Access Groups enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-DAG-01 — Data Access Groups; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Import User-DAG Assignments API method assigns users to Data Access Groups (DAGs) in your project. You provide a JSON or CSV payload containing usernames and the unique group names of the DAGs to which they should be assigned. An empty group name removes a user from all DAG assignments, granting them all-DAG view permissions. Use this method to automate user access provisioning, migrate user assignments between projects, or bulk-assign users to DAGs.

---

# 2. Key Concepts & Definitions

### API Token
A unique credential string issued by REDCap that authenticates your API requests. For this method, your token must have both API Import/Update and Data Access Groups privileges at the project level.

### Data Access Group (DAG)
A data isolation mechanism in REDCap that restricts which records a user can access. Each user can be assigned to at most one DAG. An empty assignment grants the user access to all records across all DAGs.

### Unique Group Name
The system identifier for a DAG (e.g., `'group_1'`, `'api_testing_group'`), distinct from the human-readable display label. The API always requires unique group names, not display labels.

### All-DAG Access
When a user is assigned an empty `redcap_data_access_group` value, they can view and edit records from all Data Access Groups in the project. This is typically granted to administrators and managers.

### Bulk Assignment
The ability to assign multiple users to DAGs in a single API call by passing an array of user-DAG records in the `data` parameter.

### User-DAG Mapping
The relationship between a username and the unique group name of the DAG to which the user is assigned. One mapping exists per user per project.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update **and** Data Access Groups privileges at the project level. |
| `content` | Required | Always `'userDagMapping'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `format` | Required | Format of the `data` payload and response: `'csv'`, `'json'`, or `'xml'` (default). |
| `data` | Required | Array of user-DAG assignment records in the specified format. Each record must contain `username` and `redcap_data_access_group`. There must be only one record per username. To modify an existing assignment, you must provide both the username and the current group name. If `redcap_data_access_group` is omitted or empty, the user is unassigned from all DAGs. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value passed in `format`. Not applicable when using a background process. |

---

# 3. Request Examples

## 4.1 Python
```python
from config import config
import requests, json

record = {
    'username': 'testuser',
    'redcap_data_access_group': 'api_testing_group'
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'userDagMapping',
    'action': 'import',
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
	username='testuser',
	redcap_data_access_group='api_testing_group'
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='userDagMapping',
	action='import',
    format='json',
    data=data
)
print(result)
```

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=userDagMapping&action=import&format=json&data=[{\"username\":\"testuser\",\"redcap_data_access_group\":\"api_testing_group\"}]"

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

$data = array(
	array(
		'username' => 'testuser1',
		'redcap_data_access_group'    => 'api_testing_group1'
	),
	array(
		'username' => 'testuser2',
		'redcap_data_access_group'    => 'api_testing_group2'
	),
);

$data = json_encode($data);

$fields = array(
	'token'    => $GLOBALS['api_token'],
	'content'  => 'userDagMapping',
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

# 5. Response

On success, the API returns the count of user-DAG assignments created or updated. For example: `2` means two users were assigned or reassigned to DAGs. If a user already has the same DAG assignment, the operation is still counted as successful.

Example response: `2`

---

# 6. Common Questions

**Q: Can I assign a user to multiple DAGs?**

**A:** No. Each user can be assigned to at most one DAG. If you need a user to see data from multiple groups, assign them an empty `redcap_data_access_group` value (or omit it from the import) to grant them all-DAG view permissions.

**Q: How do I remove a user from a DAG assignment?**

**A:** Set `redcap_data_access_group` to an empty string. This grants the user all-DAG access and removes their DAG restriction.

**Q: What if the user doesn't exist yet?**

**A:** The import will fail if the user account does not exist in the project. Use the Import Users method (RC-API-23) to create the user first, then assign them to a DAG.

**Q: What if the DAG doesn't exist?**

**A:** The import will fail if the DAG does not exist. Use the Import DAGs method (RC-API-29) to create the DAG first, then assign users to it.

**Q: Can I assign multiple users to the same DAG in one call?**

**A:** Yes. Pass multiple user records in the `data` array, with each user assigned to the desired DAG.

**Q: What happens if I assign a user to a DAG they were already assigned to?**

**A:** The API counts this as a successful update. The user's assignment is confirmed or updated, but the outcome is the same.

**Q: What permissions are required?**

**A:** Your API token must have both API Import/Update **and** Data Access Groups privileges enabled at the project level. Having only one of the two is not sufficient.

---

# 7. Common Mistakes & Gotchas

**Using the DAG display name instead of the unique group name.** The `redcap_data_access_group` field requires the unique group name (e.g., `'group_1'`, `'boston_site'`), not the human-readable label (e.g., `'Boston Site'`). Use the Export DAGs method (RC-API-28) to find the correct unique names.

**Forgetting to check if users exist.** If a user account does not exist in the project, the assignment will fail. Ensure all usernames are valid before attempting assignment.

**Forgetting to check if DAGs exist.** If a DAG does not exist, the assignment will fail. Export DAGs (RC-API-28) first to verify the correct unique group name.

**Not realizing that empty `redcap_data_access_group` grants all-DAG access.** An empty string or null value means the user sees all data across all DAGs. This is common for administrators, but ensure it is intentional.

**Missing the correct permissions.** This method requires both API Import/Update **and** Data Access Groups privileges. Having only one is not sufficient — the import will fail if either is missing at the project level.

**Not URL-encoding the `data` field in cURL.** In shell scripts, ensure special characters in JSON (like `"` and spaces) are properly encoded or escaped.

**Including more than one record per username.** The API requires exactly one record per username in the `data` payload. Submitting duplicate username entries in a single import call will cause an error. If you need to update a user's assignment, include a single record with their new group name.

**Confusing user assignment with role assignment.** DAG assignment controls data access by group, not permissions. If you need to set specific permissions (form access, export rights, etc.), also use the Import User Roles method (RC-API-26) or Import Users method (RC-API-23).

---

# 8. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-DAG-01 — Data Access Groups (explains DAG concepts, structure, and configuration)
- RC-DE-09 — Data Entry with Data Access Groups (covers data entry constraints in DAG-enabled projects)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for user permission types)
- RC-API-22 — Export Users (retrieve user account details)
- RC-API-23 — Import Users (create or update user accounts)
- RC-API-28 — Export DAGs (retrieve DAG definitions and unique names)
- RC-API-29 — Import DAGs (create or update DAG definitions)
- RC-API-31 — Export User-DAG Assignments (retrieve existing assignments)
- RC-API-33 — Switch DAG (allow users to change their active DAG context)
