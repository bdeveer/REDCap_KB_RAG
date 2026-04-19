RC-API-56

**Import User-Role Assignments API**

| **Article ID** | RC-API-56 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API official documentation |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-55 — Export User-Role Assignments; RC-API-25 — Export User Roles; RC-USER-01 — User Rights: Overview & Three-Tier Access |

---

# 1. Overview

The Import User-Role Assignments API method assigns existing project users to existing user roles, or removes users from their current role. The payload is a list of username-to-role mappings. Passing an empty `unique_role_name` for a user will remove them from any role assignment.

Use this method to automate bulk role assignments, replicate role structures across projects, or programmatically manage access when user lists change.

> **Important:** There must be only one record per username in the data payload. Duplicate usernames will cause an error. To modify an existing assignment, provide the username with the new `unique_role_name` — the existing assignment will be overwritten.

---

# 2. Key Concepts & Definitions

### User Role
A template of permissions that can be assigned to multiple users. Each role has a unique system-generated ID (unique_role_name).

### Unique Role Name
A system-generated identifier for a role (e.g., `U-2119C4Y87T`), used to specify which role to assign during import.

### Role Assignment
The mapping of a specific user to a specific role. Determines the permissions that user has in the project.

### Data Access Group (DAG)
A logical division of project users and records. Can be assigned to a user at the same time as a role assignment using the optional data_access_group field.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and User Rights rights. |
| `content` | Required | Always `'userRoleMapping'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `format` | Optional | Data format: `'csv'`, `'json'`, or `'xml'` (default). |
| `data` | Required | List of user-role mapping objects. Each must include `username` and `unique_role_name`. See Section 2.1 for details and format examples. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not specified, or `'xml'` if neither is provided. Does not apply when using background processing. |

---

## 3.1 Data Attribute Reference

Each record in the `data` payload contains:

| Field | Required | Description |
|---|---|---|
| `username` | Required | The existing REDCap username to assign. Must already be a user in the project. |
| `unique_role_name` | Required | The system ID of the role to assign (e.g., `U-2119C4Y87T`). Pass an empty string to remove the user from any role. |
| `data_access_group` | Optional | A valid unique DAG name. If the project uses DAGs, you may assign the user to a DAG at the same time as assigning their role. |

**JSON example:**

```json
[{"username":"global_user","unique_role_name":""},
 {"username":"ca_dt_person","unique_role_name":"U-2119C4Y87T"},
 {"username":"fl_dt_person","unique_role_name":"U-2119C4Y87T"}]
```

**CSV example:**

```
username,unique_role_name
ca_dt_person,U-2119C4Y87T
fl_dt_person,U-2119C4Y87T
global_user,
```

**XML example:**

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<items>
   <item>
      <username>ca_dt_person</username>
      <unique_role_name>U-2119C4Y87T</unique_role_name>
   </item>
   <item>
      <username>fl_dt_person</username>
      <unique_role_name>U-2119C4Y87T</unique_role_name>
   </item>
   <item>
      <username>global_user</username>
      <unique_role_name></unique_role_name>
   </item>
</items>
```

---

# 4. Request Examples

## 4.1 Python
```python
from config import config
import requests, json

data = [
    {"username": "ca_dt_person", "unique_role_name": "U-2119C4Y87T"},
    {"username": "fl_dt_person", "unique_role_name": "U-2119C4Y87T"},
    {"username": "global_user",  "unique_role_name": ""},
]

fields = {
    'token':   config['api_token'],
    'content': 'userRoleMapping',
    'action':  'import',
    'format':  'json',
    'data':    json.dumps(data),
}

r = requests.post(config['api_url'], data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 4.2 R
```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)
library(jsonlite)

data <- toJSON(list(
    list(username="ca_dt_person", unique_role_name="U-2119C4Y87T"),
    list(username="fl_dt_person", unique_role_name="U-2119C4Y87T"),
    list(username="global_user",  unique_role_name="")
), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='userRoleMapping',
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

DATA="token=$API_TOKEN&content=userRoleMapping&action=import&format=json\
&data=[{\"username\":\"ca_dt_person\",\"unique_role_name\":\"U-2119C4Y87T\"},\
{\"username\":\"fl_dt_person\",\"unique_role_name\":\"U-2119C4Y87T\"},\
{\"username\":\"global_user\",\"unique_role_name\":\"\"}]"

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

$data = json_encode(array(
    array('username' => 'ca_dt_person', 'unique_role_name' => 'U-2119C4Y87T'),
    array('username' => 'fl_dt_person', 'unique_role_name' => 'U-2119C4Y87T'),
    array('username' => 'global_user',  'unique_role_name' => ''),
));

$fields = array(
    'token'   => $GLOBALS['api_token'],
    'content' => 'userRoleMapping',
    'action'  => 'import',
    'format'  => 'json',
    'data'    => $data,
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5.

---

# 5. Response

On success, the API returns a count of user-role assignments added or updated. For example: `3` means three assignment records were processed.

---

# 6. Common Questions

**Q: How do I remove a user from their role without deleting the user?**

**A:** Include the user in your data payload with an empty `unique_role_name`. The user will be unassigned from their role but remain in the project with no role-based permissions. Their permissions will effectively drop to zero unless individual permissions are set separately.

**Q: What happens if I omit `unique_role_name` entirely (rather than passing an empty string)?**

**A:** Per the official documentation, if `unique_role_name` is not provided, the user will not be assigned to any role — the behavior is the same as passing an empty string. Always include the field explicitly to avoid ambiguity.

**Q: Can I assign a user to a role and a DAG in the same call?**

**A:** Yes. Include the optional `data_access_group` field with a valid unique DAG name in the same record. This allows you to set both the role assignment and DAG membership in one API call.

**Q: What if I submit two records for the same username?**

**A:** The API requires exactly one record per username. Submitting duplicate usernames will cause an error. Deduplicate your data before sending.

**Q: How do I find the `unique_role_name` for a role?**

**A:** Use the Export User Roles method (RC-API-25) to retrieve all role definitions and their system IDs.

**Q: How do I know what role a user is currently in before modifying their assignment?**

**A:** Use Export User-Role Assignments (RC-API-55) to retrieve the current state before making changes.

---

# 7. Common Mistakes & Gotchas

**Omitting `unique_role_name` when you meant to keep the assignment.** If you build your data payload from a partial record and forget to include the role field, the user will be unassigned. Always verify your payload includes both `username` and `unique_role_name` for every record you intend to keep assigned.

**Duplicate usernames in the payload.** Each username must appear exactly once. If the same username appears twice (even with different role names), the import will fail. Deduplicate your data before calling the API.

**Using `role_label` instead of `unique_role_name`.** The `unique_role_name` is the system ID (e.g., `U-2119C4Y87T`), not the human-readable label (e.g., `'Data Entry Person'`). Export roles first to get the correct IDs.

**Assigning a user to a role they don't have access to.** The user must already exist in the project. This method assigns role templates; it does not add new users. Use Import Users (RC-API-23) first if the user isn't yet in the project.

**Forgetting the User Rights permission.** This method requires both API Import and User Rights rights. A token with only API Import will fail.

---

# 8. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-API-55 — Export User-Role Assignments (retrieve current assignments before modifying them)
- RC-API-25 — Export User Roles (get role definitions and their `unique_role_name` IDs)
- RC-API-26 — Import User Roles (create or update role definitions)
- RC-API-23 — Import Users (add users to the project before assigning roles)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (conceptual overview of roles and assignments)
- RC-DAG-01 — Data Access Groups (background on DAGs if using the `data_access_group` field)
