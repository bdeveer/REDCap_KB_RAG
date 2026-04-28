RC-API-34

**Export Project Info API**

| **Article ID** | RC-API-34 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-35 — Import Project Info; RC-API-36 — Export Project XML; RC-API-37 — Import Project (Create Project) |

---

# 1. Overview

The Export Project Info API retrieves project metadata and configuration settings without exporting the actual data or instruments. This is useful for auditing project structure, verifying project properties programmatically, or comparing projects across instances. You receive information such as project title, production status, longitudinal configuration, survey enablement, and other key project attributes.

This method requires only the API Export right and returns a JSON object containing all project-level configuration fields.

---

# 2. Key Concepts & Definitions

### Project Metadata
Project-level configuration and properties including title, production status, longitudinal/survey settings, PI information, and structural flags. This does not include data or instrument designs.

### Production Status
A boolean field indicating whether the project is in production (active data collection) or in development/draft mode. Once a project is in production, certain structural changes are restricted.

### API Export Privilege
A permission that allows reading project data, metadata, and configuration via the API. This is the only privilege required for the Export Project Info method.

### Boolean Fields
Metadata fields that represent true/false values returned as `'0'` (false) or `'1'` (true) in the API response, rather than as JSON boolean types.

### Configuration Flag
A binary setting that controls project behavior, such as `surveys_enabled`, `randomization_enabled`, `record_autonumbering_enabled`, or `is_longitudinal`.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'project'` |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`) |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not specified. Does not apply when using background processing. |

---

# 4. Request Examples

## 4.1 Python
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

## 4.2 R
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

## 4.3 cURL
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

## 4.4 PHP
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

# 5. Response

The API returns project metadata in the format specified. Boolean values are represented as `'0'` (false) or `'1'` (true). All date/time values are returned in `Y-M-D H:M:S` format.

**Returned fields:**

| Field | Type | Description |
|---|---|---|
| `project_id` | Integer | Internal REDCap project ID |
| `project_title` | String | Project name |
| `creation_time` | DateTime | When the project was created |
| `production_time` | DateTime | When the project was moved to production |
| `in_production` | Boolean | Whether the project is currently in production |
| `project_language` | String | Language used in the project interface |
| `purpose` | Integer | Project purpose code |
| `purpose_other` | String | Free-text description when purpose is "Other" |
| `project_notes` | String | Notes about the project |
| `custom_record_label` | String | Custom label for the record ID field |
| `secondary_unique_field` | String | Field name designated as a secondary unique field |
| `is_longitudinal` | Boolean | Whether the project is longitudinal |
| `has_repeating_instruments_or_events` | Boolean | Whether repeating instruments or events are enabled |
| `surveys_enabled` | Boolean | Whether surveys are enabled |
| `scheduling_enabled` | Boolean | Whether scheduling is enabled |
| `record_autonumbering_enabled` | Boolean | Whether record autonumbering is enabled |
| `randomization_enabled` | Boolean | Whether randomization is enabled |
| `ddp_enabled` | Boolean | Whether dynamic data pull is enabled |
| `project_irb_number` | String | IRB approval number |
| `project_grant_number` | String | Grant number associated with the project |
| `project_pi_firstname` | String | Principal investigator first name |
| `project_pi_lastname` | String | Principal investigator last name |
| `project_pi_email` | String | Principal investigator email address |
| `display_today_now_button` | Boolean | Whether the Today/Now button is shown |
| `missing_data_codes` | String | Configured missing data codes |
| `external_modules` | String | Enabled external modules |
| `bypass_branching_erase_field_prompt` | Boolean | Whether the branching logic erase prompt is bypassed |

---

# 6. Common Questions

**Q: What is the difference between Export Project Info and Export Project XML?**
**A:** Export Project Info (RC-API-34) returns only project metadata and configuration. Export Project XML (RC-API-36) returns the complete project structure including instruments, fields, events, and can be used to recreate the project.

**Q: Can I export all projects' metadata at once?**
**A:** No. Each API call requires a project-specific token. You must loop through your project tokens and call the API for each project separately.

**Q: Which right do I need to use this method?**
**A:** You need the API Export right at the user level within the project.

**Q: Can I modify project settings using this API?**
**A:** Not with this method. Use RC-API-35 (Import Project Info) to update project settings. Export Project Info is read-only.

**Q: What format options are available?**
**A:** You can request `'csv'`, `'json'`, or `'xml'`. The default is `'xml'` if no format is specified. JSON is more commonly used in modern integrations, so it's worth specifying explicitly.

---

# 7. Common Mistakes & Gotchas

**Missing format parameter:** While format is optional, always explicitly specify `'csv'`, `'json'`, or `'xml'` to avoid ambiguity. The default is `'xml'`, which may catch you off guard if you're expecting JSON without specifying it.

**Assuming read/write permission:** This API method uses only the Export right. You do not need (and should not have) Project Setup or Data Import/Manipulation rights to run this method.

**Checking `in_production` vs production status in UI:** The `in_production` field returned is an integer (0 or 1), not a boolean. Always test with `== "1"` rather than boolean checks in scripting languages.

---

# 8. Related Articles

- RC-API-01 — REDCap API
- RC-API-35 — Import Project Info
- RC-API-36 — Export Project XML
- RC-API-37 — Import Project (Create Project)
