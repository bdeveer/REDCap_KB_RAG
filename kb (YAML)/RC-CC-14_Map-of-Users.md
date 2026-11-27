---
id: RC-CC-14
title: Map of Users
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: 'REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Map of
  Users behaviour checked against source code; checked live on v17.5.6 (read-only):
  first-use state only'
prerequisites:
- REDCap administrator access with the administrator privilege for Control Center
  dashboards
version: '1.3'
last_updated: 2026-11
related:
- id: RC-CC-12
  title: 'Control Center: User Activity Log'
- id: RC-CC-13
  title: 'Control Center: User Activity Graphs'
- id: RC-CC-15
  title: 'Control Center: Top Usage Report'
tags:
- control center (admin)
synonyms:
- control center map of users
- geographic map of where users access redcap
- see user locations by ip address
- google maps view of redcap users
- user distribution by region admin
- map showing redcap user activity by location
- ip geolocation map of users
- where are my redcap users located
---

# 1. Overview

The Map of Users displays a geographic map showing where users are accessing REDCap from, based on their IP addresses. It is accessible under "Dashboards & Activity" in the Control Center sidebar and uses Google Maps to render the visualization. This tool provides a visual summary of user distribution and activity patterns across geographic regions.

> **Version caveat (REDCap 17.x vs 16.0.x LTS) — Google Maps API key.**
> - **17.x (from 17.5.4 Standard / 17.3.18 LTS, per the changelog):** you must store your own Google Maps API key. The map shows only once a key is stored. After the first-use test passes with no key stored, the page shows a yellow **NEED GOOGLE MAPS API KEY** box with the SQL to run to store your key. There is no Control Center field for the key in any version; the SQL on the page is the way to set it.
> - **16.0.x LTS:** the page uses a shared key built into REDCap and replaces any key an administrator stores, so you cannot use your own key on 16.0.x. The map works only for as long as Google accepts that shared key. If the map is blank or broken on 16.0.x, the fix is to upgrade to 17.x and store your own key.
> - **Upgraded from 16 to 17.x:** if your site used the map on 16, the old shared key is already stored, so 17.x does not show the "need key" box. Overwrite it with your own key using the same SQL as for a new setup.
>
> **Getting the key:** create it in the Google Cloud console with the **Maps JavaScript API** enabled (that is the API the page loads in your browser), and restrict it by HTTP referrer to your REDCap server's address, because the key is visible in the page source.

---

# 2. How It Works

**First use:** The page can open with a setup test and a **Test web service** button instead of the map. That is what a 17.5.6 test instance showed. The test checks that your server can reach the geolocation service; it can reappear later. Your REDCap server needs outbound internet access (through your configured proxy, if you use one).

> **Version caveat (16.0.x LTS):** if the test fails on 16.0.x behind a proxy that inspects HTTPS traffic, check with your network team.

REDCap resolves user IP addresses to approximate geographic coordinates using a geolocation service run by the REDCap Consortium at Vanderbilt. Only IP addresses are sent, 100 per request. Google receives only your API key, and the Google Maps script loads in the administrator's browser.

IP addresses are processed in batches of 100 so the page stays responsive. When new IP addresses are waiting, processing starts automatically when the page loads, and the **Update map** button processes the next batch. A progress counter shows the number of IPs processed. Each IP address is looked up once and the result is kept permanently; it is never looked up again.

**Not every IP address becomes a marker.** REDCap skips survey participants, private (internal) network addresses, malformed or very short addresses, activity it cannot tie to a known user, and results that resolve only to a generic "United States" location. That is why the IP count can be larger than the number of markers on the map.

---

# 3. Time Window

The map shows user activity within a time window chosen from a dropdown of presets:

| Option | Shows activity from |
|---|---|
| **24 hours** (default) | The past day |
| **Week** | The past 7 days |
| **Month** | The past month |
| **3 months** | The past 3 months |
| **6 months** | The past 6 months |
| **Year** | The past year |

There is no free-text hours entry and no 1-hour option. Use the shorter windows to look at recent activity and the longer ones for overall usage patterns.

---

# 4. Map Markers

Active users appear as blue pin markers on the map, one marker per IP address. Hovering over a marker shows nothing; click it to open an info window with:

- City, region and country
- Username
- Full name, linked to the user's email address
- A **view projects** link

The info window contents are the same in all supported versions. This lets administrators drill down from the map to see who is accessing REDCap from a given location.

---

# 5. Limitations and Privacy Considerations

IP geolocation is approximate — it identifies a general geographic area, not a precise location. Accuracy varies by IP type:
- Institutional networks often map to a central campus location; users on private (internal) addresses do not appear at all
- VPN users may appear at the VPN exit point rather than their actual location
- Mobile users may show approximate locations based on their ISP's service area

Administrators should be aware of any institutional privacy policies before sharing or acting on geographic user data. The data should be treated with appropriate care, as it reveals information about user location patterns.

---

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

**Q: The Map of Users is blank. Is something wrong with our instance?**
Probably not; it usually means no working Google Maps API key. On 17.x, follow the instructions on the page (the yellow **NEED GOOGLE MAPS API KEY** box) to obtain your own key and store it with the SQL shown. If you upgraded from 16, overwrite the old stored shared key with your own key using the same SQL. On REDCap 16.0.x LTS you cannot use your own key, so there is no fix other than upgrading to 17.x.

**Q: What does the time window parameter do?**
The time window dropdown controls how far back the map looks: **24 hours** (default), **Week**, **Month**, **3 months**, **6 months** or **Year**. A longer window shows more user activity on the map. There is no option shorter than 24 hours.

**Q: If I click on a marker on the map, what information is shown?**
The info window shows the city, region and country, the username, the user's full name (linked to their email address) and a **view projects** link. Hovering shows nothing; you must click. Each marker represents one IP address.

**Q: Why are there fewer markers than the number of IPs processed?**
Survey participants, private network addresses, very short or malformed addresses, activity not tied to a known user, and IPs that resolve only to a generic "United States" location are not plotted.

**Q: Can I export the map data or save it as an image?**
The map is displayed in Google Maps, which allows you to take screenshots or save them to your device. Some browsers and mapping tools allow exporting or printing maps. For detailed geographic data, use the System Statistics page or export the User Activity Log for further analysis.

---

# 8. Common Mistakes & Gotchas

**Assuming IP geolocation is precise enough for security decisions.** IP geolocation is approximate and can be off by miles or even show users in the wrong country, especially for VPN users. Never use the Map of Users as the sole basis for determining whether access is legitimate or suspicious. Always investigate further using the User Activity Log and project context.

**Forgetting that VPN users appear at the VPN exit point, not their actual location.** If your institution uses a VPN service or if remote researchers connect through a corporate VPN, their traffic may appear to originate from the VPN provider's location rather than where they actually are. Be aware of this when interpreting geographic data.

**Misinterpreting institutional network consolidation as anomalous clustering.** Large institutions often route all traffic through centralized gateways or proxies, causing all users to appear in one location (e.g., the main campus) on the map. This is normal and expected. Understand your institution's network topology before investigating apparent geographic anomalies.

**Not waiting for new IP addresses to be processed.** IP addresses are looked up in batches of 100. If many new addresses are waiting, the map fills in gradually; let the progress counter finish, or click **Update map** to process the next batch.

**Keeping the old shared key after upgrading from 16.0.x.** A site that used the map on 16.0.x LTS already has REDCap's shared key stored, so 17.x does not prompt for a key. Overwrite it with your own key using the same SQL as for a new setup, or the map can stop working without warning.

**Leaving the Google key unrestricted.** The key is visible in the page source. Restrict it by HTTP referrer to your REDCap address and enable only the **Maps JavaScript API**.

**Ignoring mobile users and off-campus workers.** Mobile users appear based on their cellular ISP's service area, which may not match their actual location. Similarly, remote workers may appear in different geographic locations depending on their ISP and network configuration. Do not assume that geographic markers represent permanent user locations.

---

# 9. Related Articles

- [RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)
- [RC-CC-13 — Control Center: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md)
