RC-PIPE-13

**Smart Variables: Randomization**

| **Article ID** | RC-PIPE-13 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with REDCap Randomization module enabled |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers |

---

# 1. Overview

Randomization smart variables expose information about a record's randomization assignment in REDCap projects using the Randomization module. They return the randomization number/allocation group assigned to the record, the date and time the randomization occurred, and the equivalent UTC timestamp. These variables are useful for personalizing forms and emails based on randomization status, validating that randomization has occurred, and tracking randomization timestamps. They are only available in projects with the Randomization module enabled.

---

# 2. Key Concepts & Definitions

**Randomization**

A process in REDCap that automatically assigns records to study groups (arms, treatment arms, or allocation groups) based on a pre-configured randomization scheme. Randomization can occur automatically when a trigger is met or manually by a coordinator.

**Randomization Number / Allocation Group**

The assignment result of the randomization process. This may be a randomization number (for text-field randomization) or an allocation group identifier (for categorical randomization). It uniquely identifies which group the record was assigned to.

**Text-Field Randomization (Blinded Allocation)**

A randomization scheme where the allocation is stored in a text field and is opaque to the coordinator. The randomization number is typically a code like "R1-5638" that does not directly reveal the allocation group.

**Categorical Randomization (Open Allocation)**

A randomization scheme where allocation groups have meaningful names (e.g., "Control", "Treatment A", "Treatment B") and are directly visible. If allocation group numbers are uploaded, the smart variable can return the numeric ID.

**Randomization Timestamp**

The server date and time at which the record was randomized. REDCap records this automatically. Timestamps can be displayed in user-formatted or raw (YYYY-MM-DD HH:MM:SS) formats.

**UTC Time**

Coordinated Universal Time (UTC), also called GMT. REDCap records randomization in UTC and provides conversion to the user's local timezone for display purposes.

**Multiple Randomizations**

Projects can have more than one randomization scheme. The `:n` suffix (e.g., `:1`, `:2`) allows you to reference a specific randomization when multiple are in use.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Randomization Number (Default) | `[rand-number]` | The randomization number assigned to the record. For text-field randomization, equivalent to piping the randomization field. For categorical randomization, returns the number associated with the allocation group. | R1-5638 |
| Randomization Number (Specific) | `[rand-number:n]` | References randomization `n` when the project has more than one randomization. Default is n=1. | R2-4231 |
| Randomization Time (Default) | `[rand-time]` | The server date/time at which the record was randomized. In piping context, displays per user's date/time preferences. Append `:value` for raw YYYY-MM-DD HH:MM:SS format (better for logic/calculations). | 31/05/2024 4:02pm |
| Randomization Time (Raw Format) | `[rand-time:value]` | The randomization time in raw YYYY-MM-DD HH:MM:SS format, suitable for calculations and branching logic. | 2024-05-31 16:02:15 |
| Randomization Time (Specific) | `[rand-time:n]` | References the randomization time for randomization `n` when the project has multiple randomizations. | 31/05/2024 4:02pm |
| Randomization Time (Specific, Raw) | `[rand-time:n:value]` | Raw format randomization time for a specific randomization. | 2024-05-31 16:02:15 |
| Randomization UTC Time (Default) | `[rand-utc-time]` | The UTC (GMT) date/time at which the record was randomized. In piping context, displays per user's date/time preferences. Append `:value` for raw YYYY-MM-DD HH:MM:SS format. | 31/05/2024 5:02am |
| Randomization UTC Time (Raw Format) | `[rand-utc-time:value]` | The randomization UTC time in raw YYYY-MM-DD HH:MM:SS format. | 2024-05-31 05:02:15 |
| Randomization UTC Time (Specific) | `[rand-utc-time:n]` | References the UTC time for randomization `n`. | 31/05/2024 5:02am |
| Randomization UTC Time (Specific, Raw) | `[rand-utc-time:n:value]` | Raw format UTC time for a specific randomization. | 2024-05-31 05:02:15 |

---

# 4. Usage Notes

**Randomization Module Required**

All randomization smart variables only function if your project has the REDCap Randomization module enabled. Using them in projects without this module will return blank values or errors. Contact your REDCap administrator if you need to enable randomization.

**Time Formats**

By default, randomization timestamp smart variables display per the user's date/time preferences (configured in their REDCap profile). To get a raw `YYYY-MM-DD HH:MM:SS` format suitable for use in calculations or branching logic, append `:value`:
- `[rand-time:value]` → `2024-05-31 16:02:15`
- `[rand-utc-time:value]` → `2024-05-31 05:02:15`

Use the `:value` format in calculated fields, branching logic, and anywhere exact timestamps are required.

**Server Time vs. UTC Time**

`[rand-time]` is the server's local time (displayed according to the user's timezone preference). `[rand-utc-time]` is the same moment expressed in UTC/GMT. They represent the same instant but in different timezones. Use the server time for user-facing display; use UTC if you need an absolute, timezone-independent reference.

**Multiple Randomizations**

If your project uses more than one randomization (e.g., one for initial enrollment, another for a treatment crossover):
- `[rand-number:1]` references the first randomization.
- `[rand-number:2]` references the second randomization.
- Similarly for time variables: `[rand-time:2]`, `[rand-utc-time:2]`, etc.
- The default (without a number) is randomization 1.

**Randomization Validation**

Use randomization smart variables to validate whether randomization has occurred. For example, a calculated field: `if([rand-number]='', 'Not yet randomized', [rand-number])` displays the randomization status.

**Common Use Cases**

Randomization smart variables are useful for:
- Displaying the allocation group in a participant confirmation email: "You have been assigned to group `[rand-number]`."
- Personalizing instructions based on group: "As a member of the `[rand-number]` group, please..."
- Tracking when randomization occurred: "Randomized on `[rand-time]`."
- Conditional logic: Show fields only after randomization: `[rand-number]<>''`

**Blank Randomization Values**

If a record has not been randomized, all randomization smart variables return blank. Plan your logic to handle the not-yet-randomized case gracefully.

---

# 5. Common Questions

**Q: How do I display a record's randomization assignment in a form field or email?**

**A:** Use `[rand-number]` in the field label, field note, or email body. For example: "Your treatment group is: `[rand-number]`" or "You have been randomized to arm `[rand-number]`."

**Q: What is the difference between `[rand-time]` and `[rand-utc-time]`?**

**A:** Both record the moment of randomization, but in different timezones. `[rand-time]` displays in the user's local timezone (adjusted per their profile preferences). `[rand-utc-time]` displays in UTC/GMT, which is independent of timezone. For most user-facing display, use `[rand-time]`. Use UTC if you need an absolute reference time.

**Q: I want to show the randomization date in a calculated field. Should I use `:value`?**

**A:** Yes, if you are using the timestamp in a calculation or comparison. For example: `if([rand-time:value]='', 'Not randomized', 'Randomized')` requires the `:value` format. If you are only displaying the date (not calculating with it), you can use `[rand-time]` without `:value`.

**Q: My project has two randomizations. How do I reference the second randomization?**

**A:** Append `:2` to the smart variable. For example: `[rand-number:2]` for the randomization number, `[rand-time:2]` for the time, and `[rand-utc-time:2]` for UTC. Use `:1` (or no number) for the first randomization.

**Q: Can I use randomization smart variables in branching logic?**

**A:** Yes. For example, `[rand-number]<>''` shows a field only if the record has been randomized. Or `[rand-number]='R1-5638'` shows a field only if the record was assigned to a specific group.

**Q: What happens if randomization hasn't occurred yet?**

**A:** All randomization smart variables return blank. Plan your designs to handle this case. For example, use conditional logic: `if([rand-number]='', 'Awaiting randomization', [rand-number])` or hide fields using branching logic.

**Q: I need to track when participants were randomized. How do I display just the date (not the time)?**

**A:** Unfortunately, the randomization smart variables return the full date/time. To display only the date, you could use a calculated field with text manipulation or place the randomization time in a note and ask users to read only the date portion. Alternatively, pipe the value into a text field and manually edit if needed.

---

# 6. Common Mistakes & Gotchas

**Using randomization smart variables in projects without the Randomization module enabled.** If your project does not have the Randomization module, these smart variables return blank or produce errors. Confirm that your project has randomization enabled before relying on these variables.

**Confusing randomization numbers with allocation group names.** In text-field randomization, the randomization number is opaque (e.g., "R1-5638") and does not reveal the actual allocation. In categorical randomization, the number may correspond to a group (e.g., 1 = Control, 2 = Treatment). Check your randomization scheme to understand what the number represents.

**Not accounting for blank values when randomization hasn't occurred.** If you use `[rand-number]` in a form or email before a record is randomized, it displays blank. Use conditional logic or the `:hideunderscore` modifier to handle this gracefully.

**Using `:value` format in user-facing display.** The `:value` format (raw YYYY-MM-DD HH:MM:SS) is for calculations and logic, not user display. It ignores the user's timezone preferences and locale settings. For display, omit `:value` and let REDCap format the timestamp appropriately.

**Mixing up randomization time and UTC time.** `[rand-time]` is server/local time; `[rand-utc-time]` is UTC. If you are storing or comparing timestamps across different timezones, use UTC. For display to users in your institution's timezone, use server time.

**Assuming multiple randomizations without verifying project setup.** If you use `[rand-number:2]` in a project with only one randomization configured, the variable returns blank. Verify that your project actually has multiple randomizations before relying on these references.

**Using randomization smart variables in Data Quality rules.** Randomization smart variables work in DQ rules, but they can slow down rule execution significantly. Avoid them in DQ rules unless absolutely necessary.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (timestamp formats and modifiers)
- RC-AT-08 — Action Tags: Conditional IF (using randomization smart variables in conditional logic)
