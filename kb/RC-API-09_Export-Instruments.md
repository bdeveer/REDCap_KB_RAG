RC-API-09

**Export Instruments API**

| **Article ID** | RC-API-09 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-07 — Export Metadata; RC-API-15 — Export Instruments PDF |

---

# 1. Overview

The Export Instruments API method retrieves a list of all instruments (forms) defined in a REDCap project. Each instrument has metadata including its name, display name, and other properties. This method provides a lightweight way to discover the structure of a project's instruments without downloading the full data dictionary.

When to use this method: When you need to list all instruments in a project, discover instrument names for use in other API calls, or build dynamic menus or forms based on a project's instruments.

---

# 2. Endpoint

```
POST https://your-redcap-instance.edu/api/
```

Only `POST` is supported.

---

# 3. Permissions Required

To call this method, the API token's owner must have **API Export** privilege in the project. Calls from tokens lacking this privilege will fail with a permissions error.

---

# 4. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'instrument'` for this method. |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'` (default). |
| `returnFormat` | Optional | Format of error messages (does not affect a successful response shape): `'csv'`, `'json'`, or `'xml'`. |

---

# 5. Request Examples

## 5.1 Python

```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'instrument',
    'format': 'json'
}

r = requests.post(config['api_url'],data=fields)
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
    content='instrument',
    format='json'
)
print(result)
```

## 5.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=instrument&format=json"

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
	'content' => 'instrument',
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

The method returns the project's instruments in the requested format, **ordered according to their order in the project** (matching the instrument ordering shown on the project's left-hand menu and in the Data Dictionary). Each instrument has an internal name (`instrument_name`) and a display label (`instrument_label`).

**JSON format:**
```json
[
  {
    "instrument_name": "demographics",
    "instrument_label": "Demographics"
  },
  {
    "instrument_name": "medical_history",
    "instrument_label": "Medical History"
  },
  {
    "instrument_name": "lab_results",
    "instrument_label": "Lab Results"
  }
]
```

**CSV format:** A table with columns for instrument_name and instrument_label, one row per instrument.

---

# 7. Common Questions

**Q: What's the difference between instrument_name and instrument_label?**

**A:** The `instrument_name` is the internal identifier used in API calls, data exports, and field definitions (the Data Dictionary form_name column). The `instrument_label` is the human-readable name displayed to users. For example, name: `demographics`, label: `Demographics`.

**Q: Can I use the instrument names returned by this API in other API calls?**

**A:** Yes. The instrument_name returned by this method is the same value you use in the `forms` parameter when exporting records (RC-API-02) or in the form_name column when working with the data dictionary.

**Q: Does this method include disabled or hidden instruments?**

**A:** No, this method returns only active instruments. Instruments that have been disabled are not included in the response.

**Q: In a longitudinal project, are instruments listed per event?**

**A:** No, this method returns only the list of instruments themselves, not their event assignments. To see which instruments are assigned to which events, use RC-API-10 (Export Instrument-Event Mappings).

**Q: Can I use this to discover system fields like record_id?**

**A:** No, system fields like record_id are not in instruments; they are special project properties. This method returns only user-defined instruments (forms).

---

# 8. Common Mistakes & Gotchas

**Assuming all returned names are instruments.** This method returns only form (instrument) names. Do not confuse these with field names or event names.

**Not using the correct name in follow-up calls.** Always use instrument_name (not instrument_label) in API calls that accept form or instrument parameters. Using the label instead of the name causes API errors.

**Expecting detailed instrument properties.** This method returns only the name and label. To get detailed information about fields within an instrument, use RC-API-07 (Export Metadata) and filter by form_name.

**Forgetting to specify format.** Always explicitly set the `format` parameter. Different formats may be useful for different downstream systems.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-02 — Export Records (use instrument names to export specific forms)
- RC-API-07 — Export Metadata (get detailed field information within instruments)
- RC-API-10 — Export Instrument-Event Mappings (see instrument assignments in longitudinal projects)
- RC-API-15 — Export Instruments PDF (export instrument as PDF files)
- RC-FD-01 — Form Design Overview (instrument design concepts and terminology)
- RC-FD-02 — Online Designer (the GUI for creating and managing instruments)
