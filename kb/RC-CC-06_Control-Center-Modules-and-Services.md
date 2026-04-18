RC-CC-06

**Control Center: Modules & Services Configuration**

| **Article ID** | RC-CC-06 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-05 — File Storage & Upload Settings; RC-CC-02 — General Configuration; RC-ALERT-01 — Alerts & Notifications; RC-EM-01 — External Modules Overview; RC-INST-01 — Institution-Specific Settings & Policies; RC-AI-01 — REDCap AI Tools: Overview & Security; RC-AI-02 — AI Writing Tools; RC-AI-03 — AI Translations; RC-AI-04 — AI Summarization |

---

The **Modules/Services Configuration** page (under **System Configuration**) is the largest configuration page in the Control Center. It controls which features and integrations are enabled across the entire instance, and includes settings for third-party services like SMS platforms and email delivery providers.

---

# External Module Framework

<!-- PLACEHOLDER: Insert annotated screenshot of External Module Framework section -->

**Enable the Built-in Process for Users to Request External Module Activation**
When enabled, a "Request Activation" button appears in project External Module lists, allowing users to submit a request to the REDCap administrator to activate a specific module for their project. This provides a managed workflow for EM activation rather than requiring direct contact with an administrator.

> **Note:** The Request Activation button only appears for modules that have been marked as "Discoverable" by the administrator. Modules that are not discoverable will not show the button even when this setting is on.

For the full External Modules policy and activation process, see your institution's External Modules documentation.

---

# Feature Enable/Disable Table

<!-- PLACEHOLDER: Insert annotated screenshot of feature enable/disable table -->

The following features can be enabled or disabled system-wide. When a feature is disabled here, it is unavailable in all projects regardless of project-level settings.

| Feature | Notes |
| --- | --- |
| **Surveys** | Enables the survey functionality across all projects. A sub-setting controls **Google reCAPTCHA** on public surveys — see the reCAPTCHA section below |
| **URL Shortening Service** | Enables short link generation for public survey links, public project dashboards, and public report links via the REDCAP.LINK service hosted by Vanderbilt on AWS. Disable if your server cannot make outbound HTTP requests to the public web |
| **Randomization** | Enables the randomization module; see RC-RAND-01 |
| **REDCap Shared Library** | Enables access to the Consortium's instrument-sharing library on the Online Designer page |
| **REDCap Messenger** | Enables the in-platform messaging system between users. A sub-setting controls whether users are allowed to message administrators directly |
| **REDCap API** | Enables API access for all projects; see RC-API-01 |
| **REDCap Mobile App** | Enables offline data collection via the mobile app. Users must be explicitly granted mobile app privileges within a project to use it; see RC-MOB-01 |
| **MyCap Mobile App** | Enables MyCap participant mobile app support. When enabled, a per-project toggle determines whether individual projects use MyCap. A sub-setting controls whether project users can enable MyCap themselves or whether an administrator must do so. See RC-MYCAP-01. **Note on limitations:** MyCap does not support piping, smart variables, field embedding, special functions, calculated fields, or most action tags (@HIDDEN and @MC-prefixed tags *are* supported). Branching logic is partially supported (simple single-statement logic only — no AND, OR, or special functions) |
| **External Modules Alternate Directory** | Allows loading external modules from a non-default directory path. Useful for staging or internal module development. Multiple directories can be separated with a pipe \| |
| **File Version History for 'File Upload' Fields** | When enabled, users can upload a new file to a File Upload field without deleting the current one — previous versions are preserved and accessible from the Data History popup. If disabled, users must delete the current file before uploading a replacement. Can be enabled or disabled per project on the Project Setup page |
| **Field Bank in the Online Designer** | Enables the 'Import from Field Bank' button in the Online Designer, allowing users to pull fields from standardized instrument catalogs. If disabled, the button is hidden for all users |
| **Video Embedding on Forms & Surveys** | Allows a video URL to be attached to a Descriptive field, displaying a play button that opens the video in a popup. Compatible with most hosting services; most reliable with YouTube and Vimeo |
| **Text-to-Speech for Surveys** | Enables text-to-speech on survey pages, reading survey text aloud via the IBM Watson Text-to-Speech API hosted by Vanderbilt University. Requires the REDCap server to be able to make outbound HTTP requests to `https://redcap.vumc.org` |
| **Auto-Suggest for Biomedical Ontologies** | Enables the BioPortal ontology lookup service for fields on forms and surveys. Requires a valid BioPortal API token and outbound HTTP access to `https://data.bioontology.org/` |
| **Data Entry Trigger** | Enables the Data Entry Trigger feature for all projects. When enabled, users can configure a URL that REDCap will POST to whenever a record is created or modified via normal data entry or a survey response. **Not triggered by** API imports, data imports via the import tool, or Mobile App imports; see RC-INTG-01 |
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

<!-- PLACEHOLDER: Insert annotated screenshot of Twilio section -->

Twilio is a third-party service that enables SMS and voice call delivery for survey invitations and alerts. Requires a Twilio account and configuration of account credentials in REDCap.

- **Enable Twilio** — Enables or disables the integration globally. Requires a Twilio account and credentials. The REDCap server must be able to make outbound HTTPS requests to `https://api.twilio.com`, and the server must be publicly reachable from the web so Twilio can POST back to it
- **Who Can Enable Twilio in a Project** — Three options:
  - *All users* — any user with Project Design/Setup rights can enable Twilio in their project
  - *Admin approval* — users can see the setting and request activation, but an administrator must approve before the service is active
  - *Administrators only* — the setting is hidden from non-admin users entirely
- **Display Twilio Information to All Users** — Only relevant when "Administrators only" is selected. Controls whether Twilio is advertised on the Project Setup page; set to "No" to keep Twilio invisible to regular users

See RC-TXT-01 and RC-TXT-02 for more on texting workflows and administrator setup.

## Mosio (SMS)

Mosio is an alternative SMS service provider. Configuration mirrors Twilio, including the same three-option access control (All users / Admin approval / Administrators only) and the "Display information to all users" visibility toggle. Requires outbound HTTPS access to `https://api.mosio.com` and a publicly reachable server. See your institution's SMS strategy documentation before enabling.

## SendGrid (Email Templates)

SendGrid is an external email delivery service that enables template-based emails for Alerts & Notifications. Requires a SendGrid account and API key, and outbound HTTPS access to `https://api.sendgrid.com/v3`. Access control has two options: *All users* or *Administrators only* (no Admin approval option). Includes the same "Display information to all users" visibility toggle. See your institution's email delivery architecture before enabling.

---

# Statistics & Charts

<!-- PLACEHOLDER: Insert annotated screenshot of Stats & Charts section -->

**Enable Stats & Charts Module for All Projects**
Enables the Statistics & Charts feature globally. When enabled, project users can view aggregate data visualizations from the Stats & Charts tab.

**Allow Survey Respondents to View Aggregate Survey Results**
When enabled, project administrators can opt to show a respondent their responses plotted against aggregate data after completing a survey.

---

# e-Consent Framework for PDF Auto-Archiver

<!-- PLACEHOLDER: Insert annotated screenshot of e-Consent section -->

**Display 'e-Consent Framework' Option for All Surveys**
Makes the e-Consent configuration option visible in survey settings across all projects.

**Capture IP Address of Participants**
When an e-Consent is certified, the participant's IP address is stored in the File Repository table as part of the e-Consent record.

**Custom Message for e-Consent Framework Settings**
Optional text shown to project administrators when configuring e-Consent. A good place to link to institutional guidance on electronic consent requirements.

See RC-SURV-08 for detailed e-Consent setup documentation.

---

# Alerts & Notifications Settings

<!-- PLACEHOLDER: Insert annotated screenshot of Alerts & Notifications Settings section -->

These settings control what information users can include in alert recipient fields:

- **Allow normal users to use project variables for email fields** — Allows To/CC/BCC fields in alerts to reference project fields containing email addresses
- **Allow normal users to manually enter freeform email addresses** — Allows free-text email entry in alert recipient fields; can be further restricted by a domain allowlist
- **Domain allowlist for freeform email entry** — Optionally restricts freeform email addresses to specified domains
- **Allow normal users to use project variables for phone fields** — Allows recipient phone number fields to reference project data fields
- **Allow normal users to enter freeform phone numbers** — Allows manual phone number entry for SMS alerts

See RC-ALERT-01 for alert setup and RC-TXT-01 for SMS alert configuration.

---

# File Upload Field Enhancement

<!-- PLACEHOLDER: Insert annotated screenshot of File Upload Enhancement section -->

An optional enhancement that adds password verification before a file in a File Upload field can be accessed, with optional automatic archiving to external storage. Requires specific configuration for full Part 11 compliance workflows. Leave disabled unless your institution has a specific FDA or Part 11 compliance requirement.

---

# Rapid Retrieval (Page-Level Caching)

<!-- PLACEHOLDER: Insert annotated screenshot of Rapid Retrieval section -->

Rapid Retrieval caches certain REDCap pages to improve load times on large or high-traffic instances. Can be configured to use file-based or database-based storage. An alternative directory can be specified for the cache.

---

# Record-Level Locking Enhancement

<!-- PLACEHOLDER: Insert annotated screenshot of Record-Level Locking section -->

An optional enhancement to the record locking feature that generates a PDF confirmation when a record is locked, with optional automatic archiving to external storage. Primarily useful for studies that require a full Part 11-compliant electronic signature and audit trail. Leave disabled unless there is a specific regulatory requirement.

---

# e-Consent Framework: PDF External Storage Settings

<!-- PLACEHOLDER: Insert annotated screenshot of e-Consent PDF Storage section -->

When the e-Consent Framework is used in Part 11-compliant workflows, this section allows the e-Consent PDFs to be automatically archived to an external storage location (same options as the File Upload Settings storage configuration). Leave disabled unless required for regulatory compliance.

---

# AI Services

<!-- PLACEHOLDER: Insert annotated screenshot of AI Services section -->

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
| **Feature 1 — Writing Tools** | A magic wand icon appears in the toolbar of all rich text editors throughout REDCap (except the @RICHTEXT action tag). Users can alter and enhance text including changing length, tone, and reading level. See RC-AI-02 |
| **Feature 2 — Summarize free-form text on reports** | A magic wand icon appears next to free-form text fields on reports, allowing users to have the AI service summarize field values across the report. See RC-AI-04 |
| **Feature 3 — Auto-translate on MLM setup page** | On the Multi-Language Management page, a button appears that auto-translates all untranslated text in one click. See RC-AI-03 |

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

See RC-AI-01 for an overview of REDCap's AI tools and security considerations.
