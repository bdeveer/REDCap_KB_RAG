# Established Domain Slugs

Alphabetical by slug. Every slug in use in `kb/` appears here — if a slug is missing, that is a defect in this table, not a signal to stop. See **Keeping this table accurate** below. This file is the canonical slug list.

| Slug | Domain | Notes |
|---|---|---|
| AI | AI Tools | Covers writing tools, AI translations, and AI summarization. System-level AI configuration lives in CC |
| ALERT | Alerts & Notifications | — |
| API | API | One article per endpoint, plus RC-API-01 for general concepts |
| AT | Action Tags | Subdomain: EM (action tags supplied by External Modules, not core REDCap) |
| BL | Branching Logic | — |
| CAL | Calendar | Covers the Calendar and Scheduling modules: manual entries, schedule generation, Ad Hoc events, iCal export, visit statuses, logging |
| CALC | Calculations & Special Functions | Covers built-in REDCap functions: date/datetime, numeric, text, conditional |
| CC | Control Center | Administrator-facing system configuration, one article per Control Center page or page group. Use for *what the setting does*; use INST for *what this institution set it to* |
| CDIS | Clinical Data Interoperability Services | FHIR/EHR integration: Clinical Data Pull (CDP), Clinical Data Mart (CDM), Break the Glass. Distinct from DDP — see that row |
| DAG | Data Access Groups | Record-level access partitioning. Not to be confused with Access Control Groups (RC-CC-25) or Project Administrator Groups |
| DDE | Double Data Entry | Independent duplicate entry and reconciliation. Distinct from DE |
| DDP | Dynamic Data Pull | The older custom DDP integration. Distinct from CDIS/CDP — the changelog refers to "CDP and Custom DDP" as separate things |
| DE | Data Entry | Entering and editing record data. Field-level design belongs in FD |
| DQ | Data Quality | Covers the Data Quality module, default rules, custom rules, and Rule H |
| DSGN | Project Design Best Practices | Cross-cutting design conventions: field alignment, project structure, branching logic patterns, repeating instruments, form hygiene |
| EM | External Modules | Framework, Module Manager, and per-instance installed catalogues. Catalogue articles follow the instance-tier pattern (Production / Test / Development) |
| EXPRT | Exports, Reports & Stats | — |
| FD | Form Design | Instrument and field design, Online Designer, Data Dictionary, field embedding |
| FDL | Form Display Logic | — |
| FILE | File Repository | Project-level file storage. Distinct from SENDIT (ad-hoc secure transfer) and from File Upload *fields*, which are FD/DE |
| IMP | Data Import | Covers the Data Import Tool and every bulk-upload CSV format |
| INFRA | Self-Hosting, Deployment & Release Management | Running a private/non-production REDCap instance: containerized stacks, install/upgrade, mail capture, AI proxy, remote access/HTTPS, backups. Platform-specific guides (e.g. Synology) live here too. Also covers the REDCap release model itself — Standard vs LTS lines, version numbering, changelog reading and patching practice — which applies to all readers, not only self-hosters |
| INST | Institution-Specific | Local policy and configuration values, deliberately quarantined from the institution-agnostic core. Follows the instance-tier pattern (Production / Test / Development) |
| INTG | Integrations | Outbound hooks into external systems, e.g. the Data Entry Trigger |
| LOCK | Record Locking & E-Signatures | — |
| LOG | Logging | Project-level audit trail; logging module access, filters, entry anatomy, retention, regulatory compliance context |
| LONG | Longitudinal & Repeated Setup | Covers longitudinal mode, arms/events, repeated instruments & events |
| MCP | MCP Server | The REDCap MCP server that exposes API methods as assistant tools. Tooling around REDCap, not a REDCap feature |
| MLM | Multi-Language Management | — |
| MOB | REDCap Mobile App | Study-team offline data collection app. Separate from MYCAP |
| MSG | Messenger | Covers REDCap Messenger: conversations, user roles, notifications, file sharing |
| MYCAP | MyCap Mobile App | Participant-facing mobile app; separate from MOB (REDCap Mobile App for study teams) |
| NAV | Navigation | Subdomains: UI (project menus, bookmarks, My Projects), REC (record navigation, dashboards, arms, repeating instances) |
| OPS | Operational Use Cases | Using REDCap for non-research operational workflows, e.g. request management |
| PIPE | Piping | Covers piping basics, longitudinal/repeated piping, modifiers, smart variables, emails & notifications |
| PLUS | REDCap+ | Features gated by the REDCap+ subscription rather than by version. Applies from v17.0.0 |
| PROF | My Profile | A user's own account settings. Use USER for administering *other* users' privileges |
| PROJ | Project | Covers project lifecycle, setup checklist, and project dashboards |
| RAND | Randomization | — |
| SENDIT | Send-It | Ad-hoc secure file transfer to named recipients. **Six characters — an accepted exception to the 5-character limit; the ID is permanent.** Do not create further slugs over five characters |
| SURV | Surveys | — |
| TXT | Texting (SMS) | Covers Twilio/Mosio setup, SMS invitations, voice calls, and admin configuration |
| USER | User Rights | Administering other users: roles, privileges, user management. Use PROF for a user's own profile |

### Keeping this table accurate

This table drifted badly once — 14 slugs were in active use in `kb/` while absent here, which turned the "stop and confirm" rule in the skill's Step 2 into a false stop on long-established domains. Check it rather than trusting it:

```bash
# Run from the repo root. Slugs used in kb/ but missing from this table (should print nothing)
comm -23 \
  <(ls kb/RC-*.md | sed -E 's|.*/RC-([A-Z]+)-.*|\1|' | sort -u) \
  <(grep -oE '^\| [A-Z]+ ' "claude skills/kb-creation/references/domain-slugs.md" | tr -d '| ' | sort -u)
```

Run this before relying on the table to reject a slug. If it prints anything, add the missing rows first — a slug already carrying published articles is established by definition, whatever this table says.

When you *do* add a genuinely new slug, add the row to this file in the repo (`claude skills/kb-creation/references/domain-slugs.md`) in the same commit as the first article that uses it. A slug with no article is a guess; a slug with an article and no row is the drift above.
