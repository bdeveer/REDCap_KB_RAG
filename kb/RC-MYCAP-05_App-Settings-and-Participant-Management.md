RC-MYCAP-05

**MyCap: App Settings & Participant Management**

| **Article ID** | RC-MYCAP-05 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | Projects with MyCap enabled |
| **Prerequisite** | RC-MYCAP-01 — MyCap: Overview & Enabling |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-MYCAP-02 — Designing Instruments for MyCap; RC-MYCAP-04 — Participant Onboarding |

---

# 1. Overview

This article covers two related areas of the MyCap project configuration: App Settings and Participant Management. App Settings control how the app presents itself to participants — including the About pages, Contacts, Links, Theme, and Notification settings. Participant Management is the central hub for tracking who has joined, sending messages and announcements, and troubleshooting sync issues. Both are accessed from the MyCap section of the left-hand project menu.

---

# 2. Key Concepts & Definitions

**App Settings**

The section of the MyCap configuration where the study team customizes the app's appearance and branding for their project. Changes to App Settings require publishing before participants see them.

**About Page**

A customizable page within the MyCap app where the study team provides information about the project. Displayed to participants in the app's project information area.

**Contacts**

A section of App Settings where the study team lists contact information for participants who need help (e.g., coordinator phone number, study email). Must not include MyCap or Vanderbilt contact information.

**Links**

A section of App Settings where the study team can provide web links relevant to the study (e.g., study website, participant portal). Links can optionally include appended project or participant codes for integration with external participant portals.

**Theme**

Visual customization of the MyCap app's color scheme using Material Design. Currently available on iOS only; not available on Android.

**Notification Settings**

The time of day at which MyCap sends push notifications to participants when new tasks become available. Default is 8:00 AM local device time.

**Participant Management**

The central hub in the MyCap section for tracking participant enrollment status, sending messages, sending announcements, and reviewing sync issues.

**Message**

A direct message sent to one or more specific participants through MyCap. Participants receive a push notification and see the message in the app.

**Announcement**

A broadcast message sent to all participants in the project simultaneously. Useful for study-wide communications (e.g., app update reminders, study milestone messages).

**Sync Issue**

An error or warning logged when a participant's data fails to sync correctly from the app to the REDCap server. Visible in the Participant Management interface.

**Publish**

The action of pushing the current App Settings and project configuration to participants' devices. Required after any App Settings change.

---

# 3. App Settings

App Settings are accessed from **MyCap > App Settings** in the left-hand project menu. All App Settings changes require publishing before taking effect on participants' devices.

## 3.1 About Pages

About pages provide participants with information about the study. They appear in the app's project information section.

- **Image format:** PNG, 1024 × 1024 pixels recommended.
- **Minimum requirement:** At least one About page is required. The home/first About page cannot be deleted.
- **Multiple pages:** You can add multiple About pages to present extended project information (e.g., overview, contact procedures, FAQs).
- **Order:** Pages can be reordered.

> **Note:** About pages are static image-based pages. They cannot include interactive elements or dynamic content.

## 3.2 Contacts

The Contacts section allows the study team to provide participant-facing contact information.

- Add contacts with name, role, phone number, and/or email address.
- **Do not include MyCap or Vanderbilt contact information.** This section is for study-specific contacts only. Participants should contact study staff, not MyCap's development team.
- Contacts appear in the app under the project's contact section, giving participants a way to reach study staff directly from the app.

## 3.3 Links

The Links section allows the study team to add web links that participants can access from within the app.

- Each link has a display label and a URL.
- Links can include dynamic appended values using MyCap's link append feature:
  - Append the **project code** to the URL for project-level identification.
  - Append the **participant code** to the URL for participant-level identification.
  - This enables integration with external participant portals or result websites that need to identify the study and/or individual participant.

## 3.4 Theme

The Theme setting allows customization of the app's primary color using Material Design color options.

- Available on **iOS only**. Android does not support MyCap theme customization.
- The selected theme color is applied to the app's interface elements (buttons, highlights) for the project.

## 3.5 Notification Settings

Controls when MyCap sends push notifications to participants when new tasks become available.

- **Default:** 8:00 AM local device time.
- **Format:** 24-hour time format (e.g., 08:00, 20:00).
- All participants in the project receive notifications at the same configured time.
- Per-participant notification time customization is not currently supported.

---

# 4. Publishing App Settings Changes

After making any change to App Settings (About, Contacts, Links, Theme, Notification Settings):

1. Navigate to **MyCap > Publish MyCap Version**.
2. Review the summary of changes.
3. Click **Publish**.

Participants receive the updated App Settings on their next app open with internet connectivity.

---

# 5. Participant Management

Participant Management is accessed from **MyCap > Participant Management** in the left-hand project menu. It serves as the central hub for all participant-level activity in MyCap.

## 5.1 Participant Status Overview

The Participant Management table shows a row for each record in the project with MyCap-relevant status information:

| Column | Description |
|---|---|
| Record ID | The REDCap record identifier |
| Participant Code | The unique MyCap code for the participant |
| Join Status | Whether the participant has joined (enrolled) in the app |
| Last Sync | Date and time of the participant's most recent data sync |
| App Link / QR Code | Access to joining methods for this participant |
| Messages | Number of sent messages |
| Sync Issues | Flag if sync errors are present |

## 5.2 Invitations

From Participant Management, you can view whether a participant has joined. For participants who have not yet joined:

- Copy or resend the App Link from their row.
- Display or download their QR code.

For automated invitation workflows, see RC-MYCAP-04 — Participant Onboarding.

## 5.3 Sending Messages

Messages are direct communications to specific participants. They appear in the participant's app as a message notification.

**To send a message to one participant:**
1. Locate the participant's row in Participant Management.
2. Click **Send Message** (or the message icon).
3. Enter the message subject and body.
4. Click **Send**.

**To send a message to multiple participants:**
1. Select multiple participants using the checkboxes.
2. Click **Send Message** from the bulk actions toolbar.
3. Enter the message and send.

The participant receives a push notification and the message appears in the MyCap app's messages section.

## 5.4 Sending Announcements

Announcements are broadcast to all participants in the project simultaneously.

1. In Participant Management, click **Send Announcement**.
2. Enter the announcement subject and body.
3. Click **Send**.

All currently enrolled participants receive the announcement as a push notification and it appears in the app.

**Appropriate uses for announcements:**
- Reminding participants to update the MyCap app.
- Notifying participants of a study milestone or change.
- Sending holiday or seasonal messages.
- Communicating maintenance windows.

## 5.5 Troubleshooting Sync Issues

If a participant's data fails to sync correctly, a sync issue flag appears in their row in Participant Management.

**To review a sync issue:**
1. Click the sync issue icon or flag for the relevant participant.
2. Review the error description — this typically includes information about which instrument or record was affected and the nature of the error.

**Common causes of sync issues:**
- The participant's record has been deleted in REDCap.
- The instrument the participant completed is no longer enabled for MyCap.
- A field on the instrument has been deleted or renamed after the participant completed the task.
- The participant's record has been locked.

**Resolution:** After identifying the cause, correct it in REDCap (e.g., re-enable the instrument, restore the deleted field, unlock the record). The participant's next sync attempt should succeed. If the issue persists, contact your REDCap administrator.

---

# 6. Common Questions

**Q: Can I customize the notification time per participant?**

**A:** No. Notification time is a project-level setting that applies to all participants. Per-participant notification scheduling is not currently supported. Participants can sometimes adjust their device-level notification settings, but the MyCap app's push notification time itself is set project-wide.

**Q: What happens if I do not publish after changing App Settings?**

**A:** Participants continue to see the previous version of the App Settings. Changes are staged but not delivered until a Publish action is performed.

**Q: Can participants see messages from the study team in the app?**

**A:** Yes. Messages sent via Participant Management appear in the participant's MyCap app in a messages inbox. The participant also receives a push notification.

**Q: How do I know if a participant has joined?**

**A:** The Join Status column in Participant Management shows whether a participant has enrolled in the app. You can also see the date of their last sync.

**Q: Can I delete an About page?**

**A:** The home (first) About page cannot be deleted — at least one About page must exist. Additional pages can be deleted.

**Q: What format should About page images be?**

**A:** PNG format, 1024 × 1024 pixels. Other formats or sizes may not display correctly.

**Q: Can the links in the Links section include participant-specific information?**

**A:** Yes. When adding a link in App Settings, you can configure it to append the project code, participant code, or both to the URL. This enables integration with external websites or portals that need to identify the participant.

---

# 7. Common Mistakes & Gotchas

**Including MyCap or Vanderbilt contact information in the Contacts section.** The Contacts section is for study-specific contacts only. Do not include MyCap support or Vanderbilt University contact details. Participants with app technical issues should be directed to the study team, who can then contact REDCap support if needed.

**Forgetting to publish after App Settings changes.** App Settings changes — including About page updates, new contacts, theme changes, and notification time changes — are not visible to participants until the project is published. Always publish after making App Settings changes.

**Sending announcements for individual participant issues.** Announcements go to all participants. For issues specific to one participant, use the direct message feature instead.

**Expecting the Android theme to apply.** The Theme customization is iOS-only. Android participants see the default MyCap interface regardless of the theme setting.

**Not checking sync issues promptly.** Unresolved sync issues mean participant data is not reaching REDCap. Check Participant Management regularly, especially after making instrument changes (renaming or deleting fields can cause sync failures for participants who have completed tasks with those fields).

---

# 8. Related Articles

- RC-MYCAP-01 — MyCap: Overview & Enabling
- RC-MYCAP-02 — Designing Instruments for MyCap (publishing workflow)
- RC-MYCAP-04 — Participant Onboarding (invitation and joining methods)
- RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links
- RC-MYCAP-08 — Testing MyCap (testing App Settings and notifications)
