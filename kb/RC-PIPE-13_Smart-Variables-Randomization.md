

**Smart Variables: Randomization**

| **Article ID** | [RC-PIPE-13 — Smart Variables: Randomization](RC-PIPE-13_Smart-Variables-Randomization.md) |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with REDCap Randomization module enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — smart-variable behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md)|
| **Synonyms** | [rand-number] smart variable; how to pipe a randomization number with [rand-number]; randomization smart variables for the time randomized [rand-time]; [rand-utc-time] randomization timestamp smart variable; show when a record was randomized using [rand-time:value]; reference a specific randomization model with [rand-number:n]; pipe the randomization assignment time into a field or email; randomization-related smart variables; is [rand-time] shown in the user's timezone or the server's; [rand-number] blank after randomization; [rand-number] does not show the allocation group |

---

## 1. Overview

Randomization smart variables expose information about a record's randomization assignment in REDCap projects using the Randomization module. They return the randomization number assigned to the record, the date and time the randomization occurred, and the equivalent UTC timestamp. None of them returns the allocation group itself: to display or test the group, reference the randomization variable directly. These variables are useful for showing randomization details on forms and in emails, checking whether randomization has occurred, and tracking randomization timestamps. They only return values in projects with the Randomization module enabled; elsewhere they are blank.

---

## 2. Key Concepts & Definitions

**Randomization**

A process in REDCap that automatically assigns records to study groups (arms, treatment arms, or allocation groups) based on a pre-configured randomization scheme. Randomization can occur automatically when a trigger is met or manually by a coordinator.

**Randomization Number vs. Allocation Group**

The allocation group is the group the record was assigned to; it is stored in the randomization variable. The randomization number is a separate value from the allocation table. In text-field (blinded) randomization, the randomization number is what is stored in the randomization variable. In categorical (open) randomization, the allocation table can optionally carry an **alternate randomization number** for each slot alongside the group. `[rand-number]` returns the randomization number, never the group.

**Text-Field Randomization (Blinded Allocation)**

A randomization scheme where the allocation is stored in a text field and is opaque to the coordinator. The randomization number is typically a code like "R1-5638" that does not directly reveal the allocation group.

**Categorical Randomization (Open Allocation)**

A randomization scheme where the randomization variable is a dropdown or radio field whose choices are the allocation groups (e.g., "Control", "Treatment A", "Treatment B"), so the group is directly visible. If alternate randomization numbers were uploaded in the allocation table, `[rand-number]` returns the alternate number for the record's slot; if none were uploaded, `[rand-number]` is blank even after randomization. To show the group, pipe the randomization variable itself (e.g., `[rand_group]`).

**Randomization Timestamp**

The server date and time at which the record was randomized. REDCap records this automatically. Timestamps can be displayed in user-formatted or raw (YYYY-MM-DD HH:MM:SS) formats.

**UTC Time**

Coordinated Universal Time (UTC), also called GMT. REDCap stores both the server time and the UTC time of each randomization. Neither is converted to the viewing user's timezone: only the display **format** follows the user's date/time preferences.

**Multiple Randomizations**

Projects can have more than one randomization scheme. The `:n` suffix (e.g., `:1`, `:2`) allows you to reference a specific randomization when multiple are in use.

---

## 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Randomization Number (Default) | `[rand-number]` | The randomization number assigned to the record. For text-field (blinded) randomization, the same value as piping the randomization variable. For categorical (open) randomization, the alternate randomization number from the allocation table, or blank if none was uploaded. Never returns the allocation group. | R1-5638 |
| Randomization Number (Specific) | `[rand-number:n]` | References randomization `n` when the project has more than one randomization. Default is n=1. | R2-4231 |
| Randomization Time (Default) | `[rand-time]` | The server date/time at which the record was randomized. When piped for display, formatted per the user's date/time preferences. Logic and calculations receive the raw YYYY-MM-DD HH:MM:SS value automatically. | 31/05/2024 4:02:15pm |
| Randomization Time (Raw Format) | `[rand-time:value]` | The randomization time in raw YYYY-MM-DD HH:MM:SS format, for display piping where you want the raw value instead of the user's format. | 2024-05-31 16:02:15 |
| Randomization Time (Specific) | `[rand-time:n]` | References the randomization time for randomization `n` when the project has multiple randomizations. | 31/05/2024 4:02:15pm |
| Randomization Time (Specific, Raw) | `[rand-time:n:value]` | Raw format randomization time for a specific randomization. | 2024-05-31 16:02:15 |
| Randomization UTC Time (Default) | `[rand-utc-time]` | The UTC (GMT) date/time at which the record was randomized. When piped for display, formatted per the user's date/time preferences. Append `:value` to display the raw YYYY-MM-DD HH:MM:SS format. | 31/05/2024 5:02:15am |
| Randomization UTC Time (Raw Format) | `[rand-utc-time:value]` | The randomization UTC time in raw YYYY-MM-DD HH:MM:SS format. | 2024-05-31 05:02:15 |
| Randomization UTC Time (Specific) | `[rand-utc-time:n]` | References the UTC time for randomization `n`. | 31/05/2024 5:02:15am |
| Randomization UTC Time (Specific, Raw) | `[rand-utc-time:n:value]` | Raw format UTC time for a specific randomization. | 2024-05-31 05:02:15 |

---

## 4. Usage Notes

**Randomization Module Required**

All randomization smart variables only return values if your project has the REDCap Randomization module enabled. In a project without randomization they return blank; they never produce an error. The same applies before a record is randomized, and when `:n` refers to a randomization model the project does not have. Contact your REDCap administrator if you need to enable randomization.

**Time Formats**

When piped for display (field labels, field notes, survey text, emails, `@DEFAULT` and similar), randomization timestamp smart variables are formatted per the user's date/time preferences (configured in their REDCap profile), including seconds, e.g. `31/05/2024 4:02:15pm`. To display the raw `YYYY-MM-DD HH:MM:SS` format instead, append `:value`:
- `[rand-time:value]` → `2024-05-31 16:02:15`
- `[rand-utc-time:value]` → `2024-05-31 05:02:15`

`:value` is not required in branching logic, calculated fields, `@CALCTEXT`, report filters or Data Quality rules: these already receive the raw `YYYY-MM-DD HH:MM:SS` value. Adding `:value` there is harmless. It only changes the result in display piping.

**Server Time vs. UTC Time**

`[rand-time]` is the REDCap **server's** local time. It is not converted to the viewing user's timezone; only its display format (date order, 12/24-hour clock) follows the user's date/time preferences. `[rand-utc-time]` is the same moment expressed in UTC/GMT. They represent the same instant but in different timezones. Use the server time for user-facing display when your users share the server's timezone; use UTC if you need an absolute, timezone-independent reference. A user in another timezone sees the server's clock time, not their own.

**Multiple Randomizations**

If your project uses more than one randomization (e.g., one for initial enrollment, another for a treatment crossover):
- `[rand-number:1]` references the first randomization.
- `[rand-number:2]` references the second randomization.
- Similarly for time variables: `[rand-time:2]`, `[rand-utc-time:2]`, etc.
- The default (without a number) is randomization 1.

**Randomization Validation**

Use randomization smart variables to check whether randomization has occurred. For example, a `@CALCTEXT` field: `@CALCTEXT(if([rand-time]='', 'Not yet randomized', 'Randomized'))` displays the randomization status. Test `[rand-time]` rather than `[rand-number]` for this: in an open (dropdown/radio) model with no alternate randomization numbers, `[rand-number]` stays blank after randomization. The most reliable test is the randomization variable itself (e.g., `[rand_group]<>''`), which is filled for every randomized record. `[rand-time]` can be blank for records randomized on old REDCap versions that predate randomization timestamps.

**Common Use Cases**

Randomization smart variables are useful for:
- Showing a blinded randomization number in a confirmation email: "Your randomization number is `[rand-number]`."
- Tracking when randomization occurred: "Randomized on `[rand-time]`."
- Conditional logic: Show fields only after randomization: `[rand-time]<>''` (or test the randomization variable itself)

To display or test the allocation group, reference the randomization variable itself, not a smart variable. For example, if the randomization variable is `rand_group`: "You have been assigned to the `[rand_group]` group." (piping shows the choice label), or the branching logic `[rand_group]='2'` (logic uses the raw choice code).

**Blank Randomization Values**

If a record has not been randomized, all randomization smart variables return blank. Plan your logic to handle the not-yet-randomized case gracefully. When piped for display on a data entry form or survey, a blank value appears as an underline (`______`) unless you add the `:hideunderscore` modifier, e.g. `[rand-number:hideunderscore]`.

---

## 5. Common Questions

**Q: How do I display a record's randomization assignment in a form field or email?**

**A:** To show the allocation group, pipe the randomization variable itself in the field label, field note, or email body, e.g. "Your treatment group is: `[rand_group]`" (substitute your randomization variable's name; piping shows the choice label). Use `[rand-number]` only to show the randomization number: the blinded randomization number in a text-field model, or the alternate randomization number in a dropdown/radio model. `[rand-number]` never returns the group.

**Q: Why is `[rand-number]` blank even though the record has been randomized?**

**A:** Your randomization variable is most likely a dropdown or radio field (an open model). In an open model, `[rand-number]` returns the alternate randomization number from the allocation table, and it is blank if the allocation table was uploaded without alternate numbers. It does not fall back to the group. Pipe the randomization variable to show the group, or use `[rand-time]` to confirm that randomization happened. If the project has several randomization models, also check that `:n` points at the right one.

**Q: What is the difference between `[rand-time]` and `[rand-utc-time]`?**

**A:** Both record the moment of randomization, but in different timezones. `[rand-time]` is the REDCap server's local time; it is not shifted to the viewing user's timezone, and only its date/time format follows their profile preferences. `[rand-utc-time]` is the same moment in UTC/GMT. For most user-facing display, use `[rand-time]`. Use UTC if you need an absolute reference time.

**Q: I want to show the randomization date in a calculated field. Should I use `:value`?**

**A:** It is not required. Calculations, `@CALCTEXT`, branching logic, report filters and Data Quality rules already receive the raw `YYYY-MM-DD HH:MM:SS` value, so `if([rand-time]='', 'Not randomized', 'Randomized')` and `if([rand-time:value]='', 'Not randomized', 'Randomized')` behave the same. Adding `:value` in logic is harmless. `:value` only makes a difference in display piping (labels, field notes, emails, `@DEFAULT`), where it shows the raw format instead of the user's date/time format.

**Q: My project has two randomizations. How do I reference the second randomization?**

**A:** Append `:2` to the smart variable. For example: `[rand-number:2]` for the randomization number, `[rand-time:2]` for the time, and `[rand-utc-time:2]` for UTC. Use `:1` (or no number) for the first randomization.

**Q: Can I use randomization smart variables in branching logic?**

**A:** Yes. For example, `[rand-time]<>''` shows a field only if the record has been randomized. To show a field only for a specific allocation group, test the randomization variable itself, e.g. `[rand_group]='2'` (the raw choice code), not `[rand-number]`, which never returns the group.

**Q: What happens if randomization hasn't occurred yet?**

**A:** All randomization smart variables return blank (no error). Plan your designs to handle this case. For example, use conditional logic: `@CALCTEXT(if([rand-time]='', 'Awaiting randomization', 'Randomized'))`, hide fields using branching logic, or add `:hideunderscore` so a blank piped value does not show as an underline (`______`).

**Q: I need to track when participants were randomized. How do I display just the date (not the time)?**

**A:** Unfortunately, the randomization smart variables return the full date/time. To display only the date, you could use a calculated field with text manipulation or place the randomization time in a note and ask users to read only the date portion. Alternatively, pipe the value into a text field and manually edit if needed.

---

## 6. Common Mistakes & Gotchas

**Using randomization smart variables in projects without the Randomization module enabled.** If your project does not have the Randomization module, these smart variables silently return blank; there is no error to alert you. Confirm that your project has randomization enabled before relying on these variables.

**Expecting `[rand-number]` to return the allocation group.** It never does. In text-field (blinded) randomization, it returns the opaque randomization number (e.g., "R1-5638"), which does not reveal the group. In categorical (open) randomization, it returns the alternate randomization number from the allocation table, and is blank if none was uploaded. To display or test the group, reference the randomization variable itself (e.g., `[rand_group]`).

**Using `[rand-number]` to check whether a record has been randomized.** In an open model without alternate randomization numbers, `[rand-number]<>''` stays false after randomization. Test `[rand-time]<>''` or the randomization variable instead.

**Not accounting for blank values when randomization hasn't occurred.** If you pipe `[rand-number]` into a form or survey before a record is randomized, it displays as an underline (`______`); in an email it is simply blank. Use conditional logic or the `:hideunderscore` modifier to handle this gracefully.

**Using `:value` format in user-facing display.** In display piping, the `:value` format shows the raw YYYY-MM-DD HH:MM:SS value and ignores the user's date/time display format preference. For display, omit `:value` and let REDCap format the timestamp. In logic and calculations `:value` makes no difference, because they already use the raw value.

**Mixing up randomization time and UTC time.** `[rand-time]` is the server's time, not the user's local time; `[rand-utc-time]` is UTC. If you are storing or comparing timestamps across different timezones, use UTC. For display to users in your institution's timezone, use server time.

**Assuming multiple randomizations without verifying project setup.** If you use `[rand-number:2]` in a project with only one randomization configured, the variable returns blank. Verify that your project actually has multiple randomizations before relying on these references.

**Using randomization smart variables in Data Quality rules.** Randomization smart variables work in DQ rules, but they can slow down rule execution significantly. Avoid them in DQ rules unless absolutely necessary.

---

## 7. Related Articles

- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (overview of all smart variable categories)
- [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) (timestamp formats and modifiers)
- [RC-AT-08 — Action Tags: @IF — Conditional Logic](RC-AT-08_Action-Tags-Conditional-IF.md) (using randomization smart variables in conditional logic)
