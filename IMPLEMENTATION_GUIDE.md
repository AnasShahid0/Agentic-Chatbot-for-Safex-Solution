# Implementation Guide — SafeX Solutions Agentic Chatbot

This document provides a comprehensive technical walkthrough of the architecture, component interactions, API design, and extension patterns for the **SafeX Solutions Agentic Chatbot & Incident Management Platform**.

---

## 1. System Architecture

The application adopts an asynchronous client-server architecture with an embedded **Autonomous Tool Calling Loop**:

```
+--------------------------------------------------------------+
|                    Browser Web Client                        |
|   (HTML5 / Glassmorphic CSS / Vanilla JS app.js)             |
+--------------------------------------------------------------+
         |                                           ^
         | POST /api/chat                            | SSE / JSON
         | GET  /api/status, /api/incidents          | Response
         v                                           |
+--------------------------------------------------------------+
|                 FastAPI Application Server                   |
|                   (main.py on Uvicorn)                       |
+--------------------------------------------------------------+
         |                                           |
         v                                           v
+------------------------+             +-----------------------+
|   SafeXAgent Core      |             | In-Memory Incident DB |
|   (agent/core.py)      |             | & Telemetry Store     |
+------------------------+             +-----------------------+
         |              |
         v              v
+---------------+  +-----------------------------+
| Domain RAG    |  | Deterministic Tool Engine   |
| Knowledge Base|  | (agent/tools.py)            |
| (knowledge.py)|  | - check_system_health       |
+---------------+  | - safety_compliance_audit   |
                   | - create_incident_ticket    |
                   | - dispatch_emergency_team   |
                   +-----------------------------+
```

---

## 2. API Endpoint Specification

### `POST /api/chat`
Handles user conversation, triggers agent reasoning, executes required tools, and returns final responses with thought chains.

- **Request Body**:
```json
{
  "message": "We have an ammonia gas leak in Sector 4! Dispatch emergency team immediately.",
  "session_id": "session_abc123"
}
```

- **Response Structure**:
```json
{
  "reply": "EMERGENCY PROTOCOL ACTIVATED: Hazardous Material Response Team HAZ-Sector 4 has been dispatched...",
  "tools_executed": [
    {
      "tool": "dispatch_emergency_team",
      "args": { "location": "Sector 4", "hazard_type": "chemical", "priority": "critical" },
      "result": { "status": "dispatched", "dispatch_id": "DISP-8921", "eta_minutes": 4 }
    },
    {
      "tool": "create_incident_ticket",
      "args": { "title": "Ammonia Gas Leak", "severity": "critical", "location": "Sector 4" },
      "result": { "ticket_id": "INC-2026-9142", "status": "open" }
    }
  ],
  "thought_process": [
    "Detected high-severity incident: ammonia gas leak in Sector 4.",
    "Formulating action plan: (1) Dispatch Hazmat team, (2) File critical incident ticket.",
    "Executing dispatch_emergency_team...",
    "Executing create_incident_ticket...",
    "Synthesizing emergency evacuation directives for operator."
  ]
}
```

---

### `GET /api/status`
Returns real-time server and environmental monitoring telemetry.
- **Response**:
```json
{
  "status": "online",
  "active_sensors": 48,
  "system_load": "24%",
  "active_incidents": 2,
  "telemetry": {
    "server_uptime": "99.98%",
    "agent_version": "2.4.0",
    "hazard_level": "normal"
  }
}
```

---

### `GET /api/incidents`
Returns the array of currently active and resolved safety incidents tracked during the session.

---

### `GET /api/tools`
Returns the JSON Schema definitions of all registered tools available to the agent.

---

## 3. Tool Execution Registry (`agent/tools.py`)

Each tool is exposed as a typed function with clear parameter definitions:

1. **`check_system_health(subsystem: str)`**:
   - Queries telemetry for `ventilation`, `fire_suppression`, `gas_sensors`, `power_grid`, or `all`.
   - Returns operational status, load, temperature, and alerts.

2. **`safety_compliance_audit(category: str)`**:
   - Evaluates protocols against OSHA 1910 and ISO 45001 safety frameworks.
   - Flags missing PPE, overdue inspections, or ventilation shortcomings.

3. **`create_incident_ticket(title: str, severity: str, location: str, description: str)`**:
   - Logs an incident into the active registry.
   - Generates unique ticket numbers (`INC-2026-XXXX`) with timestamp and priority routing.

4. **`dispatch_emergency_team(location: str, hazard_type: str, priority: str)`**:
   - Simulates immediate alarm sounding and team routing.
   - Calculates estimated time of arrival (ETA) and team unit designations.

---

## 4. Frontend Design System (`static/`)

The web UI is designed according to **Glassmorphism & Rich Aesthetics** guidelines:
- **Color Palette**: Dark slate background (`#0b0f19`, `#111827`) with neon cyan accents (`#06b6d4`), amber warnings (`#f59e0b`), and crimson critical badges (`#ef4444`).
- **Dynamic Feedback**: Real-time pulsing dots indicate agent status; tool badges render inline inside agent message cards.
- **Thought Drawer**: Expandable `<details>` drawer lets technical evaluators inspect the agent's step-by-step reasoning chain for complete explainability.

---

## 5. Local Setup & Verification

```bash
# 1. Clone repository
git clone https://github.com/AnasShahid0/Agentic-Chatbot-for-Safex-Solution.git
cd Agentic-Chatbot-for-Safex-Solution

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run automated test suite
python -m pytest test_agent.py -v

# 4. Start local development server
python main.py
```
Open **`http://127.0.0.1:8000`** in your browser.
