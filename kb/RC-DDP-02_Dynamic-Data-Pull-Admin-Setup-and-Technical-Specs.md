RC-DDP-02

**Dynamic Data Pull (DDP) — Admin Setup & Technical Specs**

| **Article ID** | RC-DDP-02 |
|---|---|
| **Domain** | Integration — Dynamic Data Pull |
| **Applies To** | REDCap Administrators |
| **Prerequisite** | RC-DDP-01 — Dynamic Data Pull: Overview & User Guide |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DDP-01 — DDP Overview & User Guide; RC-INTG-01 — Data Entry Trigger |

---

# 1. Overview

This article covers everything a REDCap Administrator needs to configure and enable the Dynamic Data Pull (DDP). It includes the Control Center settings, descriptions of all configurable options, and the full technical specifications for the web services that must be built and hosted by the institution to support the DDP.

For an explanation of the DDP from a user perspective (field mapping, adjudication, etc.), see **RC-DDP-01**.

---

# 2. Architecture Overview

The DDP operates by having REDCap communicate with one or two mandatory web services — and optionally a third — that the institution builds and hosts. REDCap sends HTTP POST requests to these services; the services respond in a standardized format. This architecture gives institutions direct control over how their source system data is exposed and who can access it.

The three web services are:

| Service | Required? | Purpose |
|---|---|---|
| **Metadata Web Service** | Required | Returns a list of all available fields from the source system with their attributes |
| **Data Web Service** | Required | Returns actual data values for a given record from the source system |
| **User Access Web Service** | Optional | Validates whether the current REDCap user is authorized to access source system data |

REDCap v5.9.0+ is required to use the DDP.

---

# 3. Control Center Configuration

The DDP is configured at **Control Center → Miscellaneous Modules → Dynamic Data Pull (DDP) — Custom**.

### Enable Dynamic Data Pull (DDP)
**Options:** Disabled / Enabled

Enables or disables DDP at the system level. Once enabled globally, an administrator can then activate it for individual projects via each project's Project Setup page (under "Optional Modules and Customizations").

> **Note:** If either the Metadata Web Service or Data Web Service URLs are not defined or are not functioning correctly, the DDP will not work. It is strongly recommended to have both services built and tested before enabling DDP system-wide.

---

### Custom Name for the External Source System
**Default:** *(blank — displays as "source system")*
**Examples:** Epic, Cerner, EMR, EDW

Sets the display name for the external source system as shown to users throughout the DDP interface. If left blank, REDCap will use the generic term "source system."

---

### URL for Metadata Web Service
**Required**

The URL of the institution's Metadata Web Service endpoint. REDCap calls this service when users are mapping fields on the DDP setup page. The service must return a list of all available source system fields and their attributes.

A **Test** button is provided on the settings page to verify the URL is reachable from the REDCap web server.

---

### URL for Data Web Service
**Required**

The URL of the institution's Data Web Service endpoint. REDCap calls this service when pulling actual data for a specific record from the source system (both real-time on record identifier entry and via the background cron job).

A **Test** button is provided to verify the URL is reachable.

---

### URL for User Access Web Service
**Optional**

The URL of the institution's User Access Web Service endpoint. When configured, REDCap calls this service once per project per session to verify that the current user is authorized to access data from the source system. If the service indicates the user does not have access, they receive an error message when attempting to adjudicate data.

This service adds an extra layer of security and is particularly important when the User Rights setting below is configured to allow normal users to grant DDP privileges.

---

### Custom Text for Users
**Default:** *(blank — generic contact text is displayed)*

HTML-enabled text displayed at the top of the DDP information popup shown to users. This field should describe your institution's process for requesting DDP access — for example, linking to a request form or providing contact information for the REDCap support team.

If left blank, REDCap displays a generic message instructing users to contact their REDCap administrator.

---

### Display Information About DDP on Project Setup Page
**Options:** Yes (display) / No (hide)
**Default:** Yes

Controls whether DDP is advertised to users on a project's Project Setup page. Setting this to **No** hides all DDP-related UI from project users — useful for restricting awareness of DDP to a limited audience without advertising it broadly.

---

### Allow Normal Users to Grant DDP Privileges to Other Users
**Options:** Yes, normal users can grant DDP rights / No, only Administrators can grant DDP rights
**Default:** No (Administrators only)

Determines who can assign DDP user privileges on a project's User Rights page.

> **Security note:** If the User Access Web Service is not configured, it is **strongly recommended** to set this to **No** (Administrators only). Without the User Access Web Service, there is no automatic check that a REDCap user actually has authorization to access the source system data. Allowing normal users to grant DDP rights in that scenario creates a meaningful security risk for sensitive source data.

Choosing **Yes** is most appropriate when a User Access Web Service is in place to enforce source system authorization independently of REDCap.

---

### Data Fetch Interval
**Default:** 24 hours | **Range:** 1–999 hours

How frequently REDCap's background cron job will re-check the source system for new data for each active record in DDP-enabled projects. The exact check time per record is calculated from the time of the last fetch for that record.

---

### Inactivity Timeout
**Default:** 7 days | **Range:** 1–100 days

The amount of project or record inactivity after which REDCap stops automatically fetching data for that project or record:

- If a DDP-enabled project has had no logged user activity for this many days, REDCap pauses automatic data fetching for the entire project.
- If a specific record within an active project has had no data modifications for this many days, REDCap pauses automatic fetching for that individual record.

Automatic fetching resumes when activity is detected.

---

### Convert Source System Timestamps from GMT to Local Server Time
**Options:** No (leave as-is) / Yes (convert from GMT)
**Default:** No

If the source system outputs temporal data timestamps in Greenwich Mean Time (GMT), enabling this setting causes REDCap to automatically convert those timestamps to the local server time before displaying them in the adjudication interface.

> **Caution:** Only enable this if you can definitively confirm that the source system outputs timestamps in GMT. Enabling it when timestamps are already in local time will produce incorrect offsets. This setting is not retroactive — it only affects data pulled after the setting is changed.

---

# 4. Web Service Technical Specifications

All three web services use **HTTP(S) POST** requests. The Metadata Web Service and User Access Web Service receive requests as **multipart form data** (`content-type: application/x-www-form-urlencoded`). The Data Web Service receives requests as **JSON-encoded POST** (`content-type: application/json`).

### Securing Web Service Communication

Two methods are available for securing DDP web service transactions:

1. **IP allowlist:** Restrict the web service so that only the REDCap server's IP address(es) can call it.
2. **Secret hash in the URL:** Embed a shared secret in the web service URL (e.g., `https://your-institution.edu/ddp_service.php?secret=abc123xyz`). This secret can be defined when configuring the URLs in the Control Center. Using both methods together provides the highest level of authenticity verification.

---

### Common POST Parameters (Sent to All Three Services)

| Parameter | Type | Description |
|---|---|---|
| `user` | string | The REDCap username of the current user. If the cron job is fetching data (no authenticated user), this value will be blank. |
| `project_id` | string | The unique numeric ID of the REDCap project (the `pid` value in the project URL). |
| `redcap_url` | string | The base URL of the REDCap installation (home page URL). |

---

### 4.1 Metadata Web Service

**Purpose:** REDCap calls this service when users are on the DDP field mapping page. The service returns the full list of fields available from the source system so users can select which ones to map to REDCap fields.

**Request method:** POST (multipart form data)
**Input:** No input from REDCap beyond the common POST parameters above.

**Return format:** JSON-encoded array of field objects. Each object must have a `field` attribute (required); all others are optional.

| Attribute | Type | Required | Description |
|---|---|---|---|
| `field` | string | Yes | Unique field name. Must contain only letters, numbers, underscores, and dashes. |
| `label` | string | No | Short human-readable label for the field. Default: blank. |
| `description` | string | No | Additional description beyond the label. Default: blank. |
| `temporal` | string | No | `"1"` if the field has multiple values over time (temporal); `"0"` if it has a single value. Default: `"0"`. |
| `category` | string | No | High-level grouping (e.g., "Demographics", "Vitals", "Labs"). Default: blank. |
| `subcategory` | string | No | Subcategory within a category (e.g., "Glucose Tests"). Default: blank. |
| `identifier` | string | No | `"1"` if this field is the record identifier field in the source system (e.g., MRN). Default: blank. |

**Example response:**
```json
[
  {"field":"mrn","label":"Medical Record Number","description":"Patient's MRN","temporal":0,"category":"Demographics","identifier":"1"},
  {"field":"dob","label":"Date of Birth","description":"Patient's date of birth (Y-M-D format)","temporal":0,"category":"Demographics"},
  {"field":"glucose_wb","label":"GLUCOSE WHOLE BLOOD","description":"Glucose whole blood result","temporal":1,"category":"Labs","subcategory":"Glucose Tests"}
]
```

---

### 4.2 Data Web Service

**Purpose:** REDCap calls this service when pulling actual data for a specific record — both in real-time (when the record identifier is entered) and during scheduled cron fetches.

**Request method:** POST (JSON-encoded)
**Content-type:** `application/json`

**JSON parameters sent by REDCap:**

| Parameter | Type | Description |
|---|---|---|
| `user` | string | REDCap username (blank if cron job) |
| `project_id` | string | REDCap project ID |
| `redcap_url` | string | REDCap base URL |
| `id` | string | The value of the external source system's identifier field for this record (e.g., the MRN value stored in REDCap) |
| `fields` | array | List of source fields to retrieve (see below) |

Each object in the `fields` array contains:

| Attribute | Type | Description |
|---|---|---|
| `field` | string | The unique source field name (as defined in the Metadata Web Service) |
| `timestamp_min` | string | *(Temporal fields only)* Lower bound of the time window: `YYYY-MM-DD HH:MM:SS`. Calculated by REDCap as: associated date field value minus the day offset. |
| `timestamp_max` | string | *(Temporal fields only)* Upper bound of the time window: `YYYY-MM-DD HH:MM:SS`. Calculated by REDCap as: associated date field value plus the day offset. |

**Example request body:**
```json
{
  "user": "jsmith",
  "project_id": "394",
  "redcap_url": "https://your-institution.edu/redcap/",
  "id": "123456",
  "fields": [
    {"field": "dob"},
    {"field": "gender"},
    {"field": "glucose_wb", "timestamp_min": "2024-06-14 10:51:00", "timestamp_max": "2024-06-16 10:51:00"}
  ]
}
```

**Return format:** JSON-encoded array of result objects. Each object must include `field` and `value`. Temporal fields may also include `timestamp`.

| Attribute | Type | Description |
|---|---|---|
| `field` | string | The unique source field name |
| `value` | string | The data value for this field |
| `timestamp` | string | *(Temporal fields only)* Date/time when this value was recorded in the source system. Accepted formats: `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`, or `YYYY-MM-DD HH:MM:SS`. |

**Example response:**
```json
[
  {"field":"gender","value":"0"},
  {"field":"dob","value":"1984-03-22"},
  {"field":"glucose_wb","value":"181","timestamp":"2024-06-14 14:32"},
  {"field":"glucose_wb","value":"124","timestamp":"2024-06-15 06:55"},
  {"field":"glucose_wb","value":"91","timestamp":"2024-06-15 10:09"}
]
```

> **Note:** REDCap will automatically ignore any temporal field values whose timestamps fall outside the `timestamp_min`/`timestamp_max` range. The service should ideally only return values within the requested range, but REDCap will filter out-of-range values automatically if the service returns extras.

---

### 4.3 User Access Web Service (Optional)

**Purpose:** REDCap calls this service once per project per session to determine whether the current user has authorization to access data from the external source system. If the service returns `"0"` (no access), the user receives an error message when attempting to adjudicate data.

**Request method:** POST (multipart form data)
**Input:** The three common POST parameters (`user`, `project_id`, `redcap_url`).

**Return format:** Boolean string — `"1"` if the user has access to the source system, `"0"` if not.

---

# 5. Testing and Evaluation

REDCap provides a set of **DDP demo files** (available as a ZIP download from the DDP settings page in the Control Center) containing a mock web service implementation for testing and evaluation. This allows administrators to test DDP connectivity and behavior without a live source system connection.

Each web service URL field in the Control Center settings also includes a **Test** button that sends a request to the URL and reports whether it is reachable from the REDCap server.

---

# 6. Enabling DDP for a Specific Project

After system-level DDP configuration is complete:

1. Navigate to the project → **Project Setup** → **Optional Modules and Customizations**.
2. Enable **Dynamic Data Pull** for the project.
3. Grant individual users DDP privileges via the project's **User Rights** page:
   - **DDP Mapping/Setup** — allows the user to configure field mappings on the DDP setup page
   - **DDP Adjudication** — allows the user to review and approve incoming data from the source system

> **Important:** If the User Access Web Service is not configured and the system-level setting allows normal users to grant DDP rights, any project user with User Rights management access could grant themselves or others DDP access. For sensitive source systems, restrict this via the Control Center setting.

---

# 7. Common Questions

**Q: Do we have to build the web services ourselves?**

**A:** Yes. The institution is responsible for building and hosting the Metadata and Data Web Services (and optionally the User Access Web Service). REDCap provides the technical specifications (this article) and demo files to guide development. The web services can be written in any server-side language capable of handling HTTP POST requests and returning JSON.

**Q: Can DDP be used with FHIR/CDIS?**

**A:** The DDP described here is the "Custom" DDP that uses institution-built web services. REDCap also has a separate FHIR-based clinical data interoperability feature ("Clinical Data Interoperability Services"), configured under a different Control Center section. They are distinct features.

**Q: What happens if the Data Web Service is temporarily unavailable?**

**A:** REDCap makes the request and moves on. If the service is unavailable, the fetch for that record is skipped. The record will be retried at the next scheduled cron interval. No alert is sent to users or administrators.

**Q: The cron job interval is set to 24 hours. When exactly does each record get checked?**

**A:** The interval is measured from the time of the last fetch for each individual record — not from a fixed clock time. Records are not all checked simultaneously; they are staggered based on their individual fetch history.

---

# 8. Related Articles

- RC-DDP-01 — Dynamic Data Pull: Overview & User Guide (user-facing concepts, mapping, adjudication)
- RC-INTG-01 — Data Entry Trigger (related integration pattern using HTTP POST)
- RC-USER-02 — User Rights: Adding Users and Managing Roles (DDP privilege assignment)
