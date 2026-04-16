RC-API-21

**Delete Events API**

| **Article ID** | RC-API-21 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-19 — Export Events; RC-API-20 — Import Events |

---

# 1. Overview

The Delete Events API method removes one or more events from a longitudinal REDCap project. You specify the unique event names to delete, and REDCap will remove them along with all data stored in those events.

> **Important:** Events exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project. Additionally, deleting events will permanently remove all data stored in those events. This action cannot be undone.

> **Important:** Because of this method's destructive nature, it is only available for projects in **Development** status. It cannot be used on projects in Production or Analysis/Cleanup status.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update privileges and Project Design/Setup privileges. |
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See RC-API-01 — Section 3.5 for why SSL certificate validation matters.

---

# 4. Response

On success, the method returns the number of events deleted as a plain integer. The HTTP status code will be 200. All data stored in those events will be permanently removed.

Example response:
```
1
```

---

# 5. Common Questions

**Q: Can I delete an event on a classic project?**

**A:** No. Events are a longitudinal-only feature. This method will fail on classic projects.

**Q: My project is in Production. Can I use Delete Events?**

**A:** No. Delete Events is only available for projects in **Development** status. Because deletion causes irreversible data loss, REDCap restricts this method to Development as a safeguard. If you need to remove an event from a Production project, you must move it back to Development first, which should be done with great care to avoid disrupting active data collection.

**Q: Do I need any special permissions beyond API access?**

**A:** Yes. You need both **API Import/Update** privileges and **Project Design/Setup** privileges. API Export rights alone are not sufficient.

**Q: What happens to the data when I delete an event?**

**A:** All data stored in the deleted event is permanently deleted from the project. Before deleting an event, export the data you need to preserve. This action cannot be undone.

**Q: How do I find the correct `unique_event_name`?**

**A:** Use the Export Events method (RC-API-19) to retrieve the list of events. The response will include the `unique_event_name` for each event. Do not confuse `unique_event_name` with `event_name` (the human-readable label).

**Q: How do I specify multiple events to delete?**

**A:** Provide the `events` parameter as an array. In URL encoding: `events[0]=event_1_arm_1&events[1]=event_2_arm_1`. In Python: `'events[0]': 'event_1_arm_1', 'events[1]': 'event_2_arm_1'`. In R: `'events[]'=c('event_1_arm_1', 'event_2_arm_1')`. In PHP: `'events' => array('event_1_arm_1', 'event_2_arm_1')`.

---

# 6. Common Mistakes & Gotchas

**Not backing up data before deletion.** Deleting an event deletes all data in that event. There is no undo. Always export your project data before deleting events if you may need it later.

**Calling Delete Events on a classic project.** Events are a longitudinal-only feature. This method will fail on classic projects. Always verify your project is longitudinal before calling this method.

**Calling Delete Events on a Production project.** This method is restricted to Development status by design — deleting events causes irreversible data loss and REDCap blocks this on Production projects. If you get an unexpected error, check your project's status first.

**Using `event_name` instead of `unique_event_name`.** Always use the `unique_event_name` (e.g., `event_1_arm_1`), not the `event_name` (e.g., "Baseline Visit"). Using the wrong name will cause the delete to fail.

**Misformatting the `events` parameter.** The `events` parameter must be an array. In URL encoding, use `events[0]=event_1_arm_1&events[1]=event_2_arm_1`. Do not send `events=event_1_arm_1` or `events="event_1_arm_1,event_2_arm_1"` as these will not be parsed correctly.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-19 — Export Events (retrieve event metadata from a project)
- RC-API-20 — Import Events (add or modify events in a project)
- RC-LONG-01 — Longitudinal Project Setup (events overview; context for when deletion is appropriate)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeating event setup is affected by deletion)
