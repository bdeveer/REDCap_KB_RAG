---
id: RC-INFRA-01
title: Self-Hosting a Private REDCap Instance for Development, Testing & Validation
domain: Self-Hosting, Deployment & Release Management
applies_to:
- Administrators and developers running a non-production REDCap instance off the main
  institutional server
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS)
prerequisites:
- None
version: '1.1'
last_updated: 2026-08
related:
- id: RC-INFRA-02
  title: Self-Hosting REDCap on a Synology NAS with Docker Compose
- id: RC-INFRA-03
  title: REDCap Versions, Release Lines & Patching
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-AI-01
  title: 'REDCap AI Tools: Overview & Security'
- id: RC-EM-01
  title: 'External Modules: Overview & Manager'
tags:
- self-hosting, deployment & release management
synonyms:
- how do i set up my own private redcap test server
- run a private redcap sandbox for development
- self-host redcap for external module development
- stand up a non-production redcap instance
- install redcap in docker containers
- personal redcap instance for testing upgrades
- redcap licensing for a private sandbox
- test redcap configuration changes safely off production
- what php version does redcap require
- unicode transformation before upgrading redcap
- utf8mb4 charset requirement for redcap database
---

# 1. Overview

This article explains how to stand up your own private, non-production REDCap instance — a personal "sandbox" that is completely separate from your institution's production server. The most common reasons to do this are External Module (EM) development, testing risky configuration changes, validating an upgrade before it reaches production, and training. Because the instance holds no real participant data, it can run on modest hardware (a home server, a NAS, a spare workstation, or a small cloud VM) using containers, and it can safely use features — like AI tools — that you might not be allowed to point at production data. This article is platform-agnostic; for a concrete end-to-end build, see [RC-INFRA-02 — Self-Hosting REDCap on a Synology NAS with Docker Compose](RC-INFRA-02_Self-Hosting-REDCap-on-Synology-Docker.md).

> **Critical — licensing and data.** REDCap source code is only available to licensed institutions through the REDCap Community site, and a personal sandbox must be covered by your institution's license (it permits non-production instances; confirm with your REDCap administrator). A self-hosted sandbox is **not** validated for PHI or real research data — keep only test data in it.

---

# 2. Key Concepts & Definitions

## Non-Production Instance
A REDCap installation used for development, testing, training, or validation rather than collecting real data. It mirrors the production application but runs on separate infrastructure and is not held to the same compliance, backup, or uptime standards.

## Container / Docker
A container packages an application and its dependencies into an isolated, reproducible unit. REDCap's runtime (a web server with PHP, and a MySQL/MariaDB database) maps naturally onto a small set of containers, which is far easier to stand up and tear down than installing PHP and MySQL directly on a host.

## Docker Compose
A tool that defines a multi-container application in a single `docker-compose.yml` file — which images to run, how they network together, what volumes persist data, and which ports are published. One `docker compose up` brings the whole stack online.

## Volume
Docker's mechanism for persisting data outside a container's lifecycle. A database container is ephemeral, but its data lives in a volume so it survives restarts and image updates. The two things worth persisting in a REDCap stack are the database and the uploaded-documents folder.

## Web Root vs. App Directory
REDCap is served from a web root, with the application files (including the versioned `redcap_vXX.X.X/` folder) underneath it, so the app is reached at the `/redcap/` path. Keeping uploaded files **outside** the web root is a security best practice (see Section 5).

## Mail Catcher
A fake SMTP server (e.g., Mailpit, MailHog) that accepts all outgoing email and displays it in a web inbox instead of delivering it. Essential for a sandbox so test survey invitations and alerts never reach real people.

## OpenAI-Compatible Endpoint
REDCap's AI features speak the OpenAI API format. Any server that exposes that format can act as REDCap's "AI server," including a local proxy that translates the requests to a different provider (see Section 6).

---

# 3. The Container Stack

A minimal REDCap sandbox is three containers; a fuller one adds convenience services. Each runs as its own container on a shared private network so they can reach each other by name.

| Container | Role | Required? |
|---|---|---|
| **Web** | A web server (Apache or nginx) with PHP and the extensions REDCap needs (mysqli, gd, curl, zip, mbstring, intl, openssl; optionally ldap, imagick). Serves the REDCap application files. | Yes |
| **Database** | MySQL 8 (or MariaDB / Percona), configured for **full Unicode** — `utf8mb4` charset and collation. Holds the entire REDCap schema and all project data. | Yes |
| **Mail catcher** | Captures all outbound email into a web inbox so the sandbox never sends real mail. | Strongly recommended |
| **Database GUI** | A web tool such as Adminer or phpMyAdmin for read/write SQL access (REDCap's built-in Query Tool is read-only by design — see [RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md)). | Optional |
| **AI proxy** | An OpenAI-compatible proxy that backs REDCap's AI features (Section 6). | Optional |

The containers reach each other by service name on the internal network — REDCap's database host is simply `db`, its mail relay is `mailpit:1025`, its AI endpoint is `http://litellm:4000`. None of those need to be published to the host; only the web UI (and any admin tools you want in a browser) need published ports.

## 3.1 PHP version

Match the PHP version to your REDCap version. An unsupported PHP will fail the install or the Configuration Check.

| REDCap version | Minimum PHP | Notes |
|---|---|---|
| 15.0.8 and higher | 8.0.2 | PHP 7 support dropped. PHP 8.0 through 8.4 supported |
| 16.0.5 and higher | **8.1.0** | PHP 8.0 support dropped. PHP 8.5 officially supported from this version |

PHP 8.3 remains a safe, well-supported middle choice. If you want the newest runtime, 8.5 is supported from REDCap 16.0.5 onward.

> **Version caveat (≤16.0.10 LTS / ≤16.0.9 Standard):** On PHP 8.4 or 8.5 the REDCap **upgrade page** fails to load with a fatal PHP error, so you cannot upgrade *out of* an affected version while running one of those PHP releases. Fixed in 16.1.0 Standard / 16.0.11 LTS. If you hit a blank upgrade page on a new PHP, temporarily drop the container back to PHP 8.3, complete the upgrade, then move forward again.

## 3.2 Database charset — a hard upgrade prerequisite

Build the database with the `utf8mb4` charset and a `utf8mb4` collation from the start. This is not a preference; on current REDCap it is a precondition for the application running at all.

> **Critical — Unicode Transformation (REDCap 15.6.0+).** REDCap dropped support for the legacy `UTF8` / `UTF8-MB3` charset and collation, following their deprecation in MySQL and MariaDB. **You cannot upgrade to REDCap 15.6.0 or higher until the Unicode Transformation has been performed on the REDCap database tables.** On a fresh sandbox this is a non-issue provided you create the database as `utf8mb4`. On an instance carrying forward an older database, it is the single most likely thing to block an upgrade.

**If you need to perform the transformation:**

| Your current REDCap version | Path |
|---|---|
| 13.2.0 or higher | The **Configuration Check** page carries the instructions and the transformation utility |
| Below 13.2.0 | Upgrade to **15.5.0** first, perform the Unicode Transformation, then continue upward |
| Transformation suspected but unconfirmed | Upgrade to **15.5.40** first. That version correctly refuses to let you move to 16.0.0+ until the transformation is done — which is the behaviour you want |

> **Version caveat (Easy Upgrade, ≤15.5.39 LTS / ≤17.0.2 Standard):** The Easy Upgrade feature mistakenly allowed admins to **bypass** the Unicode Transformation entirely, producing an instance on 16.0.0+ whose tables were never transformed. The bypass could not be fixed retroactively in the version being upgraded *from*. Two consequences: a later traditional upgrade gets **stuck on the upgrade page** (fixed 17.0.4), and the database is in a state REDCap no longer expects. From **17.0.3** the remedy page `ControlCenter/fixdb.php` has been restored and is reachable from the Configuration Check page, so the transformation can be completed after the fact. If you suspect an instance was upgraded past 15.6.0 via Easy Upgrade without transforming, check there.

> **Note — MySQL 8.4 foreign-key setting.** REDCap 15.6.1 added a Configuration Check recommendation to set `restrict_fk_on_non_standard_key` to `OFF` on MySQL 8.4.0+. That check was **removed again in 15.8.4** as misleading and incorrect. If you saw the recommendation on an older version, no action is needed. It never applied to MariaDB or to MySQL below 8.4.0.

---

# 4. Installing the REDCap Application

The container images provide the *runtime*; REDCap's *source* is mounted in from a folder you control.

1. **Download** the REDCap installer ZIP from the REDCap Community site under your institution's license (the full "Install" package for a new instance; the smaller "Upgrade" package for version bumps).
2. **Unzip** it into the web container's mounted folder so the application sits at the `/redcap/` path.
3. **Configure the database connection.** REDCap reads its credentials from `database.php`. In a containerized stack, point that file at the database container (host `db`) and the credentials you set for the database container — ideally by having `database.php` read them from environment variables rather than hard-coding secrets into the source tree.
4. **Run the install.** Visit `install.php` in a browser; the wizard checks PHP/extensions, confirms the database connection, and creates the schema. If the wizard cannot create tables directly, it generates SQL you run manually — REDCap also ships the schema as `Resources/sql/install.sql` (tables) and `install_data.sql` (default `redcap_config` rows). Load both as the database root user.
5. **Finish in the Control Center:** create your admin account and set the **REDCap Base URL** to however you reach the instance.

> **Important — the salt.** REDCap uses a crypto salt (in `database.php`) to hash stored values. Set it once to a long random string and **never change it** afterward, or stored hashes break.

---

# 5. Email, File Storage & Other Sandbox Hygiene

**Email → mail catcher.** REDCap has no generic "SMTP server / port" field in its UI; it sends through the server's PHP mail subsystem (see [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md), which covers only Universal FROM/DO-NOT-REPLY addresses and third-party API providers). To route mail to a catcher, configure the *web container's* mail transport — install a lightweight sendmail shim (e.g., `msmtp`) and point PHP's `sendmail_path` at the mail-catcher container. REDCap's "Send test email" then lands in the catcher's inbox with no UI change.

**Move uploaded files outside the web root.** By default REDCap stores uploaded documents in its `edocs` folder under the web root, which the Configuration Check flags as "exposed to the web." Set an alternate storage path (Control Center → File Upload Settings) to a directory **outside** the document root, backed by a persistent volume, and the warning clears.

**The cron job.** REDCap requires a process that runs `cron.php` every minute to drive surveys, alerts, scheduled tasks, and data-quality checks (see [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md)). In a container, schedule this from the host (e.g., a system cron or the platform's task scheduler) calling `cron.php` inside the web container once a minute.

**Backups.** The database and the uploaded-files volume are the two things worth backing up. Because the database lives in a container volume, back it up with `mysqldump` rather than copying files, and archive the uploads volume separately.

---

# 6. AI Tools via an OpenAI-Compatible Proxy

REDCap's three AI features — Writing Tools, Summarization, and MLM auto-translation — call out to an "AI server" you configure (see [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md)). The configuration lives in **Control Center → Modules/Services → AI Services** and expects an **API Endpoint URL**, **API Key**, and **API Model Name** in OpenAI format.

You can point this at a hosted OpenAI-compatible service directly, but a common sandbox pattern is to run a small **proxy container** (such as LiteLLM) that exposes the OpenAI format and forwards to whatever provider you actually use — including providers that are *not* natively OpenAI-shaped. The proxy:

- Presents `http://<proxy>:4000/v1` on the internal network as REDCap's AI endpoint.
- Authenticates REDCap with a master key you choose (REDCap puts it in the "API Key" field).
- Maps a friendly model name (what you type in "API Model Name") to the real upstream model, and carries the provider's own API key.
- Can be told to **drop unsupported parameters**, because REDCap sends OpenAI-style fields (e.g., `presence_penalty`, `frequency_penalty`) that some providers reject.

Because all inference happens upstream, the local box does no AI compute — it only proxies. Keep the proxy on the internal network (no published port) so only REDCap can reach it.

> **Note — API access is separate from a chat subscription.** Programmatic API access (what the proxy needs) is billed separately from any consumer chat subscription you may have with the same vendor. You will need an API key with its own billing/credits set up on the provider's developer console.

---

# 7. Remote Access & HTTPS

A sandbox usually shouldn't be exposed directly to the internet. Three common approaches, from most to least private:

| Approach | What it gives you | Trade-off |
|---|---|---|
| **Mesh VPN** (e.g., Tailscale, WireGuard) | Private encrypted access from your own devices; can also terminate real HTTPS with a valid cert (e.g., Tailscale Serve). Nothing is public. | Each device needs the VPN client. |
| **Reverse proxy + TLS** (e.g., the platform's built-in proxy + Let's Encrypt + a DDNS hostname) | A normal `https://host/` URL; works for any visitor. | Requires a public hostname and a router port-forward; exposes the login. |
| **Public tunnel** (e.g., Tailscale Funnel, Cloudflare Tunnel) | Public HTTPS with no port-forward, useful for testing surveys from outside. | The whole app (including the admin login) becomes internet-reachable — use a strong admin password and no real data. |

Whatever the front door, set the **REDCap Base URL** to match it. When a reverse proxy terminates TLS and forwards plain HTTP to the container, REDCap detects HTTPS from the `X-Forwarded-Proto` header, so the SSL Configuration Check passes without changing the web server.

> **Note — survey end-point self-check.** On NAT'd or containerized setups, the Configuration Check's "internal survey end-point" test often fails because the container cannot make an HTTP call to its own public address (a hairpin-routing limitation). This does not affect surveys working in a browser and generally cannot be fixed from within REDCap.

---

# 8. Common Questions

**Can I run my own copy of REDCap for testing?**
Yes, provided your institution holds a REDCap license — it covers non-production instances. Download the source from the REDCap Community site, run it on separate infrastructure (containers are easiest), and keep only test data in it. Confirm the specifics of non-production use with your REDCap administrator.

**Why would I self-host instead of using my institution's test server?**
For full administrator control — you can install and develop External Modules, run the Control Center, test upgrades, and try AI features without affecting shared infrastructure or waiting on a central team. It's especially useful for EM development and for validating changes before requesting them in production.

**Do I need a powerful server?**
No. Because no real workload or AI inference runs locally, a small machine (a NAS, a mini-PC, or a small VM with a couple of CPU cores and a few GB of RAM) is sufficient for a single-developer sandbox.

**How do I keep test emails from reaching real people?**
Route all outgoing mail to a mail-catcher container (Mailpit, MailHog). REDCap's email then lands in a local web inbox instead of being delivered. Configure this at the web-container level, since REDCap has no SMTP host field in its UI.

**Can I use REDCap's AI features on a self-hosted instance?**
Yes. Configure an OpenAI-compatible endpoint under Control Center → Modules/Services → AI Services. A small proxy container (e.g., LiteLLM) lets you back those features with the provider of your choice using your own API key. Because no real data should live in the sandbox, this is a safe place to experiment with AI features.

**Is a self-hosted instance safe for real participant data?**
No. A personal sandbox is not validated, backed up, or secured to institutional standards. Use it only for test data; real or identifiable data belongs on your institution's production server.

---

# 9. Common Mistakes & Gotchas

**Putting real or identifiable data in a sandbox.** A self-hosted instance lacks the compliance controls, backups, and security of a production server. Loading PHI or real research data — even "just to test" — creates real risk. Keep the sandbox to synthetic/test data only.

**Mismatching the PHP version to the REDCap version.** Installing a current REDCap on an older PHP (below 8.1.0 from REDCap 16.0.5 onward) causes install failures or Configuration Check errors. Pick a web image whose PHP version satisfies your REDCap version before building — see Section 3.1 for the version table.

**Creating the database with a legacy charset.** A database built as `UTF8` / `UTF8-MB3` rather than `utf8mb4` will block any upgrade to REDCap 15.6.0 or higher until the Unicode Transformation is performed, and the block appears only when you attempt the upgrade — not when you install. Create the database as `utf8mb4` at the outset; retrofitting it later is far more work than getting it right on day one. See Section 3.2.

**Assuming a successful Easy Upgrade means the database was transformed.** On affected versions, Easy Upgrade would carry an instance past 15.6.0 without performing the Unicode Transformation and without complaining. The instance appears fine until a later traditional upgrade sticks on the upgrade page. If an instance was Easy Upgraded from v15 to v16, verify the transformation actually ran rather than assuming it did.

**Planning a multi-version jump without reading the intermediate changelogs.** Upgrade prerequisites accumulate — PHP minimums and the charset requirement both changed inside the 15.x–16.x range — and several releases shipped fixes for upgrade SQL scripts that failed on particular MySQL and MariaDB versions and configurations. Read the changelog between your current version and your target, not just the target's entry. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

**Forgetting the cron job.** Without a per-minute `cron.php` runner, survey invitations, alerts, and scheduled tasks silently never fire — with no error on screen. Set up the cron from the host immediately after install and confirm it's "Good" on the Cron Jobs page.

**Leaving uploaded files in the default web-root `edocs` folder.** This trips the "documents exposed to the web" check. Move storage to a path outside the document root via File Upload Settings, backed by a persistent volume.

**Exposing the admin login publicly without hardening.** If you put the instance on the public internet (a tunnel or reverse proxy), the Control Center login is reachable by anyone. Use a strong admin password, rely on the built-in rate limiter, and never combine public exposure with real data.

---

# 10. Related Articles

- [RC-INFRA-02 — Self-Hosting REDCap on a Synology NAS with Docker Compose](RC-INFRA-02_Self-Hosting-REDCap-on-Synology-Docker.md) (concrete end-to-end build of this pattern)
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) (Standard vs LTS, reading the changelog before an upgrade)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (where AI services and email providers are configured)
- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) (Configuration Check, cron jobs, base URL, SSL)
- [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) (what the AI features are and how the AI server is meant to work)
- [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md) (a primary reason to run a private instance)
- [RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md) (read-only by design; why a DB GUI is useful in a sandbox)
