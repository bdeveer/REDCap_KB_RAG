---
id: RC-API-27
title: Delete User Roles API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Delete
  User Roles behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.3'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
tags:
- api
synonyms:
- how do i delete user roles via the api
- delete user roles api call
- remove custom roles from a project through the api
- api method to delete role definitions by unique role name
- bulk delete user roles with the api
- remove role templates programmatically
- api endpoint to delete user roles
- delete a role and unassign its users via api
---

# 1. Overview

The Delete User Roles API method removes custom user roles from your project. You provide a list of role IDs (the `unique_role_name` values) to delete.

> **Unassign users first.** In the user interface REDCap **refuses** to delete a role that still has users assigned to it (see [RC-USER-02](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) §5 and [RC-USER-04](RC-USER-04_User-Rights-User-Management.md) §7); the role must be emptied first. This API method has **no such guard**: it deletes the role even if users are still assigned to it. Those users are left with no role and fall back to the individual rights stored on their own account from before they were put in the role, which may be more or less than the role granted. Move the role's users to another role or to deliberately set individual rights before you call this method.

Use this method to clean up unused roles, automate role lifecycle management, or revoke access granted through a specific role.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update and User Rights (full access, not Read Only), and the token's user must also have the Delete Records right. |
| `content` | Required | Always `'userRole'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `roles[0]`, `roles[1]`, ... | Required | Array of role IDs to delete (the `unique_role_name` values). Pass as `roles[0]=U-527D39JXAC&roles[1]=U-XXXXX`, etc. If `roles` is missing or is not sent as an array, the call returns HTTP 400. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'userRole',
    'action': 'delete',
    'format': 'json',
    'roles[0]': 'U-522RX7WM49'
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
    content='userRole',
    action='delete',
    'roles[0]'='U-522RX7WM49'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=userRole&action=delete&format=json&roles[0]=U-522RX7WM49"

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
	'content' => 'userRole',
	'action'  => 'delete',
	'format'  => 'json',
	'roles'  => array('U-522RX7WM49'),
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

# 4. Response

On success, the API returns a count of roles deleted. For example: `1` means one role was removed from the project.

If any role ID in the request does not exist in the project, the whole call fails with HTTP 400 and an error saying that one or more of the roles are not valid and no roles were deleted. Nothing in the call is deleted, including the valid IDs. Export the roles first ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)) and copy the exact `unique_role_name` values.

If the token's user lacks the Delete Records right, the call returns HTTP 403 with `You do not have Delete Record privileges`.

Deleting a role also removes any File Repository folder restriction tied to that role; those folders are no longer limited to the role.

---

# 5. Common Questions

**Q: What happens to users assigned to a deleted role?**

**A:** The role is removed, but the users are not deleted and the API does not stop you. They lose the permissions granted by that role and fall back to the individual rights stored on their account from before they were put in the role. That is not necessarily zero access: it can be broader or narrower than the role was. Reassign them to another role or set their individual rights deliberately, ideally before deleting the role.

**Q: What is the `unique_role_name`?**

**A:** It's the system-generated alphanumeric ID assigned to the role (e.g., `U-522RX7WM49`). To find this ID, export existing roles using the Export User Roles method ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)).

**Q: What if I try to delete a role that doesn't exist?**

**A:** The call fails with HTTP 400, saying one or more roles are not valid and no roles were deleted. This applies to the whole request: if one ID in a multi-role call is wrong, none of the roles are deleted. Correct the ID and send the call again.

**Q: Can I delete multiple roles at once?**

**A:** Yes. Pass multiple role IDs using array syntax: `roles[0]=U-XXXXX&roles[1]=U-YYYYY`. All roles in the array will be deleted in a single call.

**Q: Can I undo a role deletion?**

**A:** No. Role deletion is permanent. To restore a role, you must import it again using the Import User Roles method ([RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md)) with the same or similar definition.

---

# 6. Common Mistakes & Gotchas

**Deleting a role without reassigning its users.** Empty the role before calling this method. Use [RC-API-55 — Export User-Role Assignments](RC-API-55_Export-User-Role-Assignments.md) to list who is currently assigned, then move those users to another role or give them individual permissions. The interface blocks deletion of a populated role outright, but this API method does not: the call succeeds and the users silently fall back to whatever individual rights were stored on their accounts.

**Confusing role labels with role IDs.** The `unique_role_name` is the system ID (e.g., `U-522RX7WM49`), not the human-readable label (e.g., `'Project Manager'`). Use the ID, not the label, in the delete request.

**Including one wrong role ID in a batch.** A single role ID that does not exist makes the whole call fail with HTTP 400, and none of the roles in the request are deleted. Export the roles first and use the exact IDs; check the returned count matches the number you sent.

**Forgetting the User Rights or Delete Records right.** This method requires API Import/Update and full User Rights (Read Only is not enough). The token's user also needs the Delete Records right; without it the call returns HTTP 403 `You do not have Delete Record privileges`.

**Inadvertently deleting the wrong role.** Role IDs are alphanumeric and easy to mistype. Always verify the correct role ID by exporting existing roles before deletion.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (explains role-based access)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (reference for permission types)
- [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) (retrieve role definitions and their IDs)
- [RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md) (create or update roles)
- [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md) (see which users are assigned to which roles)
- [RC-API-22 — Export Users API](RC-API-22_Export-Users.md) (identify users and their permissions)
