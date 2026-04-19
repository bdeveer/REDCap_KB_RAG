RC-EM-01

**External Modules — Overview & Control Center Manager**

| **Article ID** | RC-EM-01 |
|---|---|
| **Domain** | External Modules |
| **Applies To** | REDCap administrators; also relevant to project users when enabling modules at the project level |
| **Prerequisite** | Control Center access for system-level management; Project Design and Setup rights for project-level enabling |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-EM-02 — External Modules Catalog; RC-AT-01 — Action Tags Overview; RC-INST-01 — Institution-Specific Settings |

---

# 1. Overview

External Modules are individual packages of software that can be downloaded and installed by a REDCap administrator. Modules extend REDCap's current functionality and can provide customizations and enhancements for REDCap's existing behavior and appearance — either at the system level (affecting all projects) or at the project level (enabled per project).

The **External Modules — Module Manager** is the Control Center page where administrators manage the complete lifecycle of installed modules: downloading from the REDCap Repo, enabling or disabling modules system-wide, configuring global settings, and monitoring usage across projects.

A separate **Project Module Manager** exists within each individual project, where project designers can enable modules for that specific project and configure any project-level settings.

---

# 2. Key Concepts & Definitions

**External Module**
A self-contained add-on that extends REDCap beyond its built-in feature set. Modules are distributed through the REDCap Repo (a curated community repository maintained by Vanderbilt) or can be developed and installed locally. Each module is identified by a unique prefix (e.g., `instance_table`, `hide_submit`).

**REDCap Repo**
The centralized repository at Vanderbilt where the REDCap community publishes External Modules. Administrators can browse, download, and install modules directly from the Control Center Manager page, provided the server has outbound internet connectivity to the Repo.

**Module Prefix**
The internal identifier for a module (e.g., `api_sync`, `record_autonumber`). Prefixes appear in URLs, log entries, and developer documentation. Each installed version directory on the server is named `prefix_vX.Y.Z`.

**Discoverable**
A badge that appears on some modules in the Project Module Manager. A Discoverable module can be seen by project users with Design and Setup rights, even before it is enabled for their project. This allows users to browse available modules and — depending on administrator configuration — may allow them to request enablement or enable the module themselves.

**System-Level vs. Project-Level Enablement**
A module installed by an administrator is not automatically active in every project. The administrator can choose to enable a module globally (active in all projects by default) or leave it available for project-by-project enablement. Some configuration settings exist at the system level (accessible only to administrators) and others at the project level (accessible to project designers).

---

# 3. Accessing the Module Manager

The Control Center Module Manager is accessible two ways:

1. **Control Center menu** → scroll to the **External Modules** section in the left sidebar → click **Manage**
2. **Direct URL shortcut:** From any Control Center page, type `emm` in the navigation bar and press Enter

The External Modules section in the Control Center left sidebar also shows a **View Logs** link for quick access to the EM Logs page.

---

# 4. Module Manager Interface

## 4.1 Module Update Notifications

When one or more installed modules have newer versions available in the REDCap Repo, a yellow notification banner appears at the top of the Manager page. The banner shows how many updates are available and lists each module along with its current and available version. Options:

- **Update All** — downloads and upgrades all listed modules in a single action
- **Update** (per module) — upgrades an individual module
- **Release Notes** (per module) — opens the module's GitHub release page in a new tab

## 4.2 Primary Action Buttons

| Button | Function |
|---|---|
| **Enable a module** | Opens the Available Modules dialog, which lists all modules downloaded to the server but not yet enabled. Use the search box to filter by name. |
| **View modules available in the REDCap Repo** | Opens the REDCap Repo in a new browser tab (authenticated using your REDCap credentials). Browse and download new modules from here. |
| **Configure Cron Start Times** | Opens a dialog to set system-wide start times for any modules that use scheduled cron jobs. |

## 4.3 Module Action Tag and API Method Reference

Below the primary buttons, two smaller buttons provide quick access to module-contributed extensions:

- **@ Action Tags** — lists all action tags registered by currently enabled External Modules (separate from the built-in REDCap action tags)
- **API Methods** — lists all API endpoints registered by enabled External Modules

## 4.4 Currently Enabled Modules Table

The main table lists all modules currently enabled at the system level. Each row shows:

- **Module name and version** — with a Discoverable badge if applicable
- **Description** — a brief summary of what the module does
- **Author and institution** — with a link to the author's contact email
- **View Documentation** link — opens the module's README or documentation

Each module row has three action buttons:

| Button | Function |
|---|---|
| **Configure** | Opens the module's system-level configuration settings dialog. Settings vary by module; some modules have no system-level settings at all. |
| **Disable** | Disables the module system-wide. A confirmation dialog appears before the action completes. The module's files remain on the server — it can be re-enabled via "Enable a module." |
| **View Usage** | Shows a list of all projects currently using this module. Includes an export button to download the usage list with design-rights user details. |

A search box in the top-right of the table allows filtering the enabled modules list by name.

---

# 5. Custom Text for the Project Module Manager

Administrators can configure optional custom text that appears to all users on the External Modules "Project Module Manager" page within each project. This is useful for:

1. Making users aware of institutional policies or procedures required before an administrator enables a module
2. Displaying guidelines (or a link to a guidelines page) for module usage at your institution
3. Highlighting anything particularly relevant about External Modules at your installation

To configure: click the **Set custom text for Project Module Manager page** button (top-right of the Module Manager heading). The text box accepts HTML, allowing links, formatting, and images. The text is displayed at the top of the Project Module Manager for all users.

---

# 6. Module Settings Export and Import

The Module Manager supports exporting and importing module configuration settings, which is useful when moving a module configuration between projects or systems.

**Export:** Select which modules to include → click Export. The export file is a zip archive containing the Configure dialog settings and any behind-the-scenes module settings. Settings flagged `super_user_only` in the module's `config.json` are excluded from exports (these may contain sensitive data).

**Import:** Choose an export zip file, confirm the replacement warning, then click Import. Important caveats:

- Settings with type `project-id` in the module's config are not imported, as project IDs may differ across systems and user access rights may vary.
- Importing replaces **all** settings for included modules — including any hidden settings used behind the scenes. Settings not present in the export file will be permanently removed.
- Always export current settings as a backup before importing.
- After import, fully review and test each affected module.

---

# 7. Developer Tools

The Module Manager page includes a **Developer Tools** section with:

- **External Module Framework Documentation** — links to the official GitHub documentation for building or modifying External Modules
- **Module Security Scanning** — opens a dialog showing the results of automated security scanning for installed modules

These tools are aimed at administrators and developers who maintain or author External Modules, rather than end users.

---

# 8. Project-Level Module Management

Within each project, users with Project Design and Setup rights can access the **External Modules** link in the left-hand project menu. This opens the **Project Module Manager**, where they can:

- See modules enabled system-wide for all projects
- Enable additional modules that are available at the system level but not yet enabled for their project (if administrator configuration permits)
- Configure project-level settings for any enabled module
- View action tags and API methods contributed by that module

Whether project users can enable modules themselves, or must request administrator enablement, depends on the system-level settings configured by the administrator.

---

# 9. Common Questions

**Where do module files live on the server?**
Each installed module version is stored as a directory on the REDCap web server under the modules path (e.g., `modules/instance_table_v1.13.3/`). Multiple versions of the same module can coexist on disk, though only one version is active at a time.

**Can a module be installed without being enabled?**
Yes. Downloading a module from the Repo places its files on the server. Enabling it is a separate step. The "Enable a module" button lists all modules that are installed but not currently enabled.

**What happens to data when a module is disabled?**
Disabling a module deactivates its functionality but does not delete any data stored by the module. If the module stores project-level data (e.g., configuration in module settings), that data is retained and will be available if the module is re-enabled.

**How do I know which modules are available at my installation?**
The "Enable a module" button in the Module Manager shows all currently downloaded modules. The REDCap Repo (via "View modules available in the REDCap Repo") shows the full community catalog of available modules.

> See RC-EM-02 for a catalog of modules commonly installed at REDCap installations, with descriptions and use cases.
