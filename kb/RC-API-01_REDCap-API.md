

**REDCap API**

| **Article ID** | [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
|---|---|
| **Domain** | API |
| **Applies To** | All REDCap projects |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured. API core behaviour (tokens, rights, formats, errors, rate limiting) checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS). API import rights checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| **Version** | 1.6 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Source** | REDCap API v16.1.3 official documentation |
| **Related Topics** | [RC-INTG-01 — Data Entry Trigger](RC-INTG-01_Data-Entry-Trigger.md); [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md); [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md); [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) |
| **Synonyms** | how do i get started with the redcap api; what is an api token and how do i get one; redcap api overview and authentication; connect an external application to redcap programmatically; api user rights and token requirements; how does the redcap api work over http; enable api access for a project; introduction to redcap api methods; redcap api http error codes and ip rate limit ban |

---

## 1. Overview

The REDCap API (Application Programming Interface) allows external applications to connect to REDCap remotely and interact with it programmatically — importing or exporting records, retrieving project configuration, managing files, and more. Instead of a person working through the REDCap interface, a program sends structured requests to REDCap over HTTP (the same protocol browsers use to load web pages) and REDCap responds with the requested data or confirmation of the action taken.

Common use cases include automated nightly data pulls into a statistical analysis environment, populating REDCap records from an external clinical system, and building custom dashboards or integrations that read from or write to REDCap without manual steps. Programmers can use the API to build applications, websites, scripts, and automated workflows that interact with REDCap directly.

Access to the API requires both a user right assignment and a project-specific API token. For exports, a token is scoped to the access level of the user it belongs to and cannot return more than the user could export in the REDCap interface. **Imports are not scoped the same way:** with **API Import/Update**, a token can write to any instrument, including ones the user can only view or cannot see, and can create records without the **Create Records** right; DAG restrictions and record locking still apply. Grant API Import/Update only to users who may edit every instrument. There is one important export exception: a user with the **Mobile App** right gets full data access through the app's API calls whatever their data export rights (see §9a). REDCap administrators are not limited by project rights at all.

---

## 2. Key Concepts & Definitions

**API (Application Programming Interface)**

A defined, standardized way for software programs to communicate with each other. The REDCap API defines a set of methods — specific request types — that external programs can call to read from or write to REDCap.

**API Token**

A unique, project-specific authentication key assigned to a REDCap user. The token is included in every API request in place of a username and password. Tokens are per-user and per-project: a user who is in five projects needs five separate tokens. A project token is 32 characters long. Tokens inherit the requesting user's access rights, and REDCap checks those rights afresh on every call, so a rights change takes effect on the next request. Which fields a call returns follows the user's **data export** rights for each instrument, not their data viewing rights — an instrument set to **No Access** for export is left out of API exports even if the user can view it on screen. The Mobile App right is the exception noted in §9a.

**API Method (Endpoint)**

A specific action the API can perform, such as "Export Records" or "Import Data Dictionary." Each method specifies what parameters it accepts and what it returns. The full list of supported methods is available in the API Playground and in the API documentation page linked from each project.

**HTTP POST**

The network request type used by the REDCap API for all methods. Both data imports and data exports use POST requests — the method type (import vs. export) is specified as a parameter within the request body, not by the HTTP verb.

**API Playground**

A built-in REDCap tool, linked from the project's left-hand menu when the API is enabled and you hold an API right in the project, that lets users explore API methods interactively and generate sample code without writing any code themselves. The Playground is the recommended starting point for anyone new to the REDCap API.

**Format**

The data format the API uses to deliver or receive data. The three main formats are JSON (JavaScript Object Notation — easiest to work with in modern languages), CSV (comma-separated, compatible with spreadsheets and R), and XML (the format returned when `format` is omitted, and the basis of the CDISC ODM flavor, which can be re-imported into REDCap or other EDC systems). Always set `format` explicitly: the default is XML, which is rarely what a modern client expects.

**API Export Right / API Import Right**

Two separate user rights that control API access. **API Export** allows programmatic data export; **API Import/Update** (called API Import in this article) allows programmatic data import and other write operations. A user can hold one or both. A third right, **External Modules API**, controls only whether the token can call API methods provided by External Modules. At least one of these rights must be granted on the User Rights page (by someone with the User Rights privilege) before the API and API Playground links appear and a token can be requested.

**Super API Token**

A special token required to use the **Create Project** API method. Super tokens are 64 characters long (regular tokens are 32 characters). Each REDCap user can hold at most one super token. A super token works only with Create Project (and Export REDCap Version); it cannot be used in place of a project token for any project-level method. Only a REDCap administrator can create one, and an administrator can give one to any user, so ask your administrator if you need to create projects programmatically. Create Project returns the new project's own token in its response.

---

## 3. Requesting and Managing API Access

### 3.1 Prerequisites

Before requesting a token:

1. Confirm that API access is enabled at the system level — the REDCap API must be enabled by an administrator in the Control Center (System Configuration → Modules/Services Configuration — see **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)**). If the API link is missing from the project menu entirely, the API may be disabled instance-wide.
2. Verify that you have been granted the **API Export** and/or **API Import/Update** user right in the project (User Rights → your user → API section). Either one is enough to get a token.

### 3.2 Requesting a Token

1. Open the project and select **API** in the Applications section of the left-hand menu.
2. On the API page, select **Request API token** (or **Create API token now** / **Generate API token** if you are allowed to create one yourself).
3. Your token is displayed on the same API page once it exists. Copy it and store it securely — treat it like a password.

Whether step 2 needs approval depends on the Control Center setting **Allow normal users to auto-generate API tokens for their projects?**:

| Setting | What happens |
|---|---|
| No — an administrator must approve | The request goes to the administrators' To-Do List and by email. You receive an email when it is approved. |
| **Yes, allow ALL users to generate API tokens on their own** | The token is created immediately. |
| **Yes, allow SELECTED users to generate API tokens on their own** | Users given this privilege on their account create tokens immediately; everyone else requests approval. |

REDCap administrators can always create their own tokens without approval.

> **Institution-specific:** Which of these options is set varies by installation. Check with your REDCap administrators whether token requests need approval and how long approval usually takes.

> **Note:** If you do not see an **API** link in the left-hand menu, either the API is disabled on your instance or you have not been granted an API right in that project. Ask someone with the User Rights privilege to assign the API Export and/or API Import/Update right to your account via the User Rights page.

### 3.3 Token Security

- **Never share your token.** Anyone with your token has the same access to that project's data as you do.
- **Never include your token in code that is stored in a public repository** (e.g., GitHub). Use environment variables or a secrets manager instead.
- **Use HTTPS.** Always send API requests to the HTTPS version of your REDCap URL. Sending tokens over plain HTTP exposes them in transit.
- If you believe a token has been compromised, regenerate or delete it yourself on the project's API page — the old token stops working at once. Your REDCap administrator can also revoke or regenerate it from the Control Center, and should be told about the possible leak.

> **From 17.0.7 the token is masked on screen.** The project API page no longer displays your token in plain text on load — select the unmasking button beside it to reveal it. This mainly protects against shoulder-surfing and against tokens appearing in screenshots and screen-shares, which is a common accidental disclosure route. Note that [RC-PROF-01 — My Profile: User Profile Settings](RC-PROF-01_My-Profile-User-Profile-Settings.md) warns separately about API tokens appearing in profile screenshots.

### 3.3a Call the API at the Non-Versioned URL

Always call the API at the instance's stable endpoint:

```
https://redcap.example.edu/api/index.php
```

**not** at a path containing the version directory, such as `https://redcap.example.edu/redcap_v17.4.1/API/index.php`.

> **Version caveat (16.1.5 Standard and higher):** REDCap **rejects** survey and API calls whose URL contains a version directory, returning an error. Any integration, script or saved request still using a versioned URL breaks the moment the instance reaches 16.1.5 — and the failure looks like an API fault rather than a URL problem, because the endpoint plainly exists. The change is pre-emptive hardening; REDCap noted no known vulnerabilities at those endpoints at the time. See [RC-INFRA-01 — Self-Hosting a Private REDCap Instance](RC-INFRA-01_Self-Hosting-a-Private-REDCap-Instance.md) §4a.4.

A versioned URL also breaks on every upgrade regardless, since the directory name changes. There is no reason to use one.

### 3.4 Multiple Tokens

Each user gets one token per project. If you need API access to three projects, you need three tokens — one from each project's API page. Token requests are submitted and managed independently per project.

### 3.5 SSL Certificate Validation

Although REDCap API requests use HTTPS (SSL), which encrypts traffic between your script and the REDCap server, there is an additional step that is **highly recommended** for any API script handling sensitive data: validating the REDCap server's SSL certificate.

**Why this matters — Man-in-the-Middle attacks**

SSL certificates allow a server's identity to be verified before encrypted communication begins. Even over HTTPS, a Man-in-the-Middle (MiM) attack is theoretically possible: a malicious actor impersonates the REDCap server using a fake SSL certificate. If your script does not validate the certificate, it may unknowingly send the request — including your API token — to the attacker instead of REDCap. The attacker can then use your token to make API requests as if they were you.

**How to prevent it**

Force your API script to validate REDCap's SSL certificate before sending any request. REDCap's certificate will always be valid; a fake certificate cannot pass validation. In most programming languages and HTTP libraries, this is a single setting:

- **cURL** (used by PHP, R, SAS, and many others): set `CURLOPT_SSL_VERIFYPEER` to `TRUE`.
- **Other languages**: search for your language + "verify SSL certificate" (e.g., "Python verify SSL certificate") to find the equivalent setting. Most modern HTTP libraries enable this by default — verify that it has not been disabled in your code.

> **Important:** While REDCap has many built-in security layers, it is your responsibility to ensure that your API scripts follow secure practices. Validating the SSL certificate is one of the most effective steps you can take to protect your data and your token.

### 3.6 What Happens to a Token When Rights or Accounts Change

Because rights are checked on every call, a token is only as useful as the account behind it at that moment:

- **API rights removed:** the token stops working, but it is not deleted. If the right is granted again later, the **same** token works again. If the token may have been shared or copied while it was unused, regenerate it after re-granting.
- **User removed from the project:** the token is deleted.
- **Account suspended:** calls with the token are rejected.
- **Account expiration date reached:** the API does not check the expiration date itself; it keeps accepting the token until REDCap's scheduled job suspends the account. Expect a short delay rather than an instant cut-off.
- **Project access expired** (the expiration date on the user's project rights): calls are rejected with 403.
- **Project deleted, marked Completed, or taken Offline,** or the API disabled system-wide: calls are rejected with 400.

When someone leaves a study, remove them from the project rather than only removing their API rights, so their token is deleted. An administrator can transfer a token to another user from the Control Center **API Tokens** page if an integration must keep running.

---

## 4. Available API Methods

The REDCap API organizes its functionality into method groups. The methods available to a given token depend on the user's rights and the project's configuration.

### 4.1 Records

| Method | Description |
|---|---|
| Export Records | Retrieve some or all records, with optional filtering by record, form, event, or field. There is no DAG filter; an option only adds a `redcap_data_access_group` column, and a DAG-assigned user automatically gets only their own DAG's records |
| Import Records | Add new records or update existing ones |
| Delete Records | Permanently remove records from the project |
| Rename Record | Change a record's ID value |
| Generate Next Record Name | Retrieve the next auto-number value REDCap would assign |

### 4.2 Project Metadata and Configuration

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

> **Important — design methods in Production:** **Import Metadata** is refused in a Production project (error 400); it does not go through Draft Mode. Make Production design changes in Draft Mode through the Online Designer or a Data Dictionary upload instead. **Import Instrument-Event Mappings** is also refused in Production. **Import/Delete Events** and **Import/Delete Arms** are refused in Production unless an administrator has allowed event changes in Production and the request explicitly asks to override. Import Metadata also needs the **Project Design and Setup** right; without it the call fails with 400.

### 4.3 Users and Access

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

> **Note:** Users who are themselves assigned to a DAG cannot use the DAG methods; they get 403.

> **Important — deleting a role through the API:** Unlike the User Rights page, **Delete User Roles** is not blocked when users are still assigned to the role. Those users stay in the project with only their leftover individual rights. For users who were added straight into a role, those leftovers are REDCap's defaults, which can include the **User Rights** privilege. After deleting a role through the API, review the rights of every user who was in it.

### 4.4 Files

| Method | Description |
|---|---|
| Export File | Download a file attached to a file-upload field for a specific record |
| Import File | Upload a file to a file-upload field for a specific record |
| Delete File | Remove a file from a file-upload field |
| Export PDF | Generate and download a PDF of an instrument or all instruments for a record |

### 4.5 Reports and Logging

| Method | Description |
|---|---|
| Export Reports | Pull data from a saved REDCap report by report ID, respecting the report's field and filter settings |
| Export Logging | Retrieve the project audit log entries |

### 4.6 Surveys

| Method | Description |
|---|---|
| Export Survey Participant List | List participants (participant list surveys) |
| Export Survey Link | Generate a unique survey link for a specific record |
| Export Survey Queue Link | Get the survey queue link for a specific record |
| Export Survey Return Code | Get the return code for a partially completed survey |
| Export Survey Access Code | Get the survey access code for a record on a specific survey instrument. Requires 15.1.0+ — see [RC-API-54](RC-API-54_Export-Survey-Access-Code.md) |

> **Developer method equivalent (15.1.0+):** `REDCap::getSurveyAccessCode()` provides the same capability inside hooks, plugins and External Modules. It takes the record and instrument, plus the event ID in longitudinal projects, and assumes the record already exists. Note REDCap's own changelog spells it `getSurveyAccesCode` — a typo in the release notes rather than the method name; verify against the External Module Framework documentation before relying on the spelling.

---

## 5. Using the API Playground

The API Playground is the best place to start with the REDCap API. It requires no programming setup and provides an interactive, guided way to test any API method.

**Accessing the Playground:** Open your project and select **API Playground** in the left-hand menu (under Applications). The link appears only when the API is enabled on your instance and you hold the API Export or API Import/Update right in the project; without one of those rights the Playground will not open. It shows a list of all available methods on the left.

**How the Playground works:**

1. Select a method (e.g., "Export Records").
2. Fill in the parameters using the form fields provided — the Playground explains each parameter inline.
3. Select **Execute** to run the request and see the raw response.
4. Switch to the **Code** tab to see ready-to-copy sample code in PHP, Perl, Python, Ruby, Java, R, C#, or cURL.

The Playground uses your existing token automatically, so you can run real requests against real project data to verify what the API returns before writing a script.

> **Note:** Requests executed through the Playground are real — they affect live project data and are recorded in the project's Logging like any other API call. Use a test project or development environment when testing import or delete methods.

---

## 6. Export Data Formats

When exporting records or reports, you can specify the format and type of returned data:

**Format options:**
- **JSON** — Easily consumed by Python, R (via jsonlite), and most modern programming languages. Not the default: you must ask for it with `format=json`.
- **CSV** — Flat text file, compatible with Excel, R (via read.csv), and SAS. Familiar format for analysts who use manual exports.
- **XML** — The default when `format` is omitted. Available as standard XML or as CDISC ODM, which includes full metadata and can be re-imported into REDCap or other EDC systems.

Always set `format` explicitly, so a script never receives XML when it expects JSON or CSV.

**Type options (for record export):**
- **flat** — One row per record (classic projects) or one row per record-event combination (longitudinal).
- **eav** — Entity-Attribute-Value format. One row per field value. Useful for sparse data or when building generic processing pipelines.

**Label vs. raw values:**
By default, REDCap exports coded values (e.g., `1`, `2`, `3` for a dropdown). Setting `rawOrLabel=label` returns the text labels instead. Setting `rawOrLabelHeaders=label` returns human-readable column headers rather than field variable names.

---

## 7. HTTP Status Codes & Error Handling

### 7.1 HTTP Status Codes

Every API response includes an HTTP status code indicating whether the request succeeded or failed. Checking this code is the first step in debugging a failed request.

| Code | Meaning | What it indicates |
|---|---|---|
| 200 | OK | Request succeeded. |
| 400 | Bad Request | The request was invalid: an unknown `content` or `action` value, malformed import data, a method not allowed in the project's current status (e.g. Import Metadata in Production), a project that is deleted, Completed or Offline, or the API disabled on the instance. Some missing-rights cases also return 400, for example Import Metadata without the Project Design and Setup right. The message explains which. |
| 403 | Forbidden | The token is missing, invalid, or belongs to an account that cannot use it (suspended, expired project access, no API right for this method, or **No Access** export rights on every instrument). DAG-assigned users calling DAG methods also get 403. |
| 429 | Too Many Requests | Your IP address has been banned by the rate limiter (see §7.3). |
| 500 | Internal Server Error | REDCap encountered an error processing your request. |
| 501 | Not Implemented | The request was not sent as an HTTP POST. |

REDCap itself does not send 401, 404 or 406 for API errors (a 404 can still come from your web server if the URL path is wrong). A bad token is 403 and badly formatted import data is 400, so scripts should read the error message rather than branch on those codes.

### 7.2 Error Message Format

When an API request fails, REDCap returns the error message in the format you specified using the `returnFormat` parameter. If `returnFormat` is not set, REDCap uses the `format` value, and if neither is set, XML. For example, an XML error looks like:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<hash>
  <error>detailed error message</error>
</hash>
```

JSON requests return the message as JSON. CSV requests return plain text in the form `ERROR: detailed error message`. Always log or surface the full response body when debugging — the error message text typically identifies the exact problem (e.g., invalid parameter name, field not found, insufficient rights).

### 7.3 Rate Limiting

REDCap limits how many requests a single IP address may make per minute. The limit is set by the administrator in the Control Center (**Rate Limiter: Page hit threshold for a single IP address**, default 600 requests per minute) and counts API calls and normal page use together, so a script and a browser on the same machine share it.

If the limit is exceeded, REDCap **bans that IP address permanently** — it is not a short cool-down — and emails an administrator. Every further request from the address, API or browser, fails with 429 until an administrator lifts the ban.

- Do not run tight loops of small requests. Batch records into fewer, larger calls, and pause between calls in long-running jobs.
- If a script that worked suddenly gets 429 for every call, stop it and contact your REDCap administrator; retrying does not help.

> **Institution-specific:** The threshold, and whether any addresses (such as known integration servers) are exempt, vary by installation. Ask your REDCap administrators before running high-volume jobs.

---

## 8. Common Questions

**Q: Do I need a separate token for each project?**

**A:** Yes. API tokens are scoped to a single project. Each project you need API access to requires its own token (and, on instances that require it, administrator approval). There is no single token that works across all projects. A super token is not one either: it works only for Create Project and Export REDCap Version, not for project-level methods.

**Q: What data can my API token access?**

**A:** Only what your REDCap user account can access, checked on every call. If you are assigned to a DAG, your token can only see records in your DAG. Fields follow your **data export** rights per instrument: an instrument set to **No Access** for export is left out, even if you can view it on screen, and if every instrument is No Access the call is refused with 403. The exception is the **Mobile App** right, which gives full data access through the app whatever your export rights (your DAG still applies) — see §9a. REDCap administrators are not limited by project rights. **Writing is different:** an API Import/Update token can write to any instrument and create records, whatever your instrument rights (DAG and locking still apply).

**Q: Can the API trigger the Data Entry Trigger (DET)?**

**A:** No. The DET fires only on interactive data entry — saves made by a user on a REDCap form or survey. Data imported via the API does not trigger the DET. See [RC-INTG-01 — Data Entry Trigger](RC-INTG-01_Data-Entry-Trigger.md) for details.

**Q: Does the API trigger Alerts & Notifications or Automated Survey Invitations (ASIs)?**

**A:** It depends on the trigger type. Completion triggers and combination triggers require a direct form or survey save — they do not fire on API or data import writes. Logic triggers evaluate against the record on every write, including API imports, so they do fire. If your workflow depends on an alert or ASI firing after an API write, make sure it uses a logic trigger. See [RC-ALERT-01 — Alerts and Notifications Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) for details on trigger types.

**Q: I requested a token but don't see it on the API page. What's wrong?**

**A:** On instances where administrators approve token requests, the token does not appear until the request is approved; you get an email when it is. If the request has been pending for longer than expected, contact your REDCap administrator. Some instances let users create tokens themselves, in which case the page shows a button to create one instead (§3.2). Also verify that you have the API Export or API Import/Update user right assigned — without one, the API page will not display a token field.

**Q: Can I use the API in a project that is in Production?**

**A:** Yes, for data: record, file, report and user methods work in Production. Design methods do not go through Draft Mode. **Import Metadata** (uploading a modified data dictionary) and **Import Instrument-Event Mappings** are refused in Production, and arm and event changes are refused unless an administrator allows them (§4.2). Make Production design changes in Draft Mode in the interface. Projects that are Completed, Offline or deleted refuse all API calls.

**Q: How do I export data from a specific instrument only?**

**A:** Use the `forms` parameter in the Export Records method. Pass the instrument's variable name (not its label) to limit the export to fields on that instrument. Multiple instruments can be listed.

**Q: What is the difference between the Export Records and Export Reports methods?**

**A:** Export Records pulls data directly from the project's full record set, with parameters to control which fields, events, and records are included (DAG scoping comes from the user's own DAG assignment, not a parameter). Export Reports runs a pre-defined saved report by its report ID, using the field selection, filtering, and ordering that was configured when the report was built. Both return record-level data; the report method is easier to use when a researcher has already set up a report that matches the data subset they need.

**Q: Is there a limit on how many records or how much data I can pull at once?**

**A:** There is no hard row limit documented for standard API exports, but very large datasets can time out or cause performance issues. For large projects, it is best practice to paginate exports using the `records` or `events` parameters to pull data in batches rather than all at once. There is, however, a limit on how **often** you can call: a per-IP limit on requests per minute (default 600), shared with normal page use. Exceeding it bans your IP address until an administrator lifts the ban (§7.3), so keep batches reasonably large rather than making thousands of tiny calls.

---

## 9. Common Mistakes & Gotchas

**Storing the token in version-controlled code.** A token hardcoded in a script that gets committed to GitHub is effectively public. Always store tokens as environment variables or in a credentials file excluded from version control. Treat token leaks as a security incident and request revocation immediately.

**Forgetting that the API returns coded values, not labels.** By default, the export returns raw coded values (`1`, `0`, `2`) for dropdown, radio, and checkbox fields — not the labels that display in the interface. If your downstream analysis expects text labels, add `rawOrLabel=label` to the request. Forgetting this leads to mysterious numeric columns in exported data.

**Assuming export includes all fields by default.** The Export Records method returns all fields when no field list is specified, but includes all events in longitudinal projects regardless of instrument-event assignment. In large longitudinal projects, this can produce very wide, sparse output. Always specify `forms`, `fields`, or `events` parameters to limit the export to what you actually need.

**Using an HTTP URL instead of HTTPS.** API tokens are transmitted in the request body. Sending a request to an HTTP URL exposes the token to anyone who can observe the network traffic. Always verify your REDCap instance URL begins with `https://`.

**Expecting the API to fire alerts or ASIs.** Whether an Alert or ASI fires on an API import depends on its trigger type. Completion triggers and combination triggers — which require a specific form or survey save — do not fire when data is written via the API or Data Import tool. Logic triggers, which evaluate a condition against the record regardless of save source, do fire after API writes. If your alert or ASI uses a completion trigger, it will not respond to API-imported data; if it uses a logic trigger, it will. Test with a real API call before building a workflow that depends on this behavior.

**Confusing `instrument` (variable name) with the instrument's label.** API parameters that reference instruments — such as the `forms` parameter in Export Records — require the instrument's unique variable name (e.g., `demographics`), not its display label (e.g., `Demographics`). The variable name is found in the Online Designer or data dictionary. These often match, but not always, especially if an instrument was renamed after creation.

**Looping over records one call at a time.** A script that exports or imports one record per request, or retries failures in a tight loop, can exceed the per-IP rate limit within a minute. REDCap then bans the IP address — for the browser as well as the script — until an administrator lifts it (§7.3). Batch records and add a pause between calls.

**Expecting 401 for a bad token.** REDCap returns 403 for a missing or invalid token and 400 for most malformed requests (§7.1). Error handling that only checks for 401 will treat a token problem as something else.

**Not handling repeating instrument data correctly.** When exporting from a project with repeating instruments or events, each instance appears as a separate row identified by `redcap_repeat_instrument` and `redcap_repeat_instance`. Code that assumes one row per record will produce incorrect results. Always inspect the structure of export output from repeating projects before building a processing pipeline.

---

## 9a. Rights Enforcement in API Methods

API access is scoped by the calling user's project rights — the token grants no more than the user already has, with the Mobile App exception below. That principle has needed enforcing in several specific places, and the fixes matter because each one silently returned data the caller should not have received.

| Issue | Fixed in |
| --- | --- |
| **File Export** returned the file even where the user had **No Access** export rights for the instrument holding the File Upload field | 16.0.9 Standard / 15.5.33 LTS |
| **Export a Survey Link** returned a link for records outside the API user's **Data Access Group** | 16.0.28 LTS |
| **Export a Survey Access Code**, **Export a Survey Queue Link** and **Export a Survey Return Code** returned codes and links for records outside the caller's DAG | 17.1.0 Standard / 16.0.31 LTS |
| **Access Control Group** compliance checks could be bypassed by importing user rights or role assignments via the API or the User Rights CSV upload | 16.1.4 Standard |
| **File Repository listing** returned admin-restricted folders, which it should exclude | 16.0.8 Standard |

> **Important for anyone auditing API access.** These were not permission-configuration errors — the rights were set correctly and the API returned the data anyway. If your institution has relied on DAG separation or instrument-level export rights to constrain API users on an older instance, the boundary was not fully enforced. Reviewing the version history against these fixes is the way to establish whether it applied to you.

> **Important — the Mobile App right overrides export rights.** A user with the **Mobile App** right can download all data on every instrument through the REDCap Mobile App, which uses the API, whatever their API rights and data export rights are — including instruments set to **No Access** or **De-Identified** for export. Their DAG assignment still applies. REDCap shows a warning to this effect when the right is ticked. Grant the Mobile App right only to users who may see the full data set for their DAG.

Data Access Group behaviour is documented in [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); export rights levels in [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md).

---

## 10. Administrator Configuration

The REDCap API must be enabled at the system level before any project can use it. This is done in the Control Center under System Configuration → Modules/Services Configuration. When disabled system-wide, the API link does not appear in any project's left-hand menu, no tokens can be requested, and API calls are refused with 400.

Administrators can also manage, view, regenerate, transfer and revoke API tokens for any user from the Control Center under Users → API Tokens. Super tokens (required for the Create Project method) must be granted there as well; any administrator can give one to any user.

Two other Control Center settings shape API use:

- **Allow normal users to auto-generate API tokens for their projects?** — whether token requests need administrator approval, or all or selected users can create tokens themselves (§3.2). Requests that need approval arrive on the To-Do List and by email.
- **Rate Limiter: Page hit threshold for a single IP address** — the per-IP requests-per-minute limit (default 600), shared by API calls and page views. An IP address that exceeds it is banned permanently and an administrator is emailed; an administrator must lift the ban (§7.3).

> **See also:** [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)

---

## 11. Related Articles

- [RC-INTG-01 — Data Entry Trigger](RC-INTG-01_Data-Entry-Trigger.md) (separate mechanism for real-time notification of data changes to external systems; does not fire on API imports)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (manual export workflow; for comparison with API-based export)
- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (manual import methods; API import is the programmatic equivalent)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (where API Export and API Import rights are granted)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG-scoped access applies equally to API tokens)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (essential background for working with repeating data via the API)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (system-level API enable/disable and token management)
