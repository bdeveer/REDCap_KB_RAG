RC-API-41

**Export Survey Queue Link API**

| **Article ID** | RC-API-41 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with Survey Queue enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-40 — Export Survey Link; RC-API-42 — Export Survey Return Code |

---

# 1. Overview

The Export Survey Queue Link API generates a unique URL that allows a respondent to access their personalized survey queue. The Survey Queue is a feature that presents multiple surveys to a respondent in a guided workflow. This API is essential for sending queue links via email, SMS, or other communication channels in automated workflows.

Survey Queue must be enabled on the project for this method to work.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyQueueLink'` |
| `format` | Optional | Response format: `'json'` (default) or `'xml'` |
| `record` | Required | Record ID (must exist in the project) |
| `event` | Optional | Event name (for longitudinal projects) |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyQueueLink',
    'record': 'f21a3ffd37fc0b3c',
    'instrument': 'demographics',
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
    content='surveyQueueLink',
    record='f21a3ffd37fc0b3c',
    instrument='demographics',
    event='event_1_arm_1',
    format='json'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=surveyQueueLink&record=f21a3ffd37fc0b3c&instrument=test_instrument&event=event_1_arm_1&format=json"

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
	'content'    => 'surveyQueueLink',
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

The API returns a unique survey queue URL:

```json
{
  "survey_queue_url": "https://myredcap.edu/surveys/?s=Q7K2L1M5N3P8R4T9X1Y0Z6C2D5E3F4G1"
}
```

This URL presents the respondent with all surveys in their queue for the specified record and event.

---

# 5. Common Questions

**Q: What is the difference between a survey link and a survey queue link?**
A: A survey link (RC-API-40) is specific to one instrument. A survey queue link (RC-API-41) presents multiple surveys in a guided workflow on a single page.

**Q: Which surveys appear in the queue?**
A: The queue displays all surveys assigned to the record and event. The order and visibility depend on the survey queue configuration in your project settings.

**Q: Can I customize which surveys appear in the queue via API?**
A: No. Survey queue membership is configured in the project design. Use the REDCap interface to specify which instruments are part of the queue.

**Q: For classic (non-longitudinal) projects, should I include the event parameter?**
A: For classic projects, you may omit the event parameter. It is required only for longitudinal projects.

**Q: What happens if the record has no surveys in its queue?**
A: The API still returns a valid URL, but accessing it shows a message that no surveys are available.

---

# 6. Common Mistakes & Gotchas

**Confusing surveyLink and surveyQueueLink:** These are distinct content types. Use `'surveyLink'` for single instrument surveys and `'surveyQueueLink'` for multi-survey workflows.

**Missing event for longitudinal projects:** Always specify the event for longitudinal studies. Omitting it may return an error or an incomplete queue.

**Assuming Survey Queue is enabled:** Verify Survey Queue is enabled in your project settings. If it's disabled, this API method will not work.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-40 — Export Survey Link
- RC-API-42 — Export Survey Return Code
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-07 — Survey Queue (how the survey queue works; context for the queue link)
