---
id: RC-API-42
title: Export Survey Return Code API
domain: API
applies_to:
- REDCap projects with surveys enabled
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — return
  code behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-11
source: REDCap API official documentation (Export a Survey Return Code for a Participant)
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-40
  title: Export Survey Link API
- id: RC-API-41
  title: Export Survey Queue Link API
tags:
- api
synonyms:
- export survey return code api method
- how do i get a survey return code via the api
- api call to retrieve a save and return later code
- get the code to resume an incomplete survey through the api
- export survey return code for a participant using the api
- api method to fetch a survey resumption code
- programmatically get the return code with the api
---

# 1. Overview

The Export Survey Return Code API returns a unique code in plain text that allows a respondent to resume an incomplete survey. When a respondent saves progress and closes the survey, they open the survey link again and enter the return code to continue from their saved point. This is useful for multi-session surveys and for building custom resumption workflows outside REDCap's built-in invitation system. A code can be retrieved before the respondent has started the survey.

Two conditions must be true for this method to work: (1) the instrument must be enabled as a survey, and (2) the **Save & Return Later** feature must be enabled on that survey. If the instrument is not a survey, the API returns an error. If Save & Return Later is not enabled, the API also returns an error, except when Survey Login is enabled for the project, in which case no error is given. Either way, enable Save & Return Later on any survey you export return codes for: it is the feature that lets respondents resume with the code.

**Permissions required:** API Export privileges and the **Survey Distribution Tools** user right, in all versions. A user missing either receives a 403 error. A 403 error is also returned if the record is not in the user's Data Access Group, or if the user is a Double Data Entry user.

---

# 2. Key Concepts & Definitions

### Return Code
A unique 8-character code (uppercase letters and digits) that allows a respondent to resume a partially completed survey from their last saved point. The respondent opens the survey link and types the code into the return code box REDCap shows for returning respondents.

### Save & Return Later
A survey feature that enables respondents to save their progress, close the survey, and resume later using a return code. Must be explicitly enabled in survey settings.

### Survey Link
The URL that gives access to a survey. A returning respondent opens this link and enters the return code to resume from a saved point. The link and the code are separate pieces of information.

### Respondent Session
A respondent's interaction with a survey. Return codes are not tied to a browser session: each code belongs to one survey response (the combination of record, instrument, event and repeat instance) and allows re-entry at the previously saved point from any browser or device.

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
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`). If omitted, the value of `format` is used instead. Has no effect on the response itself, which is always plain text |

---

# 4. Request Examples

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) Section 3.5.

---

# 5. Response

The API returns the return code as a plain text string (not wrapped in JSON or XML):

```
K7Q2M9XA
```

Return codes are 8 characters long and contain uppercase letters and digits.

To let a respondent resume their survey, send them both the survey link and the return code, for example in the same email. Retrieve the survey link separately using the Export Survey Link method ([RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)), or use the survey's public link. The respondent opens the link, chooses the option for returning respondents, and types the code into the return code box:

```
Survey link: https://redcap.example.edu/surveys/?s=<survey_link_code>
Return code: K7Q2M9XA
```

---

# 6. Common Questions

**Q: How do I use a return code with a survey link?**
**A:** Keep them separate. Get the survey link from [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md) (or use the public link) and send it to the respondent together with the return code. The respondent opens the link and types the code into the return code box REDCap shows for returning respondents. Do not try to build the code into the URL.

**Q: What does the response look like?**
**A:** It is a plain text string (just the code itself), not a JSON object or XML document. Don't try to parse it; use the string directly.

**Q: Does Save & Return Later need to be enabled?**
**A:** Yes. If the survey does not have **Save & Return Later** enabled in its Survey Settings, this method returns an error. The one exception is a project with Survey Login enabled, where no error is given; even then, enable Save & Return Later, since that is the feature that lets respondents resume with the code.

**Q: Can I get a return code for a survey that hasn't been started yet?**
**A:** Yes. Return codes can be retrieved at any time regardless of response status. If the respondent hasn't started yet, using the code opens the survey from the beginning.

**Q: Does a return code expire?**
**A:** Return codes do not have a time-based expiration. They remain usable while the response is incomplete, unless the record is deleted or the survey is closed. Once the response is completed, the code no longer resumes it, unless the survey allows respondents to edit their completed responses.

**Q: What is the difference between a return code and the survey link itself?**
**A:** A survey link takes the respondent to the survey. A return code, entered after opening that link, resumes the respondent's own response from their last saved point.

---

# 7. Common Mistakes & Gotchas

**Save & Return Later not enabled:** If the survey doesn't have Save & Return Later enabled, this API returns an error (unless Survey Login is enabled for the project). This is easy to overlook — verify the survey setting before debugging API calls.

**Appending the code to the survey URL:** The return code is not added to the survey link. Send the link and the code separately (for example, both in one email); the respondent opens the link and types the code into the return code box.

**Missing user rights or record access:** A 403 error means the token's user lacks API Export or Survey Distribution Tools rights, the record is outside the user's Data Access Group, or the user is a Double Data Entry user.

**Trying to parse the response as JSON:** The response is plain text — just the code string. Passing it through a JSON parser will fail.

**Assuming return codes prevent re-answering:** Return codes allow respondents to resume, but they can still change previous answers. There is no read-only mode enforced by return codes.

**Expecting `format` to change the response:** The response is always plain text. Neither `format` nor `returnFormat` changes it; both only affect error messages. If `returnFormat` is omitted, the value of `format` is used for error messages.

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)
- [RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md)
- [RC-API-43 — Export Survey Participants API](RC-API-43_Export-Survey-Participants.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals)
- [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md) (return code configuration in survey settings)
