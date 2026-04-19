RC-PIPE-17

**Smart Variables: Miscellaneous**

| **Article ID** | RC-PIPE-17 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview |

---

# 1. Overview

Miscellaneous smart variables provide system-level information about the REDCap installation and the current project. These variables return the project's unique identifier, title, status, purpose, and IRB number, as well as information about the REDCap instance itself (version number, base URL, database table name). These variables are primarily useful for REDCap administrators, system integrators, and power users who need to reference project metadata or system configuration. Most project designers will not need these variables.

---

# 2. Key Concepts & Definitions

**Project ID (PID)**

REDCap's unique numeric identifier for a project within the REDCap installation. The Project ID is assigned at project creation and does not change. It is used internally for database references and API calls.

**Project Status**

A classification indicating the current phase of a project: Development (not yet active), Production (active data collection), or Analysis/Cleanup (completed data collection, analysis phase).

**Project Purpose**

A classification indicating why a project was created: Practice/Just for fun, Other, Research, Quality Improvement, or Operational Support.

**IRB Number**

The Institutional Review Board (IRB) approval number associated with the project, if applicable. Used for regulatory tracking and documentation.

**Data Table**

The name of the specific database table (in REDCap's MySQL database) where a project's data is stored. REDCap distributes records across multiple tables (redcap_data1, redcap_data2, etc.) for performance optimization.

**REDCap Installation / Instance**

The specific deployment of REDCap software at an institution. An institution may have one or multiple REDCap instances. Each instance has its own version number, base URL, and database.

**REDCap Version**

The version number of the REDCap software running on the current installation (e.g., 16.1.3).

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Project ID | `[project-id]` | The unique numeric Project ID of the current REDCap project. | 39856 |
| Project Title | `[project-title]` | The title of the current project, as configured in project settings. | Health Progression Study |
| Project Status | `[project-status]` | The status of the current project: 0 = Development, 1 = Production, 2 = Analysis/Cleanup. Returns the numeric code. | 0 |
| Project Purpose | `[project-purpose]` | The purpose of the current project: 0 = Practice/Just for fun, 1 = Other, 2 = Research, 3 = Quality Improvement, 4 = Operational Support. Returns the numeric code. | 2 |
| Project IRB Number | `[project-irb-number]` | The IRB approval number associated with the current project, as configured in project settings. Returns blank if no IRB number is defined. | 2025-1234 |
| Data Table (Current Project) | `[data-table]` | The name of the database table used by the current project to store record data. | redcap_data3 |
| Data Table (Specific Project) | `[data-table:PID]` | The name of the database table used by a specific project (identified by Project ID). Replace PID with a numeric project ID. | redcap_data2 |
| REDCap Base URL | `[redcap-base-url]` | The base web address (URL) of this REDCap installation. | https://redcap.yourinstitution.edu/ |
| REDCap Version | `[redcap-version]` | The current version number of the REDCap software running on this installation. | 16.1.3 |
| REDCap Version URL | `[redcap-version-url]` | The base web address (URL) of the current REDCap version directory on this installation. | https://redcap.yourinstitution.edu/redcap_v16.1.3/ |
| Survey Base URL | `[survey-base-url]` | The base web address (URL) for surveys on this REDCap installation. | https://redcap.yourinstitution.edu/surveys/ |

---

# 4. Usage Notes

**Administrator-Focused Variables**

Most miscellaneous smart variables are intended for use by REDCap administrators, system integrators, and power users who need to reference system configuration or project metadata. Regular project designers rarely need these variables.

**Project Status and Purpose Codes**

Project status and purpose are returned as numeric codes, not human-readable text:
- **Project Status:** 0 = Development, 1 = Production, 2 = Analysis/Cleanup
- **Project Purpose:** 0 = Practice, 1 = Other, 2 = Research, 3 = Quality Improvement, 4 = Operational Support

To display human-readable text, use a calculated field with conditional logic: `if([project-status]=0, 'Development', if([project-status]=1, 'Production', 'Analysis/Cleanup'))`.

**Data Table References**

The `[data-table]` smart variable returns the name of the MySQL table where a project's data is stored. This is useful for:
- Database administrators writing SQL queries against REDCap data.
- System integrators writing scripts that interface with REDCap's database.
- Troubleshooting data storage issues.

The data table name itself is not user-facing and is rarely displayed to end users.

**Data Table for Other Projects**

Use `[data-table:PID]` to get the data table name for a different project. Replace PID with the numeric Project ID. This is useful in multi-project environments or for administrative scripts.

**IRB Number Handling**

The `[project-irb-number]` variable returns blank if no IRB number has been entered in project settings. If your project has regulatory requirements, ensure the IRB number is configured in Project Setup if you plan to reference it.

**REDCap URLs**

The base URLs (`[redcap-base-url]`, `[redcap-version-url]`, `[survey-base-url]`) are useful for:
- Constructing URLs in custom scripts or integrations.
- Documentation or support materials that need to reference the REDCap installation.
- Troubleshooting connection issues by verifying the correct URL.

**Version Information**

The `[redcap-version]` variable is useful for:
- Checking which version of REDCap is in use (helpful when troubleshooting version-specific features or bugs).
- Documenting the REDCap environment in system integration logs.
- Alerting when outdated versions are in use.

---

# 5. Common Questions

**Q: How do I display the project's IRB number in a form or email?**

**A:** Use `[project-irb-number]` in a field label, field note, or email body. For example: "This project is approved under IRB #`[project-irb-number]`." If no IRB number is configured, the variable returns blank.

**Q: What is the project ID, and why would I need it?**

**A:** The project ID is REDCap's unique numeric identifier for your project. You might need it for:
- Referencing the project in API calls or database queries.
- System integration or custom development.
- Support tickets or communication with your REDCap administrator.

**Q: How can I tell if my project is in Production or Development status?**

**A:** Use `[project-status]`, which returns a numeric code: 0 = Development, 1 = Production, 2 = Analysis/Cleanup. To display readable text, use a calculated field: `if([project-status]=1, 'Production', 'Not Production')`.

**Q: What version of REDCap is my institution using?**

**A:** Use `[redcap-version]` to display the version number. For example: "This project is running on REDCap `[redcap-version]`."

**Q: What is the data table, and when would I need to reference it?**

**A:** The data table is the name of the MySQL database table (e.g., redcap_data3) where your project's data is stored. Database administrators and system integrators may need this for direct database queries or backups. Regular users do not need to reference the data table.

**Q: Can I use miscellaneous smart variables in branching logic?**

**A:** Yes, but rarely. For example, you could use `[project-status]=0` in logic to show fields only in development projects. In practice, this is not commonly done because these variables represent static project properties rather than participant data.

---

# 6. Common Mistakes & Gotchas

**Confusing project status and purpose codes with readable text.** Project status and purpose are returned as numbers (0, 1, 2, etc.), not as words like "Production" or "Research". If you need readable text, use a calculated field to convert the codes.

**Assuming the IRB number is always defined.** If an IRB number has not been entered in project settings, `[project-irb-number]` returns blank. Do not rely on this variable without first confirming that the IRB number is configured.

**Referencing data tables in user-facing forms.** Data table names are technical database identifiers and are meaningless to study participants or coordinators. Do not display `[data-table]` in forms or emails intended for users; this variable is for administrators and developers only.

**Using data table variables in projects you don't own.** Referencing the data table of another project (`[data-table:OTHER-PID]`) is generally safe, but only administrators or integrators who need this information should do so. Regular users do not have a legitimate use for this variable.

**Not accounting for version differences in documentation.** The `[redcap-version]` shows the current version, but features and behaviors change between versions. If you document a feature or workaround, note the version it applies to rather than relying on the version variable alone.

**Attempting to use miscellaneous variables for non-administrative purposes.** These variables are designed for system administrators and developers. Attempting to use them in regular project design (e.g., displaying project ID to participants) is usually a sign that a different approach is needed.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
