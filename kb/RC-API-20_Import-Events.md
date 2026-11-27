

**Import Events API**

| **Article ID** | [RC-API-20 — Import Events API](RC-API-20_Import-Events.md) |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.6 (Standard) — §1, §2, §4–§6 (Production-status restriction and rights not re-tested) live-tested via the API on a sandbox project (2026-10); LTS line last reviewed against the v17.3.7 (LTS) changelog; import behaviour (incl. rights and Production status, which were not live-tested) checked against source code on v17.6.5 / v17.3.31 / v16.0.61 |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-19 — Export Events API](RC-API-19_Export-Events.md); [RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md)|
| **Synonyms** | how do i import events via the api; import events api call; create or modify events in a longitudinal project through the api; api method to add timepoints and event labels; configure events and offsets programmatically; bulk update events with the api; api endpoint to import events; add events to an arm via the api; renaming event changes unique event name api; import events api rename event |

---

## 1. Overview

The Import Events API method creates or modifies events in a longitudinal REDCap project. Events are timepoints or phases within an arm. Each event has a name, label, arm assignment, and offset information.

The `override` parameter controls behavior: when set to `0`, the method adds or modifies events without deleting others; when set to `1`, all existing events are deleted and replaced with the events you provide.

To modify an existing event, provide its `unique_event_name`. If `unique_event_name` is missing from a record and `override=0`, REDCap treats it as a new event to create (an event with a label that's already used gets a suffixed unique name, e.g. `visit_arm_1b`). You can't set the `unique_event_name` yourself — but REDCap **regenerates it when you change the label**: renaming `visit_arm_1` to "Visit renamed" turns it into `visit_renamed_arm_1`.

> **Important:** Events exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project.

> **Important:** In **Development** status this method always works (given the right privileges). In **Production** it is blocked unless a REDCap administrator has enabled the Control Center setting that lets normal users add or modify events while a project is in production. When that setting is on, imports with `override=0` work in Production, but `override=1` is always refused. REDCap administrators are not exempt: the same rules apply to their API tokens.

> **Institution-specific:** Whether normal users may add or modify events in Production is a system-wide choice made by each installation's REDCap administrators. Check with your REDCap administrators before planning event changes on a Production project.

> **Important:** Imports are all-or-nothing. If any row fails validation, no events are created or changed.

---

## 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update privileges and Project Design/Setup privileges. |
| `content` | Required | Always `'event'` for this method. |
| `action` | Required | Always `'import'` for this method. |
| `override` | Optional | `0` = add new events or modify existing ones without deleting others (default); `1` = delete all existing events and replace with the provided set. |
| `format` | Optional | Data format: `'csv'`, `'json'`, or `'xml'`. Default is `'xml'`. |
| `data` | Required | The event records to import. Each record must include `event_name` (the human-readable label, maximum 30 characters) and `arm_num` (the arm the event belongs to; assumes `1` if the project has only one arm — but always include `arm_num` in every row, which is the safest practice). To modify an existing event, you must also provide `unique_event_name`. The optional `custom_event_label` sets the event's custom label. The offset fields `day_offset`, `offset_min`, and `offset_max` are optional and must be numeric (`day_offset` may be negative; `offset_min` and `offset_max` must be 0 or more); if `day_offset` is omitted, events are auto-numbered in the order provided. You can't choose the `unique_event_name`; it is generated from the label and changes when the label changes. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to whatever `format` is set to. If neither is provided, defaults to `'xml'`. Not applicable when using background processing. |

---

## 3. Request Examples

### 3.1 Python

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

### 3.2 R

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

### 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=event&action=import&override=0&format=json&data=[{\"event_name\":\"Event%201\",\"arm_num\":\"1\",\"day_offset\":\"0\",\"offset_min\":\"0\",\"offset_max\":\"0\",\"unique_event_name\":\"event_1_arm_1\"}]"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

### 3.4 PHP

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

## 4. Response

On success, the method returns the number of events imported as a plain integer (not a JSON object). The HTTP status code will be 200.

Example response:
```
3
```

---

## 5. Common Questions

**Q: What is the `unique_event_name` and how does it differ from `event_name`?**

**A:** The `event_name` is the human-readable label (e.g., "Baseline Visit"). The `unique_event_name` is the system identifier used in data exports and API calls (e.g., `event_1_arm_1` or `baseline_visit_arm_1`). The `unique_event_name` must be unique and typically follows the pattern `[event_label]_arm_[arm_num]`.

**Q: What do the offset fields represent?**

**A:** `day_offset` is the expected number of days after enrollment for the event. `offset_min` and `offset_max` define the acceptable window. For example, a visit expected at day 7 with min/max of ±3 days is acceptable from day 4 to day 10. These are used for visit compliance tracking.

**Q: Can I use this method on a classic project?**

**A:** No. Events are a longitudinal-only feature. This method will fail on classic projects.

**Q: My project is in Production. Can I still use Import Events?**

**A:** Only if your REDCap administrators have enabled the Control Center setting that lets normal users add or modify events in production. If it is off, the call is refused, even with an administrator's token. If it is on, imports with `override=0` work, but `override=1` (replace all events) is always refused in Production. Ask your REDCap administrators which applies on your installation.

**Q: If I update an existing event, do I only need to send the columns I want to change?**

**A:** No. An update overwrites the whole event with the row you send. Columns you leave out are not kept: an omitted `day_offset` is reset to the row's position in your data, omitted `offset_min` and `offset_max` are reset to `0`, and an omitted `custom_event_label` is cleared. Always send full rows, ideally taken from Export Events ([RC-API-19 — Export Events API](RC-API-19_Export-Events.md)) and edited.

**Q: Do I need any special permissions beyond API access?**

**A:** Yes. You need both **API Import/Update** privileges and **Project Design/Setup** privileges in the project. API Export rights alone are not sufficient.

**Q: What happens if I specify an `arm_num` that does not exist?**

**A:** The API returns the error `The arm number "N" does not exist in the project.` and imports nothing. You must specify `arm_num` values that correspond to existing arms in the project. Use Export Arms ([RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md)) to discover valid arm numbers.

---

## 6. Common Mistakes & Gotchas

**Calling Import Events on a classic project.** Events are a longitudinal-only feature. This method will fail on classic projects. Always verify your project is longitudinal before calling this method.

**Calling Import Events on a Production project.** In Production the call is refused unless your administrators have enabled the Control Center setting that lets normal users add or modify events in production, and `override=1` is refused in Production even then. Administrators' tokens follow the same rules. Check with your REDCap administrators before relying on this in Production.

**Sending partial rows when updating an event.** An update replaces the event's settings with exactly what you send: omitted offsets are reset (`day_offset` to the row's position, `offset_min`/`offset_max` to `0`) and an omitted `custom_event_label` is cleared. Export the events first ([RC-API-19 — Export Events API](RC-API-19_Export-Events.md)), edit those full rows, and import them back.

**Leaving out `arm_num`.** Include `arm_num` in every row, even in a one-arm project. It is the safest practice and removes any doubt about which arm an event belongs to.

**Using an `event_name` longer than 30 characters.** Event names are limited to 30 characters. Because imports are all-or-nothing, one invalid row stops the whole import.

**Forgetting to JSON-encode the `data` parameter.** The `data` parameter must be a valid JSON array. Use `json.dumps()` in Python, `toJSON()` in R, or `json_encode()` in PHP to properly format it.

**Using `event_name` when you should use `unique_event_name`.** The `event_name` is the label; the `unique_event_name` is the identifier. In other API calls, always use `unique_event_name`.

**Renaming an event breaks references to it.** Changing `event_name` for an existing event also changes its `unique_event_name` (`visit_arm_1` → `visit_renamed_arm_1`). Branching logic, calculations, reports, `events=` filters and scripts that use the old unique name stop working. Use `custom_event_label` if you only want a different display name.

**Using `override=1` when you only want to add a single event.** The `override=1` flag deletes all existing events, and all record data in them. If you only want to add or modify one event, use `override=0` instead.

---

## 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-19 — Export Events API](RC-API-19_Export-Events.md) (retrieve event metadata from a project)
- [RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md) (remove events from a project)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (how events are structured; use case for programmatic import)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (how repeating events integrate with the event structure)
