

**Branching Logic — Longitudinal Projects**

| **Article ID** | [RC-BL-05 — Branching Logic — Longitudinal Projects](RC-BL-05_Branching-Logic-in-Longitudinal-Projects.md) |
|---|---|
| **Domain** | Branching Logic |
| **Applies To** | Longitudinal REDCap projects; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — longitudinal logic checked against source code; §3–§8 live-tested on v17.5.6; pages not re-captured |
| **Prerequisite** | [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) |
| **Version** | 1.4 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md); [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md); [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md); [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md); [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) |
| **Synonyms** | branching logic across events; how do i reference a field from another event in branching logic; cross-event branching logic syntax; branching logic in longitudinal projects; show a field based on data from a previous visit; using event names in branching logic; branching logic with arms and repeating instruments; reference an earlier event in logic; errors exist on this form after renaming an event; hidden fields showing after event rename |

---

## 1. Overview

This article covers how branching logic works in longitudinal REDCap projects — specifically, how to reference fields in other events using the cross-event syntax, how local vs. cross-event references differ, and how arms and repeated instruments interact with branching logic. It is part of the Branching Logic series and assumes familiarity with REDCap logic syntax ([RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)) and longitudinal project setup ([RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md)).

---

## 2. Key Concepts & Definitions

**Unique Event Name**

The system-generated identifier for an event in a longitudinal project, derived from the arm number and the event label (e.g., `baseline_arm_1`, `followup_4wk_arm_2`). This is the identifier used in cross-event branching logic references. It changes if the event label is renamed (see §3.2 for how it is formed).

**Local Reference**

A logic statement that references a field within the same event as the field being shown or hidden. Local references use only the variable name in brackets — no event prefix is required. Example: `[consent_status]='1'`.

**Cross-Event Reference**

A logic statement that references a field in a different event. Cross-event references require a two-part bracket syntax: the unique event name in its own brackets, followed immediately by the variable name in its own brackets. Example: `[baseline_arm_1][consent_status]='1'`.

**Cross-Event Blank Behavior**

When a cross-event field has not yet been saved for a record, REDCap returns an empty string (`''`), not zero. A field that was never filled in and a field that was filled in with zero are different states and must be tested differently. Checkboxes are the exception: a checkbox option in another event is never blank — an unchecked (or never-saved) option returns `0`, so test it with `[baseline_arm_1][symptoms(1)]='0'`, not `=''`.

Values from other events are loaded when the form or survey page opens. If the other event's data changes while the form is open (for example, another user saves it), the open form does not see the change until the page is reloaded.

---

## 3. Cross-Event Reference Syntax

In a non-longitudinal project, a variable reference in branching logic uses only the variable name:

```
[consent_status]='1'
```

In a longitudinal project, when referencing a field **in a different event**, prepend the unique event name in its own pair of square brackets:

```
[unique_event_name][variable_name]
```

**Example — show a follow-up field only if the participant consented at baseline:**

```
[baseline_arm_1][consent_status]='1'
```

**Example — show a week 12 question only if a week 4 value was recorded:**

```
[followup_4wk_arm_1][adverse_event]<>''
```

The two bracket pairs are written immediately adjacent — no space, no operator between them.

### 3.1 Local vs. Cross-Event References

| | **Local Reference** | **Cross-Event Reference** |
|---|---|---|
| **When to use** | Referencing a field in the same event | Referencing a field in a different event |
| **Syntax** | `[variable_name]` | `[unique_event_name][variable_name]` |
| **Example** | `[age]>=18` | `[baseline_arm_1][age]>=18` |
| **Event prefix required?** | No | Yes |

> **Note:** "Same event" means any field in any instrument designated to the current event. If two instruments are both designated to Event A, a field in the first can reference a field in the second using a local reference — no event prefix needed.

> **Note:** The event-prefix syntax is not restricted to different events — REDCap accepts any valid unique event name in the prefix position, including the current event's own name. The prefix is *required* only when referencing a field from a different event; for same-event fields, the current event is assumed and the prefix may be omitted. Explicitly prefixing same-event references is occasionally useful when editing logic in bulk via the Data Dictionary, where uniform syntax is easier to audit. Omitting the prefix for same-event fields remains the standard practice.

### 3.2 Finding the Unique Event Name

The unique event name is visible in the **Define My Events** table in Project Setup. It appears in the **Unique Event Name** column next to each event. It is auto-generated from the event label and arm number and cannot be manually overridden.

How REDCap forms the unique event name:

- It removes non-alphanumeric characters from the event label (other than spaces and underscores), replaces spaces with `_`, keeps the first 18 characters and lowercases them, then appends `_arm_N` for the event's arm. For example, `Follow-up Visit 1` becomes `followup_visit_1_arm_1`.
- If two events in the same arm produce the same name, the later ones get a letter added at the end (`b`, `c`, …) in event order, e.g. `visit_arm_1`, `visit_arm_1b`.
- Changing only the capitalisation of a label does not change the name. The **Custom Event Label** has no effect on it.
- Deleting or reordering events that share the same label, or changing an arm's number, can change existing unique event names. Re-check the **Unique Event Name** column after any of these changes.

> **Important:** If you rename an event label, the unique event name changes automatically (e.g. `baseline_arm_1` → `screening_arm_1`), but logic that references the old name is **not** updated. On data entry forms REDCap then shows an **ERRORS EXIST ON THIS FORM!** dialog listing the affected fields, and those fields are **displayed regardless of their logic** — questions meant to be hidden become visible. Surveys show **SURVEY ERRORS EXIST: CANNOT CONTINUE!**. Server-side uses — report filters, alert conditions, Automated Survey Invitation logic and Survey Queue conditions — give no error and simply stop working as intended. Always audit all logic after renaming an event, including every report filter.

> **Note:** In a project in Production, only REDCap administrators can rename events; administrators see a warning before doing so. Plan event labels before moving to Production.

---

## 4. Arm-Specific Considerations

In a multi-arm project, each arm has its own set of events with distinct unique event names (e.g., `baseline_arm_1` vs. `baseline_arm_2`). Logic referencing a specific arm's event will only evaluate correctly for records assigned to that arm.

### 4.1 Instruments Shared Across Arms

When the same instrument is designated to events in multiple arms, a cross-event reference within that instrument must match the arm of the current record. A reference to `[baseline_arm_1][diagnosis]` in an instrument that appears in both Arm 1 and Arm 2 will:

- Return the expected value for records in Arm 1 (where `baseline_arm_1` exists)
- Return blank for records in Arm 2 (where `baseline_arm_1` does not exist)

This means that arm-specific logic can emerge unintentionally from cross-event references. If an instrument is shared across arms and contains cross-event logic, verify that the referenced event exists in every arm where the instrument appears.

### 4.2 Writing Arm-Aware Logic

If a field should appear conditionally depending on which arm a record is in, use smart variables to reference the current arm. For example, to show a field only for records in Arm 2:

```
[arm-number]='2'
```

See [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md) for syntax details.

Branching logic is stored once per field, not once per arm. If an instrument is shared across arms and the condition differs by arm, the conditions for every arm must live in the same statement, each qualified by the arm:

```
([arm-number]='1' and [baseline_arm_1][x]='1') or ([arm-number]='2' and [baseline_arm_2][x]='1')
```

Alternatively, use an arm-relative event smart variable as the event prefix, so one reference works in every arm. `[first-event-name][x]='1'` checks `x` in the first event of the record's own arm.

Both approaches work; they make the logic longer and harder to audit, so test them with a record in every arm.

### 4.3 Event Smart Variables

These smart variables can be used in place of a unique event name, either on their own (e.g. `[event-name]='baseline_arm_1'`) or as an event prefix (e.g. `[previous-event-name][weight]`):

| **Smart Variable** | **Returns** |
|---|---|
| `[event-name]` | The current event's unique event name |
| `[previous-event-name]` | The event before the current one |
| `[next-event-name]` | The event after the current one |
| `[first-event-name]` | The first event |
| `[last-event-name]` | The last event |

`[previous-event-name]`, `[next-event-name]`, `[first-event-name]` and `[last-event-name]` stay within the record's current arm, and skip events where the current instrument is not designated. See [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md).

---

## 5. Repeated Instruments and Repeated Events

Branching logic in a longitudinal project with repeated instruments or repeated events follows additional constraints beyond standard cross-event syntax.

### 5.1 Within a Repeated Instrument (Same Instance)

Logic within a repeated instrument that references other fields **in the same instance** works reliably using local references (no event prefix, no instance reference). Example: a logic statement on field B in instance 3 can reference field A in instance 3 using `[field_a]`.

### 5.2 Cross-Event References to Non-Repeated Fields

A repeated instrument can reference non-repeated fields from other events using standard cross-event syntax:

```
[baseline_arm_1][eligibility_confirmed]='1'
```

This works reliably because the referenced field in the baseline event has exactly one value per record.

### 5.3 Referencing Specific Instances of a Repeated Instrument

When branching logic needs to evaluate a value from a specific instance of a repeated instrument, REDCap supports two methods — the same syntax used for piping (see [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md), Section 4.2).

#### Method 1: Direct Instance Number

Append the instance number in its own brackets immediately after the variable name:

```
[variable_name][instance_number]
```

**Example** — show a field only if the medication name in instance 1 is "Aspirin":

```
[med_name][1]='Aspirin'
```

In a longitudinal project, prepend the event name:

```
[event_name][variable_name][instance_number]
```

**Example:**

```
[event_1_arm_1][med_name][1]='Aspirin'
```

#### Method 2: Smart Variable Targeting

Use `[first-instance]` or `[last-instance]` to reference the first or last instance without knowing the exact number:

```
[variable_name][first-instance]
[variable_name][last-instance]
```

In a longitudinal project, prepend the event name:

```
[event_name][variable_name][first-instance]
```

> **Important:** `[last-instance]` always points to the highest-numbered instance — normally the most recently created one. Its value changes if new instances are added later. Use it only when dynamic "latest entry" behavior is what you need.

> **Important:** When you reference data in a repeating instrument or repeating event **in another event**, always add an instance qualifier (`[1]`, `[first-instance]`, `[last-instance]`). Without one, it is not obvious which instance REDCap evaluates, and the result may not be the one you expect.

#### Within a Repeated Series

When branching logic runs inside a repeated instrument (i.e., the field being shown or hidden is itself in the repeated instrument), additional smart variables are available to reference other instances in the same series:

| **Smart Variable** | **Target** |
|---|---|
| `[previous-instance]` | The current instance number minus 1 |
| `[next-instance]` | The instance immediately after the current one |
| `[first-instance]` | The first instance in the series |
| `[last-instance]` | The highest-numbered instance |

**Example** — inside a repeated instrument, show a field only if the previous instance's visit was marked complete:

```
[visit_status][previous-instance]='complete'
```

`[previous-instance]` is simply the current instance number minus 1. If that instance does not exist — because the current instance is the first, or because instance numbers have a gap after a deletion — the reference returns blank.

> **Version caveat (below 17.5.0 Standard; LTS):** If the referenced field is a **date or datetime field with a Missing Data Code** saved, logic like `[visit_date][last-instance]<>''` could return an unexpected result on the form or survey. Server-side evaluation (Data Quality rule H, calculations during import) was correct, so the same logic could behave differently on the page and in a report. Fixed in Standard 17.5.x; not confirmed for 17.3 LTS; not fixed in 16.x LTS. On those versions, test such logic on the form itself, or avoid blank checks on date fields that can hold a Missing Data Code.

> **Version caveat (below 17.5.4 Standard / 17.3.18 LTS; all 16.x LTS):** On **repeating events**, branching logic on integer and number fields could treat `0` as blank and blank as non-blank. The fix also covers instance-qualified references (e.g. `[weight][previous-instance]`) and calculated and slider fields. 16.x LTS does not have the fix: on 16.x, test for the positive or non-zero case instead of `=''` or `='0'`, or upgrade. See [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) §6.

> **See also:** [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (Section 8.1) for a broader discussion of how repeated setups affect branching logic; [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) (Section 4.2–4.3) for the parallel piping syntax.

---

## 6. Common Cross-Event Logic Patterns

### 6.1 Gate a Later-Event Field Behind a Baseline Answer

Show a follow-up question only if a baseline field was answered with a specific value:

```
[baseline_arm_1][enrolled]='1'
```

### 6.2 Show a Field Only if a Prior-Event Field Was Filled In

Use the empty-string check to require that any value was saved at a prior event:

```
[baseline_arm_1][primary_diagnosis]<>''
```

This will evaluate to true as soon as anything is saved in `[primary_diagnosis]` at baseline, and to false if the field is blank (never saved).

### 6.3 Combine a Cross-Event Condition with a Local Condition

Show a follow-up question only if baseline consent was given AND the current event has a specific status:

```
[baseline_arm_1][consent_status]='1' AND [visit_status]='completed'
```

Here, `[consent_status]` references the baseline event; `[visit_status]` references the same event as the field being shown (local reference).

### 6.4 Use a Numeric Cross-Event Value

Show a field at a follow-up event only if a baseline score exceeded a threshold:

```
[baseline_arm_1][phq9_total]>=10
```

REDCap evaluates the number at baseline and applies the result to the current event's field visibility.

---

## 7. Common Questions

**Q: Do I need to include the event prefix when referencing a field in the same event?**

**A:** No. Local references — fields in the same event — use only the variable name: `[field_name]`. The event prefix is only required for fields in different events. Adding the prefix for the current event's own fields also works but is not required.

**Q: How do I find the unique event name to use in my logic?**

**A:** Go to **Project Setup → Define My Events**. The **Unique Event Name** column lists the auto-generated identifier for each event. Copy it exactly, including the `_arm_N` suffix.

**Q: What does a cross-event field return if the referenced event hasn't been filled in yet?**

**A:** It returns an empty string (`''`). REDCap does not return zero or null — it returns blank. Use `<>''` to test whether the field has been filled in at all, and `=''` to test whether it is still empty. The exception is checkboxes: an unchecked checkbox option in another event returns `0`, never blank, so test it with `='0'`.

**Q: What happens if I rename an event after writing cross-event logic?**

**A:** Renaming an event changes its unique event name, and REDCap does not update logic that uses the old name. On data entry forms, every field whose branching logic references the old name triggers an **ERRORS EXIST ON THIS FORM!** dialog when the form opens, and those fields are shown regardless of their logic; surveys show **SURVEY ERRORS EXIST: CANNOT CONTINUE!**. Report filters, alert conditions, Automated Survey Invitation logic and Survey Queue conditions give no error — they simply stop working as intended. Nothing warns you at the moment of renaming, so audit all logic that references the event's unique name before and after renaming, and re-check every report filter afterwards.

**Q: Can I reference a field from a different arm in my logic?**

**A:** Syntactically yes — you can write `[baseline_arm_2][field_name]` in a field that appears in Arm 1. However, records in Arm 1 will not have data in Arm 2 events, so the reference will always return blank for those records. This is almost never the intended behavior. Logic should reference events within the same arm as the current record.

**Q: Can I write logic that shows a field only in a specific arm?**

**A:** Yes. Use the `[arm-number]` smart variable: `[arm-number]='2'` shows the field only for records in Arm 2. If the condition differs by arm, combine the arms in one statement, e.g. `([arm-number]='1' and [baseline_arm_1][x]='1') or ([arm-number]='2' and [baseline_arm_2][x]='1')` — see §4.2. See [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md).

**Q: Can I write branching logic that checks a value from a specific instance of a repeated instrument?**

**A:** Yes. Use the instance qualifier syntax: `[variable_name][instance_number]` for a fixed instance, or `[variable_name][first-instance]` / `[variable_name][last-instance]` to dynamically target the first or last instance. Inside a repeated instrument, you can also use `[variable_name][previous-instance]` or `[variable_name][next-instance]` to reference instances relative to the current one. In a longitudinal project, prepend the event name: `[event_name][variable_name][instance_number]`.

**Q: Does cross-event logic work in the Survey Queue or Alerts?**

**A:** Yes. The same cross-event syntax works in any REDCap feature that uses the logic language — Survey Queue conditions, Automated Survey Invitation logic, alert conditions, and reports. The syntax is identical.

The evaluation context is not always identical, though. A form evaluates logic for the event it is open in. In a report, the option **Show data for all events for each record returned** is ticked by default, so a filter like `[baseline_arm_1][enrolled]='1'` returns **all events** of each matching record; untick it to get only the rows of the events the filter references. An API filter (`filterLogic`) returns only the matching events — here, each matching record's **baseline** row, not its follow-up rows. See [RC-API-02 — Export Records API](RC-API-02_Export-Records.md).

---

## 8. Common Mistakes & Gotchas

**Omitting the event prefix for cross-event references.** A reference to `[dob]` in a follow-up event will look for `dob` in the *current* event. If `dob` is only collected at baseline, the reference returns blank and the logic evaluates incorrectly. Always include the unique event name prefix when referencing a field from a different event.

**Testing for zero instead of blank on unsaved cross-event fields.** If a referenced field in another event has never been saved, it returns `''` (empty string), not `0`. A condition like `[baseline_arm_1][score]<>0` will evaluate to true for unsaved fields — because blank does not equal zero. Use `<>''` to test whether a cross-event field has been filled in at all. Checkboxes work the other way round: an unchecked option is `0`, never blank, so `[baseline_arm_1][symptoms(1)]=''` is never true.

**Breaking logic by renaming events.** Renaming an event label changes its unique event name without warning, and existing logic keeps the old name. Forms then show an error dialog and display the affected fields unconditionally — hidden questions appear — and surveys cannot continue. Report filters, alerts, Automated Survey Invitations and the Survey Queue give no error but stop working as intended. After renaming an event, search for the old unique event name and update every reference in:

- branching logic and calculations (Data Dictionary download)
- `@CALCTEXT`, `@CALCDATE`, `@IF` and `@DEFAULT` action tags (Field Annotation column)
- validation minimum and maximum values
- report filters
- Data Quality rules
- Automated Survey Invitation logic
- alert conditions
- Survey Queue conditions

**Referencing arm-specific events from instruments shared across arms.** An instrument designated to both arms that contains `[baseline_arm_1][field]` will work for Arm 1 records but return blank for Arm 2 records. This can cause fields to appear or disappear unexpectedly depending on the record's arm assignment. Validate cross-event logic against test records in every arm where the instrument appears.

**Using `[last-instance]` where a stable reference is needed.** The `[last-instance]` smart variable always points to the highest-numbered instance. If users add more instances later, what it returns changes. For logic that must evaluate a fixed instance, use a direct instance number (`[variable_name][1]`) rather than `[last-instance]`.

---

## 9. Related Articles

- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (introduction to the series; lists cross-event logic as a topic)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (prerequisite — logic syntax fundamentals)
- [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md) (AND, OR, parentheses for multi-condition logic)
- [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md) (checkbox and radio field syntax)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (unique event names, arms, and events — prerequisite)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (how repeated setups affect branching logic)
- [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) (parallel cross-event syntax for piping)
- [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md) (arm and event smart variables for arm-aware logic)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (bulk editing of branching logic — useful for auditing cross-event references after an event rename)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) (`filterLogic` evaluates cross-event logic differently from forms)
