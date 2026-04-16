RC-API-43

**Export Survey Participants API**

| **Article ID** | RC-API-43 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with participant-list surveys enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-40 — Export Survey Link |

---

# 1. Overview

The Export Survey Participants API retrieves the participant list for a survey-enabled instrument. This list includes contact information, invitation status, opt-out flags, and timestamps. This is essential for managing external survey respondents, tracking invitation delivery, and monitoring response rates for surveys sent outside your project's normal workflow.

Participant lists apply to surveys configured with the "Use a participant list" setting in the project design.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'participantList'` |
| `format` | Optional | Response format: `'json'` (default), `'xml'`, or `'csv'` |
| `instrument` | Required | Instrument name (must be configured as a participant-list survey) |
| `event` | Optional | Event name (required for longitudinal projects) |

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

The API returns an array of participant records with contact and invitation information:

```json
[
  {
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "record": "001",
    "invitation_sent_status": "1",
    "invitation_send_time": "2024-06-15 10:30:45",
    "optout": "0"
  },
  {
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "record": "002",
    "invitation_sent_status": "1",
    "invitation_send_time": "2024-06-15 10:31:12",
    "optout": "0"
  },
  {
    "email": "bob.wilson@example.com",
    "first_name": "Bob",
    "last_name": "Wilson",
    "record": "003",
    "invitation_sent_status": "0",
    "invitation_send_time": "",
    "optout": "0"
  }
]
```

---

# 5. Common Questions

**Q: What does `invitation_sent_status` mean?**
A: `1` indicates the invitation has been sent to the participant; `0` means no invitation has been sent yet. This is typically managed by automated survey distribution workflows.

**Q: Can I modify participant information via API?**
A: No. The Export Survey Participants API is read-only. To add or modify participants, use the REDCap interface or the standard data import API (RC-API-03).

**Q: What does `optout` mean?**
A: `optout: 1` indicates the participant has opted out and should not receive further survey invitations. `optout: 0` means they are active.

**Q: For longitudinal projects, what happens if I don't specify an event?**
A: For longitudinal studies, you must specify the event. Omitting it will result in an error.

**Q: How is the participant list populated?**
A: Participants are defined in your project design through the "Participant List" interface. They can be added manually or imported via the data import API.

---

# 6. Common Mistakes & Gotchas

**Requesting participants for a non-participant survey:** If the survey is configured as a standard survey (not participant-list), this API will fail or return empty results. Verify the survey type in project design.

**Missing event for longitudinal surveys:** For longitudinal projects, always include the event parameter. Omitting it causes an error.

**Misinterpreting invitation_sent_status:** This field reflects REDCap's tracking of invitation distribution, not actual email delivery confirmation. It depends on your survey distribution setup.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-40 — Export Survey Link
- RC-API-02 — Export Records
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-05 — Participant List & Manual Survey Invitations (the participant list this method reads from)
