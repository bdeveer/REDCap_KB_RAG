RC-API-53

**Import Repeating Instruments and Events API**

| **Article ID** | RC-API-53 |
|---|---|
| **Domain** | API |
| **Applies To** | Projects with repeating instruments or repeating events |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API official documentation |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-51 — Export Repeating Instruments and Events; RC-API-09 — Export Instruments; RC-API-10 — Export Instrument-Event Mappings; RC-LONG-02 — Repeated Instruments & Events Setup |

---

# 1. Overview

The Import Repeating Instruments and Events API method configures which instruments and events in a project are designated as repeating. It does not import record data — it modifies the project's structural configuration by defining which instruments or events are set to repeat.

Each item submitted must include the instrument's internal name (as it appears in the second column of the Data Dictionary) and, optionally, a custom repeating instrument label. For longitudinal projects, the unique event name must also be provided to identify which event the repeating instrument belongs to.

Repeating events must be submitted as separate items with a blank or null instrument name, which signals that the entire event repeats rather than a single instrument within it.

When to use this method: when programmatically configuring a project's repeating structure, replicating a repeating setup from one project to another, or automating project setup workflows via the API.

---

# 2. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

# 3. Permissions Required

To call this method, the API token's owner must have both **API Import/Update** privilege **and** **Project Setup/Design** privilege in the project. Both are required; neither alone is sufficient.

Super API Tokens (issued by a REDCap administrator via the API Tokens page in the Control Center) can also be used for this method in place of a project-level API token.

---

# 4. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token (or Super API Token). Requires API Import/Update and Project Setup/Design rights. |
| `content` | Required | Always `'repeatingFormsEvents'` for this method. |
| `format` | Optional | Format of the data being submitted: `'csv'`, `'json'`, or `'xml'` (default). |
| `data` | Required | The repeating instrument/event definitions to import, in the format specified. |
| `returnFormat` | Optional | Format of error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to the value of `format` if not provided, or `'xml'` if neither is set. Not applicable when using background processing. |

---

# 5. Data Structure

The `data` payload follows the same structure as the export response from RC-API-51. Each item represents one repeating instrument or one repeating event.

**Key fields:**

| Field | Description |
|---|---|
| `event_name` | The unique event name (longitudinal projects only; leave blank for classic projects). |
| `form_name` | The instrument's internal name. **Leave blank/null to indicate a repeating event** rather than a repeating instrument. |
| `custom_repeat_instrument_label` | Optional custom label for the repeating instrument instance header. Leave empty to use the default. |

**JSON example — classic project:**
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

**JSON example — longitudinal project with a repeating event:**
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

In the second entry above, `form_name` is blank, configuring `follow_up_arm_1` as a repeating event.

---

# 6. Request Examples

## 6.1 Python

```python
#!/usr/bin/env python

import json
from config import config
import requests

data = [
    {
        "event_name": "",
        "form_name": "adverse_events",
        "custom_repeat_instrument_label": "Adverse Event"
    }
]

fields = {
    'token': config['api_token'],
    'content': 'repeatingFormsEvents',
    'format': 'json',
    'data': json.dumps(data)
}

r = requests.post(config['api_url'], data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 6.2 R

```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)
library(jsonlite)

data <- toJSON(list(
    list(event_name="", form_name="adverse_events", custom_repeat_instrument_label="Adverse Event")
))

result <- postForm(
    api_url,
    token=api_token,
    content='repeatingFormsEvents',
    format='json',
    data=data
)
print(result)
```

## 6.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=repeatingFormsEvents&format=json&data=[{\"event_name\":\"\",\"form_name\":\"adverse_events\",\"custom_repeat_instrument_label\":\"Adverse Event\"}]"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -X POST \
      -d $DATA \
      $API_URL
```

## 6.4 PHP

```php
<?php

include 'config.php';

$data = json_encode(array(
    array(
        'event_name' => '',
        'form_name' => 'adverse_events',
        'custom_repeat_instrument_label' => 'Adverse Event'
    )
));

$fields = array(
    'token'   => $GLOBALS['api_token'],
    'content' => 'repeatingFormsEvents',
    'format'  => 'json',
    'data'    => $data
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

# 7. Response

On success, the method returns the **number of repeating instruments or repeating events that were imported** as an integer.

```
2
```

On failure, an error message is returned in the format specified by `returnFormat`.

---

# 8. Common Questions

**Q: Does this method add to the existing repeating configuration, or does it replace it?**

**A:** This method replaces the project's repeating instrument/event configuration entirely. Any instruments or events not included in the submitted data will no longer be configured as repeating after the call. If you want to preserve existing entries, export them first with RC-API-51 and merge before re-importing.

**Q: Can I use this method to configure repeating instruments on a project that has existing record data?**

**A:** REDCap does allow changes to the repeating configuration after data collection has started, but this should be done with caution. Adding a repeating designation to an instrument that already has data may affect how instances are counted and displayed. Test on a development copy first.

**Q: What does the return value represent?**

**A:** The integer returned is the count of repeating instrument or event entries successfully imported — not the number of records or instances affected.

**Q: What is a Super API Token, and when would I use it here?**

**A:** A Super API Token is a special token issued by a REDCap administrator that grants cross-project API access. It is typically used in administrative or automation scripts. For most users, a standard project-level API token is appropriate.

**Q: How do I indicate a repeating event vs. a repeating instrument?**

**A:** Leave `form_name` blank or null to configure a repeating event. Provide a value in `form_name` to configure a repeating instrument. This mirrors the convention used in the export method (RC-API-51).

---

# 9. Common Mistakes & Gotchas

**Submitting a partial list and losing existing configuration.** This method overwrites the full repeating configuration. If you only include one instrument in the payload, all other repeating instruments are removed. Always export the current configuration first (RC-API-51) and merge your changes before importing.

**Forgetting Project Setup/Design permission.** This method requires both API Import/Update and Project Setup/Design. A token with only API Import/Update will receive a permissions error. Confirm both privileges are enabled in User Rights.

**Using instrument labels instead of internal names.** The `form_name` field must be the internal instrument name from the Data Dictionary (e.g., `adverse_events`), not the human-readable label (e.g., `Adverse Events`). Using the label causes a validation error.

**Omitting event_name in longitudinal projects.** In a longitudinal project, each repeating instrument entry must include the correct `event_name`. Omitting it or providing a wrong event name will result in an error or misassignment.

**Misreading the return value.** The method returns a count of imported entries, not a success/failure boolean. A return of `0` may indicate that no items were actually processed — verify your payload if you receive an unexpected zero.

---

# 10. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-51 — Export Repeating Instruments and Events (retrieve current repeating configuration before importing)
- RC-API-09 — Export Instruments (get full instrument list to verify form names before importing)
- RC-API-10 — Export Instrument-Event Mappings (confirm event-instrument assignments in longitudinal projects)
- RC-LONG-02 — Repeated Instruments & Events Setup (configuring repeating instruments and events via the UI)
