"""
Unit / Smoke Test for SafeX Agent Core Logic
"""

from agent.core import SafeXAgent
from agent.tools import get_active_incidents, run_system_diagnostics

def test_agent_reasoning():
    agent = SafeXAgent()

    print("[1] Testing Knowledge Query...")
    res1 = agent.run("What cybersecurity services does SafeX provide?")
    assert len(res1["steps"]) > 0
    assert "Cybersecurity" in res1["response"]
    print("  [PASS] Knowledge Query passed.")

    print("[2] Testing Safety Hazard Evaluation...")
    res2 = agent.run("There is a chemical leak and toxic fumes in the production bay")
    assert "assess_safety_compliance" in res2["tools_called"]
    assert "Risk Rating" in res2["response"]
    print("  [PASS] Safety Hazard Evaluation passed.")

    print("[3] Testing Incident Ticket Logging...")
    res3 = agent.run("Report incident: High severity server breach attempt detected")
    assert "log_incident_ticket" in res3["tools_called"]
    assert "SFX-" in res3["response"]
    print("  [PASS] Incident Logging passed.")

    print("[4] Testing Emergency Protocol...")
    res4 = agent.run("Emergency: Evacuate Facility Zone B immediately")
    assert "dispatch_emergency_response" in res4["tools_called"]
    assert "EMERGENCY DISPATCH PROTOCOL ACTIVATED" in res4["response"]
    print("  [PASS] Emergency Protocol passed.")

    print("\nALL AGENT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_agent_reasoning()
