RC-API-11

**Import Instrument-Event Mappings API**

| **Article ID** | RC-API-11 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API; RC-API-10 — Export Instrument-Event Mappings |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-09 — Export Instruments; RC-API-10 — Export Instrument-Event Mappings; RC-API-20 — Import Events |
| **Important** | **Longitudinal projects only** — This method is only available for longitudinal projects (projects with multiple arms and/or repeating events). Classic projects do not have instrument-event mappings. |

---

# 1. Overview

The Import Instrument-Event Mappings API method allows you to create or modify the mapping of instruments (forms) to events in a longitudinal REDCap project. This controls which instruments are presented to users at each event and repeating instance. This method enables automated configuration of longitudinal project workflows, cloning of project structures, and bulk modification of instrument-event assignments.

When to use this method: When you need to programmatically assign instruments to events, clone the event structure from one project to another, automate longitudinal project provisioning, or bulk update instrument-event mappings.

---

# 2. Important Notes

- **Longitudinal Only:** This method only works with longitudinal projects. Using it on a classic project returns an error.
- **Development Status Only:** This method is only available for projects in Development status. It cannot be used on projects in Production or Analysis status.
- **Requires API Import/Update AND Project Design/Setup:** You must have both API Import/Update privileges and Project Design/Setup privileges in the project. API Import/Update alone is not sufficient.
- **Replaces Existing Mappings:** This method replaces the entire mapping structure. All existing mappings are removed and replaced with the provided data.
- **Instruments Must Exist:** All instruments referenced in the mappings must already exist in the project. Use RC-API-07 (Export Metadata) or RC-API-09 (Export Instruments) to verify.
- **Events Must Exist:** All events referenced in the mappings must already exist in the project. Create events using RC-API-20 (Import Events) if needed.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update **and** Project Design/Setup rights. |
| `content` | Required | Always `'formEventMapping'` for this method. |
| `format` | Required | Data format of the `data` parameter: `'csv'`, `'json'`, or `'xml'` [default: `xml`]. |
| `data` | Required | The mappings to import. Each mapping must contain `arm_num` (arm number), `unique_event_name` (the auto-generated unique event name), and `form` (the instrument's unique form name). Provide in the format specified by `format`. |
| `returnFormat` | Optional | Specifies the format of error messages: `'csv'`, `'json'`, or `'xml'`. If omitted, defaults to the `format` value (or `xml` if `format` was also omitted). Does not apply when using a background process (`backgroundProcess=true`) — in that case, `success:true` or `success:false` is returned in the appropriate format. |

---

# 4. Data Structure

The `data` parameter is a flat list of instrument-event mappings — one row per instrument per event. Each mapping has three fields: `arm_num`, `unique_event_name`, and `form`. The officially documented format is flat (not nested).

**JSON format:**
```json
[{"arm_num":"1","unique_event_name":"baseline_arm_1","form":"demographics"},
{"arm_num":"1","unique_event_name":"visit_1_arm_1","form":"day_3"},
{"arm_num":"1","unique_event_name":"visit_1_arm_1","form":"other"},
{"arm_num":"1","unique_event_name":"visit_2_arm_1","form":"other"}]
```

**CSV format:**
```
arm_num,unique_event_name,form
1,baseline_arm_1,demographics
1,visit_1_arm_1,day_3
1,visit_1_arm_1,other
1,visit_2_arm_1,other
```

**XML format:**
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<items>
   <item>
      <arm_num>1</arm_num>
      <unique_event_name>baseline_arm_1</unique_event_name>
      <form>demographics</form>
   </item>
   <item>
      <arm_num>1</arm_num>
      <unique_event_name>visit_1_arm_1</unique_event_name>
      <form>day_3</form>
   </item>
   <item>
      <arm_num>1</arm_num>
      <unique_event_name>visit_1_arm_1</unique_event_name>
      <form>other</form>
   </item>
   <item>
      <arm_num>1</arm_num>
      <unique_event_name>visit_2_arm_1</unique_event_name>
      <form>other</form>
   </item>
</items>
```

> **Note:** Some REDCap API client libraries (e.g., RCurl in R) may also accept a nested structure grouping forms under each event. The flat format above is the officially documented format and should be preferred for reliability.

---

# 5. Request Examples

## 5.1 Python

```python
#!/usr/bin/env python

from config import config
import requests, json

record = {
    'arm': {
        'number': 1,
        'event': [
            {
                'unique_event_name': 'event_1_arm_1',
                'form': ['instr_1', 'instr_2',]
            },
            {
                'unique_event_name': 'event_2_arm_1',
                'form': ['instr_1',]
            },
        ]
    }
}

data = json.dumps([record])

fields = {
    'token': config['api_token'],
    'content': 'formEventMapping',
    'format': 'json',
    'data': data,
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 5.2 R

```r
#!/usr/bin/env Rscript

source('config.R')
library(RCurl)
library(jsonlite)

record <- list(
	arm=list(
		number=1,
		event=list(
			list(
				unique_event_name='event_1_arm_1',
				form=list('instr_1', 'instr_2')
			),
			list(
				unique_event_name='event_2_arm_1',
				form=list('instr_1')
			)
		)
	)
)

data <- toJSON(record, auto_unbox=TRUE)

result <- postForm(
    api_url,
    token=api_token,
    content='formEventMapping',
    format='json',
    data=data
)
print(result)
```

## 5.3 cURL

```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=formEventMapping&format=json&data=[{\"arm\":{\"number\":\"1\",\"event\":[{\"unique_event_name\":\"event_1_arm_1\",\"form\":[\"instr_1\",\"instr_2\"]}]}},{\"arm\":{\"number\":\"2\",\"event\":[{\"unique_event_name\":\"event_2_arm_1\",\"form\":[\"instr_1\"]}]}}]"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      $API_URL
```

## 5.4 PHP

```php
<?php

include 'config.php';

$data = array(
	array(
		'arm_num' => '1', 'unique_event_name' => 'event_1_arm_1', 'form' => 'instr_1',
	),
	array(
		'arm_num' => '1', 'unique_event_name' => 'event_1_arm_1', 'form' => 'instr_2',
	),
	array(
		'arm_num' => '1', 'unique_event_name' => 'event_2_arm_1', 'form' => 'instr_1',
	)
);

$data = json_encode($data);

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'formEventMapping',
	'format'  => 'json',
	'data'    => $data,
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
?>
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 for why SSL certificate validation matters.

---

# 6. Response

On success, the method returns the number of instrument-event mappings imported as a plain integer (e.g., `4`). On failure, an error message is returned in the format specified by `returnFormat` (or `format`, or `xml` by default).

---

# 7. Common Questions

**Q: What happens to existing mappings when I import new ones?**

**A:** All existing mappings are replaced by the provided mappings. If an instrument-event pair exists in the old mappings but not in the new data, it is removed. Always export and back up existing mappings before updating.

**Q: Can I add mappings without removing existing ones?**

**A:** No, this method replaces all mappings. To add new mappings without losing existing ones, first export the current mappings (RC-API-10), add your new mappings to the data, and then import the complete set.

**Q: Do I need to specify all instruments for all events?**

**A:** No, you only specify the instrument-event pairs that should exist. Instruments that don't have a mapping to an event will not be available at that event.

**Q: What if an instrument or event referenced in the data doesn't exist?**

**A:** The import fails with a validation error. Ensure all instruments and events exist before importing mappings. Create missing instruments using RC-API-08 (Import Metadata) and events using RC-API-20 (Import Events).

**Q: Can I use this on a project that's already in Production?**

**A:** No. This method only works on projects in Development status. If your project is in Production, you would need to move it back to Development first (which typically requires REDCap administrator involvement), or make the mapping changes manually through the REDCap interface.

**Q: Can I use this method to set up repeating instruments?**

**A:** This method sets up static instrument-event mappings. Repeating instruments are configured separately through project settings. Once an instrument is mapped to an event, you can configure it as repeating through the REDCap interface or other API endpoints.

---

# 8. Common Mistakes & Gotchas

**Calling this method on a project in Production or Analysis status.** This method only works on projects in Development status. If your project is in Production, you cannot use this endpoint — you need to move to Development first (or use the REDCap interface to make mapping changes via a revision/move-to-dev workflow).

**Using only API Import/Update right without Project Design/Setup.** Both privileges are required. A user with only API Import/Update will get a permissions error even though that right sounds sufficient for an import operation.

**Forgetting to format data as JSON array.** The data must be a JSON-encoded array, even if you're only importing a few mappings. Single mapping objects must be wrapped in an array.

**Using incorrect event names.** Event names are case-sensitive. If you reference `'event_1_arm_1'` but the actual event is `'Event_1_Arm_1'`, the import fails with a validation error.

**Referencing non-existent instruments.** If you map an instrument that doesn't exist in the project, the import fails. Verify all instrument names exist before importing mappings.

**Failing to back up current mappings.** Since this method replaces all existing mappings, always export the current state (RC-API-10) before importing changes. If something goes wrong, you can restore the previous mappings.

**Incomplete mapping data.** If you omit important arms or events, the resulting project structure will be incomplete. Ensure your mapping data covers all arms and events that should exist.

**Not testing on a development copy.** Always test instrument-event mapping changes on a development or test project first. Mistakes can disrupt the entire project workflow.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-10 — Export Instrument-Event Mappings (read current mappings)
- RC-API-09 — Export Instruments (list available instruments)
- RC-API-20 — Import Events (create or update events)
- RC-API-08 — Import Metadata (create or update instruments/fields)
- RC-LONG-01 — Longitudinal Project Setup (how arms and events are structured)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeating instruments are configured per event)
