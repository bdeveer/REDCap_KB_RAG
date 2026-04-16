RC-API-44

**Export REDCap Version API**

| **Article ID** | RC-API-44 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap instances |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API |

---

# 1. Overview

The Export REDCap Version API returns the version number of your REDCap instance. This is the simplest API method available and requires no additional parameters beyond the token. It is useful for scripting, compatibility checks, and verifying instance connectivity in automated workflows.

The method is read-only and works across all REDCap instances regardless of project configuration or user permissions.

> **Super API Tokens are accepted.** In addition to a standard project-level API token, a Super API Token can be used for this method. Super tokens are granted by a REDCap administrator via the API Tokens page in the Control Center.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'version'` |
| `format` | Required | Response format: `'csv'`, `'json'`, `'xml'` (default) |

---

# 3. Request Examples

## 3.1 Python
```python
#!/usr/bin/env python

from config import config
import requests

fields = {
    'token': config['api_token'],
    'content': 'version'
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
    content='version'
)
print(result)
```

## 3.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=version"

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
	'content' => 'version'
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

The API returns the version string as plain text:

```
16.1.3
```

The format is `MAJOR.MINOR.PATCH`. For example:
- `16.1.3` (typical production version)
- `13.12.1` (older version)
- `17.0.0` (newer version)

---

# 5. Common Questions

**Q: Why is this API useful?**
A: Use this method to (1) verify API connectivity, (2) detect instance version before calling version-specific APIs, (3) log version information in automated workflows, or (4) ensure compatibility with your script.

**Q: How do I parse the response in my script?**
A: The response is plain text. Simply read the returned string and split on periods to extract major, minor, and patch versions. Example: `version.split('.')` returns `['16', '1', '3']`.

**Q: Does the version change frequently?**
A: REDCap typically releases major and minor versions annually. Patch versions address critical issues more frequently. Check with your administrator for your instance's update schedule.

**Q: Can I use this API to detect feature availability?**
A: Partially. Version number indicates when features were introduced, but not all features are available in every instance. Consult the REDCap documentation for version-specific features.

**Q: What format does the response come in?**
A: The version endpoint accepts `format` values of `csv`, `json`, or `xml`, with `xml` as the default. That said, since the response is a single string value, the format distinction matters very little in practice — most callers just read the raw response text regardless of format.

---

# 6. Common Mistakes & Gotchas

**Incorrect content value:** Use exactly `'version'` (lowercase). Using `'Version'` or other variations will fail.

**Defaulting to XML without realizing it:** Like several other API methods, the default `format` is `xml`, not `json`. If you omit the `format` parameter and try to parse the response as JSON, it will fail. Pass `format='json'` explicitly if that's what your code expects.

---

# 7. Related Articles

- RC-API-01 — REDCap API
