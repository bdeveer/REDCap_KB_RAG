---
name: redcap-dd-fixer
description: |
  Fix errors and problems in a REDCap Data Dictionary CSV. Use this skill whenever a user uploads or shares a data dictionary that has issues, fails to upload to REDCap, or needs corrections applied. Trigger on: "fix my data dictionary", "my DD won't upload", "the upload is failing", "fix the branching logic in my DD", "clean up this CSV", "there are errors in my data dictionary", "can you fix this", or any time a data dictionary CSV is shared alongside a complaint, error message, or request to fix/correct/clean something. Also trigger when parse_dd.py or REDCap itself reports upload errors. Use this skill even for partial fixes — "just fix the branching logic columns" or "clean up the validation columns" — this skill handles targeted repairs too. Do NOT use for building a new data dictionary from scratch (use redcap-dd-builder) or for summarizing/explaining what a DD contains (use redcap-data-dictionary).
---

# REDCap Data Dictionary Fixer

> **REDCap connectors:** before calling any REDCap MCP tool from this skill, read `references/CONNECTOR-RULES.md` (bundled with this skill; the source copy is `claude skills/CONNECTOR-RULES.md` in the REDCap_KB_RAG repo) and follow it — confirm the connector and PID, flag production, stay read-only unless the user explicitly confirms a write on a non-production connector, and never expose the API token.

**Working from a live project.** If the user names a project instead of attaching a CSV, pull the DD with `export_metadata`, save the JSON to a file and run the fixer on it (the output CSV uses the standard upload headers). Hand the fixed CSV to the user to upload on the project's **Data Dictionary** page. Do not call `import_metadata` yourself unless the user asks for it on a non-production connector — it replaces the entire data dictionary.

This skill diagnoses issues in a REDCap Data Dictionary CSV, applies safe automatic corrections, flags remaining problems that need manual attention, and delivers a corrected CSV ready for re-upload.

**Dependency:** `fix_dd.py` imports the shared module `dd_common.py`, and Step 1 uses `parse_dd.py`, both from the redcap-data-dictionary skill — that skill must be installed alongside this one.

---

## Step 1: Parse the DD

Start by running the parser to understand what's in the file and surface any structural issues.

```bash
python <skill_path>/../redcap-data-dictionary/scripts/parse_dd.py <path_to_csv> --text
```

Read the output. Pay attention to the "Potential Issues" section — these are the problems you need to fix or flag.

**Finding `<skill_path>`** (used for `fix_dd.py` below): This skill's base directory, shown when the skill loads (normally `~/.claude/skills/redcap-dd-fixer`).

**Finding the input file:** Use the path the user gives or attaches. If they only name the file, look in the folder they are working in or use Glob to find it; ask if more than one file matches.

Write output files next to the input file, or to a folder the user names (never a temp folder), and give the user the full path of each file.

---

## Step 2: Run the Fixer

Apply automatic corrections:

```bash
python <skill_path>/scripts/fix_dd.py <path_to_csv> --output <output_path>
```

The fixer writes a change log next to the output CSV (`<output>_changes.txt`, or `.json` with `--log-json`) before writing the CSV, and prints the same log. Input may use display headers or API-style headers (`field_name`, `branching_logic`, ...); the output keeps the input's header style.

For a machine-readable change log (useful for downstream processing):
```bash
python <skill_path>/scripts/fix_dd.py <path_to_csv> --output <output_path> --log-json
```

The fixer applies these corrections automatically:

| What it fixes | Where | How |
|---|---|---|
| Leading/trailing whitespace | All cells | Stripped |
| Uppercase field types | Column D | Lowercased |
| `"double-quoted"` strings in branching logic | Column L | Converted to `'single quotes'` — unless the string contains an apostrophe (e.g. `"O'Brien"`), which is left as-is and flagged. Why: REDCap accepts both, but opening a DD with double quotes in Excel mangles them |
| `==` equality operator | Column L | Replaced with `=` (operators inside string literals are never touched) |
| `!=` not-equal operator | Column L | Replaced with `<>` |
| `&&` boolean and | Column L | Replaced with `AND` |
| `\|\|` boolean or | Column L | Replaced with `OR` |
| `Y`/`yes`/`1`/`true` in Identifier? | Column K | Normalized to `y` (`N`/`no`/`0`/`false` → blank; anything else kept and flagged) |
| `Y`/`yes`/`1`/`true` in Required? | Column M | Same as Identifier? |
| Validation min/max on fields other than text/slider | Columns I/J | Cleared |
| `"double-quoted"` strings in @CALCTEXT/@CALCDATE | Column R | Converted to single quotes (same apostrophe rule; nested parentheses handled) |

The fixer also flags — but does **not** auto-fix — these issues that require human judgment:

- **Missing choices** on dropdown/radio/checkbox fields → REDCap rejects the upload
- **Missing formula** on calc fields → field will display blank
- **Duplicate variable names** → REDCap rejects the upload
- **Invalid field types** → REDCap rejects the upload
- **Uppercase or invalid variable names** (e.g. `Age`) → reported with every row that references them; never renamed by the script
- **Unrecognised Identifier?/Required? values** → kept as-is for you to decide
- **Double-quoted strings containing an apostrophe**, unbalanced quotes, or unclosed @CALCTEXT/@CALCDATE parentheses
- **Complex expression errors** in branching logic or formulas (see Step 3)

---

## Step 3: Check Expressions

The fixer script handles simple operator issues, but it cannot catch more complex expression problems. After running the fixer, review each expression-bearing field for issues the script cannot handle.

### Which fields to check

Check these columns after the fixer runs:

| Column | What to check |
|---|---|
| **Column L (Branching Logic)** | All fields with non-empty branching logic |
| **Column F (Choices/Calc)** on `calc` fields | The formula expression |
| **Column R (Field Annotation)** | Any `@CALCTEXT(...)` or `@CALCDATE(...)` calls |

### Expression issues to look for

**Bracket and quote balance**
Every `[` needs `]`, every `(` needs `)`, every `'` needs a closing `'`.

**Exponentiation**
Both base and exponent need their own parentheses: `([height])^(2)` not `[height]^2`.

**Checkbox field references**
A plain `[symptoms]` on a checkbox field returns blank in logic contexts. Use `[symptoms(3)]='1'` to check if option 3 is selected.

**Variables inside quoted strings**
`@CALCTEXT(if([group]='1', 'Hello [name]', ''))` — `[name]` here is literal text, not the field's value. Use `[name]` outside the quotes or `concat('Hello ', [name])`.

**Function argument counts**
Common misses: `datediff()` requires 3 args (unit string is mandatory); `if()` requires exactly 3 args; `@CALCDATE()` requires exactly 3 args.

**@CALCDATE unit strings (case-sensitive)**
`'M'` = months, `'m'` = minutes — a silent error if swapped.

**Cross-event references (longitudinal)**
Format is `[event_name][field_name]` — no dot, no space, no nested brackets.

> For complex expression repairs, the `redcap-syntax` skill (fix mode) has the full set of rules and handles reference checking (whether fields and events actually exist in the project). If you need to go deep on a specific expression, read that skill's SKILL.md and `references/fix-mode.md`.

---

## Step 4: Handle Flagged Issues

After delivering the auto-fix report and corrected CSV, go through **each flagged issue one by one** and prompt the user with a concrete suggestion. Don't just list the problems — actively help resolve them. Frame each prompt so the user knows exactly what information or decision you need.

### Missing choices on dropdown/radio/checkbox (ERROR — blocks upload)

Present the field and ask for the options. Give an example of the expected format to make it easy.

> `[field_name]` is a `[type]` field but has no choices defined — REDCap won't accept the upload until this is filled in. What options should users be able to select? For example: `1, Option A | 2, Option B | 99, Unknown`

Once the user provides the options, add them to the corrected CSV in Column F and re-export it.

### Missing formula on calc field (ERROR — field will always be blank)

Ask what the field should compute. If the user describes it in plain language, use the `redcap-syntax` skill to write the formula.

> `[field_name]` is a calculated field with no formula — it will always display blank. What should it calculate? If you describe the calculation (e.g. "sum of phq9_q1 through phq9_q9"), I can write the formula for you.

### Duplicate variable names (ERROR — blocks upload)

Explain the stakes before asking for a decision.

> `[variable_name]` appears more than once (rows X and Y). REDCap requires unique variable names. One option is to rename the duplicate — but be aware that if data has already been collected under either name, renaming it will sever the link to that data. Which occurrence should keep the name, and what should the other one be renamed to? Or should one be deleted entirely?

### Invalid field type (ERROR — blocks upload)

Show what REDCap received and list the valid alternatives.

> `[variable_name]` has field type `[invalid_type]`, which REDCap doesn't recognise. The valid types are: `text`, `notes`, `dropdown`, `radio`, `checkbox`, `calc`, `file`, `descriptive`, `slider`, `yesno`, `truefalse`. Which type did you intend?

### Uppercase or invalid variable names (ERROR — may block upload or cause issues)

Show the problem, the references the fixer listed, and offer a suggested correction. Only rename after the user confirms, and then rename consistently: the variable itself **and every reference** (`[Age]`, `[Age(1)]`, `[event][Age]`, piping) in branching logic, calc formulas, annotations, labels, and notes. List every change.

> `[variable_name]` isn't a valid REDCap variable name — names must start with a letter and contain only lowercase letters, digits, and underscores. It's referenced in rows X and Y. A corrected version might be `[suggested_name]`, updated in those references too. If data has already been collected under this name, renaming will orphan it. Rename?

### Complex expression errors in branching logic or formulas (WARNING)

If the syntax checker or your own review found an error the script couldn't auto-fix, quote the expression and explain the specific problem.

> The branching logic for `[field_name]` looks like it may have an issue: `[paste expression]`. [Describe the problem, e.g. "the exponentiation syntax needs parentheses around both the base and the exponent"]. Here's a corrected version: `[corrected expression]` — does that match what you intended?

---

## Step 5: Report and Deliver

Present the results in this order:

1. **Summary line**: "X auto-fixes applied, Y issues still need your input before the file can be uploaded."
2. **Change table**: For each auto-fix — which field, which column, what changed and why. Group repeated fix types (e.g. "8 fields: double quotes → single quotes in branching logic").
3. **Corrected file**: Link to the fixed CSV. Make clear this is a partial fix if flagged issues remain.
4. **Then immediately proceed to Step 4** — go through each flagged issue one by one and prompt the user for what you need to resolve it.

Keep the summary concise. Bas has solid REDCap knowledge — explain *what* was fixed and *why it matters* for anything non-obvious, but don't over-explain.

> **Data collection note:** If the user has already started collecting data, call out any changes that could affect stored records. Branching logic changes can affect which fields appear for existing records. Choice value changes affect how stored raw values are displayed. Variable renaming (if needed to resolve a duplicate) severs the link to all previously collected data under that name.

---

## When to Stop and Ask

Don't auto-fix if you're unsure. Specifically:

- **Never invent choices** for choice-type fields without asking the user
- **Never invent formulas** for calc fields without asking the user  
- **Never rename variables** without explicit user confirmation — renaming deletes data
- If branching logic has a complex error you can't confidently fix, show it to the user and explain the problem rather than guessing

The fixer script is designed to be safe: it only touches things it can reliably correct. Bring the user in for everything else.
