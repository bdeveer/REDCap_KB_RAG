RC-API-08

**Import Metadata (Data Dictionary) API**

| **Article ID** | RC-API-08 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-API-01 — REDCap API |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | RC-API-01 — REDCap API; RC-API-07 — Export Metadata |
| **Important** | **Development status only** — This method only works on projects in Development status. It cannot be used on projects in Production or Analysis/Cleanup status. |

---

# 1. Overview

The Import Metadata API method allows you to create or update the data dictionary (metadata) for a REDCap project programmatically. This is the primary way to modify project structure via API — adding fields, forms, validation rules, branching logic, and other configuration details. This method enables automated project setup, project cloning, and bulk metadata modifications.

When to use this method: When you need to programmatically create or modify the data dictionary, import a data dictionary from another project, automate project provisioning, or bulk update field properties across many fields.

---

# 2. Important Notes

- **Development status only:** This method is restricted to projects in Development status. Attempting to use it on a Production or Analysis/Cleanup project will fail. This restriction exists because of the method's destructive potential.
- **Dual permission requirement:** You must have both API Import/Update privileges and Project Design/Setup privileges. Either one alone is not sufficient.
- **Metadata Validation:** REDCap validates the metadata before import. Invalid field definitions will be rejected with error messages.
- **Destructive Operation:** This method can overwrite or remove existing field definitions. Always test on a development project, and export a backup of the current metadata (RC-API-07) before importing.

---

# 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update and Project Design/Setup rights. |
| `content` | Required | Always `'metadata'` for this method. |
| `format` | Required | Format of the `data` being imported: `'csv'`, `'json'`, or `'xml'` (default). |
| `data` | Required | The formatted metadata to import. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to match `format` if omitted; defaults to `'xml'` if neither is passed. Does not apply when using a background process. |

---

# 4. Data Structure

The `data` parameter must contain field definitions in JSON format. Each field is an object with the following structure:

```json
[
  {
    "field_name": "f1",
    "form_name": "instr_1",
    "section_header": "",
    "field_type": "text",
    "field_label": "f1",
    "select_choices_or_calculations": "",
    "field_note": "",
    "text_validation_type_or_show_slider_number": "",
    "text_validation_min": "",
    "text_validation_max": "",
    "identifier": "",
    "branching_logic": "",
    "required_field": "",
    "custom_alignment": "",
    "question_number": "",
    "matrix_group_name": "",
    "matrix_ranking": "",
    "field_annotation": ""
  }
]
```

All Data Dictionary columns are supported in the import structure. Empty strings are used for optional fields that have no value.

---

# 5. Request Examples

## 5.1 PHP (Full Example)

```php
<?php

include 'config.php';

$data = array(
	'field_name' => 'f1',
	'form_name' => 'instr_1',
	'section_header' => '',
	'field_type' => 'text',
	'field_label' => 'f1',
	'select_choices_or_calculations' => '',
	'field_note' => '',
	'text_validation_type_or_show_slider_number' => '',
	'text_validation_min' => '',
	'text_validation_max' => '',
	'identifier' => '',
	'branching_logic' => '',
	'required_field' => '',
	'custom_alignment' => '',
	'question_number' => '',
	'matrix_group_name' => '',
	'matrix_ranking' => '',
	'field_annotation' => ''
);

$data = json_encode( array( $data ) );

$fields = array(
	'token'   => $GLOBALS['api_token'],
	'content' => 'metadata',
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

The method returns a count of fields that were successfully created or modified, along with any validation errors.

**Successful response (JSON):**
```json
{
  "count": 1
}
```

**Response with errors (JSON):**
```json
{
  "error": "Error validating metadata: Field 'f1' in form 'instr_1' is invalid because [specific error message]"
}
```

---

# 7. Common Questions

**Q: What permissions do I need to use this method?**

**A:** You need two separate rights: API Import/Update privileges and Project Design/Setup privileges. Both are required — having only one is not sufficient.

**Q: Can I import a data dictionary from one project to another?**

**A:** Yes. Export the metadata from the source project (RC-API-07), format it correctly, and import it into the destination project using this method. Be aware that field names and form names must be unique within the destination project.

**Q: What happens if I try to import a field that already exists?**

**A:** If the field name and form name match an existing field, the existing field is updated with the new properties. If only the name is the same but form differs, it is treated as a new field.

**Q: Can I delete fields using this method?**

**A:** No, this method only creates or updates fields. To delete fields, you must do so manually in the REDCap interface or use project editing features not available via this API method.

**Q: What field types are supported?**

**A:** All field types are supported: text, number, date, choice (radio, dropdown, checkbox), matrix, file upload, calculated, slider, and custom fields. Ensure field_type is set to a valid REDCap field type.

**Q: Can I modify field labels and validation rules using this method?**

**A:** Yes. Most Data Dictionary columns can be modified via import, including field_label, text_validation rules, branching_logic, and field_note. Some properties like identifier status may have restrictions.

---

# 8. Common Mistakes & Gotchas

**Attempting to import on a Production or Analysis/Cleanup project.** This method is restricted to Development status only. If your project has already moved to Production, the API call will fail. You must either use the GUI to make changes in Production (which requires a move-to-production request) or move the project back to Development if your institution allows it.

**Not formatting data as JSON array.** The data must be a JSON-encoded array, even if you're only importing one field. Single objects must be wrapped in an array: `json_encode([field_object])`.

**Forgetting form_name for each field.** Every field must belong to a form (instrument). The form_name is required, even for the primary identifier record_id field. If you omit it, import fails.

**Using invalid field types.** Field types must match REDCap's predefined types (text, radio, dropdown, etc.). Typos in field_type cause validation errors. Always validate field_type against the REDCap documentation.

**Circular branching logic.** If you import branching logic that references fields that don't exist or creates circular dependencies, the import fails with a validation error. Test branching logic carefully.

**Matrix and slider field misconfigurations.** Matrix fields require matrix_group_name; slider fields require specific validation settings. Incomplete configuration of these field types causes errors.

**Exceeding project field limits.** Some REDCap instances have limits on the number of fields per project. If you exceed the limit, the import fails. Check your instance configuration.

**Not validating data before import.** Always test metadata imports on a development project first. Importing invalid metadata can corrupt your project structure.

---

# 9. Related Articles

- RC-API-01 — REDCap API (overview; authentication, tokens, playground)
- RC-API-07 — Export Metadata (read the data dictionary)
- RC-FD-02 — Online Designer (the GUI alternative to API-based metadata import)
- RC-FD-03 — Data Dictionary (format specification for the CSV being imported)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (column reference for valid values in each field)
