---
id: RC-PLUS-03
title: 'REDCap+: Reward Services'
domain: REDCap+
applies_to:
- REDCap Administrators configuring the service (§3–5)
- study teams running participant compensation (§6–7)
requires: REDCap v17.0.0+ and a REDCap+ subscription. Also requires a funded institutional
  account with the third-party gift card provider — see §2
verified_against: REDCap 17.3.6 (LTS) — Control Center configuration (§4–5) verified
  against a live instance; project-level interface (§6) checked against source code
  only (not observed live) — see the scope note. Checked against source code of v17.6.5
  (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- 'RC-PLUS-01 — REDCap+: Overview and Subscription'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-PLUS-01
  title: 'REDCap+: Overview and Subscription'
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-CC-09
  title: 'Control Center: To-Do List'
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-PROJ-02
  title: Project Setup Checklist
- id: RC-INFRA-03
  title: REDCap Versions, Release Lines & Patching
tags:
- redcap+
synonyms:
- how do i pay participants in redcap
- participant compensation redcap
- gift card integration
- tango card redcap
- reward services setup
- incentive payments to study participants
- who approves participant payments in redcap
- rewards sandbox vs production
- reward options manager role
---

> **Scope note.** Sections 4 and 5 are verified against the Control Center of a live instance running 17.3.6 LTS. Sections 1–3 and 6 were first written from REDCap's 17.0.0 release notes and have since been **checked against REDCap's source code** (v17.6.5 Standard / v17.3.31 LTS), but they have still **not been observed live** on a subscribed instance with the feature active. Exact screen labels and workflow details inside a project should be confirmed before this article is used as a step-by-step guide.
>
> **Why the project-level sections have not been observed live — a standing limitation.** The instance this KB is maintained against does **not** hold a REDCap+ subscription. The Control Center sections could still be documented because gating on the *Modules/Services Configuration* page is cosmetic: the settings are rendered server-side and merely disabled in the browser, so the page is readable without a subscription. This does not hold for every REDCap+ page — see [RC-PLUS-01](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) §4a. The project-level interface is different — Reward Services must actually be *enabled* in a project before the Participant Manager and the reward workflow exist to be looked at, and enabling it requires the subscription. No amount of reading an unsubscribed instance will close that gap; a source-code check confirms behaviour but not the exact wording on screen.
>
> **What would close it:** a page capture or walkthrough from an institution running Reward Services in production. Until then, treat §6 and the permission behaviour in §3 as source-checked but not observed. The version caveats in §7 are drawn from the release notes and are unaffected by this limitation.
>
> **This article documents how the REDCap feature works. It is not financial, tax or compliance guidance.** Participant compensation carries institutional obligations — tax reporting thresholds, IRB-approved compensation schedules, treasury and procurement rules — that vary by institution and jurisdiction. Involve your finance and compliance offices before the first order is placed, not after.

---

# 1. Overview

**Reward Services** (also called **REDCap Rewards**) manages participant compensation inside REDCap: tracking who is owed what, routing each payment through an approval chain, and then issuing it as an **electronic gift card**.

The critical architectural fact is that **REDCap does not hold or move the money**. The feature integrates with a third-party gift card vendor, **Tango**, through the Tango Card API. The flow is:

1. Your institution opens an account with Tango and **deposits funds into it**.
2. REDCap authenticates to the Tango API using credentials you configure.
3. When a reward order is placed in REDCap, the service **withdraws from your institutional Tango balance** and issues an electronic gift card to the participant.

So the money is Tango's problem and your finance office's problem; REDCap's role is eligibility, approval, authorization and order placement. That division matters when troubleshooting: an order that fails for lack of funds is not a REDCap fault.

REDCap publishes a **Rewards document package** — a detailed feature overview, guidance on setting up and using the vendor's website, pre-made Project XML files that can be turned into Project Templates for reward-enabled projects, and SOPs for using the feature in a project. It is linked directly from the Reward Services section of the Control Center (§4). For an institution standing this up, that package is the starting point, not this article.

---

# 2. Prerequisites

| Requirement | Notes |
| --- | --- |
| REDCap **17.0.0 or later** | Reward Services was introduced as a REDCap+ feature in 17.0.0 |
| A **REDCap+ subscription** | The Control Center explicitly states: *"You must have a REDCap+ subscription to enable and configure this setting."* |
| An **institutional Tango account**, funded | Set up on the vendor's website; funds must be deposited before orders can be fulfilled |
| **Outbound HTTPS from the REDCap server** | The Control Center warns that the web server must be able to make outbound HTTP/HTTPS requests to the rewards provider API. A server behind a restrictive firewall cannot use the feature |
| A working **cron job** | Scheduled workflow steps, including scheduled orders, are processed by a cron task (§6.6). See [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) |

> **Note:** The subscription requirement here is unlike the Project Migration Tool's, which is asymmetric. Reward Services simply requires a subscription on the instance using it. LTS 16 contains some early Rewards code but lacks much of the configuration described here, so treat 17.0.0 as the practical minimum.

---

# 3. The Role-Based Workflow

Reward Services separates participant compensation into **four workflow roles**. This is the design feature that distinguishes it from paying participants out of a spreadsheet: the person who decides a participant is *eligible* is not the person who commits the *money*, and neither is the person who *places the order*.

| Role | Responsibility |
| --- | --- |
| **Reviewer** | Confirms eligibility. Approves or rejects compensation against predefined criteria, ensuring only eligible participants receive rewards |
| **Payment Authorizer** | Commits the money. Provides **final financial approval between eligibility review and order placement**, checking the payment against budgetary and institutional guidelines |
| **Order Manager** | Fulfils. Places orders for financially authorized rewards so participants receive their redeem codes and notifications. A user who can place orders can also reject a reward at that stage |
| **Rewards Options Manager** | Configures. Creates and modifies the reward options available to participants — amounts, products, currency, eligibility conditions |

Each reward carries a **status** reflecting its stage in that chain, so at any point you can see which rewards are awaiting review, awaiting authorization, or awaiting fulfilment (§6.5).

## 3.1 Configuration and viewing permissions

The four roles are the practical way to think about the workflow, but they are granted as individual **Rewards permissions**, and the list goes beyond the four roles. Alongside them sit:

| Permission | What it allows |
| --- | --- |
| **Manage permissions** | Grant and remove Rewards permissions for other project users (the **Permissions** tab) |
| **Manage project settings** | Change the project's Rewards settings (the **Settings** tab) |
| **Manage API settings** | Change which vendor account and credentials the project uses (the **API Settings** tab, §6.9) |
| **View logs** / **View orders** | Read-only access to Rewards activity and placed orders |

> **Important — two configuration permissions matter for separation of duties.** A user with **Manage permissions** can grant themselves any workflow role, so in practice they can hold all of them. A user with **Manage API settings** can point the project at a different vendor account or credentials. Treat both as being as sensitive as Payment Authorizer, and keep them away from the people who review and order.

> **Note — REDCap administrators automatically hold every Rewards permission.** They do not need to be granted them. (When an administrator views the project as another user, they see that user's permissions instead.) Separation of duties can therefore only be enforced among **non-admin** users; an administrator can always act at every stage.

> **The separation is the control.** Assigning one person all four roles is technically possible and removes the segregation of duties the feature exists to provide. Institutions with procurement or internal-audit requirements around disbursements will usually want at least the Payment Authorizer separated from the Reviewer and Order Manager.

**Bulk actions** are available across the workflow — approving, rejecting, or placing orders for many rewards at once. Useful at scale, and worth pairing with the segregation above, since a bulk approval commits many payments in one click.

---

# 4. System-Level Configuration

*Verified against 17.3.6 LTS.*

**Where:** Control Center → **Modules/Services Configuration** → **Reward Services**. The section carries a `REDCap+` badge and includes links to the Rewards document package and to Consortium call videos demonstrating setup and use.

## 4.1 Enablement settings

| Setting | Options | Effect |
| --- | --- | --- |
| **Enable Reward Services?** | Disabled / Enabled | The master switch. Enabling it here allows Reward Services to be *configured and utilized* in projects — but the feature must still be enabled per project |
| **Who can enable Reward Services in a given project?** | All users (who have Project Design privileges) / **Only administrators** can view the setting and enable it | Under "Only administrators", normal users do not even see the option on the project's Project Setup page |
| **Allow normal users to enable this feature on their own, or require a request?** | Yes, allow users with Project Setup/Design rights to enable it / No, an administrator must enable it via a user request | **Only used when the setting above is set to "All users."** Under "No", requests route to the Control Center To-Do List for admin action |
| **Custom message when enabling Reward Services in a project** | Free text, **HTML permitted** | Displayed to users when they attempt to enable Rewards at the project level. Intended for terms of service, institutional guidelines or instructions |
| **Bypass sensitive confirmation when managing Rewards permissions?** | Disabled / Enabled | See §4.2 |

> **The two enablement settings interact, and the second is conditional on the first.** "Who can enable…" is the gate; "Allow normal users to enable this feature on their own…" only takes effect when that gate is set to "All users". Setting the gate to "Only administrators" makes the second setting irrelevant — a common source of confusion when an admin changes one and expects the other to follow.

The **custom message** field is worth using. It is the one place in the workflow where an institution can put its compensation policy in front of a study team at the moment they turn the feature on.

## 4.2 The sensitive-action confirmation bypass

Managing Rewards permissions is treated as a sensitive action, which by default requires both an audit reason **and** an extra confirmation step.

From **17.1.3**, administrators can enable **"Bypass sensitive confirmation when managing Rewards permissions?"**. When enabled, users managing Rewards permissions must **still enter a reason that is logged for auditing** — only the additional confirmation step is dropped.

> **Note:** This reduces friction, not accountability. The audit reason remains mandatory either way. Institutions that want the extra deliberate step before permission changes should leave it Disabled.

---

# 5. Vendor Credentials and Environments

*Verified against 17.3.6 LTS.*

Four credential fields plus an environment selector configure REDCap's connection to Tango:

| Field | Purpose |
| --- | --- |
| **Environment** | *No environment selected* / **Production** / **Sandbox**, with a **Check** button to test the connection |
| **Client ID** | Institutional API client identifier |
| **Client Secret** | Institutional API client secret |
| **Tango Service Account Username** | Tango requires a service account token using the password grant |
| **Tango Service Account Password** | Used together with the Client ID and Client Secret to acquire a service account token |

## 5.1 System defaults and project overrides

These values are the **system-level defaults that projects inherit** when a project selects **"Use System Default"** on its API settings page.

> **Critical — project-level credentials override the system defaults entirely.** Where a project sets its own credentials, those are used instead of the values configured here. A project with its own credentials will not follow a change made at the system level. Where an institution runs everything from one funded account, leaving projects on "Use System Default" keeps a single point of control; where individual studies hold their own Tango accounts, expect system-level changes not to reach them.

## 5.2 "No environment selected"

The environment selector's third option exists for a specific reason, stated on the page: choose **No environment selected** when you need to leave the defaults incomplete, and **REDCap will preserve any credentials already entered instead of clearing them**.

This is the safe way to stage a configuration — enter credentials without committing the instance to either environment.

## 5.3 Sandbox before Production

REDCap **strongly recommends** validating the configuration in the Tango **Sandbox** before enabling Rewards in production. The stated sequence:

1. Create a sandbox account through the vendor's portal.
2. Once approved, log in to the sandbox portal and review the available reward options and settings.
3. Complete the initial setup following the vendor's official documentation.
4. **Simulate the full rewards lifecycle end to end** — eligibility review, authorization, and order placement — to confirm roles, permissions and integrations behave as expected.

> **Why this matters more than the usual "test first" advice.** Every other REDCap feature can be tested with throwaway data at no cost. Here, a misconfigured Production environment sends real gift cards, funded by real institutional money, to real people — and a gift card issued in error is not straightforwardly recoverable. The sandbox is the only place the workflow can be rehearsed without financial consequence.

---

# 6. Using Reward Services in a Project

> **Checked against source code, not observed live.** This section was checked against REDCap's source code (v17.6.5 Standard / v17.3.31 LTS) but has not been seen on a subscribed instance — the pages described here only exist once Reward Services is enabled in a project, which requires the subscription. Behaviour is described as the code implements it; exact on-screen labels may differ. See the scope note at the top of this article.

## 6.1 Enabling it in the project

Once enabled system-wide, Reward Services must be turned on for each project. Depending on the settings in §4.1, a user with Project Setup/Design rights either enables it themselves, or submits a request that an administrator processes from the Control Center **To-Do List** — see [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md).

## 6.2 Finding it: the Rewards link and its tabs

Once enabled, a **Rewards** link appears in the project's left-hand menu. It carries a **counter** for reports that currently have rewards ready for attention. The link is hidden when the project is locked or archived, and when the instance's REDCap+ subscription is not active.

The Rewards page is organised into tabs:

| Tab | Who can open it |
| --- | --- |
| **Information** | Any user with access to the Rewards page |
| **Participant Manager** | Any user with access to the Rewards page; the actions offered depend on the user's workflow permissions (§3) |
| **Reports** | Any user with access to the Rewards page |
| **Settings** | Users with **Manage project settings** |
| **Permissions** | Users with **Manage permissions** |
| **API Settings** | Users with **Manage API settings** |

A separate Rewards **Logs** page is controlled by the standard **Project Design and Setup** user right rather than by a Rewards permission. It remains available after Reward Services has been turned off in the project, so the audit trail stays readable.

## 6.3 The Participant Manager and data access

The **Participant Manager** is the working surface. It presents participant details in a flat layout with **rewards displayed as individual columns**, so each participant's reward statuses and the actions available on them are visible in one place. **Bulk actions** apply the same step to many rewards at once.

What a user sees is scoped by their ordinary project rights, not only by their Rewards permissions:

- **Data Access Groups** — a user assigned to a DAG sees only the records in that DAG.
- **Data viewing and data export rights** — the participant data shown alongside rewards, and what can be exported, follow the user's existing viewing and export rights.

## 6.4 Reward options

A **reward option** defines one reward a participant can earn. Users with **Manage reward options** (the Rewards Options Manager role) create and edit them.

| Field | Purpose |
| --- | --- |
| **Product ID** | The vendor's identifier for the gift card product |
| **Description** | A description of the reward |
| **Amount** | The value of the reward |
| **Currency** | Defaults to **USD** |
| **Eligibility logic** | REDCap logic that decides when a record becomes eligible for this reward — written like branching logic (see [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)) |

> **Important — edits to a reward option apply only to entries not yet in review.** Once a reward has entered review (or a later stage), it keeps the terms it had at that point; changing the option's amount, product, currency or eligibility logic affects only rewards that have not reached review. On older versions this did not hold for reported totals — see §7.

## 6.5 Workflow statuses

Each reward moves through a status that shows where it sits in the chain. In plain terms (on-screen wording may differ):

| Stage | Statuses |
| --- | --- |
| Eligibility | Pending eligibility; eligible; ineligible; invalid |
| Review | Reviewer approved; reviewer rejected |
| Authorization | Payment approved; payment rejected |
| Fulfilment | Order placed; completed |
| Other | Canceled; error |

Each workflow step can also be **scheduled**, which gives it a corresponding "scheduled" status until the step runs (§6.6).

## 6.6 Scheduling

**Any workflow step can be scheduled** — review, payment authorization and order placement — not only orders. Scheduled steps are carried out by a REDCap cron task. Two consequences:

- If the REDCap cron is not running, scheduled steps will not happen and nothing tells the study team. See [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md).
- The scheduled-orders cron task has been a source of defects — see §7.

## 6.7 Reports and email digests

The **Reports** tab holds the Rewards reports, which help each role find the rewards waiting on them; the left-menu counter reflects reports that have rewards ready. Users can also set up **recurring email digests** of these reports, so reviewers, authorizers and order managers are told what is waiting instead of having to check the page.

## 6.8 Rewards Smart Variables

When Reward Services is enabled, a **Rewards** category appears in the project's Smart Variables list (it is hidden otherwise — see [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md)). These variables pipe details of a specific reward option for a record:

- the reward **amount**, **product ID** and **product name**;
- the reward's **status**;
- the **REDCap order ID** and the **provider order ID**;
- the **reward URL** or **reward link**;
- **redemption** details — redemption details, link, URL, code, instructions and credentials.

Use the Smart Variables list in your project for the exact syntax.

> **Note:** The reward link and redemption variables carry what a participant needs to redeem the gift card. Pipe them only into messages sent to that participant, never into staff alerts or reports that are shared more widely.

## 6.9 Project API settings

The **API Settings** tab (needs **Manage API settings**) connects the project to the vendor:

| Setting | Purpose |
| --- | --- |
| **Group Identifier** | The vendor's **Customer** that the project orders under |
| **Campaign Identifier** | The vendor's **Account** (the funded balance) that the project draws from |
| **Credentials** | **Use System Default** (the Control Center values, §5) or the project's own credentials as an optional override |

Choosing project-level credentials detaches the project from future Control Center changes — see §5.1.

---

# 7. Known Issues by Version

Reward Services shipped in 17.0.0, but Rewards-related code was present and running earlier — which produced defects on instances that were not using the feature at all.

> **Critical — historical compensation totals can be wrong after editing a reward option (below 17.4.1 Standard / 17.3.7 LTS).** Where an option's **amount, product, currency, or eligibility conditions** are edited *after* review or scheduling has begun, users see **inaccurate historical compensation and order totals** in the Participant Manager, in Rewards reports, and in **CSV exports**. Financial figures pulled for reconciliation or reporting on affected versions cannot be trusted. This is the most recently fixed defect in the feature and shipped on both release lines on the same day.

> **Critical — the project-level enable option was visible to normal users despite the "Only administrators" setting (below 17.2.1 Standard).** With Reward Services enabled system-wide and *"Who can enable Reward Services in a given project?"* set to **Only administrators**, the project-level option was still shown to normal users on the Project Setup page. An institution that used that setting as its control on who can spend money did not have the control it thought it had.

> **Version caveat (below 17.2.1 Standard):** When a user triggered a request for an admin to enable Reward Services in a project, the request popup on the **To-Do List** page was blank — preventing administrators from processing Reward Services requests there at all.

> **Version caveat (below 17.3.1 Standard):** In projects using **non-numeric record IDs**, users could encounter an error when viewing reward records after adding a reward option.

> **Version caveat (below 16.0.6 Standard / 15.5.30 LTS):** The Rewards-related cron job could be recorded with an incorrect enabled/disabled value in the database, **causing it to run despite the feature being turned off**. This affected instances that had never enabled Reward Services.

> **Version caveat (15.5.5 Standard, Major):** The cron job that processes scheduled reward orders could crash repeatedly. The bug emerged in the immediately preceding version.

> **Version caveat (below 15.6.1 Standard / 15.5.10 LTS):** REDCap's own **Smart Variables documentation** listed Rewards-related Smart Variables before the feature had been released. Anyone who built logic against those documented variables on an affected version was referencing something that did not exist. See [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md).

---

# 8. Common Questions

**Q: Does REDCap hold our money?**

**A:** No. Your institution funds an account with Tango, and REDCap draws against that balance through the Tango API when an order is placed. REDCap manages eligibility, approval and ordering; the funds sit with the vendor.

**Q: What do we need before we can turn this on?**

**A:** REDCap 17.0.0+, a REDCap+ subscription, a funded institutional Tango account, outbound HTTPS from the REDCap server to the provider's API, and a working cron. Then configure the credentials in the Control Center.

**Q: Can one person run the whole process?**

**A:** Technically yes — the four roles can be held by one user, and REDCap administrators hold every Rewards permission automatically. Doing so removes the segregation of duties the workflow is built around, specifically the separation of eligibility review from financial authorization. Most institutions with procurement or audit requirements will want at least the Payment Authorizer held separately — and **Manage permissions** and **Manage API settings** kept away from reviewers and order managers, since either can undo the separation (§3.1).

**Q: We changed the Tango credentials in the Control Center but one project is still using the old ones. Why?**

**A:** That project has project-level credentials set, which override the system defaults entirely. Only projects set to **"Use System Default"** on their API settings page follow the Control Center values.

**Q: Should we test in Sandbox first?**

**A:** Yes, and this is stronger advice than the usual. In Production the feature sends real gift cards funded by real institutional money to real participants, and an erroneously issued card is not easily recovered. Rehearse the full lifecycle — review, authorization, order placement — in the sandbox first.

**Q: A user asked us to enable Rewards in their project and the To-Do List popup is empty.**

**A:** A defect below 17.2.1 Standard made that popup blank, preventing admins from processing Reward Services requests via the To-Do List. Upgrade, or enable the feature for the project directly.

**Q: Our compensation totals don't reconcile with what we think we paid out. Where do we start?**

**A:** Check the version first. Below 17.4.1 Standard / 17.3.7 LTS, editing a reward option's amount, product, currency or eligibility conditions after review or scheduling had begun produced inaccurate historical totals in the Participant Manager, Rewards reports **and CSV exports**. If the instance is on an affected version and anyone edited an option mid-study, the discrepancy may be a display defect rather than a payment error.

**Q: We don't use Rewards at all — why is there a Rewards cron job running?**

**A:** Below 16.0.6 Standard / 15.5.30 LTS, the Rewards cron could be recorded with the wrong enabled/disabled value and run despite the feature being off. It is fixed; on an affected version it is a known defect rather than a sign the feature is active.

---

# 9. Common Mistakes & Gotchas

**Assuming the "Only administrators" setting was actually enforcing.** Below 17.2.1 Standard, normal users could still see the project-level enable option regardless. If your instance ran on an affected version, check which projects have Rewards enabled rather than assuming the setting held.

**Editing a reward option mid-study.** Changing an option's amount, product, currency or eligibility conditions after review or scheduling has begun corrupted historical totals below 17.4.1 / 17.3.7. Even on a fixed version, changing the terms of a reward partway through a study is a decision to make with the study team and IRB, not a configuration tweak.

**Expecting a system-level credential change to reach every project.** Projects holding their own credentials override the system defaults and will not follow. Confirm which projects are set to "Use System Default" before treating a Control Center change as instance-wide.

**Configuring Production before rehearsing in Sandbox.** The one REDCap feature where a misconfiguration spends money and reaches participants irreversibly. The sandbox exists for this.

**Giving one user all four roles.** It works, and it dissolves the separation between deciding someone is eligible and committing the funds — which is most of the reason to use the feature rather than a spreadsheet.

**Overlooking the configuration permissions.** Separating the four workflow roles achieves little if a reviewer or order manager also holds **Manage permissions** (and can grant themselves the rest) or **Manage API settings** (and can change which account pays). Remember too that REDCap administrators hold every Rewards permission automatically.

**Forgetting the cron.** Scheduled workflow steps, including scheduled orders, are carried out by a REDCap cron task. No cron, no scheduled steps — and the failure is silent from the study team's perspective.

**Overlooking the outbound-connectivity requirement.** A REDCap server that cannot make outbound HTTPS requests to the provider's API cannot use the feature at all. Worth confirming with your network team before promising it to a study.

**Treating the Bypass setting as removing the audit trail.** It does not. The audit reason remains mandatory; only the extra confirmation step is dropped.

---

# 10. Related Articles

- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) — the page hosting all settings in §4 and §5
- [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md) — where project enablement requests are processed
- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) — cron configuration, which scheduled orders depend on
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) — how the Rewards permissions sit alongside standard project rights (DAGs, data viewing and export rights, Project Design)
- [RC-PROJ-02 — Project Setup Checklist](RC-PROJ-02_Project-Setup-Checklist.md) — where Rewards is enabled within a project
- [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md) — the other 17.0.0 REDCap+ feature
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — reading the Standard and LTS version windows in §7
