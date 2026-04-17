RC-MOB-01

**REDCap Mobile App**

| Field | Value |
|---|---|
| Article ID | RC-MOB-01 |
| Domain | Mobile |
| Applies To | All REDCap projects; requires Mobile App module enabled by administrator |
| Prerequisite | None |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-AT-11 — Action Tags: Mobile App Action Tags; RC-MYCAP-01 — MyCap: Overview & Enabling; RC-USER-01 — User Rights: Overview & Three-Tier Access |

---

# 1. Overview

This article covers the REDCap Mobile App — a native iOS and Android application that allows study team members to enter and edit record data offline from a mobile device. The app is distinct from MyCap (the participant-facing mobile application). It is intended for staff who collect data in environments without reliable internet access, such as clinical settings, field sites, or participant homes. Data entered offline is stored locally on the device and synchronized with the REDCap server when a connection becomes available.

> **Yale-specific:** [Confirm whether the REDCap Mobile App module is enabled on your institution's REDCap server and whether any approval is required before use. Contact your local REDCap support team.]

---

# 2. Key Concepts & Definitions

## REDCap Mobile App

The official REDCap application for iOS and Android, published by Vanderbilt University. It is used by study team members (not participants) and requires a REDCap login. The app enables offline data entry for any REDCap project it has been initialized with.

## Mobile App User

A distinct user credential created within a REDCap project specifically for the mobile app. A mobile user is not a full REDCap account — it is a lightweight credential tied to a single project that grants access to the app for that project. Mobile users are managed at the project level under User Rights.

## App Username

The username a mobile user enters when logging into the app. This may differ from the user's REDCap server username. The action tag `@APPUSERNAME-APP` captures the app username at time of data entry (see RC-AT-11).

## Initialize (a project)

The process of downloading a project's structure and existing records to the mobile device. A project must be initialized before offline data entry can begin. Initialization requires an internet connection.

## Synchronize (Sync)

The process of uploading locally entered data to the REDCap server and downloading any changes made on the server since the last sync. Sync requires an internet connection and should be performed regularly to avoid conflicts.

## Offline Mode

When the device has no internet connection, the app operates in offline mode. Data entered during offline mode is queued locally and uploaded during the next sync.

## Draft Record

A record edited or created in the mobile app that has not yet been synchronized to the server. Draft records are visible in the app and flagged as pending until sync completes.

---

# 3. REDCap Mobile App vs. MyCap vs. Browser-Based Entry

The REDCap Mobile App is one of three primary data collection interfaces in REDCap. Choosing the right interface depends on who is collecting data and under what conditions.

| Feature | REDCap Mobile App | MyCap | Browser-Based Entry |
|---|---|---|---|
| Who uses it | Study team members | Research participants | Study team members or participants |
| REDCap login required | Yes (mobile user credential) | No | Yes (for staff); No (for survey links) |
| Installed on | Study team–owned device | Participant's personal device | Any web browser |
| Primary use case | Offline data entry at point of care | Remote, repeated participant data collection | Online data entry and survey completion |
| Works offline | Yes | Yes | No |
| Supports active tasks | No | Yes | No |
| Longitudinal projects | Yes | Yes | Yes |

Use the REDCap Mobile App when study staff need to collect data in person at a location with unreliable or no internet (e.g., a bedside interview, a field visit, a community health site). Use MyCap when participants will complete assessments on their own devices over time. Use browser-based entry for all other scenarios. See RC-MYCAP-01 — MyCap: Overview & Enabling for a detailed comparison of MyCap and the Mobile App.

---

# 4. Administrator Setup

Before any project can use the REDCap Mobile App, a REDCap administrator must enable the Mobile App module for the server.

## 4.1 Enable the Mobile App Module

An administrator enables the Mobile App module in the REDCap Control Center under the **Mobile App** section. Once enabled, the module becomes available to all projects on the server.

> **Yale-specific:** [Confirm whether the Mobile App module is already enabled and whether additional administrator approval is required to activate it for a specific project.]

## 4.2 Mobile App Settings in the Control Center

Administrators can configure several server-wide settings:

- **Allow users to download records to the app** — Controls whether the initialization process downloads existing records. Disabling this means the app can only create new records offline.
- **Require a PIN or biometric lock** — Enforces a device-level lock on the app.
- **Offline record limit** — Sets a maximum number of records that can be held on a device at one time. Limits protect against large data sets being held on potentially unsecured devices.

---

# 5. Project-Level Setup

## 5.1 Enable the Mobile App for a Project

Within a project, navigate to **Project Setup** → **Enable optional modules and customizations** → check **Use the REDCap Mobile App**. This exposes the Mobile App section in the left sidebar under Applications.

## 5.2 Create Mobile App Users

Navigate to **Applications** → **REDCap Mobile App** → **Add Mobile App User**. Each mobile user needs:

- A unique **app username**
- A **PIN** (used to log into the app)
- An optional **name** for identification

Mobile users are project-specific — the same person working on two projects needs a separate mobile user credential for each project.

> **Note:** Mobile users are not the same as REDCap user accounts. They have no access to the REDCap web interface and cannot log into the REDCap server.

## 5.3 Instrument Assignment (Optional)

If the project uses multiple instruments, you can restrict a mobile user to specific instruments. Navigate to **REDCap Mobile App** → **Instrument assignment** to specify which instruments appear for each mobile user. By default, all instruments are available.

---

# 6. Initializing and Using the App

## 6.1 Install the App

Download the REDCap Mobile App from the Apple App Store (iOS) or Google Play Store (Android). Search for "REDCap" — the publisher is Vanderbilt University Medical Center.

## 6.2 Connect to the REDCap Server

When first opening the app:

1. Enter the **REDCap server URL** (the base URL of your institution's REDCap installation, without a trailing slash)
2. Enter the **app username** and **PIN** created in Section 5.2
3. The app will connect and display the projects associated with that mobile user

> **Yale-specific:** [Provide the correct server URL for your institution's REDCap installation.]

## 6.3 Initialize a Project

After connecting, select a project from the list and tap **Initialize**. The app downloads the project's data dictionary (instruments, fields, branching logic) and optionally existing records. Initialization requires an internet connection and may take several minutes for large projects.

A project must be re-initialized after major structural changes (e.g., new fields added, branching logic updated). Minor record-level changes are reconciled through normal sync.

## 6.4 Entering Data Offline

Once initialized, the app can be used without an internet connection:

1. Open the app and select the initialized project
2. Browse existing records or tap **Add New Record** to create one
3. Navigate through instruments using the navigation buttons at the bottom of each form
4. Complete fields as you would in the browser — branching logic, required fields, and validation rules all function in the app
5. Save the record — it is stored locally as a draft until sync

> **Note:** Calculated fields may not update until the record is synced to the server, depending on whether the calculation depends on data from other instruments or events.

## 6.5 Synchronizing

To sync, the device must have an active internet connection. Tap **Sync** within the project view. The app will:

1. Upload all draft records and edits to the REDCap server
2. Download any records or edits made on the server since the last sync

Sync is not automatic — users must initiate it manually. Best practice is to sync at the start and end of each data collection session.

> **Important:** If the same record was edited both in the app and on the REDCap server between syncs, a conflict may occur. REDCap will flag the conflict for resolution. Avoid parallel editing of the same record in the app and the browser.

---

# 7. Security Considerations

The REDCap Mobile App stores project data locally on the device. This introduces security considerations that do not apply to browser-based access.

- **Encrypted storage** — REDCap Mobile App encrypts locally stored data at rest. The specific encryption standard depends on the app version; consult your institution's IT security team for details.
- **PIN lock** — The app supports a numeric PIN lock and biometric authentication (Face ID / fingerprint) to prevent unauthorized access.
- **Remote wipe** — If the device is lost or stolen, an administrator or project user with appropriate rights can remove the mobile user's access in the REDCap web interface. This will prevent future syncs, but data already on the device is not remotely wiped — device management software (MDM) would be needed for a true remote wipe.
- **Study team devices** — Because data is stored locally, the REDCap Mobile App should be used only on study team–owned and managed devices, not personal devices. This distinguishes it from MyCap, which is designed for participant personal devices.

> **Yale-specific:** [Confirm whether IRB or institutional data security requirements mandate additional controls for devices running the REDCap Mobile App, such as MDM enrollment or full-disk encryption requirements.]

---

# 8. Common Questions

**Q: What is the difference between the REDCap Mobile App and MyCap?**

**A:** The REDCap Mobile App is for study team members. It requires a REDCap login and is installed on study team–owned devices for offline data entry at the point of care. MyCap is for research participants. It is installed on the participant's personal device and is designed for repeated, participant-reported data collection over time. They serve different audiences and different workflows. See RC-MYCAP-01 — MyCap: Overview & Enabling for a detailed comparison.

**Q: Does the REDCap Mobile App work with longitudinal projects?**

**A:** Yes. The app supports longitudinal projects. During data entry, the user selects the event as they would in the browser.

**Q: Can the app be used with surveys?**

**A:** The REDCap Mobile App is designed for staff-entered (non-survey) instruments. Survey instruments are not presented in survey mode within the app — they appear as regular forms. If you need participant-facing surveys on a mobile device, use MyCap or send a survey link that participants can open in a mobile browser.

**Q: What happens if I lose the device before syncing?**

**A:** Any data entered since the last sync will be lost along with the device. This is one reason to sync frequently — ideally at the end of every data collection session. Data that was previously synced is safe on the REDCap server.

**Q: Can multiple devices use the same mobile user credential simultaneously?**

**A:** It is not recommended. While the system does not prevent it, using the same mobile user credential on two devices simultaneously creates a high risk of sync conflicts, since both devices will attempt to upload drafts that may reference the same records.

**Q: What happens to the app data after a mobile user is deleted?**

**A:** Deleting a mobile user in REDCap prevents that credential from syncing in the future. Data already synced to the server is preserved. Draft records that were never synced will remain on the device until the app is cleared or the project is removed from the device.

**Q: Can the app be used for repeating instruments or events?**

**A:** Yes. If a project uses repeating instruments or repeating events, these are accessible in the app the same way they are in the browser — the user can add new instances of a repeating instrument or event during offline data entry.

---

# 9. Common Mistakes & Gotchas

**Forgetting to sync before ending a session.** Data entered in the app is not transmitted to the server until sync is manually triggered. Staff who close the app or leave a site without syncing risk data loss if the device is damaged, lost, or reset. Build sync into end-of-session workflows as a required step.

**Editing the same record in the browser and the app simultaneously.** If a record is opened and saved in the REDCap web interface while a draft of that record also exists in the app, a conflict will occur on the next sync. REDCap will not silently overwrite — it will flag the conflict — but resolving conflicts adds administrative burden. Coordinate data entry to ensure only one interface edits a record at a time.

**Re-initializing too rarely after project changes.** If new fields, instruments, or branching logic are added to a project in Development or after a Draft Mode approval, the app must be re-initialized before those changes take effect on the device. Mobile users who do not re-initialize will be working with an outdated version of the data dictionary and may not see new fields.

**Using personal devices for app data collection.** The REDCap Mobile App stores PHI or sensitive study data locally. Using personal devices is an information security risk and may violate your institution's IRB or data governance policies. Always use study team–owned, managed devices.

**Assuming calculated fields update offline.** Calculations that depend on data from multiple instruments, multiple events, or server-side logic may not evaluate correctly while the device is offline. The calculated value will update after sync when the server processes the full record. Do not rely on app-displayed calculated values as final during offline entry.

---

# 10. Related Articles

- RC-AT-11 — Action Tags: Mobile App Action Tags (`@APPUSERNAME-APP`, `@BARCODE-APP`, `@SYNC-APP`)
- RC-MYCAP-01 — MyCap: Overview & Enabling (participant-facing mobile app; MyCap vs. REDCap Mobile App comparison)
- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-USER-02 — User Rights: Adding Users & Managing Roles
- RC-PROJ-01 — Project Lifecycle: Status and Settings
- RC-NAV-UI-01 — Project Navigation UI
