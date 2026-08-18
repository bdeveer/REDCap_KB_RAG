

**REDCap+: Email Verification & Unsubscribe**

| **Article ID** | [RC-PLUS-05 — REDCap+: Email Verification & Unsubscribe](RC-PLUS-05_Email-Verification-and-Unsubscribe.md) |
| --- | --- |
| **Domain** | REDCap+ |
| **Applies To** | Study teams sending participant emails; REDCap Administrators (§3) |
| **Requires** | REDCap v17.3.0+ and a REDCap+ subscription |
| **Verified Against** | REDCap 17.3.6 (LTS) — the system-level setting (§3) verified against a live instance. The Smart Variables, dashboard page and participant-facing pages are from the 17.3.0 release notes and are not yet verified |
| **Prerequisite** | [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-08 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md); [RC-SURV-06 — Automated Survey Invitations](RC-SURV-06_Automated-Survey-Invitations.md); [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md); [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) |
| **Synonyms** | email unsubscribe redcap; let participants opt out of emails; verify participant email address; email-verify-link; email-unsubscribe-link; email-verified smart variable; stop sending emails to a participant; verified and unsubscribed emails page; opt out link in survey invitations |

---

> **Scope note.** The system-level setting in §3 is verified against a live instance running **17.3.6 LTS**. The Smart Variables, the project dashboard page and the participant-facing verify/unsubscribe pages are described from REDCap's **17.3.0** release notes and have not been verified — they require an active REDCap+ subscription to exist. See [RC-PLUS-01 §4a](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) on what is and is not observable without one.

---

## 1. Overview

Two related REDCap+ features, introduced together in **17.3.0**:

- **Email Verification** — a participant confirms that an email address they supplied actually reaches them.
- **Email Unsubscribe** — a participant opts out of all emails from a project.

Both work through a suite of four **Smart Variables** plus a project dashboard page. Both are **entirely opt-in**: enabling the feature at system level makes the Smart Variables and the dashboard *available*, but nothing changes in any project until a user deliberately puts one of the Smart Variables into an email, an alert, or trigger logic.

> **This is a build-it-yourself feature, not a switch.** REDCap does not add an unsubscribe link to your emails, and does not start verifying addresses, because you turned the feature on. It gives you the links and the flags; where they go and what they gate is your design decision. A project that never uses the Smart Variables behaves exactly as it did before.

The one thing REDCap *does* enforce on your behalf is the suppression itself — see §5.

---

## 2. The Four Smart Variables

| Smart Variable | Type | Purpose |
| --- | --- | --- |
| `[email-verify-link]` | Link | Generates a link the participant clicks to verify their email address |
| `[email-verified]` | Flag | `1` if the participant's address has been verified, `0` if not. For use in logic |
| `[email-unsubscribe-link]` | Link | Generates a link the participant clicks to unsubscribe from the project |
| `[email-unsubscribed]` | Flag | `1` if the participant has unsubscribed, `0` if not. For use in logic |

The two link variables accept custom link text — for example `[email-verify-link:Please click here]` renders as a link reading "Please click here".

The pattern is consistent: **a link variable to put in an email, and a flag variable to put in logic.** They are designed to be used as a pair.

Full definitions live in REDCap's own Smart Variables documentation, which is where the flags' exact behaviour in edge cases will be stated. See [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md).

---

## 3. System-Level Setting

*Verified against 17.3.6 LTS.*

**Where:** Control Center → **Modules/Services Configuration** → **Email Verification and Email Unsubscribe Features**, marked with a `REDCap+` badge and the note *"A REDCap+ subscription is required in order to use this feature."*

| Setting | Options | Default |
| --- | --- | --- |
| Email Verification and Email Unsubscribe Features | Disabled / **Enabled** | **Enabled** |

The on-page description: *"If enabled, a suite of Smart Variables and a dashboard page can be utilized by users in a project to allow participants to verify their email address or unsubscribe from all emails from the current project. If disabled, this feature and its Smart Variables will not be available to use in any project."*

**Disabling has two effects:**

1. The **Verified & Unsubscribed Emails** dashboard page is hidden from all projects.
2. All related Smart Variables are **hidden from the Smart Variable documentation**.

> **Critical — think before disabling this on an instance where projects already use it.** The feature is enabled by default, so studies may have built unsubscribe links and `[email-unsubscribed]` trigger logic without an administrator ever making a decision about it. Turning it off makes those Smart Variables unavailable, which affects live alert and ASI logic and the unsubscribe links already sitting in participants' inboxes. Audit usage before switching it off.

---

## 4. Email Verification

A participant's email address **does not** need to be verified for them to receive emails. Verification is good practice, not a precondition — REDCap will happily send to an unverified address.

The intended pattern uses the two verification Smart Variables together:

1. **Capture and prompt.** A public survey collects an email address. An alert triggered on completion contains `[email-verify-link:Please click here]` — for example: *"Thanks for taking the survey. [email-verify-link:Please click here] to verify your email address."*
2. **Gate downstream sends.** Later alerts and ASIs add `[email-verified] = "1"` to their trigger logic, so nothing is sent or scheduled until the participant has actually verified.

That second step is what makes verification worth doing. Without it, verification records a fact nobody acts on; with it, the project stops sending follow-ups into addresses that were mistyped or never belonged to the participant.

---

## 5. Email Unsubscribe

Place `[email-unsubscribe-link]` wherever you want the opt-out to appear — conventionally at the foot of outgoing emails.

### 5.1 What happens when a participant unsubscribes

**REDCap refuses to send them any email from that project.** This is enforced by REDCap, not by your logic: even if a user actively tries to email that participant from the project, the send is refused.

> **Scope of the block:** unsubscribing applies to **one project only**. A participant who is also enrolled in another project on the same instance continues to receive that project's emails. There is no instance-wide opt-out.

### 5.2 Re-subscribing

The participant can undo it themselves — clicking the unsubscribe link again opens a page offering a link to re-subscribe to the project.

### 5.3 The critical distinction: scheduling vs sending

> **Critical — unsubscribing blocks the send, not the schedule.** Alerts and ASIs will **still be scheduled** for an unsubscribed participant. The block happens later, at the moment REDCap is ready to send: the email is simply not sent.
>
> The consequence is that a project can accumulate a queue of scheduled emails for people who will never receive them. Nothing errors, and the schedule looks normal.
>
> To prevent scheduling in the first place, add `[email-unsubscribed] = "0"` to the trigger logic of your alerts and ASIs.

This is the single most important thing to understand about the feature. The safety net exists and works, but it operates one step later than most people assume, and relying on it alone leaves misleading state in the alert queue.

### 5.4 Getting notified of unsubscribes

REDCap's own suggested pattern: create an alert whose logic is **only** `[email-unsubscribed] = "1"`. It fires whenever a participant unsubscribes, which is a simple way to keep the study team informed of attrition.

---

## 6. The Verified & Unsubscribed Emails Page

Every project gains a dashboard page named **"Verified & Unsubscribed Emails"**, listing which email addresses in the project have been verified and which have unsubscribed.

**Access is restricted.** Only users with **Survey Distribution Tools** privileges *or* **Alerts & Notifications** privileges can view and manage the page. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md).

> **Note:** The page is hidden entirely when the feature is disabled at system level (§3).

---

## 7. Side Effects on Calculations, Alerts and ASIs

> **Critical — verifying or unsubscribing is a data event that can trigger things.** REDCap states this directly: the act of verifying or unsubscribing an email address **can trigger calculations, Automated Survey Invitations, and alerts** where the verify/unsubscribe Smart Variables appear in their logic.
>
> A participant clicking a link in their own time can therefore set off project logic — including sending them further emails, if an alert's condition happens to become true on verification. This is exactly what the intended `[email-verified] = "1"` gating pattern relies on, so it is by design; but it means the participant, not the study team, controls when that logic fires.

Worth thinking through before deploying: what becomes true the instant someone verifies, and is that what you want to happen unprompted?

---

## 8. Version History

| Version | Change |
| --- | --- |
| **17.3.0 Standard** | Email Verification and Email Unsubscribe introduced as REDCap+ features |
| **17.3.3 Standard** | **System Statistics** gained counters for the Email Verification/Unsubscribe features, shown when a REDCap+ subscription is active. See [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) |

No defects specific to these features appear in the Standard or LTS changelogs through 17.4.1.

> **Version caveat (LTS):** These features arrived in **17.3.0 Standard**. An LTS instance receives them only if its line was cut from a Standard release at or above that version — LTS 17.3.x qualifies, LTS 16.0.x does not and will not gain them through patching. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

---

## 9. Common Questions

**Q: Do participants have to verify their email address before we can email them?**

**A:** No. Verification is optional and REDCap sends to unverified addresses normally. It becomes meaningful only when you gate downstream alerts or ASIs on `[email-verified] = "1"`.

**Q: We enabled the feature but nothing changed. Is it broken?**

**A:** No — it is entirely opt-in. Enabling it makes the Smart Variables and dashboard page available; nothing happens until someone puts `[email-unsubscribe-link]` into an email or a flag variable into trigger logic.

**Q: A participant unsubscribed but alerts are still being scheduled for them. Is the block failing?**

**A:** No. Unsubscribing blocks the **send**, not the **schedule**. The emails are queued and then not sent. To stop them being scheduled at all, add `[email-unsubscribed] = "0"` to the alert or ASI trigger logic.

**Q: Does unsubscribing stop emails from all our projects?**

**A:** No, it applies to that one project only. A participant enrolled in several projects would need to unsubscribe from each.

**Q: Can a participant re-subscribe?**

**A:** Yes. Clicking the unsubscribe link again opens a page with a link to re-subscribe.

**Q: How do we find out when someone unsubscribes?**

**A:** Create an alert whose trigger logic is only `[email-unsubscribed] = "1"`.

**Q: Who can see the Verified & Unsubscribed Emails page?**

**A:** Users with **Survey Distribution Tools** privileges or **Alerts & Notifications** privileges. It is not visible to all project users.

**Q: Can we turn this off for the whole instance?**

**A:** Yes, on the Modules/Services Configuration page. It is Enabled by default, so check whether projects are already relying on it — disabling hides the dashboard and removes the Smart Variables from use everywhere.

**Q: Why don't the Smart Variables appear in our Smart Variable documentation?**

**A:** Either the feature is disabled at system level, which hides them from the documentation, or the instance has no REDCap+ subscription, or it is below 17.3.0.

---

## 10. Common Mistakes & Gotchas

**Assuming unsubscribe prevents scheduling.** It prevents sending. Alerts and ASIs keep getting scheduled for unsubscribed participants and then silently fail to send, leaving a queue that misrepresents what will actually happen. Add `[email-unsubscribed] = "0"` to trigger logic.

**Adding an unsubscribe link without an unsubscribe policy.** Once a participant opts out, REDCap refuses every email from that project — including ones the study genuinely needs to send, such as safety or scheduling notices. Decide in advance which communications are participant-elective and whether an all-or-nothing opt-out is appropriate for the study.

**Collecting verification but never using it.** `[email-verify-link]` on its own records a status nobody acts on. The value comes from pairing it with `[email-verified] = "1"` in downstream trigger logic.

**Not anticipating that a participant click fires project logic.** Verifying or unsubscribing can trigger calculations, alerts and ASIs. The participant chooses the moment; the project must be designed to cope with it.

**Disabling the feature system-wide without auditing usage.** It is Enabled by default, so projects may already depend on it. Disabling hides the dashboard and makes the Smart Variables unavailable, affecting live alert and ASI logic.

**Expecting the opt-out to be instance-wide.** It is per project. A participant in several projects must unsubscribe from each.

**Assuming everyone on the study team can see the dashboard.** It requires Survey Distribution Tools or Alerts & Notifications privileges.

---

## 11. Related Articles

- [RC-PIPE-03 — Smart Variables: Overview](RC-PIPE-03_Smart-Variables-Overview.md) — where the four Smart Variables sit in the wider set
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) — trigger logic, where the flag variables belong
- [RC-SURV-06 — Automated Survey Invitations](RC-SURV-06_Automated-Survey-Invitations.md) — ASIs are subject to the same schedule-versus-send distinction
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) — the system-level setting
- [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) — usage counters added in 17.3.3
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) — the two privileges that grant access to the dashboard page
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have these features
