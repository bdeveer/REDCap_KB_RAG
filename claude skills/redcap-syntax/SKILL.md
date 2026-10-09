---
name: redcap-syntax
description: >
  Write, fix, or explain REDCap expressions — branching logic, calculated fields, @CALCTEXT,
  @CALCDATE, and the smart variables, instance qualifiers, and cross-event references used inside
  them. Three jobs: (1) WRITE a new expression from a described goal or complete a partial one;
  (2) FIX/diagnose an expression that isn't working, returns blank, shows unexpectedly, or contains
  a mistake — separating syntax errors from reference errors (field, event, designation, repeat
  setup); (3) EXPLAIN/read an existing expression — what it does, what type it is, what it returns.
  Triggers include: "write me a formula", "how do I calculate X", "I need branching logic that
  shows Y when Z", "build a calc field for", "create an expression", "write a @CALCTEXT", "help me
  make a calculated field", "what would the syntax be for", "can you write the logic for", "how
  would I express this in REDCap", "fix this", "what's wrong with", "this isn't working", "my
  calculation is blank", "branching logic not showing", "can you check this expression", "is this
  valid REDCap syntax?", "what does this expression mean?", "why is my calculation blank?", "what's
  the difference between a calc field and @CALCTEXT?", or any pasted snippet with square-bracket
  variables, REDCap operators, or @CALCTEXT/@CALCDATE syntax. Use it even if the expression looks
  almost right. Do NOT use for: repairing a whole data dictionary CSV (use redcap-dd-fixer),
  building a data dictionary (use redcap-dd-builder), or KB lookups unrelated to a specific
  expression (use kb-search).
---

# REDCap Syntax

> **REDCap connectors:** before calling any REDCap MCP tool from this skill, read `C:\Users\bd593\Documents\RCRAG\REDCap_KB_RAG\claude skills\CONNECTOR-RULES.md` and follow it — confirm the connector and PID, flag production, stay read-only unless the user explicitly confirms a write on a non-production connector, and never expose the API token.

One skill for every REDCap expression task. Pick the mode first, then read only the references
that mode needs.

---

## Step 0: Pick the mode

| Mode | The user has… | Tell-tale signs | Read |
|---|---|---|---|
| **Write** | A goal, or a partial expression to finish | "write", "build", "create", "how do I calculate", "what would the syntax be" — no complete expression yet | `references/write-mode.md` |
| **Fix** | A complete expression plus a problem, or a request to check it | "fix", "not working", "blank", "not showing", "wrong", "check this", "is this valid" | `references/fix-mode.md` |
| **Explain** | A complete expression and a question about what it means | "what does this mean", "explain", "what type is this", "what does it return" — no complaint | `references/explain-mode.md` |

**Mixed requests:**
- "Explain why this is wrong" / "why is my calculation blank?" → **Fix** mode; give the explanation
  inside each error entry.
- "Is this valid?" → **Fix** mode (it is a check). If nothing is wrong, say so and briefly explain
  what it does.
- "Explain this, and change it so it also does X" → **Explain** the existing expression first, then
  **Write** the new version.
- "Fix this and add a condition for Y" → **Fix** first (list every error), then extend it using
  Write-mode construction rules.
- Pure conceptual question ("calc field vs @CALCTEXT?") with no expression → **Explain** mode using
  the type tables in `references/syntax-core.md`.

If you genuinely can't tell, ask one question: "Do you want me to write a new expression, fix this
one, or explain what it does?"

---

## Universal rules (all modes)

- **Read `references/syntax-core.md`** for any non-trivial expression — it holds the expression
  types, operators, quoting, blank handling, checkbox, cross-event, instance-qualifier, smart-variable,
  and @CALCDATE rules. It is the single source for those rules; don't contradict it.
- **Read `references/functions.md` before writing, checking, or explaining any Special Function**
  (`if`, `datediff`, `age_at_date`, `sum`, `concat_ws`, …). Argument counts and order matter, and wrong
  arguments often fail silently.
- Identify the expression type (branching logic / calculated field / @CALCTEXT / @CALCDATE) before
  anything else — the type decides which rules apply. If it's ambiguous, ask where the expression
  lives, or cover both possibilities.
- Use variable names, never field labels. Use unique event names, never event labels.
- Prefer single quotes in anything that may pass through a Data Dictionary edited in Excel.
- Don't invent problems in a correct expression, and don't silently change anything you don't
  explain.
- Logic is not used for field validation constraints — those use the field's native validation
  settings.
- When citing behavior, cite the KB article (e.g., RC-CALC-01 §6.3) where the core reference gives one.

---

## Optional: live-project validation (Write and Fix modes only)

If the user names a REDCap MCP connector **and** a project, you may check field names, checkbox
codes, unique event names, instrument–event designations, and repeat setup against the live
project instead of asking the user to paste them.

- **Connectors:** which ones exist and which are **production** is listed in the local connector map,
  `~/.claude/redcap-connectors.md` (see `CONNECTOR-RULES.md`).
- **Confirm first:** restate the connector (and that it is **production**, if it is) and get a yes
  before the first call.
- **Allowed tools — read-only metadata only:** `export_project_info`, `export_metadata`,
  `export_events`, `export_instrument_event_mappings`, `export_repeating_instruments_events`,
  `export_redcap_version` (for the version-defect check in `fix-mode.md` 4f).
- **Never** call any import, delete, rename, randomize, or record/report/file export tool from this
  skill — not even "just to look".
- What to check is listed in the Reference check of `references/fix-mode.md`; use the same list to
  confirm names before handing over a Write-mode expression.

---

## Reference files

| File | Contents | When |
|---|---|---|
| `references/syntax-core.md` | Shared rules: types and return values, operators, quoting, blank handling, checkboxes, cross-event, instance qualifiers, smart variables, calc / @CALCTEXT / @CALCDATE rules, KB article list | Every mode, any non-trivial expression |
| `references/functions.md` | Special Function signatures, argument counts, return types, common mistakes | Before using or judging any function |
| `references/write-mode.md` | Context questions, construction patterns by type, output format | Write mode |
| `references/fix-mode.md` | Syntax checklist, reference check, output format | Fix mode |
| `references/explain-mode.md` | How to recognise each type, explanation structure, output format | Explain mode |
