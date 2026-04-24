# REDCap KB → ServiceNow Import: Admin Handoff Notes

**Prepared by:** REDCap Support Team  
**Date:** 2026-04-23  
**Contact:** basdeveer@proton.me

---

## What We're Importing

We maintain a structured REDCap knowledge base written as markdown files. Each article has a consistent ID scheme (`RC-FD-06`, `RC-SURV-01`, etc.) and explicit cross-references to prerequisite and related articles.

The export tool (`kb_to_servicenow.py`) converts these into a single Excel workbook (`REDCap_KB_ServiceNow_Import.xlsx`) with three sheets:

- **Articles** — one row per article, body pre-converted to HTML, ready to load into `kb_knowledge`
- **Relationships** — every cross-reference extracted (Prerequisites + Related Topics), one row each
- **Import Instructions** — field-by-field guidance for the import

---

## Questions to Ask the Admin

### Before Anything

1. **Which Knowledge Base do we load into?** We need the name or `sys_id` of the target KB so we can fill in the `kb_knowledge_base` column before importing. Is there an existing KB for IT/research tools, or should we create a new one called "REDCap"?

2. **What workflow state should articles start in?** The export defaults to `draft`. Do you want us to import as `draft` (review in SN before publishing), or is it okay to import as `published` directly?

3. **Who should be listed as the author?** The articles currently say "REDCap Support." Does that need to match a real ServiceNow user account? If so, which account or group should own them?

4. **Are there existing category records we should match?** Our articles have domains like *Form Design*, *Data Import*, *Surveys*, *Branching Logic*, etc. Do those need to exist as category records in SN before import, or does the import create them?

### About the Custom Field (Important)

5. **Can you add a custom field `u_source_id` (string) to `kb_knowledge`?** This stores our internal RC-xxx article ID alongside the ServiceNow KB number. It gives us two benefits:
   - We can re-import updated articles later without creating duplicates (match on `u_source_id` instead of title)
   - Users and scripts can look up articles by our familiar ID scheme

   This is low-effort to add and makes every future re-import much cleaner. We'd strongly recommend doing this before the first import.

### About the Import Itself

6. **Do you use Import Sets or the Table API?** We can deliver either an Excel file (for Import Sets) or have a script POST directly to the Table API — whichever fits your workflow better.

7. **If Import Sets: do you have a transform map for `kb_knowledge` already, or do we need to build one together?** The column names in our Articles sheet match `kb_knowledge` field names to make mapping straightforward.

8. **How do you handle the article body (HTML)?** The `text` column in our sheet is pre-rendered HTML. Does your import process paste this directly into `kb_knowledge.text`, or does it need any sanitisation first?

### About Cross-Linking

9. **Does your ServiceNow instance use the native Related Articles feature on `kb_knowledge`?** If yes, we have a Relationships sheet with every cross-reference ready to go. We'd want to wire these up after the initial article import (Pass 2). Can that be scripted, or does it need to be done manually?

10. **How do you prefer to handle links within article bodies?** Once articles are in SN, references like "see RC-FD-02" in the body text could become clickable links to the actual SN article. We can script a post-import pass that swaps RC-xxx references for SN article URLs — but we need to know the URL pattern your instance uses (e.g., `https://yourinstance.service-now.com/kb_view.do?sysparm_article=KB0001234`).

---

## Suggested Import Order

1. **Admin creates `u_source_id` custom field** on `kb_knowledge`
2. **We fill in `kb_knowledge_base`** column in the Articles sheet with the correct KB name/sys_id
3. **We confirm author field** matches a valid SN user
4. **Pass 1 — Import Articles sheet** via Import Sets or Table API
5. **Admin shares the article number mapping** (RC-xxx → KB00XXXXX) after import
6. **Pass 2 — Wire up relationships** using the Relationships sheet + article number mapping

---

## Regenerating the Export

When new KB articles are written or existing ones are updated, re-run:

```
python3 kb_to_servicenow.py
```

This re-reads all `RC-*.md` files in the KB folder and produces a fresh `REDCap_KB_ServiceNow_Import.xlsx`. If `u_source_id` is in place in SN, updated articles can be re-imported cleanly by matching on that field rather than creating new records.

---

## Files in This Folder

| File | Purpose |
|---|---|
| `kb_to_servicenow.py` | The export script — run this to regenerate the import file |
| `REDCap_KB_ServiceNow_Import.xlsx` | Most recent export — ready to hand to the SN admin |
| `ServiceNow_Admin_Handoff.md` | This document |
