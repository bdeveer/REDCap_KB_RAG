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
