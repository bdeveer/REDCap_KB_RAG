RC-API-24

**Delete Users API**

| **Article ID** | RC-API-24 |
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

The Delete Users API method removes users from a project. You provide a list of usernames to remove, and the API deletes their access to the project. Users are removed completely; their account in the REDCap system is not deleted (that requires administrator action), but their assignment to the project is terminated.

Use this method to offboard team members, automate user lifecycle management, or revoke access to former collaborators.

---

# 2. Permissions Required

To call this method, your API token must have **API Import/Update** privileges *and* **User Rights** privileges in the project.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. |
| `content` | Required | Always `'user'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `users[0]`, `users[1]`, ... | Required | Array of usernames to delete. Pass as `users[0]=username1&users[1]=username2`, etc. |

---

# 4. Request Examples

## 4.1 Python
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

## 4.2 R
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

## 4.3 cURL
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

## 4.4 PHP
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5.

---

# 5. Response

On success, the API returns a count of users deleted. For example: `1` means one user was removed from the project. If a username does not exist in the project, it is ignored and does not affect the response.

---

# 6. Common Questions

**Q: Does this delete the user from the entire REDCap system?**

**A:** No. This method removes the user only from the specific project. The user's REDCap account remains active in the system and in other projects. To delete a user's entire REDCap account, an administrator must do so via the REDCap admin panel.

**Q: What if I try to delete a user who is not in the project?**

**A:** The API will ignore the username and not report an error. It simply has no user to delete. If you delete a user and the API returns 0, it means the user was not found in the project.

**Q: Can I delete the project owner?**

**A:** Technically yes, but this may lock you out of the project. Be cautious when deleting users with design or user_rights permissions, as you may lose the ability to manage the project. Ensure at least one administrator remains assigned.

**Q: Can I delete multiple users at once?**

**A:** Yes. Pass multiple users using array syntax: `users[0]=user1&users[1]=user2&users[2]=user3`. All users in the array will be deleted in a single call.

**Q: Will this affect the user's data records?**

**A:** No. Deleting a user removes only their access to the project. Records they created or modified remain in the project. The user history (data logging) will still show their username as the person who created or edited records.

---

# 7. Common Mistakes & Gotchas

**Expecting an error when deleting a non-existent user.** The API does not return an error if a username is not found in the project; it simply returns 0. Check the response count to verify that the expected number of users were deleted.

**Not realizing you can lock yourself out.** If you delete all users with admin rights (including yourself), you may be unable to manage the project via the REDCap interface. Coordinate with your REDCap administrator before deleting admin-level users.

**Forgetting the User Rights permission.** This method requires both API Import and User Rights rights. If your token lacks User Rights, the deletion will fail with an authentication error.

**Deleting users case-sensitively incorrectly.** Usernames are case-sensitive in REDCap. Ensure you use the exact username: `test_user_47` is different from `Test_User_47`. If the deletion returns 0, check username capitalization.

---

# 8. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (explains the three access tiers)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for user permission types)
- RC-API-22 — Export Users (list current project users)
- RC-API-23 — Import Users (add users to the project)
