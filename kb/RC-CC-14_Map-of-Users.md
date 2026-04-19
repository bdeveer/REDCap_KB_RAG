RC-CC-14

**Map of Users**

| **Article ID** | RC-CC-14 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-12 — User Activity Log; RC-CC-13 — User Activity Graphs; RC-CC-15 — Top Usage Report |

---

# 1. Overview

The Map of Users displays a geographic map showing where users are accessing REDCap from, based on their IP addresses. It is accessible under "Dashboards & Activity" in the Control Center sidebar and uses Google Maps to render the visualization. This tool provides a visual summary of user distribution and activity patterns across geographic regions.

# 2. How It Works

REDCap resolves user IP addresses to approximate geographic coordinates using an IP geolocation service. IP addresses are processed in batches (asynchronously) to avoid long page load times. A progress counter updates as batches complete, showing the number of IPs processed. This asynchronous approach ensures the page remains responsive while geolocation data is being collected and mapped.

# 3. Time Window

The map shows user activity within a configurable time window (in hours). Adjusting this parameter allows viewing recent activity (e.g., past hour) or broader activity patterns (e.g., past 24 hours). This flexibility helps administrators focus on specific time periods of interest, such as recent unusual activity or typical usage patterns.

# 4. Map Markers

Active users appear as blue pin markers on the map. Clicking a marker opens an info window with details about the user, such as username and activity context. This interactive feature allows administrators to drill down from the map view to understand who is accessing REDCap from specific locations.

# 5. Limitations and Privacy Considerations

IP geolocation is approximate — it identifies a general geographic area, not a precise location. Accuracy varies by IP type:
- Institutional networks often map to a central campus location
- VPN users may appear at the VPN exit point rather than their actual location
- Mobile users may show approximate locations based on their ISP's service area

Administrators should be aware of any institutional privacy policies before sharing or acting on geographic user data. The data should be treated with appropriate care, as it reveals information about user location patterns.

# 6. Use Cases

Common uses for the Map of Users include:

- **Verifying expected user geographic distribution** — Confirming that study participants or research teams are accessing REDCap from expected regions
- **Identifying unexpected access** — Spotting unusual geographic access patterns that may warrant further investigation
- **Understanding institutional reach** — Visualizing the geographic spread of users across multiple sites or regions in multi-institutional studies or deployments

---

# 7. Common Questions

**Q: How is user location determined on the Map of Users?**
User location is determined by resolving their IP address to geographic coordinates using an IP geolocation service. The resolution is approximate and identifies a general geographic area rather than a precise location. IP geolocation accuracy varies depending on IP type (institutional networks, VPNs, mobile ISPs, etc.).

**Q: Why do all my users appear to be in the same location when I know they are distributed across multiple sites?**
This commonly occurs when users access REDCap through a centralized proxy, VPN, or NAT gateway. All traffic appears to originate from the gateway's IP address, so all users map to that single location. Contact your IT department to understand your institution's network architecture if you see unexpected geographic clustering.

**Q: How can I use the Map of Users to verify that participants in a multi-site study are accessing from expected locations?**
Generate the map for the time period of active data collection. The map should show markers in the geographic regions where your study sites are located. If you see markers in unexpected locations, investigate whether those represent legitimate access (e.g., remote researchers, participants traveling) or potential security concerns.

**Q: What does the time window parameter do?**
The time window (in hours) controls how recent the user activity is. Adjusting this parameter from, for example, 1 hour to 24 hours will show more user activity on the map. A 1-hour window shows only very recent activity, while a 24-hour window shows all activity from the past day.

**Q: If I click on a marker on the map, what information is shown?**
Clicking a marker displays an info window with details about the user, such as their username or email and their recent activity context. The exact information varies by REDCap version and configuration.

**Q: Can I export the map data or save it as an image?**
The map is displayed in Google Maps, which allows you to take screenshots or save them to your device. Some browsers and mapping tools allow exporting or printing maps. For detailed geographic data, use the System Statistics page or export the User Activity Log for further analysis.

# 8. Common Mistakes & Gotchas

**Assuming IP geolocation is precise enough for security decisions.** IP geolocation is approximate and can be off by miles or even show users in the wrong country, especially for VPN users. Never use the Map of Users as the sole basis for determining whether access is legitimate or suspicious. Always investigate further using the User Activity Log and project context.

**Forgetting that VPN users appear at the VPN exit point, not their actual location.** If your institution uses a VPN service or if remote researchers connect through a corporate VPN, their traffic may appear to originate from the VPN provider's location rather than where they actually are. Be aware of this when interpreting geographic data.

**Misinterpreting institutional network consolidation as anomalous clustering.** Large institutions often route all traffic through centralized gateways or proxies, causing all users to appear in one location (e.g., the main campus) on the map. This is normal and expected. Understand your institution's network topology before investigating apparent geographic anomalies.

**Not refreshing the map when changing the time window.** After you adjust the time window parameter, the map may need a few seconds to reload with new data. If the markers don't change immediately, wait a moment or manually refresh the page to update the display.

**Ignoring mobile users and off-campus workers.** Mobile users appear based on their cellular ISP's service area, which may not match their actual location. Similarly, remote workers may appear in different geographic locations depending on their ISP and network configuration. Do not assume that geographic markers represent permanent user locations.

# 9. Related Articles

- RC-CC-12 — User Activity Log
- RC-CC-13 — User Activity Graphs
