RC-PIPE-08

**Smart Variables: Survey**

| **Article ID** | RC-PIPE-08 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types with surveys enabled |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers; RC-PIPE-07 — Smart Variables: Form; RC-PIPE-04 — Piping in Emails and Notifications |

---

# 1. Overview

Survey smart variables return information about surveys in REDCap — including survey links, access codes, timestamps for when surveys were started and completed, and the total time spent completing a survey. These variables are especially useful in survey invitation emails, confirmation messages, and field notes within surveys. Use them to dynamically generate survey URLs, reference participant progress, and personalize survey communications based on when participants engaged with the form.

---

# 2. Key Concepts & Definitions

**Survey**

A public-facing, link-based data collection instrument in REDCap. Unlike standard data entry forms (accessed by logged-in users), surveys can be distributed to participants who access the form via a unique link or QR code without a REDCap account.

**Survey Access Code**

A security token specific to each record/event/instance that grants access to a survey for that particular record. Access codes are unique per record and instrument, preventing participants from accidentally accessing another record's survey.

**Survey Return Code**

A security token that allows a participant to return to a partially completed survey (Save & Return Later feature). Return codes are different from access codes and serve a different purpose — they enable resumption of incomplete surveys.

**Survey Queue**

A feature in REDCap that displays all surveys available to a participant for a given record. The survey queue is a convenient way for participants to see and access multiple surveys associated with one enrollment.

**Survey Timestamps**

REDCap records when a survey is started, when it is completed, and how long the participant spent on the survey. These timestamps can be piped into other forms, emails, or calculated fields for tracking and follow-up purposes.

**Survey Duration**

The elapsed time from survey start to completion (or from start to current time if the survey is still in progress). Duration can be expressed in various units: seconds, minutes, hours, days, months, or years.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Is Survey | `[is-survey]` | Returns 1 if the current instrument is being accessed as a survey; returns 0 if accessed as a data entry form. Useful in branching logic. | 1 (or 0) |
| Survey URL (Current or Specified) | `[survey-url]` or `[survey-url:instrument]` | The web address (URL) for the specified survey. Can omit `instrument` when used inside a survey invitation (assumed). Can be combined with event prefix: `[previous-event-name][survey-url:followup_survey]`. | https://redcap.yourinstitution.edu/surveys/?... |
| Survey Link (Current or Specified) | `[survey-link]`, `[survey-link:instrument]`, or `[survey-link:instrument:Custom Text]` | An HTML web link to the specified survey. Multiple syntax forms supported. Custom text is optional; if omitted, defaults to the survey title. Can be used as `[survey-link:Custom Text]` when instrument is assumed, or `[survey-link]` inside a survey invitation. Can be combined with event prefix: `[next-event-name][survey-link:followup_survey]`. | Follow-up Survey or Take the pre-screening survey |
| Survey Access Code (Current or Specified) | `[survey-access-code]` or `[survey-access-code:instrument]` | The unique access code for the specified survey for the current record/event/instance. Can omit `instrument` inside a survey invitation (assumed). Can be combined with event prefix: `[previous-event-name][survey-access-code:followup_survey]`. | LDNP3EW7W |
| Survey Return Code (Current or Specified) | `[survey-return-code]` or `[survey-return-code:instrument]` | The unique return code allowing a participant to resume a partially completed survey (Save & Return Later). Can omit `instrument` in a survey invitation context. Can be combined with event prefix. | TFX4E4YN |
| Survey Queue URL | `[survey-queue-url]` | The web address (URL) of the survey queue for the current record. Displays all surveys available to the participant. | https://redcap.yourinstitution.edu/surveys/?... |
| Survey Queue Link | `[survey-queue-link]` or `[survey-queue-link:Custom Text]` | An HTML web link to the survey queue. Custom text is optional; if omitted, defaults to "Survey Queue Link". | Survey Queue Link or View your survey progress |
| Survey Title (Current or Specified) | `[survey-title]` or `[survey-title:instrument]` | The title (display name) of the specified instrument as configured in survey settings. Blank if not in an instrument/survey context. | Enter to Win a New Car or Cardiology Study: Pre-Screening Survey |
| Survey Time Started (Specified) | `[survey-time-started:instrument]` or `[survey-time-started:instrument:value]` | The date and time the specified survey was started. In piping context, displays per user's date/time preferences. Append `:value` for raw YYYY-MM-DD HH:MM:SS format (better for logic). Returns blank if survey was never started or if response began before REDCap collected start times. Can be combined with instance qualifier: `[survey-time-started:followup][last-instance]`. | 12/25/2018 09:00am or 2018-12-25 09:00:00 |
| Survey Date Started (Specified) | `[survey-date-started:instrument]` or `[survey-date-started:instrument:value]` | Date only (no time) the specified survey was started. Append `:value` for raw YYYY-MM-DD format. Can be combined with instance qualifier. | 12/25/2018 or 2018-12-25 |
| Survey Time Completed (Specified) | `[survey-time-completed:instrument]` or `[survey-time-completed:instrument:value]` | The date and time the specified survey was completed. Append `:value` for raw format. Returns blank if survey has not been completed. Can be combined with instance qualifier. | 12/25/2018 09:30am or 2018-12-25 09:30:00 |
| Survey Date Completed (Specified) | `[survey-date-completed:instrument]` or `[survey-date-completed:instrument:value]` | Date only the specified survey was completed. Append `:value` for raw format. Returns blank if not completed. Can be combined with instance qualifier. | 12/25/2018 or 2018-12-25 |
| Survey Duration | `[survey-duration:instrument]` or `[survey-duration:instrument:units]` | Time elapsed since the survey was started. Can be expressed in units: y (years), M (months), d (days), h (hours), m (minutes), s (seconds, default). For partially completed surveys in a calculated field, value keeps changing — run Data Quality rule H for accurate results. Can be combined with instance qualifier: `[visit_1_arm_1][survey-duration:prescreener][last-instance]`. | 845 or 2.34 |
| Survey Duration Completed | `[survey-duration-completed:instrument]` or `[survey-duration-completed:instrument:units]` | Total time to complete the survey (start to completion). Returns blank if survey has not been completed. Same unit options as survey-duration. | 93 or 12.7 or 3.89 |

---

# 4. Usage Notes

**Survey URL and Link Parameters**

When using `[survey-url:instrument]` or `[survey-link:instrument]`, replace `instrument` with the unique form name. You can omit the instrument parameter when the smart variable is used inside a survey invitation email (REDCap assumes the current survey).

**Custom Text in Survey Links**

Use `[survey-link:instrument:Custom Text]` to generate a link with custom text instead of the survey title. For example: `[survey-link:followup_survey:Complete the follow-up survey]`. If omitted, REDCap uses the survey's configured title.

**Event Prefixes in Longitudinal Projects**

In longitudinal projects, you can prepend an event name to a survey smart variable to reference a survey in a different event:
- `[baseline_arm_1][survey-link:demographics]`
- `[next-event-name][survey-url:visit_survey]`
- `[previous-event-name][survey-access-code:followup_survey]`

See RC-PIPE-02 for details on event prefixes.

**Survey Timestamp Formats**

By default, survey timestamps display per the logged-in user's date/time preferences. To get a raw `YYYY-MM-DD HH:MM:SS` format suitable for calculations or logic, append `:value`:
- `[survey-time-started:instrument:value]` → `2018-12-25 09:00:00`
- `[survey-date-completed:instrument:value]` → `2018-12-25`

Use the `:value` format when piping into calculated fields or branching logic.

**Missing Start Times**

If a survey response began before REDCap started collecting start times (in older responses), `[survey-time-started]` and `[survey-date-started]` return blank. Plan your logic accordingly when working with historical data.

**Survey Duration Units**

When specifying units for duration, use only the letter code without quotes:
- `[survey-duration:prescreener:s]` → seconds
- `[survey-duration:prescreener:m]` → minutes
- `[survey-duration:prescreener:h]` → hours
- `[survey-duration:prescreener:d]` → days

Do NOT use quotes around the unit code.

**Instance Qualifiers for Repeating Surveys**

In projects with repeating instruments, you can append instance qualifiers to survey smart variables:
- `[survey-time-started:followup_survey][last-instance]` — start time of the last instance
- `[survey-duration-completed:prescreener][current-instance]` — duration of the current instance

See RC-PIPE-10 for more on instance qualifiers.

**Dynamically Changing Duration in Calculated Fields**

If you place `[survey-duration:instrument]` in a calculated field for a survey that is still in progress, the value will change every time the record is saved. Use a Data Quality rule (Rule H) to capture the final, accurate duration once the survey is completed.

**Survey Timestamp Context**

Survey timestamps are most meaningful after a survey has been started or completed. Avoid piping survey-completion timestamps into fields that appear before the survey has been accessed; they will be blank.

---

# 5. Common Questions

**Q: How do I send a participant a link to a survey in an email invitation?**

**A:** Use `[survey-link:instrument:Custom Text]` in your email body. For example:
```
Dear participant,

Please complete the enrollment survey by clicking this link:
[survey-link:enrollment_survey:Start Enrollment Survey]

Your access code is: [survey-access-code:enrollment_survey]
```

**Q: What is the difference between `[survey-access-code]` and `[survey-return-code]`?**

**A:** The access code grants initial access to the survey. The return code allows a participant to resume a partially completed survey (Save & Return Later). Both are unique to the record/event/instance combination. Always provide both to participants in case they need to return to the survey later.

**Q: Can I use survey smart variables in branching logic?**

**A:** Yes, some survey smart variables work in logic. For example, `[is-survey]=1` shows fields only in survey mode. Timestamp and duration smart variables also work in logic, but are less commonly used there. Most branching logic uses survey smart variables for conditional display based on access context.

**Q: How do I display when a participant completed a survey in a confirmation email?**

**A:** Use `[survey-time-completed:instrument]` or `[survey-date-completed:instrument]` in your email body. For example:
```
Thank you for completing the survey on [survey-date-completed:enrollment_survey].
```

If the survey has not been completed, the variable will be blank.

**Q: I have a repeating survey. How do I reference a specific instance?**

**A:** Append an instance qualifier: `[survey-time-started:followup_survey][last-instance]` references the start time of the last instance. See RC-PIPE-10 for all instance qualifier options.

**Q: What is the survey queue, and how do I link to it?**

**A:** The survey queue displays all surveys available to a participant for a given record. Use `[survey-queue-link]` or `[survey-queue-url]` to generate a link to the queue in an email or form. This is useful if you want participants to see all their available surveys at once.

**Q: Can I use the `:value` format for survey timestamps in field labels or emails?**

**A:** Yes, but it displays the raw format (YYYY-MM-DD HH:MM:SS). If you want a formatted, human-readable timestamp for display to participants, omit `:value` and let REDCap apply the user's locale preferences. Use `:value` only in calculated fields or logic conditions.

---

# 6. Common Mistakes & Gotchas

**Omitting the instrument name when it is not assumed.** Inside a survey invitation, you can use `[survey-link]` or `[survey-access-code]` without specifying an instrument. However, in field labels, emails, and other contexts outside the invitation, you must include the instrument: `[survey-link:enrollment_survey]` not just `[survey-link]`. Omitting it will cause the smart variable to return blank.

**Confusing survey smart variables with form smart variables.** Survey variables like `[survey-link]` are for public survey access. Form variables like `[form-link]` are for data entry forms. Using the wrong type in an email or form may not produce the intended result. See RC-PIPE-07 for form smart variables.

**Not testing survey links in survey invitations.** Survey links can be long and complex. Always test survey invitations in a development environment before sending them to real participants to ensure links are valid and access codes work correctly.

**Using survey-completion timestamps before surveys are completed.** If you pipe `[survey-time-completed:instrument]` in a field that appears before participants complete the survey, it will be blank. Plan your data flow carefully and only reference completion timestamps after the survey step.

**Forgetting to append `:value` in calculated fields using survey timestamps.** Survey timestamps in formatted display mode (without `:value`) may not calculate correctly in logic or calculated fields. Always use the `:value` format when piping timestamps into calculations.

**Not accounting for blank start times in historical data.** Very old survey responses may have blank start time values because REDCap did not always collect them. If your logic relies on survey start times, handle the blank case gracefully or filter out historical data.

**Assuming survey duration is final in partially completed surveys.** In a calculated field, `[survey-duration:instrument]` for an incomplete survey changes every time the form is saved. Use Data Quality rule H to capture the final duration once the survey is submitted.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (event prefixes and instance qualifiers)
- RC-PIPE-07 — Smart Variables: Form (form-specific smart variables for comparison)
- RC-PIPE-10 — Smart Variables: Repeating Instruments and Events (instance qualifiers for repeating surveys)
- RC-PIPE-04 — Piping in Emails and Notifications (using survey smart variables in survey invitations)
