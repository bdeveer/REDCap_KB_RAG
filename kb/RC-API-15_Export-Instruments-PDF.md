RC-API-15

**Export Instruments PDF API**

| **Article ID** | RC-API-15 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API |

---

# 1. Overview

The Export Instruments PDF API method generates a PDF document containing one or more data collection instruments (forms) from your REDCap project. It returns the exact same PDF file that is downloadable from a project's data entry form in the web interface.

There are five distinct export modes, controlled by which parameters you pass:

1. A single instrument, blank (template for one form)
2. All instruments, blank (templates for every form in the project)
3. A single instrument, populated with data from one record
4. All instruments, populated with data from one record
5. All instruments, populated with data from **all** records (one page per record/instrument)

Requires **API Export** privileges. The user's data export rights are enforced just as they are in the web interface — if the user has de-identified data export rights, certain fields will be removed or blanked out in the generated PDF. If the user has **No Access** data export rights, the method will return an error.

This method is useful for generating printable forms, creating patient handouts, or exporting blank form templates for external use.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'pdf'` for this method. |
| `record` | Optional | The record ID for which to populate the PDF with data. If blank (default), returns a PDF with no data. If provided, returns a single instrument or all instruments populated with data from that record only. |
| `event` | Optional | The unique event name (longitudinal projects only). If `record` is provided and `event` is blank, returns data for all events for that record. If both are provided, returns data only for the specified event. |
| `instrument` | Optional | The unique instrument (variable) name as seen in the second column of the Data Dictionary. If blank (default), exports all instruments. If `record` is provided and `instrument` is blank, returns all instruments for that record. |
| `repeat_instance` | Optional | For projects with repeating instruments/events only. The repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default is `1`. |
| `allRecords` | Optional | If this parameter is passed **with any value** (the value itself is ignored), it exports all instruments — and all events, for longitudinal projects — populated with data from every record in the project. When `allRecords` is passed, the `record`, `event`, and `instrument` parameters are ignored. |
| `compactDisplay` | Optional | Set to `TRUE` to return a compact-formatted PDF that excludes fields with no data saved and omits unselected multiple choice options, producing a smaller file. Set to `FALSE` (default) to display all fields normally. |
| `returnFormat` | Optional | `csv`, `json` [default], or `xml`. Only affects the format of error messages returned by the API — it does not change the PDF itself. |

> **Note on `allRecords`:** Because its value is ignored, simply including `allRecords` in your POST payload will trigger the all-records export. Do not include `allRecords` unless you want that behavior.

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

**Q: How do I export a single instance from a repeating instrument or event?**

**A:** Pass `repeat_instance` along with `record` (and `event`, if longitudinal). For example, `repeat_instance=3` returns the third instance. If you omit it, REDCap defaults to instance `1`.

**Q: How do I shrink the PDF when exporting records with a lot of empty fields?**

**A:** Set `compactDisplay=TRUE`. This excludes fields with no saved data and hides unselected multiple choice options, which can significantly reduce the size of PDFs for records that only populated a subset of fields.

**Q: The API returned an error instead of a PDF — why?**

**A:** The most common cause is insufficient export privileges. If your user account has **No Access** data export rights for the project, this method will fail. If you have **De-Identified** export rights, the method will succeed but certain identifier fields will be stripped from the PDF, matching the behavior of the web interface.

---

# 6. Common Mistakes & Gotchas

**Writing the file in text mode instead of binary mode.** The most common mistake is opening the file for writing in text mode. Always use binary mode: `'wb'` in Python, `writeBin()` in R, or `fopen($file, 'wb')` in PHP.

**Forgetting the `event` parameter in longitudinal projects.** If you want to export data for a record in a specific event, include the `event` parameter. Omitting it may result in an incomplete PDF or an error.

**Accidentally including `allRecords` in the payload.** The value of `allRecords` is ignored — merely passing the parameter (with any value, including `false` or an empty string) triggers the all-records export, and causes `record`, `event`, and `instrument` to be silently ignored. Only include `allRecords` when you actually want to export every record.

**Forgetting `repeat_instance` for repeating data.** If you're exporting data from a repeating instrument or repeating event and don't pass `repeat_instance`, you'll get instance `1` by default. This may not be the instance you wanted.

**Assuming `returnFormat` changes the PDF.** `returnFormat` only controls the format of API error responses (csv/json/xml). The successful response is always a binary PDF regardless of this setting.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-FD-01 — Form Design Overview (instrument design concepts and terminology)
- RC-SURV-09 — PDF Snapshots of Records (manual PDF export for records; related concept)
