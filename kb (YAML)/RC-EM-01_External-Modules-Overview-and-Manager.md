---
id: RC-EM-01
title: External Modules — Overview & Control Center Manager
domain: External Modules
applies_to:
- REDCap administrators
- also relevant to project users when enabling modules at the project level
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — External
  Module manager behaviour checked against source code; pages not re-captured
prerequisites:
- System-level actions (download, enable, configure, disable) need the administrator
  privilege **Install, upgrade, and configure External Modules**
- any Control Center user can view the Manager page. Project-level configuration needs
  Project Design and Setup rights
- enabling a module in a project needs an administrator unless the module allows non-admins
  to enable it
version: '1.2'
last_updated: 2026-11
related:
- id: RC-EM-02
  title: 'External Modules: Installed Catalog — Production'
- id: RC-AT-01
  title: 'Action Tags: Overview'
- id: RC-INST-01
  title: Institution-Specific Settings & Policies — Production
tags:
- external modules
synonyms:
- how do i install an external module
- enable a module for my project
- download a module from the redcap repo
- what are external modules in redcap
- module manager in the control center
- configure external module settings
- add functionality with a plugin module
- enable or disable modules system-wide
- request activation of an external module
---

# 1. Overview

External Modules are individual packages of software that can be downloaded and installed by a REDCap administrator. Modules extend REDCap's current functionality and can provide customizations and enhancements for REDCap's existing behavior and appearance — either at the system level (affecting all projects) or at the project level (enabled per project).

The **External Modules — Module Manager** is the Control Center page where administrators manage the complete lifecycle of installed modules: downloading from the REDCap Repo, enabling or disabling modules system-wide, configuring global settings, and monitoring usage across projects.

A separate **Project Module Manager** exists within each individual project. Users with Project Design and Setup rights can configure project-level settings for modules enabled in their project. Enabling a module in a project needs a REDCap administrator by default; a project designer can enable it only when the administrator has turned on **Allow non-admins to enable this module on projects** for that module (and the module is visible to them, for example because it is discoverable). Otherwise the designer can request activation — see §8.

---

# 2. Key Concepts & Definitions

**External Module**
A self-contained add-on that extends REDCap beyond its built-in feature set. Modules are distributed through the REDCap Repo (a curated community repository maintained by Vanderbilt) or can be developed and installed locally. Each module is identified by a unique prefix (e.g., `instance_table`, `hide_submit`).

**REDCap Repo**
The centralized repository at Vanderbilt where the REDCap community publishes External Modules. Administrators can browse, download, and install modules directly from the Control Center Manager page, provided the server has outbound internet connectivity to the Repo.

**Module Prefix**
The internal identifier for a module (e.g., `api_sync`, `record_autonumber`). Prefixes appear in URLs, log entries, and developer documentation. Each installed version directory on the server is named `prefix_vX.Y.Z`.

**Discoverable**
A badge that appears on some modules in the Project Module Manager. An administrator makes a module discoverable with the system setting **Make module discoverable by users** ("Display info on External Modules page in all projects"). A discoverable module is listed in every project's Project Module Manager even before it is enabled there. Depending on the administrator's configuration, a project designer can then enable it themselves or use **Request Activation** to ask an administrator.

**System-Level vs. Project-Level Enablement**
A module installed by an administrator is not automatically active in every project. The administrator can choose to enable a module globally (**Enable module on all projects by default**) or leave it available for project-by-project enablement. Some configuration settings exist at the system level (accessible only to administrators) and others at the project level (accessible to project designers). Modules can also mark individual settings as admin-only; those are visible and editable only by administrators, even in a project.

**Framework Version**
The version of the External Module Framework a module is written against, declared in the module's configuration. REDCap supports multiple framework versions simultaneously so that older modules keep working as the framework evolves. The framework reached **Version 17** in REDCap 17.0.1. A module with **no** framework version declared falls back to framework version 1.

> **Version caveat (LTS 16):** The 16.0 LTS line supports framework versions up to 16 only. A module that requires framework 17 will not run there; the first LTS release with framework 17 is 17.3.5. Before downloading a module on an LTS 16 server, check its required framework version in the Repo, or upgrade to a 17.x release.

---

# 2a. Framework and Module Behaviour Changes

Points that affect module authors, and administrators diagnosing module faults.

| Change | Version |
| --- | --- |
| **Twig 3 bundled in REDCap itself**, not only in the EM Framework, making it available to internal REDCap code | 15.5.0 |
| New **API endpoints** for External Modules — see the EM Framework documentation | 15.5.2 |
| EM links appear in the left-hand menu while a project is in **Analysis/Cleanup** status. Previously they showed only in Development and Production | 15.6.0 |
| Framework advanced to **Version 17**, adding **strict variables in Twig** (errors raised only on servers not flagged as production — see below) | 17.0.1 |
| Module file uploads **hash their edoc IDs**; module documentation can link to files inside the module's own directory | 17.3.1 |
| Two new hooks that fire **before and after the Project Dashboard is rendered**, letting a module alter dashboards | 17.4.1 Standard; also on 17.3.x LTS |
| Autocomplete drop-downs in module configuration settings | 16.1.8 (on by default from 17.x) |
| Clearer error messaging when a module download fails | 16.1.6 |
| Module descriptions and documentation that vary by context, and a hook that fires when record changes are saved | Present in 17.6 Standard; absent in 17.3.31 LTS |

> **Version caveat (LTS 16 and 17.3 LTS):** Several items above are 17.x-only and do not exist on the 16.0 LTS line: hashed edoc IDs and documentation links to module files, the Project Dashboard hooks, and the clearer download error messages. On LTS 16, autocomplete in module settings is opt-in per setting rather than on by default. The context-specific descriptions/documentation and the record-save hook are present in 17.6 but not in 17.3.31 LTS. If a module's documentation says it needs one of these, confirm your server's release line before enabling it, or ask the module author for a compatible version.

> **Important for module authors — Twig 3 (15.5.0).** Bundling Twig 3 in REDCap core means a module using **Twig below 3.9.0** may hit a compatibility problem. If a module that worked previously starts failing after an upgrade across 15.5.0, its Twig version is the first thing to check. The **strict variables** change in framework 17 is a second boundary: templates that reference undefined variables raise errors, but only on servers flagged as development or test. Production servers are unaffected, so test a module on a non-production server to surface these errors before it reaches production.

> **Version caveat (16.0.0–16.0.3 Standard):** The framework method modules use to read the current user's rights could exit early and return **no rights** where the current user lacked User Rights privileges in the calling context. Any module, hook or plugin using it to make an access decision would have seen no rights rather than the actual rights — which fails open or closed depending on how the calling code is written. Fixed in 16.0.4.

> **Version caveat (16.0.2 Standard only):** The framework could delay EM cron jobs and generate large volumes of email to the administrator address with the subject "REDCap External Module Error". Introduced in 16.0.2 and fixed in 16.0.3, so the exposure was a single release — but a noisy one if you were on it.

> **Version caveat (below 17.4.0 Standard):** Enabling a module whose configuration declared **no framework version** would fail rather than defaulting to version 1, and disabling **all** modules could stop the Control Center loading entirely. Both fixed in 17.4.0.

---

# 3. Accessing the Module Manager

The Control Center Module Manager is accessible two ways:

1. **Control Center menu** → scroll to the **External Modules** section in the left sidebar → click **Manage**
2. **Direct URL shortcut:** From any Control Center page, type `emm` in the navigation bar and press Enter

The External Modules section in the Control Center left sidebar also shows a **View Logs** link for quick access to the EM Logs page.

Any Control Center user can open the page, but downloading, enabling, configuring, updating and disabling modules need the administrator privilege **Install, upgrade, and configure External Modules**.

---

# 4. Module Manager Interface

## 4.1 Module Update Notifications

When one or more installed modules have newer versions available in the REDCap Repo, a yellow notification banner appears at the top of the Manager page. The banner shows how many updates are available and lists each module with its available version. Options:

- **Update All** — downloads and upgrades all listed modules in a single action
- **Update** (per module) — upgrades an individual module
- **Release Notes** (per module) — opens the release notes link supplied by the Repo in a new tab

> **Version caveat (17.x only):** Showing each module's current version next to the available one, a warning when an update is a major version change, and the **Release Notes** link appear only on 17.x releases. On LTS 16 the banner is simpler; check the module's Repo page for changes before updating, especially across a major version.

## 4.2 Primary Action Buttons

| Button | Function |
|---|---|
| **Enable a module** | Opens the Available Modules dialog, which lists all modules downloaded to the server but not yet enabled. Use the search box to filter by name. From this dialog you can also **Change Version** (pick which downloaded version to enable) and **Delete Versions** (remove old version folders from the server). |
| **View modules available in the REDCap Repo** | Opens the REDCap Repo in a new browser tab. This is not a login to the Repo: REDCap passes along your username, name, email and institution, your REDCap and PHP versions, and the list of modules already installed, so the Repo can show compatibility and offer downloads back to your server. |
| **Manager for Timed Crons** | Opens a separate page for setting the start times of modules that use **timed** cron jobs. Modules whose crons run on a fixed interval are not managed here. |
| **Test Crons** | On servers not flagged as production, lets you run module cron jobs on demand to test them. |

When you enable a module, the confirmation dialog lists what the module asks to do — for example which REDCap hooks it uses and which module API actions it provides. On 17.x it also warns if the module can run its own database queries. Read this list before confirming, especially for a module you have not used before.

## 4.3 Module Action Tag and API Method Reference

Below the primary buttons, two smaller buttons provide quick access to module-contributed extensions:

- **@ Action Tags** — lists all action tags registered by currently enabled External Modules (separate from the built-in REDCap action tags)
- **API Methods** — lists all API endpoints registered by enabled External Modules

## 4.4 Modules Currently Available on this System

The main table, headed **Modules Currently Available on this System**, lists all modules enabled at the system level. Each row shows:

- **Module name and version** — with badges where they apply: **Discoverable**, **Enabled for All Projects**, and **API** (the module provides API methods)
- **Description** — a brief summary of what the module does
- **Author and institution** — with a link to the author's contact email
- **View Documentation** link — opens the module's README or documentation

Each module row has three action buttons:

| Button | Function |
|---|---|
| **Configure** | Opens the module's system-level configuration settings dialog. Alongside any module-specific settings, this is where the access settings in §5 live. |
| **Disable** | Disables the module system-wide. A confirmation dialog appears before the action completes. The module's files remain on the server — it can be re-enabled via "Enable a module." Re-enabling it system-wide makes it active again in every project that had it enabled before. |
| **View Usage** | Shows a list of all projects currently using this module. Includes an export button to download the usage list with design-rights user details. |

A search box in the top-right of the table allows filtering the enabled modules list by name.

# 5. System-Level Access Settings

The system-level **Configure** dialog includes standard settings that control who can see, enable and use a module in projects:

| Setting | Effect |
|---|---|
| **Enable module on all projects by default** | Makes the module active in every project without project-level enabling. |
| **Make module discoverable by users** | Lists the module in every project's Project Module Manager, even where it is not enabled. |
| **Allow non-admins to enable this module on projects** | Lets project designers enable the module themselves. Without it, enabling in a project needs an administrator (or a request — see §8). |
| **Hide this module from non-admins in the list of enabled modules on this project** | Keeps the module out of the Project Module Manager list for non-admin users, even where it is enabled. |
| **Require module-specific user privilege** | Only users who are given this module's privilege can configure it in a project. A checkbox for the module then appears in each project's User Rights editor, where it can be granted to users who do not have Project Design rights. |
| **Disable authenticated access to this module's API methods** / **Disable non-authenticated access to this module's API methods** | Switches off the module's API methods in project contexts, for token-authenticated calls, unauthenticated calls, or both. Use these when a module's API methods are not needed at your installation. |

> **Institution-specific:** Which modules are discoverable, which allow non-admins to enable them, and what review an administrator does before enabling a module vary between installations. Check with your REDCap administrators.

---

# 6. Custom Text for the Project Module Manager

Administrators can configure optional custom text that appears to all users on the External Modules "Project Module Manager" page within each project. This is useful for:

1. Making users aware of institutional policies or procedures required before an administrator enables a module
2. Displaying guidelines (or a link to a guidelines page) for module usage at your institution
3. Highlighting anything particularly relevant about External Modules at your installation

To configure: click the **Set custom text for Project Module Manager page** button (top-right of the Module Manager heading). The text box accepts HTML, allowing links, formatting, and images. The text is displayed at the top of the Project Module Manager for all users.

---

# 7. Developer Tools

The Module Manager page includes a **Developer Tools** section with a link to the **External Module Framework Documentation** — the official documentation for building or modifying External Modules.

Module security scanning is deliberately **not** run from the web interface. The Manager explains how to run the scan from the server's command line instead, so ask your server team to run it when reviewing a module before installation.

These tools are aimed at administrators and developers who maintain or author External Modules, rather than end users.

---

# 7a. Modules Absorbed into REDCap Core

REDCap periodically adopts a widely-used community module as a built-in feature. This is a compliment to the module's author, and a trap for administrators, because **adopting the feature does not remove the module**.

| Core feature | Absorbed from | Version |
| --- | --- | --- |
| **Access Control Groups** — see [RC-CC-25](RC-CC-25_Access-Control-Groups.md) | Andrew Poppe's *Security Access Groups* | 16.0.0 |
| **Editable field validation types** — see [RC-CC-08](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) §6 | Adam Nunez's *Add Validation Types* | 17.4.0 |
| **Automatic Version Redirect** — see [RC-CC-02](RC-CC-02_Control-Center-General-Configuration.md) | Andy Martin's *REDCap Redirect* | 17.2.2 |
| **Record logging links** in the Choose action for record menu — see [RC-DE-13](RC-DE-13_Record-Administration-Choose-Action-for-Record.md) | Luke Stevens' *Record Logging Links* | 15.0.3 |

> **Version caveat (LTS lines):** Editable validation types are available from 17.4.0 Standard; they are not on the 17.3 or 16.0 LTS lines, so keep the *Add Validation Types* module (or ask your server team) there. Automatic Version Redirect is 17.x only and is not on LTS 16. Check the version column against your release line before disabling a module in favour of the core feature.

> **Critical — upgrading does not disable the module or migrate its settings.** REDCap states this explicitly for Access Control Groups, and the same pattern applies to the others: after the upgrade you have **both** the core feature and the still-enabled module, configured independently and unaware of each other. Two systems enforcing overlapping rules with different settings is a genuine hazard — particularly for Access Control Groups, where both govern what rights users may hold.
>
> After any upgrade that absorbs a module you use, decide deliberately which implementation to keep, then disable the other. Do not assume the upgrade handled it.

---

# 8. Project-Level Module Management

The **External Modules** link appears in the left-hand project menu only when at least one module is enabled in the project or discoverable. Users with Project Design and Setup rights see it, and so do users without Design rights who hold a module-specific privilege (see §5). It opens the **Project Module Manager**, where users can:

- See modules enabled in the project, including those enabled system-wide for all projects
- Enable additional modules that are available at the system level but not yet enabled for their project (only where the module allows non-admins to enable it)
- Request activation of a discoverable module they cannot enable themselves
- Configure project-level settings for any enabled module (admin-only settings are visible only to administrators)
- View action tags and API methods contributed by that module
- **View Logs** for the project's modules (needs Project Design and Setup rights)

## 8.1 Requesting activation

When the system setting for module activation requests is turned on (Control Center → **Modules & Services Configuration** — see [RC-CC-06](RC-CC-06_Control-Center-Modules-and-Services.md)), a **Request Activation** button appears next to discoverable modules that the user cannot enable themselves. The request goes to the administrators' To-Do List and by email, and a REDCap administrator approves it by enabling the module in the project.

## 8.2 Module settings export and import

The Project Module Manager can export and import module configuration settings, which is useful when moving a module configuration between projects or servers. The buttons appear only in a project, not on the Control Center Manager page, and need Project Design and Setup rights.

**Export:** Select which modules to include → click Export. The export file is a zip archive containing the Configure dialog settings and any behind-the-scenes module settings. Settings that the module marks as admin-only are excluded from exports (these may contain sensitive data).

**Import:** Choose an export zip file, confirm the replacement warning, then click Import. Important caveats:

- Settings that point to another project (project-ID settings) are not imported, as project IDs may differ across systems and user access rights may vary.
- Importing replaces **all** settings for included modules in this project — including any hidden settings used behind the scenes. Settings not present in the export file will be permanently removed.
- On 17.x, only modules whose settings you are allowed to save are included.
- Always export current settings as a backup before importing.
- After import, fully review and test each affected module.

---

# 9. Common Questions

**Where do module files live on the server?**
Each installed module version is stored as a directory on the REDCap web server under the modules path (e.g., `modules/instance_table_v1.13.3/`). Multiple versions of the same module can coexist on disk, though only one version is active at a time. Old versions can be removed with **Delete Versions** in the Enable a module dialog.

**Can a module be installed without being enabled?**
Yes. Downloading a module from the Repo places its files on the server. Enabling it is a separate step. The "Enable a module" button lists all modules that are installed but not currently enabled.

**What happens to data when a module is disabled?**
Disabling a module deactivates its functionality but does not delete any data stored by the module. If the module stores project-level data (e.g., configuration in module settings), that data is retained and will be available if the module is re-enabled. Re-enabling a module system-wide also reactivates it in the projects that had it enabled.

**How do I know which modules are available at my installation?**
The "Enable a module" button in the Module Manager shows all currently downloaded modules. The REDCap Repo (via "View modules available in the REDCap Repo") shows the full community catalog of available modules.

**Why can't I enable a module in my project?**
By default only administrators can enable modules in projects. You can enable one yourself only if the administrator allowed non-admins to enable it; otherwise use **Request Activation** (if your installation has turned it on) or contact your REDCap administrators.

> See [RC-EM-02 — External Modules: Installed Catalog — Production](RC-EM-02_External-Modules-Installed-Catalog.md) for a catalog of modules commonly installed at REDCap installations, with descriptions and use cases.

---

# 10. Related Articles

- [RC-EM-02 — External Modules: Installed Catalog — Production](RC-EM-02_External-Modules-Installed-Catalog.md)
- [RC-EM-03 — External Modules: Installed Catalog — Test / Staging](RC-EM-03_External-Modules-Installed-Catalog-Test.md)
- [RC-EM-04 — External Modules: Installed Catalog — Development](RC-EM-04_External-Modules-Installed-Catalog-Development.md)
- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)
- [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md)
