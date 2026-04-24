RC-SENDIT-01

**Send-It: Secure File Transfer**

| **Article ID** | RC-SENDIT-01 |
|---|---|
| **Domain** | Send-It |
| **Applies To** | All REDCap users (requires Send-It to be enabled by a system administrator) |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-MSG-01 — REDCap Messenger; RC-CC-05 — Control Center: File Storage & Upload Settings |

---

# 1. Overview

Send-It is a secure file transfer application built into REDCap that allows users to upload a file and distribute download access to multiple recipients via email. It is designed for two scenarios: sharing files that are too large to attach to a conventional email, and sharing files that contain sensitive data and therefore should not pass through external email systems. Send-It must be enabled by a system administrator before it appears in the navigation for any user.

---

# 2. Key Concepts & Definitions

**Send-It**

A standalone REDCap feature — not tied to any specific project — that allows a logged-in user to upload a file and send unique, password-protected download links to one or more recipients. The file is stored securely on the REDCap server and automatically deleted after the expiration period.

**Recipient**

Any individual whose email address is entered in the Send-It form. Recipients do not need to have a REDCap account. Each recipient receives their own pair of emails and a unique download URL.

**Two-Email Security Model**

Send-It delivers access credentials in two separate emails for added security: the first email contains the unique download link, and the second email (sent separately) contains the password required to access that link. This separation means that access to a single intercepted email is not sufficient to download the file.

**Expiration**

The number of days the file remains available for download after it is uploaded. After the expiration date, the file is removed from the server and can no longer be downloaded. The sender sets this at upload time.

**Download Confirmation**

An optional setting that causes the sender to receive an email notification each time a recipient downloads the file.

---

# 3. Accessing Send-It

Send-It appears as a link in the main REDCap navigation bar (labeled **Send-It**) when it is enabled on your institution's REDCap instance. It is a system-level feature, not project-specific — it is accessible from any page in REDCap, not just from within a project.

If you do not see a Send-It link in the navigation, the feature has not been enabled by your system administrator. Contact your REDCap administrator to request that it be turned on.

---

# 4. Using Send-It

## 4.1 Opening the Send-It Form

Click the **Send-It** link in the top navigation bar. This opens the Send-It upload form.

## 4.2 Form Fields

| **Field** | **Required** | **Notes** |
|---|---|---|
| From | Yes (auto-populated) | Your registered REDCap email address. If you have multiple emails associated with your account, you can select which one to send from. |
| To (Recipients) | Yes | One or more recipient email addresses. Separate multiple addresses with commas, semicolons, or line breaks. Recipients do not need REDCap accounts. |
| Email Subject | No | A custom subject line for the notification emails sent to recipients. If left blank, REDCap uses a default subject. |
| Email Message | No | Optional additional text included in the notification email. Useful for providing context about the file. |
| Expiration | Yes | Number of days before the file is deleted and download links expire. Options range from 1 to 14 days; the default is 3 days. |
| File | Yes | The file to upload. Maximum size is 512 MB. Certain file types are blocked (see Section 5). |
| Receive Confirmation | No | Check this box to receive an email notification each time one of your recipients downloads the file. |

## 4.3 Submitting the Form

After completing the form, click **Send It!**. REDCap will upload the file and then dispatch two emails to each recipient:

1. **Email 1** — Contains a unique download URL specific to that recipient.
2. **Email 2** — Contains the password needed to access the download URL.

Both emails must be received for a recipient to successfully download the file. The two-email model is intentional: it provides an additional layer of security over sending a link and password in a single message.

> **Note:** If a large file is being uploaded, the page may take some time to process after clicking Send It. Do not navigate away or close the browser until the upload confirmation appears.

---

# 5. File Type Restrictions

Certain file types are blocked from upload due to security policy. Blocked extensions include executable and script formats such as `.exe`, `.bat`, `.cmd`, `.js`, `.php`, `.ps1`, `.vbs`, `.dll`, `.msi`, and others. Attempting to upload a blocked file type will display an error message and the upload will not proceed.

The full list of blocked extensions is configured at the system level by the REDCap administrator and may vary by institution.

---

# 6. File Expiration and Deletion

Files uploaded via Send-It are stored on the REDCap server temporarily. The sender selects an expiration period of 1–14 days at upload time. After that period:

- The file is permanently deleted from the server.
- Existing download links for that file stop working.
- Recipients who have not yet downloaded the file will no longer be able to do so.

There is no way to extend the expiration after a file has been uploaded. If a file needs to remain accessible longer, it must be re-uploaded with a new expiration window.

---

# 7. Common Questions

**Q: Do recipients need a REDCap account to download a file sent via Send-It?**

**A:** No. Recipients only need access to the two emails Send-It sends them. The download page is publicly accessible to anyone with the correct link and password.

**Q: Can I send the same file to multiple people at once?**

**A:** Yes. Enter multiple email addresses in the To field, separated by commas, semicolons, or line breaks. Each recipient receives their own unique download URL and password pair.

**Q: What happens if a recipient loses one of the two emails?**

**A:** The download link and the password are each delivered in separate emails. If a recipient cannot locate both emails, they will not be able to complete the download. In this case, you would need to re-upload the file and send new links. There is no way to resend individual emails from within Send-It.

**Q: Can I cancel or delete an upload before it expires?**

**A:** There is no user-facing option to manually delete an uploaded file before its expiration date. If a file was sent in error, contact your REDCap administrator.

**Q: How large can the file be?**

**A:** The maximum file size is 512 MB. Files larger than this cannot be uploaded via Send-It.

**Q: Will I know when recipients download the file?**

**A:** Only if you check the **Receive Confirmation** checkbox before submitting the form. If checked, you will receive an email each time any one of your recipients downloads the file.

**Q: Send-It doesn't appear in my navigation. How do I get access?**

**A:** Send-It must be enabled at the system level by a REDCap administrator. If you do not see the link, contact your local REDCap support team.

---

# 8. Common Mistakes & Gotchas

**Navigating away during upload.** Large file uploads can take time to complete. If you click away or close the browser tab before the confirmation appears, the upload may fail silently. Wait for REDCap to confirm the submission before leaving the page.

**Expecting a single email to recipients.** Send-It sends two separate emails per recipient by design. Users sometimes assume the second email is a duplicate or spam and delete it — without it, the download link cannot be used. When advising recipients, let them know to expect two emails.

**Setting too short an expiration window.** The default is 3 days. If you are sending to recipients who may not check email promptly, consider selecting a longer expiration window (up to 14 days) when uploading.

**Attempting to send executable or script files.** Common file types like `.exe`, `.bat`, `.js`, and `.php` are blocked. If your workflow requires sharing files of this type, you will need to compress them into a `.zip` archive first and confirm that the archive format itself is permitted.

**Assuming Send-It is project-scoped.** Send-It is a system-level tool. It does not require a project and is not linked to any project's data or audit log. Files transferred via Send-It are not stored in any project's File Repository.

---

# 9. Administrator Notes

Send-It is enabled or disabled at the system level in the Control Center under **Modules/Services Configuration**. When enabled, it appears in the navigation for all logged-in REDCap users. There is no per-user or per-project toggle.

File upload size limits and blocked file types are configurable at the system level. Defaults are set by Vanderbilt and can be adjusted by system administrators.

---

# 10. Related Articles

- RC-MSG-01 — REDCap Messenger (for secure messaging between REDCap users within the platform)
- RC-CC-05 — Control Center: File Storage & Upload Settings (for administrator-level file upload configuration)
- RC-CC-06 — Control Center: Modules & Services Configuration (where Send-It is enabled/disabled)
