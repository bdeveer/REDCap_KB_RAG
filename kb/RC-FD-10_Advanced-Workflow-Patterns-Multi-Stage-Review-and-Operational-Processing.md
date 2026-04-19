RC-FD-10

**Advanced Workflow Patterns: Multi-Stage Review and Operational Processing**

| **Article ID** | RC-FD-10 |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; surveys enabled; Project Design and Setup rights |
| **Prerequisite** | RC-FD-09 — Field Embedding: Advanced Layout Patterns & Workflow Design |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-09 — Field Embedding: Advanced Layout Patterns & Workflow Design; RC-AT-06 — Autofill Action Tags; RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE; RC-PIPE-04 — Piping in Emails and Notifications; RC-PIPE-08 — Smart Variables: Survey; RC-ALERT-01 — Alerts & Notifications: Setup |

---

# 1. Overview

This article documents design patterns from two operational demo projects — a **Grant Approval** system and an **Equipment Request** system — that extend the patterns introduced in RC-FD-09. Both projects build on field embedding and piping but add new mechanisms: editable carry-forward of data between instruments, dropdown-driven auto-population of related fields, inline display of uploaded documents, multi-reviewer parallel workflows, a checkbox-gated email preview selector, staff-facing operational instruments, and checkbox-triggered Alerts with self-documenting labels.

Each pattern is documented with the design goal, how it works, and the specific syntax involved.

---

# 2. Key Concepts & Definitions

**`@DEFAULT`**

An action tag that pre-fills a field with a value when the record is first loaded on that instrument. Unlike piping (which displays a value read-only in a label), @DEFAULT writes a value into an editable field — the user can change it. Accepts a hard-coded value, a piped field reference, or a smart variable.

**`@CALCTEXT`**

An action tag that computes a text value from a logic expression and populates a text field with the result. The field is not editable by the user; it updates when its source fields change. Commonly used with nested `if()` functions to implement lookup-style behavior.

**`[file:inline]`**

A piping modifier applied to a file-type field that embeds the uploaded file's content directly inside the rendered page — the file renders visually in place (typically as a PDF viewer or image). Used in descriptive field labels to let reviewers read uploaded documents without leaving the REDCap page.

**`[file:link]`**

A piping modifier applied to a file-type field that renders as a clickable hyperlink to download or open the uploaded file. Does not embed the file content — just provides access via a link.

**`[form-link:instrument:Custom Text]`**

A smart variable that renders as a clickable hyperlink to a specific data entry **form** (not a survey) for the current record. Requires the recipient to be a logged-in REDCap user. Contrast with `[survey-link:]`, which links to a public survey accessible without a REDCap account.

**Parallel Reviewer Instruments**

A design pattern in which multiple identical instruments (e.g., `review_1`, `review_2`, `review_3`) each collect an independent review of the same submission from a different reviewer. Each instrument has its own survey link, and variable names are indexed (e.g., `revd1`, `revd12`, `revd123`) to keep them distinct. This is a workaround for the lack of separate-respondent repeating instruments in REDCap's standard project structure.

**Display-Then-Act Instrument**

An instrument that opens with piped read-only context tables showing the requester's submission, followed by action fields (checkboxes, date fields, notes) where the processor records what they did. The context tables have no input elements — all the data was entered elsewhere. The action fields are what the processor fills in.

---

# 3. Pattern 1 — @DEFAULT for Editable Cross-Instrument Data Carry-Forward

## 3.1 The Problem @DEFAULT Solves

In the grant approval workflow, applicants submit basic application data (project name, PI info, IRB number) through the `application` instrument. Before routing to reviewers, an administrator reviews and potentially corrects this data in the `request_info` instrument. The administrator's copy must be editable — piping (`[pname]` in a label) is read-only and won't work. @DEFAULT is the right tool.

## 3.2 How It Works

On the `request_info` instrument, parallel fields exist for each key application value:

| Application field | Request info field | @DEFAULT annotation |
|---|---|---|
| `pname` | `pname1` | `@DEFAULT="[pname]"` |
| `pifname` | `pifname1` | `@DEFAULT="[pifname]"` |
| `pilname` | `pilname1` | `@DEFAULT="[pilname]"` |
| `piemail` | `piemail1` | `@DEFAULT="[piemail]"` |
| `irb` | `irb_read` | `@DEFAULT="[irb]"` |

When the administrator opens `request_info` for the first time for a given record, each field auto-fills from the corresponding application field. The fields are fully editable — the admin can correct typos, normalize formatting, or update details before routing to reviewers.

## 3.3 Why @DEFAULT and Not Piping

| Mechanism | Syntax | Editable? | Use when |
|---|---|---|---|
| Piping | `[pname]` in a label | No — display only | Showing context a recipient should read |
| @DEFAULT | `@DEFAULT="[pname]"` in annotation | Yes — user can change it | Carrying data to a form where it may need correction |

The practical impact: the `pname1` value (from request_info) becomes the authoritative project name for all downstream instruments — reviewer forms, summary tables, and outcome emails all pipe `[pname1]`, not the original `[pname]`. If the admin corrects a typo in `pname1`, the correction propagates everywhere.

## 3.4 @DEFAULT Behavior Notes

- @DEFAULT writes the value only when the field is **blank**. If the field already has a saved value, @DEFAULT does not overwrite it.
- If the source field (`[pname]`) is blank when `request_info` is first opened, @DEFAULT pre-fills with a blank — effectively doing nothing. Ensure the source instrument is complete before the admin opens the downstream form.
- The downstream fields (`pname1`, `pifname1`, etc.) should be marked as Identifiers if they carry PHI — the same PHI rules that apply to the originating fields apply here.

---

# 4. Pattern 2 — Dropdown-Driven @CALCTEXT Lookup

## 4.1 The Design Goal

The grant review workflow assigns up to three reviewers per application. Each reviewer is selected from a shared roster of five people. When an admin selects "Thor Odinson" from a dropdown, the corresponding name and email should populate automatically in adjacent fields — so the reviewer notification email can address Thor by name and route to his correct email address.

This is a lookup pattern: given a key (the reviewer code), return the associated attributes (name, email).

## 4.2 Implementation

Three fields work together per reviewer slot, and all three are embedded in the same table row:

1. **`rev1`** — dropdown; choices are the roster of reviewers (coded 1–5)
2. **`revn1`** — text field; auto-populated with the reviewer's first name via @CALCTEXT
3. **`reve1`** — text (email validation); auto-populated with the reviewer's email via @CALCTEXT

The @CALCTEXT annotation on `revn1`:

```
@CALCTEXT(if([rev1]='1',"Tony",if([rev1]='2',"Thor",if([rev1]='3',"Natasja",if([rev1]='4',"Bruce",if([rev1]='5',"Steve",""))))))
```

The @CALCTEXT annotation on `reve1`:

```
@CALCTEXT(if([rev1]='1',"tony@stark-industry.com",if([rev1]='2',"thor@asgard.nor",if([rev1]='3',"widow@redroom.ru",if([rev1]='4',"green@giant.com",if([rev1]='5',"steverogers23@aol.com",""))))))
```

This pattern repeats identically for `rev2`/`revn2`/`reve2` and `rev3`/`revn3`/`reve3`.

## 4.3 The Embedded Table Ties It Together

All nine reviewer fields are embedded in a single descriptive field (`desc0`) as a 4-column table:

```
| Reviewer Number | Reviewer (dropdown) | Name        | Email       |
|-----------------|---------------------|-------------|-------------|
| Reviewer 1      | {rev1}              | {revn1}     | {reve1}     |
| Reviewer 2      | {rev2}              | {revn2}     | {reve2}     |
| Reviewer 3      | {rev3}              | {revn3}     | {reve3}     |
```

The admin selects from the dropdown; the name and email columns fill automatically and are visible in the same row. The layout makes it immediately clear which name and email correspond to which reviewer slot.

## 4.4 Downstream Use

The computed `revn1`, `reve1` values are then piped into the reviewer notification email templates:

```
Hi [revn1],

Please review the following grant application: [pname1] ([irb_read])

[survey-link:review_1:Grant application review link]

The review is due on [ddue].
```

Each reviewer receives a personalized email addressed to them by first name, with a link to their specific review instrument. The @CALCTEXT-computed values make this possible without any external database or lookup service.

## 4.5 Limitations

- The roster is hard-coded in the @CALCTEXT expression. Adding a new reviewer requires editing the annotation on six fields (name + email for three reviewer slots). For frequently changing rosters, a dedicated roster instrument with repeated instances or a Randomization module may be more maintainable.
- @CALCTEXT fields are not editable by users. If a reviewer's email changes, the project designer must update the annotation.

---

# 5. Pattern 3 — [file:inline] and [file:link] for In-Form Document Access

## 5.1 The Problem

Grant reviewers need to read the IRB application and study protocol to make their assessment. Attaching files to emails is impractical for large PDFs and creates version-control problems if the files are updated. The solution is to display the uploaded files directly inside the reviewer's REDCap survey.

## 5.2 [file:inline] — Embedding a File in Place

In each review instrument (`review_1`, `review_2`, `review_3`), two descriptive fields use the `:inline` modifier:

```
IRB application
[irbfile:inline]
```

```
Study Protocol
[protocol:inline]
```

The `:inline` modifier tells REDCap to render the file's content directly in the page — typically as a PDF viewer embedded in the instrument. The reviewer reads the document without navigating away from their review form.

**Syntax:** `[file_field_variable:inline]`

**Behavior:** The inline rendering depends on the file type and the browser. PDFs typically display in an embedded PDF viewer. Images display inline. Other file types may display a download prompt instead.

## 5.3 [file:link] — Providing a Download Link

A separate descriptive field provides fallback download links for all three uploaded documents:

```
Uploaded document links:

IRB application
[irbfile:link]
Study Protocol
[protocol:link]
Other documents
[otherdocs1:link]
```

The `:link` modifier renders as a hyperlink labeled with the uploaded filename. Clicking opens or downloads the file.

**Syntax:** `[file_field_variable:link]`

**Use case:** Provide download links when inline display is not ideal (large files, non-PDF formats, or users who prefer to open files in a separate application). Using both `:inline` and `:link` in the same instrument gives reviewers options.

## 5.4 Both Modifiers in the Same Instrument

The review instruments use both together: `:inline` for the primary reading experience and `:link` for backup access. This is the recommended pattern for document review workflows.

## 5.5 Important Constraint

Both `[file:inline]` and `[file:link]` reference the original file field from the application instrument. If no file has been uploaded to that field, the reference renders blank — no link, no viewer. Build Alert trigger conditions or instrument completion requirements to ensure files are uploaded before review forms are activated.

---

# 6. Pattern 4 — Multi-Reviewer Parallel Instruments with Summary Aggregation

## 6.1 The Design Goal

A grant review committee of three independent reviewers each needs to record a preliminary decision, an impact score, and comments — without seeing each other's responses before submitting. Then a program officer needs a side-by-side view of all three reviews.

## 6.2 Parallel Instruments

Three instruments (`review_1`, `review_2`, `review_3`) are structurally identical:

- A piped context table showing the application details
- `[file:inline]` display of the IRB application and protocol
- `[file:link]` fallback links
- A required radio decision (Approve/Reject)
- A notes field for rejection rationale, shown only if Rejected (`[revd1] = '2'`)
- A slider for impact rating (0–100), shown only if Approved (`[revd1] = '1'`)
- An optional additional comments notes field

Variable names use numeric suffixes to distinguish reviewers across instruments:

| Concept | Reviewer 1 | Reviewer 2 | Reviewer 3 |
|---|---|---|---|
| Decision | `revd1` | `revd12` | `revd123` |
| Impact score | `impact1` | `impact12` | `impact123` |
| Rejection reason | `revrej1` | `revrej12` | `revrej123` |
| Comments | `addcomm1` | `addcomm12` | `addcomm123` |

Each reviewer receives a unique `[survey-link:]` to their own instrument. Because each instrument is separate, reviewers cannot see each other's input — they are filling in different forms on the same record.

## 6.3 Reviewer Notification Emails with Named Greeting

The reviewer notification emails address each reviewer by the auto-computed `revn` value:

```
Hi [revn1],

Please review the following grant application: [pname1] ([irb_read])
[survey-link:review_1:Grant application review link]
The review is due on [ddue].
```

This pattern (from Pattern 2) means the notification is personalized and routes to the right instrument without any manual address lookup.

## 6.4 The Review Summary Table

After all three reviews are collected, the `review_summary` instrument aggregates everything into a single comparative view using a piped descriptive field (`sum1`):

```
|                      | Reviewer 1 ([rev1]) | Reviewer 2 ([rev2]) | Reviewer 3 ([rev3]) |
|----------------------|---------------------|---------------------|---------------------|
| Review decision      | [revd1]             | [revd12]            | [revd123]           |
| Impact Score         | [impact1]           | [impact12]          | [impact123]         |
| Rejection rationale  | [revrej1]           | [revrej12]          | [revrej123]         |
```

The column headers use `[rev1]`, `[rev2]`, `[rev3]` to pipe the reviewer identity (from the dropdown) directly into the table header, so the program officer sees the reviewer's name in the column, not just "Reviewer 1."

This is pure piping across instruments — all values come from fields that exist on the three review instruments, and REDCap pipes them freely since they are all in the same record.

## 6.5 Conditional Additional Comments Display

Below the summary table, three additional descriptive fields show each reviewer's free-text comments — but only if the reviewer actually entered something. This uses a non-empty text check in branching logic:

```
Variable: revcomm
Branching logic: [addcomm1] <> ""
Label:
Additional comments from Reviewer [rev1]

[addcomm1]
```

The `<> ""` condition (not equal to empty string) hides the descriptive field entirely when no comments were entered, keeping the summary clean. When comments exist, the field shows the reviewer's name (piped from `[rev1]`) and their comments (piped from `[addcomm1]`). Both the label text and the body content of the descriptive field are piped.

> **Note:** This is the only documented use of branching logic on a descriptive field where the condition tests a *different* field's content rather than a structured choice. The `<> ""` syntax works for any text or notes field.

## 6.6 Naming Convention Note

The suffix pattern (`revd1`, `revd12`, `revd123`) is unconventional but intentional — it avoids leading zeros and keeps names short. A cleaner convention would be `revd_1`, `revd_2`, `revd_3`, which is easier to maintain and extend. Either works; consistency within the project is what matters.

---

# 7. Pattern 5 — Checkbox-Gated Email Preview Selector

## 7.1 The Problem with Multi-Stage Email Previews

The equipment request workflow involves six distinct emails across the processing lifecycle:
1. Request confirmation (to requester)
2. Request notification (to processor)
3. Order confirmation (to requester)
4. Update reminder (to processor)
5. Delivery confirmation (to requester)
6. To-do reference panel (for processor)

Displaying all six previews at once in the `email_preview` instrument would be cluttered and difficult to review. The checkbox-gated selector provides a cleaner alternative.

## 7.2 How the Selector Works

A checkbox field (`egemail`) at the top of the `email_preview` instrument acts as the selector:

```
Show which example email:
[checkbox: egemail]
  1 - Confirmation email
  2 - Request notification
  3 - Order confirmation
  4 - Update reminder
  5 - Delivery confirmation
  6 - To do options
```

Each preview descriptive field has branching logic that shows it only when the corresponding checkbox is checked:

- `desc6` (Confirmation preview): `[egemail(1)] = '1'`
- `desc7` (Notification preview): `[egemail(2)] = '1'`
- `desc8` (Order confirmation preview): `[egemail(3)] = '1'`
- etc.

The selector checkbox has `@HIDESUBMIT-SURVEY` applied to it. This means opening the instrument as a survey hides the Submit button — the instrument is for review only, and the checkbox state is never "submitted" in a meaningful sense.

## 7.3 Benefits Over Static Preview Display

- **Focused review:** Designers can view one email at a time to check specific content without being distracted by others.
- **Multiple simultaneous:** Checking multiple boxes shows multiple previews at once for comparison.
- **Scalable:** Adding a seventh email type requires only adding a new checkbox choice and a new descriptive field with the corresponding branching condition.
- **Self-documenting:** The checkbox labels describe what each email is, acting as an index to the email library.

## 7.4 The State Problem

Because the checkbox field is in the record, checking boxes saves state to the record. When reviewing test records, the selector state persists between sessions. This is a minor operational quirk — the preview instrument is not intended to collect meaningful data. Keep this in mind when reviewing test records; the checkbox state from a prior review session may still be active.

---

# 8. Pattern 6 — [form-link:] for Internal Staff Routing

## 8.1 [form-link:] vs [survey-link:]

Both smart variables generate clickable links that route someone to a specific REDCap form for the current record. The critical difference is access requirements:

| Smart Variable | Syntax | Access Required | Use When |
|---|---|---|---|
| Survey link | `[survey-link:instrument:Text]` | None — public URL | Routing external participants or anyone without a REDCap account |
| Form link | `[form-link:instrument:Text]` | REDCap login required | Routing internal staff who have REDCap access |

## 8.2 Usage in the Equipment Workflow

The equipment request workflow has one externally-facing step (the requester submits via survey) and one internally-facing step (the processor opens the `process` form). The processor notification email uses `[form-link:]`:

```
Hi Jane,

We have received a new equipment request by [fname] [lname] ([email]).
Click here to view the details:

[form-link:process:Process form]
```

If `[survey-link:process:Process form]` were used instead, the link would work only if the `process` instrument is enabled as a survey. Using `[form-link:]` means the processor clicks through to the standard REDCap data entry form, which requires login and shows the form with all standard data entry features (field notes, audit trail, missing data codes, etc.).

## 8.3 When to Choose Which

Use `[survey-link:]` when:
- The recipient may not have a REDCap account
- You want the recipient to see the survey-formatted view
- The form is enabled as a survey

Use `[form-link:]` when:
- The recipient is a REDCap user (staff, coordinators, administrators)
- You want the recipient to see the full data entry interface
- The instrument is not (and should not be) a public survey

---

# 9. Pattern 7 — The Display-Then-Act Process Instrument

## 9.1 The Design Goal

The equipment `process` instrument is filled in by staff who receive the notification email. They need to see the full request before acting on it. But the request data lives on `equipment_request_survey` — the process instrument is a different form. The solution: open the process form with three purely piped read-only context tables, followed by action fields.

## 9.2 Structure

The `process` instrument has two distinct zones:

**Zone 1 — Read-only context (piped descriptive fields):**
Three descriptive fields display all request data using piped `[square bracket]` syntax:

- `desc3`: Requester info (date, name, email, program)
- `desc4`: Recipient info (name, position, start date, reason)
- `desc5`: Equipment details (laptop choice, specs, monitors, peripherals)

None of these fields have any input elements. They are pure display — mirrors of what the requester submitted, rendered in the same table format used in the confirmation email.

**Zone 2 — Action fields (data collection):**
After the context tables, the form collects:

- `order` (checkbox): "Equipment ordered? *(Selecting 'Yes' will kick off an email to the requester)*"
- `odate`: Order date
- `edate`: Expected delivery date
- `notes`: Optional notes to pipe into the confirmation email
- `deliver` (checkbox): "Equipment Delivered? *(Selecting 'Yes' will kick off an email to the requester)*"
- `process_notes`: Internal-only notes (not sent to requester)

## 9.3 Self-Documenting Field Labels

The `order` and `deliver` checkboxes use HTML in their field labels to add sub-text explaining what the action triggers:

```html
<p>Equipment ordered?<br>
<span style="font-weight: normal;">(Selecting "Yes" will kick off an email to the requester)</span></p>
```

This makes the form self-explanatory to anyone who opens it, even without training documentation. The light-weight sub-text (not bold) is visually subordinate to the main question but clearly explains the consequence of checking the box. Staff do not need to know about the Alert configuration — the form tells them what will happen.

## 9.4 Checkbox as Alert Trigger

Each checkbox (`order`, `deliver`) is the trigger condition for an Alert in the Alerts & Notifications module. When the processor checks `order` and saves, the Alert fires and sends the order confirmation email to the requester. When `deliver` is checked and saved, the delivery confirmation fires.

This is a clean separation of concerns: the processor interacts with checkboxes; the Alert engine handles the email. The processor does not need to manually compose or send anything.

## 9.5 Internal vs. External Notes Fields

`notes` (visible label explicitly says it "will be piped into the confirmation email") is intended for requester communication — it appears in the outgoing email via `[notes]`. `process_notes` (section header: "Internal Notes") is for staff-only documentation — it is never piped into any outgoing email. Naming conventions and field labels make this distinction clear within the form itself.

---

# 10. Pattern 8 — HTML Styling in Descriptive Field Content

## 10.1 Using CSS Classes for Emphasis

The grant review instruments use HTML with a CSS class to add visual emphasis to the due date:

```html
<div class="red"><center>This review is due on [ddue]</center></div>
```

The `class="red"` applies a built-in REDCap CSS class that renders the text in red. Centered and red, the due date is immediately prominent. Piped content (`[ddue]`) is resolved inside the HTML normally — the rendered result is red centered text showing the actual date.

**What this demonstrates:** Descriptive field HTML can combine standard HTML elements, inline CSS, CSS class references, and piped field values freely. The piping resolution happens after the HTML is evaluated, so `[ddue]` inside a `<div>` renders as the date value inside that div.

## 10.2 Using HTML in Choice Labels

The equipment request `laptoptype` radio field uses HTML in its choice labels to display multi-line technical specifications:

```
1, Standard Laptop PC<br><br>Dell Latitude 5550/Ultra<br>Intel Core Ultra 5 135U...
```

The `<br>` tags create line breaks within the choice label, allowing each option to display a formatted block of specifications. This is the same mechanism as embedding HTML in field labels — REDCap renders the HTML within choice label text.

**Use case:** Any radio or checkbox field where the choices need more description than a single line allows. This is cleaner than adding a separate descriptive field with the specs.

---

# 11. Common Questions

**Q: What is the difference between @DEFAULT and piping a value into a label?**

**A:** Piping (`[field]` in a label) displays a read-only value in text — the user sees it but cannot change it. @DEFAULT (`@DEFAULT="[field]"` in the annotation) writes the value into an editable input field — the user sees it pre-filled and can change it. Use piping when you want to show context; use @DEFAULT when you want to carry data forward that may need correction.

**Q: Can I use [file:inline] for any file type?**

**A:** REDCap will attempt to inline any uploaded file. PDFs and common image formats (JPEG, PNG) display reliably. Other file types (Word documents, Excel files, ZIP archives) typically render as a download prompt rather than inline content, since browsers cannot display them natively. Test with the actual file type your workflow will use before finalizing the design.

**Q: Can [file:link] and [file:inline] be used in email bodies (Alerts, ASIs, confirmation emails)?**

**A:** `[file:link]` works in email bodies — it renders as a hyperlink the recipient can click to download the file. `[file:inline]` does not work meaningfully in emails — HTML email clients cannot embed REDCap file viewers. Use `[file:link]` for email contexts and `[file:inline]` for in-instrument display only.

**Q: Why use parallel instruments (review_1/review_2/review_3) instead of a repeating instrument?**

**A:** Repeating instruments allow one person to enter multiple instances of the same form sequentially, typically by the same user or on the same session. They do not natively support routing different survey links to different people for the same instance. Parallel instruments give each reviewer their own distinct instrument with a unique survey link, ensuring true independent review. The trade-off is that adding a fourth reviewer requires creating a new instrument and duplicating all field definitions.

**Q: Does [form-link:] work in survey confirmation emails and automated survey invitations?**

**A:** Yes, technically — the link will be generated and will appear in the email. However, since the recipient is typically an external survey participant without a REDCap account, they will be prompted to log in when they click it. For recipients who are REDCap users (staff, coordinators), `[form-link:]` in an Alert works as intended. For external participants, always use `[survey-link:]`.

**Q: Can the [addcomm1] <> "" branching condition cause issues if addcomm1 contains only whitespace?**

**A:** Yes. A field containing only spaces or tab characters is not considered empty — the `<> ""` condition evaluates to true, and the descriptive field will display even though the content is effectively blank. If this is a concern, avoid the pattern for fields where whitespace-only entries are plausible, or use Alert-based data validation to prevent them.

**Q: Can I put @CALCTEXT on a field that is also embedded in a table?**

**A:** Yes. @CALCTEXT fields can be embedded using curly-brace syntax just like any other text field. In the reviewer table pattern, `{revn1}` and `{reve1}` are embedded in the table while simultaneously being driven by @CALCTEXT. The calculation updates when the dropdown (`rev1`) changes, and the new value displays in the table cell.

---

# 12. Common Mistakes & Gotchas

**Using @DEFAULT when piping was intended.** If a field uses @DEFAULT to carry data from a prior instrument, anyone who opens the form can modify the pre-filled value. If the data should be read-only context (for display only), use a piped descriptive field instead. Reserve @DEFAULT for situations where the downstream user legitimately needs to be able to correct or update the value.

**Relying on @DEFAULT when the source field may be blank.** @DEFAULT pre-fills from the source at form load time. If the source field has not been filled in yet, @DEFAULT writes a blank — which is indistinguishable from the user clearing the field. Build in completion requirements or trigger conditions to ensure source data exists before downstream forms open.

**Assuming [file:inline] will render all file types.** Non-PDF, non-image file types typically cannot be displayed inline by a browser. If your workflow involves Word documents or other office formats, use `[file:link]` instead of `[file:inline]`, or supplement with both.

**Forgetting that [file:link] and [file:inline] require the file to exist.** If the file upload field is empty (no file has been uploaded), the reference renders blank — no link text, no viewer. This is silent — there is no error message. Build workflow conditions to ensure files are uploaded before downstream forms that reference them are opened.

**Hard-coding email addresses in @CALCTEXT lookup expressions.** When a reviewer changes email address, the @CALCTEXT expression on multiple fields must be updated manually. For projects with frequently changing rosters, consider maintaining reviewer information in a separate lookup instrument and using smart variables or piping to pull it, rather than hard-coding in action tag expressions.

**Sending [form-link:] to external participants.** External participants clicking a form-link will hit a login screen they cannot pass. Only use [form-link:] in emails addressed to logged-in REDCap users. Use [survey-link:] for anything going to external or non-REDCap recipients.

**The checkbox-gated preview selector persists its state.** The `egemail` selector checkbox saves its state to the record like any other field. After a design review session, the checkbox state may need to be cleared manually. This is cosmetic and harmless, but can be confusing when revisiting a test record.

**Duplicating review instruments without updating all variable references.** When `review_2` and `review_3` are created by copying `review_1`, every field reference (branching logic, action tag expressions, embedded field names) must be updated to the correct suffix. Missing a reference means the wrong field is shown, calculated, or embedded. Do a full review of every field in copied instruments before testing.

---

# 13. Related Articles

- RC-FD-09 — Field Embedding: Advanced Layout Patterns & Workflow Design (prerequisite; approval workflow patterns, email preview instruments, dual syntax)
- RC-AT-06 — Autofill Action Tags (@DEFAULT behavior, source/target field interactions)
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE (@CALCTEXT syntax, nested if() expressions, limitations)
- RC-PIPE-04 — Piping in Emails and Notifications (piping in Alerts and ASIs; [survey-link:] in email context)
- RC-PIPE-08 — Smart Variables: Survey ([survey-link:] and [form-link:] full reference)
- RC-ALERT-01 — Alerts & Notifications: Setup (configuring checkbox-triggered Alerts; trigger conditions)
- RC-CALC-01 — Special Functions Reference (if() and nested function syntax used in @CALCTEXT)
