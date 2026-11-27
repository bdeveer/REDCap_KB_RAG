---
id: RC-API-26
title: Import User Roles API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — user role
  import behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
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
- how do i import user roles via the api
- import user roles api call
- create or update custom roles through the api
- api method to define role permission templates
- bulk add user roles with the api
- configure role labels and permissions programmatically
- api endpoint to import user roles
- set up role templates in a project via api
---

# 1. Overview

The Import User Roles API method creates new custom user roles or updates existing roles in your project. A user role is a template that bundles a set of permissions together and assigns a human-readable label. The data payload is a JSON or CSV array of role objects, each specifying a role label and a set of permission flags.

Use this method to automate role management, create role templates programmatically, or integrate role definitions from external governance systems.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import and full User Rights access (Read Only User Rights is not enough). |
| `content` | Required | Always `'userRole'` for this method. |
| `format` | Optional | Data format: `'csv'`, `'json'`, or `'xml'` (default). |
| `data` | Required | Array of role objects in the specified format. Each object must include `role_label` and permission flags. Include an existing `unique_role_name` to update that role; leave it blank to create a new one. See Section 2.1 for the full attribute list, value KEY, and format examples. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not specified, or `'xml'` if neither is provided. Does not apply when using background processing. |

## 2.1 Data Attribute Reference

All available attributes for the `data` payload:

`unique_role_name`, `role_label`, `design`, `alerts`, `user_rights`, `data_access_groups`, `reports`, `stats_and_charts`, `manage_survey_participants`, `calendar`, `data_import_tool`, `data_comparison_tool`, `logging`, `email_logging`, `file_repository`, `data_quality_create`, `data_quality_execute`, `api_export`, `api_import`, `api_modules`, `mobile_app`, `mobile_app_download_data`, `record_create`, `record_rename`, `record_delete`, `lock_records_customization`, `lock_records`, `lock_records_all_forms`, `forms`, `forms_export`

The `forms` attribute is the only one with sub-elements — it contains one entry per data collection instrument, each with its own Form Rights value.

**Value KEY:**

| Attribute | Value meanings |
|---|---|
| `forms_export` (per instrument) | 0 = No Access, 1 = Full Data Set, 2 = De-Identified, 3 = Remove Identifier Fields |
| `forms` (legacy, before v15.6) | 0 = No Access, 1 = View & Edit records (survey responses read-only), 2 = Read Only, 3 = Edit Survey Responses. Still accepted on import. |
| `forms` (from v15.6) | 128 = No Access, 129 = Read Only, 130 = View & Edit records (survey responses read-only). The extra rights apply to View & Edit only: 138 = View & Edit + Edit Survey Responses, 146 = View & Edit + Delete, 154 = View & Edit + Edit Survey Responses + Delete |
| All other attributes | 0 = No Access, 1 = Access (send numbers, not words like `yes`) |

Roles have no `data_export_tool` or `data_export` attribute; if you send one it is ignored. Export rights are set per instrument in `forms_export`.

> **Version caveat (16.0):** updating a role whose form rights use the newer values (128–154) may silently not save — the role is not counted in the returned number and no error is given. After updating a role on 16.0, check it on the User Rights page, or upgrade.

**Missing attribute behavior:**

- **New role**: any attribute not provided defaults to minimum privileges (0 = No Access; instruments not listed get No Access).
- **Existing role update**: any right flag not provided is reset to 0 (off) — it is **not** left unchanged. Only `forms` and `forms_export` are kept as they are if you omit them entirely; if you supply them partially, any instrument you don't list becomes No Access. The safe pattern is to export the role first ([RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)), change the values you need, and send back the full role.

**JSON example:**

```json
[{"unique_role_name":"U-2119C4Y87T","role_label":"Project Manager",
"design":"0","user_rights":"1","data_access_groups":"1","reports":"1","stats_and_charts":"1",
"manage_survey_participants":"1","calendar":"1","data_import_tool":"0","data_comparison_tool":"0","logging":"0",
"file_repository":"1","data_quality_create":"0","data_quality_execute":"0","api_export":"0","api_import":"0","api_modules":"0",
"mobile_app":"0","mobile_app_download_data":"0","record_create":"1","record_rename":"0","record_delete":"0",
"lock_records_customization":"0","lock_records":"0","lock_records_all_forms":"0",
"forms":{"demographics":"1","day_3":"2","other":"0"},"forms_export":{"demographics":"1","day_3":"2","other":"1"}}]
```

**CSV example:**

```
unique_role_name,role_label,design,user_rights,forms,forms_export
U-527D39JXAC,Data Entry Person,1,1,"demographics:1,day_3:1,other:1","demographics:1,day_3:2,other:0"
U-2119C4Y87T,Project Manager,0,0,"demographics:1,day_3:2,other:0","demographics:1,day_3:2,other:0"
```

**XML example:**

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<userRoles>
   <item>
      <unique_role_name>U-527D39JXAC</unique_role_name>
      <role_label>Data Entry Person</role_label>
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
</userRoles>
```

---

# 3. Request Examples

## 3.1 Python
```python
from config import config
import requests, json

# Updating an existing role: any right flag left out is reset to 0,
# so send the full role (export it first, change values, send it back).
record = {
    'unique_role_name'           : 'U-527D39JXAC',
    'role_label'                 : 'Project Manager',
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
    'forms'                      : {'demographics': 130, 'day_3': 130, 'other': 129},
    'forms_export'               : {'demographics': 1, 'day_3': 2, 'other': 0},
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

DATA="token=$API_TOKEN&content=userRole&format=json&data=[{\"unique_role_name\":\"U-2119C4Y87T\",\"role_label\":\"Project Manager\",\"mobile_app\":\"0\",\"mobile_app_download_data\":\"0\",\"lock_records_all_forms\":\"0\",\"lock_records\":\"0\",\"lock_records_customization\":\"0\",\"record_delete\":\"0\",\"record_rename\":\"0\",\"record_create\":\"1\",\"api_import\":\"1\",\"api_export\":\"1\",\"api_modules\":\"1\",\"data_quality_execute\":\"1\",\"data_quality_create\":\"1\",\"file_repository\":\"1\",\"logging\":\"1\",\"data_comparison_tool\":\"1\",\"data_import_tool\":\"1\",\"calendar\":\"1\",\"stats_and_charts\":\"1\",\"reports\":\"1\",\"user_rights\":\"1\",\"design\":\"1\"}]"

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5.

---

# 4. Response

On success, the API returns a count of roles created or modified. For example: `1` means one role was created or updated.

Badly formed JSON returns HTTP 200 with the body `The data is not in the specified format.` rather than an error status, so scripts should check the response body, not just the status code.

---

# 5. Common Questions

**Q: How do I update an existing role?**

**A:** Include the role's `unique_role_name` in your import data; the API updates that role's label and permissions. To create a new role, leave `unique_role_name` blank. A `unique_role_name` that does not exist in the project is rejected with HTTP 400 `Invalid Unique Role Names: …`, and nothing in that import is saved.

**Q: What is `unique_role_name`?**

**A:** A system-generated alphanumeric ID assigned by REDCap (e.g., `U-527D39JXAC`). It uniquely identifies a role and is used to reference the role in updates and deletions. Export existing roles to see their IDs.

**Q: Do I have to include all permission fields?**

**A:** It depends on whether you are creating or updating. For a **new role**, omitted fields default to minimum privileges (0 = No Access). For an **existing role** (identified by `unique_role_name`), yes in practice: every right flag you leave out is reset to 0 (off). Only `forms` and `forms_export` are kept if omitted entirely; if supplied partially, instruments not listed become No Access. Export the role first, change the values, and send back the full role. In both cases, `role_label` is always required.

**Q: Can I create a role with minimal permissions?**

**A:** Yes. For example, a read-only reviewer role could set every instrument to Read Only in `forms` and grant de-identified export in `forms_export`, leaving all other permissions at 0:

```json
[{"unique_role_name":"","role_label":"Read-only reviewer",
"forms":{"demographics":"129","day_3":"129","other":"129"},
"forms_export":{"demographics":"2","day_3":"2","other":"2"}}]
```

The role can view records and export de-identified data, but cannot create, edit or delete anything.

**Q: What happens if I import a role with the same label as an existing role but different ID?**

**A:** Two roles will exist with the same label. The `unique_role_name` is the primary key, not the label. To avoid confusion, ensure role labels are unique within your project.

---

# 6. Common Mistakes & Gotchas

**Sending a project-level export right.** Roles have no `data_export_tool` or `data_export` attribute; either is ignored and grants no export rights. Set export rights per instrument in `forms_export` (0 = No Access, 1 = Full Data Set, 2 = De-Identified, 3 = Remove Identifier Fields). Consult [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) for what each right means.

**Updating a role with a partial payload.** On an update, every right flag you leave out is reset to 0, and a partial `forms` or `forms_export` sets unlisted instruments to No Access. Export the role, edit it, and send back the full definition.

**Omitting `role_label`.** This field is required when creating a new role. If omitted, the import will fail. Ensure every role object in your data includes a label.

**Sending invalid JSON.** Ensure your data is valid JSON (or CSV). Badly formed JSON returns HTTP 200 with `The data is not in the specified format.` — check the response body, not just the status code. Flag values must be numeric (`0`/`1`, not `yes`/`no`).

**Forgetting the User Rights permission.** This method requires API Import and full User Rights access. A user with Read Only User Rights gets HTTP 400.

**Breaking Access Control Group compliance.** If the project uses Access Control Groups, an edit that would make users assigned to the role non-compliant is rejected. Adjust the role so its assigned users stay compliant, or reassign them first.

**Attempting to import roles with admin-level permissions without careful review.** Roles with `design` or `user_rights` permissions grant powerful access. Test such roles in a development project before deploying to production.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (explains role-based access)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (reference for permission field names)
- [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) (retrieve existing role definitions)
- [RC-API-27 — Delete User Roles API](RC-API-27_Delete-User-Roles.md) (remove roles from the project)
- [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md) (see which users are assigned to which roles)
- [RC-API-23 — Import Users API](RC-API-23_Import-Users.md) (assign individual users to the project)
