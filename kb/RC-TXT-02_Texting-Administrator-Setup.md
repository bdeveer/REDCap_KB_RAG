RC-TXT-02

**Texting: Administrator Setup**

| **Article ID** | RC-TXT-02 |
| --- | --- |
| **Domain** | Texting (SMS) |
| **Applies To** | REDCap administrators with "Modify system configuration pages" permission |
| **Prerequisite** | RC-TXT-01 — Texting in REDCap: Setup and Usage |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-TXT-01 — Texting in REDCap: Setup and Usage |

---

# 1. Overview

This article covers the system-level configuration that a REDCap administrator must complete before any project can use texting. It explains how to connect Twilio or Mosio to the REDCap installation, how to control which users can enable texting in their projects, and how to verify that the required phone validation types are present. Project-level setup (enabling and configuring texting within an individual project) is covered in RC-TXT-01 — Texting in REDCap: Setup and Usage.

> **Required permissions:** You must have REDCap administrator access and the ability to "Modify system configuration pages" in the Control Center to perform any steps in this article.

---

# 2. Key Concepts & Definitions

## Control Center
The administrative interface in REDCap accessible only to users with administrator privileges. System-wide settings — including texting configuration — are managed here.

## Modules/Services Configuration page
The page within the Control Center's **System Configuration** section where Twilio and Mosio are enabled, connected, and permission-leveled for the entire REDCap installation.

## Permission level
A per-provider setting that controls who can enable Twilio or Mosio within an individual project: all users with Project Design rights, users who have received administrator approval, or administrators only.

## Field Validation Types page
A Control Center page listing all phone number validation formats available to projects. If a required country format is not listed, it must be added manually before projects can use it for texting.

## Test connection button
A button on the Modules/Services Configuration page that verifies REDCap can reach the texting provider's servers. Must succeed before the provider can be enabled.

---

# 3. Enabling a Texting Provider System-Wide

## 3.1 Navigate to the configuration page

1. Open the **Control Center** from the top navigation menu.
2. Under **System Configuration**, click **Modules/Services Configuration**.
3. Scroll to approximately the middle of the page to find the **Twilio** and **Mosio** configuration sections.

## 3.2 Test the connection

Before enabling either service, verify that your REDCap server can reach the provider's API:

1. Click the **Test** button in the provider's section.
2. If the connection succeeds, a confirmation popup appears. Proceed to enable the service.
3. If the connection fails, REDCap cannot reach the provider. Check your institution's firewall rules and network configuration before proceeding. The provider cannot be enabled until the test passes.

## 3.3 Enable the provider

1. Use the dropdown in the provider's section to set the service to **Enabled**.
2. Click **Save** at the bottom of the page to lock in the change.

Both Twilio and Mosio can be enabled simultaneously in the same REDCap installation. Individual projects may only activate one provider at a time, but different projects can use different providers.

## 3.4 Configure Twilio system credentials (Twilio only)

Unlike Mosio (which is configured per-project), Twilio credentials at the system level provide a default connection that projects build on. In practice, most institutions configure Twilio credentials in the Control Center and then allow project-level configuration to inherit or override them. Refer to Twilio's documentation for account credentials setup.

---

# 4. Setting the Permission Level

After enabling a provider, you must define who is allowed to activate it in individual projects.

## 4.1 Permission options

| Permission level | Behavior |
|---|---|
| All users | Any user with Project Design and Setup rights can enable and configure texting in their project without administrator involvement. |
| Admin Approval | Users can begin configuration in Project Setup, but the service is not active until the project administrator submits a request and a REDCap administrator approves it. The user sees an "Request admin approval" button instead of an "Enable" button. |
| Only Administrators | Only REDCap administrators can enable texting in any project. Project users cannot enable or configure it themselves. |

## 4.2 Hiding the feature from non-administrators

When **Only Administrators** is selected, a secondary option controls whether non-administrators can see that texting exists:

- **Yes, display information** — the Enable button is visible to users but greyed out (non-clickable). Users know texting is a feature but must contact an administrator to use it.
- **No, hide all information** — Twilio/Mosio options do not appear in Project Setup for non-administrators. Use this when you want to enable texting for select projects without advertising it to all users.

> **Note:** Even when texting is hidden from non-administrators, the administrator view of Project Setup shows the Enable button and all configuration options normally.

## 4.3 Save after any permission change

After adjusting permission settings, click **Save** at the bottom of the Modules/Services Configuration page. Permission changes take effect immediately but require a save to persist.

---

# 5. Verifying Phone Validation Types

REDCap uses field validation types to ensure phone numbers are formatted correctly before they are passed to Twilio or Mosio.

## 5.1 Check existing validation types

1. In the Control Center, navigate to **Field Validation Types**.
2. Review the list of phone validation entries. At minimum, **Phone (North America)** should be present and enabled — Mosio requires this format, and Twilio uses it for US/Canada numbers.
3. If you are enabling Twilio for international use, check that the relevant country format is listed (e.g., Phone (Australia), Phone (United Kingdom)).

## 5.2 Add a missing validation type

If the required country phone format is not listed, you must add it manually. The format of phone validation types varies by country. Consult the REDCap Community for existing custom phone validation definitions before creating one from scratch.

> **Note:** Mosio only supports US and Canadian phone numbers. Adding non-North American validation types is only relevant for Twilio installations serving international participants.

---

# 6. Common Questions

**Q: Can both Twilio and Mosio be enabled in the same REDCap installation?**
Yes. Both can be active at the system level simultaneously. Individual projects choose one or the other when enabling texting — they cannot use both at the same time.

**Q: What does "Admin Approval" mean in practice for the user?**
The user with Project Design rights sees the texting option in Project Setup but cannot activate it. They submit a request from within Project Setup, which generates a notification to administrators. An administrator then reviews and approves the request in the Control Center. Until approval, texting is not functional in that project.

**Q: If I switch the permission level from "All users" to "Only Administrators," what happens to projects that already have texting enabled?**
Projects that are already configured and actively using texting continue to function — the permission level change only affects which users can enable texting in new projects going forward. It does not disable texting in existing projects.

**Q: Do I need to configure Mosio credentials in the Control Center?**
No. Mosio uses a per-project API key that project designers enter themselves. There are no system-level Mosio credentials to configure in the Control Center beyond enabling the service.

**Q: How do I disable texting across the entire installation?**
Set the provider's dropdown to **Disabled** on the Modules/Services Configuration page and save. This prevents new projects from using the provider but does not interrupt active projects already using it.

**Q: A user says they cannot see the texting option in their project. What should I check?**
First, confirm the provider is enabled in the Control Center. Then check the permission level — if it is set to "Only Administrators" with the "No, hide all information" option, the user will not see any texting option. Finally, verify the user has Project Design and Setup rights in that project.

**Q: Does REDCap verify that a test text is actually delivered when using the Test button?**
The Test button checks network connectivity to the provider's API only. It does not send a real test message or verify that your account credentials are valid. Account credential validation happens when a project first tries to send a message.

---

# 7. Common Mistakes & Gotchas

**Enabling the provider before the connection test passes.** If your firewall blocks outbound connections to Twilio's or Mosio's API endpoints, enabling the provider will not work — users will get errors when trying to send. Always confirm the Test button succeeds before enabling.

**Setting "Only Administrators" with "hide all information" and then fielding confused support requests.** When texting is fully hidden, users have no indication the feature exists. If you plan to offer texting to specific projects, consider using "Admin Approval" or "display information" so users know to contact support.

**Forgetting to add phone validation types before users try to configure texting.** If a project designer creates a phone variable using a validation type that is not enabled in the Control Center, REDCap will not present that variable as an option in the Twilio/Mosio configuration menus. Confirm that the necessary validation types are in place before advertising texting availability to your user base.

**Not saving after changes.** The Modules/Services Configuration page does not auto-save. Changes to provider status, permission levels, or visibility settings are lost if you navigate away without clicking Save.

---

# 8. Related Articles

- RC-TXT-01 — Texting in REDCap: Setup and Usage
