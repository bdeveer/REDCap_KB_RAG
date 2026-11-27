---
id: RC-API-16
title: Export Arms API
domain: API
applies_to:
- Longitudinal REDCap projects only
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Export
  Arms behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-17
  title: Import Arms API
- id: RC-API-18
  title: Delete Arms API
tags:
- api
synonyms:
- how do i export arms via the api
- export arms api call
- get the list of study arms through the api
- api method to list arm numbers and names
- retrieve longitudinal arms programmatically
- pull arm structure with the api
- api endpoint to export arms
- list arms in a multi-arm project via api
---

# 1. Overview

The Export Arms API method retrieves the list of arms (study branches) in a longitudinal REDCap project. Arms exist only in longitudinal projects and represent parallel or sequential study pathways. Each arm has a number and a name.

This method returns two values per arm: its arm number (`arm_num`) and its name. Arms are sorted by arm number. Only arms that have at least one event are exported; an arm you created but have not yet given any events is left out of the response. The method is useful for programmatically discovering the project structure or validating arm configuration.

> **Important:** Arms exist only in longitudinal projects. Called on a classic (non-longitudinal) project, this method returns HTTP 400 with the error "You cannot export arms for classic projects".

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** On 16.0.61 LTS, Export Arms also returns "You cannot export arms for classic projects" for a project that has longitudinal data collection enabled but only one event defined. On 17.x the method only checks whether longitudinal data collection is enabled. If you are on 16.0.61 and get this error on a longitudinal project, check that it has more than one event (Export Events or Project Setup → Define My Events).

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires the API Export right; Project Design and Setup rights are not needed. |
| `content` | Required | Always `'arm'` for this method. |
| `format` | Optional | Output format: `csv`, `json`, or `xml`. Default is `xml`. |
| `arms` | Optional | Array of specific arm numbers to export. If omitted, all arms are returned. |
| `returnFormat` | Optional | Format for error messages: `csv`, `json`, or `xml`. Defaults to the value of `format` if not specified, or `xml` if neither is set. Does not apply when using a background process. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'arm',
    'format': 'json'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 3.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='arm',
    format='json'
)
print(result)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=arm&format=json"

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
	'content' => 'arm',
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

The method returns the arms for the project in the format specified. The default format is `xml`; pass `format=json` or `format=csv` to change it.

Example JSON response:
```json
[
  {
    "arm_num": 1,
    "name": "Arm 1"
  },
  {
    "arm_num": 2,
    "name": "Arm 2"
  }
]
```

In JSON, `arm_num` is returned as a number, not a string. The XML response wraps each arm in an `<item>` element inside `<arms>`, with `<arm_num>` and `<name>` children. CSV returns a header row `arm_num,name` followed by one row per arm.

Each call is recorded in the project Logging as "Export arms (API)".

---

# 5. Common Questions

**Q: I called Export Arms on my project and got an error. Why?**

**A:** Export Arms only works on longitudinal projects. On a classic (non-longitudinal) project it returns HTTP 400 with "You cannot export arms for classic projects". Check on the Project Setup page whether longitudinal data collection is enabled, or call Export Project Info and check `is_longitudinal`. On 16.0.61 LTS, the same error also appears for a longitudinal project with only one event (see the version caveat in Section 1).

**Q: Can I export arms from a classic project?**

**A:** No. Arms are a longitudinal feature. Classic projects do not have arms. If you need to organize your classic project into groups, consider using a grouping field in your data or using Data Access Groups.

**Q: What is the difference between arm number and arm name?**

**A:** The arm number is the numeric identifier (1, 2, 3, etc.). The arm name is the human-readable label (e.g., "Treatment Group A" or "Control Arm"). The API returns both.

**Q: Can I get the format as CSV instead of JSON?**

**A:** Yes. Set `format='csv'` to receive the response as comma-separated values. You can also use `format='xml'`, which is the API default if no format is specified.

**Q: Can I export only certain arms instead of all of them?**

**A:** Yes. Pass an array of arm numbers in the `arms` parameter to limit the response to only those arms. If you omit the parameter, all arms in the project are returned.

**Q: I just created an arm but it is missing from the export. Why?**

**A:** Export Arms only returns arms that have at least one event. Add an event to the new arm (Import Events or Project Setup → Define My Events) and it will appear in the export.

---

# 6. Common Mistakes & Gotchas

**Calling Export Arms on a classic project.** Arms are a longitudinal-only feature. If your project is not longitudinal, this method fails with "You cannot export arms for classic projects". Always verify your project type before calling this method.

**Not checking if the project is longitudinal.** If your code is designed to work with multiple projects, check whether each project is longitudinal before calling Export Arms. Use [Export Project Info](RC-API-34_Export-Project-Info.md) and check `is_longitudinal` (the metadata/data dictionary export does not tell you this). Note that `is_longitudinal` is only `1` when longitudinal data collection is enabled and the project has more than one event, which also matches when 16.0.61 LTS will accept the call.

**Expecting every arm in the export.** Arms without any events are not returned. If you just created an arm with Import Arms, add its events before relying on it appearing in Export Arms.

**Assuming arm numbers are sequential starting from 1.** Although arm numbers are typically sequential (1, 2, 3), do not assume this. Always parse the response and use the actual `arm_num` values returned.

**Expecting JSON when no format is specified.** The API default for this method is `xml`, not JSON. If your code parses the response as JSON without explicitly setting `format=json`, it will fail. Always set the `format` parameter explicitly.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md) (add or modify arms in a project)
- [RC-API-18 — Delete Arms API](RC-API-18_Delete-Arms.md) (remove arms from a project)
- [RC-API-34 — Export Project Info API](RC-API-34_Export-Project-Info.md) (check `is_longitudinal` before calling Export Arms)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (how arms are configured in a longitudinal project)
