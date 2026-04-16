RC-API-18

**Delete Arms API**

| **Article ID** | RC-API-18 |
|---|---|
| **Domain** | API |
| **Applies To** | Longitudinal REDCap projects only |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-16 — Export Arms; RC-API-17 — Import Arms |

---

# 1. Overview

The Delete Arms API method removes one or more arms from a longitudinal REDCap project. You specify the arm numbers to delete, and REDCap will remove them along with all their associated events and all data collected under those events.

> **Important:** This method is only available for projects in **Development status**. It will not work on projects in Production or Analysis/Cleanup status.

> **Important:** Arms exist only in longitudinal projects. This method will return an error if called on a classic (non-longitudinal) project. Deleting an arm permanently deletes all events in that arm and all data collected under those events — this cannot be undone.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update right **and** Project Design/Setup right. |
| `content` | Required | Always `'arm'` for this method. |
| `action` | Required | Always `'delete'` for this method. |
| `format` | Optional | Set to `'json'` or `'csv'`. Default is JSON. |
| `arms` | Required | An array of arm numbers (integers) to delete. E.g., `arms[0]=1&arms[1]=2` in URL encoding, or a JSON array in JSON mode. |

---

# 3. Request Examples

## 3.1 Python

```python
from config import config
import requests, json

fields = {
    'token': config['api_token'],
    'content': 'arm',
    'action': 'delete',
    'format': 'json',
    'arms[0]': '1'
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
    content='arm',
    action='delete',
    'arms[]'=c('1')
)
print(result)
```

## 3.3 cURL

```sh
. ./config

DATA="token=$API_TOKEN&content=arm&action=delete&format=json&arms[0]=1"

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
	'content' => 'arm',
	'action'  => 'delete',
	'format'  => 'json',
	'arms'  => array(1),
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

On success, the method returns the number of arms deleted as a plain integer. All data stored in those arms' events will be permanently removed.

Example response:
```
1
```

---

# 5. Common Questions

**Q: Can I delete an arm on a classic project?**

**A:** No. Arms are a longitudinal-only feature. This method will fail on classic projects.

**Q: Can I delete arms on a project that is in Production status?**

**A:** No. Delete Arms is restricted to projects in Development status. If your project is in Production, you cannot use this API method. To delete arms you would need to move the project back to Development status first — but be aware that doing so on a live project carries significant risk.

**Q: What happens to the data when I delete an arm?**

**A:** All events in the deleted arm and all data stored in those events are permanently deleted. Before deleting an arm, export the data you need to preserve. This action cannot be undone.

**Q: How do I specify multiple arms to delete?**

**A:** Provide the `arms` parameter as an array. In URL encoding: `arms[0]=1&arms[1]=2`. In Python: `'arms[0]': '1', 'arms[1]': '2'`. In R: `'arms[]'=c('1', '2')`. In PHP: `'arms' => array(1, 2)`.

**Q: Can I undo a deletion?**

**A:** No. Delete Arms permanently removes the arms and all associated data. Always back up your project data before deleting arms. Some REDCap instances may allow restoring from backups, but the API does not provide an undo function.

---

# 6. Common Mistakes & Gotchas

**Calling Delete Arms on a project that is not in Development status.** This method only works on projects in Development status. Calling it on a Production or Analysis/Cleanup project will fail. Check your project's status before calling this method.

**Not having Project Design/Setup privileges.** API Import/Update rights alone are not sufficient. Your API token's user account must also have Project Design/Setup privileges. If you receive a permissions error, check both rights.

**Not backing up data before deletion.** Deleting an arm deletes all events and data in that arm. There is no undo. Always export your project data before deleting arms if you may need it later.

**Calling Delete Arms on a classic project.** Arms are a longitudinal-only feature. This method will fail on classic projects. Verify your project is longitudinal before calling this method.

**Assuming arm deletion does not affect data.** Arm deletion cascades to events and data. All records, field values, and survey responses in those events are permanently deleted.

**Misformatting the `arms` parameter.** The `arms` parameter must be an array. In URL encoding, use `arms[0]=1&arms[1]=2`. Do not send `arms=1` or `arms="1,2"` as these will not be parsed correctly.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-16 — Export Arms (retrieve arm metadata from a project)
- RC-API-17 — Import Arms (add or modify arms in a project)
- RC-LONG-01 — Longitudinal Project Setup (arms overview; context for when deletion is appropriate)
