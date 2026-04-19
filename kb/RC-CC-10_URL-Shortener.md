RC-CC-10

**URL Shortener**

| **Article ID** | RC-CC-10 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-01 — Notifications & Reporting |

---

# 1. Overview

The URL Shortener creates short redirect links for distribution. This service is provided externally and is hosted outside the local REDCap server. It is accessible from the Administrator Resources section of the Control Center sidebar.

# 2. Option 1: Random Short URL

The Random Short URL option generates a randomly assigned short URL that redirects to any destination URL you provide. This option is useful when you need a quick shortened link without requiring a specific custom alias.

To use this feature:
1. Navigate to the URL Shortener tool in the Control Center
2. Select the "Random Short URL" option
3. Enter the full destination URL you wish to shorten
4. The system will generate a short URL with a random alphanumeric string
5. Copy and distribute the shortened URL as needed

# 3. Option 2: Custom Alias

The Custom Alias option allows administrators to define a custom alphanumeric string for the short URL, so the shortened link takes a memorable form. The custom portion must be unique and not already in use by another shortened URL.

To use this feature:
1. Navigate to the URL Shortener tool in the Control Center
2. Select the "Custom Alias" option
3. Enter the full destination URL
4. Define your desired custom alias (alphanumeric characters only; special characters and spaces are not permitted)
5. The system validates that your alias is not already in use
6. If validation passes, the custom shortened URL is created and ready to share

# 4. Use Cases

Common uses for the URL Shortener include:

- **Survey participation links**: Shorten long survey distribution links for inclusion in emails, printed flyers, or SMS messages
- **Memorable URLs**: Create branded or easy-to-remember links for frequently shared REDCap pages or resources
- **Embedding in communications**: Use shortened URLs in contexts where long URLs are impractical or difficult to share (e.g., printed materials, verbal communication, character-limited platforms)
- **QR codes**: Pair shortened URLs with QR codes for in-person enrollment or data collection campaigns

# 5. Limitations

Since the shortening service is managed externally and not by the local institution, the availability and reliability of the service depend on the external provider's infrastructure. There is no guarantee of permanent link persistence beyond what the service provider maintains. It is recommended to:

- Test shortened URLs before widely distributing them
- Maintain a record of the original long URLs in case shortened links become unavailable
- Be aware that the external service may change policies or discontinue service without warning

---

# 6. Common Questions

**Q: What is the difference between a random short URL and a custom alias?**
A random short URL is generated automatically with a random alphanumeric string and requires no additional input from you. A custom alias lets you specify a memorable alphanumeric string to make the URL more recognizable and easier to share verbally. Both redirect to the same destination URL.

**Q: Can I use special characters or spaces in a custom alias?**
No. Custom aliases accept alphanumeric characters only. Spaces and special characters (hyphens, underscores, slashes, etc.) are not permitted. Choose a simple, easy-to-remember alias using only letters and numbers.

**Q: What happens if the custom alias I want is already in use?**
The system will notify you that the alias is unavailable. You must choose a different alias. If a specific alias is important for your project, try to create it early before others claim it.

**Q: Can I edit or change a shortened URL after it has been created?**
Typically, shortened URLs cannot be edited once created. If you need to change the destination URL, you would need to create a new shortened URL. Always test a shortened URL before distributing it widely to catch errors before they are shared.

**Q: Are shortened URLs tracked or can I see how many people have used them?**
The external shortener service may offer analytics (click counts, referrer information, etc.), but this depends on the service provider. Most external shorteners maintain basic analytics. Contact your REDCap administrator or the service provider for information about accessing these analytics.

**Q: How long do shortened URLs remain active?**
Shortened URLs remain active as long as the external service maintains them. Since the service is external and not under your institution's control, there is no guaranteed lifespan. It is best to maintain records of the original long URLs in case you need to recreate shortened links or switch services.

# 7. Common Mistakes & Gotchas

**Distributing untested shortened URLs.** Always test a newly created shortened URL to ensure it redirects to the correct destination before sharing it widely. A small typo in the destination URL can create a broken shortened link that is difficult to identify later. Test on multiple devices and browsers to confirm correct behavior.

**Assuming shortened URLs are permanent.** Because the shortener is an external service, it is not guaranteed to persist indefinitely. Do not rely solely on shortened URLs for critical, long-term links (e.g., permanent documentation or archival references). Always maintain the original long URL as a backup.

**Losing track of what shortened URLs point to.** If you create many shortened URLs, it is easy to forget which ones are in use and what they redirect to. Maintain a spreadsheet or document that maps shortened URLs (both random and custom aliases) to their destination URLs and their purpose. This is invaluable if you need to troubleshoot broken links or decommission surveys.

**Custom aliases that are too similar to other URLs.** If you create a custom alias that is similar to other institutional URLs or common typos, users may become confused. Choose aliases that are clearly distinct from existing URLs at your institution, and avoid common misspellings.

# 8. Related Articles

- RC-CC-01 — Notifications & Reporting
