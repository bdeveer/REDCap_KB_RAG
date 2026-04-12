RC-UNCLASSIFIED-01

**Unclassified: REDCap FAQ v16.1.3 Orphaned Topics**

| **Article ID** | RC-UNCLASSIFIED-01 |
|---|---|
| **Domain** | Multiple (see sections below) |
| **Applies To** | All REDCap projects |
| **Prerequisite** | None |
| **Version** | 1.2 |
| **Last Updated** | 2026-04-11 |
| **Author** | REDCap Support (sourced from FAQ v16.1.3) |
| **Related Topics** | See per-section references below |

> **Note to KB maintainers:** This article is a holding area for content from the REDCap 16.1.3 FAQ that maps to topics not yet covered by a dedicated KB article. Sections 1–2 (Project Lifecycle / Making Production Changes), 4 (API / Data Entry Trigger), 5 (Multi-Language Management), and 6 (MyCap) have been removed — those topics are now covered by dedicated articles. Only Section 3 (Data Quality Module) remains as active interim content, pending the creation of RC-DQ-01.

---

# 3. Data Quality Module

## 3.1 What It Does

The Data Quality module allows project users to find discrepancies in data. It provides a set of built-in default rules (including Rule H for calculated field corrections) and allows users to write custom rules. Rules use the same logic syntax as branching logic.

## 3.2 Custom Rules

Custom rules must evaluate to TRUE or FALSE — not to a value. They can include mathematical operations and any of the Special Functions listed in RC-CALC-01. Custom rules use the same syntax as branching logic.

## 3.3 Real-Time Execution

Each custom rule has a "Real Time Execution" checkbox. When enabled, the rule runs automatically every time a user saves a data entry form. If a discrepancy is found, a popup notifies the user. Real-time execution works only on data entry forms — it is **not** available for surveys.

## 3.4 Running Rules Manually

Running a rule manually evaluates all records in the project and shows the number of records matching the rule's criteria. Clicking "view" shows the specific records and instance numbers (for repeating instruments).

## 3.5 Rule H — Correcting Calculated Fields

Rule H finds calculated fields whose stored values differ from their computed values (which can occur after design changes or data imports). Running Rule H displays a button to auto-correct all such values across the entire project. This is the recommended way to fix calculated fields after modifying their equations or after a data import that affected dependent fields.

## 3.6 Data Quality vs. Branching Logic

A Data Quality custom rule must always evaluate to TRUE or FALSE. A calculated field must always result in a number. Branching logic can use similar syntax to both, but each context has distinct constraints.

---

# 7. Suggested New KB Articles

Based on the remaining content and other FAQ topics not yet covered by dedicated articles, the following new articles are recommended:

| Suggested Article ID | Proposed Title | Source Content |
|---|---|---|
| ~~RC-PROJ-01~~ | ~~Project Lifecycle: Setup, Status, and Settings~~ | *Resolved — see RC-PROJ-01 — Project Lifecycle: Status and Settings* |
| RC-DQ-01 | Data Quality Module | Section 3 above; FAQ "Data Quality Module" and "Functions for Logic in Reports" sections |
| ~~RC-API-01~~ | ~~API and Data Entry Trigger~~ | *Resolved — see RC-API-01 — REDCap API and RC-INTG-01 — Data Entry Trigger* |
| ~~RC-MLM-01~~ | ~~Multi-Language Management (MLM)~~ | *Resolved — see RC-MLM-01 — Multi-Language Management* |
| ~~RC-MYCAP-01~~ | ~~MyCap: Setup and Management~~ | *Resolved — see RC-MYCAP-01 through RC-MYCAP-08 (MyCap series)* |
| RC-DDE-01 | Double Data Entry | FAQ "Double Data Entry" section (merging records, reviewer role, exporting merged records) |
| RC-PROJ-02 | Project Dashboards | FAQ "What is a project dashboard?" section (smart charts, tables, public dashboards, wizard) |

---

# 8. Related Articles

- RC-CALC-01 — Special Functions Reference (functions used in Data Quality rules)
- RC-BL-01 — Branching Logic: Overview & Scope (Data Quality custom rules use the same syntax)
- RC-PROJ-01 — Project Lifecycle: Status and Settings
- RC-MLM-01 — Multi-Language Management
- RC-MYCAP-01 — MyCap: Overview & Enabling
- RC-API-01 — REDCap API
- RC-INTG-01 — Data Entry Trigger
