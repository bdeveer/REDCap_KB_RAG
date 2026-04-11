RC-AI-01

**REDCap AI Tools: Overview & Security**

| **Article ID** | RC-AI-01 |
| --- | --- |
| **Domain** | AI Tools |
| **Applies To** | All project types; feature availability depends on administrator configuration |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AI-02 — AI Writing Tools; RC-AI-03 — AI Translations; RC-AI-04 — AI Summarization |

---

# 1. Overview

This article introduces the AI features available in REDCap as of version 15.5.3. REDCap can communicate with an AI server to perform a set of pre-defined actions — text generation and editing, language translation, and data summarization. Unlike general-purpose AI chat tools, REDCap's AI features are purpose-built and integrated directly into specific parts of the application. This article explains what the three features are, how the underlying AI server architecture works, and what data privacy and security considerations apply before using these features with sensitive data.

---

# 2. Key Concepts & Definitions

## AI Server

The external server that processes AI requests from REDCap. REDCap does not connect to any public AI service (such as ChatGPT) directly. Instead, your institution's REDCap administrative team sets up a dedicated, standalone AI server. That server communicates only with REDCap and, by design, should not retain submitted data after processing.

## Pre-defined Actions

REDCap's AI features do not support open-ended chat. Instead, each feature offers a fixed set of operations — for example, "fix grammar," "translate," or "summarize." This approach gives users access to AI capabilities without requiring expertise in writing AI prompts.

## AI Writing Tools

The first of REDCap's three main AI features. Accessible anywhere the rich text editor is available, this feature generates or rewrites text based on a selected action (grammar correction, tone adjustment, length changes, etc.). See RC-AI-02 — AI Writing Tools for procedural details.

## AI Translations

The second main AI feature. Integrated directly into the Multi-Language Management (MLM) module, this feature automatically translates instrument content and the REDCap interface into a target language. See RC-AI-03 — AI Translations for procedural details.

## AI Summarization

The third main AI feature. Located in the Reports section of a project, this feature summarizes free-text variable data across records. See RC-AI-04 — AI Summarization for procedural details.

## Rich Text Editor

A text formatting interface found in several areas of REDCap (instrument field labels, survey settings text, email bodies, etc.). When enabled, the rich text editor toolbar includes the AI writing tools icon.

---

# 3. The Three AI Features at a Glance

| Feature | Where to find it | What it does |
|---|---|---|
| AI Writing Tools | Any field or area with a rich text editor (purple wizard's wand icon) | Generates, edits, corrects, or reformats text based on a selected action |
| AI Translations | Multi-Language Management module | Translates the REDCap interface and instrument content into a target language |
| AI Summarization | Reports (any report, including custom reports; purple wizard's wand icon in column headers) | Summarizes free-text variable data across records using a configurable prompt |

REDCap limits its AI functionality to these three features. Additional capabilities may be added in future versions.

---

# 4. AI Server Architecture & Security

## How the AI server works

REDCap's AI features rely on a standalone AI server provisioned and maintained by your institution's REDCap administrative team. This server is:

- **Isolated** — it communicates only with your REDCap instance, not with the public internet or external AI services.
- **Non-persistent** — it is not designed to retain submitted data between requests.
- **Institution-controlled** — your administrative team determines which AI model is used, how it is configured, and what compliance standards it meets.

This architecture means REDCap does not send your data to a third-party service like ChatGPT or a public API. The data goes to your institution's own server.

> **Important:** The security posture described above reflects the intended design. You should verify with your local REDCap administrative team that the AI server setup at your institution actually meets the relevant compliance and data privacy standards before using AI features with sensitive data such as Protected Health Information (PHI).

## Administrator controls

REDCap administrators can enable or disable each of the three AI features independently. Availability can be set globally (for all projects) or restricted to specific projects. If an AI feature is not visible in your project, it may not be enabled for your installation or your specific project. Contact your REDCap administrative team to confirm the local AI configuration.

> **Yale-specific:** [Describe which AI features are enabled, for which projects, and what the local data privacy policy is — leave blank until confirmed with Yale REDCap support team]

---

# 5. Common Questions

**What AI features does REDCap have?**
REDCap has three main AI features: AI Writing Tools (text generation and editing via the rich text editor), AI Translations (language translation integrated into Multi-Language Management), and AI Summarization (summarizing free-text variable data in reports).

**Does REDCap send my data to ChatGPT or another public AI service?**
No. REDCap is designed to use a standalone, institution-controlled AI server that is isolated from the public internet. Data submitted to the AI tools goes to that server, not to a public service. Confirm the specifics of your institution's setup with your REDCap administrative team.

**Can I use the AI features with PHI or other sensitive data?**
You should verify with your local REDCap administrative team before using AI features with sensitive data. The server architecture is designed to be compliant, but your team must confirm that the actual implementation meets all relevant standards for your use case.

**Why don't I see any AI features in my project?**
AI features may be disabled at the system level or restricted to certain projects by your REDCap administrator. Contact your REDCap administrative team to find out what is enabled for your installation.

**Can I write my own prompts or instructions to the AI?**
Yes, but only within the AI Writing Tools feature, which includes a custom prompt option. The other two features (Translations and Summarization) use system-defined prompts, though Summarization does allow you to modify the default prompt for a given variable.

**Will REDCap get more AI features in the future?**
As of version 15.5.3, REDCap provides three main AI features. Additional capabilities may be introduced in future releases.

---

# 6. Common Mistakes & Gotchas

**Assuming the AI server is equivalent to a public service.** The REDCap AI server is a dedicated, institution-managed server — not ChatGPT or a similar public API. Behavior, capabilities, and response quality may differ from what you experience with public AI tools.

**Using AI features with sensitive data without checking compliance first.** The architecture is designed for privacy, but your institution's specific implementation must be verified before you use any AI feature with PHI or other regulated data. Don't assume compliance — ask your REDCap administrative team.

**Not knowing which features are enabled.** Each of the three AI features can be turned on or off independently and can be restricted to specific projects. If a feature appears missing, it may simply be disabled — not absent from REDCap.

---

## Related Articles

- RC-AI-02 — AI Writing Tools
- RC-AI-03 — AI Translations
- RC-AI-04 — AI Summarization
- RC-NAV-UI-01 — Project Navigation UI
