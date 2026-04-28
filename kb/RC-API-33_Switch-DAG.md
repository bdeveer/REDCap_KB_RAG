RC-API-33

**Switch DAG API**

| **Article ID** | RC-API-33 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects with Data Access Groups enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-DAG-01 — Data Access Groups; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The Switch DAG API method allows the current API user to switch (assign, reassign, or unassign) their active Data Access Group context — but only if they have been assigned to multiple DAGs via the DAG Switcher page in the project. By switching to a specific DAG, the user limits their data view and entry to that group only. Passing an empty string for `dag` unassigns the user, switching them to an all-DAGs view. Use this method to automate DAG context switching in workflows or support multi-site data entry scenarios.

Caution: This method only works for users who have been set up with multiple DAG assignments via the DAG Switcher page. Users with a single fixed DAG assignment cannot use this method to change their context.

---

# 2. Key Concepts & Definitions

### Data Access Group (DAG)
A data isolation mechanism in REDCap that restricts which records a user can access. Users assigned to a DAG can only view and edit records belonging to that group.

### Unique Group Name
The system identifier for a DAG (e.g., `'group_1'`, `'boston_site'`), distinct from the human-readable display label. The `dag` parameter always requires the unique group name, not the display label.

### DAG Switching
The ability for a user to temporarily change their active DAG context to view and edit a different group's data. This is distinct from DAG assignment — a user can only switch to DAGs they are assigned to.

### All-DAGs View
A context in which the user can access records from all Data Access Groups in the project. This is activated by passing an empty string to the `dag` parameter.

### DAG Switcher Page
A REDCap administrative interface where administrators designate which users can switch between DAGs. Only users listed on this page can use the Switch DAG API method.

### API Import/Update Privilege
A permission that allows the API token user to perform write operations. While named for "import/update," this privilege is also required for the Switch DAG method (a context-switching operation).

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update privileges at the project level. |
| `content` | Required | Always `'dag'` for this method. |
| `action` | Required | Always `'switch'` for this method. |
| `dag` | Required | The unique group name of the DAG to switch to (e.g., `'group_1'`, `'boston_site'`). Pass an empty string to unassign (switch to all-DAGs view). |

---

# 4. Request Examples

## 4.1 Python
```python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'dag',
    'action': 'switch',
    'format': 'json',
    'dag': 'group_api'
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
    content='dag',
    action='switch',
    'dag'='group_api'
)
print(result)
```

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=dag&action=switch&format=json&dag=group_api"

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
	'content' => 'dag',
	'action'  => 'switch',
	'format'  => 'json',
	'dag'  => 'group_api'
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

> **Note:** CURLOPT_SSL_VERIFYPEER should be TRUE in production.

---

# 5. Response

On success, the API returns `"1"`. If the switch fails for any reason (wrong DAG name, insufficient permissions, user not set up for DAG switching), an error message is returned instead.

Example response:
```
1
```

---

# 6. Common Questions

**Q: What is the difference between switching a DAG and being assigned to a DAG?**

**A:** DAG assignment (via RC-API-32) determines which DAG(s) a user can access. DAG switching (this method) changes the user's current active context within their assigned DAG(s). A user can only switch to a DAG they are assigned to or to all-DAGs view if they have that permission.

**Q: How do I switch to all-DAGs view?**

**A:** Pass an empty string for the `dag` parameter (e.g., `'dag': ''`). This switches the user to a view where they can see data from all DAGs.

**Q: Can I switch to a DAG I'm not assigned to?**

**A:** No. You can only switch to a DAG you are assigned to. If you try to switch to an unassigned DAG, the operation will fail. Users with all-DAG permissions can switch to any DAG or back to all-DAGs view.

**Q: What is the unique group name for this parameter?**

**A:** The `dag` parameter requires the unique group name (e.g., `'group_1'`, `'boston_site'`), not the human-readable label. Use the Export DAGs method (RC-API-28) to find the correct unique names.

**Q: Do I need special permissions to use this method?**

**A:** Your API token must have API Import/Update privileges at the project level. Additionally, you must have been assigned to multiple DAGs via the DAG Switcher page in the project — users with a single fixed DAG assignment cannot use this method.

**Q: How do I know if I'm set up for DAG switching?**

**A:** Check whether you appear on the DAG Switcher page in the project (accessible via the left-hand menu under Data Access Groups). If you have only one DAG assignment or haven't been added to the Switcher, this method will fail. Your project administrator sets this up.

**Q: Is DAG switching persistent?**

**A:** The DAG context switch is typically session-based. If you switch via the API and then access the web interface, your switch context may or may not persist depending on how REDCap handles session state.

---

# 7. Common Mistakes & Gotchas

**Using the DAG display name instead of the unique group name.** The `dag` parameter requires the unique group name (e.g., `'group_1'`), not the human-readable label (e.g., `'Boston Site'`). Use the Export DAGs method (RC-API-28) to find the correct unique names.

**Trying to switch to a DAG you're not assigned to.** If your user account is assigned to DAG A but you try to switch to DAG B, the operation will fail. Ensure your assignment matches the switch target.

**Forgetting that DAG switching requires special rights.** Not all users have the ability to switch DAGs. If the API returns a permission error, contact your project administrator to enable DAG-switching rights for your account.

**Not realizing switching clears restrictions.** Switching to all-DAGs view (empty string) removes your data isolation and shows data from all groups. This is useful for administrators and managers but should be done intentionally.

**Confusing DAG switching with DAG assignment.** These are separate operations. Assignment (RC-API-32) sets which DAG(s) you can access. Switching (this method) changes your current active view. You cannot switch to DAGs you are not assigned to.

**Expecting the switch to affect other sessions or users.** DAG switching is specific to your current API session or the calling user's context. It does not affect other users or open sessions.

**Not checking if the DAG exists before switching.** If you try to switch to a non-existent DAG, the operation will fail. Export DAGs (RC-API-28) first to verify the DAG exists.

---

# 8. Related Articles

- RC-API-01 — REDCap API (foundational; required reading before using any API method)
- RC-DAG-01 — Data Access Groups (explains DAG concepts, structure, and configuration)
- RC-DE-09 — Data Entry with Data Access Groups (covers data entry constraints in DAG-enabled projects)
- RC-USER-03 — User Rights: Configuring User Privileges (reference for DAG-switching rights and user permissions)
- RC-API-28 — Export DAGs (retrieve DAG definitions and unique names)
- RC-API-29 — Import DAGs (create or update DAG definitions)
- RC-API-30 — Delete DAGs (remove DAG definitions)
- RC-API-31 — Export User-DAG Assignments (retrieve which DAGs users are assigned to)
- RC-API-32 — Import User-DAG Assignments (assign users to DAGs)
