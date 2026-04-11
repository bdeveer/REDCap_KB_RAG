RC-SURV-02

**Survey Settings: Basic Options & Design**

| **Article ID** | RC-SURV-02 |
| --- | --- |
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; assumes surveys have been enabled on at least one instrument |
| **Prerequisite** | RC-SURV-01 — Surveys – Basics |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-01 — Surveys – Basics; RC-SURV-03 — Survey Settings: Behavior, Access & Termination; RC-FD-02 — Online Designer |

---

# 1. Overview

This article is the first of a two-part series on the REDCap Survey Settings page. It covers the **Basic Options** section (survey status, title, and instructions) and the **Survey Design Options** section (layout, logo, typography, and color themes). Together these settings control whether a survey is accessible to participants and how it looks when they open it. The companion article, RC-SURV-03, covers behavioral customizations, access controls, and termination options.

To reach Survey Settings, navigate to your project, open the **Online Designer**, locate the instrument you want to configure, and click the **Survey Settings** button. Survey Settings are configured per instrument — each survey in a project has its own independent settings.

---

# 2. Key Concepts & Definitions

## Survey Settings Page

A configuration interface available for each instrument that has been enabled as a survey. Accessed through the Online Designer. Changes apply to that survey only.

## Survey Status

A dropdown that activates or deactivates a survey without deleting any settings. When set to **Survey Offline**, participants cannot access the survey via its public or individual link. Logged-in REDCap users can still fill out an offline survey as a regular instrument.

## Survey Title

The label displayed at the top of the survey page and in the participant's browser tab. Defaults to the instrument name but can be set to any value. Supports a limited set of HTML formatting tags.

## Survey Instructions

An optional block of introductory text displayed between the survey title and the first question. Supports rich text editing.

## Survey Design Options

The set of settings that control the visual appearance of a survey: layout width, logo, button style, text size, font, and color theme.

## Survey Theme

A saved collection of eight color settings that define the background and text colors for various regions of the survey interface. REDCap ships with built-in themes; institutions may add custom themes aligned to their branding guidelines. Themes can also be created and saved by individual users.

## Enhanced Radio Buttons and Checkboxes

An optional display mode that renders radio button and checkbox options as large tap-friendly blocks rather than small clickable circles. Intended for participants entering data on a mobile device.

---

# 3. Basic Survey Options

## 3.1 Survey Status

The **Survey Status** dropdown is the first control on the Survey Settings page. It has two values:

- **Survey Active** — the survey is live. Any participant with the appropriate link can access it.
- **Survey Offline** — the survey is inaccessible to participants. Logged-in project users can still fill it out as an instrument inside REDCap.

When a survey is set to offline, an optional **Offline Message** field appears. Use this to display a plain-language explanation to participants who attempt to access the survey. Rich text formatting and hyperlinks are supported, so you can direct participants to an alternative resource or provide contact information.

Example offline messages:
- "Thank you for your interest. This class has reached its maximum number of attendees."
- "Registration has closed for this school year. Please check back next summer."

> **Note:** Taking a survey offline via the Status dropdown is non-destructive — all settings, design choices, and collected data are preserved. This is the recommended approach for temporarily suspending a survey.

## 3.2 Survey Title

The **Survey Title** field controls what participants see at the top of the survey and in their browser tab. It is pre-populated with the instrument name but can be changed independently.

Use a participant-friendly title when the instrument name is technical or internal. For example:
- Instrument name: `PHQ-9`
- Survey title: `Patient Health Questionnaire`

> **Note:** The survey title supports a limited set of HTML tags, including `<u>` (underline) and `<i>` (italic). Full HTML or script tags are not permitted.

## 3.3 Survey Instructions

The **Survey Instructions** field places a block of text between the survey title and the first question. Use it to provide context, completion guidance, or consent-adjacent information that participants should read before starting.

This field supports full rich text editing — bold, italic, underline, bullet lists, hyperlinks, and basic table formatting are available through the editor toolbar.

---

# 4. Survey Design Options

## 4.1 Survey Width

The **Width of Survey** setting controls the horizontal extent of the survey on the participant's screen. Options include:

- **Fixed width** (default) — the survey displays at a consistent width regardless of screen size. This is the best option for most surveys.
- **Percentage-based widths** — stretches or compresses the survey to fill a set proportion of the screen (e.g., 75%, 90%, 100%).

> **Note:** REDCap overrides the width setting on mobile devices and scales the survey to fit the screen automatically. The width setting only has a visible effect on desktop and tablet browsers.

Higher percentages can cause very wide surveys on large monitors; lower percentages can make surveys feel cramped. If you use a percentage width, test on multiple screen sizes before distributing.

## 4.2 Logo

The **Logo** setting lets you place an image at the top of the survey, above the title. Common image formats (PNG, JPG, GIF) are supported. Images wider than 600 pixels are automatically scaled down to 600 pixels to fit the survey header.

You can optionally **hide the survey title** when a logo is present, leaving only the image at the top.

## 4.3 Enhanced Radio Buttons and Checkboxes

Standard radio button and checkbox controls are small and designed for precise mouse clicks. On touchscreen devices, small targets are difficult to tap accurately.

Enabling **Enhanced Radios and Checkboxes** replaces the standard controls with large, block-style buttons — much easier to tap with a finger.

> **Note:** This setting applies to the entire survey. You cannot enable enhanced buttons for individual questions only.

> **Alignment interaction:** Enhanced buttons still respect the **Custom Alignment** code set on each field (Column N in the Data Dictionary). Fields with a V code (RV, LV) render one button per row (full container width). Fields with an H code (LH, RH) render buttons in a two-column side-by-side grid. The L/R width designation (full-width vs. half-width) is also preserved. See RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques for alignment code details.

Consider enabling this setting if you expect participants to complete the survey on a phone or tablet.

## 4.4 Survey Text Size

The **Survey Text Size** setting sets the default font size for all text in the survey. By default, participants can also adjust the text size themselves using a control displayed on the survey page. To remove the participant-facing resize control, see the **Font Resize Options** setting in RC-SURV-03.

Tailor the default size to your audience. Surveys targeting older participants or those with low vision may benefit from a larger default.

## 4.5 Survey Text Font

The **Survey Text Font** setting applies a single typeface to all survey text. The default font, **Open Sans**, is a clean, neutral choice appropriate for most surveys.

All available fonts are web-safe or embedded — participants do not need any fonts installed on their device. Choose a font that aligns with your study's branding or the expectations of your participant population.

## 4.6 Survey Themes

A **Survey Theme** is a set of eight color values that define the colors of the survey's header, body background, text, buttons, and borders. Selecting a theme applies all eight values at once.

REDCap includes a set of built-in themes. Your institution may also have loaded themes aligned to local branding guidelines.

A **Survey Design Preview** section appears at the bottom of the Survey Design Options section and updates in real time as you make changes. Click **Expand** in the top-right corner of the preview to see a larger version.

> **Best practice:** Always test your survey design in a live test survey on all device types where you expect participants to respond — desktop, laptop, tablet, and phone. The preview is helpful but does not fully replicate mobile rendering.

### Custom Survey Themes

If none of the available themes fit your needs, click the **Customize** button next to the theme dropdown to open the custom theme editor.

The editor exposes all eight color settings as individual dropdowns. Clicking any dropdown opens a **color picker** with two controls:

- **Color square** — drag the black dot to adjust brightness and saturation within the selected hue.
- **Rainbow slider** — drag the white bar vertically to change the hue. Moving the slider updates both the color square and the preview.

You can also type or paste a **six-digit hexadecimal color code** directly into the code field at the bottom of the picker. This is the most reliable way to match a specific brand color. Most institutional branding guidelines publish hex codes for this purpose.

Click **Choose** (or click outside the picker) to confirm a color. When all eight colors are set, click **Save Custom Theme** and enter a name for the theme. REDCap links saved custom themes to your user account — they are available across all your projects without needing to be recreated.

Use **Manage Saved Themes** to edit or delete your custom themes at any time.

### Copying Design Settings to Other Surveys

The **Copy Design to Other Surveys** button (top-right of the Survey Design Options section) lets you apply your design settings to other surveys in the same project. After clicking the button, a popup lets you select which settings to copy and which surveys to copy them to. Use this to keep a consistent look across a project with multiple surveys.

---

# 5. Common Questions

**Q: Can I turn a survey off temporarily without losing my settings?**
Set **Survey Status** to **Survey Offline**. All settings and data are preserved. The survey can be re-activated at any time by switching the status back to **Survey Active**.

**Q: Can logged-in users fill out an offline survey?**
Yes. REDCap users with data entry rights can fill out an offline survey as a regular instrument from within the project interface. Participants accessing the survey via a link cannot.

**Q: My survey title is the instrument name and it looks too technical. How do I change it?**
Edit the **Survey Title** field in Survey Settings. This changes what participants see without renaming the instrument itself.

**Q: Can I use images or HTML in the survey title?**
Basic HTML tags (e.g., `<u>`, `<i>`) are supported. Full HTML, images embedded via `<img>`, and script tags are not. For rich formatting above the questions, use the **Survey Instructions** field instead, which supports the full rich text editor.

**Q: Does the enhanced radio buttons setting only affect mobile users?**
The setting changes the display for all participants, not just mobile users. Desktop users will also see the large block-style buttons. The setting is most beneficial for mobile users but is not hidden from others.

**Q: My logo is too large and looks blurry or stretched. What should I do?**
REDCap caps the display width at 600 pixels. Use an image that is natively 600 pixels wide or narrower to prevent automatic downscaling, which can reduce quality. PNG format generally preserves quality better than JPG for logos with text.

**Q: Can I copy the same theme to all surveys in my project at once?**
Yes. Use the **Copy Design to Other Surveys** button and select all surveys in the project from the popup.

**Q: Are custom themes shared with other users on my project?**
No. Custom themes are linked to the user account that created them. Other project users can see and use a theme if you have applied it to a survey, but they will not see it in their own theme dropdowns unless they create or import it themselves.

---

# 6. Common Mistakes & Gotchas

**Forgetting to re-activate a survey after edits.** Setting a survey offline for edits is good practice, but it is easy to forget to set it back to active afterward. Participants who attempt to access the survey during that window will see the offline message (or a default offline screen if no message is set). Build re-activation into your editing checklist.

**Testing design settings only in the preview panel.** The Survey Design Preview is useful for a quick check but does not accurately reflect how a survey looks on mobile devices or across all browsers. Always test the live survey on the same device types your participants will use, especially when using percentage-based widths or enhanced radios.

**Using a high-percentage survey width without testing on large monitors.** A 100% width survey on a wide monitor can feel uncomfortably stretched. Conversely, a 50% width on a small laptop can be cramped. If you deviate from fixed width, test on multiple screen sizes.

**Entering a display label rather than a hex code in the color picker.** The color code field expects a six-digit hexadecimal value (e.g., `#2A5DAB`). Entering a CSS color name or a label like "Yale Blue" will not work. Use the hex code from your branding guidelines.

**Assuming custom themes are project-wide or user-independent.** Custom themes belong to the user who creates them. If you leave a project or a colleague tries to recreate your theme in a different account, they will need the eight hex codes to reproduce it.

---

# 7. Related Articles

- RC-SURV-01 — Surveys – Basics
- RC-SURV-03 — Survey Settings: Behavior, Access & Termination
- RC-FD-02 — Online Designer
- RC-FD-06 — Online Designer – Instrument and Field Management
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (Column N alignment codes and how they interact with enhanced buttons)
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types
