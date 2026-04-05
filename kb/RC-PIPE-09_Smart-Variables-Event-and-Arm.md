RC-PIPE-09

**Smart Variables: Event & Arm**

| **Article ID** | RC-PIPE-09 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Longitudinal projects only |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers; RC-PIPE-10 — Smart Variables: Repeating Instruments and Events |

---

# 1. Overview

Event and Arm smart variables enable dynamic references to events within an arm in longitudinal REDCap projects. Rather than hard-coding a specific event name (which requires knowing the event structure at design time), these variables allow you to reference events relative to the current context — the previous event, the next event, the first event, the last event, and so forth. Use these variables in conditional logic, field labels, form links, and survey invitations to create designs that adapt automatically to your project's event structure.

---

# 2. Key Concepts & Definitions

**Longitudinal Project**

A REDCap project with multiple visits, timepoints, or data collection occasions per record. Longitudinal projects are organized into Arms (study branches) and Events (timepoints within an arm). Event and Arm smart variables only function in longitudinal projects.

**Event**

A specific data collection timepoint within an arm (e.g., "Baseline", "Month 3 Follow-up", "Study Exit"). Each event has a unique event name (e.g., `baseline_arm_1`, `month_3_arm_1`) and a human-readable label.

**Event ID**

REDCap's internal numeric identifier for an event. Event IDs are assigned by the system and are not user-modifiable.

**Event Number**

The ordinal position of an event within an arm (1st, 2nd, 3rd, etc.), as shown on the Define My Events page. Also called the event's "sequence order."

**Arm**

A study branch in a longitudinal project (e.g., "Control", "Treatment A", "Treatment B"). Each arm contains a sequence of events. Single-arm studies have one arm; multi-arm studies (like randomized trials) have multiple arms.

**Event Name (Unique Event Name)**

A unique identifier for an event within a project, configured on the Define My Events page (e.g., `baseline_arm_1`, `visit_3_arm_2`). Used in piping, logic, and system references.

**Event Label**

The human-readable name of an event (e.g., "Baseline Visit", "Month 3 Follow-up"). Labels are displayed in the user interface and can be customized for readability.

**Relative Event References**

Smart variables that reference events in relation to the current context. Examples: "the previous event", "the next event", "the first event in this arm". These allow conditional logic and links that adapt based on which event is active.

**Instrument Designation**

The specification of which instruments (forms) are assigned to each event. Not all instruments appear in every event. Event smart variables account for this when determining "previous" and "next" events relative to a specific instrument.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Event ID | `[event-id]` | The numeric ID (REDCap's internal identifier) of the current event. | 112 |
| Event Number | `[event-number]` | The ordinal position of the current event within the arm (1st, 2nd, 3rd, etc.). | 4 |
| Event Name | `[event-name]` | The unique event name of the current event. Can be used standalone or prepended to a field reference. `[event-name][weight]` → 125. | event_2_arm_1 |
| Event Label | `[event-label]` | The human-readable label of the current event. | Event 2 |
| Previous Event Name | `[previous-event-name]` | The unique event name of the event immediately before the current event. When standalone, returns the directly preceding event. When prepended to a field variable, returns the closest preceding event where that field's instrument is designated (may differ from directly preceding event). `[previous-event-name][heart_rate]` → 62. Returns blank if current event is first. | visit_4_arm_2 |
| Previous Event Label | `[previous-event-label]` | The event label of the event immediately before the current event. Returns blank if current event is first. | Visit 4 |
| Next Event Name | `[next-event-name]` | The unique event name of the event immediately after the current event. When standalone, returns the directly following event. When prepended to a field variable, returns the closest following event where that field's instrument is designated. `[next-event-name][provider]` → Taylor. Returns blank if current event is last. | event_3_arm_5 |
| Next Event Label | `[next-event-label]` | The event label of the event immediately after the current event. Returns blank if current event is last. | Third Timepoint |
| First Event Name | `[first-event-name]` | The unique event name of the first event in the current arm. When standalone, returns the absolute first event. When prepended to a field variable, returns the first event where that field's instrument is designated. `[first-event-name][heart_rate]` → 74. | visit_1_arm_2 |
| First Event Label | `[first-event-label]` | The label of the first event in the current arm. | Visit 1 |
| Last Event Name | `[last-event-name]` | The unique event name of the last event in the current arm. When standalone, returns the absolute last event. When prepended to a field variable, returns the last event where that field's instrument is designated. `[last-event-name][provider]` → Minor. | week_22_arm_1 |
| Last Event Label | `[last-event-label]` | The label of the last event in the current arm. | Week 22 |
| Arm Number | `[arm-number]` | The ordinal number of the current arm (1st, 2nd, 3rd, etc.). | 2 |
| Arm Label | `[arm-label]` | The label (display name) of the current arm. | Drug B |

---

# 4. Usage Notes

**Standalone vs. Prepended Event Smart Variables**

Event smart variables have two modes of use:

1. **Standalone**: Returns a property of the event itself. Example: `[previous-event-name]` returns the name of the event immediately before the current one.

2. **Prepended to a field variable**: Returns information for that field from a relative event. Example: `[previous-event-name][heart_rate]` returns the heart rate value from the closest previous event where the heart rate field's instrument is designated.

This distinction is important: `[previous-event-name]` and `[previous-event-name][field]` may return different event names if instruments are not designated in all events.

**Event Blank Behavior**

- `[previous-event-name]` and `[previous-event-label]` return blank if the current event is the first event in the arm.
- `[next-event-name]` and `[next-event-label]` return blank if the current event is the last event in the arm.
- Plan your designs to handle blank values gracefully (use conditional text or the `:hideunderscore` modifier).

**Longitudinal-Only**

All event and arm smart variables only function in longitudinal projects. Using them in a non-longitudinal (single-event) project will produce blank values or may cause errors. Always verify your project type before deploying designs using event smart variables.

**Event Names in Piping and Logic**

Event names are used in two ways:
1. As a variable prefix (hard-coded): `[baseline_arm_1][weight]` pipes the weight value from the Baseline event.
2. As a smart variable reference: `[first-event-name][weight]` pipes the weight value from the first event dynamically.

Both approaches work; use smart variables for flexibility and hard-coded event names for specificity.

**Arm References**

`[arm-number]` and `[arm-label]` are useful for personalizing forms and emails based on which study branch the record belongs to. For example: "You are enrolled in the `[arm-label]` arm of this study."

---

# 5. Common Questions

**Q: How do I create a field that references the previous event's data?**

**A:** Use an event-prepended smart variable. For example: `[previous-event-name][weight]` displays the weight value from the previous event. You can pipe this into a field label, field note, or calculated field. Note that if the previous event's instrument is not designated to contain the weight field, this returns blank.

**Q: What is the difference between `[previous-event-name]` and `[previous-event-name][field]`?**

**A:** `[previous-event-name]` (standalone) returns the name of the event immediately before the current one. `[previous-event-name][field]` returns the closest previous event where the specified field's instrument is designated, which may be further back if instruments are not in all events. For example, if a heart rate field only appears in Events 1, 3, and 5, `[previous-event-name][heart_rate]` from Event 5 returns Event 3, not Event 4.

**Q: Can I use event smart variables in branching logic?**

**A:** Yes. You can use event smart variables to conditionally show or hide fields based on event context. For example: `[event-label]='Baseline'` shows a field only at baseline. Or use `[previous-event-name][weight]>100` to show a field if the previous event's weight was greater than 100.

**Q: I need to create a link from the current event to the next event's form. How do I do that?**

**A:** Use `[next-event-name][form-link:instrument]`. For example: `[next-event-name][form-link:visit_data_form]` creates a link to the Visit Data form in the next event. See RC-PIPE-07 for more on form links.

**Q: What happens if I use an event smart variable in the last event?**

**A:** `[next-event-name]` and `[next-event-label]` return blank because there is no event after the last one. Plan your form design to handle this case — either hide the link to the next event, or use conditional text like "This is your final visit; thank you for your participation."

**Q: Can I use event smart variables for multi-arm studies?**

**A:** Yes. Each record belongs to one arm, and event smart variables resolve based on that arm's event structure. `[arm-label]` tells you which arm the current record belongs to. Note that different arms may have different event sequences; event smart variables adapt accordingly for each arm.

**Q: How do I reference a specific event by name?**

**A:** Use a hard-coded event prefix: `[baseline_arm_1][weight]` pipes the weight from the Baseline event of Arm 1. This requires knowing the exact event name. For dynamic, relative references, use event smart variables like `[previous-event-name][weight]`.

---

# 6. Common Mistakes & Gotchas

**Using event smart variables in non-longitudinal projects.** Event smart variables only work in longitudinal projects. If you use them in a single-event project, they return blank or may produce unexpected results. Always verify that your project is set up as longitudinal before relying on event smart variables.

**Not accounting for blank event references.** If `[previous-event-name]` is used in the first event, it returns blank. If `[next-event-name]` is used in the last event, it returns blank. If you create form links or field references using these variables, they will break in these edge cases. Plan your design to either hide these links conditionally or use conditional text that handles blanks.

**Confusing event smart variables with hard-coded event references.** `[previous-event-name][weight]` and `[baseline_arm_1][weight]` are different. The first is dynamic and adapts based on the current event; the second is fixed to a specific event. Use the appropriate approach for your design intent.

**Assuming event smart variables work the same for all fields.** When you use `[previous-event-name][field]`, it looks for the closest previous event where that field's instrument is designated. If the field's instrument is not in the previous event (even if that event exists), the smart variable skips backward to find the right event. This may surprise you if instruments are not designated uniformly across events.

**Not testing designs with different event structures.** If you later add, remove, or reorganize events in your longitudinal project, designs using event smart variables should adapt automatically. However, always test to confirm that links, logic, and field references still function correctly with the new event structure.

**Using event names from one arm in another arm.** Event names include the arm designation (e.g., `baseline_arm_1` vs. `baseline_arm_2`). If you hard-code an event name from one arm and apply the design to a record in a different arm, the reference will fail. Use event smart variables or arm-agnostic references when designing for multi-arm studies.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (hard-coded event references and event prefixes)
- RC-PIPE-07 — Smart Variables: Form (form links and URLs for cross-event navigation)
- RC-PIPE-08 — Smart Variables: Survey (survey links with event prefixes)
- RC-PIPE-10 — Smart Variables: Repeating Instruments and Events (instance qualifiers for repeating data)
