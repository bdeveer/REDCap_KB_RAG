RC-INTG-01

**Data Entry Trigger**

| **Article ID** | RC-INTG-01 |
|---|---|
| **Domain** | Integration |
| **Applies To** | All REDCap project types |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-DE-02 — Basic Data Entry; RC-SURV-01 — Surveys: Basics; RC-LONG-02 — Repeated Instruments & Events Setup; RC-DAG-01 — Data Access Groups; RC-CC-06 — Control Center: Modules & Services Configuration |

---

# 1. Overview

The Data Entry Trigger (DET) is an advanced project feature that sends an automatic HTTP POST request to a remote URL every time a record or survey response is created or modified in a REDCap project. Its primary purpose is to notify an external system — in real time — that data has changed, so that the external system can take some action in response. A common use case is triggering a call to the REDCap API from the remote server to retrieve or process the updated data.

**What triggers it:** Any data saved by a REDCap user on a data entry form or survey page. This includes creating a new record, saving an existing instrument, and submitting or partially saving a survey.

**What does not trigger it:** Data imports — including CSV imports, API imports, and Mobile App imports. The DET fires only on interactive data entry and survey submissions.

The DET is configured per project by entering a URL in the Data Entry Trigger field under Project Setup → Additional Customizations. Only one URL can be specified per project.

---

# 2. Key Concepts & Definitions

**HTTP POST Request**

A standard web request method in which the sending system (REDCap) transmits a set of named parameters to a receiving URL. The remote server at that URL receives and processes those parameters. The DET sends its parameters via HTTP POST each time data is saved.

**Trigger**

The event that causes REDCap to send the POST request — specifically, saving data on a data entry form or survey in the REDCap interface. The DET fires once per save action.

**Remote URL**

The web address of the external system that will receive the POST request. This can be any server or web application capable of accepting HTTP POST requests, including a custom script that then calls the REDCap API.

**POST Parameters**

The key-value pairs sent by REDCap in each POST request. They describe the context of the save action: which project, which record, which instrument, which event, and so on. See Section 4 for the full parameter reference.

**Survey Respondent**

When the DET is triggered by a survey submission (rather than by a staff user entering data on a data entry form), the username reported in the POST request is the literal string `[survey respondent]` — not a real REDCap username.

---

# 3. Configuration

## 3.0 System-Level Requirement

The Data Entry Trigger feature must be enabled at the system level by a REDCap administrator before any project can configure it. This is done in the Control Center under System Configuration → Modules/Services Configuration (see **RC-CC-06**). If the Data Entry Trigger field is not visible in Project Setup → Additional Customizations, the feature may be disabled for your installation.

## 3.1 Project-Level Setup

The Data Entry Trigger is configured at the project level:

1. Open the project and navigate to **Project Setup**.
2. Click **Additional Customizations**.
3. Locate the **Data Entry Trigger** field and enter the full URL of the remote endpoint that should receive the POST request.
4. Save the settings.

Once configured, REDCap will send a POST request to that URL automatically after every qualifying save action in the project. No further per-instrument configuration is needed — the DET applies to all instruments and surveys in the project.

> **Note:** If the URL is unreachable or returns an error, REDCap does not retry the request and does not alert the user. It is the responsibility of the receiving server to handle availability and logging.

---

# 4. POST Parameter Reference

REDCap sends the following parameters in each HTTP POST request. Parameters marked as conditional are only included under specific circumstances.

| **Parameter** | **Description** | **Conditional?** |
|---|---|---|
| `project_id` | The unique numeric ID of the REDCap project (the `pid` value visible in the project's URL). | No |
| `username` | The REDCap username of the person who triggered the save. For survey pages, this will be the string `[survey respondent]` rather than a real username. | No |
| `instrument` | The unique variable name of the instrument being saved. Instrument names are found in column B of the data dictionary. | No |
| `record` | The value of the project's first field for the record being created or modified. | No |
| `redcap_event_name` | The unique event name of the event in which the record was modified. | Longitudinal projects only |
| `redcap_data_access_group` | The unique group name of the Data Access Group (DAG) to which the record belongs, if any. | Only sent if the record belongs to a DAG |
| `[instrument]_complete` | The completion status of the instrument at the time of saving. The parameter name is the instrument's variable name followed by `_complete` (e.g., `demographics_complete`). For data entry forms: `0` = Incomplete, `1` = Unverified, `2` = Complete. For surveys: `0` = partial response, `2` = completed response. | No |
| `redcap_repeat_instance` | The instance number of the repeating event or repeating instrument being saved. | Only sent when saving a repeating event or repeating instrument |
| `redcap_repeat_instrument` | The unique instrument name of the repeating instrument being saved. Not sent for repeating events — only for repeating instruments. | Only sent when saving a repeating instrument |
| `redcap_url` | The base URL of the REDCap installation (the URL of REDCap's home page). Example: `https://your-institution.edu/redcap/` | No |
| `project_url` | The URL of the project's home page. Example: `https://your-institution.edu/redcap/redcap_vXX.X.X/index.php?pid=XXXX` | No |

---

# 5. Security Considerations

**Use HTTPS for sensitive record identifiers.** If the values stored in your project's first field (the Record ID field) are considered identifiers — such as a medical record number, social security number, or participant name — it is strongly recommended to use an SSL/HTTPS-secured URL for the DET endpoint. The record identifier is transmitted in plaintext in each POST request. An unencrypted HTTP connection exposes this value in transit.

**Validate the source of incoming requests.** The DET POST request can, in principle, originate from any network actor with knowledge of your endpoint's URL. The receiving server should validate that incoming requests are genuine — for example, by checking the `project_id` and `redcap_url` values against expected values, or by using a shared secret embedded in the endpoint URL.

**Protect the endpoint URL.** The DET URL is visible to anyone with access to the project's Additional Customizations settings, which typically requires administrator-level access. Treat the endpoint URL as sensitive if it contains any embedded secrets or tokens.

---

# 6. Common Questions

**Q: Will the DET fire when I import data using the REDCap API or a CSV import?**

**A:** No. The DET is triggered only by interactive data entry on REDCap forms and surveys. Imports via the API, CSV upload, and the Mobile App do not trigger it.

**Q: The DET fires on every instrument save. Can I restrict it to a specific instrument or event?**

**A:** Not natively. REDCap sends the POST request for every save action across all instruments and events in the project. The receiving server must use the `instrument` and `redcap_event_name` parameters to filter and act only on the saves it cares about.

**Q: Will the username always be a real REDCap user?**

**A:** No. When the trigger is fired by a survey submission, the `username` parameter will contain the string `[survey respondent]` instead of a real REDCap username.

**Q: Are the `redcap_repeat_instance` and `redcap_repeat_instrument` parameters always present?**

**A:** No. `redcap_repeat_instance` is only sent when the project has repeating events or instruments and the current save is on a repeating element. `redcap_repeat_instrument` is only sent for repeating instruments — it is not sent for repeating events. The receiving server should not assume these parameters are present.

**Q: What happens if the remote server is unavailable when the DET fires?**

**A:** REDCap sends the POST request and does not wait for a successful response. If the remote server is down or returns an error, the request is lost — REDCap does not queue or retry it. There is also no error displayed to the REDCap user. Logging and retry logic must be implemented on the receiving server side.

**Q: Can I configure more than one DET URL for a project?**

**A:** No. Only one URL can be entered in the Data Entry Trigger field. If you need to notify multiple endpoints, the receiving server must fan out the request to additional systems after receiving it.

---

# 7. Common Mistakes & Gotchas

**Expecting the DET to fire on imports.** A common misunderstanding is that the DET will fire on all data changes, including API and CSV imports. It only fires on interactive saves via the REDCap interface. If your integration depends on knowing about imported data, the DET alone is insufficient — consider polling the REDCap API on a schedule instead.

**Not handling missing conditional parameters.** The `redcap_event_name`, `redcap_data_access_group`, `redcap_repeat_instance`, and `redcap_repeat_instrument` parameters are not always present. Code that expects them unconditionally will fail when they are absent. Always check for the presence of a parameter before using its value.

**Using an HTTP (non-SSL) URL with identifiable record IDs.** If the Record ID field contains any personally identifiable or sensitive value and the DET URL is HTTP rather than HTTPS, that value is transmitted unencrypted over the network with every save. Always use HTTPS when record identifiers could be considered sensitive.

**Assuming REDCap will retry on failure.** REDCap makes one attempt to deliver the POST request. If the receiving server is unavailable, the notification is lost with no retry and no alert to the user or administrator. Design the receiving endpoint to be robust and implement your own logging.

**Confusing `instrument` with the instrument's label.** The `instrument` parameter contains the instrument's unique variable name (as found in column B of the data dictionary), not its human-readable label. These are often different, especially if the instrument was renamed after creation.

---

# 8. Related Articles

- RC-DE-02 — Basic Data Entry (foundational — covers the data entry workflow that triggers the DET)
- RC-SURV-01 — Surveys: Basics (surveys are a common DET trigger source; explains survey completion status)
- RC-LONG-02 — Repeated Instruments & Events Setup (required reading if your project uses repeating elements; explains `redcap_repeat_instance` and `redcap_repeat_instrument` context)
- RC-DAG-01 — Data Access Groups (explains `redcap_data_access_group` and how DAGs are assigned to records)
- RC-CC-06 — Control Center: Modules & Services Configuration (system-level Data Entry Trigger enable/disable)
