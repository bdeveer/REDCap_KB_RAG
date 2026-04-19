RC-API-52

**Randomize Record API**

| **Article ID** | RC-API-52 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with Randomization enabled |
| **Prerequisite** | RC-API-01 — REDCap API; RC-RAND-01 — Randomization Concepts & Terminology |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API official documentation |
| **Related Topics** | RC-API-01 — REDCap API; RC-RAND-01 — Randomization Concepts & Terminology; RC-RAND-02 — Randomization Setup Guide; RC-RAND-03 — Working with & Managing Randomization |

---

# 1. Overview

The Randomize Record API method triggers the randomization of an existing record in a REDCap project. It performs the same action as manually randomizing a record through the REDCap UI, but programmatically via the API.

The method requires that the record already exists and that all stratification fields for the specified randomization have been filled in. If stratification data is missing or incomplete, the call will fail with an error.

You must specify a `randomization_id`, which corresponds to a specific randomization definition (target field + event). Projects can have multiple randomization definitions; the `randomization_id` tells REDCap which one to use. This ID is visible on the Randomization page (for users with Design permissions) or on the API Playground page.

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
| `format` | Required | Response format: `'csv'`, `'json'`, or `'xml'` (default). |
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 5. Response

On success, returns the randomization result. The response includes the randomization ID, the record name, the value assigned to the target field, and (if `returnAlt=true`) the alternative target field value.

**JSON:**
```json
{
    "randomization_id": 123,
    "record": "21",
    "target_field": "1",
    "target_field_alt": "R-1005"
}
```

**CSV:**
```
randomization_id,record,target_field,target_field_alt
123,21,1,R-1005
```

**XML:**
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<item>
    <randomization_id>123</randomization_id>
    <record>21</record>
    <target_field>1</target_field>
    <target_field_alt>R-1005</target_field_alt>
</item>
```

On failure, an error message is returned in the requested `returnFormat`. Common failure reasons include: the record does not exist, stratification information is missing or incomplete, or the user lacks the Randomize privilege.

---

# 6. Common Questions

**Q: Where do I find the `randomization_id`?**

**A:** It is shown on the Randomization page in the REDCap UI (requires Design permissions) or on the API Playground page when you select the Randomize Record method. Each randomization definition in a project has a unique ID.

**Q: Can a project have more than one randomization?**

**A:** Yes. REDCap supports multiple randomization definitions within a single project, each targeting a different field/event combination. The `randomization_id` parameter is how you specify which one to trigger.

**Q: What does `target_field_alt` contain for a concealed allocation?**

**A:** For concealed allocations, `target_field_alt` always returns `'*'` regardless of the actual group assigned. This is by design to preserve blinding. The real allocation value is not exposed via the API.

**Q: What happens if I try to randomize a record that's already been randomized?**

**A:** REDCap will return an error. A record can only be randomized once per randomization definition. To re-randomize, the existing randomization would need to be reverted through the UI by a user with appropriate permissions.

**Q: Does the record need to already exist before I call this method?**

**A:** Yes. The record must already exist in REDCap and all stratification fields for the selected randomization must be populated. Use the Import Records API (RC-API-03) to create the record first if it does not exist.

---

# 7. Common Mistakes & Gotchas

**Missing stratification data.** The most common failure reason. If any stratification field for the selected randomization is empty, the call fails. Ensure all required fields are filled before calling this method.

**Wrong `randomization_id`.** Each randomization definition has a unique numeric ID. Passing the wrong one targets a different randomization (or fails entirely). Always verify the ID in the REDCap UI or API Playground first.

**Insufficient permissions.** The API token must belong to a user with the **Randomize** privilege specifically — general API Export or Edit rights are not sufficient.

**Expecting the real group value with concealed allocations.** When `returnAlt=true` and allocations are concealed, `target_field_alt` returns `'*'`, not the actual group. Do not build logic around this field for concealed studies.

**Record already randomized.** Attempting to randomize a record a second time returns an error. There is no `force` or `overwrite` option — reverting must be done through the UI.

---

# 8. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-RAND-01 — Randomization Concepts & Terminology (allocation tables, concealment, stratification)
- RC-RAND-02 — Randomization Setup Guide (how to configure randomization definitions and find the randomization_id)
- RC-RAND-03 — Working with & Managing Randomization (manual randomization workflow; reverting randomizations)
