RC-API-19

**Export Events API**

| Article ID | RC-API-19 |
|---|---|
| Domain | API |
| Applies To | Longitudinal REDCap projects only |
| Prerequisite | RC-API-01 — REDCap API |
| Version | 1.1 |
| Last Updated | 2026 |
| Author | See KB-SOURCE-ATTESTATION.md |
| Source | REDCap API v16.1.3 official documentation examples |
| Related Topics | RC-API-01 — REDCap API; RC-API-20 — Import Events; RC-API-21 — Delete Events |

---

# 1. Overview

The Export Events API method retrieves the list of events in a longitudinal REDCap project. Events represent timepoints or phases within an arm. Each event has properties such as its unique name, human-readable label, arm assignment, and offset information.

This method is useful for discovering the event structure of a project or validating event configuration programmatically.

> **Important:** Events exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'event'` for this method. |
| `format` | Required | Response format: `'csv'`, `'json'`, or `'xml'`. Default is `'xml'`. |
| `arms` | Optional | An array of arm numbers to filter events. If omitted, returns events for all arms. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to whatever `format` is set to. If neither is provided, defaults to `'xml'`. Not applicable when using background processing. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'event',
    'format': 'json',
    'arms': ''
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
    content='event',
    format='json',
    returnFormat='json',
    arms=''
)
print(result)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=event&format=json&arms="

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
	'content' => 'event',
	'format'  => 'json',
	'arms'    => array()
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

The method returns a JSON array (or CSV) containing all events in the project.

Example JSON response:
```json
[
  {
    "event_name": "Event 1",
    "arm_num": 1,
    "unique_event_name": "event_1_arm_1",
    "day_offset": 0,
    "offset_min": 0,
    "offset_max": 0
  },
  {
    "event_name": "Event 2",
    "arm_num": 1,
    "unique_event_name": "event_2_arm_1",
    "day_offset": 7,
    "offset_min": -3,
    "offset_max": 3
  }
]
```

---

# 5. Common Questions

**Q: I called Export Events on my project and got an error. Why?**

**A:** Export Events only works on longitudinal projects. If your project is classic, this method will not work. Check your project setup to confirm that your project is longitudinal.

**Q: How do I filter events by arm?**

**A:** Set the `arms` parameter to an array of arm numbers (e.g., `[1, 2]` in Python/JSON). If you omit the parameter, all events from all arms are returned.

**Q: What is the difference between `event_name` and `unique_event_name`?**

**A:** The `event_name` is the human-readable label (e.g., "Baseline Visit"). The `unique_event_name` is the system identifier used in data exports and API calls (e.g., `event_1_arm_1`). Always use `unique_event_name` in API calls.

**Q: What do the offset fields mean?**

**A:** The `day_offset` is the expected number of days after enrollment that the event should occur. The `offset_min` and `offset_max` define the acceptable window (e.g., ±3 days). These are used to track visit windows in longitudinal studies.

**Q: Can I use the `day_offset` values to calculate expected visit dates for a participant?**

**A:** Yes. Add the `day_offset` (in days) to the participant's enrollment or study start date to get the target date for each event. The `offset_min` and `offset_max` fields define the acceptable window on either side of that date. This is the standard approach for monitoring visit compliance in clinical studies.

---

# 6. Common Mistakes & Gotchas

**Calling Export Events on a classic project.** Events are a longitudinal-only feature. This method will fail on classic projects. Always verify your project is longitudinal before calling this method.

**Using `event_name` instead of `unique_event_name` in other API calls.** When you reference an event in other API methods (e.g., Export Records), use the `unique_event_name`, not the `event_name`. The `unique_event_name` is the system identifier.

**Assuming events are always sequential.** Do not assume event numbers or unique_event_names follow a sequential pattern. Always parse the response and use the actual values returned.

**Not specifying the `arms` parameter when you only need events from specific arms.** If you are working with a multi-arm project and only care about certain arms, use the `arms` parameter to filter the results rather than post-processing the response.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-20 — Import Events (add or modify events in a project)
- RC-API-21 — Delete Events (remove events from a project)
- RC-LONG-01 — Longitudinal Project Setup (how events are configured in a longitudinal project)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeating events relate to standard events)
