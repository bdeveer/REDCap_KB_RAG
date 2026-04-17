RC-API-51

**Export Repeating Instruments and Events API**

| **Article ID** | RC-API-51 |
|---|---|
| **Domain** | API |
| **Applies To** | Projects with repeating instruments or repeating events |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API official documentation |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-09 — Export Instruments; RC-API-10 — Export Instrument-Event Mappings; RC-API-19 — Export Events; RC-LONG-02 — Repeated Instruments & Events Setup |

---

# 1. Overview

The Export Repeating Instruments and Events API method retrieves a list of all repeating instruments and repeating events configured for a project. It does not return all instruments in a project — only those that have been designated as repeating.

Each result includes the instrument's internal name (as it appears in the second column of the Data Dictionary), along with its custom repeating instrument label if one has been set. For longitudinal projects, the unique event name is also returned for each repeating instrument, indicating which event the repeating instrument belongs to.

Repeating events are returned as separate items in the response. You can identify them because the instrument name field is blank or null — a blank instrument name signals that an entire event repeats, rather than a single instrument.

When to use this method: when you need to programmatically determine which instruments or events are configured as repeating, discover event-instrument pairings for repeating forms in longitudinal projects, or build logic that handles repeated instances differently from non-repeated data.

---

# 2. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

# 3. Permissions Required

To call this method, the API token's owner must have both **API Export** privilege **and** **Project Setup/Design** privilege in the project. This is a higher permission requirement than most export methods, which require only API Export.

---

# 4. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export and Project Setup/Design rights. |
| `content` | Required | Always `'repeatingFormsEvents'` for this method. |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'` (default). |

---

# 5. Request Examples

## 5.1 Python

```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'repeatingFormsEvents',
    'format': 'json'
}

r = requests.post(config['api_url'], data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 5.2 R

```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='repeatingFormsEvents',
    format='json'
)
print(result)
```

## 5.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=repeatingFormsEvents&format=json"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

## 5.4 PHP

```php
<?php

include 'config.php';

$fields = array(
    'token'   => $GLOBALS['api_token'],
    'content' => 'repeatingFormsEvents',
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

# 6. Response

The method returns results ordered according to their order in the project. Each row or object represents either a repeating instrument or a repeating event.

**Key fields:**

| Field | Description |
|---|---|
| `event_name` | The unique event name (longitudinal projects only; blank for classic projects) |
| `form_name` | The instrument's internal name. **Blank/null if this row represents a repeating event** (rather than a repeating instrument). |
| `custom_repeat_instrument_label` | The custom label configured for this repeating instrument. Empty if no custom label was set. |

**JSON format — classic project (repeating instruments only):**
```json
[
  {
    "event_name": "",
    "form_name": "adverse_events",
    "custom_repeat_instrument_label": "Adverse Event"
  },
  {
    "event_name": "",
    "form_name": "medications",
    "custom_repeat_instrument_label": ""
  }
]
```

**JSON format — longitudinal project (mix of repeating instruments and repeating events):**
```json
[
  {
    "event_name": "visit_arm_1",
    "form_name": "lab_results",
    "custom_repeat_instrument_label": "Lab Draw"
  },
  {
    "event_name": "follow_up_arm_1",
    "form_name": "",
    "custom_repeat_instrument_label": ""
  }
]
```

In the second entry above, `form_name` is blank, indicating that the entire `follow_up_arm_1` event is configured as a repeating event.

---

# 7. Common Questions

**Q: How do I tell the difference between a repeating instrument and a repeating event in the response?**

**A:** Look at the `form_name` field. If it has a value, the row is a repeating instrument. If `form_name` is blank or null, the row represents a repeating event (the entire event repeats rather than a single instrument within it).

**Q: Does this method return all instruments, or only the repeating ones?**

**A:** Only repeating instruments and repeating events are returned. Instruments that are not configured as repeating do not appear. Use RC-API-09 (Export Instruments) to get a full list of all instruments in the project.

**Q: Why does this method require Project Setup/Design privilege in addition to API Export?**

**A:** REDCap treats information about which instruments are repeating as project configuration metadata, not just data. The Project Setup/Design privilege is required to access configuration-level details via the API. This is the same permission needed to configure repeating instruments in the project setup UI.

**Q: Does this method work for classic (non-longitudinal) projects?**

**A:** Yes. For classic projects, the `event_name` field will be blank, and the response will list only repeating instruments. Repeating events are only applicable to longitudinal projects.

**Q: What is the custom_repeat_instrument_label?**

**A:** When a project designer enables repeating for an instrument, they can optionally provide a custom label that will appear in the repeating instances table header in the data entry UI (e.g., "Adverse Event" instead of the generic "Repeat Instrument"). This field returns that label. If none was set, the field is empty.

---

# 8. Common Mistakes & Gotchas

**Assuming all instruments appear in the response.** This method only returns instruments configured as repeating. Non-repeating instruments are excluded entirely. If you need the full instrument list, call RC-API-09 separately.

**Misreading blank form_name as an error.** A blank `form_name` in the response is intentional — it signals a repeating event, not missing data. Always check for this before processing the result set.

**Forgetting the Project Setup/Design permission.** Most API export calls require only API Export. This method also requires Project Setup/Design. If a user's token lacks this permission, the call returns a permissions error even though the token is otherwise valid. Confirm both privileges are enabled in User Rights.

**Using form_name values in the wrong context.** The `form_name` returned here matches the instrument name in the Data Dictionary (form_name column) and in other API calls like RC-API-02 (Export Records). Do not confuse it with the human-readable instrument label.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-09 — Export Instruments (full list of all instruments; not just repeating)
- RC-API-10 — Export Instrument-Event Mappings (which instruments are assigned to which events in longitudinal projects)
- RC-API-19 — Export Events (list all events in a longitudinal project)
- RC-LONG-02 — Repeated Instruments & Events Setup (configuring repeating instruments and events via the UI)
