RC-API-01

**REDCap API**

| **Article ID** | RC-API-01 |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Prerequisite** | RC-USER-03 — User Rights: Configuring User Privileges |
| **Version** | 1.3 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Source** | REDCap API v16.1.3 official documentation |
| **Related Topics** | RC-INTG-01 — Data Entry Trigger; RC-EXPRT-01 — Data Export Overview; RC-IMP-01 — Data Import Overview; RC-USER-03 — User Rights: Configuring User Privileges |

---

# 1. Overview

The REDCap API (Application Programming Interface) allows external applications to connect to REDCap remotely and interact with it programmatically — importing or exporting records, retrieving project configuration, managing files, and more. Instead of a person clicking through the REDCap interface, a program sends structured requests to REDCap over HTTP (the same protocol browsers use to load web pages) and REDCap responds with the requested data or confirmation of the action taken.

Common use cases include automated nightly data pulls into a statistical analysis environment, populating REDCap records from an external clinical system, and building custom dashboards or integrations that read from or write to REDCap without manual steps. Programmers can use the API to build applications, websites, scripts, and automated workflows that interact with REDCap directly.

Access to the API requires both a user right assignment and a project-specific API token. All API tokens are scoped to the access level of the user they belong to — the API cannot grant broader access than the user has in the REDCap interface.

---

# 2. Key Concepts & Definitions

**API (Application Programming Interface)**

A defined, standardized way for software programs to communicate with each other. The REDCap API defines a set of methods — specific request types — that external programs can call to read from or write to REDCap.

**API Token**

A unique, project-specific authentication key assigned to a REDCap user. The token is included in every API request in place of a username and password. Tokens are per-user and per-project: a user who is in five projects needs five separate tokens. Tokens inherit the requesting user's access rights — an export token cannot retrieve data the user cannot see in the interface.

**API Method (Endpoint)**

A specific action the API can perform, such as "Export Records" or "Import Data Dictionary." Each method specifies what parameters it accepts and what it returns. The full list of supported methods is available in the API Playground and in the API documentation page linked from each project.

**HTTP POST**

The network request type used by the REDCap API for all methods. Both data imports and data exports use POST requests — the method type (import vs. export) is specified as a parameter within the request body, not by the HTTP verb.

**API Playground**

A built-in REDCap tool, accessible from every project's left-hand menu, that lets users explore API methods interactively and generate sample code without writing any code themselves. The Playground is the recommended starting point for anyone new to the REDCap API.

**Format**

The data format the API uses to deliver or receive data. The three main formats are JSON (JavaScript Object Notation — the default for most methods and easiest to work with in modern languages), CSV (comma-separated, compatible with spreadsheets and R), and XML (includes the CDISC ODM flavor, which can be re-imported into REDCap or other EDC systems).

**API Export Right / API Import Right**

Two separate user rights that control API access. API Export allows programmatic data export; API Import allows programmatic data import and other write operations. A user can hold one or both. Both must be granted by a project administrator on the User Rights page before an API token can be requested.

**Super API Token**

A special token required to use the **Create Project** API method. Super tokens are 64 characters long (regular tokens are 32 characters). Each REDCap user can hold at most one super token. Super tokens must be requested from your REDCap administrator and are granted only to users who need to create projects programmatically.

---

# 3. Requesting and Managing API Access

## 3.1 Prerequisites

Before requesting a token:

1. Confirm that API access is enabled at the system level — contact your REDCap administrator if you are unsure.
2. Verify that you have been granted the **API Export** and/or **API Import** user right in the project (User Rights → your user → API section).

## 3.2 Requesting a Token

1. Open the project and click **API** in the Applications section of the left-hand menu.
2. On the API page, click **Request API Token** to submit a request to your REDCap administrator.
3. Once approved, your token is displayed on the same API page. Copy it and store it securely — treat it like a password.

> **Note:** If you do not see an **API** link in the left-hand menu, you have not been granted API privileges for that project. Ask a project administrator to assign the API Export and/or API Import user right to your account via the User Rights page.

> **Yale-specific:** [Describe local token approval process and expected turnaround time — leave blank until confirmed with Yale REDCap support team]

## 3.3 Token Security

- **Never share your token.** Anyone with your token has the same access to that project's data as you do.
- **Never include your token in code that is stored in a public repository** (e.g., GitHub). Use environment variables or a secrets manager instead.
- **Use HTTPS.** Always send API requests to the HTTPS version of your REDCap URL. Sending tokens over plain HTTP exposes them in transit.
- If you believe a token has been compromised, contact your REDCap administrator to have it revoked and regenerated.

## 3.4 Multiple Tokens

Each user gets one token per project. If you need API access to three projects, you need three tokens — one from each project's API page. Token requests are submitted and managed independently per project.

## 3.5 SSL Certificate Validation

Although REDCap API requests use HTTPS (SSL), which encrypts traffic between your script and the REDCap server, there is an additional step that is **highly recommended** for any API script handling sensitive data: validating the REDCap server's SSL certificate.

**Why this matters — Man-in-the-Middle attacks**

SSL certificates allow a server's identity to be verified before encrypted communication begins. Even over HTTPS, a Man-in-the-Middle (MiM) attack is theoretically possible: a malicious actor impersonates the REDCap server using a fake SSL certificate. If your script does not validate the certificate, it may unknowingly send the request — including your API token — to the attacker instead of REDCap. The attacker can then use your token to make API requests as if they were you.

**How to prevent it**

Force your API script to validate REDCap's SSL certificate before sending any request. REDCap's certificate will always be valid; a fake certificate cannot pass validation. In most programming languages and HTTP libraries, this is a single setting:

- **cURL** (used by PHP, R, SAS, and many others): set `CURLOPT_SSL_VERIFYPEER` to `TRUE`.
- **Other languages**: search for your language + "verify SSL certificate" (e.g., "Python verify SSL certificate") to find the equivalent setting. Most modern HTTP libraries enable this by default — verify that it has not been disabled in your code.

> **Important:** While REDCap has many built-in security layers, it is your responsibility to ensure that your API scripts follow secure practices. Validating the SSL certificate is one of the most effective steps you can take to protect your data and your token.

---

# 4. Available API Methods

The REDCap API organizes its functionality into method groups. The methods available to a given token depend on the user's rights and the project's configuration.

## 4.1 Records

| Method | Description |
|---|---|
| Export Records | Retrieve some or all records, with optional filtering by form, event, field, or DAG |
| Import Records | Add new records or update existing ones |
| Delete Records | Permanently remove records from the project |
| Rename Record | Change a record's ID value |
| Generate Next Record Name | Retrieve the next auto-number value REDCap would assign |

## 4.2 Project Metadata and Configuration

| Method | Description |
|---|---|
| Export Project Info | Retrieve project-level settings (title, purpose, dates, etc.) |
| Export Metadata (Data Dictionary) | Retrieve the full data dictionary in CSV or JSON |
| Import Metadata (Data Dictionary) | Push a modified data dictionary back to REDCap |
| Export Instruments | List instruments with their labels |
| Export Instrument-Event Mappings | Retrieve which instruments are assigned to which events (longitudinal projects) |
| Import Instrument-Event Mappings | Update instrument-event assignments |
| Export Events | List all events (longitudinal projects) |
| Import Events | Add or modify events |
| Delete Events | Remove events |
| Export Arms | List all arms (longitudinal projects) |
| Import Arms | Add or modify arms |
| Delete Arms | Remove arms |

## 4.3 Users and Access

| Method | Description |
|---|---|
| Export Users | List all project users and their rights |
| Import Users | Add users to the project or update their rights |
| Delete Users | Remove users from the project |
| Export User Roles | List all user roles |
| Import User Roles | Create or update user roles |
| Delete User Roles | Remove roles |
| Export User-Role Assignments | See which users are in which roles |
| Import User-Role Assignments | Update role assignments |
| Export DAGs | List all Data Access Groups |
| Import DAGs | Create or update DAGs |
| Delete DAGs | Remove DAGs |
| Export DAG Assignments | See which users are assigned to which DAGs |
| Import DAG Assignments | Update DAG user assignments |

## 4.4 Files

| Method | Description |
|---|---|
| Export File | Download a file attached to a file-upload field for a specific record |
| Import File | Upload a file to a file-upload field for a specific record |
| Delete File | Remove a file from a file-upload field |
| Export PDF | Generate and download a PDF of an instrument or all instruments for a record |

## 4.5 Reports and Logging

| Method | Description |
|---|---|
| Export Reports | Pull data from a saved REDCap report by report ID, respecting the report's field and filter settings |
| Export Logging | Retrieve the project audit log entries |

## 4.6 Surveys

| Method | Description |
|---|---|
| Export Survey Participant List | List participants (participant list surveys) |
| Export Survey Link | Generate a unique survey link for a specific record |
| Export Survey Queue Link | Get the survey queue link for a specific record |
| Export Survey Return Code | Get the return code for a partially completed survey |

---

# 5. Using the API Playground

The API Playground is the best place to start with the REDCap API. It requires no programming setup and provides an interactive, guided way to test any API method.

**Accessing the Playground:** Open your project and click **API** in the left-hand menu (under Applications). The Playground opens with a list of all available methods on the left.

**How the Playground works:**

1. Select a method (e.g., "Export Records").
2. Fill in the parameters using the form fields provided — the Playground explains each parameter inline.
3. Click **Execute** to run the request and see the raw response.
4. Switch to the **Code** tab to see ready-to-copy sample code in PHP, Python, R, Ruby, Java, cURL, or Perl.

The Playground uses your existing token automatically, so you can run real requests against real project data to verify what the API returns before writing a script.

> **Note:** Requests executed through the Playground are real — they affect live project data. Use a test project or development environment when testing import or delete methods.

---

# 6. Export Data Formats

When exporting records or reports, you can specify the format and type of returned data:

**Format options:**
- **JSON** — Default. Easily consumed by Python, R (via jsonlite), and most modern programming languages.
- **CSV** — Flat text file, compatible with Excel, R (via read.csv), and SAS. Familiar format for analysts who use manual exports.
- **XML** — Available as standard XML or as CDISC ODM, which includes full metadata and can be re-imported into REDCap or other EDC systems.

**Type options (for record export):**
- **flat** — One row per record (classic projects) or one row per record-event combination (longitudinal).
- **eav** — Entity-Attribute-Value format. One row per field value. Useful for sparse data or when building generic processing pipelines.

**Label vs. raw values:**
By default, REDCap exports coded values (e.g., `1`, `2`, `3` for a dropdown). Setting `rawOrLabel=label` returns the text labels instead. Setting `rawOrLabelHeaders=label` returns human-readable column headers rather than field variable names.

---

# 7. HTTP Status Codes & Error Handling

## 7.1 HTTP Status Codes

Every API response includes an HTTP status code indicating whether the request succeeded or failed. Checking this code is the first step in debugging a failed request.

| Code | Meaning | What it indicates |
|---|---|---|
| 200 | OK | Request succeeded. |
| 400 | Bad Request | The request was invalid. An accompanying message explains why. |
| 401 | Unauthorized | The API token was missing or incorrect. |
| 403 | Forbidden | Your account does not have permission to use the API for this project. |
| 404 | Not Found | The URL is invalid or the requested resource does not exist. |
| 406 | Not Acceptable | The data being imported was formatted incorrectly. |
| 500 | Internal Server Error | REDCap encountered an error processing your request. |
| 501 | Not Implemented | The requested method is not supported. |

## 7.2 Error Message Format

When an API request fails, REDCap returns the error message in the same format you specified using the `returnFormat` parameter. If no format was specified, REDCap uses its default format. For example, an error from an XML request looks like:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<hash>
  <error>detailed error message</error>
</hash>
```

JSON and CSV requests return errors in their respective formats. Always log or surface the full response body when debugging — the error message text typically identifies the exact problem (e.g., invalid parameter name, field not found, insufficient rights).

---

# 8. Common Questions

**Q: Do I need a separate token for each project?**

**A:** Yes. API tokens are scoped to a single project. Each project you need API access to requires its own token request and administrator approval. There is no single token that works across all projects (except administrator super tokens, which are not available to regular users).

**Q: What data can my API token access?**

**A:** Only what your REDCap user account can access. If you have restricted DAG access, your token can only see records in your DAG. If you lack rights to a specific instrument, the API will not return its fields. Tokens do not elevate or bypass your user rights.

**Q: Can the API trigger the Data Entry Trigger (DET)?**

**A:** No. The DET fires only on interactive data entry — saves made by a user on a REDCap form or survey. Data imported via the API does not trigger the DET. See RC-INTG-01 — Data Entry Trigger for details.

**Q: I requested a token but don't see it on the API page. What's wrong?**

**A:** Token requests require administrator approval and do not appear until approved. If the request has been pending for longer than expected, contact your REDCap administrator. Also verify that you have the API Export or API Import user right assigned — without a user right, the API page will not display a token field.

**Q: Can I use the API in a project that is in Production?**

**A:** Yes. The API works in all project statuses. Metadata import (uploading a modified data dictionary) in a Production project is subject to the same draft-mode review and approval process as any other design change.

**Q: How do I export data from a specific instrument only?**

**A:** Use the `forms` parameter in the Export Records method. Pass the instrument's variable name (not its label) to limit the export to fields on that instrument. Multiple instruments can be listed.

**Q: What is the difference between the Export Records and Export Reports methods?**

**A:** Export Records pulls data directly from the project's full record set, with parameters to control which fields, events, records, and DAGs are included. Export Reports runs a pre-defined saved report by its report ID, using the field selection, filtering, and ordering that was configured when the report was built. Both return record-level data; the report method is easier to use when a researcher has already set up a report that matches the data subset they need.

**Q: Is there a limit on how many records or how much data I can pull at once?**

**A:** There is no hard row limit documented for standard API exports, but very large datasets can time out or cause performance issues. For large projects, it is best practice to paginate exports using the `records` or `events` parameters to pull data in batches rather than all at once.

---

# 9. Common Mistakes & Gotchas

**Storing the token in version-controlled code.** A token hardcoded in a script that gets committed to GitHub is effectively public. Always store tokens as environment variables or in a credentials file excluded from version control. Treat token leaks as a security incident and request revocation immediately.

**Forgetting that the API returns coded values, not labels.** By default, the export returns raw coded values (`1`, `0`, `2`) for dropdown, radio, and checkbox fields — not the labels that display in the interface. If your downstream analysis expects text labels, add `rawOrLabel=label` to the request. Forgetting this leads to mysterious numeric columns in exported data.

**Assuming export includes all fields by default.** The Export Records method returns all fields when no field list is specified, but includes all events in longitudinal projects regardless of instrument-event assignment. In large longitudinal projects, this can produce very wide, sparse output. Always specify `forms`, `fields`, or `events` parameters to limit the export to what you actually need.

**Using an HTTP URL instead of HTTPS.** API tokens are transmitted in the request body. Sending a request to an HTTP URL exposes the token to anyone who can observe the network traffic. Always verify your REDCap instance URL begins with `https://`.

**Expecting the API to fire alerts or ASIs.** Alerts & Notifications and Automated Survey Invitations are triggered by data entry and certain field value conditions — but API imports do not reliably trigger ASIs the same way manual data entry does. Test thoroughly before building a workflow that depends on ASIs firing after an API import. Alerts are also not triggered by API imports in the same way.

**Confusing `instrument` (variable name) with the instrument's label.** API parameters that reference instruments — such as the `forms` parameter in Export Records — require the instrument's unique variable name (e.g., `demographics`), not its display label (e.g., `Demographics`). The variable name is found in the Online Designer or data dictionary. These often match, but not always, especially if an instrument was renamed after creation.

**Not handling repeating instrument data correctly.** When exporting from a project with repeating instruments or events, each instance appears as a separate row identified by `redcap_repeat_instrument` and `redcap_repeat_instance`. Code that assumes one row per record will produce incorrect results. Always inspect the structure of export output from repeating projects before building a processing pipeline.

---

# 10. Related Articles

- RC-INTG-01 — Data Entry Trigger (separate mechanism for real-time notification of data changes to external systems; does not fire on API imports)
- RC-EXPRT-01 — Data Export Overview (manual export workflow; for comparison with API-based export)
- RC-IMP-01 — Data Import Overview (manual import methods; API import is the programmatic equivalent)
- RC-USER-03 — User Rights: Configuring User Privileges (where API Export and API Import rights are granted)
- RC-DAG-01 — Data Access Groups (DAG-scoped access applies equally to API tokens)
- RC-LONG-02 — Repeated Instruments & Events Setup (essential background for working with repeating data via the API)
