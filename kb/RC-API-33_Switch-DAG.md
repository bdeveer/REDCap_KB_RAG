

**Switch DAG API**

| **Article ID** | [RC-API-33 — Switch DAG API](RC-API-33_Switch-DAG.md) |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects with Data Access Groups enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Switch DAG behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Synonyms** | how do i switch my dag via the api; switch dag api call; change my active data access group through the api; api method to set the current dag context; reassign or unassign my own dag programmatically; switch to an all-dags view via the api; api endpoint to switch data access group; change dag context for multi-site data entry via api |

---

## 1. Overview

The Switch DAG API method allows the current API user to switch (assign, reassign, or unassign) their active Data Access Group context — but only if they have been assigned to multiple DAGs via the DAG Switcher page in the project, meaning more than one DAG (or [No Assignment]) is enabled for them there. By switching to a specific DAG, the user limits their data view and entry to that group only. Passing an empty string for `dag` unassigns the user ("[No Assignment]", an all-DAGs view), but only if [No Assignment] is one of the user's allowed targets in the DAG Switcher. Use this method to automate DAG context switching in workflows or support multi-site data entry scenarios.

The switch is not limited to the API call or session. It changes the user's current DAG assignment in the project, exactly like using the DAG Switcher in the web interface: the user's web session and all later API calls see the new DAG until they switch again.

Caution: This method only works for users who have been set up with multiple DAG assignments via the DAG Switcher page — that is, the DAGs enabled for the user in the DAG Switcher. Users with a single fixed DAG assignment cannot use this method to change their context.

---

## 2. Key Concepts & Definitions

#### Data Access Group (DAG)
A data isolation mechanism in REDCap that restricts which records a user can access. Users assigned to a DAG can only view and edit records belonging to that group.

#### Unique Group Name
The system identifier for a DAG (e.g., `'group_1'`, `'boston_site'`), distinct from the human-readable display label. The `dag` parameter always requires the unique group name, not the display label.

#### DAG Switching
The ability for a user to temporarily change their active DAG context to view and edit a different group's data. This is distinct from DAG assignment — a user can only switch to DAGs they are assigned to.

#### All-DAGs View
A context in which the user can access records from all Data Access Groups in the project ("[No Assignment]" in the DAG Switcher). This is activated by passing an empty string (or `0`) to the `dag` parameter, and only works if [No Assignment] is enabled for the user in the DAG Switcher.

#### DAG Switcher Page
The part of the Data Access Groups page where users with the Data Access Groups right (not only administrators) designate which DAGs each user can switch between. Only users set up on this page can use the Switch DAG API method, and only for the DAGs enabled for them there.

#### API Import/Update Privilege
A permission that allows the API token user to perform write operations. While named for "import/update," this privilege is also required for the Switch DAG method (a context-switching operation).

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update privileges at the project level. |
| `content` | Required | Always `'dag'` for this method. |
| `action` | Required | Always `'switch'` for this method. |
| `dag` | Required | The unique group name of the DAG to switch to (e.g., `'group_1'`, `'boston_site'`). Pass an empty string (or `0`) to unassign (switch to [No Assignment], the all-DAGs view) — only allowed if [No Assignment] is one of your enabled targets in the DAG Switcher. |

---

## 4. Request Examples

### 4.1 Python
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
# Errors also return HTTP 200 -- check the body, not the status code
if r.text.strip() != '1':
    raise RuntimeError('DAG switch failed: ' + r.text)
```

### 4.2 R
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

### 4.3 cURL
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

### 4.4 PHP
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

## 5. Response

On success, the API returns `1`. If the switch fails, a plain-text error message is returned instead — **with HTTP status 200**, not an error status. Scripts must check that the response body is `1`; checking the status code alone will treat a failed switch as a success.

Example response:
```
1
```

Error responses:

| Response body | Meaning |
|---|---|
| `ERROR: Invalid DAG` | The `dag` value is not a unique group name in this project. |
| `ERROR: Invalid user` | The token's user could not be matched to a project user. |
| `ERROR: User/DAG assignment not permitted` | The target DAG (or [No Assignment]) is not enabled for this user in the DAG Switcher. |

Unlike Export, Import and Delete DAGs, this method works for users who are currently assigned to a DAG — that is the point of it.

---

## 6. Common Questions

**Q: What is the difference between switching a DAG and being assigned to a DAG?**

**A:** DAG assignment (via [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md)) determines which DAG(s) a user can access. DAG switching (this method) changes the user's current active context within their assigned DAG(s). A user can only switch to a DAG they are assigned to or to all-DAGs view if they have that permission.

**Q: How do I switch to all-DAGs view?**

**A:** Pass an empty string (or `0`) for the `dag` parameter (e.g., `'dag': ''`). This moves the user to [No Assignment], a view where they can see data from all DAGs — but only if [No Assignment] is one of the user's allowed targets in the DAG Switcher. Otherwise you get `ERROR: User/DAG assignment not permitted`.

**Q: Can I switch to a DAG I'm not assigned to?**

**A:** No. You can only switch to a DAG that is enabled for you in the DAG Switcher. There is no exception for users who currently see all DAGs, administrators included: anyone not set up in the DAG Switcher for the target DAG gets `ERROR: User/DAG assignment not permitted`.

**Q: What is the unique group name for this parameter?**

**A:** The `dag` parameter requires the unique group name (e.g., `'group_1'`, `'boston_site'`), not the human-readable label. Use the Export DAGs method ([RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md)) to find the correct unique names.

**Q: Do I need special permissions to use this method?**

**A:** Your API token must have API Import/Update privileges at the project level. Additionally, you must have been assigned to multiple DAGs via the DAG Switcher page in the project (the DAGs enabled for you there) — users with a single fixed DAG assignment cannot use this method.

**Q: How do I know if I'm set up for DAG switching?**

**A:** Check whether you appear on the DAG Switcher page in the project (accessible via the left-hand menu under Data Access Groups). If you have only one DAG assignment or haven't been added to the Switcher, this method will fail. Any user with the Data Access Groups right in the project can set this up.

**Q: Is DAG switching persistent?**

**A:** Yes. The switch is not per session or per API call: it changes your current DAG assignment in the project, exactly like using the DAG Switcher in the web interface. Your web session and all later API calls (with any of your access) see the new DAG until you switch again. Have scripts switch back to your usual DAG when they finish.

---

## 7. Common Mistakes & Gotchas

**Using the DAG display name instead of the unique group name.** The `dag` parameter requires the unique group name (e.g., `'group_1'`), not the human-readable label (e.g., `'Boston Site'`). Use the Export DAGs method ([RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md)) to find the correct unique names.

**Trying to switch to a DAG you're not assigned to.** If your user account is assigned to DAG A but you try to switch to DAG B, the operation will fail. Ensure your assignment matches the switch target.

**Forgetting that DAG switching requires special rights.** Not all users have the ability to switch DAGs. If the API returns a permission error, contact your project administrator to enable DAG-switching rights for your account.

**Not realizing switching clears restrictions.** Switching to all-DAGs view (empty string) removes your data isolation and shows data from all groups. This is useful for administrators and managers but should be done intentionally.

**Confusing DAG switching with DAG assignment.** These are separate operations. Assignment ([RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md)) sets which DAG(s) you can access. Switching (this method) changes your current active view. You cannot switch to DAGs you are not assigned to.

**Expecting the switch to stay inside the script.** The switch changes the user's DAG assignment in the project, not just the current API call. It does not affect other users, but it does affect that same user everywhere: if a script switches DAGs while the person is working in the browser, the records they see change under them. Switch back when the script finishes, and avoid running switching scripts under an account someone is actively using.

**Checking the HTTP status instead of the response body.** Errors come back with HTTP 200 and a text body such as `ERROR: User/DAG assignment not permitted`. Treat anything other than `1` as a failure.

**Not checking if the DAG exists before switching.** If you try to switch to a non-existent DAG, the operation will fail. Export DAGs ([RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md)) first to verify the DAG exists.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (foundational; required reading before using any API method)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (explains DAG concepts, structure, and configuration)
- [RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md) (covers data entry constraints in DAG-enabled projects)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (reference for DAG-switching rights and user permissions)
- [RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md) (retrieve DAG definitions and unique names)
- [RC-API-29 — Import DAGs API](RC-API-29_Import-DAGs.md) (create or update DAG definitions)
- [RC-API-30 — Delete DAGs API](RC-API-30_Delete-DAGs.md) (remove DAG definitions)
- [RC-API-31 — Export User-DAG Assignments API](RC-API-31_Export-User-DAG-Assignments.md) (retrieve which DAGs users are assigned to)
- [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md) (assign users to DAGs)
