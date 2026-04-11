RC-API-42

**Export Survey Return Code API**

| **Article ID** | RC-API-42 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with surveys enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-40 — Export Survey Link; RC-API-41 — Export Survey Queue Link |

---

# 1. Overview

The Export Survey Return Code API generates a unique code that allows a respondent to resume an incomplete survey from where they left off. When a respondent saves progress and closes the survey, you can use this API to generate a return code that re-opens the survey at their saved point. This is essential for multi-session surveys and respecting respondent workflow interruptions.

Surveys must be enabled on the project, and the instrument must be configured as a survey.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyReturnCode'` |
| `format` | Optional | Response format: `'json'` (default) or `'xml'` |
| `record` | Required | Record ID (must exist in the project) |
| `instrument` | Required | Instrument name (must be configured as a survey) |
| `event` | Required | Event name (for longitudinal projects); optional for classic projects |
| `repeat_instance` | Optional | Repeat instance number (for repeating instruments) |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyReturnCode',
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
    content='surveyReturnCode',
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

DATA="token=$API_TOKEN&content=surveyReturnCode&record=f21a3ffd37fc0b3c&instrument=test_instrument&event=event_1_arm_1&format=json"

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
	'content'    => 'surveyReturnCode',
	'record'     => 'f21a3ffd37fc0b3c',
	'instrument' => 'test_instrument',
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

The API returns a return code that can be appended to a survey link to resume progress:

```json
{
  "survey_return_code": "B3K2M5L1N7P9R4T8X2Y1Z3C5D6E8F1G2"
}
```

The respondent accesses the survey by visiting a URL like:
```
https://myredcap.edu/surveys/?s=<survey_link>&rc=B3K2M5L1N7P9R4T8X2Y1Z3C5D6E8F1G2
```

---

# 5. Common Questions

**Q: How do I use a return code with a survey link?**
A: First, request the survey link using RC-API-40. Then request the return code using this method. Combine them in the URL: `<survey_link>&rc=<return_code>`.

**Q: Can I generate a return code for a survey that hasn't been started?**
A: Yes. Return codes can be generated at any time. They resume from the beginning if the survey hasn't been accessed yet.

**Q: Does a return code expire?**
A: Return codes do not have a built-in expiration. They remain valid until you delete the record or close the survey instrument.

**Q: What is the difference between a return code and the survey link itself?**
A: A survey link takes the respondent to the beginning of the survey. A return code resumes from their last saved point, preserving their progress.

**Q: Can I track whether a respondent has used a return code?**
A: Use the audit log (RC-API-39) to see when survey links and return codes are accessed.

---

# 6. Common Mistakes & Gotchas

**Forgetting the `&rc=` parameter:** To use the return code, append it to the survey link with `&rc=` (not `?rc=`). The ampersand is required because the survey link already contains query parameters.

**Assuming return codes prevent re-answering:** Return codes allow respondents to resume, but they can still change previous answers. There is no read-only mode.

**Generating return codes without corresponding survey links:** Always generate the survey link first, then add the return code when you want to enable resuming from a saved point.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-40 — Export Survey Link
- RC-API-41 — Export Survey Queue Link
- RC-API-43 — Export Survey Participants
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-03 — Survey Settings: Behavior, Access & Termination (return code configuration in survey settings)
