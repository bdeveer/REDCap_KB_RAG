RC-API-42

**Export Survey Return Code API**

| **Article ID** | RC-API-42 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with surveys enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API official documentation (Export a Survey Return Code for a Participant) |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-40 — Export Survey Link; RC-API-41 — Export Survey Queue Link |

---

# 1. Overview

The Export Survey Return Code API returns a unique code in plain text that allows a respondent to resume an incomplete survey. When a respondent saves progress and closes the survey, the return code re-opens it at their saved point. This is useful for multi-session surveys and for building custom resumption workflows outside REDCap's built-in invitation system.

Two conditions must be true for this method to work: (1) the instrument must be enabled as a survey, and (2) the **Save & Return Later** feature must be enabled on that survey. If either condition is not met, the API returns an error.

**Permissions required:** API Export privileges. Note: the method description also states that users without Survey Distribution Tools privileges will receive an error, so both privileges may be needed depending on your REDCap version.

---

# 2. Key Concepts & Definitions

### Return Code
A unique alphanumeric string that allows a respondent to resume a partially completed survey from their last saved point. Appended to the survey link as a query parameter.

### Save & Return Later
A survey feature that enables respondents to save their progress, close the survey, and resume later using a return code. Must be explicitly enabled in survey settings.

### Survey Link
The base URL that gives access to a survey. The return code is appended to this link to allow resumption from a saved point.

### Respondent Session
A respondent's interaction with a survey. Return codes are tied to a specific session and allow re-entry at the previously saved point.

### Repeating Instruments/Events
Project structures where an instrument or event can be repeated multiple times per record. The repeat_instance parameter specifies which repetition the return code applies to.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyReturnCode'` |
| `record` | Required | The record ID as it exists in the project |
| `instrument` | Required | The unique instrument name from the Data Dictionary (must be enabled as a survey with Save & Return Later enabled) |
| `event` | Required (longitudinal) | The unique event name; required for longitudinal projects, omit for classic projects |
| `repeat_instance` | Conditional | The repeat instance number for repeating instruments or repeating events. Only applies to projects using repeating instruments/events. Default: `'1'` |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`). Has no effect on the response itself, which is always plain text |

---

# 3. Request Examples

## 4.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyReturnCode',
    'record': '1',
    'instrument': 'test_instrument',
    'event': 'event_1_arm_1'
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
    content='surveyReturnCode',
    record='1',
    instrument='test_instrument',
    event='event_1_arm_1'
)
print(result)
```

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=surveyReturnCode&record=1&instrument=test_instrument&event=event_1_arm_1"

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
	'token'      => $GLOBALS['api_token'],
	'content'    => 'surveyReturnCode',
	'record'     => '1',
	'instrument' => 'test_instrument',
	'event'      => 'event_1_arm_1'
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 5. Response

The API returns the return code as a plain text string (not wrapped in JSON or XML):

```
B3K2M5L1N7P9R4T8X2Y1Z3C5D6E8F1G2
```

To let a respondent resume their survey, append the code to the survey link using the `&rc=` parameter:

```
https://redcap.example.edu/surveys/?s=<survey_link_code>&rc=B3K2M5L1N7P9R4T8X2Y1Z3C5D6E8F1G2
```

Retrieve the base survey link separately using the Export Survey Link method (RC-API-40).

---

# 6. Common Questions

**Q: How do I use a return code with a survey link?**
A: Get the base survey link from RC-API-40, then append the return code: `<survey_link_url>&rc=<return_code>`. Note the `&` — not `?` — because the survey URL already contains query parameters.

**Q: What does the response look like?**
A: It is a plain text string (just the code itself), not a JSON object or XML document. Don't try to parse it; use the string directly.

**Q: Does Save & Return Later need to be enabled?**
A: Yes. If the survey does not have Save & Return Later enabled in its survey settings, this method returns an error. Enable it under Survey Settings → Termination Instruments.

**Q: Can I get a return code for a survey that hasn't been started yet?**
A: Yes. Return codes can be retrieved at any time regardless of response status. If the respondent hasn't started yet, using the code opens the survey from the beginning.

**Q: Does a return code expire?**
A: Return codes do not have a built-in expiration. They remain valid unless the record is deleted or the survey is closed.

**Q: What is the difference between a return code and the survey link itself?**
A: A survey link takes the respondent to the start of the survey. A return code, appended to that link, resumes from their last saved point.

---

# 7. Common Mistakes & Gotchas

**Save & Return Later not enabled:** If the survey doesn't have Save & Return Later enabled, this API returns an error. This is easy to overlook — verify the survey setting before debugging API calls.

**Forgetting the `&rc=` parameter:** To use the return code, append it to the survey link with `&rc=` (not `?rc=`). The ampersand is required because the survey URL already contains query parameters.

**Trying to parse the response as JSON:** The response is plain text — just the code string. Passing it through a JSON parser will fail.

**Assuming return codes prevent re-answering:** Return codes allow respondents to resume, but they can still change previous answers. There is no read-only mode enforced by return codes.

**Using `format` as a parameter:** This method does not accept a `format` parameter. The response is always plain text regardless. Only `returnFormat` is accepted, and it affects error messages only.

---

# 8. Related Articles

- RC-API-01 — REDCap API
- RC-API-40 — Export Survey Link
- RC-API-41 — Export Survey Queue Link
- RC-API-43 — Export Survey Participants
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-03 — Survey Settings: Behavior, Access & Termination (return code configuration in survey settings)
