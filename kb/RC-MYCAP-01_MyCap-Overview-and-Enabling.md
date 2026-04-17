RC-MYCAP-01

**MyCap: Overview & Enabling**

| **Article ID** | RC-MYCAP-01 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | All project types; MyCap module must be enabled at the institutional level |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-MYCAP-02 — Designing Instruments for MyCap; RC-MYCAP-03 — Task Scheduling; RC-MYCAP-04 — Participant Onboarding; RC-MOB-01 — REDCap Mobile App *(coming soon)* |

---

# 1. Overview

This article introduces MyCap, the participant-facing mobile application built into REDCap. It covers what MyCap is, when to use it, how it compares to the REDCap Mobile App, the difference between the current MyCap app and the legacy MyCap Classic, security architecture, and how to enable MyCap on a project. This is the first article in the RC-MYCAP series. For instrument design, scheduling, and onboarding, see the subsequent articles in this series.

---

# 2. Key Concepts & Definitions

**MyCap**

The participant-facing mobile application for REDCap. MyCap is installed on a participant's personal iOS or Android device and allows them to complete surveys and active tasks on their own schedule. Data is stored locally on the device when offline and synced to the REDCap project when internet connectivity is available.

**MyCap Task**

Any REDCap instrument or active task enabled for completion in the MyCap app. Tasks appear in the participant's app according to a project-defined schedule. The term "task" is used throughout MyCap instead of "instrument" or "form."

**REDCap Mobile App**

A separate mobile application used by the *study team* (not participants) to enter data offline from a study team–owned device. The REDCap Mobile App requires a REDCap login. It is distinct from MyCap in purpose and audience. See RC-MOB-01 — REDCap Mobile App *(coming soon)* for details.

**MyCap Classic**

The original MyCap app (black background, black logo). Retired in August 2024. No longer receives updates. All new projects must use the current MyCap app.

**MyCap (current app)**

The rewritten MyCap app released in September 2023 (purple background, purple logo). Built with Flutter. Requires REDCap v13.10.0 or later. Adds longitudinal project support, participant dashboards, image and video capture, multi-user device support, and full feature parity between iOS and Android.

**App Link**

A URL-based method for participants to join a MyCap project. Clicking the link opens the app if installed, or redirects to the appropriate app store if not. Replaced Firebase Dynamic Links (deprecated August 25, 2025). See RC-MYCAP-04 — Participant Onboarding for full details.

**Active Task**

A mobile sensor–based assessment built into MyCap (e.g., tapping speed, gait and balance, audio recording). Active Tasks use device hardware and are distinct from instrument-based surveys. See RC-MYCAP-06 — Active Tasks & Mobile Toolbox.

**Publish**

The action of pushing the current MyCap project configuration (schedule, App Settings) out to participants' devices. Most changes require publishing before participants see them. MLM changes and Form Display Logic changes do not require publishing.

---

# 3. When to Use MyCap

## 3.1 Decision Framework

Use this table to decide which REDCap data collection method fits a study's needs:

| Scenario | Recommended tool |
|---|---|
| Study team entering data at point of care, offline | REDCap Mobile App |
| Single data collection via survey link (email/SMS) | REDCap survey (web browser) |
| Brief, infrequent SMS-based collection | Twilio / Mosio (see RC-TXT-01 *(coming soon)*) |
| Participant-reported outcomes collected frequently over time | **MyCap** |
| Participants completing multiple tasks per day | **MyCap** |
| Active sensor-based assessments (gait, cognition, hearing) | **MyCap** |
| Offline participant data collection on participant's own device | **MyCap** |

## 3.2 MyCap vs. REDCap Mobile App

| Feature | MyCap | REDCap Mobile App |
|---|---|---|
| Who uses it | Research participants | Study team members |
| Installed on | Participant's personal device | Study team device |
| Requires REDCap login | No | Yes |
| Primary use case | Remote, repeated participant data collection | Offline data entry at point of care |
| Internet required | No (syncs when available) | No (syncs when available) |
| Supports active tasks | Yes | No |
| Longitudinal projects | Yes (new MyCap only) | Yes |

---

# 4. MyCap Classic vs. Current MyCap App

## 4.1 Version History

| | MyCap Classic | MyCap (current) |
|---|---|---|
| Logo color | Black | Purple |
| Release date | Original release | September 2023 |
| Framework | — | Flutter (full rewrite) |
| Minimum REDCap version | — | v13.10.0 |
| Retirement / status | Retired August 2024 | Active — use for all new projects |
| Longitudinal projects | No | Yes |
| Participant dashboard | No | Yes |
| Image / video capture | No | Yes |
| Multi-user device support | No | Yes |
| iOS/Android feature parity | Partial | Full |

## 4.2 Action Required

All new projects must direct participants to the current (purple) MyCap app. MyCap Classic is no longer supported and will not receive updates or bug fixes. Participants on MyCap Classic should be prompted to update to the current app.

---

# 5. Security Architecture

MyCap uses the following security controls for data protection in transit and at rest:

- **AES-256 + SHA2** encryption for data stored on the participant's device
- **TLS v1.2** for all data in transit between the device and the REDCap server
- **HMAC** (Hash-Based Message Authentication Code) to verify data integrity

These controls meet common institutional and IRB requirements for mHealth data collection. Consult your institution's IRB for the approved language describing MyCap's security posture. Template IRB language is available on the MyCap website.

> **Institution-specific:** Some IRBs have pre-approved MyCap security language for use in consent documents. Contact your IRB or REDCap administrator to determine whether pre-approved language is available at your institution.

---

# 6. Enabling MyCap on a Project

## 6.1 Institutional Requirement

MyCap must first be enabled at the institutional (server) level. If you do not see the MyCap option in your project, contact your REDCap administrator.

> **Institution-specific:** Whether MyCap is available by default or requires an administrator request varies by installation. Contact your REDCap administrator to confirm availability.

## 6.2 Enabling MyCap in Your Project

1. From the project's left-hand menu, go to **Project Setup**.
2. In the **Enable optional modules and customizations** section, check **Enable MyCap for this project**.
3. Click **Save**.

Once enabled, a **MyCap** section appears in the left-hand menu with subsections for enabling instruments, scheduling tasks, App Settings, and Participant Management.

## 6.3 Prerequisites Before Enabling

- Instruments (forms) should be designed before enabling them for MyCap. See RC-MYCAP-02 — Designing Instruments for MyCap.
- At least one record must exist in REDCap before a participant can join via the app. Participants cannot create their own records.

---

# 7. MyCap Limitations

The following REDCap features are not supported within MyCap tasks (instrument-based surveys displayed in the app):

| Unsupported feature | Notes |
|---|---|
| REDCap piping | Field values cannot be piped into MyCap instruments |
| Most REDCap action tags | `@HIDDEN` is honored; MyCap has its own mobile-specific action tags (see RC-MYCAP-02) |
| Calculated fields | Use Survey Links as a workaround to display calculated results (see RC-MYCAP-07) |
| Cross-instrument branching logic | Branching logic within a single instrument is supported; logic that references fields on other instruments is not |
| Push notification scheduling | Notifications are sent at 8:00 AM local device time; this time cannot currently be customized per participant |
| Smart variables (REDCap piping) | Not rendered in MyCap instruments |

REDCap Multi-Language Management (MLM) is supported in MyCap. See RC-MYCAP-07 — Advanced Features for setup details.

---

# 8. Common Questions

**Q: Is MyCap the same as the REDCap Mobile App?**

**A:** No. MyCap is for research participants and is installed on the participant's own device. The REDCap Mobile App is for study team members and requires a REDCap login. They serve different populations and different use cases.

**Q: My project doesn't show a MyCap option. Why?**

**A:** MyCap must be enabled at the server level by a REDCap administrator before it appears in any project. Contact your REDCap admin. Once available institution-wide, you enable it per-project in Project Setup.

**Q: Can I use MyCap with a longitudinal project?**

**A:** Yes, with the current MyCap app (purple logo, released September 2023), longitudinal projects are supported. MyCap Classic did not support longitudinal projects. See RC-MYCAP-03 — Task Scheduling for longitudinal scheduling details.

**Q: What iOS and Android versions does MyCap support?**

**A:** The current MyCap app requires iOS 13.0 or later and Android 7.0 or later.

**Q: Can participants complete tasks without an internet connection?**

**A:** Yes. MyCap stores completed task data locally on the device when offline. Data syncs to the REDCap project the next time the participant opens the app with internet connectivity.

**Q: Do I need to "publish" changes before participants see them?**

**A:** Most changes — including schedule changes and App Settings changes — require publishing before they reach participants' devices. Some changes (Form Display Logic, MLM translations) apply immediately without publishing. See RC-MYCAP-02 and RC-MYCAP-07 for specifics.

**Q: Can one participant use MyCap on multiple devices?**

**A:** Yes, the current MyCap app supports multi-user and multi-device scenarios. MyCap Classic did not support this.

**Q: Is MyCap free for participants?**

**A:** Yes. The MyCap app is free to download from the Apple App Store and Google Play Store. There is no cost to participants.

---

# 9. Common Mistakes & Gotchas

**Directing participants to MyCap Classic.** MyCap Classic (black logo) was retired in August 2024. If participants download the classic app, they will not receive updates, and some features will not work. Always instruct participants to search for and install the current MyCap app (purple logo).

**Expecting REDCap piping to work inside MyCap tasks.** Piping syntax in field labels, notes, or validation text is not rendered in MyCap — it displays as raw bracket syntax (e.g., `[first_name]`). Remove piping from instruments intended for MyCap, or use a Survey Link (RC-MYCAP-07) to display personalized content.

**Enabling MyCap before designing instruments.** Instruments that were not designed with MyCap in mind (relying on piping, calculated fields, or unsupported action tags) will behave unexpectedly in the app. Review field compatibility (RC-MYCAP-02) before enabling instruments.

**Assuming calculated fields update in MyCap.** Calculated fields do not compute inside MyCap. If you need to show participants a calculated value (e.g., a score), use the Survey Links feature to embed a REDCap survey link instead (see RC-MYCAP-07 — Advanced Features).

**Not publishing after configuration changes.** Schedule changes, App Settings changes, and newly enabled instruments do not reach participants' devices until the project is published. See RC-MYCAP-02 for publishing steps.

---

# 10. Related Articles

- RC-MYCAP-02 — Designing Instruments for MyCap
- RC-MYCAP-03 — Task Scheduling
- RC-MYCAP-04 — Participant Onboarding
- RC-MYCAP-05 — App Settings & Participant Management
- RC-MYCAP-06 — Active Tasks & Mobile Toolbox
- RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links
- RC-MYCAP-08 — Testing MyCap
- RC-MOB-01 — REDCap Mobile App *(coming soon)*
- RC-PIPE-16 — Smart Variables: MyCap
- RC-INST-01 — Institution-Specific Settings & Policies
