#!/usr/bin/env python3
"""
REDCap MCP Server

Exposes all major REDCap API methods as MCP tools so that Claude can
query and update REDCap projects directly.

Environment variables:
  REDCAP_URL    (required) Full URL to your REDCap API endpoint, e.g.
                https://redcap.yourinstitution.edu/api/
                Can be overridden per call via the redcap_url parameter.

  REDCAP_TOKEN  (optional) Default project API token. Can be overridden
                per call via the token parameter. Treat like a password.

Multi-instance usage:
  Register separate named servers for each environment:
    claude mcp add --scope user redcap-prod --env REDCAP_URL=https://redcap.example.edu/api/ -- python3 redcap_mcp_server.py
    claude mcp add --scope user redcap-test --env REDCAP_URL=https://redcap-test.example.edu/api/ -- python3 redcap_mcp_server.py
    claude mcp add --scope user redcap-dev  --env REDCAP_URL=https://redcap-dev.example.edu/api/  -- python3 redcap_mcp_server.py

  Or pass redcap_url directly on any tool call to override for that call only.

Setup:
  pip install "mcp[cli]" requests
  bash install.sh
"""

import json
import os
from typing import Any, Dict, List, Optional

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("REDCap API")


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _api_url(override: Optional[str] = None) -> str:
    url = (override or os.environ.get("REDCAP_URL", "")).strip()
    if not url:
        raise ValueError(
            "No REDCap URL provided. Pass a redcap_url argument to this tool, "
            "or set the REDCAP_URL environment variable. "
            "Example: https://redcap.yourinstitution.edu/api/"
        )
    if not url.endswith("/"):
        url += "/"
    return url


def _resolve_token(token: Optional[str]) -> str:
    t = (token or os.environ.get("REDCAP_TOKEN", "")).strip()
    if not t:
        raise ValueError(
            "No API token provided. Pass a token argument to this tool, "
            "or set the REDCAP_TOKEN environment variable."
        )
    return t


def _post_file(
    params: Dict[str, Any],
    file_path: str,
    file_field: str = "file",
    api_url: Optional[str] = None,
) -> Any:
    """
    POST multipart/form-data to the REDCap API (for file uploads).
    The file at file_path is opened and sent under file_field.
    """
    url = _api_url(api_url)
    flat: Dict[str, str] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            flat[key] = "1" if value else "0"
        else:
            flat[key] = str(value)

    with open(file_path, "rb") as fh:
        resp = requests.post(url, data=flat, files={file_field: fh}, verify=True)

    if resp.status_code == 200:
        try:
            data = resp.json()
            if isinstance(data, dict) and "error" in data:
                return {"status": "error", "message": data["error"]}
            return {"status": "success", "data": data}
        except Exception:
            text = resp.text.strip()
            return {"status": "success", "data": text if text else "(empty — upload accepted)"}
    else:
        return {
            "status": "error",
            "http_status": resp.status_code,
            "message": resp.text,
        }


def _post(
    params: Dict[str, Any],
    binary: bool = False,
    api_url: Optional[str] = None,
) -> Any:
    """
    POST to the REDCap API. List values are expanded into indexed keys
    (records[0], records[1], …) as the API expects. Always uses SSL verification.
    """
    url = _api_url(api_url)
    flat: Dict[str, str] = {}

    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            for i, item in enumerate(value):
                flat[f"{key}[{i}]"] = str(item)
        elif isinstance(value, bool):
            flat[key] = "1" if value else "0"
        else:
            flat[key] = str(value)

    resp = requests.post(url, data=flat, verify=True)

    if binary:
        return {
            "status": "success" if resp.status_code == 200 else "error",
            "http_status": resp.status_code,
            "content_type": resp.headers.get("Content-Type", ""),
            "size_bytes": len(resp.content),
            "message": resp.text if resp.status_code != 200 else None,
        }

    if resp.status_code == 200:
        try:
            data = resp.json()
            if isinstance(data, dict) and "error" in data:
                return {"status": "error", "message": data["error"]}
            return {"status": "success", "data": data}
        except Exception:
            return {"status": "success", "data": resp.text}
    else:
        return {
            "status": "error",
            "http_status": resp.status_code,
            "message": resp.text,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Connection check
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def check_connection(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Verify that the REDCap URL and API token are working by fetching the
    REDCap version. Use this to confirm a server is reachable before
    running other tools.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: Full API endpoint URL (overrides REDCAP_URL env var),
                    e.g. https://redcap-test.yourinstitution.edu/api/
    """
    return _post(
        {"token": _resolve_token(token), "content": "version", "returnFormat": "json"},
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Records
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_records(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    records: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    forms: Optional[List[str]] = None,
    events: Optional[List[str]] = None,
    raw_or_label: str = "raw",
    export_data_access_groups: bool = False,
    export_survey_fields: bool = False,
    record_type: str = "flat",
    filter_logic: Optional[str] = None,
) -> dict:
    """
    Export records from a REDCap project.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        records: Record IDs to export. If omitted, all records are exported.
        fields: Variable names to include. If omitted, all fields are included.
        forms: Instrument names to include (use the variable name, not the display label).
        events: Event names to include. Only applies to longitudinal projects.
        raw_or_label: 'raw' (default) returns coded values; 'label' returns display labels.
        export_data_access_groups: Include the redcap_data_access_group column.
        export_survey_fields: Include survey timestamp and identifier fields.
        record_type: 'flat' (default, one row per record/event) or 'eav' (one row per field value).
        filter_logic: REDCap filter expression to restrict records, e.g. "[age] > 18".
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "record",
            "format": "json",
            "type": record_type,
            "records": records,
            "fields": fields,
            "forms": forms,
            "events": events,
            "rawOrLabel": raw_or_label,
            "exportDataAccessGroups": export_data_access_groups,
            "exportSurveyFields": export_survey_fields,
            "filterLogic": filter_logic,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_records(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    overwrite_behavior: str = "normal",
    date_format: str = "YMD",
    return_content: str = "count",
    force_auto_number: bool = False,
) -> dict:
    """
    Import or update records in a REDCap project. For longitudinal projects,
    include 'redcap_event_name' in each record dict.

    Args:
        data: List of record dicts. Each dict must include the record ID field
              and the fields to import.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        overwrite_behavior: 'normal' (default, blank fields in data are ignored) or
                           'overwrite' (blank fields erase existing values).
        date_format: 'YMD' (default, YYYY-MM-DD), 'MDY' (MM/DD/YYYY), or 'DMY' (DD/MM/YYYY).
        return_content: 'count' (default), 'ids' (imported record IDs), or
                       'auto_ids' (when force_auto_number is true).
        force_auto_number: If True, auto-number the record ID even if one is provided.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "record",
            "format": "json",
            "type": "flat",
            "data": json.dumps(data),
            "overwriteBehavior": overwrite_behavior,
            "dateFormat": date_format,
            "returnContent": return_content,
            "forceAutoNumber": force_auto_number,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def delete_records(
    records: List[str],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    arm: Optional[int] = None,
    event: Optional[str] = None,
    instrument: Optional[str] = None,
) -> dict:
    """
    Delete records from a REDCap project. CAUTION: deletion is permanent.

    To delete only an instrument's data (not the whole record), specify instrument.
    To delete only one event's data, specify event.

    Args:
        records: Record IDs to delete.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        arm: Arm number — limits deletion to records in that arm (multi-arm projects).
        event: Unique event name — deletes only that event's data, not the whole record.
        instrument: Instrument variable name — deletes only that form's data for the records.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "action": "delete",
            "content": "record",
            "records": records,
            "arm": arm,
            "event": event,
            "instrument": instrument,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def rename_record(
    record: str,
    new_record_name: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    arm: Optional[int] = None,
) -> dict:
    """
    Rename a record (change its record ID value).

    Args:
        record: Current record ID.
        new_record_name: New record ID.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        arm: Arm number (longitudinal projects with multiple arms).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "record",
            "action": "rename",
            "record": record,
            "new_record_name": new_record_name,
            "arm": arm,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def generate_next_record_name(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Get the next auto-number that REDCap would assign to a new record.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {"token": _resolve_token(token), "content": "generateNextRecordName", "returnFormat": "json"},
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Project Metadata & Structure
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_project_info(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Export project-level settings: title, purpose, dates, status, missing data
    codes, and other configuration flags.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {"token": _resolve_token(token), "content": "project", "format": "json", "returnFormat": "json"},
        api_url=redcap_url,
    )


@mcp.tool()
def import_project_info(
    data: dict,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Update project-level settings (title, purpose, missing data codes, etc.).

    Args:
        data: Dict of project settings to update.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "project_settings",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_metadata(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    fields: Optional[List[str]] = None,
    forms: Optional[List[str]] = None,
) -> dict:
    """
    Export the project's data dictionary (metadata). Returns all field definitions
    including variable names, labels, field types, validation, branching logic,
    and choice labels.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        fields: Limit to specific field variable names.
        forms: Limit to fields on specific instruments.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "metadata",
            "format": "json",
            "fields": fields,
            "forms": forms,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_metadata(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Import (replace) the project data dictionary. WARNING: this overwrites the
    existing data dictionary. In production projects, changes go through draft
    mode and require administrator approval.

    Args:
        data: List of field definition dicts matching REDCap's metadata structure.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "metadata",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_field_names(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    field: Optional[str] = None,
) -> dict:
    """
    Export the list of all export field names. Particularly useful for checkbox
    fields, which expand into multiple export columns (e.g. symptoms___1, symptoms___2).

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        field: Limit to a single field name.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "exportFieldNames",
            "format": "json",
            "field": field,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_instruments(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    List all instruments (forms) in the project with their variable names and labels.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {"token": _resolve_token(token), "content": "instrument", "format": "json", "returnFormat": "json"},
        api_url=redcap_url,
    )


@mcp.tool()
def export_project_xml(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    return_metadata_only: bool = False,
    export_files: bool = False,
) -> dict:
    """
    Export the entire project as CDISC ODM XML, including metadata and optionally records.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        return_metadata_only: If True, export only metadata, no record data.
        export_files: If True, include uploaded files as base64-encoded attachments.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "project_xml",
            "returnMetadataOnly": return_metadata_only,
            "exportFiles": export_files,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_redcap_version(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Get the REDCap version running on the server.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {"token": _resolve_token(token), "content": "version", "returnFormat": "json"},
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Longitudinal: Arms, Events, Instrument-Event Mappings
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_arms(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    arms: Optional[List[int]] = None,
) -> dict:
    """
    List all arms in a longitudinal project.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        arms: Specific arm numbers to export. If omitted, all arms are returned.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "arm",
            "format": "json",
            "arms": [str(a) for a in arms] if arms else None,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_arms(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    override: bool = False,
) -> dict:
    """
    Add or modify arms in a longitudinal project.

    Args:
        data: List of arm dicts with 'arm_num' (int) and 'name' (str) keys.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        override: If True, replace all existing arms. If False (default), merge/update.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "arm",
            "action": "import",
            "format": "json",
            "override": override,
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def delete_arms(
    arms: List[int],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Delete arms from a longitudinal project.

    Args:
        arms: List of arm numbers to delete.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "arm",
            "action": "delete",
            "arms": [str(a) for a in arms],
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_events(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    arms: Optional[List[int]] = None,
) -> dict:
    """
    List all events in a longitudinal project.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        arms: Limit to events in specific arm numbers.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "event",
            "format": "json",
            "arms": [str(a) for a in arms] if arms else None,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_events(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    override: bool = False,
) -> dict:
    """
    Add or modify events in a longitudinal project.

    Args:
        data: List of event dicts. Each dict should include: event_name, arm_num,
              day_offset, offset_min, offset_max, unique_event_name.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        override: If True, replace all existing events. If False (default), merge/update.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "event",
            "action": "import",
            "format": "json",
            "override": override,
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def delete_events(
    events: List[str],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Delete events from a longitudinal project.

    Args:
        events: List of unique event names to delete.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "event",
            "action": "delete",
            "events": events,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_instrument_event_mappings(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    arms: Optional[List[int]] = None,
) -> dict:
    """
    Export which instruments are assigned to which events (longitudinal projects).

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        arms: Limit to specific arm numbers.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "formEventMapping",
            "format": "json",
            "arms": [str(a) for a in arms] if arms else None,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_instrument_event_mappings(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Update which instruments are assigned to which events (longitudinal projects).

    Args:
        data: List of dicts with 'arm_num', 'unique_event_name', and 'form' keys.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "formEventMapping",
            "action": "import",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Users, Roles, and DAGs
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_users(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    List all users in the project with their access rights.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {"token": _resolve_token(token), "content": "user", "format": "json", "returnFormat": "json"},
        api_url=redcap_url,
    )


@mcp.tool()
def import_users(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Add users to the project or update their rights.

    Args:
        data: List of user rights dicts. Must include 'username' plus any rights fields
              to set (e.g., data_export, data_import_tool, api_export, api_import, etc.).
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "user",
            "action": "import",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def delete_users(
    users: List[str],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Remove users from the project.

    Args:
        users: List of usernames to remove.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "user",
            "action": "delete",
            "users": users,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_user_roles(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    List all user roles defined in the project.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {"token": _resolve_token(token), "content": "userRole", "format": "json", "returnFormat": "json"},
        api_url=redcap_url,
    )


@mcp.tool()
def import_user_roles(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Create or update user roles in the project.

    Args:
        data: List of role definition dicts. Include 'unique_role_name' for updates,
              or omit it to create a new role.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "userRole",
            "action": "import",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def delete_user_roles(
    roles: List[str],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Delete user roles from the project.

    Args:
        roles: List of unique role names to delete.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "userRole",
            "action": "delete",
            "roles": roles,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_user_role_assignments(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Show which users are assigned to which roles.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "userRoleMapping",
            "action": "export",
            "format": "json",
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_user_role_assignments(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Update user-role assignments.

    Args:
        data: List of dicts with 'username' and 'unique_role_name' keys.
              Use empty string for unique_role_name to unassign from a role.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "userRoleMapping",
            "action": "import",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_dags(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    List all Data Access Groups (DAGs) in the project.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "dag",
            "action": "export",
            "format": "json",
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_dags(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Create or update Data Access Groups.

    Args:
        data: List of DAG dicts with 'data_access_group_name' (required) and
              optionally 'unique_group_name' (for updates).
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "dag",
            "action": "import",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def delete_dags(
    dags: List[str],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Delete Data Access Groups from the project.

    Args:
        dags: List of unique DAG names to delete.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "dag",
            "action": "delete",
            "dags": dags,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_dag_assignments(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Show which users are assigned to which Data Access Groups.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "userDagMapping",
            "action": "export",
            "format": "json",
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_dag_assignments(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Update user-DAG assignments.

    Args:
        data: List of dicts with 'username' and 'redcap_data_access_group' keys.
              Set redcap_data_access_group to empty string to unassign a user.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "userDagMapping",
            "action": "import",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def switch_dag(
    dag: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Switch the active DAG context for the API token user.

    Args:
        dag: The unique DAG name to switch to. Use empty string to switch to no DAG.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "dag",
            "action": "switch",
            "dag": dag,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Files
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_file_info(
    record: str,
    field: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
    repeat_instrument: Optional[str] = None,
    repeat_instance: Optional[int] = None,
) -> dict:
    """
    Get metadata about a file attached to a file-upload field (content-type and size).
    Note: returns file metadata only — does not download file contents.

    Args:
        record: Record ID.
        field: Variable name of the file-upload field.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (longitudinal projects).
        repeat_instrument: Repeating instrument name.
        repeat_instance: Repeating instance number.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "file",
            "action": "export",
            "record": record,
            "field": field,
            "event": event,
            "repeat_instrument": repeat_instrument,
            "repeat_instance": repeat_instance,
            "returnFormat": "json",
        },
        binary=True,
        api_url=redcap_url,
    )


@mcp.tool()
def delete_file(
    record: str,
    field: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
    repeat_instrument: Optional[str] = None,
    repeat_instance: Optional[int] = None,
) -> dict:
    """
    Delete a file from a file-upload field.

    Args:
        record: Record ID.
        field: Variable name of the file-upload field.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (longitudinal projects).
        repeat_instrument: Repeating instrument name.
        repeat_instance: Repeating instance number.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "file",
            "action": "delete",
            "record": record,
            "field": field,
            "event": event,
            "repeat_instrument": repeat_instrument,
            "repeat_instance": repeat_instance,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Reports and Logging
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_report(
    report_id: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    raw_or_label: str = "raw",
) -> dict:
    """
    Export data from a saved REDCap report using its report ID. The report's
    field selection, filters, and ordering are applied automatically.

    To find the report ID: open the report in REDCap and check the URL for 'report_id='.

    Args:
        report_id: The numeric report ID.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        raw_or_label: 'raw' (default) for coded values; 'label' for display labels.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "report",
            "report_id": report_id,
            "format": "json",
            "rawOrLabel": raw_or_label,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_logging(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    log_type: Optional[str] = None,
    user: Optional[str] = None,
    record: Optional[str] = None,
    dag: Optional[str] = None,
    begin_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> dict:
    """
    Export the project audit log entries.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        log_type: Filter by type. One of: 'export', 'manage', 'user', 'record',
                  'record_add', 'record_edit', 'record_delete', 'lock_record', 'page_view'.
                  Leave blank for all types.
        user: Filter by username.
        record: Filter by record ID.
        dag: Filter by DAG name.
        begin_time: Start of date range in format 'YYYY-MM-DD HH:MM'.
        end_time: End of date range in format 'YYYY-MM-DD HH:MM'.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "log",
            "format": "json",
            "logtype": log_type,
            "user": user,
            "record": record,
            "dag": dag,
            "beginTime": begin_time,
            "endTime": end_time,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Surveys
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_survey_participants(
    instrument: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
) -> dict:
    """
    List survey participants for a specific instrument (participant-list surveys only).

    Args:
        instrument: The instrument's unique variable name.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (longitudinal projects).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "participantList",
            "format": "json",
            "instrument": instrument,
            "event": event,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_survey_link(
    record: str,
    instrument: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
    repeat_instance: Optional[int] = None,
) -> dict:
    """
    Generate a unique survey link for a specific record and instrument.

    Args:
        record: Record ID.
        instrument: The instrument's unique variable name.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (longitudinal projects).
        repeat_instance: Repeating instance number.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "surveyLink",
            "record": record,
            "instrument": instrument,
            "event": event,
            "repeat_instance": repeat_instance,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_survey_queue_link(
    record: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Get the survey queue link for a specific record.

    Args:
        record: Record ID.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "surveyQueueLink",
            "record": record,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_survey_return_code(
    record: str,
    instrument: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
    repeat_instance: Optional[int] = None,
) -> dict:
    """
    Get the return code for a partially completed survey, allowing the respondent
    to resume where they left off.

    Args:
        record: Record ID.
        instrument: The instrument's unique variable name.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (longitudinal projects).
        repeat_instance: Repeating instance number.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "surveyReturnCode",
            "record": record,
            "instrument": instrument,
            "event": event,
            "repeat_instance": repeat_instance,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Record-level File Import  (RC-API-13)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def import_file(
    record: str,
    field: str,
    file_path: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
    repeat_instance: Optional[int] = None,
) -> dict:
    """
    Upload a file to a file-upload field on a specific record. The file must
    be accessible on the filesystem of the machine running this MCP server.
    Cannot be used with Signature fields.

    Args:
        record: Record ID to attach the file to.
        field: Variable name of the file-upload field.
        file_path: Absolute path to the local file to upload.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (longitudinal projects only).
        repeat_instance: Repeating instance number (defaults to 1).
    """
    return _post_file(
        {
            "token": _resolve_token(token),
            "content": "file",
            "action": "import",
            "record": record,
            "field": field,
            "event": event,
            "repeat_instance": repeat_instance,
            "returnFormat": "json",
        },
        file_path=file_path,
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Export Instruments as PDF  (RC-API-15)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_pdf(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    record: Optional[str] = None,
    event: Optional[str] = None,
    instrument: Optional[str] = None,
    repeat_instance: Optional[int] = None,
    all_records: bool = False,
    compact_display: bool = False,
) -> dict:
    """
    Generate a PDF of one or more data collection instruments. Returns file
    metadata (size and content-type) rather than the raw binary, since MCP
    cannot transfer binary files directly.

    Export modes:
      - Blank template for all instruments: omit record and all_records.
      - Blank template for one instrument: set instrument only.
      - One record, all instruments: set record only.
      - One record, one instrument: set record + instrument.
      - All records, all instruments: set all_records=True (record/event/instrument ignored).

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        record: Record ID to populate the PDF with data. Omit for a blank template.
        event: Unique event name (longitudinal projects). Combined with record to scope to one event.
        instrument: Instrument variable name. If omitted, all instruments are included.
        repeat_instance: Repeating instance number (defaults to 1).
        all_records: If True, export all instruments populated with data from every record.
                     Overrides record, event, and instrument.
        compact_display: If True, omit fields with no data and hide unselected choices.
    """
    params: Dict[str, Any] = {
        "token": _resolve_token(token),
        "content": "pdf",
        "returnFormat": "json",
    }
    if record:
        params["record"] = record
    if event:
        params["event"] = event
    if instrument:
        params["instrument"] = instrument
    if repeat_instance is not None:
        params["repeat_instance"] = repeat_instance
    if all_records:
        params["allRecords"] = "1"
    if compact_display:
        params["compactDisplay"] = "TRUE"

    return _post(params, binary=True, api_url=redcap_url)


# ─────────────────────────────────────────────────────────────────────────────
# Repeating Instruments and Events  (RC-API-51, RC-API-53)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_repeating_instruments_events(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Export the list of all repeating instruments and repeating events configured
    in the project. Only instruments/events designated as repeating are returned —
    non-repeating instruments are excluded.

    In the response, rows where form_name is blank represent repeating events
    (the entire event repeats); rows with a form_name represent repeating
    instruments. Requires API Export AND Project Setup/Design privileges.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "repeatingFormsEvents",
            "format": "json",
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def import_repeating_instruments_events(
    data: List[dict],
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Configure which instruments and events are designated as repeating.
    WARNING: this REPLACES the full repeating configuration — items not
    included in data will no longer be repeating. Export first (with
    export_repeating_instruments_events) and merge before re-importing.

    Requires API Import/Update AND Project Setup/Design privileges.

    Each dict in data should have:
      - event_name: unique event name (longitudinal) or '' for classic projects.
      - form_name: instrument variable name, or '' to designate a repeating event.
      - custom_repeat_instrument_label: optional display label for the instances table.

    Args:
        data: List of repeating instrument/event definition dicts.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "repeatingFormsEvents",
            "format": "json",
            "data": json.dumps(data),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Randomize Record  (RC-API-52)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def randomize_record(
    record: str,
    randomization_id: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    return_alt: bool = False,
) -> dict:
    """
    Randomize an existing record using a configured randomization definition.
    The record must already exist and all stratification fields must be filled in.
    Requires the Randomize privilege (not just API Export/Import).

    The randomization_id is visible on the Randomization page (Design access
    required) or in the API Playground.

    For concealed allocations, target_field_alt is always '*' to preserve blinding.

    Args:
        record: Record ID to randomize. Must already exist.
        randomization_id: ID of the randomization definition to use.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        return_alt: If True, include the alternative target field value in the
                    response (randomization number for open; '*' for concealed).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "record",
            "action": "randomize",
            "record": record,
            "randomization_id": str(randomization_id),
            "format": "json",
            "returnFormat": "json",
            "returnAlt": "true" if return_alt else "false",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Survey Access Code  (RC-API-54)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def export_survey_access_code(
    record: str,
    instrument: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    event: Optional[str] = None,
    repeat_instance: Optional[int] = None,
) -> dict:
    """
    Get the short alphanumeric access code for a specific record and survey
    instrument. Participants enter this code at the REDCap survey login page
    instead of clicking a full URL — useful for printed materials, SMS, or
    in-person enrollment.

    Requires API Export AND Survey Distribution Tools privileges.

    Args:
        record: Record ID (must exist in the project).
        instrument: Instrument variable name (must be enabled as a survey).
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        event: Unique event name (required for longitudinal projects).
        repeat_instance: Repeating instance number (defaults to 1).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "surveyAccessCode",
            "record": record,
            "instrument": instrument,
            "event": event,
            "repeat_instance": repeat_instance,
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# File Repository  (RC-API-45 through RC-API-49)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def create_file_repository_folder(
    name: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    folder_id: Optional[int] = None,
    dag_id: Optional[int] = None,
    role_id: Optional[int] = None,
) -> dict:
    """
    Create a new folder in the project File Repository. Returns the folder_id
    of the new folder, which can be used as a parent for nested folders or as
    the target for file uploads.

    Requires API Import/Update AND File Repository privileges.

    Args:
        name: Folder name (max 150 characters).
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        folder_id: parent folder_id to create a sub-folder. Omit for top-level.
        dag_id: Numeric DAG ID to restrict folder access. Omit for no restriction.
        role_id: Numeric User Role ID to restrict folder access. Omit for no restriction.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "fileRepository",
            "action": "createFolder",
            "name": name,
            "folder_id": folder_id,
            "dag_id": dag_id,
            "role_id": role_id,
            "format": "json",
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def list_file_repository(
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    folder_id: Optional[int] = None,
) -> dict:
    """
    List the contents of a File Repository folder (one level deep). Returns
    sub-folders (each with a folder_id) and files (each with a doc_id).
    Omit folder_id to list the top-level File Repository.

    Use this to discover folder_id and doc_id values before acting on items.
    Requires API Export AND File Repository privileges.

    Args:
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        folder_id: folder_id to list. Omit for the top-level directory.
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "fileRepository",
            "action": "list",
            "folder_id": folder_id,
            "format": "json",
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


@mcp.tool()
def export_file_repository_file(
    doc_id: int,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Export (download) a file from the File Repository by its doc_id.
    Returns file metadata (content-type, size) rather than raw binary content,
    since MCP cannot transfer binary files directly. Use list_file_repository
    to discover doc_id values.

    Requires API Export AND File Repository privileges.

    Args:
        doc_id: The doc_id of the file to download (from list_file_repository).
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "fileRepository",
            "action": "export",
            "doc_id": str(doc_id),
            "returnFormat": "json",
        },
        binary=True,
        api_url=redcap_url,
    )


@mcp.tool()
def import_file_repository_file(
    file_path: str,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
    folder_id: Optional[int] = None,
) -> dict:
    """
    Upload a file into the File Repository. The file must be accessible on
    the filesystem of the machine running this MCP server. Returns an empty
    200 on success — use list_file_repository afterward to find the new doc_id.

    Requires API Import/Update AND File Repository privileges.

    Args:
        file_path: Absolute path to the local file to upload.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
        folder_id: folder_id to upload into. Omit to place at the top level.
    """
    return _post_file(
        {
            "token": _resolve_token(token),
            "content": "fileRepository",
            "action": "import",
            "folder_id": folder_id,
            "returnFormat": "json",
        },
        file_path=file_path,
        api_url=redcap_url,
    )


@mcp.tool()
def delete_file_repository_file(
    doc_id: int,
    token: Optional[str] = None,
    redcap_url: Optional[str] = None,
) -> dict:
    """
    Delete a file from the File Repository by its doc_id. The file is moved
    to the Recycle Bin (soft delete) and can be restored within 30 days via
    the web interface. Use list_file_repository to discover doc_id values.

    Requires API Import/Update AND File Repository privileges.

    Args:
        doc_id: The doc_id of the file to delete.
        token: API token (overrides REDCAP_TOKEN env var).
        redcap_url: API endpoint URL (overrides REDCAP_URL env var).
    """
    return _post(
        {
            "token": _resolve_token(token),
            "content": "fileRepository",
            "action": "delete",
            "doc_id": str(doc_id),
            "returnFormat": "json",
        },
        api_url=redcap_url,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
