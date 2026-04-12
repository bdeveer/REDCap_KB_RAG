RC-FD-09

**Field Embedding: Advanced Layout Patterns & Workflow Design**

| **Article ID** | RC-FD-09 |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; surveys enabled; Project Design and Setup rights |
| **Prerequisite** | RC-FD-07 — Field Embedding; RC-PIPE-01 — Piping Basics, Syntax & Field Types |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-07 — Field Embedding; RC-PIPE-04 — Piping in Emails and Notifications; RC-PIPE-08 — Smart Variables: Survey; RC-ALERT-01 — Alerts & Notifications: Setup; RC-AT-EM-01 — Action Tags: HIDESUBMIT |

---

# 1. Overview

This article builds on the field embedding mechanics described in RC-FD-07 and demonstrates how embedding is applied creatively in real project designs. It covers three interconnected patterns that appear frequently in operational REDCap projects: using table-based layouts with embedded calculated fields to create document-style forms; using piped descriptive fields as live email template previews during project design; and assembling a multi-instrument approval workflow that routes a requester's submission to an approver and delivers branched outcome notifications. All three patterns are illustrated using a concrete example — a Full-Time Equivalent (FTE) position request project.

The running example has four instruments:

| Instrument | Form Name | Purpose |
|---|---|---|
| FTE Request | `fte_req` | Requester fills in position details |
| Email Preview | `email_preview` | Design preview of outgoing emails |
| Approval | `approval` | Approver reviews details and records decision |
| Decision Email Preview | `decision_email_preview` | Design preview of outcome notification emails |

---

# 2. Key Concepts & Definitions

**Document-Style Table Layout**

A form design pattern in which two or more descriptive fields, each containing an HTML table with field embedding references, are used to present data-entry fields in a structured, document-like grid rather than the default question-by-question list. The table rows and column headers provide all visible labeling; individual field labels are suppressed by the embedding mechanism.

**Live Email Preview Instrument**

An instrument used purely to visualize and validate the content of outgoing email messages during project design. Fields in this instrument use standard piping (`[variable_name]`) — not embedding — so that they display current record values. Designers populate a test record, open the preview instrument, and see exactly what each email will say with real data substituted in.

**Approval Workflow**

A multi-step process in which one party (the requester) submits information, a notification routes a second party (the approver) to a separate instrument where they record a decision, and the requester receives a notification of the outcome. REDCap implements this workflow without any external tools using surveys, Alerts & Notifications, and the `[survey-link:]` smart variable.

**`[survey-link:instrument:Custom Text]`**

A smart variable that renders as a clickable hyperlink to a specific survey for the current record. It is the primary mechanism for routing approvers to the right record's approval survey from within an email notification.

**`@HIDESUBMIT-SURVEY`**

An external module action tag that hides the Submit button when an instrument is viewed as a survey. Applied to preview instruments that should be opened for review but never submitted.

---

# 3. Pattern 1 — Document-Style Table Layouts with Embedded Calculated Fields

## 3.1 The Design Goal

Standard REDCap survey layouts present one question per row. For administrative request forms — position requests, supply orders, travel approvals — this produces a form that looks like a questionnaire rather than a structured document. A table-based embedding layout presents the same fields in a grid that resembles an internal form or memo, which matches the mental model of the people filling it out and makes the form feel purpose-built.

## 3.2 How It Works

Two descriptive fields, each holding an HTML table, divide the fields into logical groups. The first table collects requester identity; the second collects the substance of the request. All data-entry fields are embedded inside table cells; they do not appear in their normal sequential position.

**First descriptive field (`desc0`) — Requester table:**

```
Requester information

| First name  | Last name  | Email   |
|-------------|------------|---------|
| {fname}     | {lname}    | {email} |
```

**Second descriptive field (`desc1`) — Request details table:**

```
Requested FTE information

| Position Title                        | {title} |
| FTE in %                              | {fte}   |
| Expected Salary (based on 100% FTE)   | {sal}   |
| Prorated expected salary              | {calc}  |
```

The underlying fields (`fname`, `lname`, `email`, `title`, `fte`, `sal`) are text fields that accept input normally — they are simply rendered inside the table cells instead of in their default sequential positions. Because they are embedded, their Field Labels are suppressed on screen, but the table's column and row headers provide equivalent context.

## 3.3 Embedding a Calculated Field in the Table

The `calc` field is a calculated field with the formula `[sal]*([fte]/100)`. It is embedded in the same second table as its source inputs (`sal` and `fte`). Because calculated fields update in real time as the user enters data, the prorated salary cell updates the moment `sal` or `fte` changes — without a page reload. The user sees the calculation directly adjacent to the inputs it depends on, in the same document context, which eliminates the need to explain the formula or place the result on a separate form section.

This is the key advantage of embedding calculated fields in context: the result appears where it is meaningful, not as a separate labeled field below the form.

## 3.4 @PLACEHOLDER as the Primary In-Cell Label

When a field is embedded in a table cell, its Field Label is suppressed. The table column or row header already provides semantic context for the column as a whole. `@PLACEHOLDER` then provides the cell-level prompt — the grayed-out hint text inside the empty input box — completing a two-tier labeling system:

- **Table header** (e.g., "First name") = column/row-level context
- **@PLACEHOLDER** (e.g., `@PLACEHOLDER="First name"`) = in-cell prompt

Example annotation for `fname`:

```
@PLACEHOLDER="First name"
```

Even though this repeats the column header, the redundancy is intentional: the placeholder disappears once the user starts typing and serves as a prompt rather than a permanent label. For fields with more specific requirements (e.g., `fte` which accepts only 0–100), `@PLACEHOLDER` carries additional instruction:

```
@PLACEHOLDER="Please enter a value between 0 to 100"
```

> **Important:** Even though the Field Label is suppressed on the instrument, always give embedded fields meaningful Field Labels. Field Labels appear in reports, exports, and the Codebook — they are the authoritative name for the field everywhere outside the instrument.

## 3.4b Reading Embedded Tables in the Codebook vs the Data Dictionary

When auditing or inheriting a project that uses table-based field embedding, be aware that the **Codebook** and the **Data Dictionary** tell very different stories about the same descriptive field.

The **Codebook** strips all HTML markup from descriptive field labels and renders only the text content. For an embedded table like the requester table in the FTE example, the Codebook shows something like:

```
Requester information First name Last name Email {fname} {lname} {email}
```

The curly-brace tokens are preserved — you can tell that `fname`, `lname`, and `email` are embedded somewhere in this field — but the table structure, column layout, cell formatting, and any HTML styling are invisible. If you see `{variable_name}` tokens in a Codebook entry, always follow up by checking the actual HTML.

The **Data Dictionary CSV** (downloaded from the project) preserves the complete raw HTML in the Field Label column, including all table markup, `<colgroup>` widths, `border` attributes, and inline styles. This is the authoritative source for understanding the layout. The **Online Designer's Rich Text Editor** shows the same content visually.

**Practical rule:** Use the Codebook to quickly identify *which* fields are embedded in a descriptive field. Use the Data Dictionary CSV or the Online Designer to understand *how* those fields are laid out.

## 3.5 The Field Order in the Data Dictionary

The physical order of fields in the Data Dictionary does not need to match the visual order in the tables. In the FTE example, `desc0` and `desc1` appear first (rows 2–3 in the DD), followed by all the data-entry fields (`fname`, `lname`, `email`, `title`, `fte`, `sal`, `calc`) in any convenient order. REDCap resolves the embedding references and renders each field in the cell where it is referenced, regardless of where it sits in the field list.

---

# 4. Pattern 2 — Piped Descriptive Fields as Live Email Template Previews

## 4.1 The Design Problem

When setting up Alerts & Notifications or confirmation emails, designers write email bodies using piping tokens (`[field_name]`) and smart variables. The challenge is that the email body is edited in a small text box with no live preview — you cannot easily verify that the email will read correctly until you configure an actual test send.

The email preview instrument pattern solves this by building the email templates directly inside the REDCap project as survey-enabled instruments, using piped descriptive fields to render live previews against actual record data.

## 4.2 How the Preview Instrument Works

The `email_preview` instrument contains two descriptive fields, each representing one outgoing email:

- **`desc3`** — the requester confirmation email
- **`desc2`** — the approver notification email

Each field's label is the full email body, written in HTML with piping tokens in place of real values:

```
Hi [fname],

Thank you for requesting the following position:

| Position Title | [title]  |
| FTE in %       | [fte] %  |
| Expected Salary | $ [sal]  |
| Prorated salary | $ [calc] |

We've notified the appropriate approver and you can expect
a decision within X business days.
```

Notice the critical syntax difference: these fields use **square brackets** (`[fname]`, `[title]`), not curly braces. Square brackets produce piping — they substitute the stored value of the field into the label text at render time. When you open this instrument for a record where `fname = "Maria"` and `title = "Research Coordinator"`, the rendered label reads exactly as the email will read when sent to that person.

To use the preview: populate a test record with realistic data, then open the `email_preview` instrument for that record. The descriptive fields render with real data substituted in. You can validate the phrasing, check that currency formatting reads correctly, confirm the table structure looks right, and iterate on the email content directly in the project — without triggering any actual sends.

## 4.3 The [survey-link:] Preview in the Approver Email

The approver notification (`desc2`) includes one line that is not just piped field data:

```
[survey-link:approval:Approval Request Form]
```

This smart variable renders as a clickable link labeled "Approval Request Form" that goes to the `approval` instrument for the current record. In the preview instrument, this link is live — clicking it navigates to the approval survey for that test record. This lets you verify that the link routes correctly before any emails are sent.

In the actual Alert or ASI email body, the same token is copied in verbatim. When the email fires for a real record, the link goes to that record's approval survey — each approver receives a unique, record-specific link.

## 4.4 @HIDESUBMIT-SURVEY on Preview Instruments

Preview instruments are meant to be read, not submitted. The `@HIDESUBMIT-SURVEY` action tag (provided by a REDCap external module; availability varies by institution) is placed on each preview descriptive field. When the instrument is accessed as a survey, the Submit button is hidden, making it clear that this is a review-only view.

> **Institutional note:** Confirm that the HIDESUBMIT external module is enabled at your institution before relying on this tag. See RC-AT-EM-01 — Action Tags: HIDESUBMIT.

---

# 5. Pattern 3 — Approval Workflow Using Cross-Instrument Piping

## 5.1 Workflow Overview

The complete approval workflow proceeds in four steps:

1. Requester completes the `fte_req` survey and submits.
2. REDCap sends a confirmation email to the requester (via Alert or confirmation email, using `desc3` as the template).
3. REDCap sends a notification email to the approver (via Alert, using `desc2` as the template) containing a `[survey-link:approval:...]` link.
4. Approver clicks the link, lands on the `approval` survey for that record, reviews piped request details, records a decision, and submits.
5. REDCap sends an outcome email to the requester based on the decision (via Alert, using one of the three templates from `decision_email_preview`).

No external routing, ticketing, or email system is required. All of this runs inside a single REDCap project.

## 5.2 Piping Request Context into the Approval Form

The first field of the `approval` instrument is a descriptive field (`desc4`) that summarizes the request the approver is deciding on:

```
Hi Bas,

[fname] [lname] ([email]) has requested the following position on [reqdate]:

| Position Title | [title]  |
| FTE in %       | [fte] %  |
| Expected Salary | $ [sal]  |
| Prorated salary | $ [calc] |

Please use the questions below to document your decision.
```

Every value here is piped from fields that the requester entered on `fte_req`. This works because both instruments belong to the same record — REDCap pipes values across instruments freely within a record. The approver opens the approval survey and immediately sees a personalized, formatted summary of what they are approving. They do not need to look elsewhere or receive any additional context document.

Note that the `calc` field — a calculated value (`[sal]*([fte]/100)`) — is piped here just like any other field. Calculated fields are fully pipeable; `[calc]` renders their computed value.

## 5.3 The Decision and Conditional Branching

The approval instrument collects three fields after the context summary:

- `dec` (radio): Approved / Approved with conditions / Rejected
- `cond` (checkbox, branching logic: `[dec] = '2'`): Conditions to attach, shown only when "Approved with conditions" is selected
- `conoth` (notes, branching logic: `[cond(4)] = '1'`): Free-text for the "Other" condition option, shown only when that checkbox is checked

This is standard branching logic — nothing unique to the approval workflow pattern. The point worth noting is that the combination of piped context + decision fields + branching produces a complete, self-contained approval record with full audit trail, all stored in the same REDCap record as the original request.

## 5.4 Outcome Emails and the Three-Template Pattern

After the approver submits, an Alert fires based on the value of `dec`. The `decision_email_preview` instrument pre-builds three email template variants, each as a separate descriptive field under its own section header:

- **`desc5` (Approval email example):** `[dec] = '1'` — "Your request for a [title] has been **approved** on [decdate]..."
- **`desc6` (Rejection email example):** `[dec] = '3'` — "Your request for a [title] has been **rejected** on [decdate]..."
- **`desc7` (Conditional approval example):** `[dec] = '2'` — "...has been **conditionally approved**... The conditions are: [cond] [conoth]"

Each template pipes in `[decdate]` (the auto-set decision date) and the requester's fields. The conditional approval template additionally pipes `[cond]` and `[conoth]` to communicate the specific conditions attached to the approval.

The three-template approach means the Alert system sends a different email body depending on the decision. In the Alert configuration, you set the trigger condition for each Alert (`[dec] = '1'`, `[dec] = '2'`, `[dec] = '3'`) and copy the corresponding template body from the preview instrument into the Alert email body. The preview instruments are the source of truth for email content during design; the Alerts are the mechanism that sends them.

---

# 6. The Dual Syntax in Context: {Curly} vs [Square]

The FTE example project is an unusually clean illustration of when to use each syntax, because both appear in the same project for the same underlying data.

| Context | Syntax | Effect |
|---|---|---|
| `fte_req` — Requester table (data entry) | `{fname}`, `{fte}`, `{calc}` | Field embedding: places the input element inside the table cell. User types into it. |
| `email_preview` — Preview emails (display) | `[fname]`, `[fte]`, `[calc]` | Piping: substitutes the stored value into the label text. Read-only display. |
| `approval` — Approver context (display) | `[fname]`, `[title]`, `[calc]` | Piping: substitutes stored values into a summary the approver reads. |

The rule: use `{curly}` when you want an interactive field to appear at that location. Use `[square]` when you want the stored value of a field to appear as text.

A common confusion is reaching for `[square]` in a descriptive field and expecting a text box to appear. It will not — square brackets produce the value, not the input control. If you need a data-entry element inside a descriptive field, you must use `{curly}` embedding.

---

# 7. Common Questions

**Q: Can I use a piping reference (`[calc]`) to display a calculated value in an email-preview descriptive field?**

**A:** Yes. Calculated fields store their result and can be piped anywhere field values can be piped — including descriptive field labels, emails, and alerts. `[calc]` renders the most recently computed result for that field in the record.

**Q: Does the [survey-link:] smart variable work inside a descriptive field on an instrument, or only in emails?**

**A:** It works in both. When placed in a descriptive field label, it renders as a clickable link when the instrument is viewed in a browser. This is how the preview instrument makes the approver link functional during testing. In an actual email, the same token inserts a real, record-specific hyperlink.

**Q: My approval instrument pipes values from the request instrument. What if the request record is not complete when the approver opens the link?**

**A:** Piping pulls the most recently saved values for each field. As long as the requester submitted the `fte_req` survey (which saves all values), the piped fields will be populated when the approver opens the approval survey. If the approval link is sent before the requester submits, the piped values will be blank. Always configure the Alert to trigger on submission of the request instrument, not on record creation.

**Q: Can I put @HIDESUBMIT-SURVEY on only one field in a multi-field instrument, or does it hide the Submit button for the whole instrument?**

**A:** The tag on any single field in the instrument is sufficient to hide the Submit button for the entire instrument when viewed as a survey. You do not need to apply it to every field.

**Q: Are the email-preview instruments accessible to respondents, or just to staff?**

**A:** They are regular instruments in the project. If they are enabled as surveys, anyone with the survey link could access them. For preview-only instruments you do not want accessible externally, either disable the survey feature for those instruments (leaving them as data-entry-only forms) or restrict access through survey queue configuration. The `@HIDESUBMIT-SURVEY` tag hides the Submit button but does not restrict access to the instrument.

**Q: Can I use this same pattern (embed for data entry, pipe for preview) on a longitudinal project?**

**A:** Yes. The embedding and piping syntaxes work identically in longitudinal projects. If you need to pipe a value from a different event into the preview or approval form, use the longitudinal piping modifier: `[event_name][field_name]`. See RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers for full coverage.

---

# 8. Common Mistakes & Gotchas

**Using curly braces in the email-preview descriptive fields.** A `{field_name}` reference in a descriptive field embeds the input element there — which is not what you want in a preview instrument. The input box will appear instead of the stored value. Use `[field_name]` (square brackets) for display in preview instruments.

**Copying the Alert email body from the preview instrument without replacing curly braces.** If any curly-brace references accidentally end up in an email body, they will render literally (e.g., `{fname}`) rather than substituting values. Email bodies support only piping syntax (`[field_name]`), not field embedding.

**Forgetting that @HIDESUBMIT-SURVEY requires an external module.** This tag is not a native REDCap action tag. If the module is not enabled at your institution, the tag is silently ignored and the Submit button remains visible on preview instruments. Verify module availability before depending on this behavior.

**Triggering the approver Alert before the request data is saved.** If an Alert fires on record creation rather than on completion of the `fte_req` instrument, the piped values in the approval email and the approval form itself will be blank. Set the Alert trigger condition to fire when `[fte_req_complete] = '2'` (instrument complete) or on the survey submit event.

**Not marking requester identity fields as Identifiers.** Fields like first name, last name, and email address that appear in the request form should be marked as Identifiers in the field settings if they contain PHI. This affects export behavior and access controls. Marking them does not prevent field embedding or piping — it only governs who can see the raw data in exports and reports.

**Assuming [survey-link:] produces a static link.** The link is record-specific and generated at render time. Copying the URL from a preview instrument to use in a manual email will link to that specific record's approval survey, not to a generic approval page. Always use the `[survey-link:]` token in the Alert body, not a copied URL.

---

# 9. Related Articles

- RC-FD-07 — Field Embedding (mechanics of curly-brace embedding, rules, common mistakes)
- RC-PIPE-01 — Piping Basics, Syntax & Field Types (square-bracket piping syntax and field type behavior)
- RC-PIPE-04 — Piping in Emails and Notifications (piping in alerts, confirmation emails, and ASIs)
- RC-PIPE-08 — Smart Variables: Survey (full reference for [survey-link:], [survey-url:], and related survey smart variables)
- RC-ALERT-01 — Alerts & Notifications: Setup (configuring trigger conditions and email bodies for the approval workflow)
- RC-AT-EM-01 — Action Tags: HIDESUBMIT (the external module tag used on preview instruments)
- RC-CALC-02 — Calculated Fields (calc field setup, formula syntax, and behavior)
