---
id: RC-API-44
title: Export REDCap Version API
domain: API
applies_to:
- All REDCap instances
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — version
  export behaviour checked against source code; pages not re-captured
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
- export redcap version api method
- how do i get the redcap version number via the api
- api call to check the redcap instance version
- retrieve the server redcap version through the api
- api method to verify connectivity and version
- programmatically read the redcap version with the api
- get redcap build version using a super or project token
---

# 1. Overview

The Export REDCap Version API returns the version number of your REDCap instance. This is the simplest API method available and requires no parameters beyond `token` and `content`. It is useful for scripting, compatibility checks, and verifying instance connectivity in automated workflows.

The method is read-only and works the same on every REDCap instance, whatever the project's configuration. It does still check the token:

- **With a project API token**, the token's user needs **API Export** rights in that project. A token with API Import only is refused with HTTP 403 and the message "You do not have API Export privileges". If the project is offline, the call returns an error instead of the version.
- **With a Super API Token**, no project rights are needed.

Each call is recorded in REDCap's logging, like other API requests.

> **Super API Tokens are accepted.** In addition to a standard project-level API token, a Super API Token can be used for this method. Super API Tokens are 64 characters long (project tokens are 32), and only REDCap administrators can issue them, via the API Tokens page in the Control Center.

---

# 2. Key Concepts & Definitions

### API Token
A unique string credential issued by a REDCap administrator that authorizes API requests on behalf of a specific user in a specific project. Tokens are required for all API calls and can be standard (project-level) or Super tokens (cross-project).

### Version String
A semantic version identifier in the format MAJOR.MINOR.PATCH (e.g., 16.1.3) that indicates the current release of a REDCap instance. Version numbers determine which features and API endpoints are available.

### Super API Token
A special administrator-issued token that grants API access across multiple projects, without being tied to a single project context. Used primarily for administrative and system-level workflows.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'version'` |
| `format` | Optional | Ignored for the result: the version is always returned as plain text. `format` (or `returnFormat`) only changes how error messages are formatted |

---

# 4. Request Examples

## 4.1 Python
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

## 4.2 R
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

## 4.3 cURL
```sh
#!/bin/sh

. ./config

DATA="token=$API_TOKEN&content=version"

$CURL -H "Content-Type: application/x-www-form-urlencoded" \
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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `FALSE` for compatibility. Set to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) Section 3.5.

---

# 5. Response

The API returns the version string as plain text, with no JSON, XML or CSV wrapping, whatever `format` you send:

```
17.6.5
```

The response is sent with a `text/csv` content type even though it is a bare string. Read the raw response body as text; do not pass it to a JSON or XML parser.

The format is `MAJOR.MINOR.PATCH`. For example:
- `16.1.3` (typical production version)
- `13.12.1` (older version)
- `17.0.0` (newer version)

---

# 6. Common Questions

**Q: Why is this API useful?**
**A:** Use this method to (1) verify API connectivity, (2) detect instance version before calling version-specific APIs, (3) log version information in automated workflows, or (4) ensure compatibility with your script.

**Q: How do I parse the response in my script?**
**A:** The response is plain text. Read the returned string (trimming any surrounding whitespace) and split on periods to extract major, minor, and patch versions. Example: `version.split('.')` returns `['16', '1', '3']`.

**Q: Does the version change frequently?**
**A:** REDCap typically releases major and minor versions annually. Patch versions address critical issues more frequently. Check with your administrator for your instance's update schedule.

**Q: Can I use this API to detect feature availability?**
**A:** Partially. Version number indicates when features were introduced, but not all features are available in every instance. Consult the REDCap documentation for version-specific features.

**Q: What format does the response come in?**
**A:** Always plain text, such as `17.6.5`. The `format` parameter does not change the result: `format=json` does not return JSON, and `format=xml` does not return XML. `format` (or `returnFormat`) only affects how error messages are formatted, so you can omit it.

---

# 7. Common Mistakes & Gotchas

**Incorrect content value:** Use exactly `'version'` (lowercase). Using `'Version'` or other variations will fail.

**Parsing the response as JSON or XML:** Unlike most API methods, this one ignores `format` for the result. Even with `format=json`, the body is the bare version string (e.g. `17.6.5`), so `r.json()` or an XML parser will fail. Read it as text, e.g. `r.text.strip()` in Python.

**Using an import-only project token:** A project token whose user lacks **API Export** rights gets HTTP 403 "You do not have API Export privileges". Use a token with API Export rights, or a Super API Token.

---

# 8. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
