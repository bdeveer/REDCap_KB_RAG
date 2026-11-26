---
id: RC-TXT-02
title: 'Texting: Administrator Setup'
domain: Texting (SMS)
applies_to:
- REDCap administrators with "Modify system configuration pages" permission
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — texting
  administration behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-TXT-01 — Texting in REDCap: Setup and Usage'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-TXT-01
  title: 'Texting in REDCap: Setup and Usage'
tags:
- texting (sms)
synonyms:
- how do i enable texting across the whole installation
- connect twilio to redcap as an administrator
- system level sms configuration
- set texting permission levels for users
- control who can use texting in projects
- configure mosio in the control center
- admin setup for redcap sms
- enable texting system-wide
---

# 1. Overview

This article covers the system-level texting settings a REDCap administrator controls: whether Twilio and Mosio are available on the installation, which users can enable texting in their projects, and which phone validation types projects can use. On a fresh REDCap install **both Twilio and Mosio are enabled for all users**, so any user with Project Design and Setup rights can switch texting on in their own project. Review these settings early and restrict them to match your institution's policy. Project-level setup (enabling and configuring texting within an individual project) is covered in [RC-TXT-01 — Texting in REDCap: Setup and Usage](RC-TXT-01_Texting-in-REDCap-Setup-and-Usage.md).

> **Required permissions:** You must have REDCap administrator access and the ability to "Modify system configuration pages" in the Control Center to perform any steps in this article.

---

# 2. Key Concepts & Definitions

## Control Center
The administrative interface in REDCap accessible only to users with administrator privileges. System-wide settings — including texting configuration — are managed here.

## Modules/Services Configuration page
The page within the Control Center's **System Configuration** section where Twilio and Mosio are enabled or disabled and permission-leveled for the entire REDCap installation. It holds no Twilio or Mosio account credentials; those are entered per project.

## Permission level
A per-provider setting that controls who can enable Twilio or Mosio within an individual project: all users with Project Design rights, users who have received administrator approval, or administrators only.

## Field Validation Types page
A Control Center page listing all validation types available to projects, including the phone number formats used for texting. Some phone formats ship disabled and only need to be enabled. Adding a brand-new type on this page is possible from REDCap 17.4.0; on earlier versions it needs your server team.

## Test connection button
A button on the Modules/Services Configuration page that checks whether REDCap can reach the texting provider's servers. It is a diagnostic aid: REDCap does not stop you enabling a provider if you have not run it, but a failed test means texting will not work.

---

# 3. Enabling a Texting Provider System-Wide

## 3.1 Navigate to the configuration page

1. Open the **Control Center** from the top navigation menu.
2. Under **System Configuration**, click **Modules/Services Configuration**.
3. Scroll to approximately the middle of the page to find the **Twilio** and **Mosio** configuration sections.

## 3.2 Test the connection

Before relying on either service, check that your REDCap server can reach the provider's API:

1. Click the **Test** button in the provider's section.
2. If the connection succeeds, a confirmation popup appears.
3. If the connection fails, REDCap cannot reach the provider. Check your institution's firewall rules and network configuration. REDCap will still let you save the provider as enabled, but projects will not be able to send messages until the connection works.

The **Configuration Check** page (Control Center → System Configuration) also re-tests the connection to both services.

## 3.3 Enable or restrict the provider

1. Use the dropdown in the provider's section to set the service to **Enabled** or **Disabled**.
2. Click **Save** at the bottom of the page. Nothing on this page takes effect until you save.

Because both providers are enabled for all users on a fresh install, many institutions use this step to disable a provider they do not support, or to tighten the permission level (Section 4).

Both Twilio and Mosio can be enabled simultaneously in the same REDCap installation. Individual projects may only activate one provider at a time, but different projects can use different providers.

## 3.4 Account credentials are entered per project

There are no system-level Twilio or Mosio credentials for projects. Each project that uses texting enters its own provider account details in Project Setup: for Twilio, the Account SID, Auth Token and Twilio phone number; for Mosio, the project's API key. The Control Center does hold Twilio settings elsewhere, but those are used only for two-factor login text messages, not for project texting.

## 3.5 Server and provider requirements

- **Your REDCap server must be publicly reachable.** Twilio and Mosio call back to REDCap (for example to deliver incoming replies and delivery status). If your server is only reachable on an internal network, those callbacks fail.
- **Voice calls are Twilio only.** Mosio supports text messages only.
- **An alphanumeric sender ID turns off voice and inbound SMS.** If a project's Twilio number is an alphanumeric sender ID rather than a phone number, that project can send outgoing texts only: voice calls and incoming SMS replies are not available.

## 3.6 Turning Twilio off for a single project

Administrators can switch Twilio on or off for one project in **Control Center → Edit a Project's Settings**. Use this to stop texting in a specific project without changing the system-wide setting.

---

> **Admin approval workflow.** The Twilio and Mosio settings on the Modules/Services Configuration page carry an option requiring **administrator approval** before a project can enable texting, rather than letting project designers switch it on themselves. (Reported as arriving in REDCap 15.6.0, so it is present on all supported versions.) Given that texting incurs per-message cost against an institutional account, this is usually the setting institutions want. See [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md).

---

# 4. Setting the Permission Level

After enabling a provider, define who is allowed to activate it in individual projects.

## 4.1 Permission options

| Permission level | Behavior |
|---|---|
| All users | Any user with Project Design and Setup rights can enable and configure texting in their project without administrator involvement. This is the default on a fresh install. |
| Admin Approval | Any user with Project Design and Setup rights can fill in the texting settings in Project Setup, but the save button reads **Request to enable Twilio** (or **Request to enable Mosio**) instead of saving directly. The user's credentials are entered and validated first; the request then goes to REDCap administrators by email and appears in the Control Center **To-Do List**. While waiting, the button shows **Request pending**. The submitted credentials are held until an administrator approves the request, and texting is not active until then. |
| Only Administrators | Only REDCap administrators can enable texting in any project. Non-administrators cannot enable it, and they also lose the ability to modify texting settings in projects where it is already enabled. |

## 4.2 Hiding the feature from non-administrators

When **Only Administrators** is selected, a secondary option controls whether non-administrators can see that texting exists:

- **Yes, display information** — the Enable button is visible to users but greyed out (non-clickable). Users know texting is a feature but must contact an administrator to use it.
- **No, hide all information** — Twilio/Mosio options do not appear in Project Setup for non-administrators. Use this when you want to enable texting for select projects without advertising it to all users.

> **Note:** Even when texting is hidden from non-administrators, the administrator view of Project Setup shows the Enable button and all configuration options normally.

## 4.3 Save after any permission change

After adjusting permission settings, click **Save** at the bottom of the Modules/Services Configuration page. Nothing applies until the page is saved; once saved, the change takes effect straight away.

---

# 5. Verifying Phone Validation Types

REDCap uses field validation types to ensure phone numbers are formatted correctly before they are passed to Twilio or Mosio.

## 5.1 Check existing validation types

1. In the Control Center, navigate to **Field Validation Types**.
2. Review the list of phone validation entries. At minimum, **Phone (North America)** should be present and enabled. Mosio is intended for US and Canadian numbers and uses this format; Twilio uses it for US/Canada numbers.
3. If you are offering Twilio for international use, check the relevant country format. **Phone (Australia)**, **Phone (UK)** and **Phone (France)** are included with REDCap but ship **disabled**, so in most cases you only need to enable the one you need.

## 5.2 Add a missing validation type

If the country format you need is not on the list at all, you need a new custom validation type. The format of phone validation types varies by country, so consult the REDCap Community for existing custom phone validation definitions before creating one from scratch.

- **REDCap 17.4.0 and later (Standard):** add it directly on the **Field Validation Types** page. A new type starts disabled; enable it before project designers can choose it. See [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md).
- **LTS 16 and 17.3:** the page cannot add new types. Adding one requires a database change, so ask your server team.

> **Note:** Mosio is a North American service; adding non-North American validation types is only relevant for Twilio installations serving international participants.

---

# 6. Common Questions

**Q: Can both Twilio and Mosio be enabled in the same REDCap installation?**
Yes. Both can be active at the system level simultaneously, and on a fresh install both are. Individual projects choose one or the other when enabling texting — they cannot use both at the same time.

**Q: What does "Admin Approval" mean in practice for the user?**
The user with Project Design rights fills in the texting settings in Project Setup, and REDCap validates the credentials. Instead of a normal save, they click **Request to enable Twilio** (or **Request to enable Mosio**), which emails REDCap administrators and adds an item to the Control Center To-Do List. The button then shows **Request pending**. An administrator reviews and approves the request; until then, texting is not functional in that project and the submitted credentials are held waiting for approval.

**Q: If I switch the permission level from "All users" to "Only Administrators," what happens to projects that already have texting enabled?**
Texting keeps working in those projects. However, non-administrator users in those projects can no longer modify the texting settings; changes from then on must be made by an administrator.

**Q: Do I need to configure Twilio or Mosio credentials in the Control Center?**
No. Both providers use per-project credentials that project designers (or administrators) enter in Project Setup: Account SID, Auth Token and phone number for Twilio, an API key for Mosio. The Twilio settings found elsewhere in the Control Center are only for two-factor login and are not used by projects.

**Q: How do I disable texting across the entire installation?**
Set the provider's dropdown to **Disabled** on the Modules/Services Configuration page and save. This stops texting in every project using that provider, including active ones: SMS and voice survey invitations are no longer sent, and alerts that would have gone by text fall back to email. Warn affected project teams before you do this. To stop texting in one project only, use **Control Center → Edit a Project's Settings** instead (Twilio).

**Q: A user says they cannot see the texting option in their project. What should I check?**
First, confirm the provider is enabled in the Control Center. Then check the permission level — if it is set to "Only Administrators" with the "No, hide all information" option, the user will not see any texting option. Finally, verify the user has Project Design and Setup rights in that project.

**Q: Does REDCap verify that a test text is actually delivered when using the Test button?**
No. The Test button checks network connectivity to the provider's API only. It does not send a real test message or check any account credentials. Credentials are validated in the project, when the user enables texting and saves the provider settings.

**Q: Our REDCap server is only reachable inside our network. Will texting work?**
Not fully. Outgoing messages need REDCap to reach the provider, and incoming replies and status updates need the provider to reach REDCap. The server must be publicly reachable for those callbacks to work.

---

# 7. Common Mistakes & Gotchas

**Leaving the fresh-install defaults in place.** Both Twilio and Mosio start enabled for all users. If your institution has not agreed how texting is paid for or approved, any project designer can switch it on. Review the provider status and permission level soon after installing.

**Enabling the provider without checking the connection.** REDCap lets you enable a provider even if the Test button fails. If your firewall blocks outbound connections to Twilio's or Mosio's API, users will get errors when trying to send. Run the Test (or the Configuration Check) and fix any failure before advertising texting.

**Setting "Only Administrators" with "hide all information" and then fielding confused support requests.** When texting is fully hidden, users have no indication the feature exists. If you plan to offer texting to specific projects, consider using "Admin Approval" or "display information" so users know to contact support.

**Forgetting to enable phone validation types before users try to configure texting.** The phone-field picker in a project's Twilio/Mosio settings lists text fields that use a phone validation type (integer fields also appear). A designer cannot pick a disabled validation type in the first place, so if the country format their participants need is still disabled, they have no suitable field to choose. Enable the necessary validation types before advertising texting availability to your user base.

**Not saving after changes.** The Modules/Services Configuration page does not auto-save. Changes to provider status, permission levels, or visibility settings do nothing until you click Save, and are lost if you navigate away.

---

# 8. Related Articles

- [RC-TXT-01 — Texting in REDCap: Setup and Usage](RC-TXT-01_Texting-in-REDCap-Setup-and-Usage.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)
- [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md)
