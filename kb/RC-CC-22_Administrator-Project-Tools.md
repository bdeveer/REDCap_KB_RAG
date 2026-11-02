

**Administrator Project Tools**

| **Article ID** | [RC-CC-22 — Admin: Administrator Project Tools (View as User, Project Switcher)](RC-CC-22_Administrator-Project-Tools.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators only |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.6 (Standard) — checked live on a test instance, read-only: the dropdown and switcher fields, the help popover and the code that defines the targets; no view-as-user session or target navigation was run; v17.3.7 (LTS) — changelog review only |
| **Prerequisite** | [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md); [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) |
| **Synonyms** | how do i view a project as a specific user; impersonate a user to troubleshoot their access; see what a user sees in a project as admin; jump to a project by pid; project switcher quick navigation; admin troubleshooting tool for user rights; reproduce a user issue without their password; go directly to a project using project id; project switcher target codes; keyboard shortcut to jump to a project |

---

## 1. Overview

REDCap provides administrators with two project-level tools that are invisible to regular users: the **View Project as User** feature and the **Project Switcher**. Both appear within a project at the top-left of the page, just below the "Contact REDCap Administrator" link.

**View Project as User** allows an administrator to temporarily browse any project as a specific project member, with that user's rights applied. This is primarily a troubleshooting and support tool — it helps admins reproduce what a user is seeing without needing the user's login credentials.

**Project Switcher** is a quick-navigation text input that accepts a Project ID (PID) and jumps directly to that project. It saves administrators from navigating through the full project list when they know the PID they want to reach.

---

## 2. View Project as User

### 2.1 What It Does

When an administrator activates this feature, REDCap reloads the current project with the selected user's project privileges applied. The admin sees exactly what that user sees — including which instruments, menu items, and data are visible — based on that user's assigned rights.

### 2.2 Accessing the Feature

The **View Project as User** dropdown appears at the top-left of any project page, just below the "Contact REDCap Administrator" link. It is only visible to administrators — regular project users do not see it.

When expanded, the dropdown lists all users currently assigned to the project.

### 2.3 Starting a Session

1. Open the project.
2. Expand the **View Project as User** dropdown.
3. Select the desired user from the list.

REDCap confirms the change before reloading:

> *SUCCESS! You are now viewing this project as the user "[username]". This user's project user privileges will be applied to you within this project. The page will now reload to reflect this change.*

After the reload, the interface reflects only what that user is permitted to see and do.

### 2.4 Identifying an Active Session

While a view-as-user session is active, a green banner appears at the top of every project page:

> *You are currently viewing this project as the user "[username]", and their user privileges will be applied to you for the duration of this session.*

If you are unsure whether your current view is a normal admin view or an impersonated one, check for this banner.

### 2.5 Ending the Session

1. Expand the **View Project as User** dropdown.
2. Select **[Stop viewing as user]**.

REDCap confirms before reloading:

> *SUCCESS! You are no longer viewing this project as another user. The page will now reload to reflect this change.*

The administrator's full access is restored after the reload.

---

## 3. Project Switcher

### 3.1 What It Does

The Project Switcher is a text input field that accepts a Project ID (PID). Pressing Enter navigates directly to that project, bypassing the main project list. It is an admin-only tool — regular users do not see it.

### 3.2 Locations

The Project Switcher appears in two places:

**Within a project:** Located at the top-left of the page, just below the View Project as User dropdown.

**Outside a project (main menu):** Located between the REDCap logo at the top-left and the "Home" navigation tab. This allows an administrator to jump to any project directly from the home page or any other non-project page.

### 3.3 Using the Switcher

Type the PID of the target project into the input field and press Enter. REDCap navigates immediately to that project's home page.

Inside a project the field shows **Enter PID to go to project**; on non-project pages it shows **PID**. A help icon beside the field opens a **Navigate to page** popover listing the target codes below.

### 3.4 Target Codes

Enter a PID, or `cc` for the Control Center, optionally followed by a space and a target code. For example, `1234 eps` opens Edit Project Settings for that project, and `cc bu` opens Browse Users. See [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md).

**Project codes (after a PID):**

| Code | Destination | Code | Destination |
| --- | --- | --- | --- |
| `aer` | Add / Edit Records | `fcl` | Field Comment Log |
| `an` | Alerts & Notifications | `fr` | File Repository |
| `api` | API | `log` | Logging |
| `apg` | API Playground | `mlm` | Multi-Language Management |
| `cal` | Calendar | `od` | Online Designer |
| `cb` | Data Dictionary Codebook | `oeo` | Other Export Options |
| `cc` | Control Center | `of` | Other Functionality |
| `dag` | Data Access Groups | `pd` | Project Dashboards |
| `dd` | Data Dictionary | `ph` | Project Home |
| `ders` | Data Exports, Reports, and Stats | `pl` | Participant List |
| `dit` | Data Import Tool | `ps` | Project Setup |
| `dq` | Data Quality | `prh` | Project Revision History |
| `el` | Email Logging | `psl` | Public Survey Link |
| `eml` | External Module Logs | `rhp` | Record Home Page |
| `emm` | External Modules - Project Module Manager | `rsd` | Record Status Dashboard |
| `eps` | Edit Project Settings | `sdt` | Survey Distribution Tools |
| `sil` | Survey Invitation Log | `ur` | User Rights |

**Control Center codes (after `cc`):**

| Code | Destination | Code | Destination |
| --- | --- | --- | --- |
| `ap` | Administrator Privileges | `fs` | Footer Settings (All Projects) |
| `apidoc` | API Documentation | `fvt` | Field Validation Types |
| `bp` | Browse Projects | `gc` | General Configuration |
| `bu` | Browse Users | `hookdoc` | Plugin, Hook, & External Module Documentation |
| `cal` | Custom Application Links | `hps` | Home Page Settings |
| `cdis` | Clinical Data Interoperability Services | `info` | redcap_info() |
| `cron` | Cron Jobs | `ll` | Link Lookup |
| `dam` | Database Activity Monitor | `mlm` | Multi-Language Management |
| `ddp` | Dynamic Data Pull (DDP) | `msc` | Modules/Services Configuration |
| `dps` | Default Project Settings | `pt` | Project Templates |
| `dqt` | Database Query Tool | `sa` | Security & Authentication |
| `emdoc` | External Modules Documentation | `tokens` | API Tokens |
| `eml` | External Module Logs | `ual` | User Activity Log |
| `emm` | External Modules - Module Manager | `us` | User Settings |
| `eu` | Email Users | | |
| `fus` | File Upload Settings | | |

The 17.5.6 code also defines `hf` (Help & FAQ), `home` (Home), `mp` (My Projects), `np` (New Project) and `sd` (Sponsor Dashboard). The list can change between versions, so the popover is the reference for your instance.

### 3.5 Keyboard Shortcuts

In the 17.5.6 code, **Ctrl+Alt+N** (or **Cmd+Alt+N** on a Mac) moves focus to the field, and **Ctrl+Enter** opens the destination in a new tab. These were read from the code, not tried in a browser.

---

## 4. Common Questions

**Q: Can I make changes while viewing the project as another user?**
Yes — you retain the ability to act within the project, but only within the bounds of the impersonated user's rights. Actions that require rights the user does not have will behave as they would for that user (e.g., buttons may be hidden or disabled).

> **Important caveat:** In rare cases, certain features may display differently than they would for the actual user because underlying administrator privileges are not fully suppressed. The Data Export module is a known example: some export options that are restricted by user rights may remain visible or accessible to an administrator even while in an impersonated session. When diagnosing an issue involving a feature like data export, be aware that the view-as-user simulation may not be a perfect replica of the real user's experience.

**Q: Are actions I take during a view-as-user session logged under my account or the impersonated user's account?**
All actions remain attributed to the administrator's account in the audit log. Nothing is logged under the impersonated user. The view-as-user session does not transfer identity — it only applies the user's rights as a filter.

**Q: Does the view-as-user session persist if I navigate to a different project?**
No. The session is scoped to the current project. Navigating away from the project ends the impersonation.

**Q: Do I need to know a user's password to use View Project as User?**
No. The feature works entirely through the REDCap interface and does not require any credentials from the user being impersonated.

**Q: Can I use the Project Switcher to navigate to a project I am not assigned to?**
Yes. Administrators have access to all projects on the instance regardless of project membership. The Project Switcher will navigate to any valid PID.

**Q: Can I see which PID a project has?**
The PID appears in the URL when you are inside a project (e.g., `...redcap.php?pid=1234`). It is also listed in the Control Center's project list.

---

## 5. Common Mistakes & Gotchas

**Forgetting an active view-as-user session.** If you open a different browser tab or return to the project later in the same browser session, you may still be in view-as-user mode. Always check for the green banner at the top of the page if a project behaves unexpectedly.

**Trusting the impersonated view for data export troubleshooting.** Administrator privileges can bleed through in certain areas even during a view-as-user session. The Data Export module is the most documented example — some export options restricted by user rights may still appear. If a user reports they cannot export data, corroborate with the user directly rather than relying solely on the impersonated view.

**Entering an invalid PID in the Project Switcher.** If the PID does not correspond to an existing project, the switcher will either produce an error or land on an unexpected page. Double-check the PID before navigating, especially if entering it from memory.

**Using the Project Switcher target codes unintentionally.** Appending certain suffixes (like `eps`) to a PID in the Project Switcher triggers a redirect to a specific admin page rather than the project home. If you find yourself unexpectedly in the Control Center, you may have used a shortcut unintentionally.

---

## 6. Related Articles

- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) (managing user accounts and global access)
- [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md) (project-level admin configuration; Project Switcher `eps` shortcut)
- [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md) (CC structure and navigation)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (how project privileges are configured)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (assigning roles and rights to project members)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (full reference for the project left-hand menu)
