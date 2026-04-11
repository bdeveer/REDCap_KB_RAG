RC-API-34

**Export Project Info API**

| **Article ID** | RC-API-34 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-35 — Import Project Info; RC-API-36 — Export Project XML; RC-API-37 — Import Project (Create Project) |

---

# 1. Overview

The Export Project Info API retrieves project metadata and configuration settings without exporting the actual data or instruments. This is useful for auditing project structure, verifying project properties programmatically, or comparing projects across instances. You receive information such as project title, production status, longitudinal configuration, survey enablement, and other key project attributes.

This method requires only the API Export right and returns a JSON object containing all project-level configuration fields.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'project'` |
| `format` | Optional | Response format: `'json'` (default) or `'xml'` |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'project',
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
    content='project',
    format='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=project&format=json"

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
	'content' => 'project',
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 4. Response

The API returns a JSON object containing project metadata fields, such as:

```json
{
  "project_id": 123,
  "project_title": "My Research Project",
  "is_longitudinal": "0",
  "in_production": "1",
  "surveys_enabled": "1",
  "record_autonumbering_enabled": "1",
  "randomization_enabled": "0",
  "ddp_enabled": "0",
  "project_irb_number": "",
  "project_grant_number": "",
  "project_pi_firstname": "John",
  "project_pi_lastname": "Doe",
  "display_today_now_button": "1",
  "footer_contents": "My footer text"
}
```

---

# 5. Common Questions

**Q: What is the difference between Export Project Info and Export Project XML?**
A: Export Project Info (RC-API-34) returns only project metadata and configuration. Export Project XML (RC-API-36) returns the complete project structure including instruments, fields, events, and can be used to recreate the project.

**Q: Can I export all projects' metadata at once?**
A: No. Each API call requires a project-specific token. You must loop through your project tokens and call the API for each project separately.

**Q: Which right do I need to use this method?**
A: You need the API Export right at the user level within the project.

**Q: Can I modify project settings using this API?**
A: Not with this method. Use RC-API-35 (Import Project Info) to update project settings. Export Project Info is read-only.

**Q: What format options are available?**
A: You can request `'json'` (default) or `'xml'` format. JSON is more commonly used in modern integrations.

---

# 6. Common Mistakes & Gotchas

**Missing format parameter:** While format is optional, always explicitly specify `'json'` or `'xml'` to avoid ambiguity and ensure consistent parsing.

**Assuming read/write permission:** This API method uses only the Export right. You do not need (and should not have) Project Setup or Data Import/Manipulation rights to run this method.

**Checking `in_production` vs production status in UI:** The `in_production` field returned is an integer (0 or 1), not a boolean. Always test with `== "1"` rather than boolean checks in scripting languages.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-35 — Import Project Info
- RC-API-36 — Export Project XML
- RC-API-37 — Import Project (Create Project)
