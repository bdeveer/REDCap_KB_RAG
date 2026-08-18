---
id: RC-CC-06
title: 'Control Center: Modules & Services Configuration'
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: REDCap v17.3.6 (LTS) and v16.0.39 (LTS)
prerequisites:
- REDCap administrator access
version: '1.1'
last_updated: 2026-08
related:
- id: RC-CC-05
  title: 'Control Center: File Storage & Upload Settings'
- id: RC-CC-02
  title: 'Control Center: General System Configuration'
- id: RC-ALERT-01
  title: 'Alerts & Notifications: Setup'
- id: RC-EM-01
  title: 'External Modules: Overview & Manager'
- id: RC-INST-01
  title: Institution-Specific Settings & Policies — Production
- id: RC-AI-01
  title: 'REDCap AI Tools: Overview & Security'
- id: RC-CC-26
  title: 'Control Center: AI Configuration Settings'
- id: RC-AI-02
  title: AI Writing Tools
- id: RC-AI-03
  title: AI Translations
- id: RC-AI-04
  title: AI Summarization
tags:
- control center (admin)
synonyms:
- control center modules and services configuration
- enable or disable surveys api or randomization
- configure twilio or mosio sms integration
- set up sendgrid email delivery
- enable external modules framework
- turn redcap features on or off instance-wide
- configure ai services on older redcap versions
- module activation request workflow setting
---

# 1. Overview

The **Modules/Services Configuration** page is the control panel for enabling/disabling major REDCap features and configuring third-party service integrations. This is the largest and most feature-rich configuration page in the Control Center, where administrators control whether features like Surveys, the API, External Modules, Randomization, and various AI services are available to users across the instance. It also includes configuration for SMS services (Twilio, Mosio), email providers (SendGrid), and specialized features like e-Consent, CATs, and Data Transfer Services.

---

The **Modules/Services Configuration** page (under **System Configuration**) is the largest configuration page in the Control Center. It controls which features and integrations are enabled across the entire instance, and includes settings for third-party services like SMS platforms and email delivery providers.

---

# External Module Framework

**Enable the Built-in Process for Users to Request External Module Activation**
When enabled, a "Request Activation" button appears in project External Module lists, allowing users to submit a request to the REDCap administrator to activate a specific module for their project. This provides a managed workflow for EM activation rather than requiring direct contact with an administrator.

> **Note:** The Request Activation button only appears for modules that have been marked as "Discoverable" by the administrator. Modules that are not discoverable will not show the button even when this setting is on.

For the full External Modules policy and activation process, see your institution's External Modules documentation.

---

# Feature Enable/Disable Table

The following features can be enabled or disabled system-wide. When a feature is disabled here, it is unavailable in all projects regardless of project-level settings.

| Feature | Notes |
| --- | --- |
| **Surveys** | Enables the survey functionality across all projects. A sub-setting controls **Google reCAPTCHA** on public surveys — see the reCAPTCHA section below |
| **URL Shortening Service** | Enables short link generation for public survey links, public project dashboards, and public report links via the REDCAP.LINK service hosted by Vanderbilt on AWS. Disable if your server cannot make outbound HTTP requests to the public web |
| **Randomization** | Enables the randomization module; see [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) |
| **REDCap Shared Library** | Enables access to the Consortium's instrument-sharing library on the Online Designer page |
| **REDCap Messenger** | Enables the in-platform messaging system between users. A sub-setting controls whether users are allowed to message administrators directly |
| **REDCap API** | Enables API access for all projects; see [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **REDCap Mobile App** | Enables offline data collection via the mobile app. Users must be explicitly granted mobile app privileges within a project to use it; see [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md) |
| **MyCap Mobile App** | Enables MyCap participant mobile app support. When enabled, a per-project toggle determines whether individual projects use MyCap. A sub-setting controls whether project users can enable MyCap themselves or whether an administrator must do so. See [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md). **Note on limitations:** MyCap does not support piping, smart variables, field embedding, special functions, calculated fields, or most action tags (@HIDDEN and @MC-prefixed tags *are* supported). Branching logic is partially supported (simple single-statement logic only — no AND, OR, or special functions) |
| **External Modules Alternate Directory** | Allows loading external modules from a non-default directory path. Useful for staging or internal module development. Multiple directories can be separated with a pipe \| |
| **File Version History for 'File Upload' Fields** | When enabled, users can upload a new file to a File Upload field without deleting the current one — previous versions are preserved and accessible from the Data History popup. If disabled, users must delete the current file before uploading a replacement. Can be enabled or disabled per project on the Project Setup page |
| **Field Bank in the Online Designer** | Enables the 'Import from Field Bank' button in the Online Designer, allowing users to pull fields from standardized instrument catalogs. If disabled, the button is hidden for all users |
| **Video Embedding on Forms & Surveys** | Allows a video URL to be attached to a Descriptive field, displaying a play button that opens the video in a popup. Compatible with most hosting services; most reliable with YouTube and Vimeo |
| **Text-to-Speech for Surveys** | Enables text-to-speech on survey pages, reading survey text aloud via the IBM Watson Text-to-Speech API hosted by Vanderbilt University. Requires the REDCap server to be able to make outbound HTTP requests to `https://redcap.vumc.org` |
| **Auto-Suggest for Biomedical Ontologies** | Enables the BioPortal ontology lookup service for fields on forms and surveys. Requires a valid BioPortal API token and outbound HTTP access to `https://data.bioontology.org/` |
| **Data Entry Trigger** | Enables the Data Entry Trigger feature for all projects. When enabled, users can configure a URL that REDCap will POST to whenever a record is created or modified via normal data entry or a survey response. **Not triggered by** API imports, data imports via the import tool, or Mobile App imports; see [RC-INTG-01 — Data Entry Trigger](RC-INTG-01_Data-Entry-Trigger.md) |
| **Project XML Export** | Enables project backup/export as a single XML file in CDISC ODM format, available on the Project Setup page and the Data Exports page. The exported file can optionally include data and be used to clone the project |
| **Protected Email Mode** | Prevents identifying data (PHI/PII) from being included in the body of outgoing emails for alerts, survey invitations, and survey confirmation emails. When enabled at the system level, project users can activate it per project. In protected mode, recipients receive a surrogate email with a secure link to view the original message on a REDCap-hosted page; a one-time security code is required on first access (or after more than 30 days on the same device). Optionally, protection can be scoped to only emails that pipe identifier fields |
| **Email Logging** | When enabled, users with User Rights privileges in a project can opt in to the Email Logging page to search all outgoing project emails. **Note:** Outgoing emails are always stored in the backend database regardless of this setting; this toggle controls only whether users can access them through the interface |
| **Bulk Record Delete** | When enabled, users with Delete Records privileges can delete multiple records at once, or delete specific instrument data for a selected set of records |
| **E-Signature** | Enables the e-signature module for locking/certifying records. Should be disabled if your instance does not use Table-based, LDAP, or LDAP+Table-based authentication, as e-signature does not work with certain external authentication methods (e.g., Shibboleth, OAuth2) |
| **Sync Calendar to External Application** | Enables the Calendar Feed feature in projects, including the associated smart variables `[calendar-url]` and `[calendar-link]` for use in alerts and piping |
| **Image Embedding for Rich Text Editor** | Allows users to embed inline images from their local device into survey invitations, alerts, field labels, and any other rich text editor location (except the @RICHTEXT action tag on public surveys) |
| **File Attachment Embedding for Rich Text Editor** | Allows users to attach files via the rich text editor in survey invitations, alerts, and field labels (except @RICHTEXT and non-project pages). Attached files are stored in the "Miscellaneous File Attachments" folder in the project's File Repository |
| **Auto-Display Inline PDF Attachments in Instrument PDFs** | When a Descriptive Text field contains a PDF attachment, the PDF is displayed inline in downloaded instrument PDFs rather than as a link. Requires the ImageMagick PHP extension to be installed and enabled on the server |
| **DTS (Data Transfer Services)** | Enables the Data Transfer Services module, which allows data to be pushed into REDCap from external systems (e.g., an EMR or data warehouse) with an adjudication workflow for user approval before data is saved. Must be installed and configured separately before enabling here |
| **Computer Adaptive Tests (CATs) and Auto-Scoring Instruments** | Enables CAT instruments (e.g., PROMIS, Neuro-QoL) and auto-scoring for validated instruments from the REDCap Shared Library. These are driven by a third-party Assessment Center API hosted by Vanderbilt University. Data sent to the service is de-identified and cannot be linked to individual respondents. Requires outbound HTTP access to `https://www.redcap-cats.org/promis_api/` |

---

# Google reCAPTCHA for Public Surveys

Google reCAPTCHA can be enabled as an optional protection on public surveys (i.e., surveys with a public link that require no login). This is a sub-setting of the Surveys feature.

To enable it, you must first register your REDCap server with Google reCAPTCHA and obtain a **Site Key** and a **Secret Key**. When registering, choose the **reCAPTCHA v2** type with the **Checkbox** challenge option. Enter both keys in the Control Center configuration. Once set, a per-project toggle appears on the Public Survey page allowing project owners to enable reCAPTCHA for their project.

> **Note:** Google reCAPTCHA applies only to public surveys. It has no effect on survey invitations sent to specific participants.

A project-level default can be configured: new projects can default to reCAPTCHA enabled or disabled.

---

# SMS Services

## Twilio (SMS & Voice Calls)

Twilio is a third-party service that enables SMS and voice call delivery for survey invitations and alerts. Requires a Twilio account and configuration of account credentials in REDCap.

- **Enable Twilio** — Enables or disables the integration globally. Requires a Twilio account and credentials. The REDCap server must be able to make outbound HTTPS requests to `https://api.twilio.com`, and the server must be publicly reachable from the web so Twilio can POST back to it
- **Who Can Enable Twilio in a Project** — Three options:
  - *All users* — any user with Project Design/Setup rights can enable Twilio in their project
  - *Admin approval* — users can see the setting and request activation, but an administrator must approve before the service is active
  - *Administrators only* — the setting is hidden from non-admin users entirely
- **Display Twilio Information to All Users** — Only relevant when "Administrators only" is selected. Controls whether Twilio is advertised on the Project Setup page; set to "No" to keep Twilio invisible to regular users

See [RC-TXT-01 — Texting in REDCap: Setup and Usage](RC-TXT-01_Texting-in-REDCap-Setup-and-Usage.md) and [RC-TXT-02 — Texting: Administrator Setup](RC-TXT-02_Texting-Administrator-Setup.md) for more on texting workflows and administrator setup.

## Mosio (SMS)

Mosio is an alternative SMS service provider. Configuration mirrors Twilio, including the same three-option access control (All users / Admin approval / Administrators only) and the "Display information to all users" visibility toggle. Requires outbound HTTPS access to `https://api.mosio.com` and a publicly reachable server. See your institution's SMS strategy documentation before enabling.

## SendGrid (Email Templates)

SendGrid is an external email delivery service that enables template-based emails for Alerts & Notifications. Requires a SendGrid account and API key, and outbound HTTPS access to `https://api.sendgrid.com/v3`. Access control has two options: *All users* or *Administrators only* (no Admin approval option). Includes the same "Display information to all users" visibility toggle. See your institution's email delivery architecture before enabling.

---

# Statistics & Charts

**Enable Stats & Charts Module for All Projects**
Enables the Statistics & Charts feature globally. When enabled, project users can view aggregate data visualizations from the Stats & Charts tab.

**Allow Survey Respondents to View Aggregate Survey Results**
When enabled, project administrators can opt to show a respondent their responses plotted against aggregate data after completing a survey.

---

# e-Consent Framework for PDF Auto-Archiver

**Display 'e-Consent Framework' Option for All Surveys**
Makes the e-Consent configuration option visible in survey settings across all projects.

**Capture IP Address of Participants**
When an e-Consent is certified, the participant's IP address is stored in the File Repository table as part of the e-Consent record.

**Custom Message for e-Consent Framework Settings**
Optional text shown to project administrators when configuring e-Consent. A good place to link to institutional guidance on electronic consent requirements.

See [RC-SURV-08 — e-Consent Framework: Setup & Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md) for detailed e-Consent setup documentation.

---

# Alerts & Notifications Settings

These settings control what information users can include in alert recipient fields:

- **Allow normal users to use project variables for email fields** — Allows To/CC/BCC fields in alerts to reference project fields containing email addresses
- **Allow normal users to manually enter freeform email addresses** — Allows free-text email entry in alert recipient fields; can be further restricted by a domain allowlist
- **Domain allowlist for freeform email entry** — Optionally restricts freeform email addresses to specified domains
- **Allow normal users to use project variables for phone fields** — Allows recipient phone number fields to reference project data fields
- **Allow normal users to enter freeform phone numbers** — Allows manual phone number entry for SMS alerts

See [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) for alert setup and [RC-TXT-01 — Texting in REDCap: Setup and Usage](RC-TXT-01_Texting-in-REDCap-Setup-and-Usage.md) for SMS alert configuration.

---

# File Upload Field Enhancement

An optional enhancement that adds password verification and automatic external archiving to File Upload fields. When enabled at the system level and then activated in a project, any user uploading a file is asked to confirm it is the correct file. On data entry forms specifically, the user must also enter their REDCap password as part of the verification step. Once confirmed, the file is saved normally in REDCap and simultaneously stored as a duplicate on a configured external server. This feature is intended for projects that require FDA 21 CFR Part 11 compliance.

> **Note:** Enabling this at the system level does **not** auto-enable it in any project. Users with Project Setup & Design rights must activate it per project via the Additional Customizations popup on the Project Setup page.

**Supported external storage methods:**

| Method | Requirement |
| --- | --- |
| SFTP | Hostname (no protocol prefix), port 22, username, password, server directory, optional private key path |
| WebDAV | Hostname (must begin with `http://` or `https://`), port 80/443, username, password, server directory, authentication type (Digest, NTLM, or Basic) |
| Microsoft Azure Blob Storage | Only available if Azure is already configured as the system-level File Storage Method; requires bucket/container name |
| Amazon S3 | Only available if S3 is already configured as the system-level File Storage Method; requires bucket/container name |

---

# Rapid Retrieval (Page-Level Caching)

Rapid Retrieval is a read-through page-level caching feature that improves load times for slower REDCap pages, particularly exports, reports, and the record status dashboard. When a requested page is not in the cache, the system automatically fetches and stores it for subsequent requests, reducing direct database queries and wait times.

**Storage modes:**

| Mode | Notes |
| --- | --- |
| **Disabled** | Caching off; all pages load from the database directly |
| **File-based storage** *(recommended)* | Cached files are stored in REDCap's `temp` folder (or an alternative directory if configured). Files are fully encrypted at rest and are immediately removed once invalidated. Preferred for most deployments, especially high-traffic servers, because database storage can bog down the server and cause the MySQL binary log to grow rapidly |
| **Database storage** | Cached data is stored in the `redcap_cache` database table. Can degrade performance on busy servers; not recommended for high-traffic instances |

**Alternative directory for cached files (optional)**
By default, file-based caching stores files in REDCap's `temp` folder. An alternative directory path on the web server can be specified here. This is particularly useful in **load-balanced or multi-node cloud deployments** where the alternative directory points to centralized external file storage that all servers/nodes share. If REDCap is running on a single server, leaving this blank is recommended.

---

# Record-Level Locking Enhancement

An optional enhancement to the record locking feature that adds PDF review and automatic external archiving to the record locking workflow. This applies only to **entire-record locking** (not instrument-level locking). When enabled at the system level and then activated in a project, any user locking a full record is first asked to review a PDF copy of the complete record to confirm it is correct. Once the user confirms the PDF, the record is locked. At that point, the PDF is saved into the project's File Repository and a duplicate copy is archived on a configured external server. This feature is primarily useful for studies requiring a full Part 11-compliant electronic signature and audit trail.

> **Note:** Enabling this at the system level does **not** auto-enable it in any project. Users with Project Setup & Design rights must activate it per project via the Additional Customizations popup on the Project Setup page.

Supported external storage methods are identical to those for the File Upload Field Enhancement above (SFTP, WebDAV, Azure Blob Storage, Amazon S3), with the same configuration fields and prerequisites.

---

# Email Verification and Email Unsubscribe Features *(REDCap+, 17.3.0+)*

| Setting | Options | Default |
| --- | --- | --- |
| Email Verification and Email Unsubscribe Features | Disabled / Enabled | **Enabled** |

When enabled, a suite of four Smart Variables and a per-project **Verified & Unsubscribed Emails** dashboard page become available, letting participants verify their email address or unsubscribe from all emails from a project.

> **Note:** Disabling this hides the dashboard page from every project **and** removes the related Smart Variables from the Smart Variable documentation. Because the setting is Enabled by default, projects may already be relying on it — audit usage before disabling, since live alert and ASI trigger logic can depend on these variables.

See [RC-PLUS-05 — REDCap+: Email Verification & Unsubscribe](RC-PLUS-05_Email-Verification-and-Unsubscribe.md).

---

# Reward Services *(REDCap+, 17.0.0+)*

Participant compensation via electronic gift cards, integrating with the third-party vendor **Tango** through its Card API. Requires a REDCap+ subscription; the section is present on the page but not configurable without one.

Settings hosted here:

| Setting | Options |
| --- | --- |
| Enable Reward Services? | Disabled / Enabled |
| Who can enable Reward Services in a given project? | All users (with Project Design privileges) / Only administrators |
| Allow normal users to enable this feature on their own, or require a request? | Allow self-enable / Admin must enable via user request. **Only used when the setting above is "All users"** |
| Custom message when enabling Reward Services in a project | Free text, HTML permitted |
| Bypass sensitive confirmation when managing Rewards permissions? | Disabled / Enabled *(17.1.3+)* |
| Tango credentials | Environment (No environment selected / Production / Sandbox) with a Check button, Client ID, Client Secret, Service Account Username, Service Account Password |

> **Note:** The Tango credentials here are **system-level defaults** that projects inherit only when the project selects "Use System Default" on its API settings page. A project holding its own credentials overrides them entirely and will not follow a change made here.

> **Note:** The REDCap web server must be able to make outbound HTTP/HTTPS requests to the rewards provider API. REDCap strongly recommends validating the whole configuration against the Tango **Sandbox** environment before selecting Production — in Production, orders send real gift cards funded from a real institutional balance.

See [RC-PLUS-03 — REDCap+: Reward Services](RC-PLUS-03_Reward-Services.md) for the four-role workflow, the project-level experience and the known issues by version.

---

# e-Consent Framework: PDF External Storage Settings

When the e-Consent Framework is used in Part 11-compliant workflows, this section allows the e-Consent PDFs to be automatically archived to an external storage location (same options as the File Upload Settings storage configuration). Leave disabled unless required for regulatory compliance.

---

# AI Services *(pre-17.2.0 only)*

> **Version caveat (≤17.1.x Standard; LTS 16.0.x and earlier):** This section describes AI configuration **as it exists on the Modules/Services Configuration page**. In REDCap 17.2.0 all system-level AI settings were moved off this page onto a dedicated **AI Configuration Settings** page, and the AI Services section below no longer appears here at all — it is gone, not relocated within the page. If your instance is on 17.2.0 or higher (including LTS 17.3.x), see [RC-CC-26 — Control Center: AI Configuration Settings](RC-CC-26_Control-Center-AI-Configuration-Settings.md) instead. The settings below remain accurate for LTS 16.0.x instances, which is why they are retained here.

REDCap can use Artificial Intelligence (AI) to augment existing features. The AI services connect to an AI provider over a private endpoint that your institution controls, ensuring data security and privacy.

**Enable system-wide AI services?**
Master toggle for all AI features. Options are:
- *Disabled*
- *Enabled using OpenAI Service*
- *Enabled using Gemini AI Service*

Once the master toggle is on, individual AI features below become active. System-wide configuration values can be overridden at the project level on the Edit Project Settings page for individual projects.

## Individual AI Features

| Feature | Behavior when enabled |
| --- | --- |
| **Feature 1 — Writing Tools** | A magic wand icon appears in the toolbar of all rich text editors throughout REDCap (except the @RICHTEXT action tag). Users can alter and enhance text including changing length, tone, and reading level. See [RC-AI-02 — AI Writing Tools](RC-AI-02_AI-Writing-Tools.md) |
| **Feature 2 — Summarize free-form text on reports** | A magic wand icon appears next to free-form text fields on reports, allowing users to have the AI service summarize field values across the report. See [RC-AI-04 — AI Summarization](RC-AI-04_AI-Summarization.md) |
| **Feature 3 — Auto-translate on MLM setup page** | On the Multi-Language Management page, a button appears that auto-translates all untranslated text in one click. See [RC-AI-03 — AI Translations](RC-AI-03_AI-Translations.md) |

## OpenAI Configuration

Three deployment options are supported:

**Azure OpenAI (cloud-hosted) — preferred:** REDCap's AI services can use the Microsoft Azure OpenAI deployment of ChatGPT via a private virtual network endpoint. API Endpoint URL format: `https://{your-resource-name}.openai.azure.com/openai/deployments/[AI_DEPLOYMENT_NAME]`. The `[AI_DEPLOYMENT_NAME]` is the custom name given when deploying the resource (not the model name like `gpt-4o`). The Model Version field should match the `api-version` shown in the Azure Endpoint Target URI (e.g., `2024-08-01-preview`).

**Additional cloud-hosted OpenAI-compatible services:** Many cloud AI services expose an OpenAI-compatible API, including Mistral AI, Nebius AI Studio, GroqCloud, and Together AI. Each has its own endpoint URL and API key. REDCap/Vanderbilt has no affiliation with these services; review their security documentation before enabling.

**Locally-hosted OpenAI-compatible services:** Run an OpenAI-compatible server on-premises using tools such as LM Studio, LocalAI, GPT4All, or Ollama. These allow locally-hosted open-source language models. Provide the local endpoint URL; the API key field may be left blank if not required by the local service.

**OpenAI configuration fields:**
- **API Endpoint URL** — Full endpoint URL for the deployed model
- **API Key** — Secret key for authentication (may be blank for local deployments)
- **API Model Version/Name** — For Azure: the `api-version` string (e.g., `2025-01-01-preview`). For other services: the model name or identifier (e.g., `mistral-tiny`, `hermes-3-llama-3.2-3b`)

## Gemini AI Configuration

Google Gemini (cloud-hosted) can be used as an alternative to OpenAI. Obtain an API key from Google AI Studio.

**Gemini configuration fields:**
- **API Key** — Your Google Gemini API key
- **API Model Name** — The Gemini model to use (e.g., `gemini-1.5-flash`, `gemini-2.0-flash`)
- **API Version** — The API version (e.g., `v1`, `v1beta`)

See [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) for an overview of REDCap's AI tools and security considerations.

**Project-level override on this model.** When system-wide AI services are enabled, the values above can be overridden per project on the Edit Project Settings page by entering a *different endpoint URL, API key and model* for that project. Admins who did not want AI enabled everywhere were advised to leave the system-level fields blank and populate the project-level fields only where wanted. From 17.2.0 this works differently — the project picks a named configuration from a drop-down rather than re-entering credentials. See [RC-CC-26 — Control Center: AI Configuration Settings](RC-CC-26_Control-Center-AI-Configuration-Settings.md).

---

# 2. Common Questions

**Q: What is the difference between enabling a feature here and enabling it at the project level?**
System-level settings on this page are the master on/off switches — if a feature is disabled here, no project can use it, regardless of project settings. If a feature is enabled here, project-level settings then control whether individual projects use it. For example, if "Surveys" is disabled here, no project can create surveys even if they want to. If it is enabled here, each project can independently choose whether to use surveys.

**Q: Should I enable the REDCap Mobile App if we are not planning to use it?**
It is safe to leave unused features enabled — they simply will not appear in projects where they are not configured. Leaving the Mobile App enabled allows projects to start using it if research needs change, without requiring administrator intervention to toggle the system setting. However, if your institutional policy is to restrict certain features (e.g., for compliance reasons), disable them here.

**Q: What do I need to configure to use SendGrid for alerts and notifications?**
System-level configuration of SendGrid on this page (Modules/Services) enables SendGrid as an option for template-based emails in Alerts & Notifications. A separate SendGrid API key in General Configuration is used for sending general REDCap emails. Both configurations are required if you want to use SendGrid for both email delivery and alert templates.

**Q: Should I enable text-to-speech if my users' browsers do not support it?**
Text-to-speech relies on the IBM Watson service hosted by Vanderbilt and is supported in modern browsers. If your users are on older browsers that do not support the Web Audio API, text-to-speech will fail silently. Enabling it causes no harm — users on unsupported browsers simply will not see the text-to-speech button on surveys.

**Q: How do I decide whether to use OpenAI, Gemini, or a locally-hosted AI model?**
OpenAI (Azure) and Google Gemini are cloud-hosted, managed services that require no infrastructure on your side but may involve data transmission to external services. Locally-hosted OpenAI-compatible models (LM Studio, Ollama) keep all data on-premises but require server resources and ongoing maintenance. Choose based on your data governance requirements and available infrastructure.

---

# 3. Common Mistakes & Gotchas

**Enabling third-party service features (SMS, AI) without configuring the required credentials.** Enabling Twilio, SendGrid, or AI services without entering valid API credentials leaves users unable to use the feature and can generate confusing error messages. Always test third-party integrations in a staging environment and verify that API keys are correct and active before rolling out to production.

**Disabling core features that projects are already using.** If you disable Surveys or the API after projects are using them, those projects will experience broken functionality. Document which features are in use before disabling anything, and communicate deprecation timelines to project owners if you plan to remove a feature.

**Misconfiguring email service (SMTP vs. third-party API).** If you enable a third-party email provider (SendGrid, Mailgun, etc.) and it is not correctly configured, all outgoing emails (alerts, survey invitations, etc.) will fail silently. Test email delivery in staging before rolling out, and monitor the first few days of production use to catch any issues.

---

# 4. Related Articles

- [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) (overview of AI features enabled by this page)
- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) (related system-wide settings)
- [RC-CC-05 — Control Center: File Storage & Upload Settings](RC-CC-05_Control-Center-File-Storage-Settings.md) (file-related module settings)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)(alert configuration and SendGrid integration)
- [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md)(external module concepts and management)
- [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md) (mobile app module configuration)
- [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md) (MyCap module configuration)
- [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) (randomization module configuration)
- [RC-TXT-01 — Texting in REDCap: Setup and Usage](RC-TXT-01_Texting-in-REDCap-Setup-and-Usage.md)(SMS service configuration and usage)
