---
id: RC-API-22
title: Export Users API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.5.6 (Standard) — §3, §5, §7 live-tested via the API on
  a sandbox project (2026-10); Export Users behaviour (incl. rights) checked against
  source code on v17.6.5 / v17.3.31 / v16.0.61; other sections not re-tested live
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
- how do i export users via the api
- export users api call
- get the list of project users and permissions through the api
- api method to retrieve usernames and rights
- pull user permission flags with the api
- audit project users programmatically
- api endpoint to export users
- list who has access to a project via api
- forms_export in export users api
- where is data_export in export users api
---

# 1. Overview

The Export Users API method retrieves a list of all users in a project and their associated permissions. This method returns user information in JSON or CSV format, including username, email, expiration date, and a complete set of permission flags that indicate what actions each user is allowed to perform (data export, API access, record creation, deletion, and so on).

Use this method to audit user access, generate reports of project team members, or integrate with external user management systems. The method returns all users currently assigned to the project, regardless of their assigned role.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 17.x, if the token owner is assigned to a Data Access Group, the export lists only the users in that same DAG. On 16.0.61 the export lists all project users regardless of the token owner's DAG. If you need the complete user list on 17.x, use a token belonging to a user who is not assigned to a DAG.

> **Note:** If a user has been assigned to a user role, the method returns that user with the role's defined privileges — not any individually configured privileges.

---

# 2. Permissions Required

To call this method, your API token must have **API Export** privileges *and* **User Rights** privileges (Full Access or Read Only) in the project.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. |
| `content` | Required | Always `'user'` for this method. |
| `format` | Optional | Return format: `'csv'`, `'json'`, `'xml'` (default). |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, `'xml'`. Defaults to the value of `format`, or `'xml'` if `format` is not provided. Not applicable when using background processing. |

---

# 4. Request Examples

## 4.1 Python
```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'user',
    'format': 'json'
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
    format='json'
)
print(result)
```

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=user&format=json"

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

On success, the method returns an array (JSON, CSV, or XML) of user objects. Each object includes the user's profile fields and a complete set of permission flags. Two attributes have sub-elements, with one entry per data collection instrument: `forms` (each instrument's Form Rights value) and `forms_export` (each instrument's Data Export Rights value).

## 5.1 Returned attributes

`username`, `email`, `firstname`, `lastname`, `expiration`, `data_access_group`, `data_access_group_id`, `data_access_group_label`, `design`, `alerts`, `user_rights`, `data_access_groups`, `reports`, `stats_and_charts`, `manage_survey_participants`, `calendar`, `data_import_tool`, `data_comparison_tool`, `logging`, `email_logging`, `file_repository`, `data_quality_create`, `data_quality_execute`, `api_export`, `api_import`, `api_modules`, `mobile_app`, `mobile_app_download_data`, `record_create`, `record_rename`, `record_delete`, `lock_records_customization`, `lock_records`, `lock_records_all_forms`, `forms`, `forms_export`

> **Note:** The attribute set is not fixed. Some attributes appear only when the related feature is enabled on the server or in the project — for example `mobile_app` and `mobile_app_download_data`, `mycap_participants`, `data_quality_resolution`, `double_data`, and the randomization attributes (`random_*`). Parse the response by attribute name rather than assuming a fixed list or column order.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 17.x, a `redcap_share` attribute is also returned when Clinical Data Interoperability Services (CDIS) is enabled. If your script maps CSV columns by position, switch to mapping by header name before upgrading.

> **Note:** There is no project-level `data_export` attribute. Data export rights are set per instrument, so they are returned per instrument in `forms_export` (e.g. `{"demographics": 1, "lab_results": 0}`).

> **Note:** `data_access_group_id` (numeric DAG ID) and `data_access_group_label` (human-readable DAG name) are informational fields. REDCap uses `data_access_group` (the unique DAG name) as the functional key for DAG assignment.

## 5.2 Attribute value key

| Attribute | Values |
|---|---|
| `forms_export` (per instrument) | `0` = No Access, `1` = Full Data Set, `2` = De-Identified, `3` = Remove Identifier Fields |
| Form-level rights (REDCap < 15.6) | `0` = No Access, `1` = View & edit records (survey responses read-only), `2` = Read Only, `3` = Edit Survey Responses |
| Form-level rights (REDCap ≥ 15.6) | `128` = No Access, `129` = Read Only, `130` = View & edit records (survey responses read-only); add `8` to also grant Edit Survey Responses; add `16` to also grant Delete |
| `user_rights` | `0` = No Access, `1` = Full Access, `2` = Read Only |
| `lock_records` | `0` = Disabled, `1` = Locking / Unlocking, `2` = Locking / Unlocking with E-signature authority |
| All other permission attributes | `0` = No Access, `1` = Access |

See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) for a full explanation of each permission name.

---

# 6. Common Questions

**Q: How can I export just one user instead of all users?**

**A:** The Export Users method has no filter parameter; it returns every user the token can see (all project users, or on 17.x only the token owner's DAG if the owner is in a DAG — see §1). To extract a single user, filter the API response in your code using the username field.

**Q: What's the difference between `forms_export` and `api_export`?**

**A:** `forms_export` holds the user's data export rights per instrument, which apply to exports via the REDCap interface (and limit what API exports return). `api_export` allows the user to call API methods that export data. A user may have one permission but not the other.

**Q: Are expired users included in the export?**

**A:** Yes. Users whose account has expired (if an expiration date was set) are still included in the export. The `expiration` field indicates the date the account expires or becomes inactive. Check this field to identify expired accounts.

**Q: Can I see which role a user is assigned to?**

**A:** The Export Users method returns each user's effective permission flags (the role's rights for role members), but not the role name. To see which role each user is in, use the Export User-Role Assignments method ([RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md)). To see what each role grants, use Export User Roles ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)).

---

# 7. Common Mistakes & Gotchas

**Forgetting that two privileges are required, not one.** This method requires both API Export *and* User Rights privileges. Having API Export alone is not enough — the call fails with HTTP 400 if User Rights access (Full or Read Only) is absent.

**Assuming the export returns only active users.** Users with expired accounts remain in the export. Your code must check the `expiration` field to identify and filter out expired users if needed.

**Forgetting that permission flags are integers, not booleans.** Most permission values are `0` (not granted) or `1` (granted), but some take more values — `user_rights` and `lock_records` can be `2` (see §5.2). Do not compare them using boolean `true`/`false` in your code — compare to the specific integer.

**Using the wrong format parameter.** If your code expects CSV but you request JSON (or vice versa), parsing will fail. Specify the correct `format` parameter and parse the response accordingly.

**Attempting to export users from a project where you lack API Export right.** If your API token does not include the API Export right, the method fails with HTTP 403. Verify your token permissions in the API Credentials settings.

**Looking for a project-level `data_export` field.** Older scripts read `data_export` (or `data_export_tool`) for a user's export rights. Neither is returned: export rights are per instrument, in `forms_export`. When importing users or roles, set `forms_export` too — a role imported with only `data_export=2` kept No Access on every instrument.

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (explains the three access tiers and role-based access)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (complete reference for all permission names and meanings)
- [RC-API-23 — Import Users API](RC-API-23_Import-Users.md) (create and modify users via API)
- [RC-API-24 — Delete Users API](RC-API-24_Delete-Users.md) (remove users from a project via API)
- [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) (export custom role definitions)
- [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md) (see which role each user is assigned to)
