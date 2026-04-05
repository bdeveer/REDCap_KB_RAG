RC-AT-12

**Action Tags — HIDESUBMIT Action Tags (External Module)**

| **Article ID** | RC-AT-12 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | Projects on REDCap instances where the HIDESUBMIT Action Tags External Module is installed and enabled |
| **Prerequisite** | RC-AT-01 — Action Tags Overview; HIDESUBMIT Action Tags External Module must be enabled for the project |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-08 — @IF |

---

# 1. Overview

> ⚠️ **External Module required.** The action tags documented in this article are **not part of vanilla REDCap**. They are provided by the **HIDESUBMIT Action Tags** External Module (v3.1.0). These tags will only appear in your project's action tag list and will only function if this module has been installed on your REDCap instance and enabled for your project. Contact your REDCap administrator if you need this module enabled.

The HIDESUBMIT Action Tags module adds nine action tags that conditionally hide save and submit buttons on data entry forms and survey pages based on branching-logic-style conditions. This allows project designers to prevent users from saving or submitting a form unless specific data conditions are met — without writing custom code or JavaScript.

---

# 2. How These Tags Work

All HIDESUBMIT tags share the same activation mechanism: the button is hidden **if the tagged field is visible due to branching logic**. This means you do not configure a condition directly in the action tag — instead, you control the behavior by attaching branching logic to the field that carries the action tag.

**Pattern:**
1. Create a field (typically hidden or descriptive) and give it branching logic that reflects the condition under which you want to hide the button.
2. Add the appropriate HIDESUBMIT action tag to that field.
3. When the field becomes visible (i.e., the branching logic condition is true), the corresponding button is hidden.

---

# 3. Tag Reference

## 3.1 Tags That Hide All Save/Submit Buttons

### @HIDESUBMIT

Hides **all save buttons** on data entry forms and both the **Submit/Next Page button** and the **"Take this survey again" button** on surveys — when the tagged field is visible due to branching logic.

```
@HIDESUBMIT
```

### @HIDESUBMIT-FORM

Same as `@HIDESUBMIT` but applies to **data entry forms only**.

```
@HIDESUBMIT-FORM
```

### @HIDESUBMIT-SURVEY

Same as `@HIDESUBMIT` but applies to **survey pages only** — hides the Submit/Next Page button and the "Take this survey again" button.

```
@HIDESUBMIT-SURVEY
```

---

## 3.2 Tags That Hide Submit-Only Buttons (Preserving "Add New Instance")

### @HIDESUBMITONLY

Hides all save buttons on data entry forms **except** "Save & Add New Instance", and hides the Submit/Next Page button on surveys — when the tagged field is visible due to branching logic.

```
@HIDESUBMITONLY
```

### @HIDESUBMITONLY-FORM

Same as `@HIDESUBMITONLY` but applies to **data entry forms only** — hides all save buttons except "Save & Go To Next Instance".

```
@HIDESUBMITONLY-FORM
```

### @HIDESUBMITONLY-SURVEY

Same as `@HIDESUBMITONLY` but applies to **survey pages only** — hides the Submit/Next Page button.

```
@HIDESUBMITONLY-SURVEY
```

---

## 3.3 Tags That Hide the Repeat Instance Button

### @HIDEREPEAT

Hides the **"Save & Go To Next Instance"** button on data entry forms and the **"Take this survey again"** button on surveys — when the tagged field is visible due to branching logic.

```
@HIDEREPEAT
```

### @HIDEREPEAT-FORM

Same as `@HIDEREPEAT` but applies to **data entry forms only** — hides the "Save & Go To Next Instance" button.

```
@HIDEREPEAT-FORM
```

### @HIDEREPEAT-SURVEY

Same as `@HIDEREPEAT` but applies to **survey pages only** — hides the "Take this survey again" button.

```
@HIDEREPEAT-SURVEY
```

---

# 4. Tag Summary Table

| Tag | Hides on Forms | Hides on Surveys |
|---|---|---|
| `@HIDESUBMIT` | All save buttons | Submit/Next Page + Take again |
| `@HIDESUBMIT-FORM` | All save buttons | — |
| `@HIDESUBMIT-SURVEY` | — | Submit/Next Page + Take again |
| `@HIDESUBMITONLY` | All save buttons except Save & Add New Instance | Submit/Next Page |
| `@HIDESUBMITONLY-FORM` | All save buttons except Save & Go To Next Instance | — |
| `@HIDESUBMITONLY-SURVEY` | — | Submit/Next Page |
| `@HIDEREPEAT` | Save & Go To Next Instance | Take this survey again |
| `@HIDEREPEAT-FORM` | Save & Go To Next Instance | — |
| `@HIDEREPEAT-SURVEY` | — | Take this survey again |

---

# 5. Example Usage

**Scenario:** Prevent survey submission unless a required agreement field is checked.

1. Create a checkbox field `agreement_check` with one option (coded `1`): "I agree."
2. Create a hidden helper field `block_submit` with branching logic: `[agreement_check(1)] <> '1'` (the field is visible when the checkbox is NOT checked).
3. Add `@HIDESUBMIT-SURVEY` to the `block_submit` field.

Result: The Submit button is hidden until the agreement checkbox is checked.

---

# 6. Common Questions

**Q: Will these tags appear in the action tag reference popup inside my project?**

**A:** Only if the HIDESUBMIT Action Tags External Module is installed on your REDCap instance and enabled for your project. If the module is not active, the tags do not appear and will have no effect if manually typed into a field.

**Q: Can I verify whether the module is enabled for my project?**

**A:** Yes. Navigate to **Project Setup → External Modules** to see which modules are currently enabled for the project. If HIDESUBMIT Action Tags does not appear there, contact your REDCap administrator.

**Q: Can these tags be combined with @IF?**

**A:** Yes. Because the hide behavior is driven by the field's branching logic visibility, and `@IF` is an independent action tag evaluation, combining them is possible but requires careful design to avoid unexpected interactions.

---

# 7. Common Mistakes & Gotchas

**Expecting these tags to work without the module enabled.** HIDESUBMIT action tags are silently ignored on any REDCap instance or project where the External Module is not installed and active. If the buttons are not hiding as expected, confirm the module is enabled.

**Confusing the activation mechanism.** The button is hidden when the tagged field is **visible** (branching logic is true), not when a parameter evaluates to true. The condition logic lives in the field's branching logic, not in the action tag itself.

**Using @HIDESUBMIT on a field that is always visible.** If the tagged field has no branching logic (or branching logic that is always true), the button will always be hidden. Ensure the branching logic correctly reflects when hiding is desired.

---

# 8. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and the distinction between native and External Module tags
- RC-AT-08 — @IF: native conditional action tag logic (no External Module required)
- RC-BL-01 — Branching Logic Overview: branching logic controls when HIDESUBMIT tags activate
