RC-API-43

**Export Survey Participants API**

| **Article ID** | RC-API-43 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with participant-list surveys enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API official documentation (Export a Survey Participant List) |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-40 — Export Survey Link |

---

# 1. Overview

The Export Survey Participants API retrieves the participant list for a survey-enabled instrument. It returns contact information, invitation status, response status, and direct survey access links. This is useful for tracking invitation delivery, monitoring response rates, and programmatically retrieving per-participant survey links.

**Permissions required:** The calling user must have both API Export privileges and Survey Distribution Tools privileges. If either is missing, the API returns an error. If the specified instrument has not been enabled as a survey, an error is also returned.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'participantList'` |
| `instrument` | Required | The unique instrument name as shown in the Data Dictionary (must be enabled as a survey) |
| `event` | Required (longitudinal) | The unique event name; required for longitudinal projects, omit for classic projects |
| `format` | Optional | Response format: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`) |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to match `format` if omitted |

---

# 3. Request Examples

## 3.1 Python
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

## 3.2 R
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

## 3.3 cURL
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

## 3.4 PHP
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 4. Response

The API returns an array of participant records. Each record contains exactly these eight fields:

| Field | Description |
|---|---|
| `email` | The participant's email address |
| `email_occurrence` | Count of how many times this email appears in the list. Because the same email can be added more than once, `email` + `email_occurrence` together form a unique identifier |
| `identifier` | The participant identifier (typically a name or label entered in the participant list) |
| `invitation_sent_status` | `1` if an invitation has been sent; `0` if not |
| `invitation_send_time` | Date/time of the next scheduled invitation. Blank if no invitation is scheduled |
| `response_status` | `0` = No response, `1` = Partial, `2` = Completed |
| `survey_access_code` | The unique access code for this participant's survey session |
| `survey_link` | The direct, participant-specific URL to the survey |

Example JSON response:

```json
[
  {
    "email": "john.doe@example.com",
    "email_occurrence": "1",
    "identifier": "John Doe",
    "invitation_sent_status": "1",
    "invitation_send_time": "",
    "response_status": "2",
    "survey_access_code": "ABCD1234",
    "survey_link": "https://redcap.example.edu/surveys/?s=ABCD1234"
  },
  {
    "email": "jane.smith@example.com",
    "email_occurrence": "1",
    "identifier": "Jane Smith",
    "invitation_sent_status": "0",
    "invitation_send_time": "2026-05-01 09:00:00",
    "response_status": "0",
    "survey_access_code": "EFGH5678",
    "survey_link": "https://redcap.example.edu/surveys/?s=EFGH5678"
  }
]
```

> **Note:** This response does not include `first_name`, `last_name`, `record`, or `optout`. To retrieve record-level data, use the Export Records API (RC-API-02).

---

# 5. Common Questions

**Q: What does `invitation_sent_status` mean?**
A: `1` means an invitation has been sent to the participant; `0` means no invitation has been sent yet. Note: this reflects REDCap's tracking of distribution — it is not confirmation of email delivery.

**Q: What does `email_occurrence` mean?**
A: It is the count of how many times that email address appears in the participant list. Because the same email can be added more than once (e.g., to send multiple surveys), `email` alone is not unique. Use `email` + `email_occurrence` together as the unique identifier.

**Q: What does `response_status` mean?**
A: `0` = No response, `1` = Partial response, `2` = Completed. This is the same status shown in the Survey Distribution Tools interface.

**Q: What are `survey_access_code` and `survey_link`?**
A: Each participant receives a unique access code and a direct URL to their survey session. The `survey_link` is the full URL a participant would use to access the survey; you can send this in a custom notification rather than using REDCap's built-in invitation system.

**Q: Can I modify participant information via API?**
A: No. This method is read-only. To manage participants, use the Survey Distribution Tools interface in REDCap.

**Q: For longitudinal projects, what happens if I don't specify an event?**
A: REDCap will return an error. The `event` parameter is required for longitudinal projects.

---

# 6. Common Mistakes & Gotchas

**Calling without Survey Distribution Tools privilege:** This method requires both API Export and Survey Distribution Tools rights. If your token belongs to a user without Survey Distribution Tools access, the API returns an error — not an empty result. Verify user privileges before troubleshooting elsewhere.

**Instrument not enabled as a survey:** If the instrument exists in the project but hasn't been enabled as a survey, the API returns an error. Enable it via Survey Settings in the Online Designer first.

**Missing event for longitudinal projects:** The `event` parameter is required for longitudinal projects. Omitting it produces an error.

**Expecting record-level fields in the response:** This API does not return `first_name`, `last_name`, `record`, `optout`, or other data-entry fields. It returns only the eight participant-list fields. Use the Export Records API (RC-API-02) if you need record data.

**Treating `email` as a unique key:** The same email address can appear multiple times in the participant list. Always use `email` + `email_occurrence` together to uniquely identify a participant row.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-40 — Export Survey Link
- RC-API-02 — Export Records
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-05 — Participant List & Manual Survey Invitations (the participant list this method reads from)
