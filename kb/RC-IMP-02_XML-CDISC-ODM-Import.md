

**XML / CDISC ODM Import: Format Reference and Workflow**

| **Article ID** | [RC-IMP-02 — XML / CDISC ODM Import: Format Reference and Workflow](RC-IMP-02_XML-CDISC-ODM-Import.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types; requires Data Entry rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-05-13 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md); [RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md); [RC-API-03 — Import Records API](RC-API-03_Import-Records.md); [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) |
| **Synonyms** | how to import an xml file into redcap; cdisc odm import workflow; transfer data from another redcap installation; import a project xml backup with data; what xml format does redcap accept; odm import handling of existing records; import clinical data from a cdisc compliant system; xml data import reference |

---

## 1. Overview

REDCap's Data Import Tool supports two import formats: CSV and CDISC ODM XML. While CSV is the standard format for most bulk imports, the ODM XML pathway serves a distinct set of use cases — chiefly transferring data from another REDCap installation or from a third-party system that produces CDISC-compliant output. This article covers the ODM import pathway in full: what the format is, when to use it, what files are accepted, how the import process works step by step, and how REDCap handles records that already exist in the project. The brief procedural summary in [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (§8.4) is the entry point; this article is the complete reference.

---

## 2. Key Concepts & Definitions

**CDISC ODM (Operational Data Model)**

An open, vendor-neutral XML standard maintained by the Clinical Data Interchange Standards Consortium (CDISC) for the interchange and archival of clinical and research data. ODM encodes both data and metadata — it can describe field definitions, choice lists, and other project structure alongside the actual participant values. REDCap uses ODM version 1.3.X for its XML export and import formats.

**OID (Object Identifier)**

A unique string used within ODM files to identify elements such as studies, forms, items (fields), and item groups. In a REDCap-generated ODM file, OIDs map directly to REDCap variable names. REDCap uses OIDs during import to match incoming data values to the correct variables in the target project.

**REDCap-generated ODM file**

An ODM XML file produced by REDCap's own export tools — either from the Data Exports, Reports & Stats module or via the API. These files are pre-formatted to REDCap's internal ODM dialect and are the most reliable input for re-import. The OIDs in the file correspond directly to the variable names of the project that generated them.

**Third-party ODM file**

An ODM XML file produced by an external system (e.g., another EDC platform, a clinical data management system). REDCap can import these files provided they conform to ODM version 1.3.X and their OIDs match the variable names defined in the target REDCap project. Structural differences in ODM dialect between vendors are a common source of import errors.

**Data Import Tool**

The built-in REDCap application for bulk importing participant record data. Accessible from the project's left-hand Applications menu. Offers both a CSV tab and a CDISC ODM (XML) tab. The ODM tab is this article's subject.

**Overwrite Data with Blank Values**

An import setting that controls whether empty elements in the ODM file erase existing stored values. When set to Yes, a missing or empty data point in the file overwrites the stored value with nothing. The default is No: blank elements are ignored and existing data is preserved.

**Additive import**

REDCap's ODM import is additive by default: incoming records are merged with existing records, not replaced wholesale. If a record ID already exists, only the fields present in the import file are updated (subject to the Overwrite setting). Records not referenced in the file are untouched.

---

## 3. ODM Import vs. CSV Import: Choosing the Right Format

Use this section to decide which import format fits your situation.

### 3.1 When ODM Import is the Right Choice

| Scenario | Why ODM |
|---|---|
| You exported data from a REDCap project (same or different installation) and want to re-import it | REDCap ODM exports are already formatted for re-import; no spreadsheet editing needed |
| You are transferring data from a third-party EDC or data management system that produces CDISC ODM output | ODM is the interoperability standard; if the external system supports it, no conversion is required |
| You need to carry both data values and their associated metadata labels in a single file for archival purposes | ODM includes field definitions alongside data; CSV carries data only |
| Your data includes special characters, rich text, or multilingual content that may not survive CSV encoding | XML encoding handles character sets more robustly than CSV |

### 3.2 When CSV Import is the Better Choice

| Scenario | Why CSV |
|---|---|
| You are building an import file manually or editing exported data in a spreadsheet | CSV is editable in Excel, Google Sheets, or any text editor; ODM XML is not spreadsheet-friendly |
| You are importing a subset of fields or correcting specific values in existing records | CSV partial imports are straightforward; ODM imports are harder to scope down to individual fields |
| You want to run a background import for a large file | Background processing is only available for CSV; ODM imports run in real time only |
| Your source system produces CSV output | No need to convert if CSV is already available and correctly formatted |

> **Note:** CSV import is the recommended format for the majority of REDCap use cases. ODM import is a specialized pathway — reach for it when you have an ODM file in hand, not as a general alternative to CSV.

---

## 4. File Requirements

### 4.1 ODM Version

REDCap accepts only **ODM version 1.3.X**. Files produced by ODM 1.2 or earlier, or by ODM 2.0, are not guaranteed to import correctly and may be rejected outright. The ODM version is declared in the root element of the XML file:

```xml
<ODM ODMVersion="1.3.2" ...>
```

Check this attribute before attempting an import if you are working with a file from an external system.

### 4.2 REDCap-Generated ODM Files

The most reliable ODM source for re-import into REDCap is a file produced by REDCap itself. You can obtain one in two ways:

**From the Data Exports module:**

| 1 | Navigate to **Applications → Data Exports, Reports & Stats**. |
|---|---|
| 2 | Select the report or record set you want to export. |
| 3 | Choose **CDISC ODM (XML)** as the export format. |
| 4 | Click **Export Data** and download the file. |

See [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md) for full coverage of export format options.

**From the API:**

The Export Project XML endpoint ([RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md)) returns a full project ODM export programmatically. The Export Records endpoint ([RC-API-02 — Export Records API](RC-API-02_Export-Records.md)) also supports an `xml` format type that returns record data in ODM structure. API usage requires a token and developer familiarity — see [RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md).

### 4.3 Third-Party ODM Files

REDCap can import ODM files from external systems provided two conditions are met:

1. **ODM version 1.3.X** — see §4.1.
2. **OID–variable name alignment** — The OID values used in the external file's `<ItemData>` elements must match the variable names defined in the target REDCap project. REDCap uses OIDs as the mapping key; if OIDs in the file do not correspond to any variable in the project, those data points are skipped or produce an error.

> **Important:** Different EDC vendors implement ODM with slightly different conventions (namespace declarations, OID formats, attribute ordering). Even a technically valid ODM 1.3 file from another vendor may require manual adjustment before REDCap accepts it. If you encounter import errors with a third-party file, compare its structure against a REDCap-generated ODM export from the same project to identify discrepancies.

### 4.4 What ODM Import Updates — and What It Does Not

The ODM import in the Data Import Tool updates **participant record data only**. It does not modify:

- Instrument definitions (field types, labels, validation rules)
- Survey settings
- Longitudinal structure (arms, events, instrument–event mappings)
- User rights or user accounts
- Alerts, notifications, or other project configuration

If you need to restore or migrate a full project including its metadata, use the project XML backup/restore feature described in [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (§7) instead.

---

## 5. REDCap ODM XML Format Reference

This section documents the structure and encoding of REDCap-generated ODM XML files. Use it to understand what a valid file looks like, diagnose import errors, or prepare a third-party ODM file for import into REDCap.

### 5.1 Document Structure Overview

A REDCap ODM XML file has two top-level blocks inside the root `<ODM>` element:

```
<ODM>                          ← Root element (file-level metadata)
  <Study>                      ← Project structure (metadata)
    <GlobalVariables>          ← Project settings
    <MetaDataVersion>          ← Instrument and field definitions
      <Protocol>               ← Arms, events, instrument–event mappings
      <FormDef>                ← One per instrument
      <ItemGroupDef>           ← One per section header / field group
      <ItemDef>                ← One per field (or one per checkbox choice)
      <CodeList>               ← Choice options for radio/dropdown/checkbox
  <ClinicalData>               ← Participant record data
    <SubjectData>              ← One per record
      <StudyEventData>         ← One per event the record has data in
        <FormData>             ← One per instrument instance
          <ItemGroupData>      ← One per field group
            <ItemData>         ← One data value
```

### 5.2 Root ODM Element Attributes

The `<ODM>` element carries file-level metadata. Key attributes in a REDCap export:

| Attribute | Example value | Meaning |
|---|---|---|
| `ODMVersion` | `1.3.1` | ODM standard version. REDCap imports require 1.3.X. |
| `FileType` | `Snapshot` | Always `Snapshot` for REDCap exports (a point-in-time capture). |
| `Description` | `Test Bas` | The project title. |
| `AsOfDateTime` | `2026-05-13T23:52:03` | Timestamp of the export (ISO 8601). |
| `CreationDateTime` | `2026-05-13T23:52:03` | Same as `AsOfDateTime` in REDCap exports. |
| `SourceSystem` | `REDCap` | Always `REDCap` for REDCap exports. |
| `SourceSystemVersion` | `16.0.25` | The REDCap version that generated the file. |

The `xmlns:redcap="https://projectredcap.org"` namespace declaration enables the `redcap:` prefixed extensions that carry REDCap-specific metadata throughout the file.

### 5.3 MetaDataVersion — Field Definitions

Each field in the project appears as an `<ItemDef>` element. The attributes on `<ItemDef>` encode the field's full definition:

| Attribute | Example | Meaning |
|---|---|---|
| `OID` | `screen_date` | The field's variable name. Used as the mapping key during import. For checkbox fields, format is `fieldname___code` (see §5.5). |
| `DataType` | `text`, `date`, `float`, `integer`, `boolean` | ODM data type. `boolean` is used for checkbox choices. |
| `Length` | `999` | Maximum character length. Usually 999 for text fields. |
| `redcap:Variable` | `screen_date` | The REDCap variable name. Matches `OID` for non-checkbox fields; for checkboxes, points to the parent field name. |
| `redcap:FieldType` | `text`, `radio`, `select`, `checkbox`, `yesno`, `calc`, `descriptive`, `textarea` | The REDCap field type. |
| `redcap:TextValidationType` | `date_mdy`, `float`, `int`, `email`, `phone` | Validation applied to text fields. Only present when validation is set. |
| `redcap:SectionHeader` | `Eligibility Screening` | The section header label displayed above this field. |
| `redcap:RequiredField` | `y` | Present when the field is marked required. |
| `redcap:BranchingLogic` | `[screen_sex_female] = '1'` | Branching logic expression (HTML-entity-encoded in the XML). |
| `redcap:Calculation` | `datediff([demo_dob],'today','y')` | Calculation formula for `calc` field type. |
| `redcap:Identifier` | `y` | Present when the field is flagged as a participant identifier. |
| `redcap:FieldNote` | `Auto-calculated from date of birth` | The field note displayed below the field. |
| `redcap:FieldAnnotation` | `@TODAY` | Action tag(s) applied to the field. |
| `redcap:CustomAlignment` | `LH`, `LV` | Choice alignment: LH = left-horizontal, LV = left-vertical. |
| `redcap:QuestionNumber` | `1` | Display question number (if enabled in project settings). |

**Validation range checks** appear as child `<RangeCheck>` elements with `Comparator` (GE, LE, GT, LT) and `SoftHard` (Soft = warning, Hard = error) attributes.

### 5.4 ClinicalData Structure — How Records Are Encoded

Participant data is nested four levels deep:

```
<ClinicalData StudyOID="Project.TestBas" MetaDataVersionOID="Metadata.TestBas_...">
  <SubjectData SubjectKey="1" redcap:RecordIdField="record_id">
    <StudyEventData StudyEventOID="Event.baseline_arm_1"
                    StudyEventRepeatKey="1"
                    redcap:UniqueEventName="baseline_arm_1">
      <FormData FormOID="Form.demographics" FormRepeatKey="1">
        <ItemGroupData ItemGroupOID="demographics.demo_dob" ItemGroupRepeatKey="1">
          <ItemData ItemOID="demo_dob" Value="2026-05-01"/>
        </ItemGroupData>
      </FormData>
    </StudyEventData>
  </SubjectData>
</ClinicalData>
```

| Element / Attribute | Meaning |
|---|---|
| `SubjectData SubjectKey` | The record's Record ID value. |
| `redcap:RecordIdField` | The variable name used as the Record ID in this project (e.g., `record_id`). |
| `StudyEventData StudyEventOID` | The event, in the format `Event.uniqueeventname`. |
| `redcap:UniqueEventName` | The unique event name (e.g., `baseline_arm_1`). Must match an event defined in the target project. |
| `StudyEventRepeatKey` | Always `1` for standard (non-repeating) events. |
| `FormData FormOID` | The instrument, in the format `Form.instrument_name`. |
| `FormData FormRepeatKey` | Instance number for repeating instruments (`1`, `2`, `3`…). See §5.6. |
| `ItemData ItemOID` | The field's variable name (or `fieldname___code` for checkboxes). |
| `ItemData Value` | The stored value. Dates are in `YYYY-MM-DD` format. Choice fields use the raw coded value (not the label). |

### 5.5 Checkbox Field Encoding

Checkbox fields receive one `<ItemDef>` per choice, and one `<ItemData>` per choice in the data. The OID follows the pattern `fieldname___code` (three underscores):

```xml
<!-- MetaDataVersion: each checkbox choice is a separate ItemDef -->
<ItemDef OID="demo_race___1" DataType="boolean" redcap:Variable="demo_race" redcap:FieldType="checkbox">
  <Question><TranslatedText>Race (select all that apply)</TranslatedText></Question>
</ItemDef>
<ItemDef OID="demo_race___2" DataType="boolean" redcap:Variable="demo_race" redcap:FieldType="checkbox">
  ...
</ItemDef>

<!-- ClinicalData: each choice is a separate ItemData element -->
<ItemData ItemOID="demo_race___1" Value="1"/>  <!-- choice 1 is checked -->
<ItemData ItemOID="demo_race___2" Value="0"/>  <!-- choice 2 is unchecked -->
```

- `DataType="boolean"` is always used for checkbox choices.
- Value is `"1"` (checked) or `"0"` (unchecked).
- The `redcap:Variable` attribute always points to the parent field name (`demo_race`), not the choice-specific OID.
- The three-underscore separator (`___`) distinguishes checkbox OIDs from regular field OIDs and from instrument-complete status fields.

> **Note:** This OID naming convention matches the CSV export convention for checkboxes (`fieldname___code`), so if you are familiar with CSV imports, the pattern is the same.

### 5.6 Repeating Instrument Encoding

For repeating instruments, each instance appears as a separate `<FormData>` element with an incrementing `FormRepeatKey`:

```xml
<StudyEventData StudyEventOID="Event.baseline_arm_1" redcap:UniqueEventName="baseline_arm_1">

  <!-- Instance 1 of the medication_list repeating instrument -->
  <FormData FormOID="Form.medication_list" FormRepeatKey="1">
    <ItemGroupData ItemGroupOID="medication_list.med_name" ItemGroupRepeatKey="1">
      <ItemData ItemOID="med_name" Value="Lisinopril"/>
    </ItemGroupData>
  </FormData>

  <!-- Instance 2 of the same instrument -->
  <FormData FormOID="Form.medication_list" FormRepeatKey="2">
    <ItemGroupData ItemGroupOID="medication_list.med_name" ItemGroupRepeatKey="1">
      <ItemData ItemOID="med_name" Value="Metformin"/>
    </ItemGroupData>
  </FormData>

</StudyEventData>
```

`FormRepeatKey` is the ODM equivalent of `redcap_repeat_instance` in CSV imports. The numbering starts at `1` and increments per instance. When importing, REDCap matches instances by their `FormRepeatKey` value — so importing a file with `FormRepeatKey="2"` will update instance 2, not append a new one.

### 5.7 GlobalVariables — Project Settings

The `<GlobalVariables>` block stores project-level settings using `redcap:` namespaced elements. These settings are included in backup exports but are **not applied during a data-only ODM import via the Data Import Tool** — they only take effect during a full project restore (Create New Project → Upload XML). Key settings encoded here include:

| redcap: element | Meaning |
|---|---|
| `redcap:SurveysEnabled` | Whether surveys are enabled (0/1) |
| `redcap:SchedulingEnabled` | Whether the scheduling module is active |
| `redcap:RandomizationEnabled` | Whether the randomization module is active |
| `redcap:RecordAutonumberingEnabled` | Whether auto-numbering of Record IDs is active |
| `redcap:DataResolutionWorkflowEnabled` | Whether the data resolution (query) module is active |
| `redcap:RepeatingInstrumentsAndEvents` | Defines which instruments and events repeat, and any custom repeat labels |
| `redcap:MissingDataCodes` | Project-level missing data codes (e.g., `NI=Not indicated`) |

---

## 6. ODM Import Process

### 6.1 Navigating to the ODM Import Tab

| 1 | From the project left-hand menu, navigate to **Applications → Data Import Tool**. |
|---|---|
| 2 | At the top of the Data Import Tool page, locate the tab row. Click the **CDISC ODM (XML)** tab. (The CSV tab is selected by default.) |

> **Note:** If you do not see the Data Import Tool in the Applications menu, your user account may not have Data Entry rights for this project. Contact your project administrator.

### 6.2 Import Settings

The ODM import tab offers a single configurable setting before file selection:

| **Setting** | **Options** | **Notes** |
|---|---|---|
| Overwrite data with blank values | No (default) / Yes | When No, blank or missing elements in the ODM file are ignored — existing stored values are preserved. When Yes, blank elements overwrite existing values with nothing. Leave at No unless you deliberately intend to clear data. |

The delimiter and date format settings present on the CSV tab do not appear on the ODM tab — these parameters are encoded in the XML file itself and do not require separate configuration.

### 6.3 Step-by-Step Import Procedure

| 1 | On the CDISC ODM (XML) tab, confirm the **Overwrite data with blank values** setting. |
|---|---|
| 2 | Click **Browse** (or **Choose File**) and select the ODM XML file from your computer. You can also drag and drop the file onto the Choose File button. |
| 3 | Click **Upload File**. REDCap reads the file and validates it against the project's variable definitions. |
| 4 | REDCap displays a preview of the data to be imported, along with any errors or warnings found during validation. **The data has not been saved yet.** |
| 5 | Review the preview carefully. If errors are listed, click **Cancel**, correct the file, and upload again. |
| 6 | If the preview looks correct, scroll down and click **Import Data** to commit the import. |

> **Important:** Clicking "Upload File" stages a preview only. The data is not saved to the project until you click "Import Data" at the bottom of the results screen. This is the same two-step pattern as the CSV import — a common point of confusion.

> **Note:** The ODM import runs in real time in the browser. There is no background processing option. For very large ODM files this means the browser must remain open and active until the import completes.

### 6.4 Reviewing the Import Preview

The preview screen shows the records and values REDCap detected in the file. Pay attention to:

- **Error count** — any rows or elements REDCap could not process appear with an explanation. Common errors include unrecognized OIDs (variable name mismatch), invalid coded values, and malformed XML.
- **Record count** — confirm the number of records detected matches what you expect from the source file.
- **Existing vs. new records** — REDCap distinguishes between records being updated and records being created for the first time.

---

## 7. How REDCap Handles Existing Records During ODM Import

### 7.1 Additive Merge Behavior

ODM import merges incoming data with existing records — it does not replace them. If a record with the same Record ID already exists in the project:

- Fields present in the import file are updated with the incoming values.
- Fields not referenced in the import file are left unchanged.
- The existing record is not deleted or overwritten wholesale.

If a record ID in the import file does not exist in the project, REDCap creates a new record.

### 7.2 Effect of "Overwrite Data with Blank Values"

The Overwrite setting modifies what happens when the import file contains a blank or missing value for a field that already has data in REDCap:

| Setting | Existing value | Incoming value | Result |
|---|---|---|---|
| No (default) | Stored | Blank/missing | Existing value **preserved** |
| Yes | Stored | Blank/missing | Existing value **erased** |
| Either | Any | Non-blank | Existing value **replaced** with incoming value |

> **Important:** "Overwrite data with blank values = Yes" can silently erase participant data if the import file is incomplete. Only enable this setting when blanking existing values is your explicit intent.

### 7.3 Record ID Matching

REDCap matches incoming records to existing records using the Record ID field. The Record ID in the ODM file's subject key must correspond to the Record ID values in the target project. If the Record ID format in the file differs from the target project (e.g., leading zeros, different prefix), records will be created as new rather than updating existing ones.

### 7.4 Longitudinal Projects

For longitudinal projects, the ODM file encodes event context through the study event reference structure in the XML. REDCap maps data to the correct event using this structure — you do not need to add a separate event name column as you would in a CSV import. However, the event names in the file must correspond to events defined in the target project; mismatches cause those data points to be skipped.

---

## 8. Common Questions

**Q: When should I use ODM import instead of CSV import?**

**A:** Use ODM import when you already have an ODM XML file — typically a REDCap export from another installation or output from a third-party EDC system. If you are building your import file from scratch, editing data in a spreadsheet, or doing a partial field update, CSV import is simpler and more practical.

**Q: Can I import an ODM file from a different REDCap project or installation?**

**A:** Yes, provided the target project's variable names match the OIDs in the file. REDCap ODM exports use variable names as OIDs, so importing into a project with the same instrument and variable structure works cleanly. Importing into a project with different variable names will result in unrecognized OID errors for the mismatched fields.

**Q: Does ODM import support background processing like the CSV import does?**

**A:** No. ODM imports run in real time in the browser only. The browser must stay open and active until the import completes. For very large datasets, consider using the API Import Records endpoint with XML format instead, which does not have this limitation.

**Q: Will importing an ODM file delete records that are in the project but not in the file?**

**A:** No. The ODM import is additive — it only affects records that appear in the import file. Records in the project that are not referenced in the file are completely untouched.

**Q: What happens if my ODM file has a variable (OID) that doesn't exist in this project?**

**A:** REDCap will flag it as an unrecognized OID error in the import preview. The affected data points are not imported. All other data in the file that maps to valid variables will be processed normally. You must fix the OID mismatch in the file — either by correcting the OID to match the variable name in the target project, or by removing the non-matching elements — before those values can be imported.

**Q: Can I use ODM import to restore a full project backup, including instruments and settings?**

**A:** No. The Data Import Tool's ODM import updates participant record data only — it does not modify project structure, survey settings, or user rights. To restore a full project from a backup XML file (which includes metadata and data), use the project creation screen: Create New Project → Upload a REDCap project XML file. See [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) §7 for the full backup/restore workflow.

**Q: My ODM file came from another vendor's EDC system and keeps failing. What should I check?**

**A:** Start by verifying the ODM version attribute in the root element — it must be 1.3.X. Then compare the OID values in your file against the variable names in the target REDCap project; they must match exactly. Also check for namespace declarations or XML attributes that REDCap may not recognize. Exporting a small set of records from the target project in ODM format and comparing that file's structure to your third-party file is usually the fastest way to identify the discrepancy.

---

## 9. Common Mistakes & Gotchas

**Clicking "Upload File" but not "Import Data."** The upload step stages a preview only — no data is saved until you scroll down and click "Import Data." If you close the browser tab or navigate away after uploading, nothing is imported. This two-step pattern is the same as CSV import and is the most common cause of "the data didn't appear" support requests.

**OID mismatch between source and target projects.** If the ODM file was exported from a project with different variable names than the target project, REDCap will not be able to match the incoming data to any field. The preview will show unrecognized OID errors. The fix is to align the variable names between projects before re-exporting, or to edit the OIDs in the XML file manually — though the latter is error-prone and not recommended for non-technical users.

**Using ODM import to try to restore project structure.** The Data Import Tool's ODM tab only processes participant data. Attempting to import a full project backup XML (which contains instrument definitions, events, and survey settings) through this tab will either fail or import only the data portion while silently ignoring the metadata. Use the Create New Project → Upload XML pathway for full project restores.

**Enabling "Overwrite data with blank values" on a partial file.** If your ODM file contains only a subset of fields for each record, enabling Overwrite will erase all existing values for fields not present in the file. Only enable this setting when the file is comprehensive and you intentionally want to clear fields not included in the import.

**Importing from a different ODM version.** REDCap requires ODM 1.3.X. Files produced by older systems (ODM 1.2) or newer ones (ODM 2.0) may not validate correctly. Check the `ODMVersion` attribute in the file's root element before importing.

**Browser timeout on large files.** Because ODM import runs in real time with no background option, very large files can cause the browser to time out before the import completes. If you need to import a large dataset in ODM format, use the API Import Records endpoint ([RC-API-03 — Import Records API](RC-API-03_Import-Records.md)) with `format=xml` instead — it does not have this constraint.

---

### API Access

> **Note:** The following REDCap API methods provide programmatic access to import and export functionality related to ODM XML. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-03 — Import Records API](RC-API-03_Import-Records.md)** — supports `format=xml` (CDISC ODM) for programmatic record import; runs asynchronously and is not subject to browser timeout limitations
- **[RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md)** — exports the full project (metadata + data) as ODM XML; useful for generating files to re-import into another installation

---

## 10. Related Articles

- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (prerequisite; §8.4 contains the introductory ODM import summary this article expands)
- [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md) (covers how to produce a REDCap ODM export file for re-import)
- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (CSV alternative to ODM for most import use cases)
- [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md)(step-by-step guide to CSV record import)
- [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) (programmatic record import; supports XML/ODM format; no browser timeout limitation)
- [RC-API-36 — Export Project XML API](RC-API-36_Export-Project-XML.md) (API method for obtaining a full project ODM export)
- [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md)(full project migration workflow using XML backup/restore; distinct from data-only ODM import)
