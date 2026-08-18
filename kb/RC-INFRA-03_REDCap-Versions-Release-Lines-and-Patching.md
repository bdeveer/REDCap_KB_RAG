

**REDCap Versions, Release Lines & Patching**

| **Article ID** | [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) |
| --- | --- |
| **Domain** | Self-Hosting, Deployment & Release Management |
| **Applies To** | All REDCap users; REDCap Administrators (Sections 5–7) |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026-08 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-INFRA-01 — Self-Hosting a Private REDCap Instance](RC-INFRA-01_Self-Hosting-a-Private-REDCap-Instance.md); [RC-INFRA-02 — Self-Hosting REDCap on a Synology NAS with Docker Compose](RC-INFRA-02_Self-Hosting-REDCap-on-Synology-Docker.md); [RC-API-44 — Export REDCap Version API](RC-API-44_Export-REDCap-Version.md); [RC-CC-23 — Backup Options](RC-CC-23_Backup-Options.md); [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) |
| **Synonyms** | what redcap version am i running; difference between redcap lts and standard; should we use lts or standard redcap; how often is redcap released; what does long term support mean in redcap; why is our redcap version number lower than another site; how to read the redcap changelog; how do i know if my redcap needs patching; what redcap version introduced this feature; redcap release schedule and upgrade cadence |

---

## 1. Overview

REDCap is not distributed as a single stream of releases. It is published on **two parallel release lines** — Standard and Long Term Support (LTS) — that carry different version numbers, ship on different schedules, and are aimed at institutions with different priorities. An instance running "REDCap 17.3.7" and one running "REDCap 17.4.1" may have received the same security patch on the same day, despite the different numbers.

This article explains what the two lines are, how to read a REDCap version number, how to find the version your instance is running, how to read the official changelog, and why keeping current is the main risk control an institution actually has. It does not cover the mechanics of performing an upgrade — see `RC-INFRA-01 — Self-Hosting a Private REDCap Instance` for that.

Understanding this matters even if you never touch a server. Every KB article carries a `Requires` and a `Verified Against` version, colleagues at other institutions will quote version numbers that look older or newer than yours, and the answer to "why does that feature not appear in my REDCap?" is very often the release line rather than a configuration setting.

---

## 2. Key Concepts & Definitions

### Release line

One of the two parallel streams in which REDCap is published. Every REDCap installation follows exactly one line at a time. The two lines are **Standard** and **LTS**. Moving between them is a deliberate administrative decision, not something that happens automatically.

### Standard release

The line that receives **new features, improvements, changes, bug fixes and security fixes**. It is the line where everything appears first. Institutions that want current functionality and can absorb frequent change run Standard.

### LTS (Long Term Support) release

A line **branched from a specific Standard release** and thereafter maintained with **fixes only** — bug fixes and security fixes, no new features. The functional surface of an LTS line is frozen at the moment it was cut. Institutions that prioritise stability, or that operate under validation and regulatory obligations, run LTS.

### Branch point

The Standard release an LTS line was cut from. For example, LTS 17.3.5 was branched from Standard 17.3.4 on 2026-07-30. The LTS line inherits that release's feature set permanently and then diverges only in its patch number.

### Version number

Three dot-separated integers, `MAJOR.MINOR.PATCH` — e.g. `17.4.1`. What each position signifies differs between the two lines; see Section 3.

### Patch release

An incremental release within an existing line that raises only the third number. On the LTS line, essentially every release after the branch point is a patch release.

### Changelog

The official cumulative record of every change in every release. Published separately for each line, and the authoritative source for what a given version contains. See Section 6.

### Severity label

The classification the changelog assigns to each entry — `New Feature`, `Improvement`, `Change`, `Bug fix`, `Major bug fix`, and four grades of security fix (`Minor`, `Medium`, `Major`, `Critical`). These labels are how you triage whether a release needs to be applied urgently.

---

## 3. How the two release lines differ

| | **Standard** | **LTS** |
|---|---|---|
| New features | Yes | No — frozen at the branch point |
| Bug fixes | Yes | Yes |
| Security fixes | Yes | Yes, in parallel with Standard |
| New line cut | Continuous | Roughly every 6 months |
| Typical release interval | About weekly | About weekly |
| Functional change between releases | Expected | Minimal by design |
| Suited to | Teams wanting current features | Regulated, validated or change-averse environments |

The essential trade is **features versus stability**, and it is a real trade rather than a tiering: LTS is not a lesser product, and Standard is not less safe. Both lines receive the same security fixes, typically on the same day.

### 3.1 Release cadence

Both lines release frequently — the median gap between consecutive releases on either line is **7 days**. An institution on either line should expect to see a new version available most weeks. The great majority of those releases are fixes, not functional change.

A new LTS line is cut roughly **every six months**, historically at the end of January and the end of July. Recent branch points:

| LTS line begins | Date | Branched from |
|---|---|---|
| 15.0.9 | 2025-01-30 | Standard 15.0.8 |
| 15.5.7 | 2025-07-31 | Standard 15.5.6 |
| 16.0.10 | 2026-01-29 | Standard 16.0.9 |
| 17.3.5 | 2026-07-30 | Standard 17.3.4 |

### 3.2 Version numbers are not comparable across lines

This is the single most common source of confusion, and the reason every version reference in this KB names its line.

An LTS line **keeps the version prefix of the Standard release it was branched from** and then increments only the patch number. So LTS 16.0.10 through 16.0.47 all carry the `16.0` prefix inherited from Standard 16.0.9 — even though, by the time 16.0.47 shipped, Standard had moved on to 17.4.1.

The consequence: a *lower* version number does not mean a *less current* instance.

> **Important:** On 2026-08-13, three releases shipped on the same day — Standard **17.4.1**, LTS **17.3.7**, and LTS **16.0.47**. All three contained the same security fix. Their version numbers differ by more than a full major version, but none of them was behind on patches. Always ask which line a version belongs to before concluding anything about how current it is.

### 3.3 Two LTS lines are supported at once

When a new LTS line is cut, the previous one does not stop immediately. There is an overlap of several months during which both receive fixes, giving institutions a window to plan and test their move rather than being forced onto the new line on cut day.

Observed lifespans of recent LTS lines:

| LTS line | Releases | Active from | Through |
|---|---|---|---|
| 15.0.x | 32 | 2025-01-30 | 2025-10-29 |
| 15.5.x | 34 | 2025-07-31 | 2026-04-23 |
| 16.0.x | 38 | 2026-01-29 | 2026-08-13 |
| 17.3.x | 3 | 2026-07-30 | *(current)* |

Each line runs roughly nine months in practice — about six months as the current LTS, then a further overlap period after its successor is cut.

> **Note:** These lifespans are observed from the published changelogs, not a stated guarantee. Confirm the supported window for your line before planning around it.

---

## 4. Finding the version you are running

| Method | Where | Who can use it |
|---|---|---|
| Page footer | Bottom of any REDCap page — displays the version number | All users |
| Control Center home | The main Control Center page states the current version and, if Easy Upgrade is available, whether newer versions exist | Administrators |
| API | The **Export REDCap Version** method returns the version string — see `RC-API-44 — Export REDCap Version API` | Any user with an API token |

The footer and API return a bare version number without naming the line. To determine your line, compare against the branch points in Section 3.1, or check whether your instance receives new features between releases — if the feature set never changes, you are on LTS.

---

## 5. Choosing a line

The decision belongs to whoever owns the institutional instance, and it is normally made once and revisited rarely.

**Reasons to run LTS:**

- The instance supports research under regulatory obligations where a changing feature set creates validation burden — 21 CFR Part 11 environments are the usual case.
- Local validation, SOP or training material must be re-checked whenever behaviour changes, making frequent functional change genuinely expensive.
- Support staff need the UI to stay put so documentation and training remain accurate.

**Reasons to run Standard:**

- Users need features soon after release rather than up to six months later.
- The institution wants access to newly introduced capability without waiting for the next branch point.
- There is no validation regime that makes functional change costly.

> **Important:** The choice affects how long you wait for a feature, not whether you receive security fixes. Both lines are patched in parallel. Choosing LTS is not a decision to be less current on security, and choosing Standard does not mean accepting unpatched risk.

> **Institution-specific:** *[Record here which line this institution's production, test and development instances run, who owns the upgrade decision, and the expected lag between a release being published and being applied locally. Leave blank until confirmed with the local REDCap administration team.]*

---

## 6. Reading the changelog

The changelog is the authoritative record of what a version contains, published separately for each line. Every entry carries a **release date**, a **version**, a **type** and a **severity label**, followed by a description.

### 6.1 Entry types

| Type | Meaning | Documentation impact |
|---|---|---|
| `New Feature` | Capability that did not previously exist | High — may need new documentation |
| `Improvement` | Existing capability made better | Moderate — often changes described behaviour |
| `Change` | Behaviour deliberately altered | Moderate to high — can invalidate existing guidance |
| `Bug fix` | Defect repaired | Usually none |
| `Major bug fix` | Defect with significant impact repaired | Sometimes high — may define a window when documented behaviour did not hold |

### 6.2 Security severity grades

| Grade | Typical response |
|---|---|
| `Critical security fix` | Apply as soon as practical. Historically these have included Remote Code Execution issues. |
| `Major security fix` | Apply promptly. |
| `Medium security fix` | Apply in the normal cycle. |
| `Minor security fix` | Apply in the normal cycle. |

### 6.3 Provenance statements

Some entries state when a defect was introduced — *"Bug emerged in REDCap 17.2.0"* or *"Bug exists in REDCap 15.0.0 and higher."* These are the most useful sentences in the changelog. They let you determine whether **your** instance was ever affected, and therefore whether you need to go back and check your own data.

> **Note:** Where an entry gives no provenance, the fix version tells you only when the defect was repaired — never when it started. Do not infer an affected range from a fix version alone.

---

## 7. Patching practice

Running an unpatched instance is the largest controllable risk an institution carries with REDCap, and it compounds silently.

- **Security fixes ship in most releases, on both lines simultaneously.** Staying near the head of your line is the single most effective control available.
- **Most vulnerabilities require an authenticated user.** This is not reassurance. In a typical REDCap instance, the authenticated population is large — every study team member across every project. A handful of issues have been exploitable by unauthenticated survey participants.
- **Remove old version directories from the server.** REDCap has explicitly flagged that leaving prior version directories in place keeps known vulnerabilities reachable. On newer versions, calls to survey and API endpoints containing a version directory in the URL are refused outright.
- **Check upgrade prerequisites before planning a jump.** Minimum PHP version and database charset requirements have both changed, and either can block an upgrade — see `RC-INFRA-01 — Self-Hosting a Private REDCap Instance`.
- **Read the changelog between your version and your target**, not just the target's entry. A multi-version jump accumulates changes, and provenance statements in intermediate releases may tell you to go re-check data.

> **Important:** Because LTS lines carry an older version prefix, an LTS instance can look alarmingly out of date to someone who does not know the release model. Judge currency by how far behind the head of your own line you are — not by comparing against a Standard version number.

---

## 8. Common Questions

**Q: What REDCap version am I running?**

**A:** Look at the footer of any REDCap page. Administrators can also see it on the Control Center home page, and any user with an API token can call the Export REDCap Version method — see `RC-API-44 — Export REDCap Version API`. Note that none of these tell you which release line you are on; compare against the branch points in Section 3.1 to work that out.

**Q: What is the difference between REDCap LTS and Standard?**

**A:** Standard receives new features, improvements, changes and fixes. LTS is branched from a Standard release and then receives fixes only — its feature set is frozen at the branch point. Both receive security fixes in parallel, usually on the same day. A new LTS line is cut roughly every six months.

**Q: Our REDCap is on 16.0.47 and another institution is on 17.4.1. Are we badly out of date?**

**A:** Not necessarily. Those two versions shipped on the same day and contained the same security fix. 16.0.47 is an LTS release; 17.4.1 is Standard. You have fewer features, but you are not behind on patches. What matters is the gap between your version and the head of *your own* line.

**Q: Why can't I find a feature that the documentation describes?**

**A:** Three likely reasons, in order. First, you may be on an LTS line branched before the feature existed — check the article's `Requires` field against your version. Second, the feature may require a REDCap+ subscription — see `RC-PLUS-01 — REDCap+: Overview and Subscription`. Third, it may be disabled at the system level by your administrators.

**Q: Should we switch from Standard to LTS, or the other way around?**

**A:** It depends on whether functional change is expensive for you. If you operate under validation or regulatory obligations where every behaviour change triggers re-validation, LTS is designed for exactly that. If your users need features promptly and you have no validation regime, Standard suits better. It is not a decision about security — both lines are patched in parallel.

**Q: How often do we need to upgrade?**

**A:** Releases appear on both lines roughly weekly, but few institutions apply every one. A common approach is to apply security releases promptly according to their severity grade and batch the rest into a regular maintenance window. What you should avoid is falling far enough behind that a future upgrade becomes a large, risky jump across accumulated prerequisites.

**Q: How do I tell whether a bug ever affected our data?**

**A:** Look for a provenance statement in the changelog entry — "Bug emerged in REDCap X" or "Bug exists in REDCap X and higher." Compare that range against the versions your instance has actually run. If your instance was never on an affected version, no action is needed. If it was, the entry description usually indicates what to re-check.

---

## 9. Common Mistakes & Gotchas

**Comparing version numbers across release lines.** Treating 16.0.47 as older than 17.0.0 because the number is lower. The two lines number independently, and an LTS release can ship the same day as a Standard release with a much higher number. Always establish which line a version belongs to before drawing any conclusion about currency. When quoting a version anywhere — a ticket, an email, a KB article — name the line alongside it.

**Assuming LTS means "not patched as often."** LTS receives security fixes in parallel with Standard, typically on the same day. What LTS withholds is new features, not fixes. Institutions sometimes move off LTS for the wrong reason, believing they are improving their security posture when they are only accepting more functional churn.

**Inferring when a bug started from the version that fixed it.** A fix in 17.1.2 does not mean the defect appeared in 17.1.1 — it may have existed for years. Only an explicit provenance statement establishes the affected range. Guessing produces false confidence in exactly the situation where you most need accuracy: deciding whether your own data was affected.

**Letting the gap to the head of your line grow.** Skipping releases is normal; skipping them indefinitely is not. Upgrade prerequisites accumulate — minimum PHP versions and database charset requirements have both changed — so a long-deferred upgrade becomes a multi-step project rather than a maintenance task. Deferring also means every intermediate security fix remains unapplied.

**Leaving old version directories on the server after upgrading.** The upgrade succeeds and the instance works, so the old directories are easy to forget. They remain reachable and carry the vulnerabilities that were fixed by upgrading, which substantially undoes the benefit of having upgraded.

---

## 10. Related Articles

- [RC-INFRA-01 — Self-Hosting a Private REDCap Instance for Development, Testing & Validation](RC-INFRA-01_Self-Hosting-a-Private-REDCap-Instance.md) — install and upgrade mechanics, PHP and database prerequisites
- [RC-INFRA-02 — Self-Hosting REDCap on a Synology NAS with Docker Compose](RC-INFRA-02_Self-Hosting-REDCap-on-Synology-Docker.md) — platform-specific deployment, including known-bad install versions
- [RC-API-44 — Export REDCap Version API](RC-API-44_Export-REDCap-Version.md) — retrieving the version programmatically
- [RC-CC-23 — Backup Options](RC-CC-23_Backup-Options.md) — what to secure before an upgrade
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — features gated by subscription rather than by version
- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) — system-level settings referenced when checking version and upgrade status
