RC-API-10

**Export Instrument-Event Mappings API**

| **Article ID** | RC-API-10 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-09 — Export Instruments; RC-API-11 — Import Instrument-Event Mappings; RC-API-20 — Import Events |
| **Important** | **Longitudinal projects only** — This method is only available for longitudinal projects (projects with multiple arms and/or repeating events). Classic projects do not have instrument-event mappings. |

---

# 1. Overview

The Export Instrument-Event Mappings API method retrieves the mapping of instruments (forms) to events in a longitudinal REDCap project. This mapping defines which instruments are presented to users at each event and repeating instance. This method shows the complete structure of when and where instruments appear in a longitudinal workflow.

When to use this method: When you need to understand the instrument-event structure of a longitudinal project, programmatically verify which instruments are assigned to which events, export and clone the mapping structure, or validate event setup.

---

# 2. Important Notes

- **Longitudinal Only:** This method only works with longitudinal projects. If you use it on a classic (non-longitudinal) project, it returns an error or empty result.
- **Requires API Export Right:** You must have API Export permission on the project.
- **Read-Only:** This method only exports mappings. To modify mappings, use RC-API-11 (Import Instrument-Event Mappings).

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'formEventMapping'` for this method. |
| `format` | Required | Response format: `'csv'`, `'json'`, or `'xml'` [default: `xml`]. |
| `arms` | Optional | An array of arm numbers to filter results to specific arms. By default, mappings for all arms are returned. |
| `returnFormat` | Optional | Specifies the format of error messages: `'csv'`, `'json'`, or `'xml'`. If omitted, defaults to the `format` value (or `xml` if `format` was also omitted). Does not apply when using a background process (`backgroundProcess=true`) — in that case, `success:true` or `success:false` is returned in the appropriate format. |

---

# 4. Request Examples

## 4.1 Python

```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'formEventMapping',
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
    content='formEventMapping',
    format='json'
)
print(result)
```

## 4.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=formEventMapping&format=json"

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
	'content' => 'formEventMapping',
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
?>
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 for why SSL certificate validation matters.

---

# 5. Response

The method returns the mapping of instruments to events, organized by arm and event. The response shows which instruments are assigned to each event in the project.

**JSON format (example):**
```json
[
  {
    "arm_num": "1",
    "unique_event_name": "visit_1_arm_1",
    "form": "demographics"
  },
  {
    "arm_num": "1",
    "unique_event_name": "visit_1_arm_1",
    "form": "medical_history"
  },
  {
    "arm_num": "1",
    "unique_event_name": "visit_2_arm_1",
    "form": "lab_results"
  },
  {
    "arm_num": "2",
    "unique_event_name": "visit_1_arm_2",
    "form": "demographics"
  }
]
```

**CSV format:** A table with columns arm_num, unique_event_name, and form, with one row per instrument-event mapping.

---

# 6. Common Questions

**Q: What do the columns mean in the response?**

**A:** `arm_num` is the arm number; `unique_event_name` is the unique event identifier (used in API calls); `form` is the instrument (form) name. Together, these define: "In arm 1, at event visit_1_arm_1, the instrument demographics is available."

**Q: Can I modify mappings using this API?**

**A:** No, this method is read-only. To modify instrument-event mappings, use RC-API-11 (Import Instrument-Event Mappings).

**Q: How do repeating instruments appear in this output?**

**A:** Repeating instruments are still listed as mappings to events. To determine if an instrument is repeating at an event, you may need to check project settings or use other API endpoints that provide additional metadata about repeating instruments.

**Q: What is unique_event_name?**

**A:** The unique_event_name is the REDCap-generated unique identifier for an event. It's typically in the format "event_name_arm_X" and is used in API calls when specifying events (e.g., in the `events` parameter of RC-API-02).

**Q: Can I use this to clone a longitudinal project's structure?**

**A:** Yes. Export the mappings from the source project, export events (RC-API-20), export instruments (RC-API-09), and export metadata (RC-API-07). Use these to recreate the structure in a new project.

**Q: Can I retrieve mappings for just one arm instead of all arms?**

**A:** Yes. Pass the `arms` parameter with an array of arm numbers (e.g., `arms[0]=1`). Only mappings for the specified arm(s) will be returned. If you omit `arms`, all arms are included.

---

# 7. Common Mistakes & Gotchas

**Not specifying `format` and getting XML back unexpectedly.** The default format for this method is `xml`, not `json`. If you omit the `format` parameter, you will receive an XML response. Always pass `format=json` (or `format=csv`) explicitly if you want non-XML output.

**Using on a classic (non-longitudinal) project.** This method does not work on classic projects. If you call it on a non-longitudinal project, you get an error or empty result. Always verify the project is longitudinal first.

**Confusing form and instrument names.** The `form` column in the response contains instrument (form) names, not field names. Do not try to use these names as field names in other API calls.

**Assuming all instruments are in all events.** The mappings show only the actual assignments. An instrument that is not assigned to an event will not appear in the response. Do not assume all instruments are available at all events.

**Not understanding arm numbers.** In multi-arm projects, the same event can exist in multiple arms with different mappings. The arm_num disambiguates which arm each mapping belongs to.

**Forgetting repeating events.** If your project has repeating events (multiple instances of the same event), the mappings still show only the event name, not the repeat instance. Repeat instances are handled separately in data structures.

---

# 8. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-09 — Export Instruments (list available instruments)
- RC-API-11 — Import Instrument-Event Mappings (modify the mappings)
- RC-API-20 — Import Events (create or update events)
- RC-LONG-01 — Longitudinal Project Setup (how arms and events are configured; instrument-event mapping context)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeating instruments affect event mappings)
