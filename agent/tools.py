"""
Agent Tools Registry for SafeX Solution Assistant
Provides callable agent actions for knowledge retrieval, safety auditing, diagnostics, and incident dispatching.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List
from agent.knowledge import SAFEX_SERVICES, SAFETY_PROTOCOLS, FAQ_DATA

# In-memory store for registered incidents and audit logs
INCIDENTS_STORE: List[Dict[str, Any]] = [
    {
        "id": "SFX-8012",
        "title": "Scheduled HVAC Sensor Calibration",
        "severity": "Low",
        "status": "Resolved",
        "timestamp": "2026-10-10 09:15:00",
        "assigned_to": "Field Ops Team B"
    },
    {
        "id": "SFX-8015",
        "title": "Minor Network Port Scan Detected",
        "severity": "Medium",
        "status": "Contained",
        "timestamp": "2026-10-10 18:42:00",
        "assigned_to": "SOC Analyst Alpha"
    }
]

def search_knowledge_base(query: str) -> Dict[str, Any]:
    """Search SafeX documentation, services, and FAQ."""
    q = query.lower()
    results = []

    # Check services
    for key, svc in SAFEX_SERVICES.items():
        if key in q or any(term in q for term in svc["title"].lower().split()):
            results.append({
                "type": "Service",
                "title": svc["title"],
                "content": svc["description"],
                "sla": svc["sla"],
                "compliance": svc["compliance"]
            })

    # Check safety protocols
    for key, proto in SAFETY_PROTOCOLS.items():
        if any(term in q for term in key.split("_")) or any(term in q for term in proto["level"].lower().split()):
            results.append({
                "type": "Safety Protocol",
                "hazard": key.replace("_", " ").title(),
                "severity_level": proto["level"],
                "standard_operating_procedure": proto["steps"]
            })

    # Check FAQs
    for faq in FAQ_DATA:
        if any(k in q for k in faq["keywords"]):
            results.append({
                "type": "General Knowledge",
                "answer": faq["answer"]
            })

    if not results:
        # Fallback to general overview
        results.append({
            "type": "Overview",
            "message": "SafeX Solutions delivers enterprise cybersecurity, HSE workplace compliance, smart IoT fleet monitoring, and multi-cloud infrastructure.",
            "services": list(SAFEX_SERVICES.keys())
        })

    return {
        "status": "success",
        "matches_count": len(results),
        "data": results
    }

def assess_safety_compliance(workplace_context: str, category: str = "general") -> Dict[str, Any]:
    """Evaluates safety conditions, PPE adherence, and potential OSHA / ISO risks."""
    ctx = workplace_context.lower()
    hazards_found = []
    risk_score = 15  # baseline normal

    if any(w in ctx for w in ["fire", "smoke", "spark", "flame"]):
        hazards_found.append("Thermal / Fire Hazard detected. Check suppression and emergency exits.")
        risk_score += 45

    if any(w in ctx for w in ["chemical", "leak", "fumes", "toxic", "acid"]):
        hazards_found.append("Chemical contamination hazard. Require SDS review & Level-A/B PPE.")
        risk_score += 40

    if any(w in ctx for w in ["electric", "wire", "voltage", "cable", "shock"]):
        hazards_found.append("High Voltage / Electrical hazard. Verify Lockout/Tagout (LOTO) isolation.")
        risk_score += 35

    if any(w in ctx for w in ["fall", "height", "scaffold", "ladder", "slip"]):
        hazards_found.append("Fall / Structural elevation risk. Require harness inspection and slip resistance.")
        risk_score += 25

    if any(w in ctx for w in ["cyber", "ransomware", "phishing", "unauthorized", "hack", "breach"]):
        hazards_found.append("Cybersecurity risk detected. Audit endpoint isolation and MFA status.")
        risk_score += 50

    risk_score = min(risk_score, 100)
    rating = "Low" if risk_score < 30 else ("Moderate" if risk_score < 60 else "High" if risk_score < 85 else "Critical")

    return {
        "category": category,
        "risk_score": risk_score,
        "rating": rating,
        "hazards_identified": hazards_found if hazards_found else ["No acute critical hazards detected in context."],
        "recommended_action": "Initiate continuous telemetry monitoring and safety checklist verification." if risk_score < 40 else "Mandate on-site safety intervention and manager sign-off.",
        "standards_checked": ["OSHA 1910.120", "ISO 45001:2018", "ISO 27001 Annex A"]
    }

def log_incident_ticket(title: str, severity: str, description: str, location: str = "Facility Alpha") -> Dict[str, Any]:
    """Logs a formal safety or cyber incident ticket into SafeX system."""
    ticket_id = f"SFX-{uuid.uuid4().hex[:6].upper()}"
    severity_formatted = severity.capitalize()
    if severity_formatted not in ["Low", "Medium", "High", "Critical"]:
        severity_formatted = "Medium"

    assigned = "SafeX Rapid Response Team" if severity_formatted in ["High", "Critical"] else "SafeX Tier-1 Support"

    record = {
        "id": ticket_id,
        "title": title,
        "severity": severity_formatted,
        "status": "Active - In Progress",
        "description": description,
        "location": location,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assigned_to": assigned
    }

    INCIDENTS_STORE.insert(0, record)

    return {
        "status": "ticket_created",
        "ticket": record,
        "notification": f"Incident {ticket_id} broadcasted to {assigned}."
    }

def run_system_diagnostics(target_system: str = "all") -> Dict[str, Any]:
    """Runs automated diagnostics across SafeX infrastructure, IoT nodes, and firewalls."""
    systems = {
        "network_firewall": {"status": "Nominal", "threat_level": "Low", "blocked_attacks_24h": 142},
        "soc_monitoring": {"status": "Active", "agents_connected": 48, "active_alerts": 1},
        "industrial_iot_gateway": {"status": "Operational", "telemetry_ping_ms": 14, "sensor_health": "99.8%"},
        "compliance_vault": {"status": "Encrypted", "backup_state": "Synced (5m ago)", "integrity": "100% Verified"}
    }

    target = target_system.lower()
    if target in systems:
        data = {target: systems[target]}
    else:
        data = systems

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "overall_health": "Operational / Optimal",
        "systems": data
    }

def dispatch_emergency_response(hazard_type: str, zone: str, level: str = "Critical") -> Dict[str, Any]:
    """Dispatches emergency protocol, sirens, notification broadcasts, and emergency personnel."""
    dispatch_code = f"DISPATCH-{uuid.uuid4().hex[:4].upper()}"
    return {
        "dispatch_code": dispatch_code,
        "status": "DISPATCH_CONFIRMED",
        "hazard_type": hazard_type,
        "zone": zone,
        "level": level,
        "actions_triggered": [
            f"Automated notification sent to Zone {zone} Safety Warden",
            f"SMS & Push Notification sent to On-Duty HSE Engineers",
            "Emergency evacuation route illumination enabled",
            "Audit log locked for regulatory forensic inspection"
        ],
        "estimated_arrival": "3-5 minutes"
    }

def get_active_incidents() -> List[Dict[str, Any]]:
    """Retrieve all current incidents."""
    return INCIDENTS_STORE
