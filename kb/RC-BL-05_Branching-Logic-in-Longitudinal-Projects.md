RC-BL-05

**Branching Logic — Longitudinal Projects**

| **Article ID** | RC-BL-05 |
|---|---|
| **Domain** | Branching Logic |
| **Applies To** | Longitudinal REDCap projects; requires Project Design and Setup rights |
| **Prerequisite** | RC-BL-02 — Branching Logic: Syntax & Atomic Statements; RC-LONG-01 — Longitudinal Project Setup |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-BL-01 — Overview & Scope; RC-BL-02 — Syntax & Atomic Statements; RC-BL-03 — Combining Statements; RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup; RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers |

---

# 1. Overview

This article covers how branching logic works in longitudinal REDCap projects — specifically, how to reference fields in other events using the cross-event syntax, how local vs. cross-event references differ, and how arms and repeated instruments interact with branching logic. It is part of the Branching Logic series and assumes familiarity with REDCap logic syntax (RC-BL-02) and longitudinal project setup (RC-LONG-01).

---

# 2. Key Concepts & Definitions

**Unique Event Name**

The system-generated identifier for an event in a longitudinal project, derived from the arm number and the event label (e.g., `baseline_arm_1`, `followup_4wk_arm_2`). This is the identifier used in cross-event branching logic references. It changes if the event label is renamed.

**Local Reference**

A logic statement that references a field within the same event as the field being shown or hidden. Local references use only the variable name in brackets — no event prefix is required. Example: `[consent_status]='1'`.

**Cross-Event Reference**

A logic statement that references a field in a different event. Cross-event references require a two-part bracket syntax: the unique event name in its own brackets, followed immediately by the variable name in its own brackets. Example: `[baseline_arm_1][consent_status]='1'`.

**Cross-Event Blank Behavior**

When a cross-event field has not yet been saved for a record, REDCap returns an empty string (`''`), not zero. A field that was never filled in and a field that was filled in with zero are different states and must be tested differently.

---

# 3. Cross-Event Reference Syntax

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

## 3.1 Local vs. Cross-Event References

| | **Local Reference** | **Cross-Event Reference** |
|---|---|---|
| **When to use** | Referencing a field in the same event | Referencing a field in a different event |
| **Syntax** | `[variable_name]` | `[unique_event_name][variable_name]` |
| **Example** | `[age]>=18` | `[baseline_arm_1][age]>=18` |
| **Event prefix required?** | No | Yes |

> **Note:** "Same event" means any field in any instrument designated to the current event. If two instruments are both designated to Event A, a field in the first can reference a field in the second using a local reference — no event prefix needed.

> **Tip:** You can also include the current event's unique event name in a cross-event-style reference, and it will work correctly. This is occasionally useful when writing logic in bulk via the Data Dictionary, where you want all references to be explicit. However, omitting the prefix for same-event fields is the standard practice.

## 3.2 Finding the Unique Event Name

The unique event name is visible in the **Define My Events** table in Project Setup. It appears in the **Unique Event Name** column next to each event. It is auto-generated from the event label and arm number and cannot be manually overridden.

> **Important:** If you rename an event label, the unique event name changes automatically. Any branching logic that references the old unique event name will silently stop working. Always audit all logic after renaming an event.

---

# 4. Arm-Specific Considerations

In a multi-arm project, each arm has its own set of events with distinct unique event names (e.g., `baseline_arm_1` vs. `baseline_arm_2`). Logic referencing a specific arm's event will only evaluate correctly for records assigned to that arm.

## 4.1 Instruments Shared Across Arms

When the same instrument is designated to events in multiple arms, a cross-event reference within that instrument must match the arm of the current record. A reference to `[baseline_arm_1][diagnosis]` in an instrument that appears in both Arm 1 and Arm 2 will:

- Return the expected value for records in Arm 1 (where `baseline_arm_1` exists)
- Return blank for records in Arm 2 (where `baseline_arm_1` does not exist)

This means that arm-specific logic can emerge unintentionally from cross-event references. If an instrument is shared across arms and contains cross-event logic, verify that the referenced event exists in every arm where the instrument appears.

## 4.2 Writing Arm-Aware Logic

If a field should appear conditionally depending on which arm a record is in, use smart variables to reference the current arm. See RC-PIPE-09 — Smart Variables: Event & Arm for syntax details.

For most common patterns — gating later events behind earlier answers — the recommended approach is to write separate, arm-specific logic for each arm's version of the instrument, rather than attempting to write one statement that covers all arms.

---

# 5. Repeated Instruments and Repeated Events

Branching logic in a longitudinal project with repeated instruments or repeated events follows additional constraints beyond standard cross-event syntax.

## 5.1 Within a Repeated Instrument (Same Instance)

Logic within a repeated instrument that references other fields **in the same instance** works reliably using local references (no event prefix, no instance reference). Example: a logic statement on field B in instance 3 can reference field A in instance 3 using `[field_a]`.

## 5.2 Cross-Event References to Non-Repeated Fields

A repeated instrument can reference non-repeated fields from other events using standard cross-event syntax:

```
[baseline_arm_1][eligibility_confirmed]='1'
```

This works reliably because the referenced field in the baseline event has exactly one value per record.

## 5.3 Cross-Instance and Cross-Event References to Repeated Fields

Logic that attempts to reference a value from a specific instance of a repeated instrument (e.g., "instance 2 of the medication instrument at week 4") is not reliably supported in branching logic. Do not design logic that depends on reading a value from a specific prior instance of a repeated instrument.

If cross-instance logic is a design requirement, reconsider the data model. Consult your REDCap administrator before building logic that depends on inter-instance values.

> **See also:** RC-LONG-02 — Repeated Instruments & Events Setup (Section 8.1) for a broader discussion of how branching logic interacts with repeated instruments.

---

# 6. Common Cross-Event Logic Patterns

## 6.1 Gate a Later-Event Field Behind a Baseline Answer

Show a follow-up question only if a baseline field was answered with a specific value:

```
[baseline_arm_1][enrolled]='1'
```

## 6.2 Show a Field Only if a Prior-Event Field Was Filled In

Use the empty-string check to require that any value was saved at a prior event:

```
[baseline_arm_1][primary_diagnosis]<>''
```

This will evaluate to true as soon as anything is saved in `[primary_diagnosis]` at baseline, and to false if the field is blank (never saved).

## 6.3 Combine a Cross-Event Condition with a Local Condition

Show a follow-up question only if baseline consent was given AND the current event has a specific status:

```
[baseline_arm_1][consent_status]='1' AND [visit_status]='completed'
```

Here, `[consent_status]` references the baseline event; `[visit_status]` references the same event as the field being shown (local reference).

## 6.4 Use a Numeric Cross-Event Value

Show a field at a follow-up event only if a baseline score exceeded a threshold:

```
[baseline_arm_1][phq9_total]>=10
```

REDCap evaluates the number at baseline and applies the result to the current event's field visibility.

---

# 7. Common Questions

**Q: Do I need to include the event prefix when referencing a field in the same event?**

**A:** No. Local references — fields in the same event — use only the variable name: `[field_name]`. The event prefix is only required for fields in different events. Adding the prefix for the current event's own fields also works but is not required.

**Q: How do I find the unique event name to use in my logic?**

**A:** Go to **Project Setup → Define My Events**. The **Unique Event Name** column lists the auto-generated identifier for each event. Copy it exactly, including the `_arm_N` suffix.

**Q: What does a cross-event field return if the referenced event hasn't been filled in yet?**

**A:** It returns an empty string (`''`). REDCap does not return zero or null — it returns blank. Use `<>''` to test whether the field has been filled in at all, and `=''` to test whether it is still empty.

**Q: What happens if I rename an event after writing cross-event logic?**

**A:** Renaming an event changes its unique event name. Any branching logic that references the old name will stop evaluating correctly — the reference will return blank as if the event doesn't exist. REDCap will not flag the broken reference automatically. Always audit all logic statements that reference an event's unique name before and after renaming.

**Q: Can I reference a field from a different arm in my logic?**

**A:** Syntactically yes — you can write `[baseline_arm_2][field_name]` in a field that appears in Arm 1. However, records in Arm 1 will not have data in Arm 2 events, so the reference will always return blank for those records. This is almost never the intended behavior. Logic should reference events within the same arm as the current record.

**Q: Can I write logic that shows a field only in a specific arm?**

**A:** Not with a direct arm-check in branching logic syntax alone. The most practical approach is to use a smart variable that surfaces the current arm, then write logic against it. See RC-PIPE-09 — Smart Variables: Event & Arm.

**Q: Does cross-event logic work in the Survey Queue or Alerts?**

**A:** Yes. The same cross-event syntax works in any REDCap feature that uses the logic language — Survey Queue conditions, Automated Survey Invitation logic, alert conditions, and reports. The syntax is identical.

---

# 8. Common Mistakes & Gotchas

**Omitting the event prefix for cross-event references.** A reference to `[dob]` in a follow-up event will look for `dob` in the *current* event. If `dob` is only collected at baseline, the reference returns blank and the logic evaluates incorrectly. Always include the unique event name prefix when referencing a field from a different event.

**Testing for zero instead of blank on unsaved cross-event fields.** If a referenced field in another event has never been saved, it returns `''` (empty string), not `0`. A condition like `[baseline_arm_1][score]<>0` will evaluate to true for unsaved fields — because blank does not equal zero. Use `<>''` to test whether a cross-event field has been filled in at all.

**Breaking logic by renaming events.** Renaming an event label changes its unique event name silently. REDCap will not warn you that existing logic references will break. After renaming an event, search the Data Dictionary's Branching Logic column for the old unique event name and update every reference before saving the project.

**Referencing arm-specific events from instruments shared across arms.** An instrument designated to both arms that contains `[baseline_arm_1][field]` will work for Arm 1 records but return blank for Arm 2 records. This can cause fields to appear or disappear unexpectedly depending on the record's arm assignment. Validate cross-event logic against test records in every arm where the instrument appears.

**Designing logic that reads across repeated instrument instances.** Branching logic cannot reliably read a value from a specific prior instance of a repeated instrument. Logic like "show this field if the previous medication instance has a stop date" is not supported and will behave unpredictably. Restructure the instrument design to avoid this pattern.

---

# 9. Related Articles

- RC-BL-01 — Branching Logic: Overview & Scope (introduction to the series; lists cross-event logic as a topic)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (prerequisite — logic syntax fundamentals)
- RC-BL-03 — Branching Logic: Combining Statements (AND, OR, parentheses for multi-condition logic)
- RC-BL-04 — Branching Logic: Structured Fields & Checkboxes (checkbox and radio field syntax)
- RC-LONG-01 — Longitudinal Project Setup (unique event names, arms, and events — prerequisite)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeated setups affect branching logic)
- RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers (parallel cross-event syntax for piping)
- RC-PIPE-09 — Smart Variables: Event & Arm (arm and event smart variables for arm-aware logic)
- RC-FD-03 — Data Dictionary (bulk editing of branching logic — useful for auditing cross-event references after an event rename)
