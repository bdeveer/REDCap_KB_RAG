

**Import Metadata (Data Dictionary) API**

| **Article ID** | [RC-API-08 — Import Metadata (Data Dictionary) API](RC-API-08_Import-Metadata.md) |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.6 (Standard) — §2, §4, §6–§8 (Production-status restriction not re-tested) live-tested via the API on a sandbox project (2026-10); LTS line last reviewed against the v17.3.7 (LTS) changelog. Import Metadata behaviour checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation examples |
| **Related Topics** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md); [RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)|
| **Synonyms** | how do i import the data dictionary via the api; import metadata api call; upload a data dictionary through the api; api method to modify project fields and forms; add fields and branching logic programmatically; bulk update metadata using the api; api endpoint to change project structure; load data dictionary into a project via api; import metadata api deletes fields not included; import metadata api returns number |
| **Important** | **Development status only** — This method only works on projects in Development status. It cannot be used on projects in Production or Analysis/Cleanup status (the error message says Production in both cases). |

---

## 1. Overview

The Import Metadata API method allows you to create or update the data dictionary (metadata) for a REDCap project programmatically. This is the primary way to modify project structure via API — adding fields, forms, validation rules, branching logic, and other configuration details. This method enables automated project setup, project cloning, and bulk metadata modifications.

When to use this method: When you need to programmatically create or modify the data dictionary, import a data dictionary from another project, automate project provisioning, or bulk update field properties across many fields.

---

## 2. Important Notes

- **Development status only:** This method is restricted to projects in Development status. Attempting to use it on a Production or Analysis/Cleanup project will fail (the error message mentions Production even for Analysis/Cleanup projects). This restriction exists because of the method's destructive potential.
- **Dual permission requirement:** You must have both API Import/Update privileges and Project Design/Setup privileges. Either one alone is not sufficient. (Tokens belonging to REDCap administrators do not need Project Design/Setup.)
- **Metadata validation:** REDCap runs the same checks as a Data Dictionary upload. Errors reject the whole import. **Warnings are not returned:** REDCap auto-corrects the problem silently and imports anyway (see §8). After every import, re-export the metadata ([RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)) and compare it with what you sent.
- **Destructive operation:** The import replaces the whole data dictionary: fields left out of the import are removed from the project. Their data is no longer accessible in forms, reports or exports. REDCap does not purge it, and it can reappear if a field with the same variable name is created again — so removing a field is not a way to remove sensitive data, and avoid reusing old variable names for new fields. Always test on a development project, and export a backup of the current metadata before importing.
- **An empty import wipes the dictionary:** sending an empty array (`[]`) removes every field in the project and returns `0` as a success response. Never send an import built by code that might produce an empty list.
- **JSON keys are matched by position, not by name:** REDCap ignores the key names in each JSON object and reads the values in order into the 18 Data Dictionary columns. A missing or reordered key silently shifts values into the wrong columns. Always send all 18 keys, in the standard order shown in §4 — the order Export Metadata returns them in.
- **Recovery:** REDCap takes an automatic data dictionary snapshot before every API metadata import. Snapshots are listed on **Project Revision History** and can be downloaded and re-uploaded if an import goes wrong.

> **Version caveat (16.0 LTS; checked on 16.0.61):** For tokens belonging to REDCap administrators, branching logic and calculation syntax problems and unsupported functions are only warnings, so the import succeeds with the broken logic in place. On 17.x they are errors for everyone (unless the logic is unchanged from the current dictionary). On 16.0, administrators should re-export after importing and check logic with the Online Designer's syntax checks.

---

## 3. Parameters

| Parameter | Required | Description |
|---|---|---|
| `token` | Required | Your project API token. Requires API Import/Update and Project Design/Setup rights. |
| `content` | Required | Always `'metadata'` for this method. |
| `format` | Optional | Format of the `data` being imported: `'csv'`, `'json'`, or `'xml'` (default). `'odm'` is not supported for this method. CSV is parsed using the CSV delimiter set in the token owner's user profile. |
| `data` | Required | The formatted metadata to import. |
| `returnFormat` | Optional | Format for error messages: `'csv'`, `'json'`, or `'xml'`. Defaults to match `format` if omitted; defaults to `'xml'` if neither is passed. Does not apply when using a background process. |

---

## 4. Data Structure

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

> **Important:** Include all 18 keys in every object, in exactly the order above (the order [RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md) returns). REDCap assigns values by position, so a dropped or reordered key puts values into the wrong columns without any error.

The first field in the import becomes the project's record ID field. REDCap forces it to be a text field and clears any section header on it.

---

## 5. Request Examples

### 5.1 PHP (Full Example)

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

> **Note:** In PHP examples, `CURLOPT_SSL_VERIFYPEER` is shown as `FALSE` for compatibility. Set it to `TRUE` in production. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for why SSL certificate validation matters.

---

## 6. Response

On success the method returns the number of fields in the imported dictionary as a plain number (e.g. `5`), not a JSON object. A response of `0` means the project now has no fields. On failure it returns HTTP 400 with the same error messages a Data Dictionary upload shows, joined one per line: as `{"error": "..."}` for JSON, `ERROR: ...` for CSV, and XML otherwise. Warnings are never returned. Because a success response does not tell you what was auto-corrected, verify every import by re-exporting the metadata and comparing it with what you sent.

**Successful response:**
```
5
```

**Response with errors (JSON):**
```json
{
  "error": "Each row MUST have a form name, but the following cells have a form name missing: B3"
}
```

---

## 7. Common Questions

**Q: What permissions do I need to use this method?**

**A:** You need two separate rights: API Import/Update privileges and Project Design/Setup privileges. Both are required — having only one is not sufficient.

**Q: Can I import a data dictionary from one project to another?**

**A:** Yes. Export the metadata from the source project ([RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)), format it correctly, and import it into the destination project using this method. Be aware that field names and form names must be unique within the destination project.

**Q: What happens if I try to import a field that already exists?**

**A:** The field is updated with the new properties. Field names are unique in a project, so importing an existing field name under a different `form_name` moves that field to the other form; it doesn't create a second field.

**Q: Can I delete fields using this method?**

**A:** Yes — by leaving them out. The import works like a Data Dictionary upload: what you send becomes the project's dictionary, and any field not in it is removed. The removed field's data is no longer accessible, but it is not purged and can reappear if a field with the same variable name is created again. To change a few fields, export the current metadata first ([RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)), edit it, and import the complete set.

**Q: What field types are supported?**

**A:** Valid `field_type` values are `text`, `notes`, `radio`, `dropdown`, `checkbox`, `yesno`, `truefalse`, `calc`, `file`, `slider`, `descriptive` and `sql` (`sql` only for REDCap administrators). Number and date fields are `text` fields with a validation in `text_validation_type_or_show_slider_number`; a matrix is a group of `radio` or `checkbox` fields sharing a `matrix_group_name`. There is no custom field type.

**Q: Can I modify field labels and validation rules using this method?**

**A:** Yes. Most Data Dictionary columns can be modified via import, including field_label, text_validation rules, branching_logic, and field_note. Invalid values in `identifier`, `required_field` or `custom_alignment` are not rejected; REDCap blanks them silently, so re-export to confirm.

---

## 8. Common Mistakes & Gotchas

**Attempting to import on a Production or Analysis/Cleanup project.** This method is restricted to Development status only. If your project has already moved to Production, the API call will fail. You must either use the GUI to make changes in Production (which requires a move-to-production request) or move the project back to Development if your institution allows it.

**Not formatting data as JSON array.** The data must be a JSON-encoded array, even if you're only importing one field. Single objects must be wrapped in an array: `json_encode([field_object])`. A bare object crashes REDCap with a PHP fatal error page (HTTP 400) instead of a validation message.

**Importing only the fields you changed.** Fields missing from the import are deleted, with their data. Always import the complete dictionary.

**Forgetting form_name for each field.** Every field must belong to a form (instrument). The form_name is required, even for the primary identifier record_id field. If you omit it, import fails.

**Using invalid field types.** Field types must match REDCap's predefined types (text, radio, dropdown, etc.). Typos in field_type cause validation errors. Always validate field_type against the REDCap documentation.

**Invalid branching logic or calculations.** The import fails if logic has a syntax error, uses an unsupported function, or references a variable that is not in the import. REDCap does not check for circular dependencies between calculations, so test those yourself.

**Matrix and slider field misconfigurations.** Matrix fields require matrix_group_name; slider fields require specific validation settings. Incomplete configuration of these field types causes errors.

**Relying on the response to catch mistakes.** Warnings are auto-corrected silently. Examples: variable names are lowercased and invalid characters stripped, invalid `identifier`, `required_field` or `custom_alignment` values are blanked, and choice codes may be adjusted. Changing which field is first (the record ID field) while the project has records is also only a warning, so it goes through without notice. Re-export after every import and compare.

**Splitting an instrument's fields.** All fields of one instrument must be together in a single block of rows. Fields of one `form_name` separated by another instrument's fields cause an error.

**Fields and instruments that can't be changed.** Fields used by randomization can't be removed, and PROMIS/CAT instruments can't be modified through this method.

**Adding or removing instruments in longitudinal projects.** New instruments are not designated to any event; designate them afterwards (Define My Events, or the Import Instrument-Event Mappings API). Removing or renaming an instrument permanently loses its event designations, repeating settings, locking and e-signature records and instrument-level user rights, even though the field data is only hidden.

**Not validating data before import.** Always test metadata imports on a development project first. Importing invalid metadata can corrupt your project structure. If it does, download the automatic snapshot from **Project Revision History** and re-import it.

---

## 9. Related Articles

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (overview; authentication, tokens, playground)
- [RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md) (read the data dictionary)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (the GUI alternative to API-based metadata import)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (format specification for the CSV being imported)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (column reference for valid values in each field)
