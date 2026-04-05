RC-PIPE-16

**Smart Variables: MyCap**

| **Article ID** | RC-PIPE-16 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with REDCap MyCap module enabled |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview |

---

# 1. Overview

MyCap smart variables provide participant-facing links and codes specific to REDCap's MyCap mobile application. These variables generate URLs and access codes that allow participants to enroll in a REDCap project using the MyCap app on their mobile device. Use MyCap smart variables in field notes, survey invitations, emails, and confirmation messages to enable easy mobile enrollment. These variables are only available in projects with the MyCap module enabled.

---

# 2. Key Concepts & Definitions

**REDCap MyCap**

A mobile application (iOS and Android) that allows research participants to access surveys and complete data collection on their smartphones. MyCap provides an alternative to web-based survey access and offers mobile-optimized interfaces.

**MyCap Project Code**

A unique identifier assigned to each REDCap project that uses MyCap. The project code is system-generated and is used to identify the project within the MyCap app environment.

**Participant Code**

A unique identifier for each record (participant) in a MyCap-enabled project. The participant code is system-generated and allows MyCap to associate the participant's mobile app activity with the correct REDCap record.

**MyCap Enrollment Link**

A special URL that allows a participant to join a REDCap project through the MyCap mobile app. The link is unique to each participant and includes the necessary codes to authorize and configure the app connection.

**MyCap Participant Link**

An HTML link (usually embedded in an email or field note) that directs participants to enroll in a project via the MyCap app.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| MyCap Project Code | `[mycap-project-code]` | The unique system-generated code for the current REDCap project within the MyCap ecosystem. This code identifies the project when users enroll via MyCap. | P-5CLDRMQ28TSJJXD7KA1K |
| MyCap Participant Code | `[mycap-participant-code]` | The unique system-generated code for the current record (participant). This code associates the participant's mobile app activity with the correct REDCap record. | U-NEXAXSMQZ3YFTZDMMSEX |
| MyCap Participant URL | `[mycap-participant-url]` | The web address (URL) for the current record that can be used by the participant to join the project on the MyCap mobile app. The URL includes all necessary enrollment parameters. | https://mycap.link/join/... |
| MyCap Participant Link (Default) | `[mycap-participant-link]` | An HTML web link for the current record that allows the participant to join the project on the MyCap mobile app. Uses the URL as the default link text. | [Clickable link with URL text] |
| MyCap Participant Link (Custom Text) | `[mycap-participant-link:Custom Text]` | An HTML web link for the current record with custom link text instead of the URL. | [Clickable link labeled "Click this MyCap link"] |

---

# 4. Usage Notes

**MyCap Module Required**

All MyCap smart variables only function if your project has the REDCap MyCap module enabled. Projects without MyCap enabled will return blank values when attempting to use these variables. Contact your REDCap administrator if you need to enable MyCap for your project.

**Participant-Facing vs. Administrator Context**

MyCap smart variables are designed to be placed in participant-facing communications (emails, surveys, field notes visible to participants). They are most useful in:
- Survey invitation emails to participants.
- Confirmation or welcome messages.
- Field notes that instruct participants on how to enroll via MyCap.
- MyCap-specific instructions or documents.

Avoid using MyCap variables in administrator-only forms or data entry contexts.

**Unique Codes Per Record**

The `[mycap-participant-code]` and `[mycap-participant-url]` are unique to the current record. Each record has its own code and enrollment URL. This ensures that when multiple participants enroll via MyCap, each is associated with the correct REDCap record.

**Link Customization**

Use `[mycap-participant-link:Custom Text]` to generate a link with custom text instead of the default URL. Examples:
- `[mycap-participant-link:Download the MyCap app and enroll]`
- `[mycap-participant-link:Join us on MyCap]`
- `[mycap-participant-link:Complete surveys on your phone]`

**URL Format**

The MyCap URL is long and includes enrollment parameters. It should be treated as an opaque string — do not attempt to parse or modify it. If you need a custom link label, use `[mycap-participant-link:Custom Text]` instead of working with the raw URL.

**Email and Invitation Context**

MyCap links are most useful in survey invitation emails and project enrollment communications. For example:

```
Dear [participant_name],

You have been invited to enroll in our research study.
Please download the MyCap app from your device's app store
and use this link to enroll: [mycap-participant-link:Enroll on MyCap]

Thank you!
```

**MyCap Project Code Use Cases**

The `[mycap-project-code]` is primarily for reference and troubleshooting. It is rarely needed in participant communications. It may be useful in:
- Support documents or FAQs for participants who are troubleshooting enrollment.
- Internal documentation about the project's MyCap configuration.
- System logs or error messages that reference the MyCap project.

**Participant Code for Support**

The `[mycap-participant-code]` can be included in support materials or error messages to help troubleshoot issues with a specific participant's MyCap enrollment. It is not typically useful to display to participants themselves unless they need to contact support.

---

# 5. Common Questions

**Q: How do I send a participant a link to enroll in my project via MyCap?**

**A:** Use `[mycap-participant-link:Custom Text]` in a survey invitation email or field note. For example:
```
[mycap-participant-link:Enroll in our study using MyCap]
```
This generates a clickable link that will direct the participant to the MyCap enrollment page.

**Q: What is the difference between the MyCap URL and the MyCap link?**

**A:** `[mycap-participant-url]` is the raw web address. `[mycap-participant-link]` is an HTML link that users can click. Use `[mycap-participant-link]` in emails and forms for a clickable link; use `[mycap-participant-url]` only if you specifically need the raw address (rarely necessary).

**Q: Can I include the MyCap link in an automated survey invitation?**

**A:** Yes. If your project uses Alerts & Notifications to send automated emails, you can include `[mycap-participant-link:Custom Text]` in the email body. Participants will receive the link and can click it to enroll via MyCap.

**Q: What is the MyCap project code used for?**

**A:** The project code is a system identifier used by the MyCap app to recognize your project. It is primarily used internally and in troubleshooting. You do not typically need to share it with participants. If a participant is having trouble enrolling, you might reference the project code in a support document.

**Q: Can I create a QR code from the MyCap enrollment link?**

**A:** Yes. You can generate a QR code from the `[mycap-participant-url]` and include it in print materials, posters, or other physical documents. Participants can scan the QR code with their phone to be directed to the MyCap enrollment page.

**Q: What if my project doesn't have MyCap enabled?**

**A:** MyCap smart variables return blank if the MyCap module is not enabled. Contact your REDCap administrator to request MyCap enablement if you need these variables.

**Q: How do participants use the MyCap link?**

**A:** Participants click or tap the link, which directs them to the MyCap enrollment page. They must have the MyCap app already installed on their mobile device. The app will open and guide them through enrollment using the participant code and project code embedded in the link.

---

# 6. Common Mistakes & Gotchas

**Using MyCap smart variables in projects without MyCap enabled.** If your project does not have the MyCap module, these variables return blank or produce errors. Verify that your project has MyCap enabled before relying on these variables.

**Confusing MyCap links with survey links.** `[mycap-participant-link]` is for mobile app enrollment via MyCap. `[survey-link]` is for web-based survey access. They serve different purposes. Use the appropriate smart variable based on how you want participants to access your study.

**Not providing the MyCap link in participant communications.** If participants are not aware that they can enroll via MyCap, they will not use the mobile app. Clearly communicate the MyCap link in emails, invitations, and welcome messages.

**Assuming participants have the MyCap app installed.** Participants must download the MyCap app from their device's app store before they can use a MyCap enrollment link. Provide clear instructions on how to download the app, or consider offering both web-based and MyCap enrollment options.

**Using MyCap variables in internal/administrator forms.** MyCap smart variables are designed for participant-facing communications. Placing them in internal forms or administrative contexts is confusing. Use them only in communications directed at participants.

**Not testing MyCap links on actual mobile devices.** MyCap links are designed for mobile access. Test enrollment on an actual iOS or Android device before deploying to real participants.

**Exposing MyCap codes unnecessarily.** While the participant code and project code are not highly sensitive, avoid sharing them unnecessarily. The important security element is the enrollment URL, which should be shared only with intended participants.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-08 — Smart Variables: Survey (survey-based smart variables for web enrollment)
- RC-ALERT-01 — Alerts and Notifications Setup (using MyCap links in automated emails)
