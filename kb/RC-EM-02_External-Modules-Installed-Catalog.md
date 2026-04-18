RC-EM-02

**External Modules — Installed Module Catalog**

| **Article ID** | RC-EM-02 |
|---|---|
| **Domain** | External Modules |
| **Applies To** | REDCap administrators; project designers evaluating module capabilities |
| **Prerequisite** | RC-EM-01 — External Modules Overview & Manager |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-EM-01 — External Modules Overview; RC-AT-01 — Action Tags Overview; RC-DAG-01 — Data Access Groups; RC-RAND-01 — Randomization Concepts |

---

# 1. Overview

This article is a template for documenting the External Modules installed at your REDCap installation. Complete it with the modules available at your site so that users and administrators have a single reference for what is installed, what each module does, and any local configuration notes.

> **Note for KB maintainers:** Entries marked with `[FILL IN]` require confirmation from the REDCap administrator before publishing. Do not leave placeholder values in the live KB. Review and update this article after every major REDCap upgrade or module change.

> For instructions on enabling, configuring, and managing modules, see RC-EM-01.

Module entries marked **[Discoverable]** are visible to project users with Design and Setup rights in the Project Module Manager, even before the module is enabled for their project.

---

# 2. Module Catalog

List each installed module below. For each entry, provide:

- **Module name** — the display name shown in the Module Manager
- **Prefix** — the module's unique system identifier (shown in the Module Manager)
- **Author** — the developer or institution that wrote the module
- **Description** — what the module does, written for a project user (not just an admin)
- **[Discoverable]** tag — include if the module is set to discoverable
- **Cross-references** — link to related KB articles where relevant
- **Local notes** — any institution-specific restrictions, configuration requirements, or contact info

Use the template block below for each module. Remove unused lines.

---

## `[FILL IN — Module Name]` `[Discoverable, if applicable]`
**Prefix:** `[FILL IN — e.g., module_prefix]`
**Author:** `[FILL IN — Developer name / Institution]`

`[FILL IN — 2–4 sentence description of what the module does and when it is useful. Write for a project designer, not just an admin.]`

> `[FILL IN — optional: See also links, e.g., RC-AT-01 — Action Tags Overview]`

> **Local note:** `[FILL IN — optional: any site-specific restriction, configuration step, or contact info]`

---

## `[FILL IN — Module Name]`
**Prefix:** `[FILL IN]`
**Author:** `[FILL IN]`

`[FILL IN — description]`

---

*(Repeat the block above for each installed module. Delete this instruction line when the catalog is complete.)*

---

# 3. Module Categories

Once the catalog is populated, this section helps users quickly find modules by type. Update these lists to match your actual installed modules.

## Modules That Add Action Tags

Some modules extend REDCap by introducing custom action tags (prefixed with `@`). These tags appear in the **@ Action Tags** popup on the Control Center Module Manager page.

**Modules with action tags at this installation:** `[FILL IN — list module names, e.g., Choice Columns, HIDESUBMIT, Instance Table]`

> See also: RC-AT-01 — Action Tags Overview for general guidance on using action tags.

## Modules That Extend the API

Some modules add new API endpoints beyond REDCap's built-in API. These endpoints appear in the **API Methods** popup on the Module Manager page.

**Modules with custom API endpoints at this installation:** `[FILL IN — list module names, e.g., Locking API, Data Quality API — or "None"]`

## Locally Developed Modules

Some installations have modules built specifically for local infrastructure — for example, modules that integrate with a local IRB management system, EMR, or institutional directory service.

**Locally developed modules at this installation:** `[FILL IN — list any local/custom modules not from the REDCap Repo, or "None"]`

---

# 4. Requesting and Enabling Modules

## Requesting a New Module

External modules are developed by the REDCap community and shared via the REDCap Repo. If your project needs a module that is not currently installed, you can request it.

**How to request a new module:** `[FILL IN — e.g., "Submit a request via the Contact REDCap Administrator link. Requests are reviewed monthly." / "Contact the REDCap administrator directly."]`

**Review criteria:** `[FILL IN — optional: describe any local criteria for approving module requests, e.g., security review, validation requirements, IRB compatibility]`

## Enabling a Module for Your Project

Once a module is installed at the system level, it must also be enabled at the project level before it takes effect.

**How project-level enabling works at this institution:** `[FILL IN — e.g., "Users with Design and Setup rights can enable approved modules themselves from the External Modules section of their project." / "All project-level module activations must be requested from the support team."]`

> See also: RC-EM-01 — External Modules Overview & Manager for step-by-step instructions on enabling modules in a project.

---

# 5. Common Questions

**Q: A module I've heard about isn't listed here. Does that mean it isn't available?**

**A:** It may not be installed at this installation, or this article may be out of date. Contact the REDCap support team to ask whether the module is available or can be requested.

---

**Q: I enabled a module in my project but it doesn't seem to do anything. What should I check?**

**A:** Most modules require configuration after enabling. Open the module's **Configure** button in the External Modules section of your project to review its settings. Consult the module's README (accessible from the Module Manager) for setup instructions. If you're still stuck, contact the support team.

---

**Q: Can I request a module that isn't on the REDCap Repo?**

**A:** Custom or locally developed modules are possible but require administrator involvement. Contact the REDCap support team to discuss feasibility and scope.

---

**Q: How do I know which version of a module is currently installed?**

**A:** The installed version number is shown in the Control Center Module Manager. This article reflects the modules installed at the time it was last updated — for current version numbers, always check the Module Manager directly.
