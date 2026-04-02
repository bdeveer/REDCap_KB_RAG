RC-DE-04

**Editing Data & Audit Trail**

  -------------------- --------------------------------------------------------------------------------------------------------
  **Article ID**       RC-DE-04
  **Domain**           Data Entry
  **Applies To**       All REDCap project types
  **Prerequisite**     RC-DE-02 --- Basic Data Entry
  **Version**          1.0
  **Last Updated**     2025
  **Author**           REDCap Support
  **Related Topics**   RC-DE-01 --- Record Creation; RC-DE-02 --- Basic Data Entry; RC-DE-03 --- Longitudinal Projects & DAGs
  -------------------- --------------------------------------------------------------------------------------------------------

**1. Overview**

This article explains how to edit previously saved data in REDCap, how
to access the audit trail for individual fields, and how to edit data
that was originally entered via a survey. REDCap records a complete
history of all data changes, and that history is always accessible to
authorized users.

**2. Key Concepts & Definitions**

**Data Edit**

The act of opening a previously saved instrument, changing one or more
field values, and saving the form again. REDCap records the old and new
values as part of the audit trail automatically.

**Audit Trail (Logging)**

A complete, timestamped record of every data change made in a REDCap
project. The audit trail records who changed what, when, and from what
value to what value. It cannot be edited or deleted.

**Field History (\'H\' button)**

An inline audit view available on individual fields during data entry.
Clicking the small \'H\' icon next to a field shows a popup with the
complete change history for that specific field in that record.

**Logging Application**

A project-level application (accessible from the left-hand menu for
authorized users) that provides a searchable, filterable view of all
audit trail events across all records, instruments, and users.

**Survey Edit Right**

A user right that must be explicitly granted to allow editing of
instrument data that was originally submitted via a survey. It is off by
default. Without this right, survey-completed instruments are read-only.

**3. Editing Previously Saved Data**

**3.1 Standard Edit Workflow**

Editing data in REDCap follows the same path as entering it for the
first time:

-   Navigate to the record using Add/Edit Records, the Record Status
    Dashboard, or any Record ID link.

-   On the Record Home Page, click the dot for the instrument you want
    to edit.

-   Change the field values you need to update.

-   Save the form using any of the four save options.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** REDCap automatically logs the old and new values, the user who made the change, and the timestamp. You do not need to do anything special to trigger audit logging --- it happens on every save.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.2 What Gets Logged**

-   Every field value change is recorded, including the previous value
    and the new value.

-   The timestamp uses the REDCap server\'s local time (not the user\'s
    browser time).

-   The username of the user who made the change is always recorded.

-   Form status changes (e.g., setting a form to \'Complete\') are also
    logged.

**4. Accessing the Audit Trail**

**4.1 Field-Level History: the \'H\' Button**

-   When viewing or editing an instrument, look for a small grey \'H\'
    icon next to each field label.

-   Click the \'H\' button to open a popup showing every saved value for
    that field in that record, in chronological order.

-   Each entry in the history shows: the value, the user who saved it,
    and the timestamp.

-   The \'H\' button is always visible during data entry, regardless of
    whether any edits have been made.

**4.2 Project-Level Logging Application**

-   If you have Logging access rights, the Logging application appears
    in the left-hand menu under Applications.

-   Logging provides a full project-level audit trail. You can filter by
    record, user, instrument, event, and date range.

-   Use Logging when you need to audit multiple records or find out what
    a specific user changed across the project.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Access to the Logging application is controlled by user rights. If you do not see it in the left-hand menu, your account has not been granted Logging access. Contact your project administrator.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**5. Editing Survey-Submitted Data**

**5.1 Why Survey Editing Is Restricted**

When a participant completes an instrument as a survey, REDCap locks the
form to prevent the study team from inadvertently altering
participant-reported data. Editing survey data is treated as a special,
deliberate action that requires an explicit user right.

**5.2 Checking Whether You Have Survey Edit Rights**

-   Navigate to the survey-completed instrument. It will display as
    read-only if survey edit rights are not enabled for your account.

-   If you have survey edit rights, an \'Edit survey response\' button
    appears at the top of the form.

-   If you do not see the button and need to edit the data, contact your
    project administrator to request the Survey Edit Responses user
    right.

**5.3 Editing a Survey Response (If You Have Rights)**

-   Navigate to the survey-completed instrument.

-   Click the \'Edit survey response\' button at the top of the form.

-   Make your changes to the field values.

-   Save the form using any of the four save options. Do not navigate
    away without saving --- unsaved changes are lost.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** Editing a survey response does not notify the original survey respondent. The edit is logged in the project\'s audit trail with your username and timestamp. Document any such edits in your study\'s data management notes per your protocol SOPs.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Questions**

**Q: Does REDCap keep a record of what data looked like before I edited
it?**

A: Yes. REDCap logs every change automatically. The old value, new
value, user, and timestamp are all preserved in the audit trail. Use the
\'H\' button next to any field or the Logging application to view the
full history.

**Q: Can I undo a change after saving?**

A: Not directly. REDCap has no undo button. To revert a value, you must
manually re-enter the original value and save the form again. The audit
trail will record the revert as a separate edit.

**Q: A form was completed as a survey and now shows as read-only. How do
I edit it?**

A: You need the \'Survey Edit Responses\' user right. If you have it, an
\'Edit survey response\' button appears at the top of the form. If you
do not have this right, contact your project administrator.

**Q: I can see the \'H\' button but the history only shows one entry. Is
that normal?**

A: Yes. If the field has only been saved once, the history will show
only one entry --- the initial value. A history with one entry simply
means the field has never been edited since it was first saved.

**Q: Can I delete an individual data point rather than editing it?**

A: In most cases, you clear a field by editing the instrument and
removing the value (leaving the field blank), then saving. Some field
types (like radio buttons) have a reset option. Permanently deleting a
record requires administrative rights.

**Q: Who can see the audit trail?**

A: Users with the Logging user right can access the full project-level
audit trail via the Logging application. The field-level \'H\' button is
visible to all users who can open the instrument, regardless of Logging
rights.

**7. Common Mistakes & Gotchas**

-   Editing a survey form and forgetting to save: survey edit mode works
    like any other data entry --- you must click a save button before
    navigating away or changes are lost.

-   Expecting an undo function: REDCap has no undo. Reversion requires
    manually re-entering the previous value. The audit trail provides
    the reference for what the old value was.

-   Not documenting survey response edits: editing a survey-submitted
    response is an unusual action that may require documentation in your
    study\'s data management records. Check your protocol SOPs before
    editing.

-   Looking for the \'H\' button and not finding it: the \'H\' button is
    only visible when the instrument is open in edit or view mode. It
    does not appear on the Record Home Page or Record Status Dashboard.

-   Confusing field history with the Logging application: the \'H\'
    button shows history for one specific field in one specific record.
    The Logging application shows all changes across all fields and
    records in the project.

**8. Related Articles**

-   RC-DE-01 --- Record Creation & the Record Home Page

-   RC-DE-02 --- Basic Data Entry (prerequisite --- covers save options
    and form navigation)

-   RC-DE-03 --- Longitudinal Projects & Data Access Groups
