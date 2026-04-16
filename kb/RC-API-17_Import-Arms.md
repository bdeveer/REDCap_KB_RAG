RC-API-17

**Import Arms API**

| **Article ID** | RC-API-17 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-16 — Export Arms; RC-API-18 — Delete Arms |

---

# 1. Overview

The Import Arms API method creates or modifies arms in a longitudinal REDCap project. Each arm consists of an arm number and a name. You can use this method to add new arms or update the names of existing arms.

The `override` parameter controls behavior: when set to `0`, the method adds or modifies arms without deleting others; when set to `1`, all existing arms are deleted and replaced with the arms you provide.

> **Important:** This method is only available for projects in **Development status**. It will not work on projects in Production or Analysis/Cleanup status.

> **Important:** Arms exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project.

**Permissions required:** The API token used must have both **API Import/Update** privileges *and* **Project Design/Setup** privileges in the project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update *and* Project Design/Setup privileges. |
| `content` | Required | Always `'arm'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `format` | Required | `'csv'`, `'json'`, or `'xml'`. Default is `'xml'` if omitted. |
| `override` | Required | `0` = add/modify arms without deleting others (default); `1` = delete all existing arms and replace with provided arms. |
| `data` | Required | Arms to import, in the format specified by `format`. Each arm must have `arm_num` and `name`. |
| `returnFormat` | Optional | `'csv'`, `'json'`, or `'xml'` — specifies the format of error messages. Defaults to the value of `format` if not specified. Not applicable when using a background process (`backgroundProcess=true`), which always returns `success:true` or `success:false`. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests, json

record = {
    'arm_num': 1,
    'name': 'Arm 1'
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'arm',
    'action': 'import',
    'format': 'json',
    'override': 0,
    'data': data,
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 3.2 R

```r
source('config.R')
library(RCurl)
library(jsonlite)

record <- c(
	arm_num=1,
	name='Arm 1'
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='arm',
	action='import',
    format='json',
	override=0,
    data=data
)
print(result)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=arm&action=import&override=0&format=json&data=[{\"arm_num\":\"1\",\"name\":\"Arm%201\"}]"

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

$data = array(
	array(
		'arm_num' => 1,
		'name'    => 'Arm ABC'
	),
	array(
		'arm_num' => 2,
		'name'    => 'Arm XYZ'
	),
);

$data = json_encode($data);

$fields = array(
	'token'    => $GLOBALS['api_token'],
	'content'  => 'arm',
	'action'   => 'import',
	'format'   => 'json',
	'override' => 0,
	'data'     => $data,
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

On success, the method returns the **number of arms imported** as a plain integer. The HTTP status code will be 200.

Example response:
```
1
```

This number reflects how many arms were created or renamed, not the total number of arms in the project.

---

# 5. Common Questions

**Q: What is the difference between `override=0` and `override=1`?**

**A:** With `override=0`, the API adds new arms or updates the names of existing arms without touching other arms. With `override=1`, all existing arms are deleted first, then replaced with the arms you provide. Use `override=1` only if you want to completely rebuild the arm structure.

**Q: Can I use this method on a classic project?**

**A:** No. Arms are a longitudinal-only feature. This method will fail on classic projects.

**Q: What happens if I import an arm with an `arm_num` that already exists?**

**A:** With `override=0`, the existing arm's name will be updated to the name you provide. With `override=1`, the entire arm structure is replaced, so the old arm is deleted and the new one takes its place.

**Q: Can I have non-sequential arm numbers (e.g., 1, 3, 5)?**

**A:** Technically yes, but this is not recommended. REDCap expects arm numbers to be sequential integers starting from 1. Using non-sequential numbers may cause unexpected behavior in the UI and in other API methods.

**Q: What does `returnFormat` control?**

**A:** `returnFormat` controls the format of any *error* messages returned by the API. It is independent of the `format` parameter (which controls how you send your data). If you omit `returnFormat`, error messages will come back in whatever format you specified with `format`. This is useful when, for example, you are sending CSV data but want JSON-formatted errors for easier parsing.

**Q: Does this method work on a project that is in Production status?**

**A:** No. Import Arms is only available for projects in **Development status**. If your project has been moved to Production, you will need to request a temporary return to Development (if your institution allows it) before you can modify arms via the API.

---

# 6. Common Mistakes & Gotchas

**Calling Import Arms on a classic project.** Arms are a longitudinal-only feature. If your project is classic, this method will fail. Always confirm your project is longitudinal before calling this method.

**Forgetting to JSON-encode the `data` parameter.** The `data` parameter must be a valid JSON array of objects. It is not a plain string. Use `json.dumps()` in Python, `toJSON()` in R, or `json_encode()` in PHP to properly format it.

**Using `override=1` when you only want to add a new arm.** The `override=1` flag deletes all existing arms and replaces them. If you only want to add a single arm, use `override=0` instead.

**Assuming arm numbers start from 0.** ARM numbers in REDCap are 1-indexed: the first arm is arm 1, not arm 0. If you submit `arm_num: 0`, it may be interpreted as invalid.

**Calling Import Arms on a Production project.** This method only works when the project is in Development status. Calling it on a Production project will fail. Move the project back to Development before using this method.

**Missing Project Design/Setup privileges.** API Import/Update rights alone are not sufficient. The user whose token you are using must also have Project Design/Setup privileges. If you receive a permissions error despite having an API Import token, check that the Design/Setup privilege is also granted.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-16 — Export Arms (retrieve arm metadata from a project)
- RC-API-18 — Delete Arms (remove arms from a project)
- RC-LONG-01 — Longitudinal Project Setup (how arms are structured; use case for programmatic import)
