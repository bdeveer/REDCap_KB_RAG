RC-MYCAP-04

**MyCap: Participant Onboarding**

| **Article ID** | RC-MYCAP-04 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | Projects with MyCap enabled |
| **Prerequisite** | RC-MYCAP-01 — MyCap: Overview & Enabling |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-MYCAP-05 — App Settings & Participant Management; RC-PIPE-16 — Smart Variables: MyCap; RC-ALERT-01 — Alerts & Notifications: Setup |

---

# 1. Overview

This article covers how participants join a MyCap project — from the initial requirement that a REDCap record must exist, through the two joining methods (App Links and QR Codes), to automated invitation workflows. It also covers the migration from Firebase Dynamic Links to App Links that took effect in August 2025, and guidance on the smart variable used to embed participant links in emails and messages. This article is for study coordinators configuring the onboarding workflow; participant-facing instructions are separate documentation provided by the study team.

---

# 2. Key Concepts & Definitions

**Record**

A REDCap data record representing a participant. Every participant must have a record in the REDCap project before they can join via MyCap. Participants cannot create their own records through the app.

**App Link**

A URL-based joining method. When a participant clicks or taps the App Link, the MyCap app opens (if installed) or the participant is redirected to the appropriate app store to install it first. After installing, the link automatically enrolls the participant in the project. App Links replaced Firebase Dynamic Links as of August 2025.

**Firebase Dynamic Link**

The legacy URL-based joining mechanism, deprecated August 25, 2025. Firebase Dynamic Links used the domain `mycapplusbeta.page.link`. Projects still using legacy links must update them. REDCap v15.3.3 and later handle this automatically; earlier versions require a manual URL replacement.

**QR Code**

A scannable code displayed by the study team (on screen or printed) that a participant scans using the MyCap app — not the device's standard camera app. The QR code contains the participant's unique project code, participant code, and institution identifier. Requires the MyCap app to be pre-installed on the participant's device.

**Participant Code**

A system-generated unique identifier for each record in MyCap. The participant code is embedded in both App Links and QR Codes and is what associates the participant's app activity with the correct REDCap record.

**Project Code**

A system-generated unique identifier for the REDCap project within MyCap. Embedded in the joining mechanism.

**Smart Variable**

A REDCap syntax expression that generates participant-specific values at runtime. The MyCap-specific smart variable `[mycap-participant-link]` generates an App Link for the current record. See RC-PIPE-16 — Smart Variables: MyCap for the full reference.

**Survey Completion Text**

A configurable message displayed to a participant after they complete a REDCap survey. Can include MyCap smart variables to deliver a joining link immediately after an enrollment survey.

---

# 3. Prerequisite: Record Must Exist First

Before a participant can join a MyCap project, a record for that participant must exist in REDCap. The study team (or an automated workflow) must create the record. Options:

- **Manual creation:** A coordinator creates the record in REDCap data entry.
- **Survey-based creation:** The participant completes an enrollment survey; REDCap auto-creates a record on survey submission. The joining link can then be delivered via Survey Completion Text or an automated alert.
- **Import:** Records are created via bulk import (RC-IMP-01 — Data Import Overview).
- **API:** Records are created programmatically (RC-API-03 — Import Records).

---

# 4. Joining Method 1: App Link

## 4.1 How App Links Work

An App Link is a URL unique to each participant (record). When clicked on a mobile device:

1. If MyCap is already installed: the app opens and the participant is automatically enrolled in the project.
2. If MyCap is not installed: the participant is redirected to the Apple App Store or Google Play Store to install MyCap. After installation, the participant returns to the link (or re-taps it) to complete enrollment.

App Links work well for **fully remote studies** where participants are not in-person with study staff.

## 4.2 Generating an App Link for a Participant

The App Link for a participant is available in two ways:

- **Smart variable:** Use `[mycap-participant-link:Custom Text]` in an email, alert, or Survey Completion Text to generate a clickable link. The raw URL can also be retrieved with `[mycap-participant-url]`. See RC-PIPE-16 — Smart Variables: MyCap.
- **Participant Management:** In the MyCap section of the left menu, go to **Participant Management**. The participant's App Link is displayed in their row and can be copied.

## 4.3 Firebase Dynamic Links Migration (August 2025)

Firebase Dynamic Links (domain: `mycapplusbeta.page.link`) were deprecated on August 25, 2025. All MyCap projects must use the new App Links (domain: `app.projectmycap.org`).

| REDCap version | Action required |
|---|---|
| v15.3.3 or later | None — REDCap auto-updates all links to the new domain |
| Earlier than v15.3.3 | Manually replace `mycapplusbeta.page.link` with `app.projectmycap.org` in every App Link URL |

The smart variable `[mycap-participant-link]` was also updated automatically in REDCap v15.3.3 and later — no changes needed to alert templates or survey completion text on upgraded systems.

> **Important:** If your institution is running REDCap earlier than v15.3.3 and you are sending participant App Links, verify your link domains. Legacy Firebase links that have already been sent to participants may no longer function. Contact your REDCap administrator to discuss upgrading.

---

# 5. Joining Method 2: QR Code

## 5.1 How QR Codes Work

A QR Code encodes the same joining information as an App Link but in scannable format. The participant scans the QR code using the **MyCap app's built-in QR scanner** — not the device's default camera app or a third-party scanner.

QR Code contents:
- Participant code (unique to the record)
- Project code (unique to the project)
- Institution identifier (links to the correct REDCap server)

## 5.2 Generating a QR Code

QR Codes are generated per-record in the **Participant Management** section:
1. In the MyCap section of the left menu, go to **Participant Management**.
2. Locate the participant's row.
3. Click **QR Code** to display the code on screen, or download/print it.

QR Codes can also be generated in bulk for multiple participants.

## 5.3 When to Use QR Codes vs. App Links

| Scenario | Recommended method |
|---|---|
| Participant is in-person with study staff; staff can show/print the QR code | QR Code |
| Study is fully remote; participant receives invitation by email or SMS | App Link |
| Participant does not yet have MyCap installed | App Link (redirects to app store) |
| Speed of enrollment is critical and app is already installed | Either |

---

# 6. Automated Invitation Delivery

Rather than manually sending each participant their joining link, you can automate delivery using standard REDCap tools.

## 6.1 Survey Completion Text

If participants complete an enrollment survey before joining MyCap, add the App Link smart variable to the survey's **Survey Completion Text** (the message shown on the final survey screen):

```
Thank you for completing enrollment!
Download the MyCap app and use this link to join the study:
[mycap-participant-link:Join the Study on MyCap]
```

The participant receives their unique link immediately after submitting the survey.

## 6.2 Alerts & Notifications

Use Alerts & Notifications (RC-ALERT-01) to send the App Link automatically based on a trigger (e.g., record creation, a status change):

1. Go to **Alerts & Notifications** in the left menu.
2. Create a new alert triggered by the appropriate condition (e.g., when a record is created).
3. In the email body, include the smart variable:
   ```
   [mycap-participant-link:Click here to join our study on MyCap]
   ```
4. Save and activate the alert.

Participants receive the email automatically when the trigger condition is met.

---

# 7. Step-by-Step: Onboarding a Participant (In-Person, QR Code)

1. Ensure the participant's record exists in REDCap.
2. Navigate to **MyCap > Participant Management** and locate the participant's record.
3. Display or print the QR code for the participant.
4. Instruct the participant to download and install the current MyCap app (purple logo) from the App Store or Google Play if not already installed.
5. In the MyCap app, the participant taps **Scan QR Code** and scans the code you displayed.
6. The app confirms enrollment and displays the participant's task list.

---

# 8. Step-by-Step: Onboarding a Participant (Remote, App Link)

1. Ensure the participant's record exists in REDCap.
2. Set up an Alert or Survey Completion Text with the `[mycap-participant-link:Custom Text]` smart variable (see Section 6).
3. The system sends the link automatically, or the coordinator copies the link from Participant Management and emails it manually.
4. The participant taps the link on their mobile device.
5. If MyCap is not installed: they are directed to the app store, install MyCap, and then return to the link.
6. If MyCap is installed: the app opens and enrollment completes automatically.

---

# 9. Common Questions

**Q: What if a participant uses the link on a desktop computer instead of their phone?**

**A:** App Links are designed for mobile devices. If accessed on a desktop, the participant will be directed to the MyCap website and will need to use their phone. Instruct participants to click the link on their iOS or Android device.

**Q: Can a participant join multiple projects?**

**A:** Yes. A participant can have multiple MyCap projects active on their device simultaneously, each with their own joining link or QR code.

**Q: What if a participant gets a new phone?**

**A:** The participant can install MyCap on the new device and use the same App Link or QR Code to rejoin. Their schedule and completed tasks will sync from the REDCap server.

**Q: Can participants join by entering the project code and participant code manually?**

**A:** No. Joining requires either scanning the QR code with the MyCap app or clicking the App Link. Manual code entry is not a supported joining workflow.

**Q: Do Firebase Dynamic Links still work after August 2025?**

**A:** No. Firebase Dynamic Links using the `mycapplusbeta.page.link` domain were deprecated August 25, 2025, and no longer function. Projects on REDCap v15.3.3+ are automatically updated; earlier versions require a manual URL replacement.

**Q: How does a participant know which version of MyCap to install?**

**A:** Instruct participants to search for "MyCap" in their device's app store and install the app with the purple logo from Vanderbilt University. The legacy app (MyCap Classic, black logo) is retired and should not be used.

**Q: Can I send the QR code by email instead of displaying it in person?**

**A:** Yes, but the QR code must still be scanned using the MyCap app's built-in scanner — not the phone's standard camera. If sending by email, ensure participants understand they must scan it from within MyCap, not from their camera app.

---

# 10. Common Mistakes & Gotchas

**Sending App Links before the participant's record exists.** The App Link is generated per-record. If no record exists yet, there is no link to send. Create the record first, then trigger the invitation.

**Participants scanning the QR code with their phone's default camera app.** The QR code must be scanned from inside the MyCap app using the app's built-in scanner. Scanning with the phone camera or a third-party app will not complete enrollment. Include explicit instructions with the QR code.

**Still using Firebase Dynamic Links (legacy URLs).** If your project is on a REDCap version earlier than v15.3.3 and you have not manually updated your App Link URLs, participants will receive broken links. Update `mycapplusbeta.page.link` to `app.projectmycap.org` in any URLs you are distributing.

**Forgetting to update alert or survey completion text templates after the Firebase migration.** Even if the Participant Management page shows updated links, stored alert email templates and survey completion text may still contain old Firebase URLs if they were saved as literal URLs rather than smart variables. Check and update these after migrating to REDCap v15.3.3+.

**Instructing participants to install MyCap Classic.** MyCap Classic is retired. If participants install the old app (black logo), they will not be able to connect to current projects properly. Always specify the purple-logo MyCap app.

---

# 11. Related Articles

- RC-MYCAP-01 — MyCap: Overview & Enabling
- RC-MYCAP-05 — App Settings & Participant Management (participant tracking and resending invitations)
- RC-MYCAP-08 — Testing MyCap (testing joining methods)
- RC-PIPE-16 — Smart Variables: MyCap (full smart variable reference)
- RC-ALERT-01 — Alerts & Notifications: Setup
