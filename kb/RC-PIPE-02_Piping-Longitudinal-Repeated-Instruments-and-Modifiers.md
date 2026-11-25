

**Piping — Longitudinal, Repeated Instruments & Modifiers**

| **Article ID** | [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) |
|---|---|
| **Domain** | Piping |
| **Applies To** | Longitudinal projects; projects with repeated instruments or repeated events; all projects using piping modifiers |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — piping syntax and modifiers checked against source code; pages not re-captured |
| **Prerequisite** | [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md)|
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md); [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) |
| **Synonyms** | how to pipe a value from another event; piping across events in a longitudinal project; how to pipe from a repeating instrument instance; using piping modifiers to control returned value; [event-name][field] cross-event piping syntax; pipe a specific repeat instance value; piping with event prefixes and instance qualifiers; how to reference a field from a different timepoint |

---

> **Version caveat (below 15.0.20 Standard):** Piping a field value **into a repeating context** — a repeating form or repeating event — from a source in a **non-repeating** context could produce a **blank value, or a value attached to the wrong instance**. Fixed in 15.0.20. Piped content that appears empty or mismatched on an older instance is worth checking against this rather than assumed to be a syntax error.

## 1. Overview

This article extends the piping basics covered in [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) into two areas: (1) piping across events and repeated instruments in longitudinal and repeating projects, and (2) using piping modifiers to control exactly what value is returned when a variable is piped. Readers should be comfortable with basic piping syntax before reading this article.

---

## 2. Key Concepts & Definitions

**Event**

A named time point or visit in a longitudinal REDCap project. Events are defined on the "Define My Events" page in Project Setup. Each event has a system-generated unique name (e.g., `event_1_arm_1`) used in piping syntax.

**Arm**

A group of events within a longitudinal project. Multi-arm projects are used for randomized or branching study designs. A record can only be enrolled in one arm at a time.

**Repeated Instrument**

An instrument configured to allow multiple instances of data collection for a single record within one event. Each instance is numbered starting at 1.

**Repeated Event**

An event configured to repeat, allowing multiple instances of all instruments assigned to that event for a single record.

**Instance**

A single occurrence within a series of repeated instrument or repeated event submissions. Instances are numbered sequentially (1, 2, 3…).

**Piping Modifier**

A suffix appended to a variable name inside a bracket expression to change what value is returned. Modifiers follow a colon immediately after the variable name: `[variable_name:modifier]`.

---

## 3. Piping Across Events in Longitudinal Projects

### 3.1 Same-Event Piping

If the source variable and the destination field are in the same event, standard piping syntax works without modification — just use `[variable_name]` as described in [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md).

### 3.2 Cross-Event Piping

To pipe a value from a different event, prefix the variable reference with the event name in its own set of brackets:

```
[event_name][variable_name]
```

**Example:** To pipe `first_name` from the first event in Arm 1:

```
[event_1_arm_1][first_name]
```

This tells REDCap to retrieve the value of `first_name` specifically from the event named `event_1_arm_1`.

**Event-relative prefixes.** Instead of a fixed unique event name, you can place an event smart variable before the field to pick the event relative to the current one:

| **Prefix** | **Pipes the field from** |
|---|---|
| `[event-name][field]` | The current event |
| `[previous-event-name][field]` | The event before the current one |
| `[next-event-name][field]` | The event after the current one |
| `[first-event-name][field]` | The first event in the current arm |
| `[last-event-name][field]` | The last event in the current arm |

**Example:** `[previous-event-name][weight]` pipes the weight recorded at the previous visit. See [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) for details.

### 3.3 Rules for Cross-Event Piping

**No space between event and variable brackets.** If there is a space between `[event_1_arm_1]` and `[first_name]`, the event part is no longer read as a qualifier: `[event_1_arm_1]` is shown as literal text, and `first_name` is resolved from the current event.

**Event names are generated by REDCap — look them up.** You control the event label displayed to users, but REDCap generates the internal event name used in piping syntax. Look up the exact event name on the "Define My Events" page in Project Setup, or in the Codebook.

**Cross-arm piping is not a supported pattern.** Each record should exist in only one arm, so a value referenced from another arm is not reliably available. Keep the source data in the same arm as the place you pipe it into, or test the exact behavior in a test record before relying on it.

**Test each arm independently.** If your project has multiple arms and uses piping, test the complete data entry workflow in each arm separately. Variables specific to one arm can be hidden in other arms using branching logic.

**Survey Queue custom text pipes from the first event.** In a longitudinal project, fields piped into the Survey Queue's custom text without an event prefix are taken from the first event. Add an explicit event prefix if you need a value from a later event.

---

## 4. Piping with Repeated Instruments and Events

There are three distinct scenarios when piping intersects with repeated instruments or repeated events.

### 4.1 Piping Into a Repeated Instrument or Event

If the source variable comes from a regular (non-repeated) instrument or event, standard piping syntax works normally — use `[variable_name]` or `[event_name][variable_name]` as appropriate. The repeated instrument or event receiving the piped value treats it like any other reference.

### 4.2 Piping Out of a Repeated Instrument or Event

It is possible to pipe a value out of a repeated instrument or repeated event using two methods. Both methods allow you to specify which instance to reference when piping to a non-repeated destination.

#### Method 1: Direct Targeting by Instance Number

If you know the specific instance number, you can reference any variable in that instance using the following syntax:

```
[variable_name][instance_number]
```

**Example:** To pipe a medication name from the first instance:

```
[med_name][1]
```

This retrieves the value of `med_name` specifically from instance 1 of the repeated series.

**Longitudinal projects:** If the repeating source is in a different event, prepend the event name. If it is in the current event, the event prefix is not needed (adding it does no harm):

```
[event_name][variable_name][instance_number]
```

**Example:**

```
[event_1_arm_1][med_name][1]
```

#### Method 2: Smart Variable Targeting

You can use the `[first-instance]` and `[last-instance]` smart variables to dynamically reference the first or last instance in a repeated series without knowing the exact instance number:

```
[variable_name][smart_variable]
```

**Example:** To pipe a medication name from the first instance:

```
[med_name][first-instance]
```

**Longitudinal projects:** If the repeating source is in a different event, prepend the event name:

```
[event_name][variable_name][smart_variable]
```

**Example:**

```
[event_1_arm_1][med_name][first-instance]
```

The available smart variables for this purpose are `[first-instance]` and `[last-instance]`. Note that `[last-instance]` always points to the most recently created instance and will change if new instances are added later.

> **Version caveat (recent Standard releases; present in 17.6, not in LTS 17.3 or 16):** **Instance Embedding** can display a table of a repeating form's instances on another form or survey. Unlike piping, it respects the user's view rights on the source form, so a user without access to that form does not see its data. On 17.6+ Standard, consider Instance Embedding instead of `[last-instance]` piping when access control matters; on LTS, use piping and limit where the piped values are shown.

### 4.3 Piping Between Instances (Within the Same Repeated Series)

Piping within a repeated instance series works the same way as piping out of a repeated series (section 4.2), but with additional smart variables available that allow you to dynamically target different instances relative to the current one.

#### Direct Targeting by Instance Number

Within a repeated series, you can reference any instance by its number:

```
[variable_name][instance_number]
```

**Example:** To pipe a value from the first instance within the same repeated series:

```
[med_name][1]
```

#### Smart Variable Targeting

You can use instance smart variables to dynamically target different instances without knowing exact instance numbers:

```
[variable_name][smart_variable]
```

**Available instance smart variables:**

| **Smart Variable** | **Target** |
|---|---|
| `[current-instance]` | The instance currently being viewed |
| `[previous-instance]` | The instance immediately before the current one |
| `[next-instance]` | The instance immediately after the current one (if it exists) |
| `[first-instance]` | The first instance in the series |
| `[last-instance]` | The most recently created instance in the series — note this changes as more instances are added |
| `[new-instance]` | The next instance to be created (last instance + 1) — mainly used in survey links and for instance numbers, since that instance holds no data yet |

**Example:** To pipe a medication name from the first instance:

```
[med_name][first-instance]
```

To pipe a visit date from the previous instance:

```
[visit_date][previous-instance]
```

> **Note:** To pipe a field value, an instance smart variable must come **after** a variable name bracket — e.g., `[visit_date][first-instance]`. On its own (e.g., `[first-instance]`), or placed before the field, it pipes the instance **number** rather than a field value.

**Longitudinal projects with repeated instruments/events:** When combining event and instance qualifiers, place the event name first, then the variable name, then the instance qualifier:

```
[event_name][variable_name][instance_number_or_smart_variable]
```

For a broader overview of all smart variables, see [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md).

---

## 5. Piping Modifiers

Modifiers let you control exactly what a pipe reference returns, overriding the default behavior for a given field type.

### 5.1 The `:value` Modifier

Appending `:value` to a variable name returns the raw coded value instead of the display label. This applies to dropdowns, radio buttons, checkboxes, yes/no, true/false, and dynamic query (SQL) fields.

**Example — Yes/No field:**

| **Expression** | **If "Yes" selected** | **If "No" selected** |
|---|---|---|
| `[yesno]` | Yes | No |
| `[yesno:value]` | 1 | 0 |

### 5.2 File Upload & Signature Modifiers

Both field types share the same modifiers:

| **Modifier** | **Effect** |
|---|---|
| `:label` | Displays the uploaded file's filename |
| `:inline` | Renders the file contents inline for images (JPG, JPEG, JPE, GIF, PNG, TIF, TIFF, BMP, WEBP, SVG). PDFs display inline on forms and surveys but not in emails; other file types show an icon rather than their content |
| `:link` | Generates a direct download link for the file, displayed as a clickable filename |

Without a modifier, piping a file upload or signature field returns an internal reference value (a number), which is rarely useful for display purposes.

> **Note:** The `:inline` modifier also works inside email bodies (survey invitations and Alerts & Notifications), allowing inline images to appear directly in the email. If the piped file is not an image type, REDCap will attach the file to the email and display the filename as a text alternative. The `:link` modifier similarly works inside email bodies, producing a clickable download hyperlink.

> **Note:** Inline images cannot be displayed inside a downloaded PDF of a survey or instrument.

### 5.3 Checkbox Modifiers

Checkbox fields allow multiple selections, so their piping behavior has additional options:

**`[my_checkbox:checked]`** — Returns a comma-separated list of the labels of all checked options. Example: "Sunday, Tuesday, Thursday". This is the default behavior when no modifier is used.

**`[my_checkbox:unchecked]`** — Returns a comma-separated list of the labels of all unchecked options. Example: "Monday, Wednesday, Friday, Saturday".

**`[my_checkbox(code)]`** — Returns "Checked" or "Unchecked" for a specific option identified by its coded value. Example: `[my_checkbox(2)]` returns "Checked" if option 2 is selected.

**Combining with `:value`:**

- `[my_checkbox:checked:value]` — Returns the raw codes of checked options instead of labels. Example: "1, 3, 5" instead of "Vanilla, Strawberry, Chocolate".
- `[my_checkbox(2):value]` — Returns 1 if option 2 is checked, 0 if unchecked.

### 5.4 The `:hideunderscore` Modifier

When a piped variable has no stored value, REDCap normally displays six underscore characters (`______`) as a placeholder. Appending `:hideunderscore` causes the blank to be piped as truly empty — invisible to the user — rather than as the underscore placeholder.

**Example:**

- `[first_name]` → displays `______` when empty
- `[first_name:hideunderscore]` → displays nothing when empty

This modifier works on both field variable references and Smart Variables.

### 5.5 The `:field-label` Modifier

Appending `:field-label` pipes the **label text** of the field rather than its data value. This is useful when you want to reference a question's wording dynamically.

**Example:** `[visit_date:field-label]` pipes the text "Date of Visit" (or whatever the field's label is), not the date value entered in that field.

### 5.6 Date & Time Modifiers

These modifiers apply to text box fields with date or time validation:

| **Modifier** | **Effect** |
|---|---|
| `:ampm` | Converts a time value from 24-hour format to AM/PM format, keeping the minutes. Example: 16:00 → 4:00pm. On datetime fields the date is kept too. Not available for time fields that include seconds (HH:MM:SS) |
| `:day` | Returns the day portion of the date as a number |
| `:month` | Returns the month portion of the date as a number |
| `:year` | Returns the year portion of the date as a number |

---

## 6. Common Questions

**Q: How do I pipe a value from a different event in a longitudinal project?**

**A:** Wrap the event name in brackets and place it immediately before the variable name bracket, with no space between them: `[event_1_arm_1][variable_name]`. Look up the exact event name on the "Define My Events" page in Project Setup — REDCap generates event names automatically.

**Q: What happens if I put a space between the event qualifier and the variable name?**

**A:** The event part is no longer treated as a qualifier: it is shown as literal text, and the variable is resolved from the current event instead.

**Q: How do I pipe the filename of an uploaded file rather than a reference number?**

**A:** Use the `:label` modifier: `[my_file_upload:label]`. This returns the filename of the uploaded document.

**Q: How do I display whether a specific checkbox option is checked?**

**A:** Use the code modifier: `[my_checkbox(code)]`, replacing "code" with the actual coded value of that option. This returns "Checked" or "Unchecked". To get a 1 or 0 instead, add `:value`: `[my_checkbox(code):value]`.

**Q: Can I pipe a value from the previous instance of a repeated instrument?**

**A:** Yes — use `[variable_name][previous-instance]` (field first, then the smart variable). This targets the instance immediately before the current one in the repeated series. Written the other way round, `[previous-instance]` pipes the previous instance number and the field comes from the current instance. On the first instance there is no previous instance, so the piped value is blank.

**Q: How do I stop REDCap from showing six underscores when a piped value is empty?**

**A:** Append `:hideunderscore` to the variable name — e.g., `[first_name:hideunderscore]`. This causes the blank to appear as truly empty rather than as `______`. This modifier works on both field variables and Smart Variables.

**Q: Can I pipe a value out of a repeated instrument or event to a non-repeated location?**

**A:** Yes — use one of two methods. **Method 1 (Direct targeting):** If you know the instance number, use `[variable_name][instance_number]` — e.g., `[med_name][1]` to reference the first instance. **Method 2 (Smart variables):** Use `[variable_name][first-instance]` or `[variable_name][last-instance]` to dynamically target the first or last instance without knowing the exact number. For longitudinal projects where the repeating source is in a different event, prepend the event name: `[event_name][variable_name][instance_number_or_smart_variable]`.

**Q: What's the difference between piping out of a repeated instrument and piping between instances in the same repeated series?**

**A:** Piping out targets a non-repeated location (e.g., a field on a regular instrument); piping between instances targets another field within the same repeated series. Both use the same syntax, but within a repeated series you have access to additional smart variables like `[previous-instance]` and `[next-instance]` that are context-aware relative to the current instance.

---

## 7. Common Mistakes & Gotchas

**Including a space between the event qualifier and the variable bracket.** `[event_1_arm_1] [first_name]` breaks the event qualifier: `[event_1_arm_1]` appears as literal text and the value is resolved from the current event. REDCap does not warn you. Always confirm the rendered output in a test record.

**Using a human-readable event label instead of the system event name.** The event name in piping syntax (e.g., `event_1_arm_1`) is not the same as the label shown to users (e.g., "Baseline Visit"). Look up the system name on the Define My Events page.

**Mistyping a unique event name.** A misspelled or non-existent unique event name does not produce an error or a blank — the piped value can silently come from a different event. Always copy unique event names from the Define My Events page or the Codebook rather than typing them, and check the result in a test record.

**Forgetting to specify the instance when piping out of a repeated instrument.** When you pipe a variable out of a repeated instrument to a non-repeated location, tell REDCap which instance to use: either Method 1 (explicit instance number like `[med_name][1]`) or Method 2 (smart variable like `[med_name][first-instance]`). Without a qualifier, REDCap uses the current instance number of the page you are on — from a non-repeating form that is instance 1, so you get instance 1's value, which may not be the one you intended. Always add an explicit qualifier.

**Expecting `[last-instance]` to be stable.** The `[last-instance]` qualifier always points to the most recently created instance. If new instances are added later, what `[last-instance]` returns will change. Do not use it where a fixed reference is needed.

**Forgetting that checkbox default piping returns labels, not codes.** `[my_checkbox]` and `[my_checkbox:checked]` both return display labels by default. If downstream logic or display needs raw codes, use `:checked:value` or `(code):value` forms.

---

## 8. Related Articles

- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (core piping syntax, locations, field type defaults)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (full list of smart variable categories including instance qualifiers)
- [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md) (applying piping in confirmation emails, invitations, and alerts)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (event and arm configuration)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (configuring repeated instruments and events)
- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) (navigating events and arms during data entry)
- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) (navigating instances during data entry)
