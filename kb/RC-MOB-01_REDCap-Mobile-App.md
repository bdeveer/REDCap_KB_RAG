

**REDCap Mobile App**

| Field | Value |
|---|---|
| **Article ID** | [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md) |
|---|---|
| **Domain** | Mobile |
| **Applies To** | All REDCap projects; requires Mobile App module enabled by administrator |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | None |
| **Version** | 1.2 |
| **Last Updated** | 2026-10 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-AT-11 — Action Tags: Mobile App Action Tags](RC-AT-11_Action-Tags-Mobile-App.md); [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md); [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md); [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) |
| **Synonyms** | how do i enter data offline on a mobile device; set up the redcap mobile app for study staff; collect data without internet then sync later; initialize a project on the mobile app with qr code; difference between the redcap mobile app and mycap; mobile app api token and initialization code; reset a mobile app user pin; sync offline records back to the redcap server; mobile app emergency data dump save to device; mobile app sync failed uploading the document has failed; get unsynced data off an ipad in the redcap app; mobile app outdated ios version will not sync |

---

## 1. Overview

This article covers the REDCap Mobile App — a native iOS and Android application that allows study team members to enter and edit record data offline from a mobile device. The app is distinct from MyCap (the participant-facing mobile application). It is intended for study staff who collect data in environments without reliable internet access, such as clinical settings, field sites, refugee settlements, rural communities, or participant homes. Data entered offline is stored locally on the device and synchronized with the REDCap server when a connection becomes available. This is the only article in the RC-MOB series.

> **Institution-specific:** Whether the REDCap Mobile App module is enabled and whether any approval or request process is required before use varies by installation. Contact your REDCap administrator to confirm local requirements.

---

## 2. Key Concepts & Definitions

### REDCap Mobile App

The official REDCap application for iOS and Android, published by Vanderbilt University. It is used by study team members (not participants) and requires a REDCap login. The app enables offline data entry for any REDCap project it has been initialized with.

### API Token

A 32-character hex string unique to a particular REDCap user's rights in a particular project. The Mobile App uses API tokens to determine which project data is accessible from the device. A single token grants access to one project with the user rights assigned to the corresponding REDCap account. Users obtain their token through the REDCap Mobile App section in the project's left-hand menu.

### QR Code / Initialization Code

Two methods for adding a project to the Mobile App on a device. After a user obtains their API token, REDCap generates a QR code they can scan with their device, or a 10-digit initialization code they can type manually. The initialization code expires after 10 minutes.

### Mobile App Admin Account

A special administrative account within the Mobile App (separate from REDCap user accounts) that manages all Mobile App users on a device. The Admin can create, update, and delete Mobile App users, reset user PINs, and grant user rights across projects. The Admin password cannot be reset — it must not be lost.

### Mobile App User

A device-level credential created by the Mobile App Admin. Each user has a unique app username and a 6-digit PIN that is separate from their REDCap server credentials. The user's REDCap project rights (form access, DAG membership) are mirrored from the server via their API token.

### App Username

The username a mobile user enters when logging into the app. This may differ from the user's REDCap server username. The action tag `@APPUSERNAME-APP` captures the app username at the time of data entry (see [RC-AT-11 — Action Tags: Mobile App Action Tags](RC-AT-11_Action-Tags-Mobile-App.md)).

### Initialize (a project)

The process of downloading a project's structure (instruments, branching logic, data dictionary) and optionally existing records to the mobile device. A project must be initialized before offline data entry can begin. Initialization requires an internet connection and uses the user's QR code or initialization code.

### Synchronize (Sync)

The process of uploading locally entered data to the REDCap server and downloading any changes made on the server since the last sync. Sync requires an internet connection and must be initiated manually by the user.

### Offline Mode

When the device has no internet connection, the app operates offline. Data entered during offline mode is stored locally and uploaded during the next sync.

### Draft Record

A record edited or created in the Mobile App that has not yet been synchronized to the server. Draft records are visible in the app and flagged as pending until sync completes.

---

> **Note (16.1.8):** The Mobile App **Dashboard** tab now shows the REDCap **username**, the **installation time**, and **latest-activity timestamps**, which makes it considerably easier to establish which device and account a given set of offline data came from.

---

## 3. REDCap Mobile App vs. MyCap vs. Browser-Based Entry

The REDCap Mobile App is one of three primary data collection interfaces in REDCap. Choosing the right interface depends on who is collecting data and under what conditions.

| Feature | REDCap Mobile App | MyCap | Browser-Based Entry |
|---|---|---|---|
| Who uses it | Study team members | Research participants | Study team members or participants |
| REDCap login required | Yes (via API token) | No | Yes (for staff); No (for survey links) |
| Installed on | Study team–owned device | Participant's personal device | Any web browser |
| Primary use case | Offline data entry at point of care | Remote, repeated participant data collection | Online data entry and survey completion |
| Works offline | Yes | Yes | No |
| Supports survey features | No (instruments treated as forms) | Yes | Yes |
| Supports active tasks | No | Yes | No |
| Longitudinal projects | Yes | Yes | Yes |

Use the REDCap Mobile App when study staff need to collect data in person at a location with unreliable or no internet (e.g., a bedside interview, a field visit, a health fair, a rural community site). Use MyCap when participants will complete assessments on their own devices over time. Use browser-based entry for all other scenarios. See [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md) for a detailed comparison of MyCap and the Mobile App.

---

## 4. Supported and Unsupported Features

### 4.1 Supported

The following REDCap features work in the Mobile App:

- Data entry on standard instruments
- Data Access Groups (DAGs) — the user's DAG from their REDCap project rights applies
- GPS field capture
- Photo capture via the device camera; photos can be synced to the server
- File Upload fields (upload only; downloaded file content is limited — see 4.2)
- Signature fields (downloaded to app for viewing when `@SYNC-APP` is applied)
- Action tags (including mobile-specific tags — see [RC-AT-11 — Action Tags: Mobile App Action Tags](RC-AT-11_Action-Tags-Mobile-App.md))
- Repeating instruments and repeating events
- Longitudinal projects (arm and event selection during data entry)
- Multi-device setups (multiple devices can access the same project simultaneously)
- Instrument securing with a PIN (see Section 6.5)
- Interface translation (buttons and instructions; instruments are not translated)

### 4.2 Not Supported

The following features are not available in the Mobile App:

- Survey-specific features: survey queue, survey instructions, stop actions, thank-you text
- Computer Adaptive Tests (CATs)
- Double data entry
- Randomization
- Inline audio/video playback
- Downloadable files stored in File Upload fields (filenames and sizes are shown, but content cannot be opened)
- Audio and video files are not downloaded to the app (even if uploaded)
- PDFs are not downloaded
- Most External Modules

> **Note:** Heavy branching logic and calculated fields can slow down form rendering in the app. Keep instruments as short as practical (fewer than 100 fields is recommended). Very long forms (1,000+ fields) can cause the app to crash. If an instrument is too long, break it into smaller instruments and use the "Save and Go to Next Instrument" workflow.

---

## 5. Administrator Setup

Before any project can use the REDCap Mobile App, a REDCap administrator must enable the Mobile App module for the server.

### 5.1 Enable the Mobile App Module

A REDCap administrator enables the Mobile App module in the REDCap Control Center under System Configuration → Modules/Services Configuration (see **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)**). Once enabled, the module becomes available to all projects on the server.

> **Institution-specific:** Whether the Mobile App module is already enabled and whether projects require administrator approval or a request form before use varies by installation. Contact your REDCap administrator to confirm.

### 5.2 Mobile App Settings in the Control Center

Administrators can configure server-wide settings including:

- **Allow users to download records to the app** — Controls whether initialization downloads existing records. When disabled, users can only create new records offline.
- **Require a PIN or biometric lock** — Enforces a device-level lock on the app.
- **Offline record limit** — Sets a maximum number of records held on a device at one time.

---

## 6. Project-Level Setup

### 6.1 Enable the Mobile App for a Project

In the project, navigate to **Project Setup** → **Enable optional modules and customizations** → check **Use the REDCap Mobile App**. This exposes the Mobile App section in the left sidebar under Applications.

> **Institution-specific:** Some institutions require a formal Mobile App request through a Help Desk form before enabling the module on a project. Confirm local procedures with your REDCap administrator.

### 6.2 Grant User Rights

Navigate to **User Rights** and grant the **REDCap Mobile App** privilege to each user who will collect data in the app. This enables the user to set up the project on a device and sync data.

An additional privilege — **Allow user to download data for all records to the app** — controls whether the user can download existing server records during initialization. Unchecking this is recommended for users who should only create new records and never access existing data on a device.

### 6.3 Obtain API Tokens

Each user navigates to **Applications** → **REDCap Mobile App** in the project and requests an API token. Once the token is generated (by the REDCap admin team at some institutions, or automatically), the user receives a notification and can access their QR code or initialization code from that same page.

> **Important:** Each user should have their own API token. Do not share a single token across multiple users or devices — doing so will merge all activity under one account and compromise the audit trail. If a single person needs to be separately identifiable across two devices, create a separate REDCap user account for each use.

### 6.4 Create Mobile App User Accounts on the Device

On the device, the Mobile App Admin account manages device-level user credentials. The Admin (typically the project administrator) creates an account for each data collector with a unique **app username** and **6-digit PIN**. These credentials are separate from REDCap server logins.

> **Critical:** The Mobile App Admin password cannot be reset. Store it securely. If it is lost, the admin account cannot be recovered.

Each app user:
- Has their own app username and PIN
- Links to their REDCap project rights via their API token
- Cannot share project copies with other users on the same device — each user maintains their own independent copy of the project

If multiple users need to access the same project, each must set up the project independently under their own account.

---

## 7. Initializing a Project on the Device

### 7.1 Install the App

Download the REDCap Mobile App from the Apple App Store (iOS) or Google Play Store (Android). Search for "REDCap" — the publisher is Vanderbilt University Medical Center.

Minimum OS requirements:
- iOS / iPadOS: version 15.0 or later for the current app (v5.31.3 on the App Store as of October 2026)
- Android: check the Google Play listing for the current minimum
- The device must support encryption. Amazon Fire devices are not supported.

The minimum OS rises over time, so check the store listing before buying or redeploying devices. A device that can't reach the required OS stays on whatever app version it last installed and stops getting fixes. Examples: the iPad Air (1st generation) can't go past iOS 12.5.x, and the iPad (5th generation) can't go past iPadOS 16.7.x. Badly outdated app and OS versions are a common cause of sync failures (see 9.7). Retire devices that can no longer run a current app version.

> **Important:** Upload all new and modified data to the server **before** updating the device's OS or the app. The app's own App Store release notes give the same advice.

### 7.2 Add a Project to the App

Log in to the app with your app username and PIN, then select **Set Up Mobile Project**. Two options are available:

- **Scan QR Code** — requires the device to have a camera and a QR code reader. The QR code is generated in the project's REDCap Mobile App section.
- **Enter Initialization Code** — a 10-digit code available from the same REDCap Mobile App section. This code expires in 10 minutes.

### 7.3 Choose What Data to Download

During initialization, the app downloads the project's data dictionary. If the project already has records, the app will offer three options:

1. Download all existing records
2. Download a partial set (filter by specific records, events, or arms)
3. Start with a blank project (no existing records downloaded)

Option 2 is useful in longitudinal studies where field staff only need records for specific sites, arms, or events. The administrator's **Allow user to download data** right must be enabled for options 1 and 2 to appear.

> **Note:** A project must be re-initialized after major structural changes (e.g., new instruments added, branching logic updated). Use **Refresh Setup & Data** after syncing to keep the local copy current.

---

## 8. Offline Data Entry

### 8.1 Entering Data

Once initialized, the app can be used without an internet connection:

1. Open the app and select the project
2. Tap **Collect Data**, then choose an instrument and a record (or create a new record)
3. Navigate through the instrument — branching logic, required fields, and validation rules all function in the app
4. Set the form status at the bottom of the instrument as needed
5. Save the record — it is stored locally as a draft until synced

For projects with auto-numbering disabled, records can be renamed on the first instrument. Renamed records will appear as new records when synced — the original record on the server must be manually deleted afterward to complete the replacement.

### 8.2 Securing an Instrument

Instruments can be secured with the user's PIN before handing the device to a participant. In secured mode, the participant can only enter data on the visible instrument and cannot browse other records or navigate elsewhere in the app. The instrument is unlocked by the user entering their PIN.

This is the standard approach when a study team member conducts a face-to-face interview where the participant self-enters answers on a portion of the instrument, or when confidentiality between the device holder and others must be maintained.

### 8.3 Supported Media During Data Entry

Photos can be captured directly from the device's camera and stored in File Upload fields. GPS coordinates can be captured in GPS fields. Audio and video files can be uploaded to file fields, but they will not be downloaded back to the app during subsequent syncs.

---

## 9. Synchronization

### 9.1 Initiating a Sync

Sync requires an active internet connection. Tap **Send Data** (or the sync button) within the project view. The app uploads all draft records and edits to the REDCap server.

### 9.2 What Happens During Sync

**New records** created in the app are added to the REDCap project immediately if no conflicts exist.

**Existing records** that were edited in the app: for projects with auto-numbering disabled, the app displays a summary of differences between the server version and the app version before confirming the upload.

**Deleted records**: deleting a record in the app does not delete it on the server. Records can only be permanently deleted from the REDCap web interface.

### 9.3 Partial Sends

A partial set of records can be sent instead of all pending drafts. This is recommended when a large number of records have accumulated and a full sync would be slow. Sending a few records at a time can also get data through a slow or unstable connection, such as a satellite link or a remote field site, where one large upload keeps dropping. The Emergency Data Dump offers the same choice through **Select records manually** (see 9.6).

### 9.4 Post-Sync Refresh

After syncing, three options are typically presented. Selecting **Refresh Setup & Data** removes all locally stored data from the device and replaces it with the most current project information from the server. This is the recommended practice after each sync session — it keeps the local copy clean and reduces the risk of stale data accumulating on the device.

### 9.5 Conflict Handling

If the same record was edited both in the app and on the REDCap server between syncs, a conflict may occur. REDCap flags the conflict for resolution. Avoid parallel editing of the same record in the app and the browser to prevent this.

### 9.6 Emergency Data Dump

If something prevents the app from syncing normally (e.g., a network error that cannot be resolved in the field), use **Send Emergency Data Dump** to export the device's data as a CSV file. It can be sent to the server, saved on the device, or both. This is a fallback mechanism; use normal sync whenever possible, because the CSV has to be reviewed and imported by hand.

**Steps in the app:**

1. Open the project in the app. On the project home screen, scroll to the bottom and tap **Send Emergency Data Dump**.
2. Choose which records to include:

| Option | Use when |
|---|---|
| **New/Modified Only** | The usual choice. Covers the records that are not yet on the server. |
| **All Records** | You're unsure which records are missing from the server. |
| **Select records manually** | You want to pick specific records, for example to send a large backlog in smaller batches. |

3. Tap **Proceed with Emergency Send**. This screen also offers to send the project logs (see 10.4).
4. Under **Choose file destination**, pick one:

| Destination | What happens |
|---|---|
| **Send to Server** | The CSV is uploaded to the project. This still needs a working, reasonably strong internet connection. |
| **Save to Device** | The CSV is written to the device only. It never reaches the server. |
| **Both** | Saves a copy on the device and also tries the upload. This is the safest choice when the connection is in doubt. |

5. A confirmation screen shows where the data went.

**Save to Device:** the app warns that the saved file is **not encrypted**, unlike the app's own storage. To get the file off the device, the app says to connect the device to a computer and look for the file in the **redcap** folder. On iOS the dump is written inside the app's documents area, in a `collector` folder, as a file named `<timestamp>.data.csv`. Treat the file as study data: move it straight to institution-approved storage, never email it, and delete the copies on the device and the computer once it's safely stored.

> **Institution-specific:** Where a saved dump may be stored (for example an institutional OneDrive), and whether unencrypted study data may sit on a device at all, depends on your institution's data security policy and your IRB protocol. Confirm with your REDCap administrator.

**On the server:** a dump sent to the server appears on the project's **REDCap Mobile App** page (left-hand menu, under Applications) on the **App Data Dumps** tab. Logs sent with it appear on the **App Logs** tab. Earlier versions of this article called this area the **Mobile App File Archive**. **Import Data from File** imports the dump into the project. Always review the data before you confirm the import, so that no existing fields are overwritten. This matters most in projects with auto-numbering, where record IDs created offline can collide with records already on the server. A dump saved to the device and brought in by hand is imported through the Data Import Tool with the same care (see [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md)).

> **Critical:** Do not run **Refresh Setup & Data** on the device until you have confirmed the data is on the server, through a sync or an imported dump. A refresh permanently erases the data stored on the device.

### 9.7 Troubleshooting a Failed Sync

**Error: "Uploading the document has failed"** with a detail line like `{"code":3,"source":"file:///…/collector/<timestamp>.data.csv",…}` and `fids.length === 0`. The connection failed before the server answered: the upload started, the connection dropped or was refused, and the server never returned a file ID. The same error can appear for a normal sync and for **Send to Server** in the Emergency Data Dump.

**Check whether the requests reach the server.** Open the project's **Logging** page (see [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md)) and filter on the app user's username. A successful sync first logs **Export REDCap version (API)**, **Export project information (API)** and **Download data dictionary (API)**, then **Create record (API)** and **Update record (API)** entries for the uploaded records. If none of these appear around the failed attempts, the requests never reached REDCap, and the problem is on the device or the network, not in the project.

**Likely causes, most common first:**

1. **Outdated app and OS.** An old app version, or an OS too old to run a current one, can lose the ability to connect securely to an updated server. The device shows it's online, but every upload fails before reaching REDCap. Compare the app version shown in the app (top right of the screen, or under Settings) with the current store version, and check the device's OS against the app's minimum (see 7.1).
2. **Network blocking or unstable links.** Firewalls, regional filtering, or slow and unstable connections (satellite, remote field sites) can block or drop the upload. Try a different network or an institutional VPN, and send records in smaller batches (see 9.3).
3. **Rights or token changes.** Check that the user still has the **REDCap Mobile App** privilege and access to every instrument, and that the account isn't expired or suspended (see 6.2). Also check the device list on the Mobile App page to make sure the device hasn't been blocked (see 10.2).

**Recovery order when the app or OS is the cause:**

1. Run an Emergency Data Dump with **Save to Device** or **Both** (see 9.6), and copy the file to institution-approved storage.
2. Confirm the file is complete before anything else changes on the device.
3. Update the OS, then the app, and try a normal sync.
4. If the device can't be updated, import the saved dump instead, and retire the device from data collection.

Don't delete or reinstall the app, remove the project, log out, or run **Refresh Setup & Data** at any point in this process. Records that haven't synced exist only on the device.

---

## 10. Device Management and Activity Logging

### 10.1 Device List and Nicknames

The Mobile App page in the REDCap project (under Applications) displays a list of all devices that have access to the project. Each device is identified by a UUID. Devices can be given a nickname (e.g., "Kenya tablet 1", "Rob's iPhone") to make activity tracking meaningful. Nicknames appear in the activity tables, dashboard, and file download tables.

### 10.2 Per-Device Blocking

Individual devices can be blocked from accessing the project without revoking the API token entirely. This is useful if a single device is lost or stolen while other devices using the same project should continue operating.

### 10.3 Remote Lockout

Two levels of remote lockout are available:

**Suspend access (reversible):** Revoke the **REDCap Mobile App** privilege in User Rights. The user can no longer access the project on their device, but data already synced to the server is preserved. This can be reversed by restoring the privilege.

**Permanent lockout:** Delete the user's API token. This permanently prevents any future access. Data already synced to the server is preserved, but any data still stored locally on the device that has not yet been synced will be lost.

> **Note:** If a device is physically stolen, revoking or deleting the token prevents future syncs and downloads — but it does not remotely wipe data already on the device. For true remote wipe capability, use a Mobile Device Management (MDM) system.

### 10.4 Activity Log

Mobile App activity logs sent from a device appear on the **App Logs** tab of the project's REDCap Mobile App page (earlier versions of this article called this area the **Mobile App File Archive**). The log records:

- Record creation, modification, and uploads
- Record renaming, deletion, and viewing
- Downloads of project instruments and records

Logs can be transmitted to the server from within the app by tapping **Send Project Logs**. Logs can be viewed in the REDCap web interface without downloading.

---

## 11. Security Considerations

The REDCap Mobile App stores project data locally on the device, introducing risks that do not apply to browser-based access.

**Encrypted storage:** REDCap Mobile App encrypts locally stored data at rest. The device itself must support encryption (devices that do not support encryption cannot use the app).

**PIN lock and biometrics:** The app supports a numeric PIN lock and biometric authentication (Face ID / fingerprint) to prevent unauthorized access if the device is unattended.

**Use study team–owned, managed devices:** Because data is stored locally, the Mobile App should be used only on study team–owned and managed devices, not personal devices. This is the fundamental distinction from MyCap, which runs on participants' personal phones.

**Separate API tokens per user:** Sharing a single API token across users or devices eliminates individual audit trail entries and makes it impossible to attribute records to a specific person. Each user must have their own token.

**IRB and data governance:** Consider whether your IRB protocol needs to address Mobile App usage specifically. Write the Mobile App protocol into your IRB application if required at your institution.

> **Institution-specific:** IRB or institutional data security requirements may mandate additional controls for devices running the REDCap Mobile App, such as MDM enrollment or full-disk encryption. Confirm requirements with your IRB and REDCap administrator.

---

## 12. Best Practices

- **Designate a point of contact** for the Mobile App setup and for field data collectors. If these are different people, the field manager needs to be as well trained as the person who set up the project.
- **Test the project on the app before deployment.** Form layout and field rendering look different in the app than in the browser. Check validated forms and instruments with complex branching logic for significant visual changes.
- **Develop a contingency plan** in case the app fails in the field (e.g., device battery dies, app crashes, initialization code expires). Define the fallback procedure — paper forms, browser access via a hotspot — before data collection begins.
- **Label devices** in the project with meaningful nicknames so the activity log is interpretable.
- **Sync and refresh frequently.** At minimum, sync at the start and end of each data collection session. Run Refresh Setup & Data after every sync to keep local copies clean.
- **Keep instruments short.** Forms with more than ~100 fields perform noticeably worse in the app. Break long instruments into smaller ones.
- **Avoid heavy branching logic or many calculated fields** in mobile instruments if rendering speed is a concern.
- **Re-initialize after data dictionary changes.** Any change to instruments, fields, or branching logic on the server must be followed by a re-initialization on each device before those changes take effect.

---

## 13. Common Questions

**Q: What is the difference between the REDCap Mobile App and MyCap?**

**A:** The REDCap Mobile App is for study team members. It requires a REDCap login and API token and is installed on study team–owned devices for offline staff data entry at the point of care. MyCap is for research participants. It is installed on the participant's personal device and designed for repeated, participant-reported data collection over time. They serve different audiences and different workflows. See [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md) for a detailed comparison.

**Q: How does a user add their project to the app?**

**A:** The user navigates to the REDCap Mobile App section in the project's left-hand menu and requests an API token. Once the token is issued, a QR code and a 10-digit initialization code become available. The user opens the app on their device, selects Set Up Mobile Project, and either scans the QR code or enters the initialization code. The initialization code expires after 10 minutes.

**Q: What happens if the admin password is forgotten?**

**A:** The Mobile App Admin password cannot be reset. It is permanently lost if not recorded. The Admin account must be set up again from scratch, which means all device-level user accounts and project setups must be recreated. Store the Admin password in a secure, accessible location before any data collection begins.

**Q: Can multiple devices use the same project simultaneously?**

**A:** Yes. Multiple devices can initialize and collect data for the same project at the same time, as long as each device user has their own API token. Avoid having two devices share a single API token — this merges all activity under one account and risks conflicting sync operations.

**Q: Does the REDCap Mobile App work with longitudinal projects?**

**A:** Yes. Longitudinal projects are supported. During data entry, the user selects the event as they would in the browser. During initialization, users can choose to download only specific arms or events, which is useful when field staff work at one site within a multi-site longitudinal study.

**Q: Can the app be used with surveys?**

**A:** The Mobile App does not support survey features (survey queue, stop actions, thank-you text, survey instructions, pagination, etc.). Survey instruments appear in the app as regular data entry forms. If participant-facing surveys are needed on a mobile device, use MyCap or send a survey link that opens in a mobile browser.

**Q: What happens if I lose the device before syncing?**

**A:** Any data entered since the last sync will be lost along with the device. Sync frequently — at the end of every data collection session. Data that was previously synced is safe on the REDCap server. If the device was stolen, delete or revoke the API token immediately to prevent unauthorized access.

**Q: What features do not work in the Mobile App?**

**A:** Survey-specific features, Computer Adaptive Tests, double data entry, randomization, inline audio/video, survey queue, downloadable files from file fields, and most External Modules are not supported. See Section 4 for the complete list.

**Q: Can repeating instruments and events be used?**

**A:** Yes. Repeating instruments and repeating events work in the app the same way they do in the browser — users can add new instances during offline data entry.

**Q: What is the Emergency Data Dump?**

**A:** Emergency Data Dump is a fallback for when normal sync fails, for example because of a persistent network error in the field. The user taps **Send Emergency Data Dump**, chooses which records to include, and picks a destination: **Send to Server**, **Save to Device**, or **Both**. A dump sent to the server appears on the **App Data Dumps** tab of the project's REDCap Mobile App page, and has to be reviewed and imported by hand. Use normal sync whenever possible. See 9.6.

**Q: Can I get the data off the device if neither sync nor the emergency data dump will upload?**

**A:** Yes. Run the Emergency Data Dump and choose **Save to Device** (or **Both**). The CSV is written to the device without contacting the server. Connect the device to a computer, find the file in the app's **redcap** folder, and copy it to institution-approved storage. The file is not encrypted, so handle it as study data. It's then imported into the project after review. See 9.6.

**Q: What does "Uploading the document has failed … code 3 … fids.length === 0" mean?**

**A:** The upload failed at the connection level, and the server never returned a file ID. Check the project's Logging for the app user. If no API entries appear around the failed attempts, the requests never reached REDCap. The usual causes are a badly outdated app or OS, or the network. See 9.7.

**Q: Is it safe to update the iPad or the app while there is unsynced data on it?**

**A:** Get the data off the device first, through a successful sync or an Emergency Data Dump saved to the device and copied somewhere safe. The app's release notes recommend uploading all new and modified data before an OS update. Only update once the data is confirmed. See 7.1 and 9.7.

---

## 14. Common Mistakes & Gotchas

**Forgetting to sync before ending a session.** Data in the app is not transmitted to the server until sync is manually triggered. Staff who close the app or leave a site without syncing risk data loss if the device is damaged, lost, or reset. Build sync into end-of-session workflows as a required step, and run Refresh Setup & Data afterward.

**Sharing a single API token across multiple users or devices.** This eliminates individual audit trail entries and merges all data creation under one account. If the token is revoked, all devices using it lose access simultaneously. Each user must have their own API token tied to their own REDCap account.

**Losing the Mobile App Admin password.** The Admin password cannot be reset. If lost, the admin account is permanently inaccessible and all device-level user accounts must be recreated from scratch. Store this password securely before any data collection begins.

**Editing the same record in the browser and the app simultaneously.** If a record is saved in the REDCap web interface while a draft of that same record also exists in the app, a conflict will occur on the next sync. REDCap will flag it for resolution, but resolving conflicts adds administrative burden. Coordinate data entry so only one interface edits a record at a time.

**Not re-initializing after data dictionary changes.** Adding new fields, instruments, or branching logic on the server does not automatically update the app. Mobile users working with an outdated copy will not see new fields and may save incomplete data. Re-initialize (or use Refresh Setup & Data) after every data dictionary change.

**Using personal devices for app data collection.** The Mobile App stores PHI or sensitive study data locally on the device. Using personal devices is a data security risk and may violate IRB or institutional data governance policies. Always use study team–owned, managed devices.

**Running Refresh Setup & Data after a failed sync.** Refresh is routine after a *successful* sync, so staff may run it out of habit. After a failed sync it permanently erases every record that hasn't reached the server. When a sync fails, stop, run an Emergency Data Dump to the device, and refresh only once the data is confirmed on the server.

**Updating the OS or the app to fix a sync problem before the data is safe.** An outdated app or OS is often the cause, so updating looks like the obvious fix. But an update is a change to the device while unsynced data sits on it. Save an Emergency Data Dump to the device and copy it to safe storage first, then update.

**Keeping devices that can no longer run a current app version.** Devices stuck on an old OS (for example iOS 12) can't install current app releases. Sooner or later they stop syncing with an upgraded server, and that tends to happen at a remote site with weeks of data on them. Check the app's minimum OS when assigning devices, and retire devices that fall below it.

**Renaming records without understanding the consequence.** For projects with auto-numbering disabled, renaming a record in the app causes it to appear as a new record on sync. The original record on the server must then be manually deleted. If users rename records without following this cleanup step, duplicate records will accumulate on the server.

---

## 15. Related Articles

- [RC-AT-11 — Action Tags: Mobile App Action Tags](RC-AT-11_Action-Tags-Mobile-App.md) (`@APPUSERNAME-APP`, `@BARCODE-APP`, `@SYNC-APP`, `@HIDDEN-APP`, `@READONLY-APP`)
- [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md) (participant-facing mobile app; MyCap vs. REDCap Mobile App comparison)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md)
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG support in the Mobile App mirrors the user's server-side DAG assignment)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (system-level Mobile App enable/disable and server-wide settings)
- [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md) (importing an Emergency Data Dump CSV)
- [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) (checking whether app sync requests reach the server)
