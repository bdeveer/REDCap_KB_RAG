RC-MSG-01

**REDCap Messenger**

| **Article ID** | RC-MSG-01 |
|---|---|
| **Domain** | Messenger |
| **Applies To** | All REDCap users; no project-specific setup required |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PROF-01 — My Profile: User Profile Settings; RC-USER-01 — User Rights: Overview & Three-Tier Access |

---

# 1. Overview

This article covers REDCap Messenger — a secure, built-in chat and file-sharing platform available to all REDCap users. Messenger allows users to send direct messages to individuals or communicate in group conversations without leaving REDCap. It is HIPAA-compliant, institution-hosted, and accessible from both the My Projects page and from within any individual project.

---

# 2. Key Concepts & Definitions

**REDCap Messenger**

A chat application built into REDCap that enables one-on-one and group messaging between REDCap users. Messenger is not an external service — it runs on the same server as your REDCap instance and inherits the same security and compliance posture.

**Conversation**

The primary organizational unit in Messenger. A conversation can be a direct (one-on-one) exchange or a group chat with multiple users. Each conversation has its own message history, member list, and title. Conversations can be archived or deleted by a conversation administrator.

**Conversation Administrator**

A user within a conversation who has management privileges: adding or removing members, renaming the conversation, and archiving or deleting it. Every conversation has at least one administrator — the user who created it. Additional administrators can be granted by the creator.

**Conversation Member**

A user who has been added to a conversation by an administrator but has not been granted administrator privileges. Members can view and post messages and attachments but cannot manage the conversation itself.

**@Mention (User Tagging)**

A way to notify a specific participant within a group conversation by typing `@username` in a message — for example, `@harrisjt`. Tagged users receive prioritized email notification if they are not currently logged in.

**Important / Urgent Flag**

A checkbox available when composing a message that marks it as important or urgent. Flagged messages receive priority treatment in email notifications sent to users who are offline.

**System Notification**

A non-message notification that appears in the Messenger panel, sent either by REDCap itself (e.g., new feature announcements) or by a REDCap Administrator (e.g., server downtime notices). System notifications do not generate email alerts.

---

# 3. Accessing Messenger

## 3.1 From the My Projects Page

Messenger is accessible from the top navigation bar on the My Projects page. Click **Messenger** in the top navigation to open the Messenger panel on the left side of the screen.

## 3.2 From Within a Project

When working inside any REDCap project, Messenger appears near the top of the left-hand project menu. Clicking it opens the same Messenger panel — all conversations are global to your REDCap account, not scoped to a single project.

## 3.3 Opening and Closing the Panel

Clicking the Messenger link opens the panel as an overlay on the left side of the page. To close it, click the **X** at the top right of the panel. Messenger will alert you to new messages without requiring the panel to remain open.

---

# 4. Creating and Managing Conversations

## 4.1 Creating a New Conversation

Any REDCap user can create a new conversation. When creating one, you automatically become its conversation administrator. From the Messenger panel, use the option to start a new conversation, give it a title, and add participants.

> **Important:** Avoid placing PHI or identifying information in a conversation's **title**. Titles are more broadly visible within the Messenger interface than message content. Place sensitive information only within the body of messages, where access is restricted to conversation members.

## 4.2 Adding Members and Granting Administrator Rights

As a conversation administrator, you can add other REDCap users to the conversation at any time. You may also grant administrator privileges to any member, giving them the same management capabilities as the conversation creator.

## 4.3 User Roles Within a Conversation

There are exactly two roles within any conversation:

| **Role** | **Capabilities** |
|---|---|
| Conversation Administrator | Add or remove members; rename the conversation; archive or delete the conversation; post messages and attachments |
| Conversation Member | View and post messages and attachments only |

## 4.4 Sharing Files and Images

Documents and images can be uploaded and shared directly within any conversation. There is no need to use email or external file-sharing services for project-related files. Attachments are stored securely on the REDCap server alongside the rest of your data.

---

# 5. Messaging Features

## 5.1 Tagging Users with @Mentions

In a group conversation, you can draw a specific user's attention by including `@username` anywhere in your message text — for example: *"Please review this, @jsmith."* The tagged user will be prioritized in any email notification Messenger sends if they are not currently logged in.

## 5.2 Marking Messages as Important

When composing a message, a **Mark as important** checkbox is available below the text field. Checking it flags the message as important or urgent. Like @mentions, important messages receive priority treatment in offline email notifications.

---

# 6. Notifications

## 6.1 Email Notifications for Unread Messages

If you receive a message while you are not logged in to REDCap, Messenger will send an email notification to your registered address after a short delay. The email notifies you that unread messages are waiting — it does **not** include the message content. You must log in to REDCap to read them.

## 6.2 Changing Notification Preferences

Email notification settings for Messenger are managed in your user profile. Navigate to the **Profile** page (accessible from the top right of the My Projects page), and look for the Messenger notification options at the bottom of the page.

## 6.3 System Notifications

From time to time, automated notices from REDCap itself or direct messages from your REDCap Administrators will appear in the Messenger panel. These may include announcements about new features, scheduled maintenance, or other institutional communications. System notifications do **not** generate email alerts — they are only visible when you open the Messenger panel.

---

# 7. Mobile and Compliance

## 7.1 Mobile Access

REDCap Messenger does not have a dedicated mobile app, but it is fully functional through a mobile browser. Log in to REDCap on your smartphone or tablet as you normally would, and Messenger will behave the same as on a desktop.

## 7.2 Security and Compliance

Messenger is hosted entirely on your institution's REDCap server. Messages are not routed through any third-party service. This design means Messenger can be used in the same compliance environments as REDCap itself, including HIPAA, GCP, 21 CFR Part 11, and FISMA.

## 7.3 Who Can Use Messenger

Messenger is intended for communication between REDCap users only. It cannot be used to contact survey participants or individuals who do not have a REDCap account at your institution.

---

# 8. Common Questions

**Q: Can I use REDCap Messenger to send messages to study participants?**

**A:** No. Messenger is designed for communication between REDCap users only. Participants who access REDCap only through surveys do not have REDCap user accounts and cannot be reached via Messenger. For participant communication, see the Alerts & Notifications feature (RC-ALERT-01) or Texting/SMS (RC-TXT-01).

**Q: Are my messages private? Can administrators read them?**

**A:** Messages are visible to all members of the conversation, including any conversation administrators. REDCap system administrators may have access to server-level data depending on local institutional policy. As with all REDCap data, messages are hosted locally at your institution.

**Q: I received an email saying I have unread messages, but the email doesn't show what they say. Is that correct?**

**A:** Yes, this is intentional. Email notifications deliberately omit message content to preserve security. You must log in to REDCap to read the messages.

**Q: How do I change how often I get email notifications from Messenger?**

**A:** Go to your Profile page (top right corner of My Projects) and scroll to the bottom of the page. The Messenger email notification preferences are located there.

**Q: Can I have multiple group conversations, and is there a limit?**

**A:** You can create as many conversations as you need. There is no stated limit on the number of conversations or members per conversation.

**Q: What is the difference between a conversation administrator and a regular member?**

**A:** An administrator can add or remove participants, rename the conversation, and archive or delete it. A member can only read and post messages and upload files. Every conversation has at least one administrator (the creator), and additional administrators can be appointed.

**Q: Does the Messenger panel need to stay open to receive messages?**

**A:** No. REDCap will notify you of new messages via the Messenger notification indicator even when the panel is closed, and will send an email notification if you are not logged in at all.

---

# 9. Common Mistakes & Gotchas

**Putting PHI in conversation titles.** Conversation titles are displayed more prominently in the Messenger interface than message content, making them more likely to be seen by people browsing the panel. PHI and identifying information should go in the body of messages only — not in titles.

**Using Messenger to contact survey participants.** Messenger only works between REDCap users. If a researcher expects to reach a participant through Messenger, that will not work — participants do not have REDCap accounts. Use Alerts & Notifications or the texting module for participant outreach.

**Expecting email notifications to contain message content.** Offline email alerts intentionally omit the message text for security reasons. Users who don't realize this sometimes assume a blank-looking notification email is an error. Clarify to team members that logging in is required to read the actual message.

**Assuming Messenger is project-scoped.** Messenger conversations are not tied to a specific project — they are associated with your REDCap user account across the entire system. A conversation started from inside one project is accessible from any other project or from the My Projects page.

---

# 10. Related Articles

- RC-PROF-01 — My Profile: User Profile Settings (where Messenger email notification preferences are configured)
- RC-ALERT-01 — Alerts & Notifications: Setup (for automated notifications to project team members or participants)
- RC-TXT-01 — Texting in REDCap: Setup and Usage (for SMS-based participant communication)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (for background on REDCap user accounts)
