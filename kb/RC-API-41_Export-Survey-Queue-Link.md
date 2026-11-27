

**Export Survey Queue Link API**

| **Article ID** | [RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with Survey Queue enabled; users with API Export and Survey Distribution Tools rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — survey queue link behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API official documentation (Export a Survey Queue Link for a Participant) |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md); [RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)|
| **Synonyms** | export survey queue link api method; how do i get a survey queue link via the api; api call to generate the survey queue url for a record; retrieve the survey queue link through the api; export survey queue url for a participant using the api; api method to get a guided multi-survey queue link; programmatically fetch the survey queue link with the api |

---

## 1. Overview

The Export Survey Queue Link API returns a unique URL in plain text for the specified record. The Survey Queue presents multiple surveys to a respondent in a guided workflow. This API is useful for sending queue links programmatically via email, SMS, or other channels in automated workflows.

Survey Queue must be enabled in the project for this method to work. "Enabled" means the queue has at least one active entry for a survey-enabled instrument (in longitudinal projects, the instrument must also be designated to the entry's event). If not, the method returns HTTP 400 with "The Survey Queue has not been enabled…".

**Permissions required:** both API Export and Survey Distribution Tools (**Manage Survey Participants**) rights, in all current versions (16.x and 17.x). A user missing either right receives HTTP 403.

---

## 2. Key Concepts & Definitions

#### Survey Queue
A REDCap feature that presents multiple surveys to a respondent in a guided, sequential workflow. Differs from individual survey links which target a single instrument.

#### Queue Link
A unique, non-expiring URL that shows the record's survey queue. Which surveys appear, and whether the next one starts automatically, follows the queue's configuration (activation conditions and auto-start), so the respondent sees the surveys whose conditions are met rather than every survey in the project. There is one link per record; once created it stays the same, so repeated calls return the same URL. Respondents access the queue via this single link.

#### Record
The unique primary identifier for a participant or subject in REDCap. The queue link is specific to a record and shows the surveys whose queue conditions are met for that record.

#### Survey Distribution Tools Privilege
The **Manage Survey Participants** user right. Required, together with API Export, to export survey queue links via the API; without it the request returns HTTP 403.

#### Content Parameter
The identifier sent in API requests specifying which type of resource to export. For Survey Queue Link, always set to `'surveyQueueLink'`.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyQueueLink'` |
| `record` | Required | The record ID as it exists in the project |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`). Has no effect on the response itself, which is always plain text |

No other parameters are used. `event`, `instrument` and similar parameters are ignored if sent.

---

## 4. Request Examples

### 4.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'surveyQueueLink',
    'record': '1'
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
    content='surveyQueueLink',
    record='1'
)
print(result)
```

### 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=surveyQueueLink&record=1"

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
	'token'   => $GLOBALS['api_token'],
	'content' => 'surveyQueueLink',
	'record'  => '1'
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

The API returns a unique survey queue URL as a plain text string (not wrapped in JSON or XML):

```
https://redcap.example.edu/surveys/?sq=Q7K2L1M5N3P8R4T9X1Y0Z6C2D5E3F4G1
```

This URL opens the survey queue for the specified record, showing the surveys whose queue conditions are met. The same URL is returned on every call for that record. It can be sent directly to participants or embedded in communications.

**Errors:**

| Situation | HTTP status |
|---|---|
| `record` missing, or the record does not exist | 400 |
| Survey Queue not enabled (no active queue entry for a survey-enabled instrument) | 400 |
| User lacks API Export or Survey Distribution Tools rights | 403 |
| Record is not in the user's Data Access Group | 403 |
| User is a Double Data Entry user | 403 |

---

## 6. Common Questions

**Q: What is the difference between a survey link and a survey queue link?**
**A:** A survey link ([RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)) is specific to one instrument. A survey queue link ([RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md)) presents multiple surveys in a guided workflow on a single page.

**Q: Which surveys appear in the queue?**
**A:** The queue shows the surveys whose queue conditions are met for the record, according to your project's Survey Queue configuration (activation logic and auto-start settings). It is not simply every survey in the project. The order and visibility are set in the project design, not via API.

**Q: Does the link change if I call the method again?**
**A:** No. There is one queue link per record, and once created it stays the same. Repeated calls return the same URL.

**Q: Can I customize which surveys appear in the queue via API?**
**A:** No. Survey queue membership is configured in the project design. Use the REDCap interface to specify which instruments are part of the queue.

**Q: Does this method accept an event parameter for longitudinal projects?**
**A:** No. Unlike some other survey API methods, this one takes only `token`, `content`, and `record` (plus `returnFormat` for errors); an `event` parameter is ignored. The queue link is record-scoped, not event-scoped.

**Q: What does the response look like?**
**A:** It is a plain text URL string — not a JSON object or XML document. Don't try to parse it as JSON; just use the string directly.

**Q: What happens if the record has no surveys in its queue?**
**A:** The API still returns a valid URL, but accessing it will show a message that no surveys are available.

---

## 7. Common Mistakes & Gotchas

**Confusing surveyLink and surveyQueueLink:** These are distinct content types. Use `'surveyLink'` ([RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)) for a link to a single instrument; use `'surveyQueueLink'` for the full multi-survey queue workflow.

**Including event or instrument parameters:** This method does not accept `event` or `instrument`. Passing them does not cause an error — REDCap ignores them — but they serve no purpose and can cause confusion.

**Trying to parse the response as JSON:** The response is plain text (a URL string). Passing it through a JSON parser will fail. Treat the response body directly as the URL.

**Survey Queue not enabled:** If the queue has no active entry for a survey-enabled instrument (in longitudinal projects, one designated to the entry's event), this method returns HTTP 400 ("The Survey Queue has not been enabled…"). Check the Survey Queue setup before troubleshooting API calls.

**Missing Survey Distribution Tools rights:** API Export alone is not enough. Without the **Manage Survey Participants** right the method returns HTTP 403.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)
- [RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (how the survey queue works; context for the queue link)
