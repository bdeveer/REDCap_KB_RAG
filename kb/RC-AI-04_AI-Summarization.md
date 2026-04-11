RC-AI-04

**AI Summarization**

| **Article ID** | RC-AI-04 |
| --- | --- |
| **Domain** | AI Tools |
| **Applies To** | All project types; requires AI Summarization to be enabled by administrator |
| **Prerequisite** | RC-AI-01 — REDCap AI Tools: Overview & Security |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AI-01 — REDCap AI Tools: Overview & Security; RC-EXPRT-01 — Data Export: Overview & Workflow; RC-EXPRT-06 — Custom Reports: Setup & Field Selection |

---

# 1. Overview

This article explains how to use REDCap's AI Summarization feature. AI Summarization allows you to send the collected free-text data from a variable — across all records visible in a report — to your institution's AI server and receive a summary in return. This is useful for quickly understanding patterns or themes across open-ended responses without reading every record individually. The feature is accessed from within any report (including custom reports) via a purple wizard's wand icon in the column header of eligible variables. You can summarize a single variable at a time or batch-process multiple variables. This article covers eligible variable types, the single-variable and bulk summarization workflows, prompt customization, and how to save or export results.

---

# 2. Key Concepts & Definitions

## Free-Text Variable

A variable that accepts unstructured text input and has no validation rule applied. In REDCap terms, this means a Text Box or Notes Box (paragraph field) with the validation field left blank. Date fields, email fields, phone number fields, and any other text box with a validation type applied are not eligible for AI Summarization.

## Notes Box

A multi-line text area field type in REDCap. Notes boxes accept free-form text of any length and are always eligible for AI Summarization (they have no validation option).

## Wizard's Wand Icon (in Reports)

The purple icon that appears in the column header of eligible free-text variables within any report. Clicking it opens the Summarization menu for that variable. Variables that are not eligible (e.g., date fields, validated text boxes) do not display the wand icon.

## Summarize Data Button

A button at the top of a report page that opens the bulk summarization workflow, allowing you to process multiple variables in a single session rather than clicking the wand on each column individually.

## Action Text (Prompt)

The instruction sent to the AI along with the variable data. The default prompt is "Summarize the following information in 150 words or less." You can modify this per variable, save the customized prompt, and reuse it in future summarization sessions.

---

# 3. Eligible Variable Types

AI Summarization works only on free-text variables. Use the table below to determine whether a given variable qualifies.

| Variable Type | Eligible? | Notes |
|---|---|---|
| Notes Box | Yes | Always eligible; no validation option |
| Text Box (no validation) | Yes | Must have the validation field left blank |
| Text Box (date validation) | No | Any validation makes it ineligible |
| Text Box (email validation) | No | Any validation makes it ineligible |
| Text Box (number validation) | No | Any validation makes it ineligible |
| Checkboxes | No | Not free text |
| Radio buttons / dropdowns | No | Not free text |
| Calculated fields | No | Not free text |

The wand icon appears only on eligible columns in the report header. If a column does not show the wand, the variable is not a supported type.

---

# 4. Single-Variable Summarization

Use this workflow to summarize one variable at a time.

1. Navigate to any report in your project. This can be the default All Data report or a custom report you have created.
2. Locate the column header for the free-text variable you want to summarize. A purple wizard's wand icon appears in eligible column headers.
3. Click the wand icon to open the Summarization menu.
4. The Summarization menu shows two steps:
   - **Step 1** — The variable to summarize is pre-set based on the column you clicked. This cannot be changed from within the menu.
   - **Step 2** — The action text (prompt). The default is: *"Summarize the following information in 150 words or less."*
5. Click **"Execute the action"** to send the prompt and all data in that variable (across all records visible in the report) to the AI server.
6. Processing time varies based on the amount of data and current AI server load.
7. When processing is complete, the result appears in the Summarization menu.

## Modifying the prompt

To use a custom prompt instead of the default:

1. Click the **Modify** link next to the action text.
2. Edit the prompt in the text editor that opens. The AI will always include the variable data as input — your prompt guides how the AI should process it.
3. Click **"Execute the action"** to test your custom prompt.
4. If satisfied with the result, click **"Save action text"** to store this prompt for this specific variable. Saved prompts are reused automatically the next time you open the Summarization menu for that variable.

> **Note:** Keep prompts relevant to the data you are summarizing. The AI always receives the full variable data as context, so prompts asking for unrelated outputs will still produce a response but may not be useful.

---

# 5. Working with Results

Once the AI returns a response, several options are available:

**Select and copy a passage** — Click and drag to select any portion of the result text, then copy it to your clipboard.

**Copy all** — Click the copy icon in the top right of the result area to copy the entire response to your clipboard.

**Download** — Click the download icon to export the result as a Word document (.docx).

> **Important:** Closing the Summarization menu discards the result. REDCap does not automatically save AI-generated summaries. If you need to preserve the output, copy or download it before clicking Close.

---

# 6. Bulk Summarization

Use bulk summarization to process multiple free-text variables from a single report in one session.

## Step 1: Define your variable selections

1. Click the **"Summarize Data"** button at the top of the report page.
2. In the dropdown that appears, click **"Pre-select fields & compose action text."**
3. A popup opens showing all eligible free-text variables in the report.
4. Select the variables you want to summarize by checking the corresponding boxes.
   - Use **"Select all"** or **"Deselect all"** to quickly adjust your selections.
   - Adjust the action text (prompt) for any variable individually if the default is not appropriate.
5. Click **Save** to store your selections. You can return and edit these selections at any time by repeating this process.

## Step 2: Generate summaries

After saving your selections, REDCap offers to take you directly to the generation step. You can also return to it later:

1. Click **"Summarize Data"** at the top of the report.
2. Click **"Generate data summaries using AI."**

> **Note:** The "Generate data summaries using AI" option is grayed out until you have saved a selection in Step 1. Complete the pre-selection step first.

3. The bulk summarization menu displays all selected variables with an "Execute the action" button next to each.
4. Choose one of two approaches:
   - Click **"Execute the action"** on an individual variable to generate its summary on demand.
   - Click the green **"Summarize All"** button to trigger the AI for all selected variables at once.
5. REDCap processes and displays results as they come in.
6. Copy or download individual results the same way as in the single-variable workflow.

> **Important:** Closing the bulk summarization menu discards all unsaved results. Copy or download summaries before closing.

---

# 7. Common Questions

**Which variable types can be summarized?**
Only free-text variables without validation: Notes Boxes (always eligible) and Text Boxes with no validation type applied. Any field with a validation rule — including dates, emails, numbers, and phone numbers — is not eligible. Structured field types (checkboxes, dropdowns, radios, calculated fields) are also not eligible.

**Can I summarize data from a filtered report?**
Yes. The AI receives only the data visible in the current report. If you apply filters to a custom report, only matching records are included in the summarization. This makes custom reports a powerful way to scope your summarization (e.g., summarize only records from a specific site or time period).

**How do I save a custom prompt so I don't have to re-enter it each time?**
After modifying the action text, click "Save action text." The prompt is saved for that specific variable and pre-filled automatically the next time you open the Summarization menu for it.

**What happens if I close the Summarization menu without saving?**
The result is discarded. REDCap does not persist AI-generated summaries automatically. Always copy or download your result before closing.

**Can I summarize the same variable multiple times with different prompts?**
Yes. You can modify the prompt, run "Execute the action," review the result, and repeat with a new prompt. Only one prompt is saved per variable (the last one you saved with "Save action text"), but you can run unsaved prompts interactively without overwriting the saved version.

**Why is the "Generate data summaries using AI" option grayed out?**
You must complete the pre-selection step first (click "Summarize Data" → "Pre-select fields & compose action text" → select fields and save). Once selections are saved, the generate option becomes active.

**How long does summarization take?**
Processing time depends on the amount of text data in the variable (number of records and text length per record) and the current load on your institution's AI server. Large datasets with many free-text records may take several minutes.

---

# 8. Common Mistakes & Gotchas

**Closing the menu before saving the result.** REDCap does not save AI summaries automatically. If you close the Summarization menu — whether the single-variable or bulk version — without first copying or downloading the output, you must regenerate it. Make it a habit to copy or download results immediately.

**Trying to summarize a validated text box.** A text box with any validation type (date, email, number, phone, etc.) is not eligible for summarization, even though it appears to accept text. Only text boxes with no validation and notes boxes are eligible. If the wand icon does not appear on a column, the variable type is not supported.

**Not using reports to scope the summarization.** By default, a report shows all records. If you want to summarize only a subset — for example, responses from a specific arm or time period — set up a custom report with the appropriate filters before running the summarization. The AI only sees data that appears in the report.

**Sending very large datasets without considering processing time.** Summarizing a variable with thousands of free-text responses across many records may take a long time and could time out depending on your institution's AI server configuration. For very large datasets, consider filtering the report to a manageable subset.

---

## Related Articles

- RC-AI-01 — REDCap AI Tools: Overview & Security
- RC-AI-02 — AI Writing Tools
- RC-AI-03 — AI Translations
- RC-EXPRT-01 — Data Export: Overview & Workflow
- RC-EXPRT-06 — Custom Reports: Setup & Field Selection
- RC-EXPRT-07 — Custom Reports: Filtering & Ordering
