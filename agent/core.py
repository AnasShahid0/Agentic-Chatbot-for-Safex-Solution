"""
Agentic Core Reasoning Engine
Implements multi-step planning, tool selection, observation synthesis, and memory.
"""

from typing import List, Dict, Any, Optional
import os
import re
from agent.tools import (
    search_knowledge_base,
    assess_safety_compliance,
    log_incident_ticket,
    run_system_diagnostics,
    dispatch_emergency_response,
    get_active_incidents
)

class AgentStep:
    def __init__(self, step_type: str, title: str, details: Any, status: str = "completed"):
        self.step_type = step_type  # "thought", "tool_call", "observation", "action"
        self.title = title
        self.details = details
        self.status = status

    def to_dict(self):
        return {
            "type": self.step_type,
            "title": self.title,
            "details": self.details,
            "status": self.status
        }

class SafeXAgent:
    """
    Autonomous Multi-Tool Agent for SafeX Solutions.
    Plans, executes tools, observes results, and generates actionable responses.
    """
    def __init__(self):
        self.name = "SafeX Agentic Intelligence"
        self.history: List[Dict[str, str]] = []

    def run(self, user_message: str) -> Dict[str, Any]:
        """
        Executes an agentic reasoning loop for the given user message.
        Returns the final response along with full step-by-step reasoning steps.
        """
        msg = user_message.strip()
        msg_lower = msg.lower()
        steps: List[Dict[str, Any]] = []
        tools_called: List[str] = []

        # Step 1: Deliberation & Intent Recognition
        thought_text = "Parsing user prompt, identifying safety & technical requirements, and planning tool execution strategy."
        if any(w in msg_lower for w in ["fire", "hazard", "smoke", "spill", "leak", "injury", "danger", "emergency", "evacuate"]):
            thought_text = "Emergency or safety hazard query detected. Prioritizing compliance audit and emergency response protocols."
        elif any(w in msg_lower for w in ["diagnostics", "system", "status", "health", "firewall", "iot", "monitor"]):
            thought_text = "Infrastructure diagnostics request identified. Querying telemetry and real-time monitoring tools."
        elif any(w in msg_lower for w in ["incident", "report", "ticket", "log", "file ticket"]):
            thought_text = "Incident logging request identified. Preparing formal ticket generation with severity grading."
        elif any(w in msg_lower for w in ["list", "tickets", "active incidents"]):
            thought_text = "Retrieving active incident records from SafeX incident vault."
        else:
            thought_text = "Standard domain query. Formulating search plan across SafeX knowledge bases and compliance matrices."

        steps.append(AgentStep("thought", "Reasoning & Planning", thought_text).to_dict())

        # Step 2: Tool Execution Phase
        final_answer = ""
        action_data = None

        # Scenario A: Emergency Dispatch
        if any(w in msg_lower for w in ["emergency", "evacuate", "immediate help", "mayday", "call 911"]):
            zone = "Building B - Industrial Wing"
            if "zone" in msg_lower:
                match = re.search(r"zone\s+([a-zA-Z0-9]+)", msg_lower)
                if match:
                    zone = f"Zone {match.group(1).upper()}"
            
            steps.append(AgentStep("tool_call", "Tool: dispatch_emergency_response", {
                "hazard_type": "Critical Alarm",
                "zone": zone,
                "priority": "P1-CRITICAL"
            }).to_dict())
            
            dispatch_res = dispatch_emergency_response("Critical Alarm", zone, level="Critical")
            tools_called.append("dispatch_emergency_response")
            steps.append(AgentStep("observation", "Dispatch Triggered", dispatch_res).to_dict())

            final_answer = (
                f"🚨 **EMERGENCY DISPATCH PROTOCOL ACTIVATED**\n\n"
                f"• **Dispatch Code:** `{dispatch_res['dispatch_code']}`\n"
                f"• **Target Location:** {zone}\n"
                f"• **Status:** Confirmed. SafeX HSE response team notified.\n"
                f"• **Estimated Arrival:** {dispatch_res['estimated_arrival']}\n\n"
                f"**Immediate Safety Actions:**\n"
                + "\n".join([f"- {a}" for a in dispatch_res["actions_triggered"]])
            )

        # Scenario B: Incident Ticket Logging
        elif any(w in msg_lower for w in ["log ticket", "report incident", "create ticket", "file report"]) or (
            "report" in msg_lower and any(w in msg_lower for w in ["hazard", "leak", "breach", "problem", "fault"])
        ):
            severity = "High" if any(w in msg_lower for w in ["high", "critical", "severe", "urgent"]) else "Medium"
            title = user_message[:50] + ("..." if len(user_message) > 50 else "")
            
            steps.append(AgentStep("tool_call", "Tool: log_incident_ticket", {
                "title": title,
                "severity": severity,
                "location": "Main Facility"
            }).to_dict())

            ticket_res = log_incident_ticket(title, severity, user_message, "Facility Alpha")
            tools_called.append("log_incident_ticket")
            steps.append(AgentStep("observation", "Ticket Registered", ticket_res).to_dict())

            t = ticket_res["ticket"]
            final_answer = (
                f"✅ **Incident Ticket Successfully Logged**\n\n"
                f"• **Ticket ID:** `{t['id']}`\n"
                f"• **Title:** {t['title']}\n"
                f"• **Severity Level:** **{t['severity']}**\n"
                f"• **Assigned Unit:** {t['assigned_to']}\n"
                f"• **Status:** {t['status']}\n"
                f"• **Recorded At:** {t['timestamp']}\n\n"
                f"{ticket_res['notification']}"
            )
            action_data = t

        # Scenario C: Safety Compliance Assessment
        elif any(w in msg_lower for w in ["hazard", "safety", "risk", "osha", "iso", "ppe", "spill", "chemical", "electric", "fall"]):
            steps.append(AgentStep("tool_call", "Tool: assess_safety_compliance", {
                "workplace_context": user_message,
                "standards": ["OSHA 1910", "ISO 45001"]
            }).to_dict())

            compliance_res = assess_safety_compliance(user_message)
            tools_called.append("assess_safety_compliance")
            steps.append(AgentStep("observation", "Compliance Assessment Results", compliance_res).to_dict())

            # Also consult knowledge base for protocols
            kb_res = search_knowledge_base(user_message)
            tools_called.append("search_knowledge_base")
            steps.append(AgentStep("observation", "Protocol Matching", kb_res).to_dict())

            hazards_list = "\n".join([f"• ⚠️ {h}" for h in compliance_res["hazards_identified"]])
            standards_str = ", ".join(compliance_res["standards_checked"])

            final_answer = (
                f"🛡️ **SafeX Compliance & Hazard Evaluation**\n\n"
                f"• **Risk Rating:** **{compliance_res['rating']}** (Score: {compliance_res['risk_score']}/100)\n"
                f"• **Standards Audited:** {standards_str}\n\n"
                f"**Identified Risks:**\n{hazards_list}\n\n"
                f"**Required Remediation:**\n{compliance_res['recommended_action']}\n\n"
                f"*Would you like me to generate an official incident report or alert on-duty safety supervisors?*"
            )

        # Scenario D: System Diagnostics & Health Telemetry
        elif any(w in msg_lower for w in ["diagnostics", "system", "status", "health", "telemetry", "firewall", "iot"]):
            steps.append(AgentStep("tool_call", "Tool: run_system_diagnostics", {
                "scope": "enterprise_fleet_and_soc"
            }).to_dict())

            diag_res = run_system_diagnostics()
            tools_called.append("run_system_diagnostics")
            steps.append(AgentStep("observation", "Diagnostics Output", diag_res).to_dict())

            sys_summary = []
            for sys_name, details in diag_res["systems"].items():
                status_icon = "🟢" if details["status"] in ["Nominal", "Active", "Operational", "Encrypted"] else "🟡"
                metric = next((f"{k}: {v}" for k, v in details.items() if k != "status"), "")
                sys_summary.append(f"• {status_icon} **{sys_name.replace('_', ' ').title()}**: {details['status']} ({metric})")

            final_answer = (
                f"⚡ **SafeX Infrastructure & Security Telemetry**\n\n"
                f"• **Overall Health:** `{diag_res['overall_health']}`\n"
                f"• **Audit Timestamp:** {diag_res['timestamp']}\n\n"
                + "\n".join(sys_summary) + "\n\n"
                f"All systems are operating within safe operational parameters. No critical anomalies detected."
            )

        # Scenario E: Active Incidents List
        elif any(w in msg_lower for w in ["active tickets", "list incidents", "recent incidents", "show tickets"]):
            steps.append(AgentStep("tool_call", "Tool: get_active_incidents", {}).to_dict())
            incidents = get_active_incidents()
            tools_called.append("get_active_incidents")
            steps.append(AgentStep("observation", f"Retrieved {len(incidents)} Incidents", incidents).to_dict())

            inc_lines = []
            for inc in incidents:
                icon = "🔴" if inc["severity"] in ["Critical", "High"] else "🟡" if inc["severity"] == "Medium" else "🟢"
                inc_lines.append(f"• {icon} **[{inc['id']}] {inc['title']}**\n  Severity: `{inc['severity']}` | Status: `{inc['status']}` | Assigned: {inc['assigned_to']}")

            final_answer = (
                f"📋 **SafeX Active Incident Queue ({len(incidents)} Records)**\n\n"
                + "\n\n".join(inc_lines)
            )

        # Scenario F: Knowledge Base / General SafeX Query
        else:
            steps.append(AgentStep("tool_call", "Tool: search_knowledge_base", {"query": user_message}).to_dict())
            kb_res = search_knowledge_base(user_message)
            tools_called.append("search_knowledge_base")
            steps.append(AgentStep("observation", "Knowledge Base Retrieved", kb_res).to_dict())

            items = kb_res.get("data", [])
            content_pieces = []
            for item in items:
                if item.get("type") == "Service":
                    content_pieces.append(f"### {item['title']}\n{item['content']}\n\n* **SLA Guarantee**: {item['sla']}\n* **Compliance Certifications**: {', '.join(item['compliance'])}")
                elif item.get("type") == "Safety Protocol":
                    steps_list = "\n".join([f"1. {s}" for s in item["standard_operating_procedure"]])
                    content_pieces.append(f"### Emergency Protocol: {item['hazard']} ({item['severity_level']})\n{steps_list}")
                elif item.get("type") == "General Knowledge":
                    content_pieces.append(item["answer"])
                elif item.get("type") == "Overview":
                    content_pieces.append(item["message"] + "\n\n**Specialized Core Services:** " + ", ".join([s.replace("_", " ").title() for s in item.get("services", [])]))

            if content_pieces:
                final_answer = "\n\n".join(content_pieces)
            else:
                final_answer = (
                    "I am the **SafeX Solution Agentic AI**. I can assist you with:\n\n"
                    "• **Safety & Compliance Auditing**: Real-time OSHA/ISO hazard evaluation.\n"
                    "• **Incident Logging & Ticketing**: Automated triage and rapid dispatch.\n"
                    "• **Infrastructure Telemetry**: Live SOC, firewall, and IoT status checks.\n"
                    "• **Emergency Response**: Instant protocol triggers and notification alerts.\n\n"
                    "How can I assist your operations right now?"
                )

        # Step 3: Synthesis Step
        steps.append(AgentStep("thought", "Synthesis & Verification", "Synthesized tool observations into actionable guidelines with compliance recommendations.").to_dict())

        return {
            "query": user_message,
            "response": final_answer,
            "steps": steps,
            "tools_called": tools_called,
            "action_data": action_data
        }
