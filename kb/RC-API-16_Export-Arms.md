RC-API-16

**Export Arms API**

| **Article ID** | RC-API-16 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-17 — Import Arms; RC-API-18 — Delete Arms |

---

# 1. Overview

The Export Arms API method retrieves the list of arms (study branches) in a longitudinal REDCap project. Arms exist only in longitudinal projects and represent parallel or sequential study pathways. Each arm has a number and a name.

This method returns metadata about arms: their arm numbers, names, and any other configured properties. It is useful for programmatically discovering the project structure or validating arm configuration.

> **Important:** Arms exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

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

---

# 5. Common Questions

**Q: I called Export Arms on my project and got an error. Why?**

**A:** Export Arms only works on longitudinal projects. If your project is classic (non-longitudinal), this method will not work. Check your project setup under Project Setup → Project Type to confirm that your project is longitudinal.

**Q: Can I export arms from a classic project?**

**A:** No. Arms are a longitudinal feature. Classic projects do not have arms. If you need to organize your classic project into groups, consider using a grouping field in your data or using Data Access Groups.

**Q: What is the difference between arm number and arm name?**

**A:** The arm number is the numeric identifier (1, 2, 3, etc.). The arm name is the human-readable label (e.g., "Treatment Group A" or "Control Arm"). The API returns both.

**Q: Can I get the format as CSV instead of JSON?**

**A:** Yes. Set `format='csv'` to receive the response as comma-separated values. You can also use `format='xml'`, which is the API default if no format is specified.

**Q: Can I export only certain arms instead of all of them?**

**A:** Yes. Pass an array of arm numbers in the `arms` parameter to limit the response to only those arms. If you omit the parameter, all arms in the project are returned.

---

# 6. Common Mistakes & Gotchas

**Calling Export Arms on a classic project.** Arms are a longitudinal-only feature. If your project is not longitudinal, this method will fail. Always verify your project type before calling this method.

**Not checking if the project is longitudinal.** If your code is designed to work with multiple projects, check whether each project is longitudinal before calling Export Arms. Use the Project Metadata API or check the project setup.

**Assuming arm numbers are sequential starting from 1.** Although arm numbers are typically sequential (1, 2, 3), do not assume this. Always parse the response and use the actual `arm_num` values returned.

**Expecting JSON when no format is specified.** The API default for this method is `xml`, not JSON. If your code parses the response as JSON without explicitly setting `format=json`, it will fail. Always set the `format` parameter explicitly.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-17 — Import Arms (add or modify arms in a project)
- RC-API-18 — Delete Arms (remove arms from a project)
- RC-LONG-01 — Longitudinal Project Setup (how arms are configured in a longitudinal project)
