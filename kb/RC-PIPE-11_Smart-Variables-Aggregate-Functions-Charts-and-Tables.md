RC-PIPE-11

**Smart Variables: Aggregate Functions, Charts, and Tables**

| **Article ID** | RC-PIPE-11 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with Project Dashboards enabled |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions |

---

# 1. Overview

Aggregate functions, charts, and tables (collectively called "Smart Functions" and "Smart Charts" in REDCap) allow project administrators and power users to display summary statistics and visualizations on Project Dashboards. These smart variables calculate descriptive statistics (min, max, mean, median, sum, count, standard deviation, unique count) across all records and optionally create data visualizations (scatter plots, line charts, bar charts, pie charts, donut charts). They are primarily used by administrators building dashboard analytics rather than by regular data entry coordinators. Optional parameters allow filtering by report, DAG, event, or visualization options.

---

# 2. Key Concepts & Definitions

**Project Dashboard**

A customizable administrative view in REDCap that displays summary information, statistics, and charts about project data. Dashboards are configured by project administrators and can be shared publicly.

**Aggregate Function**

A smart variable that calculates a summary statistic (count, sum, mean, etc.) across multiple records. The result is a single number displayed on the dashboard or in a field.

**Smart Chart / Smart Graph**

A visual representation of project data in the form of a scatter plot, line chart, bar chart, pie chart, or donut chart. Charts can include optional grouping by a categorical field.

**Stats Table**

A tabular display of descriptive statistics for specified fields. Each row represents a field, and columns display statistics like count, min, max, mean, median, standard deviation, and sum.

**Data Aggregation**

The process of combining and summarizing data from all records, all events, and all instances into a single statistic or visualization. Aggregation naturally groups data from the same event and instance.

**Grouping Field**

An optional categorical field (multiple choice, dropdown, radio, or checkbox) used to color-code or separate data in charts. The grouping field adds a visual dimension to the chart.

---

# 3. Smart Variable Reference

### 3.1 Aggregate Functions

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Minimum | `[aggregate-min:fields]` or `[aggregate-min:fields:parameters]` | The minimum value across all records, all events, and all instances for the specified field(s). Multiple fields are comma-separated. | 13 |
| Maximum | `[aggregate-max:fields:parameters]` | The maximum value across all records, all events, and all instances. | 95 |
| Mean | `[aggregate-mean:fields:parameters]` | The mean (average) value across all records, all events, and all instances. | 100.1 |
| Median | `[aggregate-median:fields:parameters]` | The median value across all records, all events, and all instances. | 57 |
| Sum | `[aggregate-sum:fields:parameters]` | The sum of all values across all records, all events, and all instances. | 9451 |
| Count | `[aggregate-count:fields:parameters]` | The count of all values (non-blank entries) across all records, all events, and all instances. | 68 |
| Standard Deviation | `[aggregate-stdev:fields:parameters]` | The standard deviation of all values across all records, all events, and all instances. | 5.4 |
| Unique Count | `[aggregate-unique:fields:parameters]` | The count of unique (non-duplicate) values across all records, all events, and all instances. | 22 |

**Syntax Notes:**
- Replace `fields` with one or more field names (comma-separated for multiple fields).
- `parameters` is optional and allows filtering by report, DAG, event, or other criteria (see RC-PIPE-12).
- Examples: `[aggregate-min:age]`, `[aggregate-min:age,participant_age,other_age]`, `[aggregate-max:weight:R-5898NNMYL4]`

### 3.2 Charts

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Scatter Plot | `[scatter-plot:x-axis-field,y-axis-field]` or `[scatter-plot:x-axis-field,y-axis-field,grouping-field]` | A scatter plot with points representing records. X-axis must be a number, date, or datetime field; Y-axis must be numeric. Optional grouping field (multiple choice only) adds color coding. If only X-axis provided, random Y values are assigned. | [Chart displayed on page] |
| Line Chart | `[line-chart:x-axis-field,y-axis-field]` or `[line-chart:x-axis-field,y-axis-field,grouping-field]` | A line chart (scatter plot with connected dots). Same axis requirements and optional grouping as scatter plot. | [Chart displayed on page] |
| Bar Chart | `[bar-chart:field]` or `[bar-chart:field,grouping-field]` | A bar chart for a single multiple-choice field. Optional color grouping with a second multiple-choice field. Bars default to horizontal; use `bar-vertical` parameter to orient vertically. Can stack bars with `bar-stacked` parameter. | [Chart displayed on page] |
| Pie Chart | `[pie-chart:field]` | A pie chart for a single multiple-choice field. Shows proportions of each response option. | [Chart displayed on page] |
| Donut Chart | `[donut-chart:field]` | A donut chart (pie chart with center removed) for a single multiple-choice field. Visually similar to pie chart but with hollow center. | [Chart displayed on page] |

### 3.3 Tables

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Stats Table | `[stats-table:fields]` or `[stats-table:fields:columns]` | A table of descriptive statistics. Each field is a row; columns display statistics (Count, Missing, Unique, Min, Max, Mean, Median, StDev, Sum). No limit on number of fields (comma-separated). Default: all columns. To show a subset, specify column designations (comma-separated): `count`, `missing`, `unique`, `min`, `max`, `mean`, `median`, `stdev`, `sum`. | [Table displayed on page] |

**Syntax Notes:**
- For stats-table, the default (without specifying columns) displays all 9 columns.
- Example: `[stats-table:age,weight,height:min,max,median]` displays only Min, Max, and Median columns.
- Default column order applies if multiple columns are specified; custom ordering is not available.

---

# 4. Usage Notes

**Scope of Aggregation**

All aggregate functions, charts, and tables naturally aggregate across all records, all events, and all repeating instances unless filtering parameters are applied. This means data is combined globally unless you specify a filter (see RC-PIPE-12 for filtering options).

**Natural Grouping**

When using multiple fields in a stats-table or chart, data is naturally grouped by the event and repeating instance they come from. For example, `[stats-table:age,weight,height]` displays statistics for age, weight, and height, with data grouped by the context in which they were collected.

**Field Requirements for Charts**

- **Scatter plot and line chart**: X-axis field must be numeric, date, or datetime; Y-axis field must be numeric.
- **Bar chart**: Field must be multiple choice, dropdown, radio, or checkbox.
- **Pie chart and donut chart**: Field must be multiple choice.
- If you use an incompatible field type, REDCap will either render the chart incorrectly or display an error.

**Grouping Field Limitations**

Grouping fields must be categorical (multiple choice, radio, dropdown, or checkbox). Numeric and text fields cannot be used as grouping fields. If you specify an invalid grouping field, the chart will display without grouping.

**Chart Display on Dashboards**

Charts and tables are rendered as interactive widgets on Project Dashboards. They display inline on the dashboard page and can be configured with titles, descriptions, and sizing options by the dashboard administrator.

**Optional Parameters**

For parameters like report filtering, DAG filtering, event filtering, and visualization options (bar-vertical, bar-stacked, no-export-link), see RC-PIPE-12. Parameters are appended as a third colon-separated argument.

**Video Resource**

REDCap provides a 14-minute video demonstration of Smart Charts, Functions, and Tables within the application. Access it from the Project Dashboard interface.

---

# 5. Common Questions

**Q: What is the difference between an aggregate function and a chart?**

**A:** An aggregate function (like `[aggregate-mean:age]`) returns a single number (the mean age across all records). A chart (like `[bar-chart:race]`) creates a visual display of data categories. Use functions for summary statistics; use charts for visualizations.

**Q: How do I create a bar chart showing the distribution of responses to a multiple-choice field?**

**A:** Use `[bar-chart:field_name]` where `field_name` is the name of your multiple-choice field. For example: `[bar-chart:sex]` creates a bar chart showing the count of male vs. female responses. Add `bar-vertical` parameter to orient bars vertically: `[bar-chart:sex:bar-vertical]`.

**Q: Can I create a chart that compares two groups?**

**A:** Yes, using the grouping-field parameter. For example, `[bar-chart:adverse_event,treatment_arm]` creates bars for adverse events, color-coded by treatment arm. Both fields must be multiple-choice.

**Q: How do I display a table showing summary statistics for multiple fields?**

**A:** Use `[stats-table:field1,field2,field3]` to display counts, minimums, maximums, means, and other statistics for all specified fields. To show only a subset of statistics, add a third parameter: `[stats-table:age,weight,height:min,max,mean]` displays only Min, Max, and Mean columns.

**Q: What fields can I use for a scatter plot or line chart?**

**A:** The X-axis field must be numeric, date, or datetime. The Y-axis field must be numeric. For example, a scatter plot of height vs. weight: `[scatter-plot:height,weight]`. A time-series plot: `[line-chart:visit_date,blood_pressure]`.

**Q: How do I filter an aggregate function to show only records in a specific Data Access Group (DAG)?**

**A:** Use the optional parameters (see RC-PIPE-12). For example: `[aggregate-mean:age:vanderbilt_group]` shows the mean age for records in the Vanderbilt Group DAG only. Multiple DAGs can be comma-separated.

**Q: Can I use aggregate functions in regular form fields or only on dashboards?**

**A:** Aggregate functions are primarily designed for use on Project Dashboards. Technically, they can be placed in field labels or notes, but they are most useful and performant on dashboards.

---

# 6. Common Mistakes & Gotchas

**Using incompatible field types in charts.** Bar charts require multiple-choice fields, not numeric or text fields. Scatter plots require numeric X-axis and Y-axis fields, not text. If you attempt to chart an incompatible field type, REDCap will display an error or render the chart incorrectly. Always verify field types before creating charts.

**Confusing aggregate functions with individual field piping.** `[aggregate-mean:age]` returns the mean age across all records. `[age]` pipes the age value for the current record. Do not mix them up; they serve different purposes. Aggregate functions are for summary statistics; field piping is for individual record data.

**Forgetting to specify the instrument when referencing a field.** If a field name is not unique across your project (e.g., if multiple instruments have an "age" field), specify the field using the unique field name from the Data Dictionary. REDCap will use the correctly named field.

**Not accounting for blank or missing values in aggregates.** Aggregate functions skip blank and missing values. Count returns the number of non-blank values; Sum skips records with missing data. If a significant portion of your data is missing, summary statistics may not be representative.

**Using grouping fields with incompatible field types.** Grouping fields must be categorical (multiple choice, radio, dropdown, checkbox). If you specify a numeric or text field as a grouping field, the chart will either display without grouping or show an error.

**Attempting to filter aggregate functions without understanding parameter syntax.** Optional parameters must follow RC-PIPE-12 syntax exactly. Incorrect syntax (e.g., missing colons, typos in DAG names) will cause the function to fail or return blank. Test filters in a development environment first.

**Assuming charts update in real-time.** Charts on Project Dashboards are generated when the dashboard is loaded or refreshed. They do not auto-update as records are modified. Refresh the dashboard to see the latest data.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions (filtering and visualization options)
