# Project To-Do

Running list of development tasks for the REDCap KB / RAG project — separate from KB article gaps (see KB-GAPS-TODO.md).

---

## KB Content

- [ ] **Create control center articles** — Cover the REDCap Control Center from an administrator perspective. Determine scope and article breakdown (domains, slugs) before starting.

- [ ] **Remove all Yale references** — Audit every article in `kb/` for Yale-specific placeholders and callout boxes. Replace with generic institution-agnostic language or a standardized `> **Institution-specific:**` placeholder pattern. Check RC-DQ-01 Rule H section as a known example.

---

## Tooling & Skills

- [ ] **Teach Claude how to build the alerts upload CSV** — Document the CSV format REDCap uses for importing Alerts & Notifications. Add to a skill (or to the relevant KB article) with enough spec detail that Claude can generate a valid import file from scratch.

- [ ] **Create an inventory of all uploadable CSV formats** — REDCap supports CSV upload for multiple features (Data Dictionary, alerts, data quality rules, randomization, user rights, DAGs, etc.). Compile a reference document listing each upload type, its columns, accepted values, and any escaping rules.

- [ ] **Create a skill: API call runner** — Skill that teaches Claude how to construct and execute REDCap API calls against a real project (token management, endpoint selection, parameter building, response parsing).

- [ ] **Create a checklist: building out a project via API** — Step-by-step checklist for provisioning a REDCap project programmatically using the API (create project, import metadata, set arms/events, configure user rights, import data, etc.).

---

## Documentation & Templates

- [ ] **Flesh out the style guide for project building** — Expand `STYLE-GUIDE.md` (or create a companion doc) to cover REDCap project design conventions: naming standards for fields/instruments/events, branching logic patterns, calculated field practices, survey design guidelines, etc. Goal: usable as a reference when building new projects.

- [ ] **Flesh out the institutional setup template** — Create or expand a template that captures institution-specific configuration (Control Center settings, external modules enabled, user role presets, DAG conventions, survey invitation defaults, etc.) so it can be filled in once and referenced by all KB articles.

---

*Last updated: 2026-04-15*
