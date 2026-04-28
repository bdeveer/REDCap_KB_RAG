RC-API-41

**Export Survey Queue Link API**

| **Article ID** | RC-API-41 |
|---|---|
| **Domain** | API |
| **Applies To** | REDCap projects with Survey Queue enabled |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API official documentation (Export a Survey Queue Link for a Participant) |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-40 — Export Survey Link; RC-API-42 — Export Survey Return Code |

---

# 1. Overview

The Export Survey Queue Link API returns a unique URL in plain text for the specified record. The Survey Queue presents multiple surveys to a respondent in a guided workflow. This API is useful for sending queue links programmatically via email, SMS, or other channels in automated workflows.

Survey Queue must be enabled in the project for this method to work. If it is not enabled, an error is returned.

**Permissions required:** API Export privileges. Note: the method description also states that users without Survey Distribution Tools privileges will receive an error, so both privileges may be needed depending on your REDCap version.

---

# 2. Key Concepts & Definitions

### Survey Queue
A REDCap feature that presents multiple surveys to a respondent in a guided, sequential workflow. Differs from individual survey links which target a single instrument.

### Queue Link
A unique, non-expiring URL that displays all surveys assigned to a record, presented in the order and manner configured in the project. Respondents access via this single link.

### Record
The unique primary identifier for a participant or subject in REDCap. The queue link is specific to a record and shows all surveys queued for that record.

### Survey Distribution Tools Privilege
A user-level permission that may be required to generate survey queue links via API, depending on REDCap version. Combined with API Export privilege.

### Content Parameter
The identifier sent in API requests specifying which type of resource to export. For Survey Queue Link, always set to `'surveyQueueLink'`.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'surveyQueueLink'` |
| `record` | Required | The record ID as it exists in the project |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'` (default: `'xml'`). Has no effect on the response itself, which is always plain text |

---

# 4. Request Examples

## 4.1 Python
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

## 4.2 R
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

## 4.3 cURL
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

## 4.4 PHP
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 5. Response

The API returns a unique survey queue URL as a plain text string (not wrapped in JSON or XML):

```
https://redcap.example.edu/surveys/?sq=Q7K2L1M5N3P8R4T9X1Y0Z6C2D5E3F4G1
```

This URL presents the respondent with all surveys in their queue for the specified record. It can be sent directly to participants or embedded in communications.

---

# 6. Common Questions

**Q: What is the difference between a survey link and a survey queue link?**
**A:** A survey link (RC-API-40) is specific to one instrument. A survey queue link (RC-API-41) presents multiple surveys in a guided workflow on a single page.

**Q: Which surveys appear in the queue?**
**A:** The queue displays all surveys assigned to the record based on your project's Survey Queue configuration. The order and visibility are set in the project design, not via API.

**Q: Can I customize which surveys appear in the queue via API?**
**A:** No. Survey queue membership is configured in the project design. Use the REDCap interface to specify which instruments are part of the queue.

**Q: Does this method accept an event parameter for longitudinal projects?**
**A:** No. Unlike some other survey API methods, this one takes only `token`, `content`, and `record`. The queue link is record-scoped, not event-scoped.

**Q: What does the response look like?**
**A:** It is a plain text URL string — not a JSON object or XML document. Don't try to parse it as JSON; just use the string directly.

**Q: What happens if the record has no surveys in its queue?**
**A:** The API still returns a valid URL, but accessing it will show a message that no surveys are available.

---

# 7. Common Mistakes & Gotchas

**Confusing surveyLink and surveyQueueLink:** These are distinct content types. Use `'surveyLink'` (RC-API-40) for a link to a single instrument; use `'surveyQueueLink'` for the full multi-survey queue workflow.

**Including event or instrument parameters:** This method does not accept `event` or `instrument`. Passing them won't necessarily cause an error — REDCap may simply ignore them — but they serve no purpose and can cause confusion.

**Trying to parse the response as JSON:** The response is plain text (a URL string). Passing it through a JSON parser will fail. Treat the response body directly as the URL.

**Survey Queue not enabled:** If Survey Queue hasn't been turned on in project settings, this method returns an error. Verify it's enabled before troubleshooting API calls.

---

# 8. Related Articles

- RC-API-01 — REDCap API
- RC-API-40 — Export Survey Link
- RC-API-42 — Export Survey Return Code
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-07 — Survey Queue (how the survey queue works; context for the queue link)
