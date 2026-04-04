# RC-AI-02 — AI Writing Tools

| Field | Value |
|---|---|
| Article ID | RC-AI-02 |
| Domain | AI Tools |
| Applies To | All project types; requires AI Writing Tools to be enabled by administrator |
| Prerequisite | RC-AI-01 — REDCap AI Tools: Overview & Security |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-AI-01 — REDCap AI Tools: Overview & Security; RC-FD-02 — Online Designer |

---

## Section 1: Overview

This article explains how to use REDCap's AI Writing Tools feature. AI Writing Tools allow you to generate, edit, correct, or reformat text in any area of REDCap that uses the rich text editor — for example, field labels in the Online Designer, survey introductory text, or email bodies. The feature is accessed through a purple wizard's wand icon that appears when the rich text editor is active. You select a pre-defined action (such as "Fix Grammar" or "Change Tone"), the AI generates a suggestion, and you decide whether to accept it. This article walks through each action, the interface layout, and important behaviors to know when working with the tool.

---

## Section 2: Key Concepts & Definitions

## Rich Text Editor

A text formatting toolbar embedded in various parts of REDCap that allows styled text input (bold, italic, hyperlinks, etc.). AI Writing Tools are only available when this editor is active. In some locations — such as field labels in the Online Designer — the rich text editor must be manually enabled before the AI icon appears.

## Wizard's Wand Icon

The purple icon that opens the AI Writing Tools menu. It appears in the rich text editor toolbar when the AI Writing Tools feature is enabled. The same purple wizard's wand icon is used for AI Summarization in reports (a different feature — see RC-AI-04 — AI Summarization).

## Finalized Text Box

The upper text area in the AI Writing Tools popup. It is pre-filled with whatever text was already in the rich text editor field. You can edit this text directly before or after generating an AI suggestion.

## Suggestion from AI Section

The lower section of the AI Writing Tools popup where the AI's generated response appears after you trigger an action. You review the suggestion here before deciding whether to use it.

## [TEXT] Placeholder

A literal placeholder string you include in a custom prompt to tell the AI to use the contents of the Finalized Text box as its input. Without `[TEXT]` in a custom prompt, the AI will not consider your existing text.

---

## Section 3: Finding and Opening AI Writing Tools

### Where the feature is available

AI Writing Tools are available wherever the rich text editor can be used in REDCap. Common locations include:

- Field labels and field notes in the Online Designer
- Survey introductory and completion text
- Email bodies in Alerts & Notifications
- Project notes and instruction text fields

### Enabling the rich text editor (where required)

In some locations — particularly field labels in the Online Designer — the rich text editor is not enabled by default. Look for a toggle or button labeled to enable rich text formatting on the field. Once enabled, the toolbar appears including the purple wizard's wand icon.

### Opening the AI Writing Tools menu

Click the purple wizard's wand icon in the rich text editor toolbar. The AI Writing Tools popup opens with:

- The **Finalized Text** section (top) — contains the current field text, editable
- The **Suggestion from AI** section (bottom) — where generated responses appear

---

## Section 4: Available Actions

Each action instructs the AI to perform a specific operation on the text in the Finalized Text box. Only one action can be executed at a time — there is no batch mode within a single session.

### Fix Grammar

Checks and corrects grammar and spelling in the Finalized Text. Clicking this button sends the text to the AI and returns a corrected version in the Suggestion from AI box.

### Set Length

Rewrites the Finalized Text to make it shorter or longer. Use the controls to indicate your target length direction before clicking the button.

### Change Tone

A dropdown that lets you rewrite the text in a different register. Options include variations such as formal, conversational, professional, and others. Select the desired tone from the dropdown, then trigger the action.

### Reading Level

Rewrites the text to match a target complexity level, based on the American school grade system. Select the desired grade level and trigger the action to produce a simpler or more advanced version of the text.

### Custom Prompt

Allows you to write any instruction to the AI. Use this when none of the pre-defined actions fit your need, or when you want to combine multiple operations in a single prompt.

To reference the current contents of the Finalized Text box in your prompt, include the placeholder `[TEXT]`. Without it, the AI will not use your existing text.

Examples:
- `Fix the grammar of [TEXT] and shorten it by 25%.`
- `Translate [TEXT] into Dutch.`
- `Summarize [TEXT] in one sentence.`
- `Tell me a story based on [TEXT].`

Type your prompt in the "Custom action text" box and click "Generate Response."

> **Note:** Custom prompts are not limited to text editing tasks. You can ask the AI to do other things entirely (e.g., "Rank the top 10 TV shows in the US."), though results unrelated to your content will not use `[TEXT]`.

---

## Section 5: Working with Suggestions

Once the AI generates a response, it appears in the Suggestion from AI section. Three buttons above the suggestion let you act on it:

**Use it** — Copies the entire suggestion into the Finalized Text box, replacing its current contents. You can also manually select and copy only part of the suggestion.

**Copy it** — Copies the full suggestion text to your clipboard so you can paste it elsewhere.

**Clear** — Removes the suggestion from the Suggestion from AI section without affecting the Finalized Text box.

### Full screen mode

If you are working with a long piece of text, use the full screen button to expand the AI Writing Tools popup. This gives you more space for both the Finalized Text and the Suggestion sections.

---

## Section 6: Finalizing and Saving

### Finalize Text & Close

When you are satisfied with the contents of the Finalized Text box, click "Finalize Text & Close." This copies the text from the Finalized Text box into the rich text editor field in REDCap and closes the popup.

> **Important:** Finalizing the text does not save the field in REDCap. After closing the popup, you must save your work using the standard save mechanism for the page you are on (e.g., clicking "Save" in the Online Designer). Failing to save will discard the finalized text.

### Cancel

Closes the AI Writing Tools popup without copying anything into the rich text editor. Any suggestions generated during the session are discarded.

---

## Section 7: Common Questions

**Where is the purple wizard's wand? I don't see it.**
The wizard's wand only appears when the rich text editor is active. In some locations (like field labels in the Online Designer), you must manually enable the rich text editor first. If the rich text editor is active and the icon is still missing, AI Writing Tools may not be enabled for your project — contact your REDCap administrative team.

**Can I use the AI to combine multiple actions in one step?**
Not with the pre-defined action buttons — each one performs a single operation. Use the Custom Prompt option to combine actions in a single instruction (e.g., "Fix the grammar of [TEXT] and change the tone to formal.").

**What happens if I don't include [TEXT] in my custom prompt?**
The AI will respond to your prompt without considering the text currently in the Finalized Text box. If your goal is to modify your existing text, always include `[TEXT]` in the prompt so the AI knows what to work with.

**Can I partially accept a suggestion?**
Yes. Instead of clicking "Use it" (which copies the entire suggestion), select only the portion of the suggestion text you want, copy it manually, and paste it into the Finalized Text box.

**Does clicking "Finalize Text & Close" save my work?**
No. It copies the finalized text into the REDCap field, but you must still save the page using the standard save button. If you close the page or navigate away without saving, the changes will be lost.

**Can I run multiple actions on the same text in sequence?**
Yes. After you use a suggestion (copying it into the Finalized Text box), you can run another action on the updated text. Iterative refinement is supported.

**Is there a limit to what the custom prompt can do?**
Custom prompts support general AI requests, not just text editing. However, prompts that go far outside the text-editing use case (e.g., asking for a recipe) will generate a result in the Suggestion box but the content will be unrelated to your field text unless you include `[TEXT]`.

---

## Section 8: Common Mistakes & Gotchas

**Not enabling the rich text editor first.** In the Online Designer and some other locations, the rich text editor is not on by default. If you don't see the wizard's wand, look for a "rich text" toggle on the field — you may need to enable it before the AI icon appears.

**Forgetting to save after "Finalize Text & Close".** Clicking "Finalize Text & Close" copies text into the REDCap field but does not trigger a save. Many users assume the field is saved when the popup closes. Always click the page's own save button afterward.

**Omitting [TEXT] in custom prompts.** If your goal is to edit or transform your existing text using a custom prompt, you must include the `[TEXT]` placeholder. Without it, the AI responds to your prompt in isolation and ignores what's in the Finalized Text box.

**Expecting multi-action execution from a single pre-defined button.** Each pre-defined action (Fix Grammar, Set Length, etc.) performs one operation. To combine operations, use the Custom Prompt option with a single instruction that covers all desired changes.

---

## Related Articles

- RC-AI-01 — REDCap AI Tools: Overview & Security
- RC-AI-03 — AI Translations
- RC-AI-04 — AI Summarization
- RC-FD-02 — Online Designer
