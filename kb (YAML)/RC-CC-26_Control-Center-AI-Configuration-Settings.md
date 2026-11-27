---
id: RC-CC-26
title: 'Control Center: AI Configuration Settings'
domain: Control Center
applies_to:
- REDCap Administrators
- requires Control Center access
requires: REDCap v17.2.0+ (Standard); LTS 17.3.x and higher
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — AI configuration
  behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-AI-01 — REDCap AI Tools: Overview & Security'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-CC-24
  title: 'Control Center: Edit Project Settings'
- id: RC-AI-02
  title: AI Writing Tools
- id: RC-AI-03
  title: AI Translations
- id: RC-AI-04
  title: AI Summarization
- id: RC-INFRA-03
  title: REDCap Versions, Release Lines & Patching
tags:
- control center
synonyms:
- where do i configure ai in the control center
- ai configuration settings page redcap
- set up multiple ai services in redcap
- ai services moved out of modules services configuration
- enable ai for one project only
- map an ai config to a specific ai feature
- why is the ai section gone from modules services
- assign an ai configuration to a project
- combine default ai config with project ai config
- project ai config overrides the default
- only one ai configuration per project
---

# 1. Overview

**AI Configuration Settings** is the Control Center page where REDCap administrators define and manage the AI services that power REDCap's AI features. It replaced the single, global AI setup that previously lived on the Modules/Services Configuration page.

The defining difference is that an administrator can now create **multiple named AI configurations**. Each configuration points at one AI service and is mapped to one or more AI features, and configurations can be applied instance-wide, made the default for all projects, or selected on individual projects. The earlier model allowed exactly one set of AI credentials for the whole instance.

> **Version caveat (introduced 17.2.0; reaches LTS with the 17.3.x line):** This page does not exist on earlier versions. On LTS 16.0.x and Standard below 17.2.0, AI configuration lives in the **AI Services** section of Modules/Services Configuration — see [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md). On 17.2.0 and higher that section is **removed entirely** from Modules/Services rather than reduced to a link, so an administrator who knows the old location will find nothing there.

> **Version caveat (LTS 16.0.x):** There is no configuration page and no configuration selector. The AI feature toggles in Modules/Services Configuration apply to **all projects**, and there is no per-project way to turn AI off. To give one project its own AI service, a super user enters that project's endpoint, key and model directly in its Edit Project Settings page — see [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md). If you need AI in only some projects on 16 LTS, leave the global settings blank and enter credentials only on the projects that should have it.

---

# 2. Key Concepts & Definitions

## AI configuration

A named, reusable set of AI service settings. Each configuration has a **Title**, a service, its own connection settings, and a selection of the **AI features** it is allowed to drive. An instance may hold many configurations at once.

## Service Type

Which kind of AI service a configuration connects to. There are two choices:

- **OpenAI Service** — any OpenAI-style endpoint: Azure OpenAI, other OpenAI-compatible cloud services, and locally hosted OpenAI-compatible servers.
- **Gemini AI Service** — Google Gemini.

> **Note:** The configuration list labels every OpenAI-type configuration **"Azure OpenAI"** in its Service Type column, even when it actually points at a non-Azure cloud service or a local server. Use the Title to make the real service clear.

## AI feature

One of the three places REDCap can use AI: **Writing Tools** in the rich text editor, **Summarize data** on reports, and **auto-translate** on the Multi-Language Management setup page. A configuration is mapped to whichever of these it should serve, so different features can run on different services.

> **Version caveat (17.6.x):** An additional **AI Chatbot** feature may appear in the configuration's feature list. Most administrators will not see it.

## Scope

Where a configuration applies. There are three independent scopes, described in Section 4: all non-project pages, all projects by default, and specific projects.

## Project-level override

A setting on a project's Edit Project Settings page that selects which AI configuration that project uses, or disables AI for it. On this model the project chooses from the configurations the administrator has already defined — it does not re-enter service credentials.

---

# 3. Finding the page

**Control Center → System Configuration → AI Configuration Settings.**

It sits directly beneath **Modules/Services Configuration** in the left-hand Control Center menu, which is the same group the AI settings previously lived in. If you do not see the entry, the instance is below 17.2.0.

Administrators without the right to modify system configuration can open the page but see it read-only: they can review configurations and scopes but not add, edit, delete or change them.

---

# 4. The three enablement scopes

The top of the page carries two drop-downs and a pointer to the third scope. Each defaults to **Disabled**.

| Setting | What it controls |
|---|---|
| **AI config enabled for all non-project pages** | Which configuration serves AI features outside any project — Writing Tools in rich text editors on Control Center pages, and Multi-Language Management auto-translate on the Control Center's own MLM setup |
| **AI config enabled for all projects by default** | Which configuration every project receives unless overridden. Set this if AI should be broadly available |
| **AI config enabled for specific projects** | Not set here. Selected per project on that project's Edit Project Settings page |

**Both drop-downs save as soon as you change them.** There is no Save button; picking a different value takes effect immediately, so change them deliberately.

The page states the interaction plainly: if a configuration is enabled for all projects by default, any individual project can still override it — or disable AI entirely for that project — from Edit Project Settings.

This yields the two deployment patterns the feature was designed around:

1. **Default-on:** set a configuration as the default for all projects, and override or disable it on the exceptions.
2. **Default-off:** leave the default disabled, and opt individual projects in one at a time.

> **Note:** The "all non-project pages" scope is separate from the project scopes and is easy to miss. If Control Center MLM auto-translate or Writing Tools on Control Center pages do not work while the same features work inside projects, this is the setting to check.

---

# 5. Managing configurations

Configurations are listed in a table with an **Add New AI Configuration** button above it. When none have been created the table reads *"No AI Configuration settings are currently added."*

| Column | Contents |
|---|---|
| **Title** | The administrator-assigned name for the configuration. This is the label that appears in the scope drop-downs and in the project-level selector, so it should identify the service and its purpose. Badges mark the configuration currently set for all non-project pages and the one set as the default for all projects |
| **Service Type** | The kind of service. Every OpenAI-type configuration shows as "Azure OpenAI", whatever it actually connects to |
| **Configuration Settings** | The endpoint and model the configuration uses. The API key is never shown in the list |
| **AI Features** | Which of the AI features this configuration is mapped to |
| **Actions** | Edit and delete controls for the row |

Because the Title is what administrators and project owners see everywhere else, name configurations for how they will be chosen — the service and its intended use — rather than with an opaque label.

## The add/edit dialog

**Add New AI Configuration** and the row's edit control open the same dialog. The fields depend on the service chosen:

| Field | Shown for | Notes |
|---|---|---|
| **Title** | All | The name used everywhere the configuration is chosen |
| **Select AI Service** | All | **OpenAI Service** or **Gemini AI Service** |
| **API Endpoint URL** | OpenAI Service | The service's endpoint (Azure, another OpenAI-compatible cloud service, or a local server) |
| **API Key** | OpenAI Service, Gemini AI Service | May be left blank for a locally hosted server that does not require a key |
| **API Model Version/Name** | OpenAI Service | The model or deployment to call |
| **API Model Name** | Gemini AI Service | The Gemini model to call |
| **API Version** | Gemini AI Service | The Gemini API version |
| **Feature #1 – Feature #3** | All | One setting per AI feature (Writing Tools, Summarize data, auto-translate), each **Disabled** or **Enabled** |

**All three features start as Disabled.** A newly created configuration does nothing until you enable at least one feature on it, even if it is selected as a default or for a project.

For provider-specific endpoint detail (Azure OpenAI, OpenAI-compatible and Gemini), see [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md); the values themselves are the same as before, now entered per configuration rather than once for the instance.

## Deleting a configuration

You cannot delete a configuration that is currently set for all non-project pages or as the default for all projects. Change those drop-downs to another configuration (or Disabled) first.

A configuration selected on individual projects *can* be deleted, and those projects then get **no AI at all** — they do not fall back to the all-projects default. Reassign those projects in Edit Project Settings before deleting.

---

# 6. Selecting a configuration for a project

On a project's **Edit Project Settings** page (Control Center → Edit Project Settings), an **AI Services** section appears with a single **Select AI Configuration** drop-down. REDCap's own wording: *if one or more AI Configuration settings are added globally, then one may select one of them at project level so that the respective AI resource/endpoint values will be utilized for this project.*

This is a meaningful simplification over the previous model, where enabling AI for one project meant typing that project's endpoint URL, API key and model into the project's settings. Credentials now live in exactly one place.

**Only one configuration is active in a project at a time.** Selecting a configuration here replaces the all-projects default for that project entirely; the two do not combine. If the default serves Writing Tools and the project selects a configuration mapped only to Summarization, the project loses Writing Tools. Map a project-level configuration to every AI feature the project should keep.

> **Note:** The drop-down always includes **Disabled**. If Disabled is the only choice, no configurations have been created on the AI Configuration Settings page yet. The configuration set as the all-projects default is marked **[default config for all projects]** in the list.

> **Version caveat (17.3.x LTS vs 17.6.x Standard):** On 17.3 LTS, administrators in a Project Administrator Group (REDCap+) can change a project's AI configuration from Edit Project Settings. On 17.6 only system administrators can; Project Administrator Group admins see the drop-down disabled. If your Project Administrator Group admins handle AI requests on 17.3, plan for those requests to come to system administrators after upgrading.

---

# 7. Upgrading from the pre-17.2.0 model

> **Version caveat (upgrading to 17.2.0–17.2.3):** If system-level AI settings were configured and enabled on a version below 17.2.0, upgrading to 17.2.0 or higher would incorrectly leave the new **"AI config enabled for all projects by default"** setting *disabled* when it should have been enabled, and any projects created after the upgrade would not receive the AI configuration. Fixed in **17.3.0**. If your instance crossed this boundary on an affected version, open AI Configuration Settings and confirm the default scope reads as you intend, then spot-check a project created shortly after the upgrade.

**The upgrade creates configurations for you.** When an instance moves to 17.2.0 or higher, REDCap converts the old global AI settings and any project-level credentials into configurations named **"Setting #1"**, **"Setting #2"** and so on. After upgrading, open each one, check which service and features it holds, and rename it so administrators can recognise it in the scope drop-downs and project selectors.

Mapping the old settings to the new model:

| Pre-17.2.0 (Modules/Services → AI Services) | 17.2.0+ (AI Configuration Settings) |
|---|---|
| **Enable system-wide AI services?** master toggle, with the provider chosen inline | Implicit. A configuration exists for each provider you want; scope is set by the two drop-downs |
| **Enable individual AI features for all projects** — three separate on/off toggles | The feature settings on each configuration, so different features can use different services |
| One global set of endpoint/key/model values | One set per configuration, with as many configurations as needed |
| Project override by re-entering endpoint, key and model on Edit Project Settings | Project override by selecting a named configuration from a drop-down |
| Leave global fields blank to restrict AI to selected projects | Leave **enabled for all projects by default** disabled and opt projects in individually |

---

# 8. Common Questions

**Q: Where did the AI settings go? They're not on Modules/Services Configuration any more.**

**A:** They moved in REDCap 17.2.0 to a dedicated **AI Configuration Settings** page, directly below Modules/Services Configuration under System Configuration in the Control Center menu. The old section was removed rather than left as a link, so there is no pointer at the previous location.

**Q: Which AI services can a configuration use?**

**A:** Two service types: **OpenAI Service**, which covers Azure OpenAI, other OpenAI-compatible cloud services and locally hosted OpenAI-compatible servers, and **Gemini AI Service**. The list shows every OpenAI-type configuration as "Azure OpenAI", so rely on the Title to tell them apart.

**Q: Can different AI features use different AI services?**

**A:** Yes, across the instance, and this is the main reason the page exists. Each configuration is mapped to whichever of the three features it should serve, so you might run Writing Tools on a locally-hosted model while MLM auto-translate uses a cloud service. Within a single project, though, only one configuration is active, so all of that project's AI features run on the one configuration it uses.

**Q: I created a configuration and set it as the default, but nothing happens. Why?**

**A:** Every feature on a new configuration starts as Disabled. Edit the configuration and set the features you want to Enabled.

**Q: How do I enable AI for just one project?**

**A:** Create the configuration on this page, enable the features it should serve, leave **AI config enabled for all projects by default** set to Disabled, then open Edit Project Settings for that project and pick the configuration from the **Select AI Configuration** drop-down. On 16 LTS, enter the credentials on that project's Edit Project Settings page instead and leave the global settings blank.

**Q: How do I turn AI off for one project when it is enabled everywhere?**

**A:** On 17.2.0 and higher, from that project's Edit Project Settings page: a project-level override can either select a different configuration or disable AI for the project. On 16 LTS there is no per-project off switch; the feature toggles apply to every project.

**Q: Why does auto-translate work inside projects but not in the Control Center?**

**A:** The Control Center's own MLM setup is not a project page, so it is governed by **AI config enabled for all non-project pages** — a separate setting from the project scopes. The same setting controls Writing Tools on Control Center pages. Set that drop-down to a configuration as well.

**Q: I upgraded and AI stopped applying to new projects. What happened?**

**A:** A bug affecting upgrades to 17.2.0 through 17.2.3 left the "enabled for all projects by default" setting disabled when it should have been enabled, and newly created projects did not pick up the configuration. Fixed in 17.3.0. Re-check the setting on this page and verify a recently created project.

**Q: After upgrading I have configurations called "Setting #1" and "Setting #2". What are they?**

**A:** The upgrade converted your old global AI settings and any project-level credentials into configurations with those names. Open each, confirm what it connects to and which features it serves, and rename it.

**Q: Can a project use the default AI configuration for one feature and its own configuration for another?**

**A:** No. A project has one active AI configuration. A project-level selection overrides the all-projects default completely rather than adding to it. To give a project its own service for one feature while keeping the others, create a configuration mapped to all the features that project needs and select it for the project.

**Q: Do I still enter the API key on each project that uses AI?**

**A:** Not on 17.2.0 and higher. Credentials belong to the configuration, and a project selects a configuration by name. On 16 LTS, yes — project-specific credentials are still entered by a super user in Edit Project Settings.

---

# 9. Common Mistakes & Gotchas

**Looking for AI settings where they used to be.** On 17.2.0+ the AI Services section is gone from Modules/Services Configuration entirely — no heading, no link, no note. An administrator who remembers the old location will reasonably conclude AI has been removed from the build. Check the left-hand menu for AI Configuration Settings before concluding anything is missing.

**Missing the "all non-project pages" scope.** Two of the three scopes concern projects, so this one is easy to overlook. The symptom is narrow and confusing: AI features work normally inside projects but Writing Tools on Control Center pages and the Control Center's own MLM auto-translate do nothing.

**Changing a scope drop-down "just to look".** The two scope drop-downs save immediately on change. There is no Save or Cancel step to back out of.

**Creating a configuration and forgetting to enable its features.** All features default to Disabled, so a new configuration has no effect until you enable them.

**Assuming an upgrade preserved the default-on behaviour.** Upgrading from below 17.2.0 on an affected version silently disabled the all-projects default and skipped applying it to new projects. Nothing warns you; existing projects keep working, so the gap only shows up on projects created after the upgrade. Verify the setting explicitly after any upgrade across the 17.2.0 boundary.

**Leaving upgrade-created configurations as "Setting #1", "Setting #2".** These names say nothing about the service behind them. Rename them right after upgrading.

**Naming configurations opaquely.** The Title is what appears in the scope drop-downs and in every project's selector. A configuration called "Config 1" forces whoever picks it to come back to this page to work out what it connects to. Name it for the service and its purpose — especially for OpenAI-type configurations, which the list labels "Azure OpenAI" regardless of the actual service.

**Expecting a project configuration to add to the default.** A project-level selection replaces the all-projects default; it does not layer on top of it. A project switched to a configuration mapped only to Summarization silently loses Writing Tools and auto-translate it had through the default. Map the project's configuration to every feature it should keep.

**Choosing "Disabled" for a project before any default exists.** If no all-projects default is set, selecting **Disabled** on a project means "follow the default" rather than "AI off". The project has no AI for now, but as soon as you set an all-projects default it picks that configuration up. Before setting a default, re-check the projects you meant to keep AI off, and set them to Disabled again once the default is in place.

**Deleting a configuration that projects are using.** A configuration set for all non-project pages or as the all-projects default cannot be deleted until you change those settings. A configuration selected on individual projects can be deleted, and those projects then lose AI entirely — they do not fall back to the default. Reassign them first.

---

# 10. Related Articles

- [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) — what the AI features are, the security model, and what must be configured before users see them
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) — the pre-17.2.0 location, still current for LTS 16.0.x, and the provider-specific endpoint detail
- [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md) — where the project-level selection is made (and, on 16 LTS, where project credentials are entered)
- [RC-AI-02 — AI Writing Tools](RC-AI-02_AI-Writing-Tools.md), [RC-AI-03 — AI Translations](RC-AI-03_AI-Translations.md), [RC-AI-04 — AI Summarization](RC-AI-04_AI-Summarization.md) — the three features a configuration can be mapped to
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have this page yet
