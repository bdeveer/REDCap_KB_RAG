---
name: redcap-dd-fixer
description: |
  Fix errors and problems in a REDCap Data Dictionary CSV. Use this skill whenever a user uploads or shares a data dictionary that has issues, fails to upload to REDCap, or needs corrections applied. Trigger on: "fix my data dictionary", "my DD won't upload", "the upload is failing", "fix the branching logic in my DD", "clean up this CSV", "there are errors in my data dictionary", "can you fix this", or any time a data dictionary CSV is shared alongside a complaint, error message, or request to fix/correct/clean something. Also trigger when parse_dd.py or REDCap itself reports upload errors. Use this skill even for partial fixes — "just fix the branching logic columns" or "clean up the validation columns" — this skill handles targeted repairs too.
---

# REDCap Data Dictionary Fixer

This skill diagnoses issues in a REDCap Data Dictionary CSV, applies safe automatic corrections, flags remaining problems that need manual attention, and delivers a corrected CSV ready for re-upload.

---

## Step 1: Parse the DD

Start by running the parser to understand what's in the file and surface any structural issues.

```bash
python <skill_path>/scripts/parse_dd.py <path_to_csv> --text
```

Read the output. Pay attention to the "Potential Issues" section — these are the problems you need to fix or flag.

**Finding `<skill_path>`:** The directory containing this SKILL.md file.
**Finding the uploaded CSV:** Files uploaded by the user land at `/sessions/.../mnt/uploads/<filename>.csv`. Check the mounted workspace folder too.

---

## Step 2: Run the Fixer

Apply automatic corrections:

```bash
python <skill_path>/scripts/fix_dd.py <path_to_csv> --output <output_path>
```

For a machine-readable change log (useful for downstream processing):
```bash
python <skill_path>/scripts/fix_dd.py <path_to_csv> --output <output_path> --log-json
```

The fixer applies these corrections automatically:

| What it fixes | Where | How |
|---|---|---|
| Leading/trailing whitespace | All cells | Stripped |
| Uppercase variable names | Column A | Lowercased |
| Uppercase field types | Column D | Lowercased |
| Double quotes in branching logic | Column L | Replaced with single quotes |
| `==` equality operator | Column L | Replaced with `=` |
| `!=` not-equal operator | Column L | Replaced with `<>` |
| `&&` boolean and | Column L | Replaced with `AND` |
| `\|\|` boolean or | Column L | Replaced with `OR` |
| `Y`/`yes`/`1` in Identifier? | Column K | Normalized to `y` |
| `Y`/`yes`/`1` in Required? | Column M | Normalized to `y` |
| Validation min/max on non-text fields | Columns I/J | Cleared |
| Double quotes in @CALCTEXT/@CALCDATE | Column R | Replaced with single quotes |

The fixer also flags — but does **not** auto-fix — these issues that require human judgment:

- **Missing choices** on dropdown/radio/checkbox fields → REDCap rejects the upload
- **Missing formula** on calc fields → field will display blank
- **Duplicate variable names** → REDCap rejects the upload
- **Invalid field types** → REDCap rejects the upload
- **Invalid variable name characters** → may be rejected or cause unpredictable behavior
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

> For complex expression repairs, the `redcap-syntax-fixer` skill has the full set of rules and handles reference checking (whether fields and events actually exist in the project). If you need to go deep on a specific expression, read that skill's SKILL.md.

---

## Step 4: Handle Flagged Issues

After delivering the auto-fix report and corrected CSV, go through **each flagged issue one by one** and prompt the user with a concrete suggestion. Don't just list the problems — actively help resolve them. Frame each prompt so the user knows exactly what information or decision you need.

### Missing choices on dropdown/radio/checkbox (ERROR — blocks upload)

Present the field and ask for the options. Give an example of the expected format to make it easy.

> `[field_name]` is a `[type]` field but has no choices defined — REDCap won't accept the upload until this is filled in. What options should users be able to select? For example: `1, Option A | 2, Option B | 99, Unknown`

Once the user provides the options, add them to the corrected CSV in Column F and re-export it.

### Missing formula on calc field (ERROR — field will always be blank)

Ask what the field should compute. If the user describes it in plain language, use the `redcap-syntax-builder` skill to write the formula.

> `[field_name]` is a calculated field with no formula — it will always display blank. What should it calculate? If you describe the calculation (e.g. "sum of phq9_q1 through phq9_q9"), I can write the formula for you.

### Duplicate variable names (ERROR — blocks upload)

Explain the stakes before asking for a decision.

> `[variable_name]` appears more than once (rows X and Y). REDCap requires unique variable names. One option is to rename the duplicate — but be aware that if data has already been collected under either name, renaming it will sever the link to that data. Which occurrence should keep the name, and what should the other one be renamed to? Or should one be deleted entirely?

### Invalid field type (ERROR — blocks upload)

Show what REDCap received and list the valid alternatives.

> `[variable_name]` has field type `[invalid_type]`, which REDCap doesn't recognise. The valid types are: `text`, `notes`, `dropdown`, `radio`, `checkbox`, `calc`, `file`, `descriptive`, `slider`, `yesno`, `truefalse`. Which type did you intend?

### Invalid variable name characters (ERROR — may block upload or cause issues)

Show the problem and offer a suggested correction.

> `[variable_name]` contains characters REDCap doesn't allow. Variable names must start with a letter and contain only lowercase letters, digits, and underscores. A corrected version might be `[suggested_name]` — does that work, or would you prefer something else?

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
