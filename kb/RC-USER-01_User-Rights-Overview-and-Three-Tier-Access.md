RC-USER-01

**User Rights — Overview & Three-Tier Access**

| **Article ID** | RC-USER-01 |
|---|---|
| **Domain** | User Rights |
| **Applies To** | All REDCap project types |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-USER-02 — Adding Users & Managing Roles; RC-USER-03 — Configuring User Privileges; RC-USER-04 — User Management; RC-DAG-01 — Data Access Groups |

---

# 1. Overview

This article explains how REDCap controls who can access what. Access in REDCap is governed by a three-tier system: global system access, project-level access, and per-project user rights. Understanding all three tiers is essential for troubleshooting access issues and for setting up a project correctly. This article is the entry point for the User Rights knowledge base series.

---

# 2. Key Concepts & Definitions

**REDCap Installation**

A single deployed instance of REDCap software, operated by one institution. Each installation has its own user accounts, authentication system, and projects. Users and projects in one installation are entirely separate from those in another.

**Authentication**

The process by which REDCap verifies a user's identity before granting access to the system. The authentication method is set at the installation level by the hosting institution.

**Single Sign-On (SSO)**

An authentication method that uses an institution's central identity system (e.g., university login, hospital network credentials) instead of a REDCap-specific username and password.

**Two-Factor Authentication (2FA)**

An optional additional security layer added on top of standard login. When enabled, a user must verify their identity through a second method (e.g., a code sent to their phone) in addition to their password.

**User Account**

A record within a REDCap installation that represents an individual user. An account must exist and be active for a user to log in at all. Account issues are handled at the system level, not the project level.

**Project Access**

Whether a user has been added to a specific project. REDCap separates data on the project level — a user who has a valid account can still only see projects they have been explicitly added to.

**User Rights**

The set of permissions that control what a user can do within a specific project. User rights are configured independently for each user in each project.

**User Role**

A named, reusable set of user rights that can be assigned to multiple users. Roles standardize access configuration and simplify bulk management.

---

# 3. The Three-Tier Access Model

REDCap access works as three successive gates. A user must pass all three to perform any action in a project.

## 3.1 Tier 1: Global System Access

Before a user can do anything in REDCap, they must have an active account in the installation and be able to log in successfully.

Authentication varies by installation. The most common methods are:

- **Username and password** — a REDCap-specific credential managed by the local support team. Password resets and account unlocks are typically handled by the REDCap support team.
- **Single Sign-On (SSO)** — uses the institution's central identity provider. Account issues (locked accounts, password resets) must be resolved through central IT, not the REDCap support team.

Some installations also require two-factor authentication as an additional layer on top of either method.

> **Institution-specific:** Authentication methods vary by installation (e.g., institutional SSO, local accounts, Shibboleth). Contact your REDCap administrator to learn which login method is in use and who handles account creation or access issues.

A suspended account (disabled at the system level by an administrator) will receive a suspension message at login and cannot access any projects.

## 3.2 Tier 2: Project-Level Access

REDCap strictly separates data by project. A user with a valid account cannot see or access any project unless they have been explicitly added to it.

A user can be added to any number of projects, or to none at all. There are three ways a user ends up on a project:

- **By another project user** — any user with the "User Rights" privilege can add others from within the project's User Rights menu. This is the most common method.
- **Automatically upon creation** — when a user creates or requests a new project, they are automatically added with full rights.
- **By a REDCap administrator** — administrators can add users to any project. In practice, this is typically done only when there are no other active users on a project to perform the task themselves.

## 3.3 Tier 3: Project-Level User Rights

Having project access does not mean having full access. Within a project, user rights define exactly what a user can see and do: which instruments they can view or edit, whether they can export data, whether they can modify the project design, and much more.

This is the most complex tier. User rights are highly configurable and differ from project to project. The remaining articles in this series cover the details:

- RC-USER-02 — Adding Users & Managing Roles
- RC-USER-03 — Configuring User Privileges
- RC-USER-04 — User Management
- RC-DAG-01 — Data Access Groups

---

# 4. Troubleshooting Access

When a user reports they cannot access a project or perform an expected action, follow this checklist in order. Each step narrows down which tier is causing the problem.

1. **Is the user logging in to the correct REDCap installation?** A REDCap installation at Institution A has no connection to the one at Institution B. Confirm the URL the user is using.

2. **Can they log in successfully?** Ask if they can reach their "My Projects" page after logging in. If they cannot, the problem is at Tier 1 — an account or authentication issue.

3. **Do they see the project in their "My Projects" list?** If the project is absent, the user has not been added to it (or the project is archived). This is a Tier 2 problem.

4. **When in the project, can they perform the action they need?** If they can see the project but are blocked from a specific action, the issue is at Tier 3 — their user rights for that project need review.

---

# 5. Common Questions

**Q: A user can log in but cannot find the project — what's wrong?**

**A:** They have not been added to the project, or the project has been archived. Someone with User Rights access in that project needs to add them. Archived projects do not appear in the standard project list.

**Q: A user's password stopped working — who do they contact?**

**A:** It depends on the authentication method. If the installation uses REDCap-specific credentials, contact the local REDCap support team. If it uses SSO, the user must contact central IT — the REDCap team cannot reset SSO credentials.

**Q: Can a user be added to a project without having a REDCap account first?**

**A:** No. A user must have an active account in the REDCap installation before they can be added to any project. If the user doesn't have an account, they need to get one through the local registration or provisioning process.

**Q: Can a user with a valid account access any project they want?**

**A:** No. Project access is strictly controlled. A user can only see and access projects they have been explicitly added to by another user or an administrator.

**Q: Does user rights configuration carry over between projects?**

**A:** No. User rights are configured independently in each project. A user might have full rights in one project and read-only access in another.

**Q: What happens if a user is added to a project by an administrator vs. another user — is there a difference in their rights?**

**A:** No functional difference in the resulting access. Regardless of who added them, the user's rights are determined by what was configured at the time they were added.

---

# 6. Common Mistakes & Gotchas

**Contacting the wrong support team for login issues.** If the installation uses SSO, the REDCap support team cannot help with password resets or account lockouts — that must go through central IT. Knowing which authentication method is in use saves time for everyone.

**Assuming account access equals project access.** A user who can log in but cannot find a project has a Tier 2 problem, not a Tier 1 problem. They need to be added to the project — they do not need a new account or a password reset.

**Assuming project access equals full rights.** Being added to a project does not mean a user can do everything in it. User rights at Tier 3 may restrict their view, editing ability, or access to features. Always check the user's actual rights configuration when troubleshooting capability problems.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-22 — Export Users API** — retrieve user permissions and settings for all users in a project
- **RC-API-23 — Import Users API** — add or update user access and permissions programmatically
- **RC-API-24 — Delete Users API** — remove a user from a project programmatically
- **RC-API-25 — Export User Roles API** — retrieve custom role definitions and their permission sets
- **RC-API-26 — Import User Roles API** — create or update custom user roles programmatically
- **RC-API-27 — Delete User Roles API** — remove a custom role from the project programmatically

---


# 7. Related Articles

- RC-USER-02 — User Rights: Adding Users & Managing Roles
- RC-USER-03 — User Rights: Configuring User Privileges
- RC-USER-04 — User Rights: User Management
- RC-DAG-01 — Data Access Groups
