RC-API-35

**Import Project Info API**

| **Article ID** | RC-API-35 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-34 — Export Project Info; RC-API-37 — Import Project (Create Project) |

---

# 1. Overview

The Import Project Info API allows you to update project-level settings programmatically, such as project title, longitudinal configuration, and survey enablement. This method is useful for bulk modifications across multiple projects or automated project setup workflows.

**Important:** This method is **PHP-only**. Python, R, and cURL implementations are not available for this API endpoint.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'project_settings'` |
| `format` | Optional | Response format: `'json'` (default) or `'xml'` |
| `data` | Required | JSON-encoded array of project settings to update |

**Data Field Options:**

| Field | Type | Description |
|---|---|---|
| `project_title` | String | Project name (up to 255 characters) |
| `is_longitudinal` | Integer | `0` (classic) or `1` (longitudinal) |
| `surveys_enabled` | Integer | `0` (disabled) or `1` (enabled) |

---

# 3. Request Examples

## 3.1 PHP
```php
<?php

include 'config.php';

$data = array(
	'project_title' => 'New Project Title via API',
	'is_longitudinal' => 0,
	'surveys_enabled' => 1
);

$params = array(
    'token' => $GLOBALS['api_token'],
    'content' => 'project_settings',
    'format' => 'json',
    'data' => json_encode($data)
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $GLOBALS['api_url']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params, '', '&'));
$output = curl_exec($ch);
print $output;
```

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is `false` for compatibility. Set to `true` in production. See RC-API-01 Section 3.5.

**Python, R, and cURL implementations are not available for this endpoint.**

---

# 4. Response

On success, the API returns a JSON message confirming the update:

```json
{
  "success": true,
  "message": "Project settings updated successfully"
}
```

On error, you receive an error object with details:

```json
{
  "error": "Invalid project_title: exceeds 255 characters"
}
```

---

# 5. Common Questions

**Q: Why is this API method PHP-only?**
A: This endpoint has historically had limited implementation across language libraries. PHP remains the most widely supported and tested implementation for updating project settings.

**Q: Can I enable longitudinal mode on an existing project?**
A: Only if the project has no data yet. Longitudinal must be set during project creation or before any records are added. Use RC-API-37 (Import Project / Create Project) to create new longitudinal projects.

**Q: What happens if I leave a field blank in the data array?**
A: Fields omitted from the data array are not modified. Only include fields you intend to change.

**Q: Do I need Project Setup rights to use this method?**
A: Yes. You must have Project Setup / Design rights to modify project settings via the API.

**Q: Can I update surveys_enabled after the project is in production?**
A: Yes. You can enable or disable surveys on a project at any time, even after data collection has begun.

---

# 6. Common Mistakes & Gotchas

**PHP-only limitation:** Attempting to use this endpoint with Python, R, or cURL will fail. Always use PHP or implement a PHP wrapper service if you need to call this from other languages.

**JSON encoding requirement:** The `data` parameter must be properly JSON-encoded. Test your JSON serialization carefully, especially for special characters in project titles.

**Project title length:** Project titles are limited to 255 characters. Longer titles will trigger an error and the update will fail.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-34 — Export Project Info
- RC-API-37 — Import Project (Create Project)
