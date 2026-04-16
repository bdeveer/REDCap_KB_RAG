RC-API-40

**Export Survey Link API**

| **Article ID** | RC-API-40 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with surveys enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-41 — Export Survey Queue Link; RC-API-42 — Export Survey Return Code |

---

# 1. Overview

The Export Survey Link API generates a unique, clickable survey URL for a specific record and instrument. This is essential for survey distribution workflows where you programmatically send survey links via email, SMS, or other channels. Each link is secure, record-specific, and does not require authentication.

Surveys must be enabled on the project, and the instrument must be marked as a survey in the project design.

> **Permissions required:** API Export privileges AND **Survey Distribution Tools** privileges. If the user lacks Survey Distribution Tools access, the API will return an error.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyLink'` |
| `record` | Required | Record ID (must exist in the project) |
| `instrument` | Required | Instrument name (must be configured as a survey) |
| `event` | Required (longitudinal) | Event name (for longitudinal projects); omit for classic projects |
| `repeat_instance` | Optional | Repeat instance number for repeating instruments/events. Default: `'1'` |
| `returnFormat` | Optional | Format for **error messages only**: `csv`, `json`, or `xml` (default). Does not affect the response — the survey link is always returned as plain text. |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyLink',
    'record': 'f21a3ffd37fc0b3c',
    'instrument': 'test_instrument',
    'event': 'event_1_arm_1',
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
    content='surveyLink',
    record='f21a3ffd37fc0b3c',
    instrument='test_instrument',
    event='event_1_arm_1',
    format='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=surveyLink&record=f21a3ffd37fc0b3c&instrument=test_instrument&event=event_1_arm_1&format=json"

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
	'token'      => $GLOBALS['api_token'],
	'content'    => 'surveyLink',
	'record'     => 'f21a3ffd37fc0b3c',
	'instrument' => 'demographics',
	'event'      => 'event_1_arm_1',
	'format'     => 'json'
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

The API returns a unique survey URL as **plain text** (not JSON):

```
https://your-redcap-instance.edu/surveys/?s=XXXXXXXXXXXXXXXXXX
```

The URL is valid immediately and can be distributed via email, text message, or embedded in web pages.

---

# 5. Common Questions

**Q: Can I regenerate the same survey URL for the same record?**
A: Yes. Calling the API multiple times for the same record and instrument always returns the same URL, allowing you to resend links as needed.

**Q: What happens if I request a survey link for a record that doesn't exist?**
A: The API will return an error or create the record (depending on instance settings). Best practice: verify the record exists before requesting the link.

**Q: How long is a survey URL valid?**
A: Survey URLs do not expire. They remain valid until you delete the record or disable the survey instrument.

**Q: Can respondents access the survey without the link?**
A: No. Survey links are private and non-guessable. Respondents must use the unique URL to access the survey without authentication.

**Q: For longitudinal projects, which event should I specify?**
A: Specify the event in which you want the respondent to complete the survey. The instrument must be assigned to that event in the project design.

---

# 6. Common Mistakes & Gotchas

**Missing Survey Distribution Tools privilege:** API Export alone is not sufficient. The user account associated with the token must also have Survey Distribution Tools access in the project. Without it, the call returns an error even if the token itself is valid.

**Missing event parameter for longitudinal projects:** For longitudinal studies, the `event` parameter is required. Omitting it results in an error.

**Using instrument label instead of variable name:** The `instrument` parameter must be the instrument's variable name (e.g., `demographics`), not its display label (e.g., "Demographics Form").

**Requesting survey link for non-survey instrument:** The instrument must be enabled as a survey in the project design. Regular instruments cannot be accessed via survey link.

**Parsing the response as JSON:** The response is plain text — just the URL string. Do not attempt to parse it as JSON or look for a `survey_url` key; treat the entire response body as the link.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-41 — Export Survey Queue Link
- RC-API-42 — Export Survey Return Code
- RC-API-43 — Export Survey Participants
- RC-SURV-01 — Surveys – Basics (survey fundamentals and how survey links work)
- RC-SURV-04 — Survey Link Types & Access Methods (the link types this method generates)
