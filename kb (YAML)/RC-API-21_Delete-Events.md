---
id: RC-API-21
title: Delete Events API
domain: API
applies_to:
- Longitudinal REDCap projects only
requires: Any supported version
verified_against: REDCap v17.5.6 (Standard) — §1, §2, §4–§6 (Production-status restriction
  and rights not re-tested) live-tested via the API on a sandbox project (2026-10);
  LTS line last reviewed against the v17.3.7 (LTS) changelog; Delete Events behaviour
  (incl. rights and Production status, which were not live-tested) checked against
  source code on v17.6.5 / v17.3.31 / v16.0.61
prerequisites:
- RC-API-01 — REDCap API
version: '1.3'
last_updated: 2026-11
source: REDCap API v16.1.3 official documentation examples
related:
- id: RC-API-01
  title: REDCap API
- id: RC-API-19
  title: Export Events API
- id: RC-API-20
  title: Import Events API
tags:
- api
synonyms:
- how do i delete events via the api
- delete events api call
- remove events from a longitudinal project through the api
- api method to delete unique event names
- remove events and their data via api
- bulk delete events with the api
- api endpoint to delete events
- delete timepoints from an arm programmatically
- delete events api returns 0
---

# 1. Overview

The Delete Events API method removes one or more events from a longitudinal REDCap project. You specify the unique event names to delete, and REDCap will remove them along with all data stored in those events.

> **Important:** Events exist only in longitudinal projects. On a classic project the call is not rejected: event names that don't exist in the project simply return `0`. That does not make it a safe no-op. A classic project has one hidden event of its own, and sending its name would delete it. Do not call this method on classic projects. Deleting events permanently removes all data stored in those events; recreating an event with the same name does not bring the data back. This action cannot be undone.

> **Important:** Because of this method's destructive nature, it is only available for projects in **Development** status. It cannot be used on projects in Production or Analysis/Cleanup status. This holds even when your administrators have turned on the Control Center setting that lets normal users add or modify events in production, and it applies to REDCap administrators' tokens too. An administrator can still delete an event from a Production project in the Online Designer.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. The token owner needs the **Delete Records** user right and the **Project Design and Setup** user right. |
| `content` | Required | Always `'event'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `events` | Required | An array of unique event names (strings) to delete. E.g., `events[0]=event_1_arm_1&events[1]=event_2_arm_1` in URL encoding. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'event',
    'action': 'delete',
    'format': 'json',
    'events[0]': 'event_1_arm_1'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
```

## 3.2 R

```r
source('config.R')
library(RCurl)

result <- postForm(
    api_url,
    token=api_token,
    content='event',
    action='delete',
    'events[]'=c('event_1_arm_1')
)
print(result)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=event&action=delete&format=json&events[0]=event_1_arm_1"

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
	'token'   => $GLOBALS['api_token'],
	'content' => 'event',
	'action'  => 'delete',
	'format'  => 'json',
	'events'  => array('event_1_arm_1'),
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

On success, the method returns the number of events deleted as a plain integer. The HTTP status code will be 200. All data stored in those events will be permanently removed.

If you send a mix of valid and unknown event names, the valid ones are deleted and the unknown ones are silently skipped: there is no error and nothing is rolled back. Always compare the returned count with the number of names you sent.

The project's Logging page records a generic event-deletion entry that does not list which events were deleted. Keep your own record (for example, the Export Events output from just before the call) of what you removed.

Example response:
```
1
```

---

# 5. Common Questions

**Q: Can I delete an event on a classic project?**

**A:** No. Events are a longitudinal-only feature. For event names that don't exist, the call returns `0` (HTTP 200), but it is not a safe no-op: a classic project has one hidden event, and deleting it would leave the project without an event. Don't call this method on classic projects.

**Q: My project is in Production. Can I use Delete Events?**

**A:** No. Delete Events is only available for projects in **Development** status. Because deletion causes irreversible data loss, REDCap restricts this method to Development as a safeguard. The Control Center setting that lets normal users add or modify events in production does not lift this restriction, and administrators' tokens are blocked as well. An administrator can delete an event from a Production project in the Online Designer instead. If you need to remove an event from a Production project, you must move it back to Development first, which should be done with great care to avoid disrupting active data collection.

**Q: Do I need any special permissions beyond API access?**

**A:** Yes. The token owner needs both the **Delete Records** user right and the **Project Design and Setup** user right. Without Delete Records, REDCap returns HTTP 403 "You do not have Delete Record privileges". The error message returned when Project Design and Setup is missing also mentions API Import rights, so its text can be misleading.

**Q: What happens to the data when I delete an event?**

**A:** All data stored in the deleted event is permanently deleted from the project. Before deleting an event, export the data you need to preserve. This action cannot be undone.

**Q: How do I find the correct `unique_event_name`?**

**A:** Use the Export Events method ([RC-API-19 — Export Events API](RC-API-19_Export-Events.md)) to retrieve the list of events. The response will include the `unique_event_name` for each event. Do not confuse `unique_event_name` with `event_name` (the human-readable label).

**Q: How do I specify multiple events to delete?**

**A:** Provide the `events` parameter as an array. In URL encoding: `events[0]=event_1_arm_1&events[1]=event_2_arm_1`. In Python: `'events[0]': 'event_1_arm_1', 'events[1]': 'event_2_arm_1'`. In R: `'events[]'=c('event_1_arm_1', 'event_2_arm_1')`. In PHP: `'events' => array('event_1_arm_1', 'event_2_arm_1')`.

---

# 6. Common Mistakes & Gotchas

**Not backing up data before deletion.** Deleting an event deletes all data in that event. There is no undo. Always export your project data before deleting events if you may need it later.

**Calling Delete Events on a classic project.** Events are a longitudinal-only feature. The call is not rejected on classic projects: names that don't exist return `0`, but the project's one hidden event can still be deleted. Always verify your project is longitudinal (Export Project Info, `is_longitudinal`) before calling this method.

**Calling Delete Events on a Production project.** This method is restricted to Development status by design — deleting events causes irreversible data loss and REDCap blocks this on Production and Analysis/Cleanup projects, for administrators too. If you get an unexpected error, check your project's status first.

**Using `event_name` instead of `unique_event_name`.** Always use the `unique_event_name` (e.g., `event_1_arm_1`), not the `event_name` (e.g., "Baseline Visit"). Using the wrong name deletes nothing — and there's no error: the call returns HTTP 200 with `0`. Check that the count matches the number of events you meant to delete.

**Misformatting the `events` parameter.** The `events` parameter must be an array. In URL encoding, use `events[0]=event_1_arm_1&events[1]=event_2_arm_1`. Do not send `events=event_1_arm_1` or `events="event_1_arm_1,event_2_arm_1"`: nothing is deleted and the call quietly returns `0`.

**Relying on the Logging page to see what was deleted.** The log entry for an API event deletion does not name the events. Save the Export Events output before you delete so you have your own record.

---

# 7. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-19 — Export Events API](RC-API-19_Export-Events.md) (retrieve event metadata from a project)
- [RC-API-20 — Import Events API](RC-API-20_Import-Events.md) (add or modify events in a project)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (events overview; context for when deletion is appropriate)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (how repeating event setup is affected by deletion)
