

**Export Survey Link API**

| **Article ID** | [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with surveys enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — survey link behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md); [RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)|
| **Synonyms** | export survey link api method; how do i get a survey link via the api; api call to generate a survey url for a record; retrieve a unique survey link through the api; export single survey link for a participant using the api; api method to get a record-specific survey url; programmatically fetch a survey link with the api; get clickable survey url for an instrument via api |

---

## 1. Overview

The Export Survey Link API generates a unique, clickable survey URL for a specific record and instrument. This is essential for survey distribution workflows where you programmatically send survey links via email, SMS, or other channels. Each link is secure and record-specific. Respondents do not need a REDCap login to open it, unless **Survey Login** is enabled for that survey, in which case they must still log in.

Surveys must be enabled on the project, the instrument must be enabled as a survey, and the record must already exist. The method never creates a record.

> **Permissions required:** the **API Export** right AND the **Survey Distribution Tools** ("Manage Survey Participants") right. If the token's user lacks either one, the API returns HTTP 403.

---

## 2. Key Concepts & Definitions

#### Survey Link
A unique, stable URL that lets a respondent open a specific survey instrument for a specific record without a REDCap login (unless Survey Login is enabled for the survey). The link includes an embedded code specific to the record, instrument, event and repeat instance. The URL itself does not change, but survey settings can still limit what it does (see Section 6).

#### Survey Distribution Tools Privilege
A user right ("Manage Survey Participants") required to use survey distribution features, including sending invitations and generating survey links via the API. The API Export right alone is insufficient.

#### Respondent
An individual completing a survey. Respondents access the survey using the generated link and do not require REDCap user accounts.

#### Repeating Instance
A specific occurrence of a repeating instrument or event. Default is `'1'`; higher numbers apply to subsequent repetitions. `repeat_instance` is ignored if the instrument and event are not set to repeat. Requesting an instance number that does not exist yet returns a link that prepares that new instance.

#### Event (Longitudinal Projects)
A time point in a longitudinal study. Required for longitudinal projects; each event can have survey instruments assigned. Classic projects do not use the event parameter.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyLink'` |
| `record` | Required | Record ID (must already exist in the project; the method does not create records) |
| `instrument` | Required | Instrument name (must be configured as a survey) |
| `event` | Required (longitudinal) | Event name (for longitudinal projects); omit for classic projects |
| `repeat_instance` | Optional | Repeat instance number for repeating instruments/events. Default: `'1'`. Ignored for non-repeating instruments/events; a new instance number returns a link for that new instance. |
| `returnFormat` | Optional | Format for **error messages only**: `csv`, `json`, or `xml` (default). Does not affect the response — the survey link is always returned as plain text. |

---

## 4. Request Examples

### 4.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyLink',
    'record': 'f21a3ffd37fc0b3c',
    'instrument': 'test_instrument',
    'event': 'event_1_arm_1',
    'format': 'json'
}

r = requests.post(config['api_url'],data=fields)
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
    content='surveyLink',
    record='f21a3ffd37fc0b3c',
    instrument='test_instrument',
    event='event_1_arm_1',
    format='json'
)
print(result)
```

### 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=surveyLink&record=f21a3ffd37fc0b3c&instrument=test_instrument&event=event_1_arm_1&format=json"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
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
	'content'    => 'surveyLink',
	'record'     => 'f21a3ffd37fc0b3c',
	'instrument' => 'demographics',
	'event'      => 'event_1_arm_1',
	'format'     => 'json'
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

The API returns a unique survey URL as **plain text** (not JSON):

```
https://your-redcap-instance.edu/surveys/?s=XXXXXXXXXXXXXXXXXX
```

The URL is valid immediately and can be distributed via email, text message, or embedded in web pages.

---

## 6. Common Questions

**Q: Can I regenerate the same survey URL for the same record?**
**A:** Yes. Calling the API again for the same record, instrument, event and repeat instance returns the same URL, so you can resend links as needed. A different event or instance gets its own URL.

**Q: What happens if I request a survey link for a record that doesn't exist?**
**A:** The API returns HTTP 400 with the message `The record "X" does not exist` (with your record ID in place of X). It never creates the record. Create the record first with [RC-API-03 — Import Records API](RC-API-03_Import-Records.md), then request the link.

**Q: How long is a survey URL valid?**
**A:** The link itself is stable: it does not change or expire on its own. What it lets the respondent do still depends on survey settings: a survey time limit, a survey expiration date or an offline (inactive) survey can block access, and once the response is completed the respondent cannot reopen it unless the survey allows editing of completed responses. The API returns a link even if the survey is not currently active, so check the survey's status before sending.

**Q: Can respondents access the survey without the link?**
**A:** This link is private and non-guessable, and it is the direct route to this record's survey. It is not the only route: respondents can also enter a survey access code, reach the survey through the survey queue, or (for the first instrument only) use the project's public survey link, which creates a new record rather than opening this one. See [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md).

**Q: For longitudinal projects, which event should I specify?**
**A:** Specify the event in which you want the respondent to complete the survey. The instrument must be assigned to that event in the project design.

---

## 7. Common Mistakes & Gotchas

**Missing Survey Distribution Tools right:** API Export alone is not sufficient. The user account associated with the token must also have the Survey Distribution Tools ("Manage Survey Participants") right in the project. Without either right, the call returns HTTP 403 even if the token itself is valid.

**Missing event parameter for longitudinal projects:** For longitudinal studies, the `event` parameter is required. Omitting it results in an error.

**Using instrument label instead of variable name:** The `instrument` parameter must be the instrument's variable name (e.g., `demographics`), not its display label (e.g., "Demographics Form").

**Requesting survey link for non-survey instrument:** The instrument must be enabled as a survey in the project design. Regular instruments cannot be accessed via survey link.

**Other errors to expect:** the API returns HTTP 400 if the record or instrument is missing, the instrument name is invalid, the instrument is not enabled as a survey, the event name is invalid, or (longitudinal) the instrument is not designated for that event. It returns HTTP 403 if the record belongs to a Data Access Group other than the user's, or if the user is a Double Data Entry user.

**Parsing the response as JSON:** The response is plain text — just the URL string. Do not attempt to parse it as JSON or look for a `survey_url` key; treat the entire response body as the link.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md)
- [RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)
- [RC-API-43 — Export Survey Participants API](RC-API-43_Export-Survey-Participants.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals and how survey links work)
- [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md) (the link types this method generates)
