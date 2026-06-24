

**Smart Variables: Repeating Instruments and Events**

| **Article ID** | [RC-PIPE-10 — Smart Variables: Repeating Instruments and Events](RC-PIPE-10_Smart-Variables-Repeating-Instruments-and-Events.md) |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with repeating instruments or repeating events enabled |
| **Prerequisite** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md); [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md) |
| **Synonyms** | [current-instance] smart variable; how to reference the current repeat instance with [current-instance]; repeating instance smart variables like [first-instance] and [last-instance]; [next-instance] [previous-instance] and [new-instance] piping; [instance-qualifier] for repeating instruments; how to number rows in a repeating instrument or event; pipe a value from a specific repeat instance; smart variables for repeating forms and repeating events |

---

## 1. Overview

Instance smart variables track and reference specific instances (repetitions) of instruments or events in REDCap. They enable you to reference data from the previous instance, the current instance, the next instance, the first instance, or the last instance within a repeating set. Additionally, the `[new-instance]` smart variable enables creation of links to new instances that do not yet exist. Use these variables in field labels, logic, form links, survey invitations, and calculated fields to navigate repeating data dynamically.

---

## 2. Key Concepts & Definitions

**Instance / Instance Number**

A single repetition of a repeating instrument or repeating event. Each instance is identified by a sequential number starting at 1. For example, in a repeating survey called "daily_log", Instance 1 is the first response, Instance 2 is the second, and so on.

**Repeating Instrument**

A single instrument (form/survey) that can be filled out multiple times per record. Each completion is a separate instance. Example: a "Daily Symptom Log" that a participant fills out every day throughout a study.

**Repeating Event**

An entire event (containing multiple instruments) that repeats. Each occurrence of the event is an instance. Example: a "Follow-up Visit" event that repeats at irregular intervals.

**Instance Qualifier**

A smart variable paired with a field variable to reference data from a specific instance. Examples: `[current-instance]`, `[last-instance]`, `[field-name][previous-instance]`. (Note: these are distinct from piping *modifiers* such as `:value` or `:label`, which are colon-prefixed suffixes that change what a field variable returns — see [RC-PIPE-03](RC-PIPE-03_Smart-Variables-Overview.md).)

**New Instance**

A future instance that has not yet been created. The `[new-instance]` smart variable calculates the next available instance number, allowing you to pre-populate links or default values for new instances before they exist.

---

## 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Current Instance | `[current-instance]` | The current repeating instance number. Using `[field][current-instance]` is functionally equivalent to using `[field]` alone on the current instance. Can be used standalone or appended to a field variable. `[heart_rate][current-instance]` → 84. | 2 |
| Previous Instance | `[previous-instance]` | The repeating instance number immediately before the current instance (current minus 1). Can be used standalone or appended to a field variable: `[weight][previous-instance]` → 145. Returns blank if the current instance is 1 (the first instance). | 3 |
| Next Instance | `[next-instance]` | The repeating instance number immediately after the current instance (current plus 1). Can be used standalone or appended: `[provider][next-instance]` → Harris. Returns a calculated number even at the last instance; there may be no data at that instance yet. | 7 |
| First Instance | `[first-instance]` | The first (lowest numbered) repeating instance number for the current record/event context, which is always 1 unless instances have been deleted. Can be used standalone or appended: `[age][first-instance]` → 24. | 1 |
| Last Instance | `[last-instance]` | The last (highest numbered) repeating instance number for the current record/event context. Can be used standalone or appended: `[glucose][last-instance]` → 119. | 6 |
| New Instance | `[new-instance]` | A new, not-yet-created repeating instance (calculated as `[last-instance]` plus 1). Can be used standalone, OR appended ONLY to these smart variables: `[survey-link]`, `[survey-url]`, `[survey-access-code]`, `[form-link]`, `[form-url]`. Example: `[survey-link:repeating_survey:Repeating Survey][new-instance]` → Repeating Survey. Returns a calculated instance number one higher than the current last instance. | 14 |

---

## 4. Usage Notes

**Instance Qualifier Syntax**

Instance smart variables are appended to field variables to retrieve data from a specific instance. The syntax is: `[field-name][instance-qualifier]`. Examples:
- `[symptom_severity][previous-instance]` — severity from the previous instance
- `[blood_pressure][last-instance]` — blood pressure from the last instance
- `[notes][current-instance]` — notes from the current instance (equivalent to `[notes]`)

**First and Previous Instance Behavior**

- `[first-instance]` always returns 1 (unless instances have been deleted, which is rare).
- `[previous-instance]` returns blank if used in Instance 1 (the first instance). Plan your designs to handle this case by using conditional logic or `:hideunderscore`.

**Next and Last Instance Behavior**

- `[last-instance]` returns the highest instance number that has been completed.
- `[next-instance]` calculates `[last-instance]` + 1, which may or may not exist yet.
- If there is no next instance yet (the user is viewing the last instance), `[next-instance]` still returns a valid number but there may be no data in that instance.

**New Instance Smart Variable Restrictions**

`[new-instance]` can only be appended to these specific smart variables:
- `[survey-link]` / `[survey-url]` / `[survey-access-code]`
- `[form-link]` / `[form-url]`

You **cannot** use `[new-instance]` with field variables. For example, `[field][new-instance]` is invalid.

**Use Cases for `[new-instance]`**

`[new-instance]` is useful for:
- Pre-populating survey or form links to the next instance before it is created.
- Generating default text like "Click here to fill out the next survey" that automatically adjusts as instances are added.
- Conditional links: show a link to the next instance only if a certain condition is met.

Example: In a repeating survey called "daily_log", you might include a button labeled "Fill out tomorrow's log" that links to `[survey-link:daily_log][new-instance]`.

**Repeating Events with Instance Qualifiers**

If your project uses repeating events, instance qualifiers work the same way. They track which repetition of the event you are in. For example, if a "Follow-up Visit" event repeats, `[baseline_arm_1][weight][last-instance]` retrieves the weight from the last instance of the Follow-up Visit event.

**Instance Qualifiers in Calculated Fields**

Instance smart variables work in calculated fields and can be combined with logic. Example: `if([current-instance]=1, "First response", "Later response")` displays different text depending on whether it is the first or a later instance.

**Longitudinal Projects with Repeating Instruments**

In longitudinal projects with repeating instruments, instance qualifiers and event prefixes can be combined:
- `[baseline_arm_1][field][last-instance]` — field from the last instance in the Baseline event
- `[previous-event-name][field][current-instance]` — field from the previous event's current instance

---

## 5. Common Questions

**Q: How do I reference data from the previous instance of a repeating survey?**

**A:** Use `[field-name][previous-instance]`. For example, if you have a repeating "daily_log" survey with a "mood" field, use `[mood][previous-instance]` to display the mood from the previous day's entry. This is useful for showing trends or allowing users to compare their responses.

**Q: What is the difference between `[last-instance]` and `[new-instance]`?**

**A:** `[last-instance]` is the instance number of the most recently completed instance (where data exists). `[new-instance]` is the instance number for the next instance that has not yet been created (calculated as `[last-instance]` + 1). Use `[last-instance]` to reference existing data; use `[new-instance]` to link to or pre-populate the upcoming instance.

**Q: Can I use instance qualifiers in branching logic?**

**A:** Yes. For example, `[mood][current-instance]>5` shows a field only if the current instance's mood score is greater than 5. Or `[is-completed:daily_log][last-instance]=0` shows a field if the last instance is incomplete. Instance qualifiers work in all logic contexts.

**Q: How do I create a link to the next instance of a repeating survey?**

**A:** It depends on whether the next instance already exists. To link to an **existing** next instance, use `[survey-link:instrument][next-instance]` — for example, `[survey-link:daily_log:Fill out tomorrow's log][next-instance]`. To link to a **not-yet-created** instance, use `[survey-link:instrument][new-instance]` — for example, `[survey-link:daily_log:Fill out tomorrow's log][new-instance]`. When in doubt, `[new-instance]` is the safer choice for "open the next unfilled instance."

**Q: What happens if I use `[previous-instance]` in the first instance?**

**A:** It returns blank because there is no instance before Instance 1. Use conditional logic to handle this: `if([current-instance]>1, [field][previous-instance], "No previous instance")`.

**Q: I need to link to a new instance that hasn't been created yet. Is this possible?**

**A:** Yes, use `[new-instance]` appended to a survey or form link: `[survey-link:repeating_form][new-instance]` or `[form-link:repeating_form][new-instance]`. This generates a link to the next instance number, which REDCap will create when the form is first accessed.

**Q: Can I use instance qualifiers in email invitations?**

**A:** Yes, if the email is tied to a repeating instrument or event context. For example, a survey invitation email for a repeating survey can include `[survey-access-code:repeating_survey][last-instance]` to reference the access code for the most recent instance.

---

## 6. Common Mistakes & Gotchas

**Using `[new-instance]` with field variables.** `[new-instance]` can only be appended to form/survey links, not to field variables. `[field][new-instance]` is invalid. Use `[last-instance]` or `[next-instance]` to reference existing instances instead.

**Not handling blank `[previous-instance]` in Instance 1.** If you use `[field][previous-instance]` in a repeating instrument where the first instance is being filled out, it returns blank. Either hide the reference with `:hideunderscore` or use conditional logic to show something like "This is your first entry."

**Assuming `[next-instance]` data exists.** `[next-instance]` returns a calculated number, but the instance may not have data yet. If you pipe `[field][next-instance]` into a field, it will be blank until the next instance is created and filled. Plan your design accordingly.

**Confusing instance qualifiers with event smart variables.** Instance qualifiers (`[current-instance]`, `[previous-instance]`) track repetitions within a repeating instrument or event. Event smart variables (`[previous-event-name]`, `[next-event-name]`) track different events. Do not mix them up; they serve different purposes.

**Not testing repeating designs with different numbers of instances.** A form that works well with 5 instances might display awkwardly if a user creates 20 instances. Test your repeating designs with varying numbers of instances to ensure labels, links, and logic remain functional.

**Using instance qualifiers outside of repeating contexts.** If you use `[current-instance]`, `[previous-instance]`, etc. in a project or form without repeating instruments/events, they return blank. Verify that your project actually uses repeating functionality before relying on instance smart variables.

**Misunderstanding how `[new-instance]` calculates next instance.** `[new-instance]` is always `[last-instance]` + 1. If the last instance is Instance 5, `[new-instance]` is Instance 6, regardless of whether Instance 6 already exists. It's the calculated next number, not a check for an existing instance.

---

## 7. Pattern: Accumulator Chain for Cross-Instance Aggregation

A common challenge with repeating instruments is aggregating a value across all instances for use in alerts or piping — for example, building a list of all staff names who completed a training, or collecting all email addresses across a repeating staff roster.

REDCap cannot directly iterate over all instances in a formula, but you can build an **accumulator chain** using `[previous-instance]` and then surface the final result with `[last-instance]` from a non-repeating instrument.

**Step 1 — Compute the unit value per instance.** In the repeating instrument, create a hidden `@CALCTEXT` field that outputs the value you want to collect for this instance, or blank if not applicable:

```
@CALCTEXT(if([training_complete]='1', concat_ws(' ', [staff_fname], [staff_lname]), ''))
```

Store this in a hidden field, e.g., `staff_trained_this`.

**Step 2 — Accumulate across instances.** In the same repeating instrument, create a second hidden `@CALCTEXT` field that appends the current instance's value to whatever was accumulated in the previous instance:

```
@CALCTEXT(concat_ws(', ', [staff_trained_all][previous-instance], [staff_trained_this]))
```

In instance 1, `[previous-instance]` is blank, so the result is just this instance's value. In instance 2, it combines instance 1's accumulated value with instance 2's value, and so on.

**Step 3 — Surface the final value.** In a **non-repeating instrument** (often a dedicated "fields for alert piping" form), create a `@CALCTEXT` field that reads from the last instance:

```
@CALCTEXT([staff_trained_all][last-instance])
```

This field always reflects the full accumulated list and can be piped into alert email bodies.

**Important:** This pattern depends on instances being recalculated in order. If earlier instances are edited after later ones are added, accumulated values may become stale. The `recalculate` external module (if installed) can force recalculation across all instances. Also note that `concat_ws` with a blank value produces no extra delimiter — `concat_ws(', ', 'Alice', '')` returns `'Alice'`, not `'Alice, '` — which keeps the list clean even when some instances contribute nothing.

---

## 8. Related Articles

- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (overview of all smart variable categories)
- [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md)(detailed instance qualifier syntax)
- [RC-PIPE-07 — Smart Variables: Form](RC-PIPE-07_Smart-Variables-Form.md) (form links combined with instance qualifiers)
- [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md) (survey links combined with instance qualifiers)
- [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md) (event smart variables for longitudinal projects)
