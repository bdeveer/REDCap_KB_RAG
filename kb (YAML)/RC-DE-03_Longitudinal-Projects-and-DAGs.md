---
id: RC-DE-03
title: Longitudinal Projects & Data Access Groups
domain: Data Entry
applies_to:
- REDCap projects with Longitudinal mode or Data Access Groups enabled
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-DE-01 — Record Creation & the Record Home Page
- RC-DE-02 — Basic Data Entry
version: '2.0'
last_updated: '2026-05-11'
related:
- id: RC-DE-09
  title: Data Entry with Data Access Groups
- id: RC-DE-10
  title: Longitudinal & Repeated Data Entry
- id: RC-NAV-REC-02
  title: Longitudinal Mode & Arms
- id: RC-NAV-REC-04
  title: Record Status Dashboard & Other Record Links
- id: RC-DAG-01
  title: Data Access Groups
tags:
- data entry
synonyms:
- how does data entry work in a longitudinal project
- data entry with events and arms
- how do data access groups change data entry
- overview of longitudinal and dag data entry
- which article covers longitudinal data entry
- entering data across multiple events
- data entry differences with dags enabled
- longitudinal versus standard data entry
---

> **Navigation article.** This article orients you to two features that change the data entry experience — Longitudinal mode and Data Access Groups — and points you to the dedicated articles for each. If you already know which feature you need, jump straight to the relevant article below.

---

# 1. Overview

Two optional project features significantly affect how data entry works in REDCap:

**Longitudinal mode** allows the same instrument to be reused across multiple timepoints (events) within a record. The Record Home Page changes from a simple list to a grid where rows are instruments and columns are events. Each cell in the grid is an independent data entry. → Full coverage: **[RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md)**

**Data Access Groups (DAGs)** partition records into named subsets — typically one per study site or department. When DAGs are enabled, you can only see and create records within your own group. Records from other DAGs are invisible to you. → Full coverage: **[RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md)

These features are independent — a project can use one, both, or neither. When both are active, longitudinal mode changes the record layout while DAGs filter which records you can see. They do not interfere with each other.

---

# 2. Where to Go from Here

| I need to… | Go to… |
| --- | --- |
| Understand the grid layout, events, and arms in a longitudinal project | [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md) |
| Understand repeated instruments or repeated events | [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md) |
| Understand why I can only see certain records | [RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md)|
| Switch between DAGs (DAG Switcher) | [RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md)|
| Understand how arms and events are structured | [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) |
| Understand how DAGs are set up and managed | [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) |

---

# 3. Related Articles

- [RC-DE-09 — Data Entry with Data Access Groups](RC-DE-09_Data-Entry-with-DAGs.md)
- [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md)
- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md)
- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md)
- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md)
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md)
