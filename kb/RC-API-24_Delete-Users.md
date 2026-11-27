

**Delete Users API**

| **Article ID** | [RC-API-24 — Delete Users API](RC-API-24_Delete-Users.md) |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Delete Users behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Synonyms** | how do i delete users via the api; delete users api call; remove users from a project through the api; api method to revoke project access; bulk remove users with the api; terminate user access programmatically; api endpoint to delete users; remove usernames from a project via api |

---

## 1. Overview

The Delete Users API method removes users from a project. You provide a list of usernames to remove, and the API deletes their access to the project. Users are removed completely; their account in the REDCap system is not deleted (that requires administrator action), but their assignment to the project is terminated.

Deleting a user also removes:

- **Their API token for this project.** If you delete your own username, the token you are calling with stops working immediately.
- **Their user role and Data Access Group assignments.** The role and the DAG themselves stay in the project; only this user's assignment is removed.

Records, data and logging history are not touched. Each removed user is recorded in the project's Logging.

Use this method to offboard team members, automate user lifecycle management, or revoke access to former collaborators.

---

## 2. Permissions Required

To call this method, the user who owns the API token needs all three of these project rights:

| Right | Level needed |
|---|---|
| **API Import/Update** | Enabled |
| **User Rights** | **Full Access** (Read Only is not enough) |
| **Delete Records** | Enabled |

Without Delete Records the call is refused with `You do not have Delete Record privileges`.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 17.x, a caller who is assigned to a Data Access Group can only delete users in their own DAG; naming a user outside it makes the call fail (see Section 5). If a script must remove users across DAGs, run it with a token belonging to a user who is not assigned to a DAG.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. |
| `content` | Required | Always `'user'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `users[0]`, `users[1]`, ... | Required | Array of usernames to delete. Pass as `users[0]=username1&users[1]=username2`, etc. |
| `format` | Optional | `csv`, `json` (default) or `xml`. |
| `returnFormat` | Optional | Format of error messages: `csv`, `json` or `xml`. |

---

## 4. Request Examples

### 4.1 Python
```python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'user',
    'action': 'delete',
    'format': 'json',
    'users[0]': 'test_user_47'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

### 4.2 R
```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='user',
    action='delete',
    'users[0]'='test_user_47'
)
print(result)
```

### 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=user&action=delete&format=json&users[0]=test_user_47"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

### 4.4 PHP
```php
<?php

include 'config.php';

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'user',
	'action'  => 'delete',
	'format'  => 'json',
	'users'  => array('test_user_47'),
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

## 5. Response

On success, the API returns a count of users deleted. For example: `1` means one user was removed from the project.

If any username in the list is not a user in the project (or, on 17.x, is outside your Data Access Group), the API returns **HTTP 400** with an error listing the usernames it could not delete, and **nothing is deleted**, not even the valid usernames in the same call. Fix or remove the listed names and send the request again.

If no `users` array is sent, the call fails with an error.

---

## 6. Common Questions

**Q: Does this delete the user from the entire REDCap system?**

**A:** No. This method removes the user only from the specific project. The user's REDCap account remains active in the system and in other projects. To delete a user's entire REDCap account, an administrator must do so via the REDCap admin panel.

**Q: What if I try to delete a user who is not in the project?**

**A:** The API returns HTTP 400 with an error naming the username(s) that are not in the project, and no users are deleted from that call. Check the current user list with [RC-API-22 — Export Users API](RC-API-22_Export-Users.md) first, then resend with only valid usernames.

**Q: Can I delete the project owner?**

**A:** Yes. The API does not stop you from deleting the project creator, yourself or the last user with User Rights access, so this can lock everyone out of managing the project. Be cautious when deleting users with design or user_rights permissions, and make sure at least one user with User Rights Full Access remains assigned. Deleting yourself also invalidates the API token you are using.

**Q: Can I delete multiple users at once?**

**A:** Yes. Pass multiple users using array syntax: `users[0]=user1&users[1]=user2&users[2]=user3`. All users in the array are deleted in a single call. The call is all-or-nothing: if any one username is invalid, none of them are deleted.

**Q: What happens to the user's role and DAG?**

**A:** The user's role assignment and Data Access Group assignment are removed with them. The role itself, and the DAG, remain in the project. To check who holds which role before deleting, see [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md).

**Q: Will this affect the user's data records?**

**A:** No. Deleting a user removes only their access to the project. Records they created or modified remain in the project. The user history (data logging) will still show their username as the person who created or edited records.

---

## 7. Common Mistakes & Gotchas

**Including one wrong username in a batch.** A single username that is not in the project makes the whole call fail with HTTP 400, and none of the other users are deleted. Read the error, which lists the bad names, and resend without them.

**Not realizing you can lock yourself out.** If you delete all users with User Rights access (including yourself), you may be unable to manage the project via the REDCap interface. Deleting yourself also removes your API token for the project, so any later calls in the same script fail. Coordinate with your REDCap administrator before deleting admin-level users.

**Missing one of the three rights.** This method requires API Import/Update, User Rights at Full Access, and Delete Records. Delete Records is off by default, even for the project creator, so it is the one most often missing.

**Username capitalization.** On 17.x, usernames are matched without regard to case, so `Test_User_47` deletes `test_user_47`.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 16.0.61 the username must match the case stored in the project exactly; a mismatch is treated as a username not in the project and the call fails with HTTP 400. Send usernames in lowercase so the same script works on both release lines.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (explains the three access tiers)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (reference for user permission types)
- [RC-API-22 — Export Users API](RC-API-22_Export-Users.md) (list current project users)
- [RC-API-23 — Import Users API](RC-API-23_Import-Users.md) (add users to the project)
- [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md) (see who holds which role before deleting)
