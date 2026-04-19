RC-TXT-01

**Texting in REDCap: Setup and Usage**

| **Article ID** | RC-TXT-01 |
| --- | --- |
| **Domain** | Texting (SMS) |
| **Applies To** | Projects with surveys enabled; requires Twilio or Mosio configured at the system level |
| **Prerequisite** | RC-SURV-01 — Surveys: Basics |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-SURV-05 — Participant List and Manual Survey Invitations; RC-SURV-06 — Automated Survey Invitations; RC-ALERT-01 — Alerts and Notifications Setup; RC-TXT-02 — Texting: Administrator Setup; RC-CC-06 — Control Center: Modules & Services Configuration |

---

# 1. Overview

REDCap can send survey invitations and alert notifications as text messages (SMS) instead of — or in addition to — email. This is done through one of two third-party providers: **Twilio** or **Mosio**. This article covers everything a project designer needs to know: how texting works conceptually, how to enable and configure a provider in a project, and how texting integrates with survey distribution tools, the participant list, Automated Survey Invitations (ASIs), and Alerts & Notifications.

For system-level setup (enabling Twilio or Mosio across the entire REDCap installation, setting permission levels), see RC-TXT-02 — Texting: Administrator Setup.

---

# 2. Key Concepts & Definitions

## SMS (Short Message Service)
The standard protocol used by mobile phones to send and receive text messages. SMS messages are transmitted over cellular networks and do not require an internet connection or a separate app. REDCap sends text messages via SMS through its configured provider.

## RCS (Rich Communication Service)
A modern successor to SMS supported by most current smartphones. For the purposes of REDCap texting, RCS and SMS behave identically — REDCap sends via the provider, and the phone handles delivery.

## Twilio
A commercial SMS and voice communications provider. Twilio requires three credentials: an Account SID, an Auth Token, and a Twilio phone number. Twilio supports SMS worldwide and additionally supports voice call surveys. Configuration is more involved than Mosio.

## Mosio
A commercial SMS provider focused on research texting. Mosio requires only a single API key. Mosio is currently available in the US and Canada only. Mosio does not support voice calls.

## Phone variable
A REDCap variable with Phone Number validation (or integer validation) that stores a participant's phone number. REDCap uses this variable to determine which number to text when sending invitations via ASIs or alerts.

## Invitation type
The delivery format for a survey invitation. With texting enabled, invitation types include: email, SMS with a survey link (webpage), SMS conversation, and (Twilio only) voice call.

## SMS conversation
A mode in which REDCap administers a survey interactively via back-and-forth text messages. The participant texts their answers directly; REDCap interprets them. Because text messages are unencrypted, this mode carries privacy risk and must be explicitly enabled by a REDCap administrator.

## Voice call
A Twilio-only feature in which an automated voice reads survey questions aloud and accepts keypress responses. Voice calls are not available with Mosio.

## Project feature setting
A Twilio/Mosio configuration option that controls which parts of a REDCap project can use texting: surveys and ASIs only, Alerts & Notifications only, or both.

## Overlapping SMS invitations
A condition that occurs when a participant has more than one active survey invitation at the same time. REDCap's behavior in this case is controlled by the "Behavior for overlapping SMS invitations" setting.

---

# 3. Before You Start

## 3.1 Is texting available in your installation?

Texting must be enabled at the system level by a REDCap administrator before any project can use it. Administrators configure Twilio and/or Mosio credentials and set access control in the Control Center under System Configuration → Modules/Services Configuration (see **RC-CC-06** and **RC-TXT-02** for the full admin setup process). Navigate to **Project Setup** and look for Twilio or Mosio in the list of optional project features. If neither appears, contact your REDCap support team. Your institution may have texting enabled but restricted to administrator-only setup — in that case, the "Enable" button will be visible but greyed out, or hidden entirely.

> **Institution-specific:** Texting provider availability (Twilio, Mosio, or both) and permission levels vary by installation. Contact your REDCap administrator to confirm which providers are enabled at your institution and what access level is required to enable them on a project.

## 3.2 Budget and cost

Both Twilio and Mosio are commercial services that charge per message. Costs are typically fractions of a cent per message, but large studies with frequent touchpoints can accumulate significant charges. Email and MyCap push notifications do not carry per-message costs. Confirm your study's budget before enabling texting.

## 3.3 Regulatory compliance

Before using texting for research recruitment or data collection:

- **Check with your IRB or compliance office.** Many institutions have rules about who may be contacted via text and how consent must be documented.
- **Follow provider requirements.** Both Twilio and Mosio require users to comply with applicable anti-spam laws (e.g., TCPA in the US). Each provider has its own onboarding documentation describing these requirements.
- **Inform participants in advance.** Modern smartphones filter texts from unknown numbers. Let participants know what number to expect contact from so they can add it to their contacts or safe-sender list.

## 3.4 Prepare a phone variable (recommended)

If you plan to send ASI invitations or alerts to participant phone numbers, create a dedicated phone variable in your instrument before enabling texting:

1. In the Online Designer, add a new Text field.
2. Set the validation type to **Phone (North America)** or the appropriate country format.
3. Note the variable name — you will need it during Twilio/Mosio configuration.

A phone variable is not required for public survey link invitations or hard-coded alert phone numbers, but it is essential for record-based texting.

---

# 4. Enabling and Configuring Twilio

## 4.1 Enable Twilio in Project Setup

1. In **Project Setup**, locate "Twilio SMS and Voice Call Services" in the list of optional features.
2. Click **Enable**. The status text turns green when enabled.
3. A credentials popup appears. Set the **Twilio SMS and Voice Services** dropdown to **Enabled**.
4. Enter your **Twilio Account SID**, **Twilio Auth Token**, and **Twilio phone number** in the corresponding fields. These are found in your Twilio account dashboard.
5. Optionally enter a **Twilio Alphanumeric Sender ID** — this replaces the numeric phone number with a text label in the sender field on compatible carriers.
6. Click **Save**.

> **Note:** You can only have one provider (Twilio or Mosio) active in a project at a time. Enabling one disables the other.

## 4.2 Configure Twilio settings

After enabling, a new **"Twilio SMS and Voice Call Services"** item appears in Project Setup. Click **Configure settings**.

**Language and gender used for voice calls**
Sets the voice used for any automated voice call surveys. Available in multiple languages and male/female varieties. Only relevant if you plan to use voice call invitations.

**Project feature**
Controls which parts of the project can use texting. Options:

| Option | What it enables |
|---|---|
| Surveys and survey invitations only (default) | ASIs and Survey Distribution Tools |
| Alerts & Notifications only | Alerts & Notifications |
| ALL: Surveys + Alerts & Notifications | Both of the above |

Enabling a feature here does not automatically configure it — you must still set up individual ASIs or alerts to use texting.

**Choose survey invitation types to use**
Defines which delivery formats are available. Options:

- **Survey as a webpage** (default, recommended) — sends a survey link via text. The link opens a secure HTTPS connection. This is the safest option because the survey data is encrypted in transit even though the text message itself is not.
- **Survey as a voice call** — Twilio calls the participant and reads survey questions aloud. Three sub-options control who initiates the call:
  - *Initiate survey as voice call* — Twilio calls the participant directly.
  - *Send SMS to take survey as voice call (respondent makes call)* — participant calls back.
  - *Send SMS to take survey as voice call (respondent receives call when replying via SMS)* — voice call starts when participant texts back.
- **Survey as an SMS conversation** — REDCap administers the survey interactively via text message exchange. Requires administrator activation (hard-coded in REDCap). Carries privacy risk due to unencrypted transmission.

Multiple types can be enabled simultaneously.

**Choose the default invitation preference for new survey participants**
Sets the default contact method for new records. Must match one of the enabled invitation types above — selecting a type that is not enabled will cause an error when invitations are sent.

**Control each participant's invitation preference using a multiple choice field**
Designates a dropdown or radio variable in your project as the per-record contact preference field. REDCap overrides the default invitation preference for any record where this field is filled in. The variable's coded values must match REDCap's expected option codes (e.g., `EMAIL`, `SMS_INVITE_WEB`).

**Designate a phone number field for survey invitations sent via SMS or voice call**
Assigns a specific phone variable from your project as the source of participant phone numbers. The variable must have Phone Number validation (or integer validation). Optional but recommended if phone numbers are part of your dataset.

**Automatically append response instructions to questions?**
When enabled, REDCap adds brief instructions to SMS or voice prompts (e.g., how to answer a multiple-choice question in an SMS conversation). Recommended to test both settings with your survey before going live.

**Behavior for overlapping SMS invitations**
Controls what happens when a participant receives a second invitation before completing the first. Options:

| Option | Best for |
|---|---|
| Use only most recent invitation | High-frequency surveys (e.g., daily diaries) where only the latest matters |
| Take surveys in same order as received | Projects where completion order affects calculations or piped fields |
| Allow participant to choose which survey to take next | Projects where completion order is flexible |

## 4.3 Analyze surveys for SMS & Voice Calls (Twilio)

Next to "Configure settings," the **Analyze surveys for SMS & Voice Calls** button checks your enabled surveys for compatibility with SMS conversation or voice call delivery. It flags variable types that cannot be transmitted in those formats (e.g., file upload fields). Fix any flagged issues in the Online Designer before going live.

---

# 5. Enabling and Configuring Mosio

## 5.1 Enable Mosio in Project Setup

1. In **Project Setup**, locate "Mosio Two-Way Text Messaging (SMS) Services."
2. Click **Enable**. A credentials popup appears.
3. Set the **Mosio SMS Services** dropdown to **Enabled**.
4. Enter your **Mosio API Key** in the corresponding field. This is found in your Mosio account dashboard.
5. Click **Save**.

> **Note:** Mosio is only available in the US and Canada. If your study contacts participants in other countries, use Twilio instead.

## 5.2 Configure Mosio settings

After enabling, click **Configure settings** under "Mosio Two-Way Text Messaging (SMS) Services."

**Project feature**
Same as Twilio — controls whether texting is enabled for Surveys/ASIs, Alerts & Notifications, or both.

**Choose survey invitation types to use**
Mosio supports two options:

- **Survey as a webpage** (default, recommended) — sends a survey link via text.
- **Survey as an SMS conversation** — interactive back-and-forth survey. Requires administrator activation. If your Mosio account is on a two-way plan, you must also enable this feature in the Mosio dashboard. On a one-way plan, it is enabled automatically.

**Choose the default invitation preference for new survey participants**
Sets the default contact method. Options with Mosio are email, SMS with a survey link, or SMS conversation. Must match an enabled invitation type.

**Control each participant's invitation preference using a multiple choice field**
Same as Twilio — designates a dropdown or radio variable as the per-record contact preference field.

**Designate a phone number field for survey invitations sent via SMS**
Same as Twilio — assigns a phone variable as the source of participant phone numbers.

**Automatically append response instructions to questions?**
Same as Twilio.

**Behavior for overlapping SMS invitations**
Same options as Twilio — most recent, in-order, or participant's choice.

## 5.3 Analyze surveys for SMS (Mosio)

The **Analyze surveys for SMS** button checks your enabled surveys for compatibility with SMS conversation delivery. Flags file upload fields and other variable types that cannot be used in SMS conversations.

---

# 6. Using Texting in Your Project

After configuring Twilio or Mosio, texting capabilities appear in three places: Survey Distribution Tools, Automated Survey Invitations, and Alerts & Notifications.

## 6.1 Survey Distribution Tools — Public Survey Link

The public survey link page gains an **"Invite participant via SMS"** button. Clicking it opens a popup where you specify:

- **Phone numbers** — enter one number per line. Numbers are not associated with any record; a record is only created if the participant responds.
- **Invitation type** — choices are determined by your configuration.
- **Message text** — enter your SMS message in the "Enter custom SMS message" box. If you are sending a survey link, include `[survey-url]` or `[survey-link]` in the message body — without it, the recipient has no link to click.

> **Note:** REDCap sends one SMS at a time (not in batches). Large sends take proportionally longer than email sends, which go out in batches of 20.

## 6.2 Survey Distribution Tools — Participant List

With texting enabled, the participant list gains phone number and invitation preference columns. When adding participants:

- A **phone number** field appears alongside the email field. At least one contact method (email or phone) is required.
- A **default invitation preference** option is available for the batch being added.

When composing survey invitations from the participant list, you must now specify an invitation type in addition to the standard scheduling options.

> **Note:** REDCap ignores the subject line for text and voice call invitations. For voice call invitations, REDCap also ignores the message body — the survey content itself becomes the voice call script.

## 6.3 Automated Survey Invitations (ASIs)

Texting adds an **invitation type** step to the ASI setup wizard. Before setting up an ASI for texting:

- Confirm that a phone variable is defined in your project **or** that participants have been added through the participant list with a phone number. Without a phone number source, REDCap cannot deliver the message.
- If you select "Participant's preference" as the invitation type, you must have configured both the default invitation preference and the invitation preference field in your Twilio/Mosio settings — otherwise REDCap cannot determine how to contact each participant.

The remaining ASI steps work identically to email ASI setup, with minor variations depending on invitation type (e.g., no subject line field for SMS conversation invitations).

For ASI setup beyond invitation type, see RC-SURV-06 — Automated Survey Invitations.

## 6.4 Alerts & Notifications

Texting adds an **Alert Type** selector to Step 3 of the alert setup. The available types depend on your provider and configuration:

| Alert type | Description |
|---|---|
| Email | Standard email — always available |
| SMS Text Message | Sends the alert body as a text message |
| Voice Call | (Twilio only) Robot voice reads the alert body aloud. Not recommended for messages containing links. |

Alert types are mutually exclusive per alert — to send the same alert via both SMS and email, duplicate the alert and select a different type for the copy.

**Defining phone numbers for an alert**

Two methods are available and can be combined in a single alert:

- **Variable-based** — select one or more phone variables from the "select recipients" dropdown. If a participant was added through the participant list with a phone number (not a phone variable), select "survey participant" to use that number. REDCap texts the phone number(s) stored in the selected variable(s) for each triggered record.
- **Hard-coded** — type one or more phone numbers directly into the number field, separated by semicolons. REDCap texts these numbers every time the alert fires, regardless of which record triggered it. Useful for notifying study team members.

> **Note:** A hard-coded alert that fires 100 times sends 100 text messages to the same number — charges accumulate accordingly. Use conditional logic in the alert trigger to limit unwanted fires.

> **Pro tip:** Combining variable-based and hard-coded recipients in the same alert lets you simultaneously text a participant at their stored number and copy a fixed study team contact.

For alert setup beyond Step 3, see RC-ALERT-01 — Alerts and Notifications Setup.

---

# 7. Best Practices

**Keep messages short.** The standard SMS character limit is 160 characters. Messages longer than 160 characters are split across multiple texts, increasing cost and reducing engagement. Survey links consume a significant portion of this limit — test your messages before sending.

**Do not pipe sensitive information into text messages.** Text messages are unencrypted and can be intercepted or read on the recipient's lock screen. Never pipe PHI, identifiers, or sensitive study data directly into an SMS body. If you need to present sensitive information to a participant, use a survey link and pipe the data inside the survey itself.

**Use survey links, not SMS conversations, when security matters.** The moment a participant clicks a survey link, they connect via HTTPS. SMS conversation mode transmits responses as unencrypted text. For any study involving sensitive data, survey-as-webpage is the recommended invitation type.

**Inform participants of the sending number beforehand.** Many smartphones automatically filter texts from unknown senders. Include the Twilio or Mosio phone number in your consent documentation so participants can add it to their contacts.

**Follow IRB and provider compliance requirements.** Obtain IRB or compliance approval before enabling texting. Follow Twilio's or Mosio's onboarding guidance on TCPA compliance, opt-out language, and identification requirements. Include contact information for the study team in your text messages where feasible.

**Proofread carefully.** Spelling and grammar errors are one of the signals that anti-spam filters use to classify messages. Proof every message before sending.

**Respect participant preferences.** Use the invitation preference field to let participants choose their preferred contact method. Participants who prefer email should receive email, not texts.

---

# 8. Common Questions

**Q: Can I use both Twilio and Mosio in the same project?**
No. Only one provider can be active per project at a time. If your institution has both available, you must choose one when enabling texting in Project Setup.

**Q: Do public survey link SMS invitations create a record?**
No. Sending a text via the public survey link's "Invite participant via SMS" button does not create a record. A record is created only when the participant responds to the survey.

**Q: Can I enable SMS conversations without administrator involvement?**
No. SMS conversation mode must be enabled by a REDCap administrator regardless of your user rights. This is hard-coded in REDCap because of the privacy implications of unencrypted text transmission.

**Q: What happens if a participant doesn't have a phone number in REDCap when an ASI fires?**
REDCap skips the invitation for that record. No text is sent and no error is logged in the participant's record. If phone numbers are collected later, REDCap does not retroactively send missed invitations.

**Q: Can I send a text to a participant and an email to myself with the same alert?**
Not with a single alert. Duplicate the alert, set one copy to SMS (recipient = participant phone variable) and the other to email (recipient = your email). Both will fire on the same trigger conditions.

**Q: Can I use piping in SMS messages?**
Yes — piping is supported in ASI and alert message bodies. Use it only for non-sensitive data (e.g., a participant's first name or a scheduled visit date). Never pipe PHI or sensitive identifiers into a text message.

**Q: What if Twilio or Mosio is not visible in my Project Setup page?**
It has not been enabled for your installation or your administrator has restricted setup to admins only. Contact your REDCap support team. See RC-TXT-02 — Texting: Administrator Setup for how administrators control provider visibility.

**Q: Does voice call work with Mosio?**
No. Voice calls are a Twilio-exclusive feature. If you need voice call survey delivery, you must use Twilio.

**Q: Can I text international phone numbers?**
With Twilio, yes — provided the appropriate country phone validation type is enabled in your REDCap installation and you have a Twilio number configured for that country's format. Mosio is limited to the US and Canada.

**Q: What does "overlapping SMS invitations" mean and which option should I choose?**
Overlapping invitations occur when a participant receives a second invitation before completing the first. Use "most recent only" for high-frequency surveys where only the latest matters; use "in-order" when survey results depend on each other; use "participant's choice" when survey completion order is flexible.

---

# 9. Common Mistakes & Gotchas

**Forgetting to include a survey link smart variable.** When sending a survey-as-webpage invitation, the message body must contain `[survey-url]` or `[survey-link]`. If omitted, participants receive a text message with no link and cannot access the survey. REDCap does not warn you about this at send time.

**Selecting a default invitation preference that conflicts with enabled invitation types.** If you set the default invitation preference to "SMS invitation (contains survey link)" but have not enabled "Survey as a webpage" in the invitation types setting, REDCap will generate an error. The default invitation preference must match one of the enabled types.

**Using SMS conversation without confirming administrator activation.** The SMS conversation option appears in the configuration menus regardless of whether an administrator has enabled it. If it has not been activated by an administrator, invitations set to SMS conversation will fail silently or error out at send time.

**Not setting up a phone variable before enabling ASI texting.** If you configure an ASI to send text invitations but no phone variable is defined (and participants were not added to the participant list with a phone number), REDCap has no number to text. The invitation will not be sent and no error appears in the record.

**Hard-coded alert phone numbers accumulating unintended charges.** An alert with a hard-coded phone number fires a text to that number every single time the alert is triggered. In a large project, an alert that fires on every form save can send hundreds or thousands of texts. Confirm your trigger logic carefully and consider budget limits before using hard-coded numbers in frequent alerts.

**Expecting the subject line to appear in text invitations.** REDCap ignores the subject line field for SMS and voice call invitations. Any content placed in the subject line will not be transmitted. For voice calls, REDCap also ignores the message body — only the survey content is read aloud.

---

# 10. Related Articles

- RC-SURV-01 — Surveys: Basics
- RC-SURV-05 — Participant List and Manual Survey Invitations
- RC-SURV-06 — Automated Survey Invitations
- RC-ALERT-01 — Alerts and Notifications Setup
- RC-TXT-02 — Texting: Administrator Setup (full admin setup: credentials, access control, provider configuration)
- RC-CC-06 — Control Center: Modules & Services Configuration (system-level Twilio/Mosio enablement and access permissions)
