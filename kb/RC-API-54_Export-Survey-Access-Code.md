

**Export Survey Access Code API**

| **Article ID** | [RC-API-54 — Export Survey Access Code API](RC-API-54_Export-Survey-Access-Code.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with surveys enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Export Survey Access Code behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API official documentation |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md); [RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md); [RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)|
| **Synonyms** | export survey access code api method; how do i get a survey access code via the api; api call to retrieve the short survey access code; get the survey login code for a record through the api; export survey access code for a participant using the api; api method to fetch a short alphanumeric survey code; programmatically get the survey access code with the api |

---

## 1. Overview

The Export Survey Access Code API returns a short alphanumeric access code for a specific record and survey instrument. Participants can enter this code on the REDCap survey login page instead of clicking a full survey URL — useful when distributing surveys via channels where long URLs are impractical (e.g., printed materials, verbal instructions, SMS with character limits).

This is distinct from the survey link ([RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)), which returns a full clickable URL, and the return code ([RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)), which allows resuming an in-progress survey.

> **Permissions required:** API Export privileges AND the **Survey Distribution Tools** user right. If the token owner lacks the Survey Distribution Tools right, the API returns a 403 error: "The API request cannot complete because currently you do not have "Manage Survey Participants" privileges, which are required for this operation." The check uses the token owner's actual project rights, so an administrator's token without that project right is refused too.

Surveys must be enabled on the project, and the instrument must be marked as a survey in the project design.

---

## 2. Key Concepts & Definitions

#### Survey Access Code
A short alphanumeric code that participants can enter at the REDCap survey login page to access their assigned survey, instead of clicking a full URL. Useful for distribution via SMS, print, or in-person enrollment.

#### Survey Link
A full URL that points directly to a survey for a specific record and instrument. Differs from an access code in that it is a direct link rather than a code to be entered.

#### Survey Distribution Tools
A REDCap permission that grants users the ability to access survey-related API methods and features beyond basic data entry.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyAccessCode'` |
| `record` | Required | Record ID (must exist in the project) |
| `instrument` | Required | Instrument name (must be configured as a survey) |
| `event` | Required (longitudinal) | Event name (for longitudinal projects); omit for classic projects |
| `repeat_instance` | Optional | Repeat instance number for repeating instruments/events. Default: `'1'` |
| `returnFormat` | Optional | Format for **error messages only**: `csv`, `json`, or `xml` (default). Does not affect the response — the access code is always returned as plain text. |

---

## 4. Request Examples

### 4.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyAccessCode',
    'record': '1',
    'instrument': 'baseline_survey',
    'event': 'event_1_arm_1'
}

r = requests.post(config['api_url'], data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

### 4.2 R
```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='surveyAccessCode',
    record='1',
    instrument='baseline_survey',
    event='event_1_arm_1'
)
print(result)
```

### 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=surveyAccessCode&record=1&instrument=baseline_survey&event=event_1_arm_1"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -X POST \
      -d $DATA \
      $API_URL
```

### 4.4 PHP
```php
<?php

include 'config.php';

$fields = array(
	'token'      => $GLOBALS['api_token'],
	'content'    => 'surveyAccessCode',
	'record'     => '1',
	'instrument' => 'baseline_survey',
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

## 5. Response

The API returns a survey access code as **plain text**:

```
A7KD3XQ2M
```

Access codes are 9 characters long. The code is created the first time it is requested for a given record, instrument, event and repeat instance, and the same code is returned on every later call.

Participants enter this code at the REDCap survey login page (e.g., `https://redcap.institution.edu/surveys/`) to access their assigned survey without needing a direct link.

---

## 6. Common Questions

**Q: What is the difference between a survey access code and a survey link?**
**A:** A survey link ([RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)) is a full URL the participant clicks to go directly to their survey. An access code is a short code the participant types at the REDCap survey login page. Both grant access to the same survey for the same record; the difference is how the participant gets there.

**Q: When would I use an access code instead of a survey link?**
**A:** Access codes are useful when a full URL is impractical — for example, printed participant packets, in-person enrollment, SMS with tight character limits, or when participants may have difficulty clicking links.

**Q: Is the access code unique per record?**
**A:** Yes. Each access code is unique to a specific record, instrument, event (if longitudinal) and repeat instance, just like a survey link.

**Q: Does an access code expire?**
**A:** The code itself does not expire. However, survey settings such as an expiration date, or a survey that has been set to inactive, can still stop the participant from taking the survey.

**Q: Can I use both a survey link and an access code for the same record?**
**A:** Yes. Both methods grant access to the same survey entry for that record. You can generate both and use whichever is appropriate for your distribution channel.

---

## 7. Common Mistakes & Gotchas

**Missing Survey Distribution Tools privilege:** API Export alone is not sufficient. The user account associated with the token must also have the Survey Distribution Tools right in the project. Without it, the call returns a 403 error ("...you do not have "Manage Survey Participants" privileges, which are required for this operation.") even if the token is otherwise valid, and this applies to administrator tokens that lack the right in that project.

**Missing event parameter for longitudinal projects:** For longitudinal studies, the `event` parameter is required. Omitting it returns "The parameter 'event' is missing"; an unknown event name returns "Invalid event".

**Using instrument label instead of variable name:** The `instrument` parameter must be the instrument's variable name (e.g., `baseline_survey`), not its display label (e.g., "Baseline Survey").

**Requesting an access code for a non-survey instrument:** The instrument must be enabled as a survey in the project design. Regular data collection instruments return the error "The instrument '<name>' has not been enabled as a survey". The same error is returned when surveys are turned off for the project. An unknown instrument name returns "Invalid instrument".

**Other errors:**
- 400 if the instrument is not designated to the requested event.
- 400 "An unknown error occurred" if the record is not in the arm that contains the requested event.
- 403 if the record belongs to a different Data Access Group than the token owner's.
- 403 for Double Data Entry users requesting records outside their own.
- `repeat_instance` on an instrument that is not repeating is treated as 1.

**Parsing the response as JSON:** The response is plain text — just the access code string. Do not attempt to parse it as JSON.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)
- [RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md)
- [RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)
- [RC-API-43 — Export Survey Participants API](RC-API-43_Export-Survey-Participants.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals and access methods)
