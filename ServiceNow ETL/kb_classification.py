"""
kb_classification.py
Publish classification for REDCap KB articles going into ServiceNow.

Given an article's RC-xxx source_id, classify() returns:
  - audience          : End-user | Power-user | Power-user/Admin | Admin | Exclude
  - feature_dependent : Yes | No
  - avail_<instance>  : one column per instance defined in the classification file
        Standard | On | On* (per-project admin activation) | Off | Verify | Part | —
  - publish_plan      : Publish | Draft (banner) | Draft (verify) | Hold | Hold (admin KB) | Exclude
  - rollout_phase     : 0 pilot | 1 core end-user | 2 feature-gated/advanced | 3 admin KB | — held/excluded
  - workflow_state    : ServiceNow value (published | draft | retired) derived from publish_plan
  - availability_note : action / caveat text
  - topic_area        : readable topic for the article's domain

Everything institution-specific — which REDCap instances exist, what is enabled
where, which articles to hold or exclude — lives in a classification file
OUTSIDE this repo. Point to it with `etl.classification_file` in
config.local.yaml (see config.example.yaml); `classification.example.yaml` in
this folder documents the format. Without a classification file every article
gets the generic default: End-user, Publish, no per-instance columns.

Resolution order for one article: overrides → topic_rules → generic default.
Articles in `pilot` that end up as a plain Publish get rollout_phase 0.
"""
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _REPO_ROOT / "config.local.yaml"

TOPIC = {
    "AI":"AI Tools","ALERT":"Alerts & Notifications","API":"API","AT":"Action Tags",
    "BL":"Branching Logic","CAL":"Calendar","CALC":"Calculations","CC":"Control Center",
    "CDIS":"Clinical Data (CDIS)","DAG":"Data Access Groups","DDE":"Double Data Entry",
    "DDP":"Dynamic Data Pull","DE":"Data Entry","DQ":"Data Quality","DSGN":"Project Design",
    "EM":"External Modules","EXPRT":"Data Export","FD":"Form Design","FDL":"Form Display Logic",
    "FILE":"File Repository","IMP":"Data Import","INFRA":"Self-Hosting","INST":"Instance Policies",
    "INTG":"Integrations","LOCK":"Record Locking","LOG":"Logging","LONG":"Longitudinal",
    "MCP":"MCP Server","MLM":"Multi-Language Mgmt","MOB":"Mobile App","MSG":"Messenger",
    "MYCAP":"MyCap","NAV":"Navigation","OPS":"Operational Use","PIPE":"Piping & Smart Vars",
    "PLUS":"REDCap Plus","PROF":"My Profile","PROJ":"Project Lifecycle","RAND":"Randomization",
    "SENDIT":"Send-It","SURV":"Surveys","TXT":"Texting (Twilio)","USER":"User Rights",
}

# ServiceNow workflow_state derived from the publish plan
PLAN_TO_STATE = {
    "Publish":"published",
    "Draft (banner)":"draft",
    "Draft (verify)":"draft",
    "Hold":"draft",
    "Hold (admin KB)":"draft",
    "Exclude":"retired",
}

_GENERIC_DEFAULT = {"audience": "End-user", "feature_dependent": "No", "availability": "standard",
                    "publish_plan": "Publish", "note": ""}


def _load_data() -> dict:
    """Load the institution's classification file named in config.local.yaml, if any."""
    if not _CONFIG_PATH.exists():
        return {}
    cfg = yaml.safe_load(_CONFIG_PATH.read_text(encoding="utf-8")) or {}
    path = (cfg.get("etl") or {}).get("classification_file")
    if not path:
        return {}
    path = Path(path).expanduser()
    if not path.is_absolute():
        path = _REPO_ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


_DATA = _load_data()
INSTITUTION = _DATA.get("institution", "")
INSTANCES = _DATA.get("instances", [])          # [{"key": ..., "label": ..., "host": ...}, ...]
INSTANCE_KEYS = [i["key"] for i in INSTANCES]
AVAIL_COLUMNS = [f"avail_{k}" for k in INSTANCE_KEYS]
PILOT = set(_DATA.get("pilot", []))
TOPIC.update(_DATA.get("topic_labels", {}))
_RULES = _DATA.get("topic_rules", [])
_OVERRIDES = _DATA.get("overrides", {})


def _availability(spec) -> list:
    """'standard' / 'none' / {instance_key: value} → one value per instance."""
    if spec == "standard":
        return ["Standard"] * len(INSTANCE_KEYS)
    if spec in (None, "none"):
        return ["—"] * len(INSTANCE_KEYS)
    return [spec.get(k, "—") for k in INSTANCE_KEYS]


def _shortid(source_id: str) -> str:
    return str(source_id).split("_")[0].strip()

def topic_key(short_id: str) -> str:
    parts = short_id.split("-")
    return parts[1] if len(parts) >= 2 else short_id

def classify(source_id: str) -> dict:
    """Return the publish classification for one article."""
    sid = _shortid(source_id)
    entry = _OVERRIDES.get(sid)
    if entry is None:
        p = topic_key(sid)
        entry = next((r for r in _RULES if p in r.get("topics", [])), None)
    if entry is None:
        entry = dict(_GENERIC_DEFAULT, phase="0" if sid in PILOT else "1")
    plan = entry["publish_plan"]
    phase = str(entry.get("phase", "1"))
    # pilot promotion for any plain end-user publish core
    if plan == "Publish" and sid in PILOT:
        phase = "0"
    result = {
        "audience": entry["audience"],
        "feature_dependent": entry["feature_dependent"],
    }
    result.update(zip(AVAIL_COLUMNS, _availability(entry.get("availability", "standard"))))
    result.update({
        "publish_plan": plan,
        "rollout_phase": phase,
        "workflow_state": PLAN_TO_STATE.get(plan, "draft"),
        "availability_note": entry.get("note", ""),
        "topic_area": TOPIC.get(topic_key(sid), topic_key(sid)),
    })
    return result
