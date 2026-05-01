RC-LONG-03

**Longitudinal Clinical Research Design Patterns**

| **Article ID** | RC-LONG-03 |
|---|---|
| **Domain** | Longitudinal & Repeated Setup |
| **Applies To** | Longitudinal REDCap projects in clinical research contexts |
| **Prerequisite** | RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup |
| **Version** | 1.2 |
| **Last Updated** | 2026-05-01 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup; RC-BL-05 — Branching Logic in Longitudinal Projects; RC-CALC-02 — Calculated Fields; RC-PROJ-04 — Project Setup: Additional Customizations; RC-FD-10 — Advanced Workflow Patterns |

---

# 1. Overview

This article documents design patterns observed in complex longitudinal clinical research projects — multi-event studies with validated instruments, medical record abstraction, care coordination tracking, and regulatory data management requirements. The patterns here extend the foundational setup covered in RC-LONG-01 and RC-LONG-02 and focus on recurring architectural decisions that arise when REDCap supports a full research protocol lifecycle.

These patterns are drawn from real projects and reflect tested design choices. Each pattern includes the problem it solves, how it is implemented, and the trade-offs involved.

---

# 2. Key Concepts & Definitions

**Validated Instrument**

A standardized assessment tool (e.g., a quality-of-life questionnaire, a cognitive screen) with fixed items, response scales, and scoring algorithms. In REDCap, this is typically one instrument (form) whose field names and structure must remain stable to preserve scoring integrity.

**Event Architecture**

The full sequence of events defined in a longitudinal project, representing the study timeline from screening through completion or discontinuation. The event architecture determines which instruments are collected at which time points and in what order.

**Instrument Reuse**

Assigning the same instrument to more than one event. REDCap stores a separate set of values for each event, so participants can have different responses at each time point even though the fields are identical.

**Call Log**

A repeating instrument used to track outreach attempts within a contact window. Each attempt (phone call, email, voicemail) is one instance of the repeating instrument.

**Adjudication Instrument**

A dedicated instrument used to review, confirm, or override data quality decisions — typically completed by a separate staff role after initial data entry.

**Source Document Checklist**

An instrument used to confirm that required paper or electronic source documents have been received, verified, and filed. Common in GCP-regulated studies.

**Scoring Instrument**

A standalone instrument containing only calculated fields that derive scores from responses entered in a separate assessment instrument. Separates raw item responses from computed outputs.

---

# 3. Standard Clinical Trial Event Architecture

## 3.1 The Pattern

Complex longitudinal studies typically follow a progression of distinct workflow phases. A well-tested event structure for a prospective cohort or interventional study looks like this:

| Event | Purpose |
|---|---|
| Screening | Assess eligibility; document inclusion/exclusion criteria |
| Enrollment | Obtain consent; assign participant to study |
| Baseline | Collect pre-intervention assessments and demographics |
| [Intervention/Visit events] | Collect data at defined follow-up intervals |
| Medical Abstraction | Capture clinical data from medical records |
| [N-month Follow-up] | Collect post-intervention outcomes |
| Readmission Review | Track unplanned healthcare encounters |
| Discontinuation | Document early withdrawal or loss to follow-up |

This structure separates workflow phases cleanly. Each event has a defined role and a distinct set of instruments. Instruments are not duplicated across events unnecessarily — the same instrument is reused where the same data needs to be collected at multiple time points (see Section 4).

## 3.2 Why Event Naming and Ordering Matter

Events are displayed in the order they appear on the Define My Events page, and this order controls the record status dashboard layout. Define events in chronological order so the dashboard reads left-to-right as a timeline.

The unique event name is generated from the event label and cannot be manually changed through the UI after creation. Choose event labels carefully before adding records — renaming an event label changes its unique event name, which breaks any branching logic or piping that references it. See RC-LONG-01 Section 2 for the naming algorithm.

## 3.3 Screening and Eligibility Exception Instruments

Projects with multi-step screening workflows often benefit from separating the primary eligibility check from protocol exceptions:

- **Screening Form** — the main inclusion/exclusion checklist. Fields are structured to gate progression (e.g., all inclusion criteria = "Yes" and all exclusions = "No" to proceed).
- **Eligibility Exception Instrument** — a separate form for documenting cases where a participant was enrolled despite not fully meeting standard criteria (e.g., a medically justified exception approved by a coordinating center). This form is completed only when an exception applies, preventing exception fields from cluttering the main screening form.

Branching logic on the eligibility exception instrument should be set to show only when a flag on the screening form indicates an exception was granted.

## 3.4 Discontinuation Event

A dedicated Discontinuation event (placed last in the event sequence) provides a structured place to record why a participant left the study early. Common fields include:

- Reason for discontinuation (dropdown: withdrew consent, lost to follow-up, deceased, physician decision, other)
- Date of discontinuation
- Date of last contact
- Whether any final data collection was completed

Placing this in its own event (rather than in a miscellaneous field on a visit form) makes it easy to filter for discontinued records in reports and exports, and avoids contaminating follow-up data with withdrawal metadata.

---

# 4. Reusing Validated Instruments Across Events

## 4.1 The Pattern

The same instrument can be assigned to multiple events. REDCap stores a separate, independent set of values for each event, so assigning an instrument to Baseline and to a 6-Month Follow-up event creates two separate data collection instances with no shared storage.

This is correct behavior by design. It means you do not need to create `phq_baseline` and `phq_followup` as separate instruments — a single `physician_health_questionnaire` instrument assigned to both events is cleaner and easier to maintain.

## 4.2 When to Reuse

Reuse an instrument across events when:
- The fields, labels, and response options are **identical** at each time point
- The intent is to measure the **same construct** at multiple time points for longitudinal comparison
- The instrument represents a **validated scale** whose field structure must not change

Do **not** reuse an instrument across events when:
- The time points require meaningfully different fields or response options
- The instrument needs to capture context-specific data that differs per visit (create a separate event-specific instrument instead)

## 4.3 Instrument-Event Mapping

Assign instruments to events via Project Setup → Define My Events → Designate Instruments for My Events. Any instrument can be assigned to any subset of events. There is no limit on how many events can share the same instrument.

When a validated instrument is reused across events, keep these conventions:
- Do not rename the instrument between events — it is the same instrument
- Do not add or remove fields between time points in production — scoring algorithms depend on field consistency
- Use branching logic at the event level (e.g., `[event-name] = 'baseline_arm_1'`) only when a question is genuinely applicable to one time point only

## 4.4 Cross-Event Calculated Fields

When the same instrument appears at multiple events, calculated fields in later events can reference earlier event values using the `[event_name][field_name]` syntax. This enables change-score calculations:

```
[baseline_arm_1][phq_total] - [6_month_followup_arm_1][phq_total]
```

See RC-BL-05 for the full syntax rules for cross-event references, and RC-CALC-02 for calculated field behavior.

---

# 5. Contact Log as a Repeating Instrument

## 5.1 The Problem

Follow-up data collection in clinical research rarely happens in a single contact. Staff may make multiple phone calls, leave voicemails, send letters, or reach out via proxy before completing an interview or confirming a participant's status. Tracking these attempts is required for protocol adherence documentation, but embedding attempt fields directly on the follow-up instrument creates a messy and fixed-count structure.

## 5.2 The Pattern

Create a lightweight standalone repeating instrument — a **call log** — and assign it to the relevant follow-up event. Each contact attempt is one instance of the repeating instrument. Staff create a new instance for each outreach attempt and record:

- Date and time of attempt
- Contact method (phone, letter, email, proxy contact)
- Outcome (reached participant, left voicemail, no answer, wrong number, deceased)
- Staff initials or username
- Notes

The actual follow-up assessment lives on a separate, non-repeating instrument in the same event. The call log and the interview instrument are distinct — one tracks attempts, the other captures research data.

## 5.3 Setup

1. Create the call log instrument with the fields above.
2. Assign it to the follow-up event(s) where it applies.
3. Go to Project Setup → Repeating Instruments and Events → enable the call log instrument as a repeating instrument within that event.
4. Set a custom form label that pipes the date and outcome so instances are identifiable on the record dashboard (e.g., `[contact_date] — [contact_outcome]`).

See RC-LONG-02 Section 6 for repeating instrument setup details and RC-LONG-02 Section 3 for guidance on using a repeating instrument (rather than a repeating event) when only one instrument within an event needs to repeat.

## 5.4 Why Not a Repeating Event?

A repeating event would repeat all instruments in the event together — including the follow-up assessment instrument. That is not the goal here: you want unlimited contact attempts tracked independently, while the assessment itself is completed once (when contact succeeds). A single repeating instrument within a non-repeating event achieves exactly this.

---

# 6. Adjudication Instruments

## 6.1 The Pattern

Some data collection workflows require a second-stage review of entered data — for example, confirming a clinical endpoint, adjudicating whether an event meets protocol-defined criteria, or reconciling discrepancies between data sources. An **adjudication instrument** handles this review as a separate, role-restricted form.

## 6.2 Structure

A typical adjudication instrument contains:

- Read-only or piped display of the original data being reviewed (using piping or @CALCTEXT to pull in key values from the primary instrument)
- A decision field: adjudicator's ruling (dropdown or radio: confirmed, not confirmed, needs further review)
- Date of adjudication
- Adjudicator identity (staff field or @USERNAME)
- Notes field for rationale

The adjudication instrument is assigned to the same event as the primary data instrument. User rights can restrict which users see the adjudication instrument (via instrument-level user access settings), keeping it accessible only to authorized staff.

## 6.3 Data Separation

Keeping adjudication on its own instrument rather than appending adjudication fields to the primary instrument avoids mixing raw data entry with reviewed conclusions. This matters for:

- Data exports (analysts can query adjudicated status without parsing primary fields)
- Audit clarity (the primary instrument's completion status reflects data entry, not adjudication)
- Role separation (data entry staff and adjudicators may be different people)

---

# 7. Source Document Checklist Instruments

## 7.1 The Pattern

In GCP-regulated or sponsor-monitored studies, staff must verify that required source documents (consent forms, medical records, lab results, signed paper forms) have been received and are on file. Rather than embedding checklist fields across multiple instruments, a dedicated **source document checklist instrument** centralizes this tracking.

## 7.2 Structure

A source document checklist instrument typically contains:

- One checkbox or yes/no field per required document type (e.g., "Signed consent form received", "Hospital discharge summary obtained")
- Date fields for when each document was received or verified
- A notes field for exceptions or pending items
- A staff-verified-by field (@USERNAME or text)

Multiple checklists may exist for different phases: one for consent and baseline documents, one for medical record abstraction documents. Each is its own instrument assigned to the appropriate event.

## 7.3 Why a Separate Instrument

- Source document tracking is operational, not scientific — it should not appear in data exports used for analysis
- Instrument-level completion status (complete/incomplete) provides a clear monitoring signal independent of the scientific data
- A monitor or coordinator can review checklist completion on the record status dashboard without opening the primary data forms

---

# 8. Separate Scoring Instruments

## 8.1 The Pattern

Validated multi-item instruments (e.g., SF-12, PHQ-9, ESAS) involve complex scoring algorithms that produce summary scores (subscales, total scores, component summaries). These scores can be computed as calculated fields directly on the assessment instrument — or they can be placed in a **dedicated scoring instrument**.

A dedicated scoring instrument contains only calculated fields. No data entry happens there. It is assigned to the same events as the assessment it scores.

## 8.2 When to Separate Scores

| Approach | When to use |
|---|---|
| **Scores on the assessment instrument** | Simple instruments; scores are few and immediately useful to data entry staff during the session |
| **Separate scoring instrument** | Complex scoring with many intermediate calculations; scoring logic may be updated independently of item text; analysts need a clean scores-only export slice |

## 8.3 Benefits of Separation

- **Maintainability** — if the scoring algorithm needs revision (e.g., a missing-item imputation rule changes), only the scoring instrument's calculated fields need updating; the item instrument is untouched
- **Export clarity** — a separate instrument gives analysts a single export target for all computed scores without having to filter out raw items
- **Data entry clarity** — staff completing the assessment see only items to fill in; scoring fields do not clutter the form
- **Completion status** — the scoring instrument's completion status (always "incomplete" until all inputs are available) does not interfere with the assessment instrument's completion status

## 8.4 Implementation Notes

Calculated fields in the scoring instrument reference fields on the assessment instrument using standard bracket notation. In a longitudinal project, since both instruments are in the same event, no cross-event reference syntax is needed — `[phq9_item1]` resolves to the current event's value automatically.

If the scoring instrument is assigned to multiple events (the same events as the assessment), calculations for each event automatically resolve to that event's item values. No per-event adjustments to the formula are needed.

---

# 9. Adverse Event Log as a Repeating Instrument

## 9.1 The Problem

Interventional studies must track adverse events (AEs) throughout the study period. Each event is discrete — it has its own onset date, severity grade, relationship to study treatment, and outcome. The number of AEs per participant is unpredictable. Embedding fixed AE fields directly on a visit instrument (e.g., `ae1_date`, `ae2_date`, `ae3_date`) caps the number that can be recorded, creates mostly-blank data, and makes reporting queries awkward.

## 9.2 The Pattern

Create a dedicated **adverse event log** instrument and configure it as a repeating instrument within each follow-up event. Each AE is one instance. Staff open a new instance for each event to report.

A typical AE log instrument contains:

- Onset date (date field, `date_mdy`)
- Brief description (text field)
- Severity grade (radio: Mild / Moderate / Severe / Life-threatening)
- Relationship to study (radio: Unrelated / Unlikely / Possible / Probable / Definite)
- SAE criteria checklist (checkbox: Hospitalization / Prolonged hospitalization / Permanent disability / Life-threatening / Death) — **display conditionally**, only when severity is Severe or Life-threatening
- Outcome (radio: Resolved / Resolving / Ongoing / Fatal / Unknown)
- Date resolved (date field) — display conditionally when outcome = Resolved
- SAE report submitted to sponsor (yes/no) — display conditionally when SAE criteria are met or severity is Life-threatening
- Date report submitted (date field) — display conditionally when report submitted = Yes
- Action taken (notes field)

Set a custom form label that pipes the onset date and a short description (e.g., `[ae_date] — [ae_description]`) so each instance is identifiable on the record status dashboard.

## 9.3 Severity-Gated Branching Logic

The SAE criteria checklist and regulatory reporting fields should only appear when the event meets the threshold for serious classification. Branching logic on those fields follows this pattern:

```
[ae_severity] = '3' or [ae_severity] = '4'
```

Where `'3'` = Severe and `'4'` = Life-threatening. This keeps the form clean for routine AEs while surfacing the full SAE workflow only when required.

The resolution date field should appear only when the outcome indicates resolution:

```
[ae_outcome] = '1'
```

The reporting date field should appear only after the staff have confirmed a report was submitted:

```
[ae_report_submitted] = '1'
```

## 9.4 Assignment to Events

Assign the AE log instrument to every event where adverse events should be captured (typically Baseline through End of Study). Do not assign it to Screening — eligibility assessments occur before the participant is enrolled and exposed to study treatment.

Both arms in a two-arm study should have the AE log assigned to the same corresponding events. Since the instrument is shared across arms, no duplication is needed.

## 9.5 Why Not a Fixed Set of Fields?

| Approach | Limitation |
|---|---|
| Fixed fields (`ae1_date`, `ae2_date` …) | Hard cap on recordable events; sparse data; awkward to query |
| Repeating event | Repeats all instruments in the event together — visit assessments would also repeat, which is not the intent |
| **Repeating instrument (AE log only)** | Unlimited instances; clean data structure; AE log repeats independently of other visit instruments |

---

# 10. Multi-Arm Parallel-Group Study Design

## 10.1 The Pattern

Parallel-group studies (e.g., randomized controlled trials with a control arm and one or more intervention arms) are supported in REDCap by creating multiple arms with **identical event sequences**. Each arm represents one group in the study; each participant is assigned to exactly one arm at enrollment.

A two-arm RCT with arms "Control" and "Intervention" might define the following events under each arm:

| Event | Day Offset | Notes |
|---|---|---|
| Screening | 0 | Eligibility assessment |
| Baseline | 7 | Pre-intervention assessments |
| 3 Month | 90 | First follow-up |
| 6 Month | 180 | Second follow-up |
| 9 Month | 270 | Third follow-up |
| End of Study | 365 | Final assessments and study completion |

This sequence is created twice — once under Arm 1 (Control) and once under Arm 2 (Intervention). REDCap generates unique event names for each: `screening_arm_1`, `screening_arm_2`, `3_month_arm_1`, `3_month_arm_2`, and so on.

## 10.2 Instrument Assignment

Assign the same instruments to the corresponding events in both arms. Since REDCap stores data separately per event (including per-arm event), no duplication of instruments is needed:

- The same Screening instrument is assigned to both `screening_arm_1` and `screening_arm_2`
- The same PHQ-9 is assigned to all follow-up events in both arms
- The same AE log repeating instrument is assigned to all post-enrollment events in both arms

This mirrors the study protocol: both groups complete the same assessments at the same time points.

## 10.3 Branching Logic and Event References

Branching logic that references a specific event must use the arm-qualified event name. If a field on the End of Study instrument should only display for participants in the intervention arm, the logic references the intervention arm's event:

```
[redcap_event_name] = 'end_of_study_arm_2'
```

Conversely, logic that applies equally to both arms should use `or`:

```
[redcap_event_name] = 'end_of_study_arm_1' or [redcap_event_name] = 'end_of_study_arm_2'
```

In practice, most instruments in a parallel-group study do not require arm-specific branching logic — both groups complete identical assessments. Reserve event-qualified branching for fields that genuinely differ by group.

## 10.4 Arm Assignment

Participants are assigned to an arm at record creation or via a designated arm-assignment field or randomization module. Once a participant has data entered under an arm, changing their arm is possible but requires care — data entered under the old arm remains attached to those events. For randomized studies, use the REDCap Randomization module (see RC-RAND-02) rather than manual arm assignment.

## 10.5 Record Status Dashboard

In a two-arm project, the record status dashboard displays all events for both arms. For projects with many events and two arms, this produces a wide grid. Consider using custom event labels and grouping related events to keep the dashboard readable. REDCap shows only the arm the record is enrolled in — rows for other arms are greyed out.

---

# 11. Cross-Event Carry-Forward for a Repeating Instrument

## 11.1 The Problem

A repeating medication list collected at every visit requires staff to re-enter the same medications visit after visit unless the prior visit's data is brought forward automatically. REDCap does not have a built-in "copy repeating instances from last event" feature, but the combination of `@IF`, `@DEFAULT`, `[current-instance]`, `[previous-event-name]`, and instance qualifiers can replicate this behaviour.

## 11.2 The Pattern

Place a `@IF` + `@DEFAULT` expression in the **Field Annotation** column of every field on the repeating instrument. The expression checks the current instance number, looks up the matching instance from the previous event, and pre-fills the field if that prior instance had data. If it did not, the field opens blank.

For a medication name field, the annotation for a list that supports up to N instances looks like this (shown here truncated to 3 instances for readability):

```
@IF([current-instance]=1 AND [previous-event-name][med_name][1]<>'',
  @DEFAULT='[previous-event-name][med_name][1]',
  @IF([current-instance]=2 AND [previous-event-name][med_name][2]<>'',
    @DEFAULT='[previous-event-name][med_name][2]',
    @IF([current-instance]=3 AND [previous-event-name][med_name][3]<>'',
      @DEFAULT='[previous-event-name][med_name][3]',
      @DEFAULT='')))
```

Extend the nesting as far as the maximum number of instances the project needs to support.

### Smart variables used

| Smart Variable | What it resolves to |
|---|---|
| `[current-instance]` | The instance number of the repeating instrument currently open |
| `[previous-event-name]` | The unique event name of the immediately preceding event in the defined event sequence |
| `[field][N]` | The value of `field` from the Nth instance of a repeating instrument (at the referenced event) |

## 11.3 Design Details

**The `<> ''` guard** — The condition `[previous-event-name][med_name][N] <> ''` ensures the carry-forward only fires if that instance actually had data at the previous event. Without this guard, REDCap would create empty instances for every instance number up to N, even if the prior visit only had two medications. The guard means REDCap creates only as many pre-filled instances as the previous visit had.

**Defaulting "ongoing" to Yes** — For a field that tracks whether the participant is still taking the medication, the final fallback (when there is no matching prior instance) can default to `@DEFAULT='1'` (Yes/ongoing) rather than blank. This is appropriate for a medication list because any medication that appears at this visit is presumed ongoing unless the staff explicitly changes it.

**Intentionally excluding certain fields** — The end-date field (`med_end_date`) should not carry forward. A discontinuation date from a prior visit is historical; at the current visit, the field should open blank so staff actively record a new end date only if the medication has since been stopped. Omit the `@IF`/`@DEFAULT` annotation entirely from fields that should never carry forward.

**`[previous-event-name]` resolves structurally, not by completion** — The smart variable points to the immediately prior event in the defined event sequence, regardless of whether data was collected at that event. If a participant skipped the 3-month visit, the 6-month carry-forward still looks to the 3-month event — and finds nothing there. Consider whether skipped visits are expected and whether the carry-forward behavior is still acceptable when they occur.

## 11.4 The Workflow This Creates

When a coordinator opens the medication list at a follow-up visit, the instrument automatically creates one pre-filled instance per medication recorded at the previous visit. The coordinator reviews each instance, updates the dose or frequency if anything changed, marks discontinued medications as ended (which triggers the end-date field via branching logic), and adds new medications as fresh instances. Data entry becomes a review-and-update task rather than a full re-entry task.

## 11.5 Caveats

- This pattern applies only when the instrument is a **repeating instrument within a non-repeating event**. It does not work across repeating events.
- The maximum instance count supported is equal to the nesting depth you build into the `@IF` chain. A medication list designed for up to 10 concurrent medications requires 10 nested `@IF` conditions per field.
- The annotations for each field are identical in structure — only the field name changes. Build the annotation for one field, verify it, then replicate it across all carry-forward fields, substituting the field name.

---

# 12. HTML Summary Panels in Descriptive Fields

## 12.1 The Pattern

A `descriptive` field type in REDCap renders its `Field Label` content as HTML. This means you can use a descriptive field as a **styled data review panel** — placing a table of key study data pulled from earlier events directly at the top of a late-stage form. Staff see the participant's full history before they start entering data, without navigating away from the form.

A typical summary panel includes:

- Demographic and contact information piped from the baseline event
- A table of longitudinal outcome scores (one row per follow-up event)
- Colour-coded rows for threshold flags or milestones
- A brief note reminding staff to review before proceeding

## 12.2 HTML in Descriptive Fields

REDCap renders HTML markup in the `Field Label` of descriptive field types. The following are supported:

- **Structural tags**: `<div>`, `<table>`, `<tr>`, `<td>`, `<th>`, `<br>`, `<span>`
- **Inline CSS**: `style="..."` attributes on any element — including colours, padding, font sizes, borders, border-radius, and CSS gradients
- **Text formatting**: `<b>`, `<i>`, `<em>`, `<strong>`, `<small>`

The following are **not** supported or should be avoided:

- External stylesheets (`<link>`)
- `<script>` tags — REDCap strips these for security
- CSS class-based styling unless the class is defined in REDCap's own stylesheet (unreliable — use inline styles only)

Piping syntax within HTML works normally. `[event_name][field_name:modifier]` references inside an HTML attribute or tag body resolve exactly as they would in plain text.

Test descriptive field HTML in both data entry mode and survey mode. Survey mode may strip certain styling for accessibility reasons.

## 12.3 Arm-Agnostic Piping

In a two-arm longitudinal project, a field from the baseline event exists in two namespaces: `[baseline_arm_1][field]` and `[baseline_arm_2][field]`. A given participant has data in exactly one of these — the arm they were enrolled in. The other resolves to blank.

Rather than writing arm-specific branching logic on a descriptive field (which cannot use branching logic to show or hide), the two references can be **concatenated**:

```
[baseline_arm_1][field:hideunderscore][baseline_arm_2][field:hideunderscore]
```

For any given participant, one reference resolves to the field value and the other resolves to empty string (suppressed by `:hideunderscore`). The result is always the value, regardless of which arm the participant is in. This technique avoids duplicating the descriptive field or adding instrument-level branching.

The `:hideunderscore` modifier is essential here. Without it, the blank arm's reference renders as `______`, making the output appear as `value______` or `______value`.

This technique works for any element of the panel that must be arm-agnostic: demographic fields, baseline scores, any event-level variable that exists under both arms.

## 12.4 Cross-Event Score Trajectories

A summary table showing all follow-up events in rows and outcome scores in columns is built by piping each event-specific value into the corresponding table cell:

```html
<tr>
  <td>Baseline</td>
  <td>[baseline_arm_1][score_total:hideunderscore][baseline_arm_2][score_total:hideunderscore]</td>
  <td>[baseline_arm_1][score_category:hideunderscore][baseline_arm_2][score_category:hideunderscore]</td>
</tr>
<tr>
  <td>3 Month</td>
  <td>[3_month_arm_1][score_total:hideunderscore][3_month_arm_2][score_total:hideunderscore]</td>
  <td>[3_month_arm_1][score_category:hideunderscore][3_month_arm_2][score_category:hideunderscore]</td>
</tr>
```

If a visit has not yet been completed, the cell displays as empty. This is expected and informative — staff can see at a glance which visits have data.

## 12.5 Practical Considerations

- **Display only** — descriptive fields are never exported. The HTML panel is purely a review aid for data entry staff; it does not appear in data exports or reports.
- **Data dictionary editing** — a descriptive field with hundreds of characters of HTML makes manual DD editing impractical. Use the Online Designer or a template-based approach when building these fields.
- **Piping resolves at form load** — the values shown in the summary panel reflect whatever was saved at the referenced events at the time the form is opened. If a prior event is edited after the End of Study form is opened and saved, the panel will reflect the updated values on the next load.
- **Keep the HTML simple and self-contained** — inline styles, a single `<div>` wrapper, and `<table>` are the most reliable elements. Avoid deeply nested CSS that is hard to maintain.

---

# 13. Common Questions

**Q: Can I assign an instrument to every event in a project?**

**A:** Yes. There is no limit on how many events share an instrument. If an instrument is relevant at every time point (e.g., a vital signs form), assign it to all events.

**Q: Does reusing an instrument across events mean the data is shared?**

**A:** No. REDCap stores a separate, independent set of values for each event. Data entered at Baseline does not appear at 6-Month Follow-up, even if the same instrument is used. Each event has its own complete copy of the instrument's data.

**Q: Can a repeating call log instrument coexist with non-repeating instruments in the same event?**

**A:** Yes. Within a longitudinal event, you can configure individual instruments to repeat independently of others. Only the instruments explicitly designated as repeating in Project Setup → Repeating Instruments and Events will repeat; others in the same event remain non-repeating. The two cannot be mixed within a *repeating event* (where the whole event repeats), but a single instrument repeating within a non-repeating event is fully supported.

**Q: Should the adjudication instrument be a survey?**

**A:** Typically no. Adjudication is an internal staff workflow, not a participant-facing task. Keep it as a standard data entry instrument with appropriate user rights restrictions.

**Q: Can calculated fields in a scoring instrument reference items from another event?**

**A:** Yes, using the `[event_name][field_name]` syntax. This is useful for change-score calculations. See RC-BL-05 for cross-event reference syntax.

**Q: What is the best way to restrict who can see the adjudication or source document checklist instruments?**

**A:** Use instrument-level user access settings (User Rights → select a user or role → expand instrument permissions). Set the instrument to "No Access" for roles that should not see it, and "View & Edit" or "Edit Only" for authorized roles.

**Q: How do I flag a record for clinical follow-up based on a total score threshold but also on a specific safety item, regardless of total score?**

**A:** Use a `@CALCTEXT` calculated field with an `if()` expression that combines both conditions using `or`:

```
@CALCTEXT(if([total_score] >= 10 or [safety_item] = '3', 'Yes', 'No'))
```

This pattern is appropriate for validated screening instruments where a high total score indicates clinical concern, but a specific item (e.g., suicidal ideation, self-harm) should trigger follow-up on its own even when the total score falls below the threshold. The `or` condition ensures neither pathway is missed. Place this field on the scoring instrument or directly on the assessment instrument — it will auto-populate as soon as the relevant items are saved.

**Q: Why would a project have two parallel medical record abstraction instruments?**

**A:** In multi-site studies, sites may have different data elements available in their medical records, or a coordinating center may perform a second-pass abstraction using a standardized form while sites use a site-adapted version. Two instruments assigned to the same event — one per abstraction pass — keeps the site-collected data and the coordinating-center-reviewed data separate, with independent completion statuses.

---

# 14. Common Mistakes & Gotchas

**Duplicating instruments instead of reusing them.** A common mistake is creating `phq_baseline` and `phq_followup` as two separate instruments when the same `physician_health_questionnaire` instrument could simply be assigned to both events. Duplicate instruments double the maintenance burden: any field label change or branching logic fix must be applied to both copies. If the data structure at each time point is identical, use one instrument and assign it to multiple events.

**Renaming events after the project has data.** Changing an event label regenerates the unique event name. Any branching logic, piping, or calculated fields that reference the old unique event name will silently fail. Audit all logic before renaming an event in a project that has collected data.

**Putting contact log fields directly on the assessment instrument.** Projects sometimes add `call_attempt_1_date`, `call_attempt_2_date`, etc. as fixed fields on the interview instrument. This limits the number of trackable attempts and creates sparse data (most fields are blank for records reached on the first try). A repeating call log instrument is more flexible and produces cleaner data.

**Assuming the scoring instrument auto-populates.** A scoring instrument that contains only calculated fields will not show as "Complete" until all the fields it references have been saved. If a data entry user saves the assessment instrument but does not open the scoring instrument, the scoring instrument will remain "Incomplete" on the record status dashboard. This is expected behavior but can confuse staff. Document it in training materials.

**Building the carry-forward annotation without the `<> ''` guard.** Omitting the `[previous-event-name][field][N] <> ''` condition causes REDCap to generate empty pre-filled instances up to the maximum instance count, even when the previous visit had fewer entries. Always include the not-empty check so instances are only created to match what the prior visit actually had.

**Forgetting to omit carry-forward from end-date or stop-date fields.** Fields that record when something ended (a medication, a side effect) should not carry forward — the end date at a prior visit is historical, not a default for the current visit. Review every field in a carry-forward instrument and explicitly decide whether it should carry or open blank.

**Using arm-qualified piping without `:hideunderscore` in HTML panels.** When concatenating `[arm_1][field][arm_2][field]` for arm-agnostic display, the arm without data renders as `______` unless `:hideunderscore` is appended to both references. The result without the modifier looks like `value______` and is confusing to staff.

**Not assigning the AE log to all post-enrollment events.** If the AE log repeating instrument is only assigned to some events, adverse events occurring between unassigned visits cannot be logged at the correct time point. Assign the AE log to every event from Baseline (or first post-enrollment visit) through End of Study in all arms.

**Writing arm-specific branching logic for instruments that are identical across arms.** In a parallel-group study, most instruments behave the same way in both arms. Adding `[redcap_event_name] = 'baseline_arm_1'` logic to fields that should display at Baseline in both arms will silently suppress them for Arm 2 participants. Only use arm-qualified event names in branching logic when behavior genuinely differs by arm.

**Using surveys for internal adjudication or source doc checklists.** These instruments are staff-only workflows. Enabling survey mode on them exposes them to public URLs and removes the normal user rights protections. Keep internal operational instruments as standard data entry forms.

**Forgetting to set a custom form label on the call log.** Without a custom form label, all call log instances show as "Instance 1," "Instance 2," etc. with no indication of content. A label that pipes in the date and outcome (e.g., `[contact_date] — [contact_outcome]`) makes the record status dashboard immediately scannable. See RC-LONG-02 Section 6 for setup details.

---

# 15. Related Articles

- RC-LONG-01 — Longitudinal Project Setup (arms, events, and instrument designation — foundational prerequisite)
- RC-LONG-02 — Repeated Instruments & Events Setup (configuring repeating instruments; custom form labels)
- RC-BL-05 — Branching Logic in Longitudinal Projects (cross-event and arm-qualified references in branching logic)
- RC-CALC-02 — Calculated Fields (building scoring instruments and change-score formulas)
- RC-AT-06 — Autofill Action Tags (@DEFAULT and [previous-event-name] — foundational building blocks for carry-forward)
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE (implementing score-based category labels and clinical flags)
- RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers (`:hideunderscore` modifier and event-qualified references)
- RC-PIPE-10 — Smart Variables: Repeating Instruments and Events ([current-instance] and instance qualifier syntax)
- RC-RAND-02 — Randomization Setup Guide (using the Randomization module for arm assignment in RCTs)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (HTML in field labels)
- RC-PROJ-04 — Project Setup: Additional Customizations (custom record label using piped patient identifiers)
- RC-FD-10 — Advanced Workflow Patterns: Multi-Stage Review and Operational Processing (adjudication and multi-stage review patterns)
