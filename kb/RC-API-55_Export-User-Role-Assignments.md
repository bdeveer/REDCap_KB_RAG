RC-API-55

**Export User-Role Assignments API**

| **Article ID** | RC-API-55 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API official documentation |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-25 — Export User Roles; RC-API-56 — Import User-Role Assignments; RC-USER-01 — User Rights: Overview & Three-Tier Access |

---

# 1. Overview

The Export User-Role Assignments API method retrieves the current mapping between users and their assigned roles in a project. Each record in the response contains a username and the `unique_role_name` of the role they are assigned to. Users who are not assigned to any role are not included in the response.

Use this method to audit which users belong to which roles, verify role assignments before making changes, or build external reporting on project access structure.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export and User Rights rights (Full Access or Read Only). |
| `content` | Required | Always `'userRoleMapping'` for this method. |
| `format` | Optional | Return format: `'csv'`, `'json'`, or `'xml'` (default). |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not specified, or `'xml'` if neither is provided. Does not apply when using background processing. |

---

# 3. Request Examples

## 3.1 Python
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

## 3.2 R
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

## 3.3 cURL
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

## 3.4 PHP
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5.

---

# 4. Response

On success, the method returns the list of user-role assignments in the requested format. Each record contains two fields:

- `username` — The REDCap username of the assigned user.
- `unique_role_name` — The system-generated role ID the user is assigned to (e.g., `U-527D39JXAC`). Use the Export User Roles method (RC-API-25) to look up what role name and privileges correspond to each ID.

Users who have no role assignment are not included in the response.

---

# 5. Common Questions

**Q: What's the difference between this method and Export Users?**

**A:** Export Users (RC-API-22) returns each user's full permission set as currently configured. Export User-Role Assignments returns only the username-to-role mapping — which role each user is assigned to. If you need to know a user's effective permissions, use Export Users. If you need to know which users belong to which role templates, use this method.

**Q: How do I find out what permissions a role grants?**

**A:** Use Export User Roles (RC-API-25) to retrieve role definitions. Cross-reference the `unique_role_name` from this method's response against the role list to see the full permission set.

**Q: Are users without a role assignment included?**

**A:** No. Only users currently assigned to a role are returned. Users with individually-set permissions (not via a role) will not appear in this export.

**Q: Can I use this export to feed an import?**

**A:** Yes. The format returned by this method matches what Import User-Role Assignments (RC-API-56) expects. You can export assignments from one project and import them into another to replicate the role structure.

---

# 6. Common Mistakes & Gotchas

**Confusing this method with Export User Roles.** Export User Roles (RC-API-25) returns role *definitions* (what permissions each role has). This method returns role *assignments* (which users are in which role). Both are needed for a full picture of project access.

**Expecting users without roles to appear.** If a user has direct individual permissions rather than a role assignment, they will not appear in this export. Use Export Users (RC-API-22) to capture all users regardless of assignment method.

**Interpreting `unique_role_name` directly.** The `unique_role_name` is a system ID (e.g., `U-527D39JXAC`), not a human-readable label. You need to cross-reference it against Export User Roles to get the `role_label`.

**Forgetting the User Rights permission.** This method requires both API Export and User Rights rights. Read-only User Rights access is sufficient (Full Access is not required).

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-API-22 — Export Users (export full per-user permission sets)
- RC-API-25 — Export User Roles (export role definitions and their privilege sets)
- RC-API-26 — Import User Roles (create or update role definitions)
- RC-API-56 — Import User-Role Assignments API (assign users to roles via API)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (conceptual overview of roles and assignments)
