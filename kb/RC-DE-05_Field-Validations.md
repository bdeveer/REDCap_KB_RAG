RC-DE-05

**Data Entry — Field Validations**

| **Article ID** | RC-DE-05 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; data entry users |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-08 — Control Center: Home Page, Templates & Project Defaults; RC-DE-06 — Bio-Medical Ontologies; RC-DE-02 — Basic Data Entry; RC-FD-01 — Form Design Overview |

---

# 1. Overview

This article explains how field validations work in REDCap from a data entry perspective. Validations are predefined checks applied to text box variables that enforce a required format or value range. When you enter a value that does not pass a validation, REDCap displays a popup message before allowing you to continue. Understanding the validation categories — dates and times, numbers, contact information, specialty, and custom — helps you enter data correctly and interpret validation error messages quickly.

---

# 2. Key Concepts & Definitions

**Validation**

A predefined rule attached to a text box variable by the instrument designer that checks whether entered data matches a required format or falls within an allowed value range. Validations are configured at the project design stage; data entry users encounter them but cannot modify them.

**Validation Error Popup**

A dialog box that appears when you attempt to save or move past a field containing a value that does not pass the attached validation. The popup names the validation type and typically describes the expected format.

**Field Note**

A short snippet of text displayed beneath a text box that provides a hint about the expected format for that variable. Field notes are set by the instrument designer and are visible at all times during data entry.

**Placeholder**

Text displayed inside a text box before any value has been entered. Placeholders serve the same purpose as field notes but disappear the moment you begin typing. A placeholder is not a prefilled value.

**Minimum / Maximum**

An optional constraint that can be added to date/time and number validations. By default, min/max constraints are **soft**: REDCap displays a warning popup if the entered value falls outside the defined range, but the user can acknowledge it and save the value anyway (to allow for legitimate outliers). The instrument designer can override this by adding the action tag **@FORCE-MINMAX** to the field, which makes the constraint **hard** — REDCap will not accept any value outside the defined range. Minimums and maximums can be set as hard values (fixed numbers or dates) or dynamic values (derived from another field's answer).

**Prefilled Value**

A value that REDCap (or an advanced feature such as action tags or piping) automatically inserts into a text box. Depending on how the instrument is designed, you may or may not be able to edit a prefilled value.

---

# 3. Validation Categories

### 3.1 Date and Time Validations

REDCap provides a large number of date, time, and date-time validation variants. The specific format in use for any given field is determined by the instrument designer; as a data entry user, you do not choose the format. There are four ways to enter a value into a date or time field:

**Manual entry.** Type the date or time directly using your keyboard. Use exactly the format shown next to or below the field — REDCap will reject entries in the wrong format.

**Date picker.** Click the calendar icon next to the field to open a calendar popup. For validations that include a time component, the popup also includes a time selector. Using the date picker guarantees the correct format because REDCap formats the value for you automatically.

**Today / Now button.** A button labeled "Today" (or "Now" for date-time validations) appears next to the date picker. Clicking it fills the field with the current date and time in your local timezone. This is the fastest way to record the current moment.

**Prefilled value.** Certain advanced project features (e.g., action tags, calculated fields, or piping) can automatically populate a date or time field when you open the instrument. Whether you can modify a prefilled value depends on how the instrument is configured.

> **Note:** Date and time validations can also include a minimum, a maximum, or both. These constraints can be hard dates (e.g., no date before January 1, 2000) or dynamic dates derived from another field's value (e.g., a visit date cannot be before the participant's date of birth). If you enter a value outside these bounds, a popup error will appear.

### 3.2 Number Validations

Number validations check that the entered value is numeric. The two most common variants are:

| **Validation** | **What It Checks** |
|---|---|
| Number | The entry is in a numeric format (integers and decimals are both accepted) |
| Integer | The entry is a whole number — no decimal places allowed |

Use the integer validation context as a signal from the instrument designer that fractional values are not meaningful for that variable (e.g., number of pregnancies, number of visits).

Number validations can also include a minimum, maximum, or both. As with date validations, these can be hard values or dynamic values derived from another field. If your entry falls outside the allowed range, a popup error will appear.

### 3.3 Contact Information Validations

REDCap provides validations for common contact information formats:

- **Email** — checks that the entry follows a standard email address format (e.g., name@domain.com)
- **Phone number** — checks that the entry matches a phone number format; multiple country-specific variants exist
- **Zip code** — checks that the entry matches a postal code format; country-specific variants exist

> **Important:** Contact information validations check format only — they do not verify that the email address, phone number, or zip code actually exists or belongs to the participant. An entry like `fake@example.com` will pass email validation.

If you trigger a contact validation error, the popup will name the specific validation in use, which is usually a reliable hint about the expected format (e.g., "Phone (North America)").

### 3.4 Specialty Validations

Specialty validations cover formats that do not fit the categories above. Examples include:

- US Social Security Number
- Letters only (no digits or special characters)
- Medical Record Number (MRN) — multiple format variants exist

If you trigger a specialty validation error, the popup names the validation. The name is usually descriptive enough to infer the expected format. If the instrument designer has added a field note or placeholder, check those first for guidance.

### 3.5 Custom Validations

In some REDCap installations, the system administrator has added validations specific to that institution. These custom validations behave the same as specialty validations — they display the validation name in the error popup — but they are not part of the standard REDCap distribution. Examples include institution-specific MRN formats, country-specific ID number formats, or locally defined code formats.

> **Institution-specific:** Some REDCap installations include custom validation types beyond the standard set. Contact your REDCap administrator to learn whether custom validations are available at your institution and what formats they expect.

---

# 4. Field Notes and Placeholders

Instrument designers frequently pair validations with field notes or placeholders to communicate the expected format to data entry users before an error occurs.

**Field notes** appear as small text beneath the input field and are always visible. **Placeholders** appear as greyed-out text inside the input field and disappear when you begin typing.

Examples of field notes and placeholders you may encounter:

- `(XXX) XXX-XXXX` — for a US phone number field
- `mg or milligrams` — for a medication dose field
- `Min: 0, Max: 120` — for an age in years field

When a field note or placeholder is present, read it before entering data. It will tell you whether a specific unit, format, or range is expected.

---

# 5. Common Questions

**Q: A validation error popup appeared — what should I do?**

**A:** Read the popup message. It will name the validation type and usually describe the required format. Check any field note or placeholder beneath or inside the field for additional guidance. Correct your entry to match the required format, then save again. If you are unsure of the correct value, leave the field blank and add a field comment explaining the issue (see RC-DE-08 — Field Comment Log).

**Q: I entered a valid-looking date but REDCap rejected it — why?**

**A:** The most common cause is entering the date in the wrong format. REDCap supports multiple date formats (e.g., MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD), and the required format is set by the instrument designer. Check the field note next to the input for the expected format, or use the date picker to avoid format errors entirely.

**Q: Can a minimum or maximum on a date field reference another field's value?**

**A:** Yes. Dynamic minimums and maximums derive their bound from the value stored in another field. For example, a visit date field might have a dynamic minimum set to the participant's date of birth — meaning no visit date before the date of birth will be accepted. If a dynamic bound is in use and the referenced field is blank, REDCap's behavior depends on how the instrument was designed.

**Q: The field I need to fill in has a number validation but I need to enter text explaining an unusual value. What should I do?**

**A:** You cannot override a validation by entering text into a validated text box — REDCap will reject the entry. Instead, leave the field blank (or enter the closest valid numeric value) and use the field comment log to document your explanation. See RC-DE-08 — Field Comment Log.

**Q: Why does the phone number validation reject a number that looks correct to me?**

**A:** REDCap has multiple phone number validation variants tailored to different countries or formats. A number that is valid for one variant (e.g., a US format) may be invalid under a different variant (e.g., a European format). The validation name shown in the error popup — such as "Phone (North America)" — tells you which format is expected.

**Q: What is the difference between a placeholder and a prefilled value?**

**A:** A placeholder is display text only — it disappears the moment you click into the field and begin typing, and it is never saved. A prefilled value is an actual value inserted into the field by REDCap (via action tags, piping, or a calculated field). Prefilled values persist and may or may not be editable depending on the instrument design.

**Q: I entered a value outside the min/max range and REDCap still let me save it. Is that a bug?**

**A:** No — this is the default, intended behavior. Min/max range constraints are soft validations. REDCap shows a warning popup to prompt you to double-check the value, but it allows you to proceed if you confirm the value is correct. This is by design, to accommodate legitimate outliers. If the instrument was configured with @FORCE-MINMAX, REDCap will instead hard-reject any value outside the range. If you're unsure whether a borderline value is acceptable, contact the instrument designer or study coordinator.

---

# 6. Common Mistakes & Gotchas

**Entering the date in the wrong format.** REDCap supports many date formats, and each field uses exactly one. If you type a date without checking the expected format first, you will trigger a validation error even if the date itself is correct. Use the date picker when in doubt — it formats the value for you automatically.

**Assuming contact information validations verify real-world validity.** Email, phone, and zip code validations check format only. A syntactically correct but fictional or wrong contact address will pass without error. Data quality review is a separate process.

**Trying to type text into a number or date field to explain an unusual value.** Validations cannot be bypassed by entering free text. If you need to explain or flag an unusual data point, leave the validated field with a valid value (or blank) and use the field comment log (RC-DE-08).

**Missing a dynamic minimum or maximum because the referenced field is blank.** If a validation's minimum or maximum is derived from another field and that field has not yet been filled in, the constraint may not apply — which means an otherwise invalid value could be accepted temporarily. Always fill prerequisite fields before dependent fields.

**Assuming a value outside the min/max range was accepted in error.** Min/max constraints are soft by default — REDCap warns you but allows the value if you confirm it. If a field has been configured with @FORCE-MINMAX, the behavior changes: REDCap will not accept values outside the range at all. If you are unsure whether an out-of-range value you entered was appropriate, add a field comment explaining the data point (see RC-DE-08).

---

# 7. Administrator Configuration

The set of validation types available in the Online Designer is controlled by a REDCap administrator in the Control Center under System Configuration → Home Page, Templates & Project Defaults (see **RC-CC-08**, "Field Validation Types" section). Administrators can enable or disable any built-in validation type and can register custom institution-specific validation types using JavaScript-based pattern matching or range checking.

A disabled validation type does not appear in the **Validation** dropdown in the Online Designer or the Add/Edit Field dialog. However, existing fields that already use a disabled type continue to function normally — the disable only prevents new fields from selecting that type via the UI. Disabled types can still be applied by entering them directly in a Data Dictionary CSV upload.

If a validation type you expect to see is missing from the Validation dropdown, contact your REDCap administrator to check whether it has been disabled, or whether a custom validation has been created to replace it.

> **See also:** RC-CC-08 — Control Center: Home Page, Templates & Project Defaults

---

# 8. Related Articles

- RC-CC-08 — Control Center: Home Page, Templates & Project Defaults (system-level management of available validation types)
- RC-DE-02 — Basic Data Entry (foundational data entry skills)
- RC-DE-06 — Bio-Medical Ontologies (a distinct lookup-based field type often paired with validated fields)
- RC-DE-08 — Field Comment Log (how to flag problematic validated fields without altering the dataset)
- RC-FD-01 — Form Design Overview (how instrument designers configure field types and validations)
