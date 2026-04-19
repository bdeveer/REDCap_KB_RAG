RC-API-50

**Generate Next Record Name API**

| **Article ID** | RC-API-50 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API official documentation |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-03 — Import Records API; RC-API-05 — Rename Record API |

---

# 1. Overview

The Generate Next Record Name API method returns what the next record ID would be if a new record were created right now. It determines this by finding the current maximum numerical record ID in the project and incrementing it by one.

**Important:** This method does not create a record. It only predicts the next name. The returned value may be stale if another user or process creates a record between your call and your subsequent import.

The method works whether or not your project has record auto-numbering enabled.

**Behavior with Data Access Groups (DAGs):** If the project uses DAGs, the returned name follows the DAG-prefixed format (e.g., `223-3`). The method determines the next value for IDs within the DAG of the API user, considering all records in the entire project — including records that were originally created in that DAG but later reassigned to another DAG.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires **API Export** privileges in the project. |
| `content` | Required | Always `'generateNextRecordName'` |

---

# 3. Request Examples

## 3.1 Python

```python
#!/usr/bin/env python
from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'generateNextRecordName'
}
r = requests.post(config['api_url'], data=fields)
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
    content='generateNextRecordName'
)
print(result)
```

## 3.3 cURL

```sh
#!/bin/sh
. ./config

DATA="token=$API_TOKEN&content=generateNextRecordName"

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
    'content' => 'generateNextRecordName'
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
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);
$output = curl_exec($ch);
print $output;
?>
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See RC-API-01 Section 3.5.

---

# 4. Response

The API returns the next record name as a plain text string — the maximum integer record ID in the project plus one.

Example response for a standard project:
```
5
```

Example response for a DAG user (DAG number 223, where 223-1 and 223-2 already exist):
```
223-3
```

On error, an error message string is returned.

---

# 5. Common Questions

**Q: Does calling this method reserve the record name?**

**A:** No. This method is read-only — it does not create a record or reserve an ID. If another user or process creates a record after you call this method but before you import your record, the returned name may already be taken. Use record auto-numbering in your import call to avoid this race condition.

**Q: Can I use this method to determine the next ID before a bulk import?**

**A:** You can, but it is risky in multi-user projects. The returned value reflects the state at the moment of the call. For bulk imports, it is safer to use REDCap's auto-numbering (`forceAutoNumber=true` on import) rather than pre-generating IDs with this method.

**Q: Does this method work if auto-numbering is disabled on my project?**

**A:** Yes. The method works regardless of whether record auto-numbering is enabled. It always finds the current maximum numeric ID and adds one.

**Q: How does the DAG number affect the result?**

**A:** If you belong to a DAG, the returned record name is prefixed with your DAG's number (e.g., `223-3`). The method counts all records project-wide — including those originally created in your DAG but since moved — when determining the maximum ID within the DAG.

**Q: What if no records exist yet in the project?**

**A:** The method returns `1` (or `[DAG number]-1` for DAG users), as that would be the first record ID.

---

# 6. Common Mistakes & Gotchas

**Treating the result as a reservation.** This method does not lock or reserve the ID. In active projects with concurrent users, the next record name can change between this call and your subsequent import. Use auto-numbering in the import instead if uniqueness is critical.

**Wrong `content` value casing.** The parameter value is `'generateNextRecordName'` — camelCase, all one word. Any variation (e.g., `'GenerateNextRecordName'`, `'generate_next_record_name'`) will fail.

**Expecting the DAG prefix without belonging to a DAG.** The DAG-prefixed format only applies when the API token belongs to a user who is currently assigned to a DAG. If the user is not in a DAG, a plain integer is returned regardless of project DAG configuration.

---

# 7. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-03 — Import Records API (creating records; use `forceAutoNumber` to avoid race conditions)
- RC-API-05 — Rename Record API (changing record IDs after creation)
