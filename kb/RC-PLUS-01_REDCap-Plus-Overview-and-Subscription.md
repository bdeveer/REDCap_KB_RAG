RC-PLUS-01

**REDCap+: Overview and Subscription**

| **Article ID** | RC-PLUS-01 |
| --- | --- |
| **Domain** | REDCap+ |
| **Applies To** | REDCap Administrators; REDCap Licensed Institutions; REDCap v17.0.0+ |
| **Prerequisite** | Existing REDCap License (REDCap Core installation) |
| **Version** | 1.0 |
| **Last Updated** | 2026-04 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PLUS-02 — Project Migration Tool *(planned)*; RC-CC-01 — Control Center Overview |

---

> **⚠️ REDCap+ Feature Tag**
> Articles in this KB use the callout block above to flag features or behaviors that are **exclusive to REDCap+ subscribers**. If you see this tag, the described functionality requires a REDCap+ subscription and is not available in REDCap Core. See [Section 8](#8-tagging-convention-for-this-kb) for details on how this tagging is applied.

---

# 1. Overview

REDCap+ is an optional, paid subscription tier that unlocks advanced features on top of the standard REDCap platform (referred to as REDCap Core). It became available in April 2026 starting with REDCap v17.0.0.

REDCap Core remains fully free and fully functional for all licensed institutions, exactly as it always has been. REDCap+ is strictly additive — choosing not to subscribe has no effect on REDCap Core functionality, security updates, or access to incremental enhancements.

The purpose of REDCap+ is to sustain the long-term development of the platform. Revenue from REDCap+ subscriptions funds the development and testing of major new features, operational infrastructure (the REDCap Community portal, weekly consortium meetings, the External Module repository), and ongoing staffing. This model allows major innovations to continue without introducing a paywall for core functionality.

---

# 2. Key Concepts & Definitions

## REDCap Core

The REDCap system as it existed through v16. REDCap Core remains available at no cost and continues to receive weekly releases of incremental enhancements (new smart variables, action tags, survey settings), security patches, and bug fixes on both standard and long-term support schedules. All major new features going forward are REDCap+ exclusive.

## REDCap+

An ever-growing suite of advanced features and modules built on top of REDCap Core. REDCap+ is unlocked by entering a special subscription key in the REDCap Control Center. It is not a separate codebase — it is the same REDCap installation with additional capabilities enabled.

## REDCap License

The standard online license agreement signed by a non-profit organization to join the REDCap Consortium. The existing REDCap License is not modified by REDCap+. Institutions that sign the REDCap License are called REDCap Licensed Institutions.

## REDCap+ Subscriber

A REDCap Licensed Institution that has signed the REDCap+ Addendum and submitted payment for at least one installation.

## Institution vs. Installation

A REDCap Licensed Institution is the non-profit organization that holds the REDCap License. An installation (also called an instance) is a single REDCap server. One institution may operate multiple installations. REDCap+ is licensed per installation — subscribing for one installation does not cover others.

## Active Users (for pricing)

For REDCap+ pricing purposes, an active user is any user account that has logged into the REDCap installation in the past 6 months. API-only accounts are not counted unless the user logs in directly.

## REDCap Learning Lab

A separate, optional fee-based online certification program assessing REDCap proficiency. Learning Lab is not included in a REDCap+ subscription, though future REDCap+ features may integrate with it (e.g., gating project creation on certification status).

---

# 3. REDCap+ vs. REDCap Core: What Changes

| Aspect | REDCap Core | REDCap+ |
|---|---|---|
| Cost | Free | Annual subscription (tiered by active users) |
| Major new features | Not included | Included |
| Incremental enhancements (action tags, smart variables, survey settings) | Included | Included |
| Security patches and bug fixes | Included | Included |
| FDA 21 CFR Part 11 validation support | Included | Included |
| Minimum version required | Any supported version | v17.0.0+ |
| Requires a subscription key | No | Yes (entered in Control Center) |

Choosing REDCap+ does not grant access to enhanced or priority support. Administrator support via the REDCap Community Portal and weekly consortium webinars continues to be available to all institutions equally. REDCap+ does add up to 12 Community Portal seats per subscribing institution.

---

# 4. Initial REDCap+ Features (2026)

> **⚠️ REDCap+ Feature Tag**
> All features listed in this section are REDCap+ exclusive and require a REDCap+ subscription on the target installation.

The first REDCap+ features became available with v17.0.0 in April 2026. Additional features are being released iteratively throughout 2026.

## Project Migration Tool

A comprehensive tool to move one or more projects — including all settings and data — from one REDCap server to another. Key points:

- Only the **destination (target)** server requires a REDCap+ subscription. The source server can be a REDCap Core installation.
- This tool can be used to consolidate multiple REDCap installations into a single instance, reducing administrative overhead.
- See RC-PLUS-02 *(planned)* for procedural details.

## REDCap Rewards

Integrates the Tango Gift Card API with REDCap+ to support participant recruitment incentives in research studies. Includes supporting materials for institutional compliance conversations (Finance, Treasury, etc.).

## REDCap SHARE

Supports participant-driven sharing of their electronic health record (EHR) data directly with researchers.

## Additional Community Portal Seats

REDCap+ subscriptions include up to 12 administrator seats on the REDCap Community Portal (versus the default allocation for non-subscribers).

---

# 5. Pricing and Tiers

REDCap+ is priced annually based on the number of active user logins on the target installation in the preceding 6 months. Subscriptions begin the day payment is received and are valid for one calendar year.

| Tier | Active Logins (last 6 months) | Annual Price |
|---|---|---|
| Tier 1 | 1–100 | $950 |
| Tier 2 | 101–500 | $2,500 |
| Tier 3 | 501–2,000 | $9,000 |
| Tier 4 | 2,001+ | $17,000 |

**Additional pricing notes:**

- Pricing is per installation, not per institution. An institution with three production installations may subscribe to any, all, or none of them independently.
- Tier prices are locked for the duration of a subscription period but may change at renewal.
- No discounts are available. The tiered structure is designed to accommodate institutions of varying sizes and resources.
- Accepted payment methods include purchase orders, electronic funds transfers (EFT), ACH transfers, wire transfers, and credit cards. Checks are not accepted.
- Subscriptions are non-refundable.

---

# 6. How to Subscribe

Before accessing REDCap+, an institution must complete the following steps:

1. **Hold a valid REDCap License** — institutions must already be licensed REDCap Consortium members.
2. **Sign the REDCap+ Addendum** — a separate agreement specific to REDCap+. The existing REDCap License does not need to be re-executed.
3. **Report active user count** — submit the number of users who have logged in during the past 6 months for the target installation (REDCap Stats report).
4. **Submit payment** — pay the annual subscription fee for the applicable tier.
5. **Upgrade to REDCap v17.0.0 or higher** — REDCap+ features are only available on v17.0.0+.

Upon completing these steps, Vanderbilt generates a special license key. Enter this key in the REDCap Control Center to activate REDCap+ features on that installation.

To retain the subscription at renewal, institutions must again report active users and submit payment before the current subscription expires.

---

# 7. Technical Notes

## Same Codebase

REDCap+ is not a separate product or fork. It is the standard REDCap codebase with additional features unlocked by the subscription key. There is no separate installation process beyond upgrading to v17.0.0+.

## Test / Non-Production Servers

REDCap+ subscribers receive both a production and a non-production subscription key. There is no limit on the number of non-production (sandbox/test) REDCap+ installations a subscriber may run. Only the production installation key is subject to user metric reporting requirements.

## What Happens When a Subscription Expires

When the REDCap+ subscription key expires, all REDCap+ features are immediately deactivated for that installation — for both existing projects that used those features and any new projects. The installation reverts to REDCap Core. Data is not lost, but REDCap+-dependent workflows will stop functioning until the subscription is renewed.

## Per-Project Purchasing

REDCap+ cannot be purchased on a per-project basis for an existing installation. The subscription applies to the entire installation. The only exception is if an institution wants to create a dedicated new installation solely for one project and subscribe to REDCap+ for that installation.

---

# 8. Tagging Convention for This KB

Because REDCap+ is an additive, subscription-based tier, **any KB article describing a REDCap+ exclusive feature must include the following callout block at the top of the relevant section (or at the article level if the entire article covers a REDCap+ feature):**

```
> **⚠️ REDCap+ Feature Tag**
> [Description of what requires a REDCap+ subscription and why]
```

This tagging approach ensures that users who encounter a feature article know upfront whether it requires a paid subscription. Articles covering REDCap Core features that have no REDCap+ dependency do not need this tag.

As new REDCap+ features are documented (e.g., the Project Migration Tool, REDCap Rewards, REDCap SHARE), each article should open with this tag block and reference RC-PLUS-01 as the parent article for subscription context.

---

# 9. Common Questions

**Will REDCap Core continue to receive updates?**
Yes. REDCap Core continues to receive weekly releases covering incremental enhancements, security patches, and bug fixes on both standard and long-term support schedules. Only major new feature modules are exclusive to REDCap+.

**Will REDCap+ features eventually roll into REDCap Core?**
No. REDCap+ features are not planned for release in the freely available REDCap Core.

**Can an institution subscribe to REDCap+ for some installations but not others?**
Yes. Subscriptions are per installation. An institution with multiple REDCap installations can choose to subscribe to any, all, or none of them.

**Is there a way to test REDCap+ before committing to a production subscription?**
REDCap+ subscribers receive a non-production key for testing purposes. Organizations that have not yet subscribed would need to subscribe and upgrade to v17.0.0+ to access features.

**Does REDCap+ affect regulatory compliance (e.g., FDA 21 CFR Part 11)?**
REDCap Core's existing validation and documentation processes are maintained. There is no indication that REDCap+ subscription status affects the ability to validate REDCap for regulatory use.

**Are there any limitations on the types of projects supported on a REDCap+ installation?**
No. REDCap+ subscribers have full discretion over the types of research and operational projects supported on their installation.

---

# 10. Related Articles

- RC-PLUS-02 — Project Migration Tool *(planned)* (moving projects between REDCap installations)
- RC-CC-03 — Control Center: Security & Authentication Configuration (system-level admin configuration)
- RC-EM-01 — External Modules: Overview & Control Center Manager (analogous subscription-based add-on model for context)
