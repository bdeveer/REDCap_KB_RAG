RC-API-26

**Import User Roles API**

| **Article ID** | RC-API-26 |
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

The Import User Roles API method creates new custom user roles or updates existing roles in your project. A user role is a template that bundles a set of permissions together and assigns a human-readable label. The data payload is a JSON or CSV array of role objects, each specifying a role label and a set of permission flags.

Use this method to automate role management, create role templates programmatically, or integrate role definitions from external governance systems.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and User Rights rights. |
| `content` | Required | Always `'userRole'` for this method. |
| `format` | Optional | Data format: `'json'` (default) or `'csv'`. |
| `data` | Required | JSON or CSV array of role objects. Each must include `role_label` and permission flags. Optionally include `unique_role_name` to update an existing role. |

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests, json

record = {
    'unique_role_name'           : 'U-527D39JXAC',
    'role_label'                 : 'Project Manager',
    'data_access_group'          : 1,
    'data_export_tool'           : 1,
    'mobile_app'                 : 1,
    'mobile_app_download_data'   : 1,
    'lock_records_all_forms'     : 1,
    'lock_records'               : 1,
    'lock_records_customization' : 1,
    'record_delete'              : 1,
    'record_rename'              : 1,
    'record_create'              : 1,
    'api_import'                 : 1,
    'api_export'                 : 1,
    'api_modules'                : 1,
    'data_quality_execute'       : 1,
    'data_quality_create'        : 1,
    'file_repository'            : 1,
    'logging'                    : 1,
    'data_comparison_tool'       : 1,
    'data_import_tool'           : 1,
    'calendar'                   : 1,
    'stats_and_charts'           : 1,
    'reports'                    : 1,
    'user_rights'                : 1,
    'design'                     : 1,
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'userRole',
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
	'unique_role_name'='U-527D39JXAC',
    'role_label'='ProjectManager',
    'data_access_group'=1,
    'data_export_tool'=1,
    'mobile_app'=1,
    'mobile_app_download_data'=1,
    'lock_records_all_forms'=1,
    'lock_records'=1,
    'lock_records_customization'=1,
    'record_delete'=1,
    'record_rename'=1,
    'record_create'=1,
    'api_import'=1,
    'api_export'=1,
    'api_modules'=1,
    'data_quality_execute'=1,
    'data_quality_create'=1,
    'file_repository'=1,
    'logging'=1,
    'data_comparison_tool'=1,
    'data_import_tool'=1,
    'calendar'=1,
    'stats_and_charts'=1,
    'reports'=1,
    'user_rights'=1,
    'design'=1
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='userRole',
    format='json',
    data=data
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=userRole&format=json&data=[{\"unique_role_name\":\"U-2119C4Y87T\",\"role_label\":\"Project Manager\",\"data_access_group\":\"1\",\"data_export\":\"0\",\"mobile_app\":\"0\",\"mobile_app_download_data\":\"0\",\"lock_records_all_forms\":\"0\",\"lock_records\":\"0\",\"lock_records_customization\":\"0\",\"record_delete\":\"0\",\"record_rename\":\"0\",\"record_create\":\"1\",\"api_import\":\"1\",\"api_export\":\"1\",\"api_modules\":\"1\",\"data_quality_execute\":\"1\",\"data_quality_create\":\"1\",\"file_repository\":\"1\",\"logging\":\"1\",\"data_comparison_tool\":\"1\",\"data_import_tool\":\"1\",\"calendar\":\"1\",\"stats_and_charts\":\"1\",\"reports\":\"1\",\"user_rights\":\"1\",\"design\":\"1\"}]"

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
    'unique_role_name'           => 'U-527D39JXAC',
    'role_label'                 => 'Project Manager',
    'data_access_group'          => '1',
    'data_export_tool'           => '1',
    'mobile_app'                 => '1',
    'mobile_app_download_data'   => '1',
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
    'reports'                    => '1',
    'user_rights'                => '1',
    'design'                     => '1',
);

$data = json_encode( array( $record ) );

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'userRole',
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

On success, the API returns a count of roles created or modified. For example: `1` means one role was created or updated.

---

# 5. Common Questions

**Q: How do I update an existing role?**

**A:** Include the `unique_role_name` field in your import data. If the role ID exists, the API will update that role's label and permissions. If the ID is omitted or does not exist, a new role is created.

**Q: What is `unique_role_name`?**

**A:** A system-generated alphanumeric ID assigned by REDCap (e.g., `U-527D39JXAC`). It uniquely identifies a role and is used to reference the role in updates and deletions. Export existing roles to see their IDs.

**Q: Do I have to include all permission fields?**

**A:** No. Include only the permissions you want to set. Omitted fields default to 0 (not granted). However, `role_label` is always required.

**Q: Can I create a role with minimal permissions?**

**A:** Yes. For example, a read-only role could set `data_export=1` but leave all other permissions at 0. This restricts the role's abilities to only data export.

**Q: What happens if I import a role with the same label as an existing role but different ID?**

**A:** Two roles will exist with the same label. The `unique_role_name` is the primary key, not the label. To avoid confusion, ensure role labels are unique within your project.

---

# 6. Common Mistakes & Gotchas

**Confusing field names between role imports and user imports.** User permission fields sometimes differ from role permission fields. For example, roles use `data_export_tool` while users use `data_export`. Consult RC-USER-03 for the exact field names required for each operation.

**Omitting `role_label`.** This field is required when creating a new role. If omitted, the import will fail. Ensure every role object in your data includes a label.

**Sending invalid JSON.** Ensure your data is valid JSON (or CSV). Invalid syntax will cause the API to reject the request. Test your JSON in a validator.

**Forgetting the User Rights permission.** This method requires both API Import and User Rights rights. If your token lacks User Rights, the import will fail.

**Attempting to import roles with admin-level permissions without careful review.** Roles with `design` or `user_rights` permissions grant powerful access. Test such roles in a development project before deploying to production.

---

# 7. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (explains role-based access)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for permission field names)
- RC-API-25 — Export User Roles (retrieve existing role definitions)
- RC-API-27 — Delete User Roles (remove roles from the project)
- RC-API-23 — Import Users (assign individual users to the project)
