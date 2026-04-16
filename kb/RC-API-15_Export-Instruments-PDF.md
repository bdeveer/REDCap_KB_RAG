RC-API-15

**Export Instruments PDF API**

| **Article ID** | RC-API-15 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API |

---

# 1. Overview

The Export Instruments PDF API method generates a PDF document containing the instruments (forms) in your REDCap project. The PDF can be blank (template), populated with data from a specific record, or can include all records in the project (one page per record).

This method is useful for generating printable forms, creating patient handouts, or exporting blank form templates for external use.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'pdf'` for this method. |
| `format` | Optional | Set to `'json'` to specify JSON format preference. Default is binary PDF. |
| `record` | Optional | The record ID for which to populate the PDF with data. If omitted, returns a blank template. |
| `event` | Optional | The unique event name (longitudinal projects only). Used with `record` to export data from a specific event. |
| `instrument` | Optional | The instrument variable name to export. If omitted, exports all instruments. |
| `allRecords` | Optional | Set to `true` or `1` to generate a PDF with one page per record for the entire project. Cannot be used with `record` parameter. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'pdf',
    'format': 'json'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))

f = open('/tmp/export.pdf', 'wb')
f.write(r.content)
f.close()
```

## 3.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='pdf',
    returnFormat='json',
    binary=TRUE
)

f <- file('/tmp/export.pdf', 'wb')
writeBin(as.vector(result), f)
close(f)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=pdf&format=json"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      -o /tmp/export.pdf \
      $API_URL
```

## 3.4 PHP

```php
<?php

include 'config.php';

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'pdf',
	'format'  => 'json'
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

$fh = fopen('/tmp/export.pdf', 'w');
fputs($fh, $output);
fclose($fh);
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

The method returns a binary PDF file. The PDF should be written to disk using a binary write operation. The HTTP status code will be 200 on success.

---

# 5. Common Questions

**Q: I want to export a blank template of all forms. Which parameters should I use?**

**A:** Set `content='pdf'` and omit the `record` and `allRecords` parameters. This will generate a blank PDF template of all instruments.

**Q: Can I export a PDF for a specific record in a longitudinal project?**

**A:** Yes. Set `record=<record_id>` and `event=<unique_event_name>`. The PDF will be populated with data from that record and event.

**Q: What happens if I set both `record` and `allRecords` to true?**

**A:** The `allRecords` parameter takes precedence if both are specified. However, it is best to use only one; using both may produce unexpected results depending on your REDCap version.

**Q: The PDF is blank or not opening. What went wrong?**

**A:** You likely wrote the file in text mode instead of binary mode. Always use binary write operations: `'wb'` in Python, `writeBin()` in R, or `fopen($file, 'wb')` in PHP.

---

# 6. Common Mistakes & Gotchas

**Writing the file in text mode instead of binary mode.** The most common mistake is opening the file for writing in text mode. Always use binary mode: `'wb'` in Python, `writeBin()` in R, or `fopen($file, 'wb')` in PHP.

**Forgetting the `event` parameter in longitudinal projects.** If you want to export data for a record in a specific event, include the `event` parameter. Omitting it may result in an incomplete PDF or an error.

**Not specifying both `record` and `allRecords` correctly.** Do not use both `record` and `allRecords` in the same request. Choose one: either export for a specific record or for all records, not both.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-FD-01 — Form Design Overview (instrument design concepts and terminology)
- RC-SURV-09 — PDF Snapshots of Records (manual PDF export for records; related concept)
