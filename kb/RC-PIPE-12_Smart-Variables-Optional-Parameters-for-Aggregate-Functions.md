RC-PIPE-12

**Smart Variables: Optional Parameters for Aggregate Functions**

| **Article ID** | RC-PIPE-12 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects using aggregate functions, charts, and tables (RC-PIPE-11) |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables |

---

# 1. Overview

Optional parameters are appended to aggregate functions, charts, and tables to filter which records are included in the calculation or to modify the visualization options. They allow you to narrow results to a specific report, Data Access Group (DAG), event, or adjust how charts display (e.g., vertical bars, stacked bars, hidden export links). Parameters are separated by colons and appended as a third argument. This article covers all available parameters, their syntax, use cases, and important restrictions.

---

# 2. Key Concepts & Definitions

**Parameter**

A modifier appended to an aggregate function, chart, or table smart variable to filter or refine its behavior. Parameters are separated by colons and appear as a third argument in the smart variable expression.

**Filtering Parameter**

A parameter that restricts which records or data points are included in the calculation. Examples: report filtering, DAG filtering, event filtering.

**Visualization Parameter**

A parameter that modifies how a chart or table displays without changing the underlying data. Examples: `bar-vertical`, `bar-stacked`, `no-export-link`.

**Mutually Exclusive**

Parameters that cannot be used together in the same smart variable expression. For example, report name filters cannot be combined with DAG, event, or other filtering parameters.

---

# 3. Smart Variable Parameter Reference

### 3.1 Report Filtering Parameter

| Parameter | Syntax | Description | Example |
|---|---|---|---|
| Report Name | `R-XXXXXXXXXX` | Filters results to include only records contained in the specified report. Use the unique report name (found on the My Reports & Exports page) in the format R- followed by alphanumeric characters. IMPORTANT: Report name filters cannot be combined with other filtering parameters (DAG, event, etc.). To combine filters, add filtering to the report definition itself. | `[aggregate-min:age:R-5898NNMYL4]` |

### 3.2 Record / Event Filtering Parameters

| Parameter | Syntax | Description | Example |
|---|---|---|---|
| Current Record | `record-name` | Filters results to include data from the current record only. Only works in contexts where a single record is being viewed (survey, data entry form, etc.). | `[aggregate-max:weight:record-name]` |
| Current Event | `event-name` | Filters results to include data from the current event only (longitudinal projects only). Only works where a single record/event is being viewed. | `[aggregate-max:weight:event-name]` |
| Specific Event(s) | Unique event name(s) | Filters to data from specific events by providing the event's unique event name from the Define My Events page. Multiple events separated by commas. Longitudinal projects only. | `[aggregate-min:weight:visit_1_arm_1]` or `[aggregate-min:weight:visit_1_arm_1,visit_1_arm_2]` |

### 3.3 Data Access Group (DAG) Filtering Parameters

| Parameter | Syntax | Description | Example |
|---|---|---|---|
| Current User's DAG | `user-dag-name` | Filters results to include only records in the current user's Data Access Group. Only works where an authenticated user is assigned to a DAG in the project (does not work on public dashboards or survey pages). | `[aggregate-mean:weight:user-dag-name]` |
| Specific DAG(s) | Unique DAG name(s) | Filters to records in specific DAGs by providing the DAG's unique group name from the Data Access Groups page. Multiple DAGs separated by commas. | `[aggregate-median:weight:vanderbilt_group]` or `[aggregate-median:weight:vanderbilt_group,duke_group,harvard_group]` |

### 3.4 Visualization Parameters

| Parameter | Syntax | Description | Example |
|---|---|---|---|
| Vertical Bar Chart | `bar-vertical` | For bar charts only: displays bars vertically instead of horizontally (the default). | `[bar-chart:race:bar-vertical]` |
| Stacked Bar Chart | `bar-stacked` | For two-field bar charts only (when a grouping field is specified): stacks bars on top of each other instead of side by side. Can be combined with `bar-vertical`. | `[bar-chart:race,sex:bar-stacked]` or `[bar-chart:race,sex:bar-vertical,bar-stacked]` |
| Hide Export Link | `no-export-link` | For stats-table only: hides the "Export table (CSV)" link that appears below the table by default. | `[stats-table:age,race,sex:no-export-link]` |

---

# 4. Usage Notes

**Parameter Syntax**

Parameters are appended as a third colon-separated argument. The general format is:
```
[function-type:fields:parameter1,parameter2,...]
```

For single parameters:
```
[aggregate-min:age:R-5898NNMYL4]
[bar-chart:race:bar-vertical]
```

For multiple parameters (comma-separated):
```
[bar-chart:race,sex:bar-vertical,bar-stacked]
[aggregate-mean:age:user-dag-name]
```

**Report Filtering Restrictions**

When using a report name filter (`R-XXXXXXXXXX`):
- NO other filtering parameters (DAG, event, record-name, event-name) can be used simultaneously.
- To combine report filtering with DAG or event filtering, add those filters directly to the report definition (in the report settings), not in the smart variable.
- If you attempt to combine a report filter with other parameters, the function may fail or behave unexpectedly.

**DAG and Event Filters Can Be Combined**

You can use DAG and event filters together: `[aggregate-mean:age:vanderbilt_group,visit_1_arm_1]` filters to records in the Vanderbilt Group DAG within the Baseline event.

**Visualization Parameters Are Optional**

Charts display with default visualization options if no visualization parameters are specified. Add parameters only if you need to customize the appearance:
- `bar-vertical`: vertical bars instead of horizontal
- `bar-stacked`: stacked bars instead of side-by-side
- `no-export-link`: hide the CSV export option for stats tables

**Event Naming**

When filtering by event, use the unique event name (e.g., `baseline_arm_1`, `month_3_arm_2`) from the Define My Events page. Do not use the event label (the human-readable name).

**DAG Naming**

When filtering by DAG, use the unique DAG name (e.g., `vanderbilt_group`, `harvard_site`) from the Data Access Groups page. Do not use the DAG label (the human-readable display name).

**Current User vs. Specific User**

The `user-dag-name` parameter filters to the current logged-in user's DAG. It does not work on public dashboards or survey pages where no user is authenticated. To filter to a specific, non-current user's DAG, use the unique DAG name directly instead.

**Record-Name and Event-Name Context Requirements**

The `record-name` and `event-name` parameters only function in contexts where a single record/event is active (e.g., in a form field, survey, data entry form). They do not work on dashboards or reports where multiple records are being viewed simultaneously.

**Multiple Values for DAGs and Events**

To include multiple DAGs or events, use comma separation (no spaces): `[aggregate-count:age:vanderbilt_group,duke_group,harvard_group]`. This filters to all three DAGs.

---

# 5. Common Questions

**Q: How do I filter an aggregate function to show only a specific Data Access Group?**

**A:** Use the DAG name parameter. For example: `[aggregate-mean:weight:vanderbilt_group]` shows the mean weight for records in the Vanderbilt Group DAG. Use the unique DAG name, not the label. To include multiple DAGs: `[aggregate-mean:weight:vanderbilt_group,harvard_group]`.

**Q: Can I combine a report filter with a DAG filter?**

**A:** No. Report name filters (`R-XXXXXXXXXX`) are mutually exclusive with other filtering parameters. If you need to combine filters, add the additional filtering logic to the report definition itself (in the report settings), then reference the report in the smart variable.

**Q: How do I display a vertical bar chart instead of horizontal?**

**A:** Add the `bar-vertical` parameter: `[bar-chart:race:bar-vertical]`. This is a visualization parameter that changes how the chart displays without changing the underlying data.

**Q: I want to filter a stats-table to show only data from a specific event in my longitudinal project. How do I do that?**

**A:** Use the event name parameter: `[stats-table:age,weight,height:baseline_arm_1]` shows statistics for those fields only from the Baseline event of Arm 1.

**Q: Can I hide the "Export table (CSV)" link from a stats-table?**

**A:** Yes, use the `no-export-link` parameter: `[stats-table:age,race,sex:no-export-link]`. This is useful if you want to prevent users from exporting the summary statistics.

**Q: How do I filter results to the current user's Data Access Group?**

**A:** Use the `user-dag-name` parameter: `[aggregate-mean:age:user-dag-name]`. This filters to whatever DAG the currently logged-in user belongs to. Note that this does not work on public dashboards.

**Q: Can I use multiple visualization parameters in one smart variable?**

**A:** Yes, for bar charts you can combine `bar-vertical` and `bar-stacked`: `[bar-chart:race,sex:bar-vertical,bar-stacked]`. This displays a stacked bar chart with vertical orientation. Separate multiple parameters with commas.

**Q: How do I reference a specific report using the report filter parameter?**

**A:** Find the unique report name on the My Reports & Exports page (it appears as "R-" followed by alphanumeric characters, e.g., "R-2554F4TCNT"). Use this name as the parameter: `[aggregate-count:age:R-2554F4TCNT]`.

---

# 6. Common Mistakes & Gotchas

**Attempting to combine report filters with other parameters.** Report name filters (`R-XXXXXXXXXX`) cannot be used with DAG, event, or record-name filters. If you need multiple filters, add them to the report definition itself, not the smart variable. A common error is: `[aggregate-mean:age:R-5898NNMYL4,vanderbilt_group]` (invalid — do not mix report and DAG filters).

**Using DAG labels instead of DAG names.** The DAG label is the human-readable display name (e.g., "Vanderbilt Group"). The DAG name is the unique identifier (e.g., "vanderbilt_group"). Always use the DAG name in parameters: `[aggregate-mean:age:vanderbilt_group]` (correct) not `[aggregate-mean:age:Vanderbilt Group]` (incorrect).

**Using event labels instead of event names.** Similarly, use unique event names (e.g., `baseline_arm_1`) not event labels (e.g., "Baseline"): `[aggregate-mean:weight:baseline_arm_1]` (correct) not `[aggregate-mean:weight:Baseline]` (incorrect).

**Assuming `record-name` and `event-name` work on dashboards.** These parameters only function in contexts where a single record or event is active (form fields, surveys, data entry). They return incorrect or blank results on dashboards where multiple records are visible.

**Forgetting commas when specifying multiple events or DAGs.** Use comma separation (no spaces) to specify multiple values: `[aggregate-mean:age:vanderbilt_group,harvard_group]` (correct) not `[aggregate-mean:age:vanderbilt_group harvard_group]` (incorrect).

**Not accounting for empty results when using strict filters.** If you filter to a DAG or event that has no data, the aggregate function may return 0 or blank. For example, if no records belong to a specific DAG, `[aggregate-count:age:vanderbilt_group]` returns 0.

**Mixing comma separators and parameter syntax incorrectly.** The syntax is: `[function:fields:param1,param2,param3]`. Commas separate parameters within the third argument, not between arguments. Do not use colons to separate multiple parameters.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables (detailed reference for functions and charts)
