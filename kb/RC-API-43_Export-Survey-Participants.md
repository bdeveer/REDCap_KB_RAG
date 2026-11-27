

**Export Survey Participants API**

| **Article ID** | [RC-API-43 — Export Survey Participants API](RC-API-43_Export-Survey-Participants.md) |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with participant-list surveys enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — participant list behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API official documentation (Export a Survey Participant List) |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)|
| **Synonyms** | export survey participant list api method; how do i get the survey participant list via the api; api call to retrieve survey participants and invitation status; export participant list with response status through the api; get per-participant survey links using the api; api method to pull survey participant contact info; programmatically retrieve the participant list with the api |

---

## 1. Overview

The Export Survey Participants API retrieves the participant list for a survey-enabled instrument. It returns contact information, invitation status, response status, and direct survey access links. This is useful for tracking invitation delivery, monitoring response rates, and programmatically retrieving per-participant survey links.

**Permissions required:** The calling user must have both API Export privileges and Survey Distribution Tools privileges. If either is missing, the API returns an HTTP 403 error. A missing or invalid `instrument`, an instrument that has not been enabled as a survey, or an invalid `event` each return an HTTP 400 error.

**Which participants you see:** Users assigned to a Data Access Group see participants whose record is in their DAG, plus participants not yet linked to any record. Users in a Double Data Entry project see only their own records. In a multi-arm longitudinal project, only participants for records in the requested event's arm are returned.

---

## 2. Key Concepts & Definitions

#### Participant List
A list of contact information (typically names and email addresses) entered in REDCap for survey distribution. Each participant receives an access code and survey link.

#### Access Code
A short alphanumeric code assigned to each participant that they can use instead of the full survey URL to access their survey from a survey login page.

#### Invitation Status
A flag indicating whether an invitation has been sent to the participant (via REDCap's built-in notification system). Does not confirm email delivery.

#### Response Status
A value indicating the completion state of a survey: `0` (No response), `1` (Partial response), or `2` (Completed).

#### Email Occurrence
The running number of that email address within the participant list: `1` for its first appearance, `2` for its second, and so on. It is not a total count. Used with the email field to uniquely identify a participant row, since the same email can be added multiple times.

#### Survey Distribution Tools Privilege
A user-level permission required to access participant lists and survey distribution features. Required along with API Export privilege to use this method.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'participantList'` |
| `instrument` | Required | The unique instrument name as shown in the Data Dictionary (must be enabled as a survey) |
| `event` | Required (longitudinal) | The unique event name; required for longitudinal projects, omit for classic projects |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`) |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to match `format` if omitted |

---

## 4. Request Examples

### 4.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'participantList',
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
    content='participantList',
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

DATA="token=$API_TOKEN&content=participantList&instrument=test_instrument&event=event_1_arm_1&format=json"

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
	'content'    => 'participantList',
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

The API returns an array of participant rows. Every row contains these nine columns, in this order:

| Field | Description |
|---|---|
| `email` | The participant's email address |
| `email_occurrence` | The running number of this email in the list (`1` for its first appearance, `2` for its second, and so on). Because the same email can be added more than once, `email` + `email_occurrence` together form a unique identifier |
| `identifier` | The participant identifier (typically a name or label entered in the participant list) |
| `record` | The record name linked to this participant. Filled only when the participant has an identifier, or when the email comes from the project's designated email field; otherwise blank, so that participants stay anonymous |
| `invitation_sent_status` | `1` if an invitation has been sent; `0` if not |
| `invitation_send_time` | Date/time of the next scheduled invitation. Blank if no invitation is scheduled |
| `response_status` | `0` = No response, `1` = Partial, `2` = Completed |
| `survey_access_code` | The unique access code for this participant's survey session |
| `survey_link` | The direct, participant-specific URL to the survey |

Extra columns appear only when relevant to the project:

| Field | When it appears |
|---|---|
| `phone` | Only when Twilio SMS/voice is enabled for the project; placed near `email` |
| `repeat_instance` | The instrument or event is repeating |
| `survey_link_expiration` | The survey has a time limit enabled |
| `survey_queue_link` | The survey queue is enabled |

> **Note:** For a completed response, `survey_access_code` and `survey_link` are blank when the survey does not allow respondents to edit completed responses.

In JSON output, `invitation_sent_status` and `response_status` are numbers, not strings. Example JSON response (classic project, no optional columns):

```json
[
  {
    "email": "john.doe@example.com",
    "email_occurrence": "1",
    "identifier": "John Doe",
    "record": "1",
    "invitation_sent_status": 1,
    "invitation_send_time": "",
    "response_status": 2,
    "survey_access_code": "ABCD1234",
    "survey_link": "https://redcap.example.edu/surveys/?s=ABCD1234"
  },
  {
    "email": "jane.smith@example.com",
    "email_occurrence": "1",
    "identifier": "",
    "record": "",
    "invitation_sent_status": 0,
    "invitation_send_time": "2026-05-01 09:00:00",
    "response_status": 0,
    "survey_access_code": "EFGH5678",
    "survey_link": "https://redcap.example.edu/surveys/?s=EFGH5678"
  }
]
```

In this example the first participant has an identifier, so `record` is filled; the second has none, so `record` is blank and the participant stays anonymous. (In the first row, the code and link are shown because this survey allows editing completed responses.)

> **Note:** This response does not include `first_name`, `last_name`, `optout`, or any data-entry fields. To retrieve record-level data, use the Export Records API ([RC-API-02 — Export Records API](RC-API-02_Export-Records.md)).

> **Version caveat (16.0.61 LTS):** On 16.x the participant list may be served from a cache, so `invitation_sent_status` and `invitation_send_time` can lag behind invitations that were recently scheduled or sent until other activity happens in the project. 17.3.31 LTS and 17.6 read invitation status live. On 16.x, if the status looks stale, confirm it on the **Participant List** page in **Survey Distribution Tools**.

---

## 6. Common Questions

**Q: What does `invitation_sent_status` mean?**
**A:** `1` means an invitation has been sent to the participant; `0` means no invitation has been sent yet. Note: this reflects REDCap's tracking of distribution — it is not confirmation of email delivery.

**Q: What does `email_occurrence` mean?**
**A:** It is the running number of that email address within the participant list: `1` for the first row with that email, `2` for the second, and so on (not a total count). Because the same email can be added more than once (e.g., to send multiple surveys), `email` alone is not unique. Use `email` + `email_occurrence` together as the unique identifier.

**Q: What does `response_status` mean?**
**A:** `0` = No response, `1` = Partial response, `2` = Completed. This is the same status shown in the Survey Distribution Tools interface.

**Q: What are `survey_access_code` and `survey_link`?**
**A:** Each participant receives a unique access code and a direct URL to their survey session. The `survey_link` is the full URL a participant would use to access the survey; you can send this in a custom notification rather than using REDCap's built-in invitation system. For a completed response, both are blank if the survey does not allow editing completed responses.

**Q: Why is `record` blank for some participants?**
**A:** `record` is filled only when the participant has an identifier, or when the email comes from the project's designated email field. Otherwise it is left blank so that participants stay anonymous.

**Q: Can I modify participant information via API?**
**A:** No. This method does not change your data or let you edit participants. REDCap may prepare participant and survey link entries for existing records when the list is exported, and the call is logged. To manage participants, use the Survey Distribution Tools interface in REDCap.

**Q: For longitudinal projects, what happens if I don't specify an event?**
**A:** REDCap will return an HTTP 400 error. The `event` parameter is required for longitudinal projects.

---

## 7. Common Mistakes & Gotchas

**Calling without Survey Distribution Tools privilege:** This method requires both API Export and Survey Distribution Tools rights. If your token belongs to a user without Survey Distribution Tools access, the API returns an HTTP 403 error — not an empty result. Verify user privileges before troubleshooting elsewhere.

**Instrument not enabled as a survey:** If the instrument exists in the project but hasn't been enabled as a survey, the API returns an HTTP 400 error. Enable it via Survey Settings in the Online Designer first. A missing or misspelled `instrument` name also returns 400.

**Missing or invalid event for longitudinal projects:** The `event` parameter is required for longitudinal projects. Omitting it or passing an invalid unique event name produces an HTTP 400 error.

**Expecting every participant in a DAG, DDE or multi-arm project:** DAG users see only participants whose record is in their DAG plus participants not yet linked to a record; Double Data Entry users see only their own records; in multi-arm projects only the requested event's arm is returned. A shorter list than the Participant List page shows an administrator is usually this, not a fault.

**Expecting record-level fields in the response:** This API does not return `first_name`, `last_name`, `optout`, or other data-entry fields. It returns the participant-list columns only (plus optional columns such as `phone` or `repeat_instance` when relevant). The `record` column is blank for anonymous participants (no identifier and no designated email field). Use the Export Records API ([RC-API-02 — Export Records API](RC-API-02_Export-Records.md)) if you need record data.

**Treating `email` as a unique key:** The same email address can appear multiple times in the participant list. Always use `email` + `email_occurrence` together to uniquely identify a participant row.

---

## 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals)
- [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md) (the participant list this method reads from)
