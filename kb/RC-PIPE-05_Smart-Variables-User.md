RC-PIPE-05

**Smart Variables: User**

| **Article ID** | RC-PIPE-05 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers |

---

# 1. Overview

User smart variables return information about the REDCap user currently interacting with the system. These variables are context-dependent, meaning they always reflect the logged-in user's data and permissions — not the participant's information. Use these variables to personalize forms, surveys, and emails based on who is accessing the project, or to route data entry tasks to specific team members based on their Data Access Group (DAG) or assigned role.

---

# 2. Key Concepts & Definitions

**User Profile**

The username, full name, and email address of the logged-in REDCap user, as configured on their Profile page. REDCap administrators can modify a user's profile information.

**Data Access Group (DAG)**

A mechanism to restrict which records a user can access and view. A DAG is identified by a unique name (for use in piping), a numeric ID, and a human-readable label. A user can belong to at most one DAG; if they are not assigned to a DAG, related smart variables return blank.

**User Role**

A custom set of permissions assigned to a user in a specific project. Roles are defined by project administrators and can restrict which instruments a user can access, whether they can edit data, whether they can export, and more. A user may be assigned to a role in one project but not another.

**Role ID vs. Role Name**

The Role ID is a numeric identifier unique across all projects in the entire REDCap installation. If a project is copied, the new project's user roles receive different Role IDs. The Role Name (also called "unique role name") is a unique identifier within the project and is preserved if the project is copied, making it suitable for use in conditional logic across project copies.

**Role Label**

The human-readable name of a role, as defined by whoever created it. This is the label users see in the interface (e.g., "Data Entry Person", "PI", "Study Coordinator").

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| User Name | `[user-name]` | The logged-in user's REDCap username. | jane_doe |
| User Full Name | `[user-fullname]` | The logged-in user's first and last name as listed on their Profile page. | Jane Doe |
| User Email | `[user-email]` | The logged-in user's primary email address as listed on their Profile page. | jane.doe@example.edu |
| User DAG Name | `[user-dag-name]` | The unique identifier of the Data Access Group to which the logged-in user belongs. Returns blank if the user is not assigned to any DAG. | site_a |
| User DAG ID | `[user-dag-id]` | The numeric ID of the DAG to which the logged-in user belongs. Returns blank if not in a DAG. | 324 |
| User DAG Label | `[user-dag-label]` | The human-readable name/label of the DAG to which the logged-in user belongs. Returns blank if not in a DAG. | Site A |
| User Role ID | `[user-role-id]` | The numeric ID of the user role assigned to the logged-in user. This ID is unique across all REDCap projects. Returns blank if the user is not assigned to a role. NOTE: Copying a project results in new Role IDs for user roles in the copy. | 127 |
| User Role Name | `[user-role-name]` | The unique name (within the current project) of the user role assigned to the logged-in user. Returns blank if not assigned to a role. NOTE: This role name is preserved when a project is copied, making it suitable for use in conditional logic. | U-699N7ET9KR |
| User Role Label | `[user-role-label]` | The human-readable label of the user role (as defined by whoever created the role). Returns blank if not assigned to a role. | Data Entry Person |

---

# 4. Usage Notes

**User vs. Participant Identity**

User smart variables always return data about the logged-in REDCap user, not the participant or subject of the record. If you need to reference participant information (such as a participant's name from a data field), use a regular field pipe reference, not a user smart variable.

**DAG Behavior**

If a user is not assigned to a DAG, `[user-dag-name]`, `[user-dag-id]`, and `[user-dag-label]` all return blank (an empty string). Plan your form labels and logic accordingly. For example, do not assume a DAG smart variable will always contain a value.

**Role Behavior**

Role smart variables behave similarly to DAG smart variables. If a user is not assigned to a role, all three role smart variables return blank. Note that role assignment is project-specific; the same user may have a role in one project but not another.

**Role ID Stability Across Project Copies**

If you copy a project that contains user roles:
- The Role IDs in the new project will be different from the originating project.
- The Role Names will be identical (preserved), so conditional logic using role names will continue to work.
- Use `[user-role-name]` (not `[user-role-id]`) in branching logic or calculations if you anticipate copying the project.

**Field Visibility and User Context**

User smart variables are particularly useful in combination with branching logic and conditional fields. For example, you could use `[user-dag-label]` in field notes to remind users which DAG they belong to, or use `[user-role-label]` to conditionally display different instructions based on the user's assigned role.

**Survey Invitation Context**

User smart variables in survey invitations and confirmation emails resolve based on the person who triggers the invitation (typically an administrator or project coordinator), not the survey respondent. This is because survey invitations are generated server-side before the participant accesses the survey.

---

# 5. Common Questions

**Q: I want to personalize a form so that it displays the current user's name. How do I do that?**

**A:** Use `[user-fullname]` in your field label, field note, or descriptive text. For example, a field label might read "Dear `[user-fullname]`, please enter your assessment results below." The variable resolves to the logged-in user's name at the time they open the form.

**Q: My project uses Data Access Groups. How can I verify that a user belongs to a specific DAG?**

**A:** Use the `[user-dag-name]` smart variable in branching logic or a calculated field. For example, you could create a branching logic rule that shows a field only if `[user-dag-name]='site_b'`. Alternatively, you can display the user's DAG label in a field note for confirmation: "You are accessing records in the `[user-dag-label]` group."

**Q: I have multiple user roles in my project. How do I use a role smart variable in conditional logic?**

**A:** Use `[user-role-name]` (not `[user-role-id]`) in your branching logic or calculated field values. Role names are preserved when a project is copied, so this ensures your logic remains valid if the project is duplicated. For example: `[user-role-name]='U-699N7ET9KR'` to show a field only for users in a specific role.

**Q: What is the difference between `[user-role-id]` and `[user-role-name]`?**

**A:** Both identify the user's assigned role, but they differ in stability across project copies. The Role ID is unique across the entire REDCap installation and changes when a project is copied. The Role Name is unique within the project and is preserved during copy, making it suitable for use in logic expressions that must work correctly after a project is duplicated. Use Role Name in your designs unless you have a specific reason to use Role ID (such as integration with external systems that track roles by ID).

**Q: My user is not in any DAG. What happens if I pipe `[user-dag-label]` into a field note?**

**A:** The smart variable returns blank, leaving an empty space in the text. To avoid confusing blank output, you can use the `:hideunderscore` modifier: `[user-dag-label:hideunderscore]`. This suppresses the default six-underscore placeholder and renders the blank invisibly instead.

**Q: Can I use user smart variables in branching logic?**

**A:** Yes. All nine user smart variables can be used in branching logic conditions. For example, `[user-dag-name]='site_a'` shows a field only for users in that DAG. However, note that branching logic is evaluated every time the form loads, so the visible fields may change if a different user accesses the same record.

---

# 6. Common Mistakes & Gotchas

**Confusing user smart variables with participant data.** `[user-fullname]` returns the name of the logged-in REDCap user, not the participant being studied. If you need the participant's name (stored in a data field), use a regular field pipe reference like `[participant_name]` instead.

**Assuming DAG and role smart variables always have values.** If a user is not assigned to a DAG or role, these smart variables return blank, not an error message. Test your designs with users who lack DAG or role assignments to ensure labels and logic behave as expected. Use conditional text or the `:hideunderscore` modifier to handle blanks gracefully.

**Using Role ID in logic when the project will be copied.** If you use `[user-role-id]` in branching logic or calculations and the project is later copied, the Role IDs in the new project will be different, breaking the logic. Use `[user-role-name]` instead to ensure logic remains valid after a copy.

**Misunderstanding survey invitation behavior with user smart variables.** In survey invitation emails, user smart variables resolve to the person who triggered the invitation (usually an administrator), not the survey respondent. Do not expect `[user-fullname]` to be the participant's name in a survey invitation; use a participant data field reference instead.

**Mixing user and participant identity in emails.** A common mistake in confirmation emails is piping `[user-email]` when you intended to use a participant email field. These are different: the user smart variable is the REDCap user's email; participant email comes from a data field.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (smart variable syntax and modifiers)
- RC-AT-06 — Action Tags: Autofill (using user smart variables with @DEFAULT and @CALCTEXT)
- RC-ALERT-01 — Alerts and Notifications Setup (using user smart variables in email alerts and notifications)
