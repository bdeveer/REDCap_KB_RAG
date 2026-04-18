RC-CC-14

**Map of Users**

| **Article ID** | RC-CC-14 |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
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
