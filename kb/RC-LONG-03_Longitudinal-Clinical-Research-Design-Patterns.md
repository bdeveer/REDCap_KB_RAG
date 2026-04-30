RC-LONG-03

**Longitudinal Clinical Research Design Patterns**

| **Article ID** | RC-LONG-03 |
|---|---|
| **Domain** | Longitudinal & Repeated Setup |
| **Applies To** | Longitudinal REDCap projects in clinical research contexts |
| **Prerequisite** | RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup |
| **Version** | 1.0 |
| **Last Updated** | 2026-04-29 |
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

# 9. Common Questions

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

**Q: Why would a project have two parallel medical record abstraction instruments?**

**A:** In multi-site studies, sites may have different data elements available in their medical records, or a coordinating center may perform a second-pass abstraction using a standardized form while sites use a site-adapted version. Two instruments assigned to the same event — one per abstraction pass — keeps the site-collected data and the coordinating-center-reviewed data separate, with independent completion statuses.

---

# 10. Common Mistakes & Gotchas

**Duplicating instruments instead of reusing them.** A common mistake is creating `phq_baseline` and `phq_followup` as two separate instruments when the same `physician_health_questionnaire` instrument could simply be assigned to both events. Duplicate instruments double the maintenance burden: any field label change or branching logic fix must be applied to both copies. If the data structure at each time point is identical, use one instrument and assign it to multiple events.

**Renaming events after the project has data.** Changing an event label regenerates the unique event name. Any branching logic, piping, or calculated fields that reference the old unique event name will silently fail. Audit all logic before renaming an event in a project that has collected data.

**Putting contact log fields directly on the assessment instrument.** Projects sometimes add `call_attempt_1_date`, `call_attempt_2_date`, etc. as fixed fields on the interview instrument. This limits the number of trackable attempts and creates sparse data (most fields are blank for records reached on the first try). A repeating call log instrument is more flexible and produces cleaner data.

**Assuming the scoring instrument auto-populates.** A scoring instrument that contains only calculated fields will not show as "Complete" until all the fields it references have been saved. If a data entry user saves the assessment instrument but does not open the scoring instrument, the scoring instrument will remain "Incomplete" on the record status dashboard. This is expected behavior but can confuse staff. Document it in training materials.

**Using surveys for internal adjudication or source doc checklists.** These instruments are staff-only workflows. Enabling survey mode on them exposes them to public URLs and removes the normal user rights protections. Keep internal operational instruments as standard data entry forms.

**Forgetting to set a custom form label on the call log.** Without a custom form label, all call log instances show as "Instance 1," "Instance 2," etc. with no indication of content. A label that pipes in the date and outcome (e.g., `[contact_date] — [contact_outcome]`) makes the record status dashboard immediately scannable. See RC-LONG-02 Section 6 for setup details.

---

# 11. Related Articles

- RC-LONG-01 — Longitudinal Project Setup (arms, events, and instrument designation — foundational prerequisite)
- RC-LONG-02 — Repeated Instruments & Events Setup (configuring the call log repeating instrument)
- RC-BL-05 — Branching Logic in Longitudinal Projects (cross-event references in branching logic and calculated fields)
- RC-CALC-02 — Calculated Fields (building scoring instruments and change-score formulas)
- RC-PROJ-04 — Project Setup: Additional Customizations (custom record label using piped patient identifiers)
- RC-FD-10 — Advanced Workflow Patterns: Multi-Stage Review and Operational Processing (adjudication and multi-stage review patterns)
