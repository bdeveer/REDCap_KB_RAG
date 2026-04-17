RC-API-27

**Delete User Roles API**

| **Article ID** | RC-API-27 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-USER-01 — User Rights: Overview & Three-Tier Access; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Delete User Roles API method removes custom user roles from your project. You provide a list of role IDs (the `unique_role_name` values) to delete. This method deletes the role definition; users currently assigned to that role are not deleted, but they lose the role's permission template. If users need to retain access after role deletion, they must be reassigned to another role or have individual permissions set.

Use this method to clean up unused roles, automate role lifecycle management, or revoke access granted through a specific role.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and User Rights rights. |
| `content` | Required | Always `'userRole'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `roles[0]`, `roles[1]`, ... | Required | Array of role IDs to delete (the `unique_role_name` values). Pass as `roles[0]=U-527D39JXAC&roles[1]=U-XXXXX`, etc. |

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5.

---

# 4. Response

On success, the API returns a count of roles deleted. For example: `1` means one role was removed from the project. If a role ID does not exist in the project, it is ignored and does not affect the response.

---

# 5. Common Questions

**Q: What happens to users assigned to a deleted role?**

**A:** The role is removed, but the users are not deleted. However, they lose the permissions granted by that role. You must either reassign them to another role or set individual permissions to maintain their access.

**Q: What is the `unique_role_name`?**

**A:** It's the system-generated alphanumeric ID assigned to the role (e.g., `U-522RX7WM49`). To find this ID, export existing roles using the Export User Roles method (RC-API-25).

**Q: What if I try to delete a role that doesn't exist?**

**A:** The API ignores the role ID and does not report an error. If you delete a role and the API returns 0, it means the role was not found in the project.

**Q: Can I delete multiple roles at once?**

**A:** Yes. Pass multiple role IDs using array syntax: `roles[0]=U-XXXXX&roles[1]=U-YYYYY`. All roles in the array will be deleted in a single call.

**Q: Can I undo a role deletion?**

**A:** No. Role deletion is permanent. To restore a role, you must import it again using the Import User Roles method (RC-API-26) with the same or similar definition.

---

# 6. Common Mistakes & Gotchas

**Deleting a role without reassigning its users.** Users assigned to a deleted role will lose the permissions granted by that role. Before deleting a role in production, ensure that affected users are reassigned to alternative roles or given individual permissions. Consider running an export to identify affected users.

**Confusing role labels with role IDs.** The `unique_role_name` is the system ID (e.g., `U-522RX7WM49`), not the human-readable label (e.g., `'Project Manager'`). Use the ID, not the label, in the delete request.

**Expecting an error when deleting a non-existent role.** The API does not return an error if a role ID is not found; it simply returns 0. Check the response count to verify the expected number of roles were deleted.

**Forgetting the User Rights permission.** This method requires both API Import and User Rights rights. If your token lacks User Rights, the deletion will fail.

**Inadvertently deleting the wrong role.** Role IDs are alphanumeric and easy to mistype. Always verify the correct role ID by exporting existing roles before deletion.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (explains role-based access)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for permission types)
- RC-API-25 — Export User Roles (retrieve role definitions and their IDs)
- RC-API-26 — Import User Roles (create or update roles)
- RC-API-55 — Export User-Role Assignments (see which users are assigned to which roles)
- RC-API-22 — Export Users (identify users and their permissions)
