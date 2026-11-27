---
id: RC-API-15
title: Export Instruments PDF API
domain: API
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Export
  Instruments PDF behaviour checked against source code; pages not re-captured
prerequisites:
- RC-API-01 — REDCap API
version: '1.2'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
tags:
- api
synonyms:
- how do i export an instrument as a pdf via the api
- export instruments pdf api call
- generate a pdf of a form through the api
- api method to download form pdf
- get a blank or filled pdf of an instrument via api
- programmatically create instrument pdfs with the api
- api endpoint to export instrument pdf
- download data entry form as pdf using the api
---

# 1. Overview

The Export Instruments PDF API method generates a PDF document containing one or more data collection instruments (forms) from your REDCap project. It returns the exact same PDF file that is downloadable from a project's data entry form in the web interface.

There are five distinct export modes, controlled by which parameters you pass:

1. A single instrument, blank (template for one form)
2. All instruments, blank (templates for every form in the project)
3. A single instrument, populated with data from one record
4. All instruments, populated with data from one record
5. All instruments, populated with data from **all** records (one page per record/instrument)

Requires **API Export** privileges. The user's data export rights are enforced just as they are in the web interface, per instrument:

| Data export right on an instrument | Effect on the API PDF |
|---|---|
| **Full Data Set** | All data shown. |
| **Remove All Identifier Fields** | Fields marked as identifiers show `[*DATA REMOVED*]`. |
| **De-Identified** | Identifiers **and** free-text, notes and date/time fields show `[*DATA REMOVED*]`. |
| **No Access** | See below — the instrument's data cannot be exported. |

The record ID itself is only hashed or removed if the record ID field is marked as an identifier.

**No Access** behaves differently depending on the request:

- **All instruments** (no `instrument` parameter) when the user has **No Access** on every instrument: the API returns an HTTP 403 error. This also blocks blank PDFs through the API.
- **All instruments** when only some instruments are **No Access**: the PDF is generated, with that instrument's data removed.
- **A single instrument** (`instrument=...`) that is **No Access** for the user: REDCap returns HTTP 200 with a short plain-text error message instead of a PDF, not a normal API error. If you save the response straight to a `.pdf` file, you get a file that will not open.

> **Important:** Always check that the response really is a PDF before saving it (for example, the content starts with `%PDF`). Do not rely on the HTTP status code alone, and do not rely on the Content-Type header.

Further restrictions:

- **Data Access Groups:** A user in a DAG can only export records in their own DAG. A record outside it is reported as not existing, and `allRecords` only includes the DAG's records.
- **Double Data Entry:** Users acting as DDE person 1 or 2 cannot use this method (HTTP 403).
- **`@HIDDEN-PDF`:** Fields with this action tag are left out of the PDF, as in the web interface.

This method is useful for generating printable forms, creating patient handouts, or exporting blank form templates for external use.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Export right. |
| `content` | Required | Always `'pdf'` for this method. |
| `record` | Optional | The record ID for which to populate the PDF with data. If blank (default), returns a PDF with no data. If provided, returns a single instrument or all instruments populated with data from that record only. |
| `event` | Optional | The unique event name (longitudinal projects only). If `record` is provided and `event` is blank, returns data for all events for that record. If both are provided, returns data only for the specified event. If you also pass `instrument`, `event` is effectively required: it must be a valid event to which that instrument is designated, otherwise REDCap returns an HTML page instead of a PDF. |
| `instrument` | Optional | The unique instrument (variable) name as seen in the second column of the Data Dictionary. If blank (default), exports all instruments. If `record` is provided and `instrument` is blank, returns all instruments for that record. |
| `repeat_instance` | Optional | For projects with repeating instruments/events only. The repeat instance number of the repeating event (longitudinal) or repeating instrument (classic or longitudinal). Default is `1`. Only applies when a single `instrument` is requested. |
| `allRecords` | Optional | If this parameter is passed **with any value** (the value itself is ignored), it exports all instruments — and all events, for longitudinal projects — populated with data from every record in the project (or in the user's DAG). When `allRecords` is passed, the `record`, `event`, and `instrument` parameters are ignored for the output, although a `record` or `instrument` you pass is still checked first and an invalid one still produces an error. |
| `compactDisplay` | Optional | Set to `TRUE` (or `1`) to return a compact-formatted PDF that excludes fields with no data saved and omits unselected multiple choice options, producing a smaller file. Set to `FALSE` (default) to display all fields normally. |
| `returnFormat` | Optional | `csv`, `json`, or `xml`. Only affects the format of error messages returned by the API — it does not change the PDF itself. If omitted, REDCap uses the value of `format` if you passed one (as the examples below do), otherwise `xml`. |

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

The method returns a binary PDF file. The PDF should be written to disk using a binary write operation. The HTTP status code will be 200 on success.

An HTTP 200 does not guarantee a PDF. In these cases REDCap returns text or HTML instead:

| Situation | What comes back |
|---|---|
| Single instrument with **No Access** export right | Plain-text error message |
| Longitudinal: `record` + `instrument` with no `event`, or an event the instrument is not designated to | HTML page (redirect), not a PDF |
| `allRecords` in a project with no records (or none in the user's DAG) | HTML notice |

Check the first bytes of the response (`%PDF`) before saving or forwarding it.

Each export is logged in the project's Logging as a PDF download made through the API. A PDF generated with `allRecords` through the API is not saved to the File Repository.

> **Version caveat (REDCap 16.0.61 LTS vs 17.x):** Enhanced signature fields (17.3+) appear in the PDF as the signature image. Instance Embedding tables, which show repeating instances inside another instrument, are rendered in the PDF in 17.6 (only where those REDCap+ features are available). On 16.0.61 neither appears this way, and 17.3 LTS does not render Instance Embedding tables — generate a test PDF on your own instance before relying on either in printed output.

---

# 5. Common Questions

**Q: I want to export a blank template of all forms. Which parameters should I use?**

**A:** Set `content='pdf'` and omit the `record` and `allRecords` parameters. This will generate a blank PDF template of all instruments.

**Q: Can I export a PDF for a specific record in a longitudinal project?**

**A:** Yes. Set `record=<record_id>` and `event=<unique_event_name>`. The PDF will be populated with data from that record and event. If you also set `instrument`, the event must be one the instrument is designated to; otherwise you get an HTML page instead of a PDF.

**Q: What happens if I set both `record` and `allRecords` to true?**

**A:** The `allRecords` parameter takes precedence if both are specified. However, it is best to use only one; using both may produce unexpected results depending on your REDCap version.

**Q: The PDF is blank or not opening. What went wrong?**

**A:** You likely wrote the file in text mode instead of binary mode. Always use binary write operations: `'wb'` in Python, `writeBin()` in R, or `fopen($file, 'wb')` in PHP.

**Q: How do I export a single instance from a repeating instrument or event?**

**A:** Pass `repeat_instance` along with `record` (and `event`, if longitudinal). For example, `repeat_instance=3` returns the third instance. If you omit it, REDCap defaults to instance `1`.

**Q: How do I shrink the PDF when exporting records with a lot of empty fields?**

**A:** Set `compactDisplay=TRUE`. This excludes fields with no saved data and hides unselected multiple choice options, which can significantly reduce the size of PDFs for records that only populated a subset of fields.

**Q: The API returned an error instead of a PDF — why?**

**A:** The most common cause is insufficient export privileges. If your account has **No Access** data export rights on every instrument, the method returns HTTP 403. If you request a single instrument that is **No Access** for you, you get HTTP 200 with a plain-text error message instead of a PDF. With **De-Identified** or **Remove All Identifier Fields** rights the method succeeds, but the affected fields show `[*DATA REMOVED*]`, matching the web interface. Other causes: the record is outside your Data Access Group (reported as not existing), you are a Double Data Entry user (403), or, in a longitudinal project, the instrument is not designated to the event you passed.

**Q: Is the API PDF of an e-Consent survey the official signed copy?**

**A:** No. The API generates a fresh PDF from the current data; it is not the archived e-Consent snapshot that REDCap stored when the participant consented. For the official copy, use the stored PDF in the File Repository or a PDF Snapshot — see [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) and [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md). To retrieve stored files programmatically, see [RC-API-47 — Export a File (File Repository) API](RC-API-47_Export-File-File-Repository.md).

---

# 6. Common Mistakes & Gotchas

**Writing the file in text mode instead of binary mode.** The most common mistake is opening the file for writing in text mode. Always use binary mode: `'wb'` in Python, `writeBin()` in R, or `fopen($file, 'wb')` in PHP.

**Forgetting the `event` parameter in longitudinal projects.** Without `event`, an all-instruments export for a record covers all its events. With `instrument` set, `event` must be a valid event the instrument is designated to; otherwise REDCap returns an HTML page instead of a PDF.

**Treating every HTTP 200 as a PDF.** A No Access single-instrument request, a wrong longitudinal event or an empty `allRecords` export all return text or HTML with status 200. Check that the response starts with `%PDF` before saving it.

**Using the API PDF as the e-Consent record.** The API regenerates the PDF; the archived consent PDF lives in the File Repository / PDF Snapshots.

**Accidentally including `allRecords` in the payload.** The value of `allRecords` is ignored — merely passing the parameter (with any value, including `false` or an empty string) triggers the all-records export, and causes `record`, `event`, and `instrument` to be silently ignored. Only include `allRecords` when you actually want to export every record.

**Forgetting `repeat_instance` for repeating data.** If you're exporting data from a repeating instrument or repeating event and don't pass `repeat_instance`, you'll get instance `1` by default. This may not be the instance you wanted. `repeat_instance` only applies when you also pass a single `instrument`.

**Assuming `returnFormat` changes the PDF.** `returnFormat` only controls the format of API error responses (csv/json/xml). The successful response is always a binary PDF regardless of this setting. If you omit it, error messages use the `format` value, or XML if neither is passed.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (instrument design concepts and terminology)
- [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md) (manual PDF export for records; related concept)
- [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) (where the archived consent PDF is stored)
- [RC-FILE-01 — File Repository](RC-FILE-01_File-Repository.md) (stored PDFs, including e-Consent copies)
