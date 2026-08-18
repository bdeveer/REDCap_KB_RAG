---
id: RC-INFRA-02
title: Self-Hosting REDCap on a Synology NAS with Docker Compose
domain: Self-Hosting, Deployment & Release Management
applies_to:
- Synology NAS (DSM 7.2+) with Container Manager
- non-production REDCap
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS)
prerequisites:
- RC-INFRA-01 — Self-Hosting a Private REDCap Instance for Development, Testing &
  Validation
version: '1.1'
last_updated: 2026-08
related:
- id: RC-INFRA-01
  title: Self-Hosting a Private REDCap Instance
- id: RC-INFRA-03
  title: REDCap Versions, Release Lines & Patching
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-CC-02
  title: 'Control Center: General System Configuration'
- id: RC-AI-01
  title: 'REDCap AI Tools: Overview & Security'
tags:
- self-hosting, deployment & release management
synonyms:
- how to run redcap on a synology nas
- redcap docker compose setup on synology container manager
- install a redcap sandbox on a nas with docker
- self-host redcap with https and vpn mesh access
- redcap docker stack with mail catcher and database gui
- wire redcap ai features to a provider in docker
- step by step redcap nas deployment
- build a redcap sandbox on a ds220 synology box
- my redcap install page is blank
- which redcap versions are known bad to install
---

# 1. Overview

This article is a concrete, end-to-end build of the pattern described in [RC-INFRA-01 — Self-Hosting a Private REDCap Instance](RC-INFRA-01_Self-Hosting-a-Private-REDCap-Instance.md), implemented on a Synology NAS using **Container Manager** and Docker Compose. It produces a private REDCap sandbox (web + database + mail catcher + database GUI + AI proxy), reachable securely over a mesh VPN with real HTTPS, with REDCap's AI features wired to a provider of your choice. It targets a modest box (the reference build used a DS220+ with 6 GB RAM) and is written for someone comfortable with the DSM interface and an occasional SSH session. Replace placeholders like `NAS-IP`, ports, and hostnames with your own. **This is a non-production sandbox — test data only.**

---

# 2. Key Concepts & Definitions

## Container Manager
Synology's GUI for Docker (DSM 7.2+). It can run individual containers or a **Project** built from a `docker-compose.yml`. This build uses a Compose project so the whole stack is defined in one file.

## Named Volume vs. Bind Mount (the Synology permissions trap)
A **bind mount** maps a host folder into a container; a **named volume** is storage Docker manages itself. On Synology, bind-mounted folders carry the share's ACLs, which frequently deny the in-container user (e.g., MySQL's uid 999) write access — causing "data directory is not writable" crashes. Database storage should therefore use a **named volume**, which Docker initializes with the right ownership.

## DSM Task Scheduler
DSM's built-in cron equivalent. Used here to run REDCap's `cron.php` every minute, since the PHP container does not run cron itself.

## Mesh VPN (Tailscale)
A zero-config VPN that gives the NAS a private address reachable from your devices. **Tailscale Serve** can additionally terminate real HTTPS with a valid certificate; **Tailscale Funnel** can expose one service to the public internet without a router port-forward.

---

# 3. The Compose Stack

The stack is five services on one internal network. Only the web UI and admin tools publish host ports; the database and AI proxy stay internal.

| Service | Image | Published port | Purpose |
|---|---|---|---|
| `web` | Custom (built from `php:8.3-apache`) | `8088` → 80 | Apache + PHP 8.3 + REDCap |
| `db` | `mysql:8.0` | none (internal) | Database, in a named volume |
| `mailpit` | `axllent/mailpit` | `8025` | Captures all outbound email |
| `adminer` | `adminer` | `8089` | Web MySQL GUI |
| `litellm` | `ghcr.io/berriai/litellm:main-latest` | none (internal) | OpenAI-compatible AI proxy |

Key points the Compose file encodes:

- **The web image is built, not pulled** — a small Dockerfile starts from `php:8.3-apache` and adds the REDCap extensions (`mysqli`, `gd`, `zip`, `intl`, `ldap`, `imagick` + Ghostscript), `mod_rewrite`, `AllowOverride All`, raised PHP limits (`max_input_vars=100000`, 64 MB uploads), an `msmtp` mail shim pointed at `mailpit`, and a folder for uploads outside the web root.
- **Database storage is a named volume** (`db_data:/var/lib/mysql`) to dodge the Synology ACL trap.
- **Uploaded documents** use a second named volume (`edocs_data`) mounted at a path *outside* the web root.
- **Ports are remapped** off 80/443 (DSM owns those). REDCap on `8088`, Mailpit on `8025`, Adminer on `8089`.
- **Credentials and the AI keys** come from a `.env` file next to the Compose file, never hard-coded.

> **Note — port conflicts.** Check a candidate host port is free before using it: `sudo netstat -tlnp | grep ':8088'` (Synology's busybox may not have `ss`). DSM and other containers commonly occupy 8080/8081.

---

# 4. Build Steps

1. **Prep DSM:** install Container Manager (Package Center) and enable SSH (Control Panel → Terminal & SNMP).
2. **Place the project** at e.g. `/volume2/docker/redcap` (Compose file, `.env`, `web/` with the Dockerfile and `database.php`, and a `litellm/` config folder).
3. **Add the REDCap source:** unzip the Community installer into a `redcap/` subfolder so the app lands at `redcap/redcap/install.php` (the outer folder is the bind-mounted web root; the inner is the app, giving the `/redcap/` URL path).
4. **Create `.env`** with database passwords, a fixed `REDCAP_SALT` (`openssl rand -hex 24`), the chosen ports, and the AI keys (Section 7).
5. **Pre-create folders Compose won't:** Synology's Container Manager does not auto-create bind-mount host folders. Named volumes are created automatically, but any bind-mounted path must exist first.
6. **Build and start:** Container Manager → Project → Create (point at the Compose file), or `sudo docker compose up -d --build`. The first build takes a few minutes while PHP extensions compile.
7. **Run the install wizard** at `http://NAS-IP:8088/redcap/install.php`; create the admin account; set the **REDCap Base URL** (Section 8).

> **Critical — REDCap 17.1.2 install bug on PHP 8 (fixed in 17.1.3).** A fresh `install.php` on REDCap **17.1.2** blanks out with an uncaught fatal: `Undefined constant "VANDERBILT_SERVER"`. The constant is referenced by the REDCap+ licensing code before it is defined, and PHP 8 turns the resulting undefined-constant *warning* (harmless on PHP 7) into a fatal error. **Use REDCap 17.1.3 or newer**, where it is fixed. If you must run 17.1.2, the workaround is to pre-define the Vanderbilt constants early (in `database.php`) by replicating `System::defineFixedConstants()`. For other versions known to break install or upgrade, see Section 9.1.

---

# 5. Synology-Specific Gotchas

**MySQL won't start — "data directory is not writable."** The database folder isn't writable by the container's MySQL user because of Synology share ACLs. Use a **named volume** for `/var/lib/mysql` (not a bind mount); Docker initializes it with correct ownership.

**Credentials look "wrong" after editing `.env`.** MySQL only reads `MYSQL_*` when it initializes an *empty* data volume. Editing passwords in `.env` after the database exists has no effect — the volume keeps the originals. On a data-free sandbox, wipe and re-init: `docker compose down`, `docker volume rm <project>_db_data`, `docker compose up -d`.

**The database user is whatever `MYSQL_USER` says.** If you set `MYSQL_USER=redcap_db`, the user is `redcap_db@'%'`, not `redcap`. Hand-test connections with your actual username over TCP: `mysql -u"$MYSQL_USER" -h127.0.0.1 -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"`. A wrong username returns "Access denied," which looks like a password problem but isn't.

**Socket connections look like `localhost`.** A `user@'%'` account matches TCP but **not** the unix socket (seen as `user@'localhost'`). Inside the db container, connect over TCP (`-h127.0.0.1`) as the app user, or use `-uroot` for admin tasks like loading SQL.

**Writable folders for REDCap.** If uploads or the install error with permission denied, the `edocs`, `temp`, and `modules` folders need to be writable: `sudo chmod -R 0777 edocs temp modules` (acceptable on a private box).

**The NAS shell is `sh`, not bash.** Source the env with `. ./.env`, not `source`. Files in the project folder are often root-owned, so writing them needs `sudo` (e.g., `sudo tee`), and `mkdir`/`nano` may need `sudo` or aren't installed (`nano` is absent — use `vi` or DSM's text editor).

---

# 6. Email, Uploads & Cron

**Email → Mailpit.** REDCap has no SMTP host field; it uses the server's PHP mail subsystem (see [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)). The web image installs `msmtp` and sets PHP's `sendmail_path` to relay to the `mailpit` container, so REDCap's "Send test email" lands in the Mailpit inbox (`http://NAS-IP:8025`). Give `msmtp` a valid default `from` address (e.g., `redcap@nas.local`); a bare sender like `root` is rejected by the catcher.

**Uploads outside the web root.** Mount a named volume (`edocs_data`) at a path outside the document root, make it writable, and set it in Control Center → File Upload Settings ("alternate internal storage of uploaded files"). This clears the "edocs exposed to the web" Configuration Check item.

**Cron via DSM Task Scheduler.** Create a scheduled task (Control Panel → Task Scheduler → user-defined script, user **root**, frequency **every 1 minute**) running:
```
docker exec redcap-web php /var/www/html/redcap/cron.php
```
After a couple of minutes the Configuration Check's cron item turns green.

---

# 7. AI Proxy (LiteLLM → your provider)

REDCap's AI features point at an OpenAI-compatible endpoint; a `litellm` container provides that and forwards to your chosen provider (the reference build used Anthropic Claude). See [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md).

The proxy config (`litellm/config.yaml`) maps a friendly model name to the upstream model and drops parameters the provider doesn't support:
```yaml
model_list:
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-6
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  drop_params: true
```
Two keys go in `.env`: the **provider API key** (`ANTHROPIC_API_KEY`) and a **master key** (`LITELLM_MASTER_KEY`) that REDCap uses to authenticate to the proxy. The master key is read from the env var automatically — do **not** also set it under `general_settings` with an `os.environ/` reference, which isn't resolved there and causes 401s.

In **Control Center → Modules/Services → AI Services**:
- Enable system-wide AI services? → **Enabled using OpenAI Service**
- API Endpoint URL: `http://litellm:4000/v1`
- API Key: the `LITELLM_MASTER_KEY` value
- API Model Name: `claude-sonnet`

> **Gotcha — `drop_params`.** Without `drop_params: true`, REDCap's requests fail with a 400 because it sends OpenAI fields (`presence_penalty`, `frequency_penalty`) that some providers reject. After any change to `.env` or `config.yaml`, recreate the container: `docker compose up -d --force-recreate litellm`.

---

# 8. Remote Access with Tailscale

The reference build keeps the stack private over a Tailscale mesh and serves real HTTPS:

**Tailnet-only HTTPS (Serve).** After enabling HTTPS Certificates + MagicDNS in the Tailscale admin console:
```
sudo tailscale serve --bg http://127.0.0.1:8088
```
This terminates TLS on 443 and proxies to REDCap, giving `https://<nas>.<tailnet>.ts.net/redcap/` with a valid cert. Set this as the **REDCap Base URL**. REDCap reads Tailscale's `X-Forwarded-Proto: https`, so the SSL check passes with no Apache change. Admin tools can ride separate HTTPS ports, e.g. `--https=8443` → Adminer, `--https=10025` → Mailpit.

**Public access (Funnel).** To reach surveys without Tailscale, expose REDCap (port 443 only):
```
sudo tailscale funnel --bg http://127.0.0.1:8088
```
This makes the whole app (including the admin login) public — keep the admin password strong, rely on REDCap's rate limiter, and store no real data. Turn it off with `sudo tailscale funnel reset`.

> **Note — DNS on managed/corporate laptops.** A device that can't resolve `*.ts.net` (corporate DNS filtering, or a stale manual DNS entry) won't reach the funnel even though it's public. Confirm public reachability from an unmanaged device or cellular connection before assuming the funnel is broken.

---

# 9. Database GUI & Upgrades

**Adminer** (`http://NAS-IP:8089`) gives read/write SQL access that REDCap's built-in Query Tool (read-only by design — [RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md)) does not. Log in with System **MySQL**, Server **db**, Username **root**, the password from `.env`, Database **redcap**.

**Upgrades** are a file drop plus a browser-driven migration: back up first, unzip the *Upgrade* package into the app folder beside the current `redcap_vXX.X.X/`, then load REDCap — the Control Center detects the new files and runs the database migration. No container rebuild is needed unless a new version requires a new PHP extension (then add it to the Dockerfile and `docker compose up -d --build web`).

Before a version jump, check three prerequisites — any of them will stop the migration:

1. **PHP version.** The minimum is PHP 8.1.0 from REDCap 16.0.5 onward; PHP 8.5 is supported from that version too. The `php:8.3-apache` base used in this build satisfies current REDCap. See [RC-INFRA-01 — Self-Hosting a Private REDCap Instance](RC-INFRA-01_Self-Hosting-a-Private-REDCap-Instance.md) Section 3.1.
2. **Database charset.** REDCap 15.6.0 and higher refuse to upgrade until the Unicode Transformation has been performed, because support for the legacy `UTF8` / `UTF8-MB3` charset was dropped. A stack built as described here starts from a fresh `mysql:8.0` database, so create it as `utf8mb4` and this never arises. See `RC-INFRA-01` Section 3.2.
3. **Target version.** Some versions are known-bad for install or upgrade — see the table below.

> **Note — sandbox upgrades are the point.** Validating an upgrade here before it reaches production is one of the main reasons to run this instance. Restore a copy of production's database into the sandbox first; an upgrade that succeeds against an empty schema proves much less than one that succeeds against real structure.

## 9.1 Known-bad install and upgrade versions

| Version | Symptom | Action |
|---|---|---|
| **17.1.2** | Fresh `install.php` blanks out with an uncaught fatal: `Undefined constant "VANDERBILT_SERVER"`. The constant is referenced by REDCap+ licensing code before it is defined, and PHP 8 turns the resulting warning into a fatal. REDCap's own changelog records the same symptom as the install page crashing silently and preventing new installations | Use **17.1.3 or newer**, where it is fixed. If you must run 17.1.2, pre-define the Vanderbilt constants early in `database.php` by replicating `System::defineFixedConstants()` |
| **16.0.9 and below (LTS 16.0.10 and below)** | The **upgrade page** fails with a fatal PHP error when running PHP 8.4 or 8.5, so you cannot upgrade out of the version | Fixed in 16.1.0 Standard / 16.0.11 LTS. Temporarily run PHP 8.3, complete the upgrade, then move forward |
| **15.5.10 (LTS)** | Mis-released — the package was actually identical to 15.0.38 | Avoid. If already applied from a 15.0.x version, REDCap's guidance was to correct `redcap_config` manually; use a later LTS patch instead |

> **Critical — Easy Upgrade and the Unicode Transformation.** On affected versions, Easy Upgrade would carry an instance past 15.6.0 **without** performing the Unicode Transformation and without reporting a problem. The result is an instance on 16.0.0+ whose tables were never transformed, which later sticks on the upgrade page during a traditional upgrade (fixed 17.0.4). From **17.0.3**, the remedy page `ControlCenter/fixdb.php` is restored and reachable from the Configuration Check page so the transformation can be completed after the fact. If it is even suspected that a transformation is outstanding, upgrade to **15.5.40** first — that version correctly blocks the move to 16.0.0+ until the transformation is done.

---

# 10. Common Questions

**Can a Synology NAS actually run REDCap?**
Yes. A modest NAS (the reference build used a DS220+, Celeron J4025, 6 GB RAM) comfortably runs a single-developer REDCap sandbox via Container Manager, because no real workload or AI inference runs locally.

**Why does MySQL crash with "data directory is not writable" on Synology?**
Synology share ACLs prevent the container's MySQL user from writing to a bind-mounted folder. Use a Docker **named volume** for `/var/lib/mysql` instead; Docker creates it with the correct ownership and the crash disappears.

**My install.php is blank — what's wrong?**
If you're on REDCap 17.1.2 with PHP 8, you've hit the `VANDERBILT_SERVER` undefined-constant fatal. Upgrade to 17.1.3+ (fixed there), or apply the `database.php` workaround that pre-defines the Vanderbilt constants. A blank page that returns HTTP 200 but is truncated mid-output is the signature.

**How do I run REDCap's cron job in a container on Synology?**
Use DSM Task Scheduler (as root, every minute) to run `docker exec redcap-web php /var/www/html/redcap/cron.php`. The PHP container doesn't run cron itself, so without this all time-dependent features silently stop.

**How do I get a real HTTPS certificate without exposing the NAS?**
Run Tailscale on the NAS and use Tailscale Serve (`tailscale serve --bg http://127.0.0.1:8088`). It issues a valid cert and serves REDCap at your tailnet hostname, reachable only from your own devices — no port-forward, no public exposure.

**Why won't REDCap's AI feature work even though the proxy is up?**
Two common causes: the proxy is missing `drop_params: true` (REDCap sends params the provider rejects → 400), or the provider API key in `.env` is wrong/placeholder (→ "invalid api key" from upstream). Check the LiteLLM logs for which one, fix `.env`/`config.yaml`, and recreate the container.

---

# 11. Common Mistakes & Gotchas

**Bind-mounting the MySQL data directory.** On Synology this causes the "not writable" crash. Always use a named volume for the database; reserve bind mounts for the REDCap source and read-only config files.

**Editing `.env` passwords after the database already exists.** The running database keeps the credentials from its first initialization, so the new values silently don't apply and you get access-denied. Wipe and re-init the `db_data` volume (safe on a data-free sandbox) so `.env` and the database agree.

**Assuming the Configuration Check should be all green.** Two items are expected to stay flagged on this kind of setup: the SSL warning (until you front it with HTTPS) and the "internal survey end-point" self-check (a NAT hairpin limitation that doesn't affect real survey use). Don't chase them.

**Testing the funnel from a managed laptop.** Corporate DNS often won't resolve `*.ts.net`, so a public funnel can look broken when it's actually fine. Verify from an unmanaged device or cellular before concluding the NAS is at fault.

**Mixing public exposure with anything sensitive.** Tailscale Funnel makes the admin login internet-reachable. Only ever do this on a sandbox with test data and a strong admin password; turn the funnel off when you don't need it.

---

# 12. Related Articles

- [RC-INFRA-01 — Self-Hosting a Private REDCap Instance for Development, Testing & Validation](RC-INFRA-01_Self-Hosting-a-Private-REDCap-Instance.md) (the platform-agnostic concepts behind this build)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (AI Services and email provider configuration)
- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) (Configuration Check, cron jobs, base URL, SSL)
- [RC-AI-01 — REDCap AI Tools: Overview & Security](RC-AI-01_REDCap-AI-Tools-Overview-and-Security.md) (the AI features the proxy powers)
- [RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md) (read-only by design; why Adminer is added)
