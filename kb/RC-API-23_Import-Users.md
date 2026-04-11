RC-API-23

**Import Users API**

| **Article ID** | RC-API-23 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-USER-01 — User Rights: Overview & Three-Tier Access; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Import Users API method adds existing REDCap system users to your project and assigns them permissions. This method does not create new REDCap accounts; it adds users who already exist in your REDCap system to your project. The data payload is a JSON or CSV array of user objects, each specifying a username and a set of permission flags (data export, API access, record creation, deletion, and so on).

Use this method to programmatically onboard team members to a project, update user permissions in bulk, or integrate with external user management systems.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and User Rights rights. |
| `content` | Required | Always `'user'` for this method. |
| `format` | Optional | Data format: `'json'` (default) or `'csv'`. |
| `data` | Required | JSON or CSV array of user objects. Each object must include `username` and permission flags. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests, json

record = {
    'username':                 'test_user_47',
    'expiration':               '2016-01-01',
    'data_access_group':        1,
    'data_export':              1,
    'mobile_app':               1,
    'mobile_app_download_data': 1,
    'lock_record_multiform':    1,
    'lock_record':              1,
    'lock_record_customize':    1,
    'record_delete':            1,
    'record_rename':            1,
    'record_create':            1,
    'api_import':               1,
    'api_export':               1,
    'api_modules':              1,
    'data_quality_execute':     1,
    'data_quality_design':      1,
    'file_repository':          1,
    'data_logging':             1,
    'data_comparison_tool':     1,
    'data_import_tool':         1,
    'calendar':                 1,
    'graphical':                1,
    'reports':                  1,
    'user_rights':              1,
    'design':                   1,
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'user',
    'format': 'json',
    'data': data,
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
library(jsonlite)

record <- c(
	username='test_user_47',
	expiration='2016-01-01',
	data_access_group=1,
	data_export=1,
	mobile_app=1,
	mobile_app_download_data=1,
	lock_record_multiform=1,
	lock_record=1,
	lock_record_customize=1,
	record_delete=1,
	record_rename=1,
	record_create=1,
	api_import=1,
	api_export=1,
	api_modules=1,
	data_quality_execute=1,
	data_quality_design=1,
	file_repository=1,
	data_logging=1,
	data_comparison_tool=1,
	data_import_tool=1,
	calendar=1,
	graphical=1,
	reports=1,
	user_rights=1,
	design=1
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='user',
    format='json',
    data=data
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=user&format=json&data=[{\"username\":\"test_user_47\",\"expiration\":\"\",\"data_access_group\":\"1\",\"data_export\":\"0\",\"mobile_app\":\"0\",\"mobile_app_download_data\":\"0\",\"lock_record_multiform\":\"0\",\"lock_record\":\"0\",\"lock_record_customize\":\"0\",\"record_delete\":\"0\",\"record_rename\":\"0\",\"record_create\":\"1\",\"api_import\":\"1\",\"api_export\":\"1\",\"api_modules\":\"1\",\"data_quality_execute\":\"1\",\"data_quality_design\":\"1\",\"file_repository\":\"1\",\"data_logging\":\"1\",\"data_comparison_tool\":\"1\",\"data_import_tool\":\"1\",\"calendar\":\"1\",\"graphical\":\"1\",\"reports\":\"1\",\"user_rights\":\"1\",\"design\":\"1\"}]"

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

$record = array(
	'username'                 => 'test_user_47',
	'expiration'               => '2016-01-01',
	'data_access_group'        => '1',
	'data_export'              => '1',
	'mobile_app'               => '1',
	'mobile_app_download_data' => '1',
	'lock_record_multiform'    => '1',
	'lock_record'              => '1',
	'lock_record_customize'    => '1',
	'record_delete'            => '1',
	'record_rename'            => '1',
	'record_create'            => '1',
	'api_import'               => '1',
	'api_export'               => '1',
	'api_modules'              => '1',
	'data_quality_execute'     => '1',
	'data_quality_design'      => '1',
	'file_repository'          => '1',
	'data_logging'             => '1',
	'data_comparison_tool'     => '1',
	'data_import_tool'         => '1',
	'calendar'                 => '1',
	'graphical'                => '1',
	'reports'                  => '1',
	'user_rights'              => '1',
	'design'                   => '1',
);

$data = json_encode( array( $record ) );

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'user',
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

# 4. Response

On success, the API returns a count of users added or modified. For example: `2` means two users were imported (or their existing permissions were updated).

---

# 5. Common Questions

**Q: What if the username doesn't exist in the REDCap system?**

**A:** The API will fail and return an error. The username must already be a valid REDCap system account. This method adds existing users to the project; it does not create new REDCap accounts. Contact your REDCap administrator to create the account first.

**Q: Can I update a user's permissions with this method?**

**A:** Yes. If the user is already assigned to the project, sending their record again with different permission flags will update their permissions. The username is the unique key; REDCap matches on username and updates permissions if provided.

**Q: What is the `expiration` field?**

**A:** An optional date in YYYY-MM-DD format when the user's access expires. After this date, the user account for the project becomes inactive. Omit this field or leave it blank for no expiration.

**Q: Can I import multiple users at once?**

**A:** Yes. The `data` parameter accepts an array of user objects. Send as many user objects as needed in a single call, and they will all be imported or updated.

**Q: Do I need to include all permission fields?**

**A:** No. Include only the fields you want to set. Omitted fields default to 0 (permission not granted). However, `username` is always required.

---

# 6. Common Mistakes & Gotchas

**Assuming this method creates REDCap accounts.** It does not. The username must already exist in the REDCap system. Only project-level access is granted by this method. Coordinate with your REDCap administrator to ensure user accounts exist before importing.

**Sending invalid JSON.** Ensure the data parameter is valid JSON (or CSV). Invalid JSON will cause the API to reject the request with a parsing error. Test your JSON in a validator before submitting.

**Forgetting the User Rights permission.** This method requires both API Import and User Rights rights. If your token lacks User Rights, the import will fail. Verify your token permissions in the API Credentials settings.

**Setting expiration dates in the wrong format.** The `expiration` field must be in YYYY-MM-DD format. Other formats will be rejected. For example, use `'2026-12-31'`, not `'12/31/2026'`.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (explains the three access tiers and role-based access)
- RC-USER-03 — User Rights: Configuring User Privileges (complete reference for all permission names and meanings)
- RC-API-22 — Export Users (retrieve user list and current permissions)
- RC-API-24 — Delete Users (remove users from a project)
- RC-API-26 — Import User Roles (assign users to custom roles)
