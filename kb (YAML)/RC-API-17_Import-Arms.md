---
id: RC-API-17
title: Import Arms API
domain: API
applies_to:
- Longitudinal REDCap projects only
requires: Any supported version
verified_against: REDCap v17.5.6 (Standard) — §1, §2, §4–§6 (Production-status restriction
  and rights not re-tested) live-tested via the API on a sandbox project (2026-10);
  LTS line last reviewed against the v17.3.7 (LTS) changelog; Import Arms behaviour
  (incl. rights and Production status) checked against source code on v17.6.5 / v17.3.31
  / v16.0.61 (Production status and rights still not live-tested)
prerequisites:
- RC-API-01 — REDCap API
version: '1.3'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-16
  title: Export Arms API
- id: RC-API-18
  title: Delete Arms API
tags:
- api
synonyms:
- how do i import arms via the api
- import arms api call
- create or rename study arms through the api
- api method to add arm numbers and names
- configure longitudinal arms programmatically
- bulk update arms with the api
- api endpoint to import arms
- add arms to a multi-arm project via api
- imported arm not showing in export arms
---

# 1. Overview

The Import Arms API method creates or modifies arms in a longitudinal REDCap project. Each arm consists of an arm number and a name. You can use this method to add new arms or update the names of existing arms.

The `override` parameter controls behavior: when set to `0` (or left out), the method adds or modifies arms without deleting others; when set to `1`, all existing arms are deleted and replaced with the arms you provide. The import is all-or-nothing: if any row fails validation, no arms are changed.

> **Important:** In **Development status** the method always works (given the rights below). For a project in **Production** (or Analysis/Cleanup) status it depends on a system-wide Control Center setting — the one that lets normal users add or modify events in production:
> - **Setting off:** the call is refused.
> - **Setting on:** adding new arms and renaming existing arms works, but `override=1` is refused with *"This 'override' parameter cannot be used while the project is in Production status."*
>
> REDCap administrators are not exempt: an admin's token gets the same result.

> **Institution-specific:** Whether normal users may add or modify events and arms in Production is a system-wide choice. Check with your REDCap administrators before planning arm changes on a Production project.

> **Important:** Arms exist only in longitudinal projects. On a classic project this method does **not** return an error (HTTP 200 with a count), so check the project type first.

**Permissions required:** The API token used must have both **API Import/Update** privileges *and* **Project Design/Setup** privileges in the project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update *and* Project Design/Setup privileges. |
| `content` | Required | Always `'arm'` for this method. |
| `action` | Required | Always `'import'` for this method. If you leave it out, the call is treated as Export Arms and returns the arm list instead of importing. |
| `format` | Optional | `'csv'`, `'json'`, or `'xml'`. Default is `'xml'` if omitted. |
| `override` | Optional | `0` = add/modify arms without deleting others (default if omitted); `1` = delete all existing arms — with their events and data — and replace with provided arms. Only the exact value `1` triggers replacement. Refused in Production status. |
| `data` | Required | Arms to import, in the format specified by `format`. Each arm must have `arm_num` (a whole number from 1 to 99) and `name` (up to 50 characters; a blank name becomes "Arm N"). |
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

On success, the method returns the **number of arms imported** as a plain integer. The HTTP status code will be 200.

Example response:
```
1
```

This number reflects how many arms you sent that were created or renamed (an arm re-sent with its current name still counts), not the total number of arms in the project.

> **Important:** Data REDCap cannot parse (for example, invalid JSON, or JSON sent with `format=csv`) comes back with **HTTP 200** and the text *"The data is not in the specified format."* rather than an error status. In scripts, check that the response body is a number before treating the call as a success.

Missing `arm_num` or `name` columns, an `arm_num` outside 1–99 (including `0`), or a name over 50 characters returns an error, and nothing is imported. The project log records the import but does not list which arms were changed.

---

# 5. Common Questions

**Q: What is the difference between `override=0` and `override=1`?**

**A:** With `override=0`, the API adds new arms or updates the names of existing arms without touching other arms. With `override=1`, all existing arms are deleted first — together with all their events and instrument-event mappings, so existing record data is no longer reachable — then replaced with the arms you provide. The new arms have **no events**: the project stays without events until you run Import Events ([RC-API-20 — Import Events API](RC-API-20_Import-Events.md)) and re-import the mappings. Use `override=1` only if you want to completely rebuild the arm structure, and only as the first step of a script that rebuilds events and mappings straight after.

**Q: Can I use this method on a classic project?**

**A:** No. Arms are a longitudinal-only feature. The call isn't rejected (it returns a count), but it has no use there — and `override=1` on a classic project deletes the project's only arm and event. No default event is recreated, so the project is left without an event until you add one (Import Events, or the project setup page). Check `is_longitudinal` with Export Project Info ([RC-API-34 — Export Project Info API](RC-API-34_Export-Project-Info.md)) first.

**Q: What happens if I import an arm with an `arm_num` that already exists?**

**A:** With `override=0`, the existing arm's name will be updated to the name you provide. With `override=1`, the entire arm structure is replaced, so the old arm is deleted and the new one takes its place.

**Q: Can I have non-sequential arm numbers (e.g., 1, 3, 5)?**

**A:** Yes — arm 5 next to arms 1 and 2 is accepted, as is any whole number from 1 to 99. Sequential numbering is still easier to work with in the UI and in scripts.

**Q: Can I send CSV or XML instead of JSON?**

**A:** Yes. Set `format` to match (`csv` with an `arm_num,name` header row, or `xml`). If `format` doesn't match what you send, the call returns HTTP 200 with *"The data is not in the specified format."*

**Q: I imported an arm but Export Arms doesn't show it. Why?**

**A:** An arm without events is not listed by Export Arms ([RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md)). Add at least one event to it with Import Events ([RC-API-20 — Import Events API](RC-API-20_Import-Events.md)) and it appears.

**Q: What does `returnFormat` control?**

**A:** `returnFormat` controls the format of any *error* messages returned by the API. It is independent of the `format` parameter (which controls how you send your data). If you omit `returnFormat`, error messages will come back in whatever format you specified with `format`. This is useful when, for example, you are sending CSV data but want JSON-formatted errors for easier parsing.

**Q: Does this method work on a project that is in Production status?**

**A:** Only if your REDCap administrator has enabled the Control Center setting that lets normal users add or modify events in production. With that setting on, you can add arms and rename existing arms (`override=0`), but `override=1` is refused with *"This 'override' parameter cannot be used while the project is in Production status."* With the setting off, the call is refused. This applies to administrators' tokens too. If the setting is off at your institution, ask your REDCap administrators how arm changes on a Production project are handled.

---

# 6. Common Mistakes & Gotchas

**Calling Import Arms on a classic project.** Arms are a longitudinal-only feature, but the call returns HTTP 200 with a count on a classic project instead of failing. With `override=1` it also deletes the project's only event and leaves the project without one. Always confirm your project is longitudinal before calling this method.

**Treating any HTTP 200 as success.** Malformed or mismatched data returns HTTP 200 with the text *"The data is not in the specified format."* Check that the response is a number.

**Forgetting to JSON-encode the `data` parameter.** The `data` parameter must be a valid JSON array of objects. It is not a plain string. Use `json.dumps()` in Python, `toJSON()` in R, or `json_encode()` in PHP to properly format it.

**Using `override=1` when you only want to add a new arm.** The `override=1` flag deletes all existing arms — and their events, instrument-event mappings and access to all record data in them — and replaces them with arms that have no events. If you only want to add a single arm, use `override=0` instead.

**Running `override=1` without re-importing events.** After an `override=1` import the project has no events at all until you run Import Events and re-import the instrument-event mappings. Export arms, events and mappings first, and run the full rebuild in one script.

**Assuming arm numbers start from 0.** Arm numbers in REDCap are 1-indexed: the first arm is arm 1. `arm_num: 0` is rejected, and so is anything above 99.

**Calling Import Arms on a Production project.** Unless your administrator has enabled the Control Center setting that lets normal users add or modify events in production, the call fails. With it enabled, adds and renames work but `override=1` is refused.

**Leaving out `action=import`.** Without it, the request is handled as Export Arms: you get the arm list back and nothing is imported.

**Missing Project Design/Setup privileges.** API Import/Update rights alone are not sufficient. The user whose token you are using must also have Project Design/Setup privileges. Without API Import/Update the call returns HTTP 403; without Project Design/Setup it returns HTTP 400. If you receive a permissions error despite having an API Import token, check that the Design/Setup privilege is also granted.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md) (retrieve arm metadata from a project)
- [RC-API-18 — Delete Arms API](RC-API-18_Delete-Arms.md) (remove arms from a project)
- [RC-API-20 — Import Events API](RC-API-20_Import-Events.md) (add events to new arms; required after `override=1`)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (how arms are structured; use case for programmatic import)
