

**Import Users API**

| **Article ID** | [RC-API-23 — Import Users API](RC-API-23_Import-Users.md) |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Import Users behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Synonyms** | how do i import users via the api; import users api call; add users to a project and set permissions through the api; api method to assign user rights; bulk add existing users with the api; provision project access programmatically; api endpoint to import users; grant users permission flags via api |

---

## 1. Overview

The Import Users API method adds existing REDCap system users to your project and assigns them permissions. This method does not create new REDCap accounts; it adds users who already exist in your REDCap system to your project. The data payload is a JSON, CSV or XML array of user objects, each specifying a username and a set of permission flags (API access, record creation, deletion, per-instrument data entry and data export rights, and so on).

Use this method to programmatically onboard team members to a project, update user permissions in bulk, or integrate with external user management systems.

---

## 2. Permissions Required

To call this method, your API token must have **API Import/Update** privileges *and* **User Rights** set to **Full Access** in the project. A user with **Read Only** User Rights cannot import users.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 17.x, if you are assigned to a Data Access Group, you can only update users who are in your own DAG, and you cannot add new users to the project. 16.0.61 does not apply this limit. If you are in a DAG on 17.x and need to add users, ask a project user who is not assigned to a DAG (or your REDCap administrator) to run the import.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. |
| `content` | Required | Always `'user'` for this method. |
| `format` | Optional | Data format: `'csv'`, `'json'`, `'xml'` (default). |
| `data` | Required | Array of user objects in the specified format. See Section 3.1 for full attribute reference and Section 4 for format examples. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, `'xml'`. Defaults to the value of `format`, or `'xml'` if `format` is not provided. Not applicable when using background processing. |

### 3.1 The `data` attribute

Each user object may include the following attributes:

`username`, `expiration`, `data_access_group`, `design`, `alerts`, `user_rights`, `data_access_groups`, `reports`, `stats_and_charts`, `manage_survey_participants`, `calendar`, `data_import_tool`, `data_comparison_tool`, `logging`, `email_logging`, `file_repository`, `data_quality_create`, `data_quality_execute`, `api_export`, `api_import`, `api_modules`, `mobile_app`, `mobile_app_download_data`, `record_create`, `record_rename`, `record_delete`, `lock_records_customization`, `lock_records`, `lock_records_all_forms`, `forms`, `forms_export`

Note the distinction between `data_access_group` (contains the unique DAG name to assign the user to a DAG) and `data_access_groups` (boolean flag for whether the user has access to the Data Access Groups page).

**There is no project-wide `data_export` attribute.** If you send `data_export`, it is ignored without an error. Data export rights are set per instrument with `forms_export`. Attributes that appear only in Export Users output, such as the user's email, first and last name, and the DAG ID or label, are also ignored on import.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 17.x, when Clinical Data Interoperability Services are enabled, `redcap_share` can also be imported. Check Export Users output on your own instance to see which attributes it uses.

**Behavior for missing attributes:**

- **New user being added** — any attribute not provided will automatically receive the minimum privilege (typically `0` = No Access).
- **Existing user being updated** — most attributes you leave out are left unchanged, with three important exceptions:
  - **`expiration`** — if omitted, the user's existing expiration date is cleared.
  - **`data_access_group`** — if omitted, the user is removed from their DAG.
  - **`forms` / `forms_export`** — if you send either one, any instrument you do not list is set to **No Access** for that right.

**Best practice for updates:** export the user first with [RC-API-22 — Export Users API](RC-API-22_Export-Users.md), change only the values you need, and send the full row back. This keeps the expiration date, DAG assignment and every instrument's rights intact.

**Attribute value key:**

| Attribute | Values |
|---|---|
| `expiration` | Date in `YYYY-MM-DD` format; blank = no expiration |
| `data_access_group` | The unique DAG name (for example `site_a`), not the DAG ID or label; blank = not in a DAG |
| `user_rights` | `0` = No Access, `1` = Full Access, `2` = Read Only |
| `lock_records` | `0` = No Access, `1` = Locking/Unlocking, `2` = Locking/Unlocking with E-signature authority |
| `forms_export` (per instrument) | `0` = No Access, `1` = Full Data Set, `2` = De-Identified, `3` = Remove Identifier Fields |
| `forms` — form-level rights (REDCap < 15.6) | `0` = No Access, `1` = View & edit records (survey responses read-only), `2` = Read Only, `3` = Edit Survey Responses |
| `forms` — form-level rights (REDCap ≥ 15.6) | `128` = No Access, `129` = Read Only, `130` = View & edit records (survey responses read-only); add `8` to also grant Edit Survey Responses; add `16` to also grant Delete |
| All other permission attributes | `0` = No Access, `1` = Access |

Both the legacy `0`–`3` values and the `128`-based values are accepted for `forms`.

---

## 4. Data Format Examples

These examples show the structure of the `data` payload for each format.

### 4.1 JSON

```json
[
  {
    "username": "harrispa",
    "expiration": "",
    "data_access_group": "",
    "design": "1",
    "user_rights": "1",
    "data_access_groups": "1",
    "reports": "1",
    "stats_and_charts": "1",
    "manage_survey_participants": "1",
    "calendar": "1",
    "data_import_tool": "1",
    "data_comparison_tool": "1",
    "logging": "1",
    "file_repository": "1",
    "data_quality_create": "1",
    "data_quality_execute": "1",
    "api_export": "1",
    "api_import": "1",
    "api_modules": "1",
    "mobile_app": "1",
    "mobile_app_download_data": "0",
    "record_create": "1",
    "record_rename": "0",
    "record_delete": "0",
    "lock_records_all_forms": "0",
    "lock_records": "0",
    "lock_records_customization": "0",
    "forms": {"demographics": "1", "day_3": "1", "other": "1"},
    "forms_export": {"demographics": "1", "day_3": "0", "other": "2"}
  },
  {
    "username": "taylorr4",
    "expiration": "2015-12-07",
    "data_access_group": "",
    "design": "0",
    "user_rights": "0",
    "data_access_groups": "0",
    "reports": "1",
    "stats_and_charts": "1",
    "manage_survey_participants": "1",
    "calendar": "1",
    "data_import_tool": "0",
    "data_comparison_tool": "0",
    "logging": "0",
    "file_repository": "1",
    "data_quality_create": "0",
    "data_quality_execute": "0",
    "api_export": "0",
    "api_import": "0",
    "api_modules": "0",
    "mobile_app": "0",
    "mobile_app_download_data": "0",
    "record_create": "1",
    "record_rename": "0",
    "record_delete": "0",
    "lock_records_all_forms": "0",
    "lock_records": "0",
    "lock_records_customization": "0",
    "forms": {"demographics": "1", "day_3": "2", "other": "0"},
    "forms_export": {"demographics": "1", "day_3": "0", "other": "2"}
  }
]
```

### 4.2 CSV

```
username,design,user_rights,forms,forms_export
harrispa,1,1,"demographics:1,day_3:1,other:1","demographics:1,day_3:0,other:2"
taylorr4,0,0,"demographics:1,day_3:2,other:0","demographics:1,day_3:2,other:0"
```

### 4.3 XML

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<users>
  <item>
    <username>harrispa</username>
    <expiration>2015-12-07</expiration>
    <user_rights>1</user_rights>
    <design>0</design>
    <forms>
      <demographics>1</demographics>
      <day_3>2</day_3>
      <other>0</other>
    </forms>
    <forms_export>
      <demographics>1</demographics>
      <day_3>0</day_3>
      <other>2</other>
    </forms_export>
  </item>
</users>
```

> **Note:** The CSV and XML examples are partial rows. If these users already exist in the project, a row without `expiration` clears their expiration date, a row without `data_access_group` removes them from their DAG, and any instrument not listed in `forms` / `forms_export` is set to No Access. See the best practice in Section 3.1.

---

## 5. Request Examples

In these examples, `site_a` stands for the unique DAG name of a Data Access Group in your project. Leave `data_access_group` blank if the user should not be in a DAG.

### 5.1 Python
```python
from config import config
import requests, json

record = {
    'username':                 'test_user_47',
    'expiration':               '2027-12-31',
    'data_access_group':        'site_a',
    'mobile_app':               1,
    'mobile_app_download_data': 1,
    'lock_records_all_forms':      1,
    'lock_records':                1,
    'lock_records_customization':  1,
    'record_delete':               1,
    'record_rename':               1,
    'record_create':               1,
    'api_import':                  1,
    'api_export':                  1,
    'api_modules':                 1,
    'data_quality_execute':        1,
    'data_quality_create':         1,
    'file_repository':             1,
    'logging':                     1,
    'data_comparison_tool':        1,
    'data_import_tool':            1,
    'calendar':                    1,
    'stats_and_charts':            1,
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

### 5.2 R
```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)
library(jsonlite)

record <- c(
	username='test_user_47',
	expiration='2027-12-31',
	data_access_group='site_a',
	mobile_app=1,
	mobile_app_download_data=1,
	lock_records_all_forms=1,
	lock_records=1,
	lock_records_customization=1,
	record_delete=1,
	record_rename=1,
	record_create=1,
	api_import=1,
	api_export=1,
	api_modules=1,
	data_quality_execute=1,
	data_quality_create=1,
	file_repository=1,
	logging=1,
	data_comparison_tool=1,
	data_import_tool=1,
	calendar=1,
	stats_and_charts=1,
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

### 5.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=user&format=json&data=[{\"username\":\"test_user_47\",\"expiration\":\"\",\"data_access_group\":\"site_a\",\"mobile_app\":\"0\",\"mobile_app_download_data\":\"0\",\"lock_records_all_forms\":\"0\",\"lock_records\":\"0\",\"lock_records_customization\":\"0\",\"record_delete\":\"0\",\"record_rename\":\"0\",\"record_create\":\"1\",\"api_import\":\"1\",\"api_export\":\"1\",\"api_modules\":\"1\",\"data_quality_execute\":\"1\",\"data_quality_create\":\"1\",\"file_repository\":\"1\",\"logging\":\"1\",\"data_comparison_tool\":\"1\",\"data_import_tool\":\"1\",\"calendar\":\"1\",\"stats_and_charts\":\"1\",\"reports\":\"1\",\"user_rights\":\"1\",\"design\":\"1\"}]"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

### 5.4 PHP
```php
<?php

include 'config.php';

$record = array(
	'username'                 => 'test_user_47',
	'expiration'               => '2027-12-31',
	'data_access_group'        => 'site_a',
	'mobile_app'               => '1',
	'mobile_app_download_data' => '1',
	'lock_records_all_forms'     => '1',
	'lock_records'               => '1',
	'lock_records_customization' => '1',
	'record_delete'              => '1',
	'record_rename'              => '1',
	'record_create'              => '1',
	'api_import'                 => '1',
	'api_export'                 => '1',
	'api_modules'                => '1',
	'data_quality_execute'       => '1',
	'data_quality_create'        => '1',
	'file_repository'            => '1',
	'logging'                    => '1',
	'data_comparison_tool'       => '1',
	'data_import_tool'           => '1',
	'calendar'                   => '1',
	'stats_and_charts'           => '1',
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5.

---

## 6. Response

On success, the API returns a count of users added or modified. For example: `2` means two users were imported (or their existing permissions were updated). Each added or updated user is recorded in the project's Logging.

The import is all-or-nothing: if any user in the request fails validation, REDCap returns an error and none of the users in the request are added or changed. Fix the reported problem and resend the whole request.

---

## 7. Common Questions

**Q: What if the username doesn't exist in the REDCap system?**

**A:** This method adds existing REDCap accounts to the project; it does not create accounts. Contact your REDCap administrator to create the account first.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 17.x, a username that does not exist in REDCap is rejected with an error, unless your administrator has enabled the Control Center setting that allows users to add usernames that do not yet exist in REDCap. 16.0.61 adds such usernames to the project without an error. On either version, check the spelling of each username before importing, and on 16.0.61 confirm afterwards that each account really exists.

**Q: Can I update a user's permissions with this method?**

**A:** Yes. If the user is already assigned to the project, sending their record again with different permission flags will update their permissions. The username is the unique key; REDCap matches on username and updates permissions if provided. Export the user first and send the full row back, because omitting `expiration`, `data_access_group` or instruments in `forms` / `forms_export` changes those settings (see Section 3.1).

**Q: Can I update a user who is assigned to a user role?**

**A:** No. A user who is assigned to a role gets their rights from the role, and Import Users returns an error for them. Change the role's rights with [RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md), or move the user to another role (or out of the role) with [RC-API-56 — Import User-Role Assignments API](RC-API-56_Import-User-Role-Assignments.md). To find out who is in a role, use [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md).

**Q: How do I give a user data export rights?**

**A:** Set them per instrument with `forms_export`, for example `"forms_export": {"demographics": "1", "day_3": "2"}` (`1` = Full Data Set, `2` = De-Identified, `3` = Remove Identifier Fields, `0` = No Access). The older project-wide `data_export` attribute is ignored.

**Q: What is the `expiration` field?**

**A:** An optional date in YYYY-MM-DD format when the user's access expires. After this date, the user's access to the project becomes inactive. Leave it blank for no expiration. When updating an existing user, include their current expiration date if you want to keep it: omitting the field clears it.

**Q: Can I import multiple users at once?**

**A:** Yes. The `data` parameter accepts an array of user objects. Send as many user objects as needed in a single call, and they will all be imported or updated. If any one of them fails, none are imported (see Section 6).

**Q: Do I need to include all permission fields?**

**A:** It depends on whether the user is new or already in the project. For a **new user**, any attribute you omit will be set to the minimum privilege (typically `0` = No Access). For an **existing user**, most omitted attributes are left as they are, but an omitted `expiration` is cleared, an omitted `data_access_group` removes the user from their DAG, and any instrument left out of `forms` / `forms_export` is set to No Access. In both cases, `username` is always required. For updates, the safest approach is to export the user, edit the values, and send the full row back.

---

## 8. Common Mistakes & Gotchas

**Assuming this method creates REDCap accounts.** It does not. The username must already exist in the REDCap system. Only project-level access is granted by this method. Coordinate with your REDCap administrator to ensure user accounts exist before importing.

**Sending a partial row to update one right.** On an existing user, a row with only `username` and the right you want to change also clears the expiration date, removes the user from their DAG, and (if `forms` or `forms_export` is included) sets unlisted instruments to No Access. Export the user, change the value, and send the full row back.

**Using `data_export` to set export rights.** It is ignored. Use `forms_export` per instrument.

**Sending a DAG ID or label in `data_access_group`.** Use the unique DAG name (for example `site_a`), as shown in Export DAGs output, not a number.

**Trying to update a user who is in a role.** Users assigned to a role cannot be updated with this method. Use [RC-API-56 — Import User-Role Assignments API](RC-API-56_Import-User-Role-Assignments.md) or change the role itself.

**Sending invalid JSON.** Ensure the data parameter is valid JSON (or CSV). Invalid JSON will cause the API to reject the request with a parsing error. Test your JSON in a validator before submitting.

**Forgetting the User Rights permission.** This method requires API Import/Update and User Rights set to Full Access. If your token's user has no User Rights, or only Read Only, the import will fail. Verify your rights on the User Rights page.

**Setting expiration dates in the wrong format.** Always use YYYY-MM-DD, for example `'2026-12-31'`, not `'12/31/2026'`. Other formats are not reliably rejected and may be misread as a different date. After importing, check the expiration date on the User Rights page or with Export Users.

---

## 9. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (explains the three access tiers and role-based access)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (complete reference for all permission names and meanings)
- [RC-API-22 — Export Users API](RC-API-22_Export-Users.md) (retrieve user list and current permissions)
- [RC-API-24 — Delete Users API](RC-API-24_Delete-Users.md) (remove users from a project)
- [RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md) (create or update user roles and their rights)
- [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md) (see which users are assigned to which role)
- [RC-API-56 — Import User-Role Assignments API](RC-API-56_Import-User-Role-Assignments.md) (assign users to roles, or remove them from a role)
