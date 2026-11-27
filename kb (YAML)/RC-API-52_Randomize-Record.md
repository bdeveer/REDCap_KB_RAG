---
id: RC-API-52
title: Randomize Record API
domain: API
applies_to:
- REDCap projects with Randomization enabled
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Randomize
  Record behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
- RC-RAND-01 — Randomization Concepts & Terminology
version: '1.1'
last_updated: 2026-11
source: REDCap API official documentation
related:
- id: RC-API-01
  title: REDCap API
- id: RC-RAND-01
  title: Randomization Concepts & Terminology
- id: RC-RAND-02
  title: Randomization Setup Guide
- id: RC-RAND-03
  title: Working with & Managing Randomization
tags:
- api
synonyms:
- randomize record api method
- how do i randomize a record via the api
- api call to trigger randomization for a record
- programmatically randomize an existing record with the api
- api method to perform randomization through the api
- randomize a participant by record id using the api
- assign randomization allocation via the api
---

# 1. Overview

The Randomize Record API method triggers the randomization of an existing record in a REDCap project. It performs the same action as manually randomizing a record through the REDCap UI, but programmatically via the API.

The method requires that the record already exists and that all stratification fields for the specified randomization have been filled in. If stratification data is missing or incomplete, the call will fail with an error.

You must specify a `randomization_id`, which corresponds to a specific randomization definition (target field + event). Projects can have multiple randomization definitions; the `randomization_id` tells REDCap which one to use. This ID is shown on the project's Randomization page (setup or dashboard view, which requires Randomization Setup or Dashboard rights) or on the API Playground page.

**Concealed vs. open allocations:** For open allocations, the actual allocation group value is returned. For concealed allocations, the `target_field_alt` value is always `'*'` to preserve blinding — the real allocation group is not exposed.

---

# 2. Key Concepts & Definitions

### Randomization
The process of assigning a record to a treatment group or allocation value based on a randomization definition configured in REDCap, often with stratification and optional concealment to maintain blinding.

### Randomization ID
A numeric identifier for a specific randomization definition in the project. Identifies which target field and event pair to randomize for.

### Stratification
One or more fields that must be populated before a record can be randomized. Used to balance treatment assignments across strata (e.g., age groups, gender).

### Concealed Allocation
A randomization setup where the actual treatment group assigned is hidden behind a code or masked value (represented as '*') to prevent bias.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires **Randomize** privilege in the project. |
| `content` | Required | Always `'record'` |
| `action` | Required | Always `'randomize'` |
| `record` | Required | The record name (ID) of the record to randomize. Must already exist and have all stratification data filled in. |
| `randomization_id` | Required | The unique ID of the randomization definition. Viewable on the Randomization page or API Playground. |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'` (default). |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to match `format` if not specified. |
| `returnAlt` | Optional | `'false'` (default) or `'true'`. When `'true'`, includes the alternative target field value (i.e., the randomization number for open allocations). For concealed allocations, always returns `'*'`. |

---

# 4. Request Examples

## 4.1 Python

```python
#!/usr/bin/env python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'record',
    'action': 'randomize',
    'record': '21',
    'randomization_id': '123',
    'format': 'json',
    'returnFormat': 'json',
    'returnAlt': 'true'
}
r = requests.post(config['api_url'], data=fields)
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
    content='record',
    action='randomize',
    record='21',
    randomization_id='123',
    format='json',
    returnFormat='json',
    returnAlt='true'
)
print(result)
```

## 4.3 cURL

```sh
#!/bin/sh
. ./config

DATA="token=$API_TOKEN&content=record&action=randomize&record=21&randomization_id=123&format=json&returnFormat=json&returnAlt=true"

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

$data = array(
    'token'              => $GLOBALS['api_token'],
    'content'            => 'record',
    'action'             => 'randomize',
    'record'             => '21',
    'randomization_id'   => '123',
    'format'             => 'json',
    'returnFormat'       => 'json',
    'returnAlt'          => 'true'
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $GLOBALS['api_url']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE); // Set to TRUE for production use
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data, '', '&'));
$output = curl_exec($ch);
print $output;
?>
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) Section 3.5.

---

# 5. Response

On success, returns the randomization result. The response includes the randomization ID, the record name, the variable name of the target field (`target_field_name`), the value assigned to it (`target_field`), and (if `returnAlt=true`) the alternative target field value. `target_field_name` is included in JSON, CSV and XML responses.

**JSON:**
```json
{
    "randomization_id": 123,
    "record": "21",
    "target_field_name": "randomization_group",
    "target_field": "1",
    "target_field_alt": "R-1005"
}
```

**CSV:**
```
randomization_id,record,target_field_name,target_field,target_field_alt
123,21,randomization_group,1,R-1005
```

**XML:**
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<items>
    <randomization_id>123</randomization_id>
    <record>21</record>
    <target_field_name>randomization_group</target_field_name>
    <target_field>1</target_field>
    <target_field_alt>R-1005</target_field_alt>
</items>
```

> **Note:** The XML root element is `<items>`, although REDCap's own API help page shows `<item>`.

**Errors.** Most "cannot randomize" failures come back as an HTTP 200 response with a plain-text message (not wrapped in the `returnFormat`). The messages are:

- `Invalid data supplied` (bad `randomization_id`, or randomization is not enabled in the project)
- `Cannot randomize. Record does not exist.`
- `Cannot randomize. Randomization already completed for record.`
- `Cannot randomize. Missing stratification data for fields: <fields>`
- `Cannot randomize. Record not assigned to a DAG`
- `Cannot randomize. No allocations available.`

Only permission problems (403), DAG or Double Data Entry access problems (403), and `Cannot randomize. An error occurred.` (400) are returned as real HTTP errors. Scripts should therefore check the response body, not only the HTTP status code.

**Rules that apply to every call:**

- A user assigned to a DAG can only randomize records in their own DAG.
- The record must exist in the arm that contains the target field's event.
- For randomization stratified by DAG, the record must already be in a DAG; the API cannot assign one.
- Allocations, and the "already randomized" check, are separate for development and production status.
- For blinded randomization (the target field is a text field), `target_field_alt` is returned as `'*'` (see the concealed allocation note in Section 1).
- The action is logged.

---

# 6. Common Questions

**Q: Where do I find the `randomization_id`?**

**A:** It is shown on the Randomization page in the REDCap UI (requires Randomization Setup or Dashboard rights) or on the API Playground page when you select the Randomize Record method. Each randomization definition in a project has a unique ID.

**Q: Can a project have more than one randomization?**

**A:** Yes. REDCap supports multiple randomization definitions within a single project, each targeting a different field/event combination. The `randomization_id` parameter is how you specify which one to trigger.

**Q: What does `target_field_alt` contain for a concealed allocation?**

**A:** For concealed allocations, `target_field_alt` always returns `'*'` regardless of the actual group assigned. This is by design to preserve blinding. The real allocation value is not exposed via the API.

**Q: What happens if I try to randomize a record that's already been randomized?**

**A:** REDCap will return the message `Cannot randomize. Randomization already completed for record.` (as an HTTP 200 plain-text response). A record can only be randomized once per randomization definition. To re-randomize, the existing randomization (the record's allocation) would need to be undone by a REDCap administrator.

**Q: Does the record need to already exist before I call this method?**

**A:** Yes. The record must already exist in REDCap and all stratification fields for the selected randomization must be populated. Use the Import Records API ([RC-API-03 — Import Records API](RC-API-03_Import-Records.md)) to create the record first if it does not exist.

---

# 7. Common Mistakes & Gotchas

**Missing stratification data.** The most common failure reason. If any stratification field for the selected randomization is empty, the call fails. Ensure all required fields are filled before calling this method.

**Wrong `randomization_id`.** Each randomization definition has a unique numeric ID. Passing the wrong one targets a different randomization (or fails entirely). Always verify the ID in the REDCap UI or API Playground first.

**Insufficient permissions.** The API token must belong to a user with the **Randomize** privilege specifically. Only the Randomize right is checked; API Import/Export rights are not required for this method (administrators always pass).

**Expecting the real group value with concealed allocations.** When `returnAlt=true` and allocations are concealed, `target_field_alt` returns `'*'`, not the actual group. Do not build logic around this field for concealed studies.

**Record already randomized.** Attempting to randomize a record a second time returns an error message (HTTP 200, see Section 5). There is no `force` or `overwrite` option — undoing a randomization, or editing the allocation table, can only be done by a REDCap administrator.

**Checking only the HTTP status code.** Most "cannot randomize" failures return HTTP 200 with a plain-text message. Always inspect the response body.

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) (allocation tables, concealment, stratification)
- [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md) (how to configure randomization definitions and find the randomization_id)
- [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md) (manual randomization workflow; reverting randomizations)
