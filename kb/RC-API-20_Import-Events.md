RC-API-20

**Import Events API**

| **Article ID** | RC-API-20 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-19 — Export Events; RC-API-21 — Delete Events |

---

# 1. Overview

The Import Events API method creates or modifies events in a longitudinal REDCap project. Events are timepoints or phases within an arm. Each event has a name, label, arm assignment, and offset information.

The `override` parameter controls behavior: when set to `0`, the method adds or modifies events without deleting others; when set to `1`, all existing events are deleted and replaced with the events you provide.

> **Important:** Events exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import right. |
| `content` | Required | Always `'event'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `format` | Optional | Set to `'json'` or `'csv'`. Default is JSON. |
| `override` | Optional | `0` = add/modify events without deleting others (default); `1` = delete all existing events and replace with provided events. |
| `data` | Required | A JSON array of event objects. Each object must include `event_name`, `arm_num`, `unique_event_name`, and optional offset fields (`day_offset`, `offset_min`, `offset_max`). |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests, json

record = {
    'event_name': 'Event 1',
    'arm_num': 1,
    'day_offset': 0,
    'offset_min': 0,
    'offset_max': 0,
    'unique_event_name': 'event_1_arm_1'
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'event',
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
	event_name='Event 1',
	arm_num=1,
	day_offset=0,
	offset_min=0,
	offset_max=0,
	unique_event_name='event_1_arm_1'
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='event',
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

DATA="token=$API_TOKEN&content=event&action=import&override=0&format=json&data=[{\"event_name\":\"Event%201\",\"arm_num\":\"1\",\"day_offset\":\"0\",\"offset_min\":\"0\",\"offset_max\":\"0\",\"unique_event_name\":\"event_1_arm_1\"}]"

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
		'event_name'        => 'Event XX',
		'arm_num'           => '1',
		'day_offset'        => '0',
		'offset_min'        => '0',
		'offset_max'        => '0',
		'unique_event_name' => 'event_xx_arm_1'
	),
	array(
		'event_name'        => 'Event YY',
		'arm_num'           => '2',
		'day_offset'        => '0',
		'offset_min'        => '0',
		'offset_max'        => '0',
		'unique_event_name' => 'event_yy_arm_2'
	),
);

$data = json_encode($data);

$fields = array(
	'token'    => $GLOBALS['api_token'],
	'content'  => 'event',
	'action'   => 'import',
	'format'   => 'json',
	'override' => 1,
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

On success, the method returns a message indicating how many events were added or modified. The HTTP status code will be 200.

Example response:
```json
{
  "success": true,
  "message": "2 event(s) added or modified"
}
```

---

# 5. Common Questions

**Q: What is the `unique_event_name` and how does it differ from `event_name`?**

**A:** The `event_name` is the human-readable label (e.g., "Baseline Visit"). The `unique_event_name` is the system identifier used in data exports and API calls (e.g., `event_1_arm_1` or `baseline_visit_arm_1`). The `unique_event_name` must be unique and typically follows the pattern `[event_label]_arm_[arm_num]`.

**Q: What do the offset fields represent?**

**A:** `day_offset` is the expected number of days after enrollment for the event. `offset_min` and `offset_max` define the acceptable window. For example, a visit expected at day 7 with min/max of ±3 days is acceptable from day 4 to day 10. These are used for visit compliance tracking.

**Q: Can I use this method on a classic project?**

**A:** No. Events are a longitudinal-only feature. This method will fail on classic projects.

**Q: What happens if I specify an `arm_num` that does not exist?**

**A:** The API will return an error. You must specify `arm_num` values that correspond to existing arms in the project. Use Export Arms (RC-API-16) to discover valid arm numbers.

---

# 6. Common Mistakes & Gotchas

**Calling Import Events on a classic project.** Events are a longitudinal-only feature. This method will fail on classic projects. Always verify your project is longitudinal before calling this method.

**Forgetting to JSON-encode the `data` parameter.** The `data` parameter must be a valid JSON array. Use `json.dumps()` in Python, `toJSON()` in R, or `json_encode()` in PHP to properly format it.

**Using `event_name` when you should use `unique_event_name`.** The `event_name` is the label; the `unique_event_name` is the identifier. In other API calls, always use `unique_event_name`.

**Using `override=1` when you only want to add a single event.** The `override=1` flag deletes all existing events. If you only want to add or modify one event, use `override=0` instead.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-19 — Export Events (retrieve event metadata from a project)
- RC-API-21 — Delete Events (remove events from a project)
- RC-LONG-01 — Longitudinal Project Setup (how events are structured; use case for programmatic import)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeating events integrate with the event structure)
