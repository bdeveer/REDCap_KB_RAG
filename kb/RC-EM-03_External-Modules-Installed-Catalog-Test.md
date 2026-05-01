RC-EM-03

**External Modules — Installed Module Catalog — Test / Staging Instance**

| Article ID | RC-EM-03 |
|---|---|
| Instance | Test / Staging |
| Domain | External Modules |
| Applies To | REDCap administrators; project designers on the Test / Staging instance |
| Prerequisite | RC-EM-01 — External Modules Overview & Manager |
| Version | 1.0 |
| Last Updated | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| Related Topics | RC-EM-01 — External Modules Overview; RC-EM-02 — Production Catalog; RC-EM-04 — Development Catalog |

---

> ## ⚠️ RAG IMPLEMENTATION NOTICE
>
> **This article is currently a template for the Test / Staging instance module catalog. It does not yet contain actual module information.**
>
> RC-EM-03 documents which External Modules are installed and available on the Test / Staging REDCap instance. Module availability on the test instance may differ from Production — some modules may be installed for evaluation purposes that are not yet approved for production use, and some production modules may not be present on test.
>
> **Before going live with this KB, your REDCap administrator should:**
> 1. Replace every `[FILL IN]` module entry with a real module entry for the Test / Staging instance
> 2. Note any modules that differ from the Production catalog (RC-EM-02)
> 3. Remove the placeholder template blocks once real entries are added
> 4. Delete this notice block once the article is fully populated
>
> **Adding more instance articles:** If your organization runs additional REDCap instances beyond Production, Test/Staging, and Development — for example, a 21 CFR Part 11-compliant instance, a FISMA-compliant instance, a GDPR-scoped instance, a dedicated Training environment, or a separate instance for a specific faculty or department — create a new module catalog article for each:
> 1. Copy RC-EM-02 (Production) as a starting template.
> 2. Assign the next sequential Article ID (`RC-EM-05`, `RC-EM-06`, etc.) and update all metadata fields accordingly.
> 3. Set the `Instance` metadata field to a short, unambiguous label that the RAG system can use to scope retrieval (e.g., `Part 11 — Production`, `FISMA`, `Training`, `Faculty of Medicine`).
> 4. Populate the module catalog (Section 2) with modules actually installed on that instance. Part 11 instances may enforce stricter module approval requirements; Training instances may have a limited module set by design.
> 5. Update the **Related Topics** metadata field and cross-references in Sections 1 and 4 in **every existing RC-EM catalog article** to include the new entry.
> 6. Add the new article to `meta/KB-INDEX.md`.

---

# 1. Overview

This article catalogs the External Modules installed on the **Test / Staging** REDCap instance. Module availability may differ from the Production instance — see RC-EM-02 for the Production catalog. Always verify module availability in the Module Manager for the instance you are working on.

> For instructions on enabling, configuring, and managing modules, see RC-EM-01.

Module entries marked **[Discoverable]** are visible to project users with Design and Setup rights in the Project Module Manager for this instance.

> **Note:** The Test / Staging instance may include modules installed for evaluation or testing that are not yet available on Production. Conversely, some Production modules may not be installed on this instance. Do not assume that module availability on Test mirrors Production.

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

---

# 6. Related Articles

- RC-EM-01 — External Modules: Overview & Manager
- RC-EM-02 — External Modules: Installed Catalog
- RC-EM-04 — External Modules: Development Catalog
- RC-CC-06 — Control Center: Modules & Services Configuration
