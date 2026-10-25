---
id: RC-API-55
title: Export User-Role Assignments API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.5.6 (Standard) — §1, §5–§7 (admin token; role-assigned
  users not yet tested) live-tested via the API on a sandbox project (2026-10); LTS
  line last reviewed against the v17.3.7 (LTS) changelog
prerequisites:
- RC-API-01 — REDCap API
version: '1.1'
last_updated: 2026-10
source: REDCap API official documentation
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-25
  title: Export User Roles API
- id: RC-API-56
  title: Import User-Role Assignments API
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
tags:
- api
synonyms:
- export user-role assignments api method
- how do i see which users are in which roles via the api
- api call to export user to role mappings
- retrieve role assignments for users through the api
- get unique_role_name per user using the api
- api method to audit user role membership
- programmatically export user-role assignments with the api
- user role assignments api blank unique_role_name
---

# 1. Overview

The Export User-Role Assignments API method retrieves the current mapping between users and their assigned roles in a project. Each record in the response contains a username and the `unique_role_name` of the role they are assigned to. Every project user is listed: users who are not assigned to a role have a blank `unique_role_name`.

Use this method to audit which users belong to which roles, verify role assignments before making changes, or build external reporting on project access structure.

---

# 2. Key Concepts & Definitions

### User Role
A template of permissions that can be assigned to multiple users as a group. Defined once and reused to manage consistent access levels across users.

### Unique Role Name
A system-generated identifier for a role (e.g., `U-527D39JXAC`), distinct from the human-readable role label.

### Role Assignment
The mapping between a specific user and a user role. Determines what permissions that user has in the project.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export and User Rights rights (Full Access or Read Only). |
| `content` | Required | Always `'userRoleMapping'` for this method. |
| `format` | Optional | Return format: `'csv'`, `'json'`, or `'xml'` (default). |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not specified, or `'xml'` if neither is provided. Does not apply when using background processing. |

---

# 4. Request Examples

## 4.1 Python
```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'userRoleMapping',
    'format': 'json'
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

result <- postForm(
    api_url,
    token=api_token,
    content='userRoleMapping',
    format='json'
)
print(result)
```

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=userRoleMapping&format=json"

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

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'userRoleMapping',
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5.

---

# 5. Response

On success, the method returns one row per project user in the requested format. Each record contains three fields:

- `username` — The REDCap username of the assigned user.
- `unique_role_name` — The system-generated role ID the user is assigned to (e.g., `U-527D39JXAC`). Use the Export User Roles method ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)) to look up what role name and privileges correspond to each ID.

- `data_access_group` — The user's Data Access Group (unique group name); blank when the user is not in a DAG.

Users without a role are included with a blank `unique_role_name`:

```json
[
  {"username": "jane.smith", "unique_role_name": "U-527D39JXAC", "data_access_group": ""},
  {"username": "admin_user", "unique_role_name": "", "data_access_group": ""}
]
```

---

# 6. Common Questions

**Q: What's the difference between this method and Export Users?**

**A:** Export Users ([RC-API-22 — Export Users API](RC-API-22_Export-Users.md)) returns each user's full permission set as currently configured. Export User-Role Assignments returns only the username-to-role mapping — which role each user is assigned to. If you need to know a user's effective permissions, use Export Users. If you need to know which users belong to which role templates, use this method.

**Q: How do I find out what permissions a role grants?**

**A:** Use Export User Roles ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)) to retrieve role definitions. Cross-reference the `unique_role_name` from this method's response against the role list to see the full permission set.

**Q: Are users without a role assignment included?**

**A:** Yes. Every project user is returned; users with individually-set permissions (not via a role) have an empty `unique_role_name`. Filter on a non-empty `unique_role_name` to list role members only.

**Q: Can I use this export to feed an import?**

**A:** Yes. The format returned by this method matches what Import User-Role Assignments ([RC-API-56 — Import User-Role Assignments API](RC-API-56_Import-User-Role-Assignments.md)) expects. You can export assignments from one project and import them into another to replicate the role structure.

---

# 7. Common Mistakes & Gotchas

**Confusing this method with Export User Roles.** Export User Roles ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)) returns role *definitions* (what permissions each role has). This method returns role *assignments* (which users are in which role). Both are needed for a full picture of project access.

**Treating every row as a role member.** Users with individual permissions are in the response too, with a blank `unique_role_name`. Skip those rows when you only want role assignments, and before passing the export to Import User-Role Assignments.

**Interpreting `unique_role_name` directly.** The `unique_role_name` is a system ID (e.g., `U-527D39JXAC`), not a human-readable label. You need to cross-reference it against Export User Roles to get the `role_label`.

**Forgetting the User Rights permission.** This method requires both API Export and User Rights rights. Read-only User Rights access is sufficient (Full Access is not required).

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-API-22 — Export Users API](RC-API-22_Export-Users.md) (export full per-user permission sets)
- [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) (export role definitions and their privilege sets)
- [RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md) (create or update role definitions)
- [RC-API-56 — Import User-Role Assignments API](RC-API-56_Import-User-Role-Assignments.md) (assign users to roles via API)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (conceptual overview of roles and assignments)
