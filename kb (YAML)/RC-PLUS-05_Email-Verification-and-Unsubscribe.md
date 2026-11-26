---
id: RC-PLUS-05
title: 'REDCap+: Email Verification & Unsubscribe'
domain: REDCap+
applies_to:
- Study teams sending participant emails
- REDCap Administrators (§3)
requires: REDCap v17.3.0+ and a REDCap+ subscription
verified_against: 'REDCap v17.5.6 (Standard) — on an unsubscribed test instance: Smart
  Variable definitions, menu item and page notice, read-only; 17.3.6 (LTS) — system-level
  setting (§3). Suppression, participant pages and dashboard checked against source
  code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS)'
prerequisites:
- 'RC-PLUS-01 — REDCap+: Overview and Subscription'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-PIPE-03
  title: 'Smart Variables: Overview'
- id: RC-ALERT-01
  title: 'Alerts & Notifications: Setup'
- id: RC-SURV-06
  title: Automated Survey Invitations
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
- id: RC-PLUS-01
  title: 'REDCap+: Overview and Subscription'
tags:
- redcap+
synonyms:
- email unsubscribe redcap
- let participants opt out of emails
- verify participant email address
- email-verify-link
- email-verify-url
- email-unsubscribe-link
- email-unsubscribe-url
- email-verified smart variable
- stop sending emails to a participant
- verified and unsubscribed emails page
- opt out link in survey invitations
---

> **Scope note.** The system-level setting in §3 is verified against a live instance running **17.3.6 LTS**. On **17.5.6** without a subscription, the Smart Variable definitions (§2) could be read in REDCap's Smart Variables documentation, and the project menu item and page introduction (§6) could be seen. How the links, flags, suppression, participant-facing pages and dashboard table behave needs an active subscription to observe, so that part has been checked against REDCap's source code rather than observed live. See [RC-PLUS-01 §4a](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) on what is and is not observable without one.

---

# 1. Overview

Two related REDCap+ features, introduced together in **17.3.0**:

- **Email Verification** — a participant confirms that an email address they supplied actually reaches them.
- **Email Unsubscribe** — a participant opts out of all emails from a project.

> **Note:** Both statuses belong to an **email address within a project**, not to a record. If several records in the same project share one email address, verifying or unsubscribing through any of them applies to all of them.

Both work through a suite of six **Smart Variables** plus a project dashboard page. Both are **entirely opt-in**: enabling the feature at system level makes the Smart Variables and the dashboard *available*, but nothing changes in any project until a user deliberately puts one of the Smart Variables into an email, an alert, or trigger logic.

> **This is a build-it-yourself feature, not a switch.** REDCap does not add an unsubscribe link to your emails, and does not start verifying addresses, because you turned the feature on. It gives you the links and the flags; where they go and what they gate is your design decision. A project that never uses the Smart Variables behaves exactly as it did before.

The one thing REDCap *does* enforce on your behalf is the suppression itself — see §5.

---

# 2. The Six Smart Variables

| Smart Variable | Type | Purpose |
| --- | --- | --- |
| `[email-verify-url]` | URL | The web address that verifies the participant's email address, without the link HTML |
| `[email-verify-link]` | Link | Generates a link the participant clicks to verify their email address. Default link text: "Verify Email Address" |
| `[email-verified]` | Flag | `1` if the participant's address has been verified, `0` if not. For use in logic |
| `[email-unsubscribe-url]` | URL | The web address that unsubscribes the participant, without the link HTML |
| `[email-unsubscribe-link]` | Link | Generates a link the participant clicks to unsubscribe from the project. Default link text: "Unsubscribe" |
| `[email-unsubscribed]` | Flag | `1` if the participant has unsubscribed, `0` if not. For use in logic |

The two link variables accept custom link text — for example `[email-verify-link:Please click here]` renders as a link reading "Please click here".

> **Note:** If the current participant has no associated email address in the project, all six return nothing: no URL, no link and no flag value.

**Which address counts.** The participant's address is the one in the project's designated email field (survey settings) or, if there is none, the email in the survey Participant List. The verify and unsubscribe links for an address are created the first time one of the link or URL variables is piped for it.

> **Note:** Ordinary users see these six in the Smart Variables documentation only while the instance has an active REDCap+ subscription. Administrators always see them listed, with or without a subscription.

The pattern is consistent: **a link or URL variable to put in an email, and a flag variable to put in logic.** They are designed to be used together.

These definitions match REDCap's own Smart Variables documentation on 17.5.6. See [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md).

---

# 3. System-Level Setting

*Verified against 17.3.6 LTS.*

**Where:** Control Center → **Modules/Services Configuration** → **Email Verification and Email Unsubscribe Features**, marked with a `REDCap+` badge and the note *"A REDCap+ subscription is required in order to use this feature."*

| Setting | Options | Default |
| --- | --- | --- |
| Email Verification and Email Unsubscribe Features | Disabled / **Enabled** | **Enabled** |

The on-page description: *"If enabled, a suite of Smart Variables and a dashboard page can be utilized by users in a project to allow participants to verify their email address or unsubscribe from all emails from the current project. If disabled, this feature and its Smart Variables will not be available to use in any project."*

## 3.1 What disabling does

1. The **Verified & Unsubscribed Emails** dashboard page is hidden from all projects.
2. All related Smart Variables are **hidden from the Smart Variable documentation**.
3. All six Smart Variables **pipe blank** in every project: no links, no URLs and no flag values.
4. The verify and unsubscribe links already sent to participants **stop working**. Clicking one shows an error page, so a participant can no longer unsubscribe, verify or re-subscribe.
5. **Suppression does not stop.** People who had already unsubscribed stay blocked from that project's emails (§5.1).

> **Critical — check dependent logic before disabling this on an instance where projects already use it.** The feature is enabled by default, so studies may have built unsubscribe links and flag-based trigger logic without an administrator ever making a decision about it. Once it is off, the flags are blank, so a condition like `[email-unsubscribed] = "0"` or `[email-verified] = "1"` becomes **false for everyone**. Every alert and ASI gated that way stops firing, including for participants who never unsubscribed. At the same time, people who already unsubscribed remain blocked, and the links in their inboxes no longer let them change that. Before switching it off, find the projects whose alerts, ASIs or calculations use these Smart Variables and agree a plan with those study teams.

## 3.2 When the subscription lapses

If the instance's REDCap+ subscription ends (after any grace period — see [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md)), the result is similar to disabling, with differences:

- The six Smart Variables pipe blank, so flag-gated alerts and ASIs stop firing in the same way as in §3.1.
- Suppression continues: unsubscribed addresses stay blocked.
- Links already sent to participants **still work**, so participants can still verify, unsubscribe and re-subscribe.
- The dashboard page shows only the subscription notice (§6); the table and its controls are not available.
- The verified/unsubscribed status line on the record's page is hidden.
- A blocked ASI is logged as a general send failure rather than as "Participant opted out".

---

# 4. Email Verification

A participant's email address **does not** need to be verified for them to receive emails. Verification is good practice, not a precondition — REDCap will happily send to an unverified address.

The intended pattern uses the two verification Smart Variables together:

1. **Capture and prompt.** A public survey collects an email address. An alert triggered on completion contains `[email-verify-link:Please click here]` — for example: *"Thanks for taking the survey. [email-verify-link:Please click here] to verify your email address."*
2. **Gate downstream sends.** Later alerts and ASIs add `[email-verified] = "1"` to their trigger logic, so nothing is sent or scheduled until the participant has actually verified.

That second step is what makes verification worth doing. Without it, verification records a fact nobody acts on; with it, the project stops sending follow-ups into addresses that were mistyped or never belonged to the participant.

---

# 5. Email Unsubscribe

Place `[email-unsubscribe-link]` wherever you want the opt-out to appear — conventionally at the foot of outgoing emails.

## 5.1 What happens when a participant unsubscribes

The participant sees a confirmation page: *"Your email address … has now been unsubscribed. You may now close this window."*, with a link to undo it straight away.

From then on, **REDCap refuses to send that address any email from that project.** This is enforced by REDCap, not by your logic: even if a user actively tries to email that participant from the project, the send is refused. The block covers:

- Alerts, ASIs and survey invitations sent from the Participant List
- Survey return-code emails and the "email myself a link" emails a participant requests from a survey page
- Any other project email addressed to that address

**CC and BCC.** The unsubscribed address is removed wherever it appears, including in CC or BCC. If **every** To address on a message is unsubscribed, the whole message is dropped, so staff in CC or BCC do not receive their copy either.

**SMS and voice are not affected.** Unsubscribing applies to email only; texting and voice-call invitations continue.

Each verify, unsubscribe and re-subscribe is recorded in the project's **Logging**, together with the email address.

> **Scope of the block:** unsubscribing applies to **one project only**. A participant who is also enrolled in another project on the same instance continues to receive that project's emails. There is no instance-wide opt-out.

## 5.2 Re-subscribing

The participant can undo it themselves, either from the link on the confirmation page or by clicking the unsubscribe link again, which opens a page offering a link to re-subscribe to the project. Study staff can also reverse an unsubscribe from the dashboard page (§6).

## 5.3 The critical distinction: scheduling vs sending

> **Critical — unsubscribing blocks the send, not the schedule.** Alerts and ASIs will **still be scheduled** for an unsubscribed participant. The block happens later, at the moment REDCap is ready to send: the email is not sent.
>
> The consequence is that a project can accumulate a queue of scheduled emails for people who will never receive them. Until the send time arrives, the schedule looks normal.
>
> To prevent scheduling in the first place, add `[email-unsubscribed] = "0"` to the trigger logic of your alerts and ASIs.

**What you see at send time:**

- **ASIs:** the invitation log shows the invitation as **Did not send**, with the reason **Participant opted out**.
- **Alerts:** the send counts as a failure, so if the alert is set up to send a failure notification, that notification goes out. A recurring alert keeps recurring and is blocked each time.

This is the single most important thing to understand about the feature. The safety net exists and works, but it operates one step later than most people assume, and relying on it alone leaves misleading state in the alert and invitation queues.

## 5.4 Getting notified of unsubscribes

REDCap's own suggested pattern: create an alert whose logic is **only** `[email-unsubscribed] = "1"`. It fires whenever a participant unsubscribes, which is a simple way to keep the study team informed of attrition.

---

# 6. The Verified & Unsubscribed Emails Page

Every project gains a dashboard page named **"Verified & Unsubscribed Emails"**, listing which email addresses in the project have been verified and which have unsubscribed.

> **Without a subscription (17.5.6):** The menu item appears and the page shows its introduction, then *"NOTICE: This feature is not available because it requires a REDCap+ subscription."* No table is shown.

**Access is restricted.** Only users with **Survey Distribution Tools** privileges *or* **Alerts & Notifications** privileges can view and manage the page. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md). A user assigned to a Data Access Group sees only their group's records.

## 6.1 Dashboard controls

With an active subscription, the page shows a table of addresses with **Verified**, **Verify Time**, **Unsubscribed** and **Unsubscribe Time** columns, plus:

| Control | What it does |
| --- | --- |
| **Auto-verify** | Marks an address as verified on the participant's behalf. Like a participant verifying, this can trigger calculations, alerts and ASIs that use `[email-verified]` (§7) |
| **Undo** (unsubscribe) | Re-subscribes an address after a confirmation (**Confirm re-subscribe**). Emails to it are sent again from then on |
| **Display as full record list** | Switches from listing only verified/unsubscribed addresses to listing every record with an email address |
| **Email status filter** | Shows verified and unsubscribed, verified only, or unsubscribed only |
| CSV download | Downloads the table |

> **Tip:** **Link Lookup** can decode a verify or unsubscribe link a participant forwards to you, so you can see what it points to.

## 6.2 Record page indicator

On the record's page, a status line shows **"Participant has unsubscribed from receiving emails."** or **"Participant's email address is verified."** when that applies to the record's email address.

> **Note:** The page is hidden entirely when the feature is disabled at system level (§3.1).

---

# 7. Side Effects on Calculations, Alerts and ASIs

> **Critical — verifying or unsubscribing is a data event that can trigger things.** REDCap states this directly: the act of verifying (or a staff member auto-verifying) or unsubscribing an email address **can trigger calculations, Automated Survey Invitations, and alerts** where the verify/unsubscribe Smart Variables appear in their logic. Because the status belongs to the address, this can happen on every record in the project that shares it.
>
> A participant clicking a link in their own time can therefore set off project logic — including sending them further emails, if an alert's condition happens to become true on verification. This is exactly what the intended `[email-verified] = "1"` gating pattern relies on, so it is by design; but it means the participant, not the study team, controls when that logic fires.

Worth thinking through before deploying: what becomes true the instant someone verifies, and is that what you want to happen unprompted?

---

# 8. Version History

| Version | Change |
| --- | --- |
| **17.3.0 Standard** | Email Verification and Email Unsubscribe introduced as REDCap+ features |
| **17.3.3 Standard** | **System Statistics** gained counters for the Email Verification/Unsubscribe features, shown when a REDCap+ subscription is active. See [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) |

No defects specific to these features appear in the Standard or LTS changelogs through 17.4.1.

> **Version caveat (LTS):** These features arrived in **17.3.0 Standard**. An LTS instance receives them only if its line was cut from a Standard release at or above that version — LTS 17.3.x qualifies, LTS 16.0.x does not and will not gain them through patching. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

---

# 9. Common Questions

**Q: Do participants have to verify their email address before we can email them?**

**A:** No. Verification is optional and REDCap sends to unverified addresses normally. It becomes meaningful only when you gate downstream alerts or ASIs on `[email-verified] = "1"`.

**Q: We enabled the feature but nothing changed. Is it broken?**

**A:** No — it is entirely opt-in. Enabling it makes the Smart Variables and dashboard page available; nothing happens until someone puts `[email-unsubscribe-link]` into an email or a flag variable into trigger logic.

**Q: A participant unsubscribed but alerts are still being scheduled for them. Is the block failing?**

**A:** No. Unsubscribing blocks the **send**, not the **schedule**. The emails are queued and then not sent: ASIs are logged as **Did not send** / **Participant opted out**, and alerts count as failed sends. To stop them being scheduled at all, add `[email-unsubscribed] = "0"` to the alert or ASI trigger logic.

**Q: Staff are CC'd on an alert to a participant who unsubscribed. Do staff still get it?**

**A:** Not if the participant is the only To recipient. The unsubscribed address is removed from To, CC and BCC, and if no To address is left the whole message is dropped, staff copies included. Send staff notifications as a separate alert addressed to staff.

**Q: Does unsubscribing stop text messages too?**

**A:** No. It applies to email only. SMS and voice invitations continue.

**Q: Does unsubscribing stop emails from all our projects?**

**A:** No, it applies to that one project only. A participant enrolled in several projects would need to unsubscribe from each.

**Q: Can a participant re-subscribe?**

**A:** Yes. The unsubscribe confirmation page offers an immediate re-subscribe link, and clicking the unsubscribe link again later opens a page with a link to re-subscribe. Study staff with access to the dashboard can also use **Undo** there.

**Q: How do we find out when someone unsubscribes?**

**A:** Create an alert whose trigger logic is only `[email-unsubscribed] = "1"`.

**Q: Who can see the Verified & Unsubscribed Emails page?**

**A:** Users with **Survey Distribution Tools** privileges or **Alerts & Notifications** privileges. It is not visible to all project users.

**Q: Can we turn this off for the whole instance?**

**A:** Yes, on the Modules/Services Configuration page. It is Enabled by default, so check whether projects are already relying on it first. Disabling hides the dashboard, makes all six Smart Variables pipe blank (so logic like `[email-unsubscribed] = "0"` or `[email-verified] = "1"` becomes false and gated alerts and ASIs stop), breaks the links already in participants' inboxes, and still keeps already-unsubscribed people blocked. See §3.1.

**Q: Why don't the Smart Variables appear in our Smart Variable documentation?**

**A:** Either the feature is disabled at system level, the instance is below 17.3.0, or the instance has no active REDCap+ subscription and you are not an administrator. Administrators always see them listed; other users see them only with an active subscription.

---

# 10. Common Mistakes & Gotchas

**Assuming unsubscribe prevents scheduling.** It prevents sending. Alerts and ASIs keep getting scheduled for unsubscribed participants; the queue looks normal until send time, when the ASI is logged as **Did not send** / **Participant opted out** and the alert counts as a failed send. Add `[email-unsubscribed] = "0"` to trigger logic.

**CC'ing staff on participant emails.** If every To address is unsubscribed, the whole message is dropped, CC and BCC copies included. Staff who rely on being copied will silently stop hearing about those participants.

**Forgetting that the status follows the address.** Records sharing one email address share one verified/unsubscribed status in the project.

**Adding an unsubscribe link without an unsubscribe policy.** Once a participant opts out, REDCap refuses every email from that project — including ones the study genuinely needs to send, such as safety or scheduling notices. Decide in advance which communications are participant-elective and whether an all-or-nothing opt-out is appropriate for the study.

**Collecting verification but never using it.** `[email-verify-link]` on its own records a status nobody acts on. The value comes from pairing it with `[email-verified] = "1"` in downstream trigger logic.

**Not anticipating that a participant click fires project logic.** Verifying or unsubscribing can trigger calculations, alerts and ASIs. The participant chooses the moment; the project must be designed to cope with it.

**Disabling the feature system-wide without auditing usage.** It is Enabled by default, so projects may already depend on it. Disabling makes the Smart Variables pipe blank, so flag-gated alerts and ASIs stop for everyone, while already-unsubscribed people stay blocked and can no longer use their links. Check dependent logic first.

**Expecting the opt-out to be instance-wide.** It is per project. A participant in several projects must unsubscribe from each.

**Assuming everyone on the study team can see the dashboard.** It requires Survey Distribution Tools or Alerts & Notifications privileges.

---

# 11. Related Articles

- [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md) — where the six Smart Variables sit in the wider set
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) — trigger logic, where the flag variables belong
- [RC-SURV-06 — Automated Survey Invitations](RC-SURV-06_Automated-Survey-Invitations.md) — ASIs are subject to the same schedule-versus-send distinction
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) — the system-level setting
- [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) — usage counters added in 17.3.3
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) — the two privileges that grant access to the dashboard page
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have these features
