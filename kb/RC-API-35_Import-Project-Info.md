RC-API-35

**Import Project Info API**

| **Article ID** | RC-API-35 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-34 — Export Project Info; RC-API-37 — Import Project (Create Project) |

---

# 1. Overview

The Import Project Info API allows you to update project-level settings programmatically, such as project title, longitudinal configuration, survey enablement, PI information, and more. This method is useful for bulk modifications across multiple projects or automated project setup workflows.

**Permissions required:** You must have both **API Import/Update** privileges **and** **Project Setup/Design** privileges in the project to use this method.

---

# 2. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your unique API token string |
| `content` | Required | Always `'project_settings'` |
| `format` | Required | Data format: `'csv'`, `'json'`, or `'xml'` |
| `data` | Required | Project settings to update, in the format specified |

**Updatable fields:**

| Field | Type | Description |
|---|---|---|
| `project_title` | String | Project name |
| `project_language` | String | Language used in the project interface |
| `purpose` | Integer | Project purpose code |
| `purpose_other` | String | Free-text description when purpose is "Other" |
| `project_notes` | String | Notes about the project |
| `custom_record_label` | String | Custom label for the record ID field |
| `secondary_unique_field` | String | Field name designated as a secondary unique field |
| `is_longitudinal` | Integer | `0` (classic) or `1` (longitudinal) |
| `surveys_enabled` | Integer | `0` (disabled) or `1` (enabled) |
| `scheduling_enabled` | Integer | `0` (disabled) or `1` (enabled) |
| `record_autonumbering_enabled` | Integer | `0` (disabled) or `1` (enabled) |
| `randomization_enabled` | Integer | `0` (disabled) or `1` (enabled) |
| `project_irb_number` | String | IRB approval number |
| `project_grant_number` | String | Grant number associated with the project |
| `project_pi_firstname` | String | Principal investigator first name |
| `project_pi_lastname` | String | Principal investigator last name |
| `project_pi_email` | String | Principal investigator email address |
| `display_today_now_button` | Integer | `0` (hidden) or `1` (shown) |
| `bypass_branching_erase_field_prompt` | Integer | `0` (show prompt) or `1` (bypass prompt) |

Boolean-type fields use `0` (false/no) or `1` (true/yes).

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

---

# 4. Response

On success, the API returns the **number of values accepted for update** (including fields whose values did not change). For example, if you submitted 3 fields, you will receive `3`.

On error, you receive an error message with details about what failed.

---

# 5. Common Questions

**Q: Can I update only some project settings, or do I need to include all fields?**
A: You only need to include the fields you want to change. Fields omitted from the data payload are left untouched.

**Q: What does the return value mean?**
A: The API returns a count of how many field values were accepted — including fields that already had the submitted value. A return of `3` means 3 fields were processed, not necessarily that 3 things changed.

**Q: Do I need special permissions to use this method?**
A: Yes. You need both **API Import/Update** privileges and **Project Setup/Design** privileges. Having only one of these is not sufficient.

**Q: Can I update surveys_enabled after the project is in production?**
A: Yes. You can enable or disable surveys on a project at any time, even after data collection has begun.

---

# 6. Common Mistakes & Gotchas

**Incomplete field list:** The API supports 19 updatable fields, including PI information, IRB/grant numbers, scheduling, randomization, and record autonumbering. Don't assume only title, longitudinal mode, and surveys are available.

**Misreading the response:** The return value is an integer count, not a success/error JSON object. A numeric response indicates success; an error message string indicates failure.

**Missing permissions:** Both API Import/Update privileges and Project Setup/Design privileges are required. If you receive a permissions error, check that both are granted — not just one.

**JSON encoding requirement:** The `data` parameter must be properly encoded in the format you specified. Test your serialization carefully, especially for special characters in free-text fields like `project_title` or `project_notes`.

---

# 7. Related Articles

- RC-API-01 — REDCap API
- RC-API-34 — Export Project Info
- RC-API-37 — Import Project (Create Project)
