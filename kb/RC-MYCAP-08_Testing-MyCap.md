RC-MYCAP-08

**MyCap: Testing**

| **Article ID** | RC-MYCAP-08 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | Projects with MyCap enabled; pre-launch testing phase |
| **Prerequisite** | RC-MYCAP-02 — Designing Instruments for MyCap; RC-MYCAP-03 — Task Scheduling |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-MYCAP-04 — Participant Onboarding; RC-MYCAP-05 — App Settings & Participant Management |

---

# 1. Overview

This article provides a structured testing workflow for MyCap projects before launching to real participants. Testing MyCap requires a mobile device and a test record in the REDCap project. The six-step process covers task appearance and functionality, App Settings, schedule behavior, notifications, joining methods, and a final publish before go-live. Complete all six steps before enrolling the first real participant.

---

# 2. Key Concepts & Definitions

**Test Record**

A REDCap record created specifically for testing purposes. Use a test record (e.g., record ID "TEST-001") to join the app as a simulated participant. Do not use real participant records for testing.

**Test Device**

A physical iOS or Android device used to test the MyCap app. Testing in a browser or simulator is not sufficient — MyCap must be tested on an actual mobile device.

**View Task Details (CSV)**

A download available in the MyCap Schedule Tasks interface that lists all scheduled task instances for the project. Used to verify that the schedule logic is generating the correct task windows.

**Infinite Schedule (for testing)**

Setting a task to Infinite during development allows the tester to trigger and complete the task at any time, without waiting for a scheduled window. Switch to the real schedule type before final publish.

**Task Notification**

A push notification delivered to the device at the configured notification time (default 8:00 AM) when a new task instance becomes available. Must be tested on a real device with push notifications enabled.

---

# 3. Pre-Testing Setup

Before beginning the six-step test:

1. **Create a test record** in the REDCap project (e.g., record ID "TEST-001" or similar).
2. **Install the current MyCap app** (purple logo) on the test device.
3. **Enable the test project** in MyCap and publish the initial version.
4. **Join the project on the test device** using the test record's App Link or QR Code (see RC-MYCAP-04 — Participant Onboarding for joining instructions).

---

# 4. Step 1: Task Appearance and Functionality

Verify that each enabled task appears correctly in the app and can be completed.

### 4.1 Set Tasks to Infinite for Testing

To test task functionality without waiting for scheduled windows, temporarily set all tasks to the **Infinite** schedule type. This makes all tasks immediately available in the app.

1. Go to **MyCap > Schedule Tasks**.
2. For each task, change the schedule to **Infinite**.
3. Publish the project.

### 4.2 Complete Each Task

On the test device:
- Open MyCap and verify the task list shows all enabled tasks.
- Complete each task, checking:
  - Field types display correctly (dropdowns, sliders, text boxes, etc.).
  - MyCap annotations behave as expected (`@MC-FIELD-SLIDER-BASIC`, `@MC-FIELD-FILE-IMAGECAPTURE`, etc.).
  - Branching logic within instruments functions correctly.
  - No piping syntax (`[field_name]`) appears as raw text in field labels or notes.
  - Task completes and is marked done after submission.

### 4.3 Review Task Details CSV

To audit the full scheduled task list:
1. Go to **MyCap > Schedule Tasks**.
2. Click **View Task Details** to download the CSV.
3. Verify the schedule logic is generating the correct task windows, dates, and frequencies for each record.

---

# 5. Step 2: App Settings Appearance

Verify that the App Settings display correctly in the app.

On the test device, navigate to the project's information section in MyCap and check:
- **About pages** display the correct images at the correct resolution.
- **Contacts** show the correct contact information.
- **Links** are present and navigate to the correct URLs (verify that any appended project/participant codes are included if configured).
- **Theme** (iOS only) applies the correct color scheme.

If any App Settings are incorrect, update them in REDCap and publish again before retesting.

---

# 6. Step 3: Schedule Testing

Verify that task scheduling works correctly, with particular attention to whether you are using install date or baseline date.

### 6.1 Testing Install-Date Schedules

- The install date is set when the test record joins the app.
- Set the schedule back to the real schedule (not Infinite) and publish.
- Check the View Task Details CSV to confirm task windows align with the expected days-after-install.
- If you need to test the schedule from a different install date, remove the test record from the app (delete or reset the participant code), create a new record, and rejoin.

### 6.2 Testing Baseline-Date Schedules

1. In the test record in REDCap, set the baseline date field to a known date (e.g., today's date minus 7 days, to simulate a past baseline event).
2. Open the app. Verify that the baseline date screen appears and prompts correctly, or is bypassed because the date was pre-filled.
3. Check that tasks scheduled relative to the baseline date appear at the correct offsets.
4. Test the "Did this happen today?" prompt by not pre-filling the baseline date in REDCap and letting the app ask the participant.
5. Test the "Enter the date" prompt by answering "No" to the today question and verifying the date-picker appears.

> **Note:** If you pre-fill the baseline date in REDCap before the participant joins, the app will not prompt the participant — it uses the stored date directly. Test both flows (pre-filled and participant-entered) to verify both work correctly.

---

# 7. Step 4: Notification Testing

Verify that push notifications are delivered at the expected time.

### 7.1 Enabling Push Notifications

- Ensure push notifications are enabled for the MyCap app on the test device (device settings > notifications > MyCap).
- Confirm the notification time in **MyCap > App Settings > Notification Settings**.

### 7.2 Testing Task Notifications

Task notifications are sent when a new task window opens (i.e., at the configured notification time on the day the task becomes available). To test:
1. Set a task to a One-Time schedule with a delay of 0 days (or set it to appear today).
2. Publish.
3. Wait for the notification time (default 8:00 AM). The device should receive a push notification.

Alternatively, change the notification time to a few minutes from now to test without waiting until 8:00 AM.

### 7.3 Testing Message Notifications

1. In **MyCap > Participant Management**, send a direct message to the test participant record.
2. Verify the device receives a push notification and the message appears in the MyCap app's message inbox.

### 7.4 Testing Announcement Notifications

1. In **MyCap > Participant Management**, send a broadcast announcement.
2. Verify the device receives the push notification and the announcement appears in the app.

---

# 8. Step 5: Joining Method Testing

Verify that both joining methods work before distributing them to real participants.

### 8.1 Testing App Link Joining

1. Use a second test record (separate from the one used in steps 1–4) or reset the first test record's participant code.
2. From Participant Management, copy the App Link for the test record.
3. Send the link to the test device (e.g., by email or messaging app).
4. Tap the link on the test device. Verify:
   - If MyCap is installed: the app opens and enrollment completes.
   - If MyCap is not installed: the device is redirected to the appropriate app store.
5. After installing and joining, verify the correct record appears in the app.

### 8.2 Testing QR Code Joining

1. From Participant Management, display or download the QR code for a test record.
2. On the test device, open MyCap and tap **Scan QR Code**.
3. Scan the QR code. Verify enrollment completes and the correct project and tasks appear.

---

# 9. Step 6: Final Publish Before Go-Live

After all testing is complete:

1. **Revert all test schedules** back to the real schedule types (change from Infinite to the intended schedule, adjust delays, etc.).
2. **Review the full configuration** one final time: enabled instruments, schedules, App Settings, FDL conditions (if used), MLM translations (if used).
3. **Publish the final version** in **MyCap > Publish MyCap Version**.

The project is now ready for real participant enrollment.

---

# 10. Common Questions

**Q: Can I test MyCap in a web browser or simulator?**

**A:** No. MyCap must be tested on a real iOS or Android device. Browser-based testing is not possible for MyCap, and iOS/Android simulators do not fully replicate the push notification behavior and sensor access needed for complete testing.

**Q: How do I test the schedule without waiting for days to pass?**

**A:** Use the Infinite schedule type during testing to make all tasks available immediately. For schedule-specific testing, use the View Task Details CSV to verify the schedule logic, then set a One-Time task with a delay of 0 and wait one notification cycle (or temporarily change the notification time).

**Q: Should I use a real participant's record for testing?**

**A:** No. Always use a dedicated test record. Using a real participant's record for testing risks creating false data, triggering unintended alerts, or confusing the participant's task history.

**Q: How do I reset the test between testing runs?**

**A:** Delete the test record from the app (log out from the MyCap app or remove the project), and either create a new test record in REDCap or reset the existing one. For baseline date testing, clear the baseline date field in REDCap before the second test run.

**Q: Do I need to test every instrument individually?**

**A:** Yes, for the first full test. Test each enabled instrument to confirm it displays correctly, all field types render properly, and the task completes and syncs. For subsequent publishes after minor changes, you only need to test the changed components.

**Q: What do I do if a task does not appear during testing?**

**A:** Check in this order: (1) Is the instrument enabled for MyCap? (2) Was the project published after enabling? (3) Is there an FDL condition blocking the task? (4) Has the test device synced with the REDCap server (internet connection required)?

---

# 11. Common Mistakes & Gotchas

**Testing on a simulator instead of a real device.** Simulators do not support push notifications and may not accurately replicate how MyCap handles device sensors. Always test on a physical iOS or Android device.

**Forgetting to revert Infinite test schedules before the final publish.** A common pre-launch error: the project goes live with tasks set to Infinite instead of the intended schedule. Double-check all schedule types in the final review before publishing.

**Not testing both joining methods.** Studies that only test one joining method (e.g., only QR) may discover problems with the other (e.g., App Links using deprecated Firebase domains) only after participants have been sent broken links.

**Using a real participant record for testing.** Test records create false data, trigger alerts to real participants, and make it difficult to clean up after testing. Create and use a dedicated test record from the start.

**Not testing baseline date on a separate device from the join device.** If the same device was used to join with a pre-filled baseline date, you may not discover that the participant-entry flow (where the app asks the participant for their baseline date) has a problem. Test both flows explicitly.

**Not verifying that notifications are enabled on the test device.** Push notifications must be explicitly allowed in the device's system settings for MyCap. If the device was set up with notifications off, notifications tests will fail silently. Check device notification settings before beginning Step 4.

---

# 12. Related Articles

- RC-MYCAP-02 — Designing Instruments for MyCap (publishing workflow)
- RC-MYCAP-03 — Task Scheduling (schedule types, View Task Details CSV)
- RC-MYCAP-04 — Participant Onboarding (App Link and QR Code joining)
- RC-MYCAP-05 — App Settings & Participant Management (notification settings, message testing)
- RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links (testing FDL and Survey Links)
