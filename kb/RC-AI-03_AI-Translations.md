# RC-AI-03 — AI Translations

| Field | Value |
|---|---|
| Article ID | RC-AI-03 |
| Domain | AI Tools |
| Applies To | Projects using the Multi-Language Management module |
| Prerequisite | RC-AI-01 — REDCap AI Tools: Overview & Security |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-AI-01 — REDCap AI Tools: Overview & Security; RC-MLM-01 — Multi-Language Management |

---

## Section 1: Overview

This article explains how to use REDCap's AI Translation feature, which is built into the Multi-Language Management (MLM) module. The feature allows you to translate your instrument content, the REDCap user interface, survey settings, alerts, and miscellaneous text into one or more target languages with a single button click — instead of manually entering translations or copying from an external translation tool. The AI sends content to your institution's AI server and returns translated strings, which you can then review and save. This article covers how to set up a language, translate the interface, translate instruments, and keep translations current when your project changes.

> **Note:** Certain regulatory contexts (such as clinical trial consent forms) require certified translations. AI-generated translations are not certifications. Verify with your Institutional Review Board (IRB) or compliance office whether certified translation documentation is required for your use case.

---

## Section 2: Key Concepts & Definitions

## Multi-Language Management (MLM)

The REDCap module that enables a project to present content in multiple languages. The AI Translation feature is located inside this module. MLM must be set up and at least two languages must be defined before AI translation becomes available.

## Language ID

A short code that uniquely identifies a language in REDCap's MLM configuration. Language IDs follow international standards (e.g., `es` for Spanish, `fr` for French). The ID is used internally; the Language Display Name is what participants see.

## Language Display Name

The name of the language as it should appear to end users. Best practice is to write this in the language itself (e.g., "Español" for Spanish, "Français" for French). REDCap uses this name as input when generating AI translations — if the name is misspelled or in the wrong language, translations may be incorrect.

## Base Language

The primary language in which your instruments are built. REDCap uses the base language as the source for all translations. A base language must be set for the MLM module to function.

## Fallback Language

The language REDCap displays when a translation for a specific element is missing. This is typically set to the same language as the base language. If no translation exists for an element in the user's selected language, REDCap shows the fallback language version instead.

## Translation Status Indicators

Red and green dots displayed next to translatable elements in the MLM interface. A red dot means the element has not yet been translated; a green dot means a translation exists. After running the AI translation, all previously red dots for translated elements turn green.

---

## Section 3: Setting Up a Language

Before you can translate anything, you must add the target language to your project.

1. Navigate to **Multi-Language Management** in the project menu.
2. Click the **+ Add a new language** button.
3. Select **"by creating the language from scratch."**
4. In the popup, enter:
   - **Language ID** — use the standard international code (e.g., `es` for Spanish).
   - **Language Display Name** — enter the name of the language in the language itself (e.g., `Español`).

   > **Important:** REDCap uses the Language Display Name as the AI translation prompt input. If this name is incorrect or written in English rather than the target language, the AI may translate into the wrong language or produce inaccurate results.

5. Click **+ Add Language**.
6. Toggle the language to **Active** using the switch next to the language name.

### Base Language and Fallback Language requirements

MLM requires at least two languages to be defined and active. You must also designate a **Base Language** and a **Fallback Language** — these are usually the same language (the language your instruments are built in). If your working language (e.g., English) is not yet listed, add it following the steps above, activate it, and select it as both Base Language and Fallback Language using the corresponding radio buttons.

> **Note:** The AI Translation button in the Forms/Surveys tab only appears after the Base Language has been set and at least two languages are active. If you do not see the AI translation option, verify these requirements are met.

---

## Section 4: Translating the REDCap Interface

Translating the user interface (UI) ensures that navigation elements, button labels, and system messages are displayed in the target language — not just your instrument content. This step is recommended before translating instruments.

1. In the Multi-Language Management menu, navigate to the **User Interface** tab.
2. Confirm the correct target language is selected in the language selector at the top of the page.
3. Choose a tab:
   - **Common** — contains the most frequently used interface elements (over 500 items). Use this for most projects.
   - **All** — combines every interface element across all tabs. Use this if you want a complete translation in one pass.
4. Click **"Translate using AI"**. REDCap will begin sending interface strings to the AI server. This process can take several minutes, depending on the number of elements.
5. REDCap displays a progress message showing how many elements are being translated.
6. When complete, red dots turn green and the translated text fills in.
7. Review the translations for accuracy. AI translations are generally reliable but may miss nuanced or context-specific phrasing — ideally, have a fluent speaker review the output.
8. Click **Save Changes** to preserve the translations.

> **Note:** After each REDCap upgrade, new interface elements may be added. Return to the User Interface tab after upgrades and run the AI translation again to cover any new items. Untranslated elements default to English.

---

## Section 5: Translating Instruments

1. In the Multi-Language Management menu, navigate to the **Forms/Surveys** tab.
2. Confirm the correct target language is selected.
3. For each instrument you want to translate, toggle **Data Entry** to enable translation for data entry mode.
   - If surveys are enabled on the project, a separate **Survey** toggle appears. Enable it to make the translation available in survey mode as well.
4. Click the **Translate** button for the instrument.
5. Click **"Translate using AI"** to translate all untranslated elements in that instrument. Processing time varies by instrument size.
6. REDCap displays a progress message while translating.
7. When complete, red dots turn green.
8. Review translations for accuracy and edit any individual strings directly if corrections are needed.
9. Click **Save Changes**.
10. Repeat steps 4–9 for each instrument you want to translate.

### Survey settings translation

If surveys are enabled on an instrument, a separate **Translate** option appears for survey settings (e.g., survey title, completion text). This is separate from translating the instrument fields. Click the corresponding Translate option and run "Translate using AI" the same way.

---

## Section 6: Keeping Translations Current

### When you modify an instrument

If you add, edit, or remove variables after translating, you must return to the MLM module and run the AI translation again on the affected instruments. REDCap identifies which elements are new or changed (red dots) and only translates those — existing green-dot translations are not re-processed.

### Alerts & Misc tabs

Two additional tabs in the MLM module are relevant to translation but only appear when the corresponding features are configured:

- **Alerts** — If Alerts & Notifications are set up in your project, alert content appears here and can be AI-translated the same way as instrument content.
- **Misc** — Contains less common elements such as missing data codes. AI translation works identically here.

---

## Section 7: Common Questions

**Why don't I see the "Translate using AI" button?**
The AI translation button only appears when: (1) at least two languages are active in the project, (2) a Base Language has been set, and (3) the AI Translations feature is enabled by your administrator. If all three conditions are met and the button is still missing, contact your REDCap administrative team.

**What language does REDCap translate from?**
REDCap translates from the Base Language you set in the MLM module. Your instrument content is read in the Base Language and translated into the selected target language.

**Does the AI re-translate items that are already translated?**
No. The AI translation only processes elements that have not yet been translated (red dots). Already-translated elements (green dots) are skipped, which prevents overwriting manual corrections.

**What happens if an interface element is not translated?**
REDCap falls back to the Fallback Language (typically English) for any element that does not have a translation. Participants or users will see the fallback language version for that specific element.

**Can I edit an AI-generated translation?**
Yes. Click directly on any translated string in the MLM interface to edit it manually. This is the recommended approach for correcting inaccurate translations.

**Do I need certified translations for my study?**
It depends on your regulatory context. Clinical trials with consent forms often require certified translations. REDCap's AI translations are not certifications. Consult your IRB or compliance office.

**What happens if I misspell the Language Display Name?**
REDCap passes the Language Display Name to the AI as the target language instruction. A misspelled or incorrect name (e.g., "Spaniss" instead of "Español") may cause the AI to translate into an unintended language or produce poor-quality output. Correct the name and re-run the translation.

---

## Section 8: Common Mistakes & Gotchas

**Setting the Language Display Name in English instead of the target language.** REDCap uses the display name as the AI prompt. If you enter "Spanish" instead of "Español," the translation quality may be affected. Always enter the display name in the language itself.

**Not setting a Base Language before attempting to translate.** MLM requires a Base Language to be defined. If you skip this step, the AI translation option will not appear. Add your primary working language, activate it, and designate it as the Base Language.

**Forgetting to click "Save Changes" after translating.** The AI populates translation strings in the interface, but they are not persisted until you explicitly save. Navigating away without saving discards all AI-generated translations for that session.

**Not re-translating after instrument changes.** If you add or edit variables after translating, those new or changed elements will revert to red (untranslated). Run the AI translation again on any modified instruments to keep translations complete.

**Assuming AI translations are always accurate.** AI translation quality is generally high but not perfect, particularly for specialized medical or scientific terminology, culturally nuanced phrasing, or languages with limited training data. Always have a fluent speaker review the output before deploying to participants.

---

## Related Articles

- RC-AI-01 — REDCap AI Tools: Overview & Security
- RC-AI-02 — AI Writing Tools
- RC-AI-04 — AI Summarization
- RC-MLM-01 — Multi-Language Management
