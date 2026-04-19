RC-CC-18

**Control Center: Custom Application Links**

| **Article ID** | RC-CC-18 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-21 — Control Center Overview; RC-CC-06 — Modules & Services Configuration; RC-API-01 — REDCap API |

---

**Custom Application Links** (found at **Control Center → Miscellaneous Modules → Custom Application Links**) allows administrators to add institution-defined links to the left-hand Applications menu of every project on the instance. These links can point to external websites, other REDCap projects, or internal resources such as a help desk form or training portal.

---

# Overview

Custom Application Links appear at the bottom of the left-hand project menu for every user in every project, by default. Administrators configure them centrally; no project-level action is required from project users.

Typical use cases:
- Linking to a support/help desk form
- Linking to institution training resources
- Linking to a related REDCap project (e.g., a central intake form)
- Linking to an external application that integrates with REDCap via the advanced identity verification mechanism

---

# Per-Link Configuration Options

Each custom link has the following settings:

| Setting | Options | Notes |
| --- | --- |---|
| **Link Label** | Free text | Text displayed on the left-hand menu |
| **Link URL / Destination** | URL or project selection | The target address or REDCap project |
| **Link Type** | Simple Link / Advanced Link / REDCap Project | Controls how navigation and identity work (see below) |
| **User Access** | All users / Selected users / Excluded projects | Controls who sees the link and in which projects |
| **Opens new window** | Yes / No | Whether the link opens in a new browser tab |
| **Append record info to URL** | Yes / No | Appends the current record ID to the URL as a query parameter |
| **Append project ID to URL** | Yes / No | Appends the current project ID to the URL as a query parameter |

---

# Link Types

## Simple Link

A Simple Link navigates the user to the target URL in a standard, anonymous fashion. No user or project information is transmitted to the target site. The external site has no way to identify who is visiting.

Use a Simple Link when the destination website does not need to know who the REDCap user is — for example, a public training website or a generic help page.

## REDCap Project

Selecting the **REDCap Project** type presents a list of all projects in production or development status. After selecting a project, REDCap creates a link directly to that project. This allows administrators to surface commonly referenced projects (e.g., a shared resource request form) in every user's menu.

> **Note:** Administrators can link to any project regardless of whether they are a member of that project. Standard users can only link to their own projects when creating bookmarks.

## Advanced Link

The Advanced Link goes beyond simple navigation by transmitting encrypted user identity information to the target website. This allows an external site to verify that the person arriving from REDCap is a valid, active REDCap user.

> **Technical prerequisite:** Using the Advanced Link requires web development knowledge and control over the target external website. The external site must be configured to receive and process the identity verification flow described below.

### How Advanced Link identity verification works

When a user clicks an Advanced Link, REDCap does not navigate directly to the URL. Instead, it submits an HTML form using the HTTP POST method. A single field — `authkey` — is posted to the external website. The authkey is an encrypted, undecipherable string that encodes the user's session.

The external site then uses the authkey to request identity information from the REDCap API:

**Step 1 — Receive the authkey**
The external site receives `authkey` via the HTTP POST request triggered when the user clicked the link.

**Step 2 — Post the authkey back to the REDCap API**
The external site sends a POST request to the REDCap API endpoint at your institution's REDCap URL:

```
POST https://[your-redcap-url]/api/
```

Only two parameters are required:
- `authkey` — the value received in Step 1
- `format` — the desired response format: `csv` (default), `json`, or `xml`

> **Note:** This API request does **not** require an API token. It is one of the few REDCap API calls that is token-free.

**Step 3 — Receive user and project information**
If the authkey is valid and the user's REDCap session is still active, the API returns the following fields (in the specified format):

| Field | Description |
| --- | --- |
| `username` | The REDCap username of the user who clicked the link |
| `project_id` | The ID of the REDCap project the user was in when they clicked the link |
| `data_access_group_name` | The name of the user's Data Access Group (blank if not in a DAG) |
| `data_access_group_id` | The numeric ID of the user's DAG (blank if not in a DAG) |
| `callback_url` | The URL of the REDCap project the user came from |

If the request is malformed or the user's session has expired, the API returns `0`.

**Step 4 — Use the returned information**
The external site can use the returned values to implement user-specific behavior — for example, granting or restricting access based on the REDCap username, pre-populating a form with the user's project context, or logging the visit with the associated project ID.

### Language compatibility

The REDCap API is language-agnostic. The external site can be written in any server-side language (PHP, Python, Node.js, etc.) as long as it can make a properly formatted HTTP POST request.

---

# User Access and Project Scope

By default, a custom link appears for **all users** in **all projects**. Administrators can narrow this:

- **Selected users** — specify a list of usernames that should see the link; all others see nothing
- **Excluded projects** — the link appears everywhere except in the listed projects

These settings are configured per link and can be updated at any time.

---

# Adding a New Link

At the bottom of the Custom Application Links page, provide:
1. A **Label** — what will appear on the left-hand menu
2. A **URL** — the target web address
3. Select the **Link Type**

Save the link, then configure User Access and other per-link settings as needed.
