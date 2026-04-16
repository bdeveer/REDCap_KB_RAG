RC-API-22

**Export Users API**

| **Article ID** | RC-API-22 |
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

The Export Users API method retrieves a list of all users in a project and their associated permissions. This method returns user information in JSON or CSV format, including username, email, expiration date, and a complete set of permission flags that indicate what actions each user is allowed to perform (data export, API access, record creation, deletion, and so on).

Use this method to audit user access, generate reports of project team members, or integrate with external user management systems. The method returns all users currently assigned to the project, regardless of their assigned role.

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5.

---

# 5. Response

On success, the method returns an array (JSON, CSV, or XML) of user objects. Each object includes the user's profile fields and a complete set of permission flags. The `forms` attribute is the only attribute with sub-elements — one entry per data collection instrument, each with its own Form Rights value.

## 5.1 Returned attributes

`username`, `email`, `firstname`, `lastname`, `expiration`, `data_access_group`, `design`, `alerts`, `user_rights`, `data_access_groups`, `data_export`, `reports`, `stats_and_charts`, `manage_survey_participants`, `calendar`, `data_import_tool`, `data_comparison_tool`, `logging`, `email_logging`, `file_repository`, `data_quality_create`, `data_quality_execute`, `api_export`, `api_import`, `api_modules`, `mobile_app`, `mobile_app_download_data`, `record_create`, `record_rename`, `record_delete`, `lock_records_customization`, `lock_records`, `lock_records_all_forms`, `forms`, `forms_export`

## 5.2 Attribute value key

| Attribute | Values |
|---|---|
| `data_export` | `0` = No Access, `1` = Full Data Set, `2` = De-Identified, `3` = Remove Identifier Fields |
| Form-level rights (REDCap < 15.6) | `0` = No Access, `1` = View & edit records (survey responses read-only), `2` = Read Only, `3` = Edit Survey Responses |
| Form-level rights (REDCap ≥ 15.6) | `128` = No Access, `129` = Read Only, `130` = View & edit records (survey responses read-only); add `8` to also grant Edit Survey Responses; add `16` to also grant Delete |
| All other permission attributes | `0` = No Access, `1` = Access |

See RC-USER-03 for a full explanation of each permission name.

---

# 6. Common Questions

**Q: How can I export just one user instead of all users?**

**A:** The Export Users method always returns all users in the project. To extract a single user, filter the API response in your code using the username field.

**Q: What's the difference between `data_export` and `api_export`?**

**A:** `data_export` allows the user to export data via the REDCap interface (Data Export tool). `api_export` allows the user to call API methods that export data. A user may have one permission but not the other.

**Q: Are expired users included in the export?**

**A:** Yes. Users whose account has expired (if an expiration date was set) are still included in the export. The `expiration` field indicates the date the account expires or becomes inactive. Check this field to identify expired accounts.

**Q: Can I see which role a user is assigned to?**

**A:** The Export Users method returns each user's individual permission flags, but not the role name if the user is role-based. To see role assignments, use the Export User-DAG Assignments method (RC-API-31) to see DAG assignments, and export the user roles separately using Export User Roles (RC-API-25).

---

# 7. Common Mistakes & Gotchas

**Forgetting that two privileges are required, not one.** This method requires both API Export *and* User Rights privileges. Having API Export alone is not enough — the call will fail with an authentication error if User Rights access (Full or Read Only) is absent.

**Assuming the export returns only active users.** Users with expired accounts remain in the export. Your code must check the `expiration` field to identify and filter out expired users if needed.

**Forgetting that permission flags are integers, not booleans.** Permission values are `0` (false/not granted) or `1` (true/granted). Do not compare them using boolean `true`/`false` in your code — compare to `0` or `1`.

**Using the wrong format parameter.** If your code expects CSV but you request JSON (or vice versa), parsing will fail. Specify the correct `format` parameter and parse the response accordingly.

**Attempting to export users from a project where you lack API Export right.** If your API token does not include the API Export right, the method will fail with an authentication error. Verify your token permissions in the API Credentials settings.

---

# 8. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (explains the three access tiers and role-based access)
- RC-USER-03 — User Rights: Configuring User Privileges (complete reference for all permission names and meanings)
- RC-API-23 — Import Users (create and modify users via API)
- RC-API-24 — Delete Users (remove users from a project via API)
- RC-API-25 — Export User Roles (export custom role definitions)
