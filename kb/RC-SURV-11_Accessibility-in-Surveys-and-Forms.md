

**Accessibility in REDCap Surveys & Forms**

| **Article ID** | [RC-SURV-11 — Accessibility in REDCap Surveys & Forms](RC-SURV-11_Accessibility-in-Surveys-and-Forms.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | Survey and instrument designers; anyone answering an institutional accessibility question about REDCap |
| **Requires** | Varies by item — see §3. Most improvements land between 16.0.6 and 17.3.0 |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review. Assistive-technology behaviour has not been independently tested |
| **Prerequisite** | [RC-SURV-01 — Surveys: Basics](RC-SURV-01_Surveys-Basics.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-08 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-SURV-02 — Survey Settings: Basic Options and Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md); [RC-SURV-03 — Survey Settings: Behavior, Access and Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md); [RC-FD-06 — Online Designer: Instrument & Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md); [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md); [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) |
| **Synonyms** | is redcap accessible; redcap screen reader support; WCAG compliance redcap; section 508 redcap surveys; keyboard navigation surveys; accessible surveys for participants with disabilities; VoiceOver redcap; low vision survey design; accessibility of redcap forms; datepicker keyboard access; what is a VPAT; accessibility conformance report; WCAG AA meaning; section 508 vs WCAG |

---

> **Scope and a caveat about what this article is.** This consolidates the accessibility work REDCap has shipped and the settings that affect accessibility, drawn from release notes through 17.4.1 Standard / 17.3.7 LTS. It has **not** been validated by testing with assistive technology, and it is **not** a conformance statement.
>
> **REDCap does not publish a WCAG or Section 508 conformance level, and neither does this article.** If your institution needs a formal accessibility statement — a VPAT or ACR, or an answer to a procurement questionnaire — that must come from your own evaluation or from the REDCap Consortium, not from a changelog summary. Those terms are defined in §1.1. What follows tells you what has been improved and what you can control; it does not tell you that any given survey is conformant.

---

## 1. Overview

Accessibility in a REDCap survey has two independent parts, and confusing them is the most common mistake:

| Layer | Who controls it | Examples |
| --- | --- | --- |
| **The platform** | REDCap's developers; your patch level | Screen-reader announcements, keyboard focus indicators, ARIA state on widgets |
| **The instrument** | You, the designer | Field labels, choice wording, colour and contrast choices, text size, whether the survey is navigable at all |

Upgrading REDCap improves the first. It does nothing for the second. A survey with unlabelled fields, colour-only meaning, or instructions embedded in an image remains inaccessible on the newest release — see §4.

Between **16.0.6** and **17.3.0** REDCap shipped a sustained run of accessibility improvements, most of them concentrated in the 17.1.x releases. That is the single strongest argument for keeping a public-facing survey instance current: participants with disabilities are the population most affected by an old patch level, and they are also the ones least able to work around it.

### 1.1 The terminology

These terms turn up in institutional accessibility requests, usually without explanation.

| Term | What it means |
| --- | --- |
| **WCAG** | *Web Content Accessibility Guidelines* — the international standard for web accessibility, published by the W3C. Organised into three conformance levels: **A** (minimum), **AA** (the level most institutions and laws require) and **AAA** (strictest, rarely required in full). "WCAG 2.1 AA" is the common procurement bar |
| **Section 508** | A provision of the US Rehabilitation Act requiring federal agencies to make electronic and information technology accessible. Since 2018 its technical requirements are **WCAG 2.0 AA**. US institutions receiving federal funding often apply it to their own systems |
| **EN 301 549** | The European equivalent, referenced by the EU Web Accessibility Directive. Also built on WCAG |
| **VPAT** | *Voluntary Product Accessibility Template* — a **standard form**, maintained by the Information Technology Industry Council, that a vendor fills in to state how their product measures up against an accessibility standard, requirement by requirement. It is a blank template, not a certification |
| **ACR** | *Accessibility Conformance Report* — a **completed** VPAT. Strictly, "VPAT" is the empty form and "ACR" is the filled-in document, though in practice people say "VPAT" for both. This is the artefact a procurement office is usually asking for |
| **Assistive technology (AT)** | Software or hardware a person uses to access a computer — screen readers (JAWS, NVDA, VoiceOver), screen magnifiers, switch devices, voice control |
| **Screen reader** | Software that reads screen content aloud and lets a user navigate by headings, links and form fields. It depends entirely on the underlying markup being correct — which is why field labels matter so much (§4) |

> **What a VPAT/ACR actually tells you.** It is a **self-assessment by the vendor**, not an audit or a certification. Its value is that it is specific: it walks each criterion and states *Supports*, *Partially Supports*, *Does Not Support* or *Not Applicable*, with explanatory notes. A procurement office asking for one wants that itemised detail, not a yes/no answer.
>
> **REDCap does not publish one**, which is why §5 exists — you will need to answer such a request from your own evaluation, or escalate it to the Consortium.

---

## 2. Accessibility-Relevant Settings You Control

These are existing REDCap features that bear directly on accessibility. They are documented in full elsewhere; collected here because they are what a designer can actually act on.

| Setting | Where | Notes |
| --- | --- | --- |
| **Text-to-Speech** | Survey settings | Reads survey text aloud. Can be off, on-by-default, or available-but-off. **Sends survey text to a third-party service** — check with your IRB before using it on sensitive surveys. See [RC-SURV-03](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md) §3.9 |
| **Survey Text Size** | Survey design options | Larger base text benefits low-vision participants without requiring browser zoom. See [RC-SURV-02](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) §4.4 |
| **Survey Text Font** | Survey design options | Font choice affects legibility, particularly for dyslexic readers. See [RC-SURV-02](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) §4.5 |
| **Survey Theme** | Survey design options | Custom themes are where **contrast** problems get introduced. A theme matching institutional branding is not automatically legible. See [RC-SURV-02](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) §4.6 |
| **Enhanced Signature field** *(17.1.0+)* | Online Designer | Accepts a **hand-typed** signature as well as a scribbled one. This matters: a mouse-drawn signature is impossible for many keyboard-only and motor-impaired users, so on any consented study the enhanced field is the accessible choice. See [RC-FD-06](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) |
| **Multi-Language Management** | Project setup | Beyond translation, MLM sets the page's `lang` attribute correctly (§3.1), which is what tells a screen reader how to pronounce the content |

> **Note:** Text-to-speech is a participant convenience, not a substitute for screen-reader compatibility. A participant using their own screen reader is not helped by REDCap reading text aloud in parallel — the two compete.

---

## 3. Platform Improvements by Version

All versions below are **Standard**. An LTS instance receives these only if its line was cut from a Standard release at or above the version shown — see [RC-INFRA-03](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

### 3.1 Screen reader support

| Version | Improvement |
| --- | --- |
| **16.0.6** | With MLM enabled on a survey, the `lang` attribute on the page's `html` tag is set to the MLM language code where it maps to an ISO 639-1 code. This is what lets a screen reader select the right pronunciation rules |
| **16.0.7** | **Descriptive Popups** made more accessible to screen readers on surveys and data entry forms |
| **16.0.9** | Screen reader users can navigate **inside** the date/time picker |
| **16.0.9** | Fixed handling of HTML `BR` tags in field labels. VoiceOver on Chrome announced a `BR` in a label as *"Empty Group"*, breaking the reading flow. **Chrome-specific** |
| **17.1.0** | Survey pages **announce page changes** — e.g. *"You are currently on page X of Y of the survey title Z."* Without this, a screen reader user could not tell whether submitting a page had done anything |
| **17.1.0** | The **language selector** widget communicates its expanded/collapsed state, so assistive technology reports when the menu opens or closes |
| **17.1.1** | Dismissing the **"required fields" error popup** now scrolls to and focuses the first incomplete required field, instead of leaving the user to re-traverse the page hunting for it |
| **17.1.4** | After a **failed login**, the error message sits closer to the login fields and is exposed to the screen reader on redirect back to the page |

### 3.2 Keyboard navigation and visible focus

| Version | Improvement |
| --- | --- |
| **16.0.9** | Keyboard users can reach the **date/time picker** at all. Previously tabbing skipped straight past it — a hard block, not an inconvenience |
| **16.1.1** | **Record Status Dashboard** rows highlight on hover *and* on keyboard focus |
| **17.1.0** | **Survey navigation buttons** ("Next Page", "Save & Continue", "Save & Return Later") show a glowing highlight on hover or keyboard focus |
| **17.1.3** | Survey **form fields and buttons** show a clear visible highlight when reached by keyboard — the single most useful change for anyone navigating without a mouse or with low vision |
| **17.1.3** | The **slider** control highlights its surrounding question in green on focus, consistent with every other field type, and the track and knob have improved contrast when active |

### 3.3 Visual presentation

| Version | Improvement |
| --- | --- |
| **17.3.0** | Button styling adjusted on surveys and project pages to improve accessibility |

### 3.4 A regression worth knowing about

> **Version caveat (16.0.9–16.1.1 Standard):** The 16.0.9 datepicker accessibility work introduced a regression — **erratic flashing of the datepicker** in the context of ASIs and Alerts & Notifications. Closing the picker returned focus to the input field, whose `onfocus` handler immediately reopened it. Fixed in **16.1.2**, which kept the accessibility improvements while restoring normal behaviour.
>
> This is a useful illustration of why accessibility fixes deserve the same regression testing as any other change: the fix was correct in intent and broke ordinary use for everyone.

---

## 4. What REDCap Cannot Fix For You

Every improvement in §3 addresses the *platform*. The most common accessibility failures in REDCap surveys are in the *instrument*, and no upgrade touches them:

- **Field labels that don't describe the field.** A screen reader reads the label. "Please enter below:" tells the user nothing.
- **Meaning carried by colour alone.** Red text marking required items is invisible to a colour-blind participant and to a screen reader alike. Say "required".
- **Instructions embedded in images.** Text in an uploaded image is unreadable to assistive technology. Use the field label or a descriptive field.
- **Descriptive text used as a heading without being one.** Section Headers give structure that screen readers can navigate by; bold descriptive text does not.
- **Custom themes with insufficient contrast.** Branding colours frequently fail contrast ratios. Check before deploying, not after a complaint.
- **Matrix fields that are very wide.** They are difficult to navigate with a screen reader and awkward on small screens, where many participants with disabilities are.
- **Time limits and forced-response patterns** that assume a participant can complete quickly.

> **The practical test.** Before releasing a public survey, complete it end to end using only the keyboard — no mouse — at the largest text size your participants might use. Most instrument-level accessibility problems surface within a minute, and it requires no specialist tooling.

---

## 5. Answering an Institutional Accessibility Question

REDCap managers are routinely asked whether REDCap is "508 compliant" or "WCAG AA". Some honest framing:

- **There is no published conformance level to cite.** REDCap ships accessibility improvements; it does not, in its release notes, claim a conformance level.
- **Conformance is per-survey, not per-platform.** Even a fully conformant platform will produce a non-conformant survey if the instrument is badly designed. The question "is REDCap accessible?" is not answerable in the abstract.
- **Patch level is part of the answer.** An instance below 17.1.3 lacks visible keyboard focus indicators on survey fields; below 16.0.9 the date picker is unreachable by keyboard. Those are concrete, checkable facts about *your* instance.
- **Escalate formal requests.** VPATs and Accessibility Conformance Reports (see §1.1) and procurement questionnaires should go to the REDCap Consortium via the Community Portal, or be answered by your institution's own evaluation.

---

## 6. Common Questions

**Q: Is REDCap accessible?**

**A:** REDCap has shipped sustained accessibility improvements from 16.0.6 through 17.3.0, particularly around screen reader announcements and keyboard focus. But accessibility is determined jointly by the platform and by how the instrument is designed — a poorly designed survey on the newest release is still inaccessible. There is no published conformance level to point at.

**Q: What's the single most valuable version to be on?**

**A:** **17.1.3 or later.** That release added clear visible highlights for survey form fields and buttons under keyboard navigation, which affects every keyboard-only and low-vision participant on every survey. 16.0.9 is the other threshold — below it, keyboard users cannot reach the date/time picker at all.

**Q: Does turning on text-to-speech make our survey accessible?**

**A:** No. It is a useful convenience for some participants, but it is not screen-reader compatibility and it does not address keyboard navigation, contrast or label quality. It also sends survey text to a third-party service, which needs IRB consideration for sensitive content.

**Q: Our participants use screen readers. Anything specific to check?**

**A:** Be on 17.1.0+ so page changes are announced, and 17.1.1+ so required-field errors move focus to the offending field. Enable MLM if the survey is not in the instance's default language, so the `lang` attribute is set. Then check your own field labels — that is where most remaining problems will be.

**Q: We have a signature field and a participant can't use a mouse. What do we do?**

**A:** Use the **Enhanced Signature** field type (17.1.0+), which accepts a hand-typed signature as well as a drawn one.

**Q: A screen reader reads odd "Empty Group" text in our field labels.**

**A:** That is the `BR` tag issue fixed in **16.0.9**, and it only occurs in Chrome with VoiceOver. Upgrade, or restructure the labels to avoid `BR` tags.

**Q: Our date picker flashes repeatedly on alert-related pages.**

**A:** A regression in 16.0.9 through 16.1.1, fixed in **16.1.2**. Upgrade.

**Q: What is a VPAT, and can we get one for REDCap?**

**A:** A **Voluntary Product Accessibility Template** is a standard form a vendor completes to state, criterion by criterion, how their product measures against an accessibility standard; a completed one is properly called an **Accessibility Conformance Report (ACR)**. It is a vendor self-assessment, not a certification or an audit — see §1.1.

REDCap does not publish one. Formal conformance documentation should be requested through the REDCap Consortium, or produced by your own institutional evaluation of your instance and your instruments.

---

## 7. Common Mistakes & Gotchas

**Treating accessibility as a platform property.** It is jointly determined. Upgrading fixes focus indicators and screen-reader announcements; it does not fix your field labels, your contrast, or your reliance on colour.

**Claiming a conformance level REDCap has not claimed.** "REDCap is 508 compliant" is not a statement the release notes support. Describe what your instance does and does not do instead.

**Running a public participant-facing instance on an old patch level.** Accessibility improvements are exactly the kind of change that only affects a minority of users — who then simply cannot complete the survey and are rarely in a position to report why.

**Assuming text-to-speech covers screen reader users.** It does not, and the two can conflict. It is a separate feature for a different need.

**Using a mouse-drawn signature field on a consent instrument.** Pre-17.1.0 signature capture excludes participants who cannot use a pointing device. On an e-consent instrument that is a consent-validity problem, not just a usability one.

**Deploying a custom survey theme without checking contrast.** Institutional brand palettes routinely fail contrast requirements.

**Never testing with the keyboard.** A single keyboard-only pass through a survey catches most instrument-level problems and takes a minute.

---

## 8. Related Articles

- [RC-SURV-02 — Survey Settings: Basic Options and Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) — text size, font and themes, the design settings with the largest accessibility impact
- [RC-SURV-03 — Survey Settings: Behavior, Access and Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md) §3.9 — text-to-speech configuration and its privacy implications
- [RC-FD-06 — Online Designer: Instrument & Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) — the Enhanced Signature field type
- [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) — language handling, which sets the `lang` attribute screen readers depend on
- [RC-SURV-08 — e-Consent Framework: Setup and Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) — where signature accessibility becomes a consent-validity question
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — how to tell which of the improvements in §3 your instance actually has
