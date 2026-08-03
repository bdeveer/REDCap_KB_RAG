"""
kb_yale_classification.py
Yale-specific publish classification for REDCap KB articles going into ServiceNow.

Given an article's RC-xxx source_id, returns:
  - audience         : End-user | Power-user | Power-user/Admin | Admin | Exclude
  - feature_dependent: Yes | No
  - avail_rc1/rc2/connect/p11 : per-instance availability
        Standard | On | On* (per-project admin activation) | Off | Verify | Part | —
  - publish_plan     : Publish | Draft (banner) | Draft (verify) | Hold | Hold (admin KB) | Exclude
  - phase            : 0 pilot | 1 core end-user | 2 feature-gated/advanced | 3 admin KB | — held/excluded
  - workflow_state   : ServiceNow value (published | draft | retired) derived from publish_plan
  - availability_note: action / caveat text

Feature availability is sourced from:
  repo/current-projects/config-scan/instance-settings-checklist.md  (section 6, CC-confirmed)
Instances: RC1 = redcap.med.yale.edu, RC2 = redcap.research.yale.edu,
           Connect = redcapynh.ynhh.org (YNHH), P11 = redcapynh-p11.ynhh.org (21 CFR Part 11)

Keep this file in sync with the config scan whenever Yale enablement changes.
"""

TOPIC = {
    "AI":"AI Tools","ALERT":"Alerts & Notifications","API":"API","AT":"Action Tags",
    "BL":"Branching Logic","CAL":"Calendar","CALC":"Calculations","CC":"Control Center",
    "CDIS":"Clinical Data (CDIS)","DAG":"Data Access Groups","DDE":"Double Data Entry",
    "DDP":"Dynamic Data Pull","DE":"Data Entry","DQ":"Data Quality","DSGN":"Project Design",
    "EM":"External Modules","EXPRT":"Data Export","FD":"Form Design","FDL":"Form Display Logic",
    "FILE":"File Repository","IMP":"Data Import","INFRA":"Self-Hosting","INST":"Yale Instance Policies",
    "INTG":"Integrations","LOCK":"Record Locking","LOG":"Logging","LONG":"Longitudinal",
    "MCP":"MCP Server","MLM":"Multi-Language Mgmt","MOB":"Mobile App","MSG":"Messenger",
    "MYCAP":"MyCap","NAV":"Navigation","OPS":"Operational Use","PIPE":"Piping & Smart Vars",
    "PLUS":"REDCap Plus","PROF":"My Profile","PROJ":"Project Lifecycle","RAND":"Randomization",
    "SENDIT":"Send-It","SURV":"Surveys","TXT":"Texting (Twilio)","USER":"User Rights",
}

# Highest-traffic, always-on end-user topics -> Phase 0 pilot
PILOT = {"RC-DE-01","RC-DE-02","RC-DE-04","RC-FD-01","RC-FD-02","RC-BL-01","RC-SURV-01",
         "RC-PIPE-01","RC-EXPRT-01","RC-USER-01","RC-PROJ-02","RC-NAV-UI-01","RC-CALC-02",
         "RC-ALERT-01","RC-IMP-01"}

STD = ("Standard","Standard","Standard","Standard")   # RC1, RC2, Connect, P11
NA  = ("—","—","—","—")

# ServiceNow workflow_state derived from the publish plan
PLAN_TO_STATE = {
    "Publish":"published",
    "Draft (banner)":"draft",
    "Draft (verify)":"draft",
    "Hold":"draft",
    "Hold (admin KB)":"draft",
    "Exclude":"retired",
}

# Per-ID overrides: short_id -> (audience, feature_dependent, (rc1,rc2,connect,p11), publish_plan, phase, note)
OV = {}
for a in ["RC-AI-01","RC-AI-02","RC-AI-03","RC-AI-04"]:
    OV[a]=("End-user","Yes",("Off","Off","Off","Off"),"Hold","—",
           "AI Tools disabled on all four instances — do not publish until enabled at Yale.")
for i in range(1,9):
    OV[f"RC-MYCAP-0{i}"]=("End-user","Yes",("On*","On*","On*","Off"),"Draft (banner)","2",
           "Enabled with per-project admin activation on RC1/RC2/Connect; disabled on P11. Add activation + P11-exclusion banner.")
OV["RC-PIPE-16"]=("End-user","Yes",("On*","On*","On*","Off"),"Draft (banner)","2",
           "MyCap smart variables — same gating as MyCap (activation; P11 excluded).")
OV["RC-TXT-01"]=("End-user","Yes",("On*","On*","On*","Off"),"Draft (banner)","2",
           "Twilio enabled with per-project admin activation on RC1/RC2/Connect; disabled on P11.")
OV["RC-TXT-02"]=("Admin","Yes",("On*","On*","On*","Off"),"Hold (admin KB)","3",
           "Administrator/Twilio setup — internal admin KB, not end-user.")
OV["RC-MOB-01"]=("End-user","Yes",("On","On","On","Off"),"Draft (banner)","2",
           "Mobile App enabled on RC1/RC2/Connect; disabled on P11. Note P11 exclusion.")
OV["RC-AT-11"]=("End-user","Yes",("On","On","On","Off"),"Draft (banner)","2",
           "Mobile-App action tags — only relevant where Mobile App is enabled (not P11).")
OV["RC-MLM-01"]=("End-user","Yes",("On","On","On","Off"),"Draft (banner)","2",
           "MLM enabled on RC1/RC2/Connect; disabled on P11. Note P11 exclusion.")
OV["RC-CC-20"]=("Admin","Yes",("On","On","On","Off"),"Hold (admin KB)","3",
           "MLM admin/Control-Center view — duplicate of RC-MLM-01 for admins.")
OV["RC-CDIS-01"]=("Admin","Yes",("Off","Off","On","Off"),"Hold (admin KB)","3",
           "CDIS setup — enabled only on REDCap Connect (YNHH). Admin/Connect-only.")
OV["RC-CDIS-02"]=("End-user","Yes",("Off","Off","On","Off"),"Draft (banner)","2",
           "Clinical Data Pull usage — enabled only on Connect. Publish as a Connect-only article.")
OV["RC-CDIS-03"]=("End-user","Yes",("Off","Off","Off","Off"),"Hold","—",
           "Clinical Data Mart not offered at Yale (CDP only) — hold.")
OV["RC-CDIS-04"]=("End-user","Yes",("Off","Off","Part","Off"),"Hold","—",
           "CDP-vs-CDM comparison — CDM not offered; hold or trim to CDP-only to avoid implying CDM is available.")
OV["RC-DDP-01"]=("End-user","Yes",("Off","Off","On","Off"),"Draft (banner)","2",
           "Dynamic Data Pull rides on CDIS/EHR — enabled only on Connect. Connect-only; verify vs CDP scope.")
OV["RC-DDP-02"]=("Admin","Yes",("Off","Off","On","Off"),"Hold (admin KB)","3",
           "DDP admin/technical setup — Connect-only, admin KB.")
for a in ["RC-INFRA-01","RC-INFRA-02"]:
    OV[a]=("Exclude","No",NA,"Exclude","—","About self-hosting your own REDCap server — not applicable to Yale users.")
OV["RC-MCP-01"]=("Exclude","No",NA,"Exclude","—","About the KB's own MCP server tooling — not a Yale REDCap end-user feature.")
OV["RC-PLUS-01"]=("Exclude","No",NA,"Exclude","—","REDCap Plus is a separate paid subscription — not offered at Yale.")
for a in ["RC-INST-01","RC-INST-02","RC-INST-03"]:
    OV[a]=("End-user","No",STD,"Publish","1",
           "Yale-specific policy article — populate from config-scan/instance-settings-checklist.md before publishing. HIGH value.")
OV["RC-INTG-01"]=("Power-user","No",STD,"Publish","2","Data Entry Trigger enabled on all four; advanced/power-user topic.")
OV["RC-OPS-01"]=("Power-user","No",STD,"Publish","2","Advanced design/use-case article.")
OV["RC-FD-12"]=("Power-user","Yes",("On*","On*","On*","On*"),"Draft (banner)","2",
           "Dynamic SQL field type is admin-granted per user — note the request step.")
OV["RC-AT-EM-01"]=("End-user","Yes",("Verify","Verify","Verify","Verify"),"Draft (verify)","2",
           "Depends on the HIDESUBMIT external module being installed/enabled — verify per instance before publishing.")
OV["RC-USER-04"]=("Admin","No",NA,"Hold (admin KB)","3","System-wide user management — admin KB.")
OV["RC-DE-13"]=("End-user","No",STD,"Publish","1",
           "Bulk Record Delete (one action here) is disabled on RC1/RC2/P11, enabled on Connect — note the exception in the article.")
OV["RC-LOCK-01"]=("End-user","No",STD,"Publish","1",
           "Base locking/e-signature enabled on all four; the Part 11 E-Sign+Locking enhancement is enabled only on P11 (SFTP).")
OV["RC-PROF-01"]=("End-user","No",STD,"Publish","1",
           "Profile name/email editable on RC1/RC2; locked on Connect/P11 — note the difference.")
for a in ["RC-PROJ-01","RC-PROJ-02","RC-PROJ-03","RC-PROJ-04","RC-PROJ-05"]:
    OV[a]=("End-user","No",STD,"Publish","1",
           "Project creation & production-move policy differ by instance (self-serve vs request) — see config-scan section 5.")


def _shortid(source_id: str) -> str:
    return str(source_id).split("_")[0].strip()

def topic_key(short_id: str) -> str:
    parts = short_id.split("-")
    if len(parts) >= 2 and parts[1] in ("NAV","AT"):
        return parts[1]
    return parts[1] if len(parts) >= 2 else short_id

def classify(source_id: str) -> dict:
    """Return the Yale publish classification for one article."""
    sid = _shortid(source_id)
    if sid in OV:
        aud, fd, av, plan, phase, note = OV[sid]
    else:
        p = topic_key(sid)
        if p in ("CC","EM"):
            aud,fd,av,plan,phase,note = ("Admin","No",NA,"Hold (admin KB)","3",
                "Control-Center / module administration — internal admin KB.")
        elif p == "API":
            aud,fd,av,plan,phase,note = ("Power-user/Admin","No",NA,"Hold (admin KB)","3",
                "API method reference (56 articles) — power-user/admin KB, later phase.")
        elif p == "RAND":
            aud,fd,av,plan,phase,note = ("End-user","Yes",("On","On","On","On"),"Publish","1",
                "Randomization enabled on all four instances (per-project setup).")
        elif p in ("SURV","MSG","SENDIT"):
            aud,fd,av,plan,phase,note = ("End-user","Yes",("On","On","On","On"),"Publish","1",
                "Enabled on all four instances.")
        else:
            phase = "0" if sid in PILOT else "1"
            aud,fd,av,plan,note = ("End-user","No",STD,"Publish","")
    # pilot promotion for any plain end-user publish core
    if plan == "Publish" and sid in PILOT:
        phase = "0"
    return {
        "audience": aud,
        "feature_dependent": fd,
        "avail_rc1": av[0], "avail_rc2": av[1], "avail_connect": av[2], "avail_p11": av[3],
        "publish_plan": plan,
        "yale_phase": phase,
        "workflow_state": PLAN_TO_STATE.get(plan, "draft"),
        "availability_note": note,
        "topic_area": TOPIC.get(topic_key(sid), topic_key(sid)),
    }
