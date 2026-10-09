# REDCap Connector Rules (shared by all REDCap skills)

Read this before calling any REDCap MCP tool (`mcp__<connector>__<tool>`). Every REDCap skill in this folder follows these rules; a skill may be stricter, never looser.

## 1. Pick and confirm the connector

Connector names are institution-specific, so they are **not** kept in this repo. Read the local connector map, `~/.claude/redcap-connectors.md`: it lists each connector and marks it **production** (live data), **non-production**, or **external** (another institution's server), and says where to find each connector's API URL. Read it instead of guessing.

If the map doesn't exist, ask the user which connectors are production before making any call, and treat every connector as production until they answer.

Before the first call, confirm with the user: **which connector, which project (PID)**, and state the API URL. If it is a production connector, say so in that message. Then call `check_connection`, and `export_project_info` to confirm the PID and title match what the user meant.

## 2. Read-only by default

Design and structure work needs only these metadata exports:

`check_connection`, `export_redcap_version`, `export_project_info`, `export_metadata`, `export_field_names`, `export_instruments`, `export_arms`, `export_events`, `export_instrument_event_mappings`, `export_repeating_instruments_events`

Do **not** call record, report, logging, file, PDF, project XML, user, DAG or survey-participant exports unless the user explicitly asks for that data. Those return participant or user data that design work never needs.

## 3. Writes (imports, deletes, renames)

- **Never on a production connector.** If the user asks for a write on production, decline and explain; they can do it in the REDCap UI themselves.
- On non-production connectors, only after the user explicitly confirms the exact call (tool, project, what will change).
- **Export first.** Before any import, export the current state of what you will change (e.g. `export_metadata` before `import_metadata`, `export_instrument_event_mappings` before importing mappings) and save it to a file the user can see, so it can be restored.
- Know what replaces vs. adds: `import_metadata` replaces the **entire** data dictionary; an instrument-event mapping import replaces the whole mapping for the arms it covers; arms and events imports add unless `override` is set. Never set `override=1` without saying so explicitly.
- Never call `delete_*`, `rename_record`, `randomize_record` or `switch_dag` unless that is precisely what the user asked for.

## 4. API tokens

- Use the connector's configured default token first (call without `token`).
- If that fails or belongs to another project, ask the user for the token and pass it **only** as the tool's `token` argument.
- Never echo a token back, never write it to a file, script, report or memory.

## 5. Report what you touched

When you finish, list every connector call that changed something (none, for read-only work) and the path of any export saved as a backup.
