---
id: RC-EXPRT-07
title: 'Custom Reports: Filtering & Ordering'
domain: Exports, Reports & Stats
applies_to:
- All project types
- longitudinal-specific features noted inline
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — report
  filtering, live filter and ordering behaviour checked against source code; pages
  not re-captured
prerequisites:
- 'RC-EXPRT-06 — Custom Reports: Setup & Field Selection'
version: '1.1'
last_updated: 2026-11
related:
- id: RC-EXPRT-06
  title: 'Custom Reports: Setup & Field Selection'
- id: RC-EXPRT-08
  title: 'Custom Reports: Management & Organization'
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
- id: RC-BL-02
  title: 'Branching Logic: Syntax & Atomic Statements'
- id: RC-BL-03
  title: 'Branching Logic: Combining Statements'
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-LONG-01
  title: Longitudinal Project Setup
tags:
- exports, reports & stats
- data
synonyms:
- how to filter a custom report
- add filter logic to a report
- show only records matching a condition in a report
- sort report results
- order report by field
- report builder step 3 and 4
- limit report to certain events or records
- filter report by branching logic conditions
---

# 1. Overview

This article covers Step 3 (filters) and Step 4 (result ordering) of the REDCap custom report builder. Filters control which records appear in a report; ordering controls the sequence in which results are displayed. Both steps are entirely optional — a report with no filters returns all records in the project, ordered by record ID (and then by event, in longitudinal projects) by default. This is the second article in the Custom Reports series; it assumes familiarity with report creation and field selection covered in [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md).

---

# 2. Key Concepts & Definitions

**Filter**
A condition that a record must satisfy to appear in a report. Filters are evaluated per record (and optionally per event in longitudinal projects). Records that do not meet the filter condition are excluded from the report.

**Logic Builder**
The default filter interface. A point-and-click tool for constructing filter conditions using AND and OR statements, without writing logic syntax manually. Supports single and combined logical statements, and event-specific filtering in longitudinal projects.

**Advanced Logic**
An alternative filter mode that accepts raw branching logic syntax — the same syntax used for branching logic on instruments. Supports all functions (e.g., `datediff`, `sum`, `ends_with`) and smart variables. Mutually exclusive with the Logic Builder within a single filter.

**Live Filter**
A variable designated as a real-time, on-the-fly filter for a saved report. Users can apply or change a live filter directly from the report view without editing the report. Up to three live filters can be set per report.

**Event Filter**
A filter available in longitudinal projects that limits report results to records with data in specific events. Configured in the Additional Filters section of Step 3.

**DAG Filter**
A filter that limits report results to records belonging to specific Data Access Groups. Available when DAGs are configured in the project.

**Show Data for All Events**
A checkbox in Step 3 (longitudinal projects, and classic projects that use repeating instruments) that controls whether filters are applied per event/instance or only at the record level. Checked by default.

---

# 3. Step 3: Filters

Filters are configured in Step 3 of the report builder. If you do not configure any filters, the report returns all records in the project.

## 3.1 Show Data for All Events (Longitudinal and Repeating Projects)

In longitudinal projects, the first option in Step 3 is **Show data for all events for each record returned**, which is checked by default. Classic projects that use repeating instruments show the same option (its label refers to repeating instances rather than events); it works the same way.

| Setting | Behavior |
|---|---|
| Checked (default) | If a record matches the filter condition at any point, the report displays all events for which the selected fields are defined. |
| Unchecked | The filter is applied to each event and repeated instrument independently. Only event/instance combinations that satisfy the filter are returned. |

The unchecked setting is an advanced option and requires careful testing. For most reports, leaving this checked is correct.

> **Note:** This option appears only in longitudinal projects and in projects that use repeating instruments or events. A classic project without repeating instruments does not show it.

## 3.2 Logic Builder

The Logic Builder is the default filter interface. It constructs filter conditions through dropdown selections rather than manual syntax entry.

**Building a filter condition:**

1. Select a variable using the look-up box or the dropdown (same two methods as Step 2 field selection).
2. In longitudinal projects, optionally select a specific event. The default is "All events."
3. REDCap adjusts the operator and value options to match the selected variable's field type:
   - Dropdown/radio/yes-no: operators are `=` and `not =`; values are the field's defined options.
   - Checkbox: choose an option, then **is checked** or **is not checked**.
   - Text/notes: operators include `=`, `≠`, `contains`, `does not contain`, `starts with`, `ends with`; value is a free-text box.
   - Calculated/number fields: operators include `=`, `≠`, `<`, `>`, `≤`, `≥`.
4. After completing one clause, select **AND** or **OR** from the row below to define the relationship to the next clause. AND requires both conditions to be true; OR requires at least one.
5. Repeat for each additional clause. Remove any clause using the red X at the end of its row. You can use the same variable in as many rows as you need.

**Filtering on blank values:** to find records where a variable is blank, leave the value box empty. To find records where it has any value, set the operator to `not =` and leave the value box empty.

**How AND and OR are grouped:** the Logic Builder does not evaluate rows strictly left to right. Consecutive rows joined by OR are grouped together first, and those groups are then joined with AND. For example, four rows entered as `A OR B AND C OR D` are evaluated as `(A OR B) AND (C OR D)`. If you need any other grouping, such as `A OR (B AND C)`, switch to Advanced Logic and write the parentheses explicitly. Clicking **Use Advanced Logic** shows the grouping REDCap applied, which is a quick way to check.

> **Note:** The Logic Builder supports combined AND/OR statements, unlike the drag-and-drop branching logic builder in the Online Designer, which accepts only one type of connector per rule set. The Logic Builder also accounts for event context in longitudinal projects.

**Converting to Advanced Logic:** Click **Use Advanced Logic** (next to "Switch Format") at any point to see the branching logic equivalent of your current Logic Builder selections. This is a useful learning tool for understanding how the Logic Builder translates to syntax.

## 3.3 Advanced Logic

Click **Use Advanced Logic** to switch the filter to a free-text syntax box. This mode accepts any valid REDCap branching logic syntax, including special functions and smart variables. Smart variables are resolved for each record, event and instance, and for the user viewing the report.

REDCap checks the logic for syntax errors and unknown variables before the report can be saved. A filter can reference up to roughly 900 fields; very large filters should be simplified or split across reports.

The logic must resolve to true or false for each record (or event, if "Show data for all events" is unchecked). Records where the logic resolves to true are included in the report.

**Example: Records where a sum of variables exceeds a threshold**
```
sum([var1],[var2],[var3]) > 2
```

**Example: Records enrolled within the last 7 days**
```
datediff([enroll_date],'today','d') <= 7
```

**Example: Records with a specific email domain**
```
ends_with([email],"@institution.edu")
```

> **Important:** It is possible to write logic that is always true or always false (e.g., comparing a field to an impossible value). Always test a new advanced filter against known records before using the report in production.

> **Note:** Switching back from Advanced Logic to the Logic Builder will prompt you to erase your advanced logic, because the Logic Builder cannot represent all advanced syntax. Do not switch back unless you intend to discard the advanced filter.

## 3.4 Additional Filters: Event and DAG

Below the main logic filter, the Additional Filters section provides dropdown selections for event-based and DAG-based filtering. These are independent of the logic filter.

**Event filter** (longitudinal projects only): Select one or more events. The report shows only rows for the selected events. The logic filter is still evaluated against the record's data in all events, so a condition on a variable collected at another event can still include or exclude a record.

**DAG filter** (if DAGs are configured): Select one or more DAGs. Only records belonging to the selected DAGs will be returned. Your own user rights still apply: a user assigned to a DAG only ever sees their own DAG's records, so if the report's DAG filter excludes that user's DAG, the report is empty for them.

When both an event filter and a DAG filter are active, a record must satisfy both conditions to appear in the report.

---

# 4. Live Filters

Live filters allow users to narrow a report's results on the fly from the report view page, without editing the report. You can designate up to three variables as live filters per report.

Live filters are most useful when a single report needs to serve multiple subgroups. For example, a class registration report with "Class" as a live filter can display all classes from one report, rather than requiring a separate report per class.

Only certain variables are eligible for live filters: the Record ID field, single-answer multiple-choice fields (dropdown, radio, yes/no, true/false), events (longitudinal projects), and DAGs. Checkbox fields cannot be used as live filters. REDCap automatically populates the live filter selection with eligible variables when you set up this section.

On the report page, each live filter offers the variable's options plus a **(blank value)** choice for records with no value.

- **Event live filter:** choosing an event shows that event's data, even if the report's own event filter is set to other events. Data is still limited by your user rights.
- **DAG live filter:** disabled for users who are assigned to a DAG, since they can only see their own DAG's records anyway.
- **Field live filters:** disabled for a user who does not have view rights to the instrument containing that field.

> **Note:** Live filter selections are not saved with the report. They are kept in the page URL, so a bookmarked or shared link to the report reopens it with the same live filter selections. Opening the report from the report list starts unfiltered.

> **Note:** If you export data from a report page while live filters are applied, REDCap asks whether to apply the live filters to the export. Exports through the API never apply live filters; they use only the filters saved in the report.

---

# 5. Step 4: Ordering Results

Step 4 controls the sort order of report results. By default, results are ordered by record ID in ascending order.

To specify a custom order:

1. Select up to three variables (**First by**, **Then by**, **Then by**) using the look-up or dropdown method. Checkbox fields cannot be used as sort fields.
2. For each variable, choose **Ascending** or **Descending** order.
3. When multiple sort variables are selected, REDCap sorts by the first variable, then by the second within ties, then by the third within remaining ties.

**Example:** Order by `gender` (ascending), then by `last_name` (ascending), then by `date_of_birth` (ascending) to produce an alphabetical list grouped by gender.

> **Note:** On the report page you can also click a column header to sort. This sorts only the page currently displayed (reports show up to 1,000 rows per page), not the whole report. For a sort that applies to all results and to exports, set it in Step 4.

---

# 6. Common Questions

**Q: Do I have to set up filters to create a report?**
**A:** No. Filters are entirely optional. A report with no filters displays all records in the project for the selected fields.

**Q: What is the difference between the Logic Builder and Advanced Logic?**
**A:** The Logic Builder is a point-and-click interface that constructs filter logic through dropdowns. Advanced Logic is a free-text syntax box accepting the same branching logic syntax used elsewhere in REDCap. Advanced Logic supports functions (`datediff`, `sum`, `ends_with`, etc.) and smart variables, which the Logic Builder does not support. Use Advanced Logic when you need anything beyond simple comparisons.

**Q: Can I use the same logic syntax I use for branching logic in a report filter?**
**A:** Yes, with one important difference in scope: branching logic hides or shows individual fields on an instrument; report filter logic includes or excludes entire records (or events, if the per-event setting is enabled). The syntax, functions, and smart variables are otherwise identical.

**Q: What does a live filter do that a regular filter does not?**
**A:** A regular filter is fixed — it applies the same condition every time the report is run. A live filter lets users change the filter value directly from the report view page without opening the report editor. Live filters are ideal when the same report needs to be sliced by different values of the same variable.

**Q: If I set both an event filter and a DAG filter in Additional Filters, how does REDCap combine them?**
**A:** With AND logic. A record must belong to a selected DAG AND have data in a selected event to appear in the report. There is no option to combine them with OR logic.

**Q: Can I write advanced logic that references smart variables like [user-dag-name]?**
**A:** Yes. Smart variables are supported in report filter logic. However, because reports can be viewed by multiple users, be cautious when using user-specific smart variables — the filter will resolve differently depending on who is viewing the report.

**Q: Why does switching from Advanced Logic back to the Logic Builder erase my filter?**
**A:** The Logic Builder can only represent a subset of possible logic expressions — it has no way to render functions like `datediff` or `sum` as its dropdown controls. REDCap warns you before erasing, so you can cancel and preserve your advanced filter if you clicked the wrong button.

---

# 7. Common Mistakes & Gotchas

**Writing logic that is always true or always false.** Advanced Logic does not validate whether a condition is logically reachable. A filter like `[age] > 200` will never return any records; `[age] >= 0` will always return all records. Test new advanced filters against a few known records with varied data before publishing the report.

**Misunderstanding "Show data for all events" in longitudinal projects.** With this option checked (default), a matching record shows all of its event data. Users sometimes expect the filter to hide events that don't match — that only happens when the checkbox is unchecked. The unchecked behavior requires careful per-event testing and is considered an advanced use case.

**Selecting both Event and DAG filters and expecting OR behavior.** When both filters are active, REDCap applies AND logic between them. If you want records from either DAG A or Event X (not both), you would need to express that in a logic filter rather than in the Additional Filters dropdowns.

**Mixing AND and OR in the Logic Builder and expecting left-to-right evaluation.** Consecutive OR rows are grouped first, then the groups are joined with AND, so `A OR B AND C OR D` means `(A OR B) AND (C OR D)`. Use Advanced Logic with explicit parentheses for any other grouping.

**Confusing live filter selections with saved report filters.** Live filter values are not saved with the report and are not stored per user. Opening the report from the report list starts unfiltered; to return to a particular selection, bookmark or share the report page link after applying the live filters.

**Excluding a DAG user's own DAG in the DAG filter.** Users assigned to a DAG see only their own DAG's records. If the report's DAG filter does not include their DAG, the report shows no records for them.

**Assuming the Logic Builder and Advanced Logic can be used simultaneously.** They are mutually exclusive. Switching from one to the other replaces the current filter content. The only shared workflow is using Advanced Logic to preview what the Logic Builder has generated, before switching back.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-38 — Export Reports API](RC-API-38_Export-Reports.md)** — the same filtering and ordering defined in the report are applied when exporting via API; live filters are not applied

---


# 8. Related Articles

- [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) (prerequisite — report creation and field selection)
- [RC-EXPRT-08 — Custom Reports: Management & Organization](RC-EXPRT-08_Custom-Reports-Management-and-Organization.md) (saving reports, organizing into folders)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (background on the logic system shared with report filters)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (syntax reference for Advanced Logic)
- [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md) (AND, OR and parentheses in Advanced Logic)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (background on DAGs referenced in event/DAG filters and live filters)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (background on events referenced in longitudinal filter options)
