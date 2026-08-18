

**Control Center: AI Configuration Settings**

| **Article ID** | [RC-CC-26 — Control Center: AI Configuration Settings](RC-CC-26_Control-Center-AI-Configuration-Settings.md) |
| --- | --- |
| **Domain** | Control Center |
| **Applies To** | REDCap Administrators; requires Control Center access |
| **Requires** | REDCap v17.2.0+ (Standard); LTS 17.3.x and higher |
| **Verified Against** | REDCap v17.3.6 (LTS) |
| **Prerequisite** | [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-08 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md); [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md); [RC-AI-02 — AI Writing Tools](RC-AI-02_AI-Writing-Tools.md); [RC-AI-03 — AI Translations](RC-AI-03_AI-Translations.md); [RC-AI-04 — AI Summarization](RC-AI-04_AI-Summarization.md); [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) |
| **Synonyms** | where do i configure ai in the control center; ai configuration settings page redcap; set up multiple ai services in redcap; ai services moved out of modules services configuration; enable ai for one project only; map an ai config to a specific ai feature; why is the ai section gone from modules services; assign an ai configuration to a project |

---

## 1. Overview

**AI Configuration Settings** is the Control Center page where REDCap administrators define and manage the AI services that power REDCap's AI features. It replaced the single, global AI setup that previously lived on the Modules/Services Configuration page.

The defining difference is that an administrator can now create **multiple named AI configurations**. Each configuration points at one AI service and is mapped to one or more AI features, and configurations can be applied instance-wide, made the default for all projects, or selected on individual projects. The earlier model allowed exactly one set of AI credentials for the whole instance.

> **Version caveat (introduced 17.2.0; reaches LTS with the 17.3.x line):** This page does not exist on earlier versions. On LTS 16.0.x and Standard below 17.2.0, AI configuration lives in the **AI Services** section of Modules/Services Configuration — see [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md). On 17.2.0 and higher that section is **removed entirely** from Modules/Services rather than reduced to a link, so an administrator who knows the old location will find nothing there.

---

## 2. Key Concepts & Definitions

### AI configuration

A named, reusable set of AI service settings. Each configuration has a **Title**, a **Service Type**, its own connection settings, and a selection of the **AI features** it is allowed to drive. An instance may hold many configurations at once.

### Service Type

Which AI provider a configuration connects to — for example an Azure-hosted OpenAI deployment, Google Gemini, or a locally-hosted OpenAI-compatible server.

### AI feature

One of the three places REDCap can use AI: **Writing Tools** in the rich text editor, **Summarize data** on reports, and **auto-translate** on the Multi-Language Management setup page. A configuration is mapped to whichever of these it should serve, so different features can run on different services.

### Scope

Where a configuration applies. There are three independent scopes, described in Section 4: all non-project pages, all projects by default, and specific projects.

### Project-level override

A setting on a project's Edit Project Settings page that selects which AI configuration that project uses, or disables AI for it. On this model the project chooses from the configurations the administrator has already defined — it does not re-enter service credentials.

---

## 3. Finding the page

**Control Center → System Configuration → AI Configuration Settings.**

It sits directly beneath **Modules/Services Configuration** in the left-hand Control Center menu, which is the same group the AI settings previously lived in. If you do not see the entry, the instance is below 17.2.0.

---

## 4. The three enablement scopes

The top of the page carries two drop-downs and a pointer to the third scope. Each defaults to **Disabled**.

| Setting | What it controls |
|---|---|
| **AI config enabled for all non-project pages** | Which configuration serves AI features outside any project — most visibly the Multi-Language Management auto-translate on the Control Center's own MLM setup |
| **AI config enabled for all projects by default** | Which configuration every project receives unless overridden. Set this if AI should be broadly available |
| **AI config enabled for specific projects** | Not set here. Selected per project on that project's Edit Project Settings page |

The page states the interaction plainly: if a configuration is enabled for all projects by default, any individual project can still override it — or disable AI entirely for that project — from Edit Project Settings.

This yields the two deployment patterns the feature was designed around:

1. **Default-on:** set a configuration as the default for all projects, and override or disable it on the exceptions.
2. **Default-off:** leave the default disabled, and opt individual projects in one at a time.

> **Note:** The "all non-project pages" scope is separate from the project scopes and is easy to miss. If Control Center MLM auto-translate does not work while project-level translation does, this is the setting to check.

---

## 5. Managing configurations

Configurations are listed in a table with an **Add New AI Configuration** button above it. When none have been created the table reads *"No AI Configuration settings are currently added."*

| Column | Contents |
|---|---|
| **Title** | The administrator-assigned name for the configuration. This is the label that appears in the scope drop-downs and in the project-level selector, so it should identify the service and its purpose |
| **Service Type** | The AI provider this configuration connects to |
| **Configuration Settings** | The connection details for that service |
| **AI Features** | Which of the three AI features this configuration is mapped to |
| **Actions** | Edit and delete controls for the row |

Because the Title is what administrators and project owners see everywhere else, name configurations for how they will be chosen — the service and its intended use — rather than with an opaque label.

> **Note:** The per-service connection fields (endpoint URL, API key, model name or version) are the same values REDCap has always required for each provider; they are now entered per configuration rather than once for the instance. See [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) for the provider-specific detail on Azure OpenAI, OpenAI-compatible and Gemini endpoints, which carries over unchanged. The add/edit dialog itself is rendered dynamically and its exact field layout should be confirmed against a configured instance before being documented here.

---

## 6. Selecting a configuration for a project

On a project's **Edit Project Settings** page (Control Center → Edit Project Settings), an **AI Services** section appears with a single **Select AI Configuration** drop-down. REDCap's own wording: *if one or more AI Configuration settings are added globally, then one may select one of them at project level so that the respective AI resource/endpoint values will be utilized for this project.*

This is a meaningful simplification over the previous model, where enabling AI for one project meant typing that project's endpoint URL, API key and model into the project's settings. Credentials now live in exactly one place.

> **Note:** The section only offers configurations that already exist. If the drop-down is empty, no configurations have been created on the AI Configuration Settings page yet.

---

## 7. Upgrading from the pre-17.2.0 model

> **Version caveat (upgrading to 17.2.0–17.2.3):** If system-level AI settings were configured and enabled on a version below 17.2.0, upgrading to 17.2.0 or higher would incorrectly leave the new **"AI config enabled for all projects by default"** setting *disabled* when it should have been enabled, and any projects created after the upgrade would not receive the AI configuration. Fixed in **17.3.0**. If your instance crossed this boundary on an affected version, open AI Configuration Settings and confirm the default scope reads as you intend, then spot-check a project created shortly after the upgrade.

Mapping the old settings to the new model:

| Pre-17.2.0 (Modules/Services → AI Services) | 17.2.0+ (AI Configuration Settings) |
|---|---|
| **Enable system-wide AI services?** master toggle, with the provider chosen inline | Implicit. A configuration exists for each provider you want; scope is set by the two drop-downs |
| **Enable individual AI features for all projects** — three separate on/off toggles | The **AI Features** mapping on each configuration, so different features can use different services |
| One global set of endpoint/key/model values | One set per configuration, with as many configurations as needed |
| Project override by re-entering endpoint, key and model on Edit Project Settings | Project override by selecting a named configuration from a drop-down |
| Leave global fields blank to restrict AI to selected projects | Leave **enabled for all projects by default** disabled and opt projects in individually |

---

## 8. Common Questions

**Q: Where did the AI settings go? They're not on Modules/Services Configuration any more.**

**A:** They moved in REDCap 17.2.0 to a dedicated **AI Configuration Settings** page, directly below Modules/Services Configuration under System Configuration in the Control Center menu. The old section was removed rather than left as a link, so there is no pointer at the previous location.

**Q: Can different AI features use different AI services?**

**A:** Yes, and this is the main reason the page exists. Each configuration is mapped to whichever of the three features it should serve, so you might run Writing Tools on a locally-hosted model while MLM auto-translate uses a cloud service.

**Q: How do I enable AI for just one project?**

**A:** Create the configuration on this page, leave **AI config enabled for all projects by default** set to Disabled, then open Edit Project Settings for that project and pick the configuration from the **Select AI Configuration** drop-down.

**Q: How do I turn AI off for one project when it is enabled everywhere?**

**A:** From that project's Edit Project Settings page. A project-level override can either select a different configuration or disable AI for the project entirely, regardless of the system default.

**Q: Why does auto-translate work inside projects but not in the Control Center?**

**A:** The Control Center's own MLM setup is not a project page, so it is governed by **AI config enabled for all non-project pages** — a separate setting from the project scopes. Set that drop-down to a configuration as well.

**Q: I upgraded and AI stopped applying to new projects. What happened?**

**A:** A bug affecting upgrades to 17.2.0 through 17.2.3 left the "enabled for all projects by default" setting disabled when it should have been enabled, and newly created projects did not pick up the configuration. Fixed in 17.3.0. Re-check the setting on this page and verify a recently created project.

**Q: Do I still enter the API key on each project that uses AI?**

**A:** No. That was the pre-17.2.0 behaviour. Credentials belong to the configuration, and a project selects a configuration by name.

---

## 9. Common Mistakes & Gotchas

**Looking for AI settings where they used to be.** On 17.2.0+ the AI Services section is gone from Modules/Services Configuration entirely — no heading, no link, no note. An administrator who remembers the old location will reasonably conclude AI has been removed from the build. Check the left-hand menu for AI Configuration Settings before concluding anything is missing.

**Missing the "all non-project pages" scope.** Two of the three scopes concern projects, so this one is easy to overlook. The symptom is narrow and confusing: AI features work normally inside projects but the Control Center's own MLM auto-translate does nothing.

**Assuming an upgrade preserved the default-on behaviour.** Upgrading from below 17.2.0 on an affected version silently disabled the all-projects default and skipped applying it to new projects. Nothing warns you; existing projects keep working, so the gap only shows up on projects created after the upgrade. Verify the setting explicitly after any upgrade across the 17.2.0 boundary.

**Naming configurations opaquely.** The Title is what appears in the scope drop-downs and in every project's selector. A configuration called "Config 1" forces whoever picks it to come back to this page to work out what it connects to. Name it for the service and its purpose.

**Deleting a configuration that projects are using.** A configuration referenced as a system default or by individual projects is not inert. Check where a configuration is in use before removing it, or those projects lose the AI features they were relying on.

---

## 10. Related Articles

- [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) — what the AI features are, the security model, and what must be configured before users see them
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) — the pre-17.2.0 location, still current for LTS 16.0.x, and the provider-specific endpoint detail
- [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md) — where the project-level selection is made
- [RC-AI-02 — AI Writing Tools](RC-AI-02_AI-Writing-Tools.md), [RC-AI-03 — AI Translations](RC-AI-03_AI-Translations.md), [RC-AI-04 — AI Summarization](RC-AI-04_AI-Summarization.md) — the three features a configuration can be mapped to
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have this page yet
