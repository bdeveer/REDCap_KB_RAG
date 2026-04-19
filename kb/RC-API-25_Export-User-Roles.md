RC-API-25

**Export User Roles API**

| **Article ID** | RC-API-25 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-USER-01 — User Rights: Overview & Three-Tier Access; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Export User Roles API method retrieves all custom user roles defined in your project. A user role is a template that bundles a set of permissions together and assigns a human-readable label. When users are assigned to a role, they inherit all permissions in that role. This method returns the role definitions, including the role's unique system ID, label, and all permission flags.

Use this method to audit role configurations, generate reports of role-based access structures, or export role definitions for use in other projects or systems.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export and User Rights rights. |
| `content` | Required | Always `'userRole'` for this method. |
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
    'content': 'userRole',
    'format': 'json'
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
    format='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=userRole&format=json"

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

On success, the method returns an array (or CSV table) of role objects in the requested format. Each object contains the following attributes:

`unique_role_name`, `role_label`, `design`, `alerts`, `user_rights`, `data_access_groups`, `reports`, `stats_and_charts`, `manage_survey_participants`, `calendar`, `data_import_tool`, `data_comparison_tool`, `logging`, `email_logging`, `file_repository`, `data_quality_create`, `data_quality_execute`, `api_export`, `api_import`, `api_modules`, `mobile_app`, `mobile_app_download_data`, `record_create`, `record_rename`, `record_delete`, `lock_records_customization`, `lock_records`, `lock_records_all_forms`, `forms`, `forms_export`

The `forms` attribute is the only one with sub-elements — it contains one entry per data collection instrument, each with its own Form Rights value.

**Value KEY:**

| Attribute | Value meanings |
|---|---|
| `data_export` | 0 = No Access, 1 = Full Data Set, 2 = De-Identified, 3 = Remove Identifier Fields |
| `forms` (legacy, before v15.6) | 0 = No Access, 1 = View & Edit records (survey responses read-only), 2 = Read Only, 3 = Edit Survey Responses |
| `forms` (from v15.6) | 128 = No Access, 129 = Read Only, 130 = View & Edit records (survey responses read-only); add 8 to also grant Edit Survey Responses; add 16 to also grant Delete rights |
| All other attributes | 0 = No Access, 1 = Access |

---

# 5. Common Questions

**Q: What's the difference between a role and a user?**

**A:** A role is a template; a user is an individual person. Roles define a reusable set of permissions. Users are assigned to roles and inherit those permissions. One role can be assigned to many users.

**Q: How do I know which role a user belongs to?**

**A:** The Export User Roles method shows role definitions, but not which users are assigned to which roles. To see user-to-role assignments, export all users (RC-API-22) and check their individual permission flags. Alternatively, examine the project's User Rights settings in the REDCap interface.

**Q: What does the `unique_role_name` look like?**

**A:** It's a system-generated alphanumeric ID assigned by REDCap when the role is created. Example: `U-527D39JXAC`. This ID is used to reference the role when importing or deleting roles via the API.

**Q: Can I export just one role?**

**A:** No. The Export User Roles method always returns all roles. To extract a single role, filter the response in your code using the `unique_role_name` or `role_label` field.

**Q: Are built-in roles (like 'Admin') included in the export?**

**A:** No. Only custom roles defined in the project are exported. Built-in REDCap roles (Admin, Standard User, etc.) are not returned by this method.

---

# 6. Common Mistakes & Gotchas

**Confusing role_label with unique_role_name.** The `unique_role_name` is a system ID (e.g., `U-527D39JXAC`); the `role_label` is the human-readable name (e.g., `'Project Manager'`). Use the correct field depending on whether you need the system ID or display name.

**Assuming permission fields match export fields exactly.** Some field names differ slightly between Export Users and Export User Roles. For example, Import User Roles uses `data_export_tool` instead of `data_export`. Consult RC-USER-03 for the exact field names.

**Forgetting the User Rights permission.** This method requires both API Export and User Rights rights. If your token lacks User Rights, the export will fail with an authentication error.

**Using exported roles to directly import to another project.** Role definitions exported from one project can be imported to another, but ensure the permission flags match your target project's configuration. Verify that the roles are compatible before importing.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (explains role-based access and the three tiers)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for permission field names and meanings)
- RC-API-22 — Export Users (export individual user permissions)
- RC-API-26 — Import User Roles (create or update custom roles)
- RC-API-27 — Delete User Roles (remove roles from the project)
- RC-API-55 — Export User-Role Assignments (see which users are assigned to which roles)
