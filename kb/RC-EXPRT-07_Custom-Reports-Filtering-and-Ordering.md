| Field | Value |
|---|---|
| Article ID | RC-EXPRT-07 |
| Domain | Exports, Reports & Stats |
| Applies To | All project types; longitudinal-specific features noted inline |
| Prerequisite | RC-EXPRT-06 — Custom Reports: Setup & Field Selection |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-EXPRT-06 — Custom Reports: Setup & Field Selection; RC-EXPRT-08 — Custom Reports: Management & Organization; RC-BL-01 — Branching Logic: Overview & Scope; RC-BL-02 — Branching Logic: Syntax & Atomic Statements; RC-DAG-01 — Data Access Groups; RC-LONG-01 — Longitudinal Project Setup |

## 1. Overview

This article covers Step 3 (filters) and Step 4 (result ordering) of the REDCap custom report builder. Filters control which records appear in a report; ordering controls the sequence in which results are displayed. Both steps are entirely optional — a report with no filters returns all records in the project, ordered by record ID by default. This is the second article in the Custom Reports series; it assumes familiarity with report creation and field selection covered in RC-EXPRT-06.

---

## 2. Key Concepts & Definitions

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
A checkbox in Step 3 (longitudinal projects only) that controls whether filters are applied per event or only at the record level. Checked by default.

---

## 3. Step 3: Filters

Filters are configured in Step 3 of the report builder. If you do not configure any filters, the report returns all records in the project.

### 3.1 Show Data for All Events (Longitudinal Projects Only)

In longitudinal projects, the first option in Step 3 is **Show data for all events for each record returned**, which is checked by default.

| Setting | Behavior |
|---|---|
| Checked (default) | If a record matches the filter condition at any point, the report displays all events for which the selected fields are defined. |
| Unchecked | The filter is applied to each event and repeated instrument independently. Only event/instance combinations that satisfy the filter are returned. |

The unchecked setting is an advanced option and requires careful testing. For most reports, leaving this checked is correct.

> **Note:** This option does not appear in projects that are not longitudinal and do not use repeated instruments.

### 3.2 Logic Builder

The Logic Builder is the default filter interface. It constructs filter conditions through dropdown selections rather than manual syntax entry.

**Building a filter condition:**

1. Select a variable using the look-up box or the dropdown (same two methods as Step 2 field selection).
2. In longitudinal projects, optionally select a specific event. The default is "All events."
3. REDCap adjusts the operator and value options to match the selected variable's field type:
   - Dropdown/radio/yes-no: operators are `=` and `≠`; values are the field's defined options.
   - Text/notes: operators include `=`, `≠`, `contains`, `does not contain`, `starts with`, `ends with`; value is a free-text box.
   - Calculated/number fields: operators include `=`, `≠`, `<`, `>`, `≤`, `≥`.
4. After completing one clause, select **AND** or **OR** from the row below to define the relationship to the next clause. AND requires both conditions to be true; OR requires at least one.
5. Repeat for each additional clause. Remove any clause using the red X at the end of its row.

> **Note:** The Logic Builder supports combined AND/OR statements, unlike the drag-and-drop branching logic builder in the Online Designer, which accepts only one type of connector per rule set. The Logic Builder also accounts for event context in longitudinal projects.

**Converting to Advanced Logic:** Click **Use Advanced Logic** (next to "Switch Format") at any point to see the branching logic equivalent of your current Logic Builder selections. This is a useful learning tool for understanding how the Logic Builder translates to syntax.

### 3.3 Advanced Logic

Click **Use Advanced Logic** to switch the filter to a free-text syntax box. This mode accepts any valid REDCap branching logic syntax, including special functions and smart variables.

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

### 3.4 Additional Filters: Event and DAG

Below the main logic filter, the Additional Filters section provides dropdown selections for event-based and DAG-based filtering. These are independent of the logic filter.

**Event filter** (longitudinal projects only): Select one or more events. Only records with data in the selected events will be returned.

**DAG filter** (if DAGs are configured): Select one or more DAGs. Only records belonging to the selected DAGs will be returned.

When both an event filter and a DAG filter are active, a record must satisfy both conditions to appear in the report.

---

## 4. Live Filters

Live filters allow users to narrow a report's results on the fly from the report view page, without editing the report. You can designate up to three variables as live filters per report.

Live filters are most useful when a single report needs to serve multiple subgroups. For example, a class registration report with "Class" as a live filter can display all classes from one report, rather than requiring a separate report per class.

Only certain variable types are eligible for live filters: multiple-choice fields (dropdown, radio, checkbox), events (longitudinal projects), and DAGs. REDCap automatically populates the live filter selection with eligible variables when you set up this section.

> **Note:** Live filter selections are user-session specific and are not saved. Each time a user opens the report, the live filter resets to its default (unfiltered) state.

---

## 5. Step 4: Ordering Results

Step 4 controls the sort order of report results. By default, results are ordered by record ID in ascending order.

To specify a custom order:

1. Select up to three variables using the look-up or dropdown method.
2. For each variable, choose **Ascending** or **Descending** order.
3. When multiple sort variables are selected, REDCap sorts by the first variable, then by the second within ties, then by the third within remaining ties.

**Example:** Order by `gender` (ascending), then by `last_name` (ascending), then by `date_of_birth` (ascending) to produce an alphabetical list grouped by gender.

---

## 6. Common Questions

**Q: Do I have to set up filters to create a report?**
A: No. Filters are entirely optional. A report with no filters displays all records in the project for the selected fields.

**Q: What is the difference between the Logic Builder and Advanced Logic?**
A: The Logic Builder is a point-and-click interface that constructs filter logic through dropdowns. Advanced Logic is a free-text syntax box accepting the same branching logic syntax used elsewhere in REDCap. Advanced Logic supports functions (`datediff`, `sum`, `ends_with`, etc.) and smart variables, which the Logic Builder does not support. Use Advanced Logic when you need anything beyond simple comparisons.

**Q: Can I use the same logic syntax I use for branching logic in a report filter?**
A: Yes, with one important difference in scope: branching logic hides or shows individual fields on an instrument; report filter logic includes or excludes entire records (or events, if the per-event setting is enabled). The syntax, functions, and smart variables are otherwise identical.

**Q: What does a live filter do that a regular filter does not?**
A: A regular filter is fixed — it applies the same condition every time the report is run. A live filter lets users change the filter value directly from the report view page without opening the report editor. Live filters are ideal when the same report needs to be sliced by different values of the same variable.

**Q: If I set both an event filter and a DAG filter in Additional Filters, how does REDCap combine them?**
A: With AND logic. A record must belong to a selected DAG AND have data in a selected event to appear in the report. There is no option to combine them with OR logic.

**Q: Can I write advanced logic that references smart variables like [user-dag-name]?**
A: Yes. Smart variables are supported in report filter logic. However, because reports can be viewed by multiple users, be cautious when using user-specific smart variables — the filter will resolve differently depending on who is viewing the report.

**Q: Why does switching from Advanced Logic back to the Logic Builder erase my filter?**
A: The Logic Builder can only represent a subset of possible logic expressions — it has no way to render functions like `datediff` or `sum` as its dropdown controls. REDCap warns you before erasing, so you can cancel and preserve your advanced filter if you clicked the wrong button.

---

## 7. Common Mistakes & Gotchas

**Writing logic that is always true or always false.** Advanced Logic does not validate whether a condition is logically reachable. A filter like `[age] > 200` will never return any records; `[age] >= 0` will always return all records. Test new advanced filters against a few known records with varied data before publishing the report.

**Misunderstanding "Show data for all events" in longitudinal projects.** With this option checked (default), a matching record shows all of its event data. Users sometimes expect the filter to hide events that don't match — that only happens when the checkbox is unchecked. The unchecked behavior requires careful per-event testing and is considered an advanced use case.

**Selecting both Event and DAG filters and expecting OR behavior.** When both filters are active, REDCap applies AND logic between them. If you want records from either DAG A or Event X (not both), you would need to express that in a logic filter rather than in the Additional Filters dropdowns.

**Confusing live filter selections with saved report filters.** Live filter values reset each time the report is opened. They are not stored per user. If users expect their last live filter selection to persist, clarify that they will need to re-apply the filter each session.

**Assuming the Logic Builder and Advanced Logic can be used simultaneously.** They are mutually exclusive. Switching from one to the other replaces the current filter content. The only shared workflow is using Advanced Logic to preview what the Logic Builder has generated, before switching back.

---

## 8. Related Articles

- RC-EXPRT-06 — Custom Reports: Setup & Field Selection (prerequisite — report creation and field selection)
- RC-EXPRT-08 — Custom Reports: Management & Organization (saving reports, organizing into folders)
- RC-BL-01 — Branching Logic: Overview & Scope (background on the logic system shared with report filters)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (syntax reference for Advanced Logic)
- RC-DAG-01 — Data Access Groups (background on DAGs referenced in event/DAG filters and live filters)
- RC-LONG-01 — Longitudinal Project Setup (background on events referenced in longitudinal filter options)
