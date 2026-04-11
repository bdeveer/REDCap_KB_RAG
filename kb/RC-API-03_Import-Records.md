RC-API-03

**Import Records API**

| **Article ID** | RC-API-03 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-02 — Export Records; RC-API-04 — Delete Records; RC-API-07 — Export Metadata |

---

# 1. Overview

The Import Records API method writes record data into a REDCap project. This is the primary way to programmatically create new records or update existing records in an automated workflow. You provide record data in JSON, CSV, or XML format, and the API creates or updates the records based on the record ID and the overwrite behavior you specify.

When to use this method: When you need to load data from an external system into REDCap, create records in bulk, update field values via automation, or sync data between systems.

**Important note:** The Data Entry Trigger (DET) is NOT fired by API imports. If your workflow depends on triggering an external notification on data import, the DET alone is insufficient — you must implement your own notification logic after the import completes.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import right. |
| `content` | Required | Always `'record'` for this method. |
| `format` | Required | Data format: `'json'`, `'csv'`, or `'xml'`. Must match the structure of the `data` parameter. |
| `type` | Optional | Data structure: `'flat'` (default) or `'eav'` (entity-attribute-value). |
| `data` | Required | The record data to import, formatted as JSON, CSV, or XML string. |
| `overwriteBehavior` | Optional | How to handle existing records: `'normal'` (default; blank fields are ignored) or `'overwrite'` (blank fields overwrite existing values). |
| `dateFormat` | Optional | Date format: `'MDY'` (default; MM/DD/YYYY), `'DMY'` (DD/MM/YYYY), or `'YMD'` (YYYY-MM-DD). |
| `returnContent` | Optional | What to return: `'count'` (default; returns count of imported records), `'ids'` (returns array of record IDs), or `'auto_ids'` (auto-generated record IDs). |
| `forceAutoNumber` | Optional | `true` or `false` (default). If `true`, auto-numbers the record ID field even if a record ID is provided in the data. |
| `returnFormat` | Optional | Response format (alternative to `format` parameter): `'json'`, `'csv'`, or `'xml'`. |

---

# 3. Request Examples

## 3.1 Python

```python
#!/usr/bin/env python

from config import config
import requests, hashlib, json

record = {
    'record_id': hashlib.sha1().hexdigest()[:16],
    'first_name': 'First',
    'last_name': 'Last',
    'address': '123 Cherry Lane\nNashville, TN 37015',
    'telephone': '(615) 255-4000',
    'email': 'first.last@gmail.com',
    'dob': '1972-08-10',
    'age': 43,
    'ethnicity': 1,
    'race': 4,
    'sex': 1,
    'height': 180,
    'weight': 105,
    'bmi': 31.4,
    'comments': 'comments go here',
    'redcap_event_name': 'events_2_arm_1',
    'basic_demography_form_complete': '2',
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'record',
    'format': 'json',
    'type': 'flat',
    'data': data,
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
library(digest)
library(jsonlite)

record_id = substr(digest(Sys.time(), algo='sha1'), 0, 16)

record <- c(
    record_id=record_id,
    first_name='First',
    last_name='Last',
    address='123 Cherry Lane\nNashville, TN 37015',
    telephone='(615) 255-4000',
    email='first.last@gmail.com',
    dob='1972-08-10',
    age=43,
    ethnicity=1,
    race=4,
    sex=1,
    height=180,
    weight=105,
    bmi=31.4,
    comments='comments go here',
    redcap_event_name='event_1_arm_1',
    basic_demography_form_complete='2'
)

data <- toJSON(list(as.list(record)), auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='record',
    format='json',
    type='flat',
    data=data
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh

. ./config

RECORD_ID=`date | openssl sha1 -hmac | tail -c 16`

DATA="token=$API_TOKEN&content=record&format=json&type=flat&data=[{\"record_id\":\"$RECORD_ID\",\"first_name\":\"First\",\"last_name\":\"Last\",\"address\":\"123%20Cherry%20Lane\nNashville,%20TN%2037015\",\"telephone\":\"(615)%20255-4000\",\"email\":\"first.last@gmail.com\",\"dob\":\"1972-08-10\",\"age\":\"43\",\"ethnicity\":\"1\",\"race\":\"4\",\"sex\":\"1\",\"height\":\"180\",\"weight\":\"105\",\"bmi\":\"32.4\",\"comments\":\"comments%20go%20here\",\"redcap_event_name\":\"event_1_arm_1\",\"basic_demography_form_complete\":\"2\"}]"

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

$record = array(
	'record_id' => substr(sha1(microtime()), 0, 16),
	'first_name' => 'First',
	'last_name' => 'Last',
	'address' => '123 Cherry Lane\nNashville, TN 37015',
	'telephone' => '(615) 255-4000',
	'email' => 'first.last@gmail.com',
	'dob' => '1972-08-10',
	'age' => '43',
	'ethnicity' => '1',
	'race' => '4',
	'sex' => '1',
	'height' => '180',
	'weight' => '105',
	'bmi' => '31.4',
	'comments' => 'comments go here',
	'redcap_event_name' => 'event_1_arm_1',
	'basic_demography_form_complete' => '2',
);

$data = json_encode( array( $record ) );

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'record',
	'format'  => 'json',
	'type'    => 'flat',
	'data'    => $data,
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

# 4. Response

On success, the API returns one of the following based on the `returnContent` parameter:

- **`returnContent='count'` (default):** Returns the number of records imported (e.g., `1`).
- **`returnContent='ids'`:** Returns a JSON array of record IDs that were imported.
- **`returnContent='auto_ids'`:** Returns a JSON array of auto-numbered record IDs if `forceAutoNumber` is `true`.

On error, the API returns an error message describing what went wrong (e.g., missing required fields, invalid field names, validation errors).

---

# 5. Common Questions

**Q: What's the difference between normal and overwrite behavior?**

**A:** In `'normal'` mode (default), if a record already exists, blank fields in the import data are ignored — existing values are preserved. In `'overwrite'` mode, blank fields overwrite (erase) existing values. Use overwrite mode only if you want to clear fields explicitly.

**Q: Can I import data into a longitudinal project's specific event?**

**A:** Yes. Include the `redcap_event_name` field in your data to specify which event the record belongs to. For example, `'redcap_event_name': 'visit_1_arm_1'` imports the record into that event.

**Q: What happens if I import a record with an ID that already exists?**

**A:** In normal behavior, the import updates the existing record. In overwrite behavior, the import updates the existing record and blank fields erase existing values. If you want to force creation of a new record with an auto-numbered ID, set `forceAutoNumber` to `true`.

**Q: Can I import choice field values using the raw numeric code or only the label?**

**A:** You should use the raw numeric code for choice fields. If you import a label string by mistake, the API will likely fail validation or store the wrong value.

**Q: Does importing data fire the Data Entry Trigger?**

**A:** No. The Data Entry Trigger fires only on interactive saves via the REDCap interface. API imports do not fire it. If you need to notify external systems of imported data, implement your own notification logic after the import completes.

**Q: How many records can I import in a single request?**

**A:** The API has no hard limit, but very large imports (thousands of records) may timeout. If your import is large, consider splitting it into batches.

---

# 6. Common Mistakes & Gotchas

**Forgetting to JSON-encode the data parameter.** The `data` parameter must be a JSON, CSV, or XML string — not a native object or array. Depending on your language, you must serialize the data first using `json.dumps()`, `toJSON()`, or equivalent.

**Using the wrong field names.** Field names in the import data must exactly match the variable names in the data dictionary. A typo or using the field label instead of the variable name will cause the API to ignore that field or return an error.

**Assuming blank fields don't matter in normal mode.** In normal mode, including blank fields in your import data is harmless — they are ignored. But be aware of this behavior if you're expecting an update to clear a field. Use overwrite mode if you need to explicitly clear values.

**Not handling validation errors.** If your import data contains invalid values (e.g., text in a numeric field, an invalid date, or a non-existent choice code), the API will return an error and the import will fail. Validate your data before importing.

**Mixing up record_id and redcap_event_name.** In a longitudinal project, the record ID and event name are separate. `record_id` identifies the participant; `redcap_event_name` identifies the visit or time point. Both are usually required in longitudinal imports.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-02 — Export Records (reading data from REDCap)
- RC-API-04 — Delete Records (removing records)
- RC-API-07 — Export Metadata (get the data dictionary to understand field names)
- RC-INTG-01 — Data Entry Trigger (explains why DET does not fire on API imports)
- RC-IMP-01 — Data Import Overview (manual import workflow and formatting rules)
- RC-DAG-01 — Data Access Groups (how DAGs affect imported data)
- RC-LONG-02 — Repeated Instruments & Events Setup (repeat instance handling in imports)
