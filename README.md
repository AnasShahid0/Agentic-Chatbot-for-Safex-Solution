# 🛡️ SafeX Solutions — Autonomous Agentic AI Chatbot & Incident Management Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Agentic AI](https://img.shields.io/badge/AI-Autonomous_Tool_Calling-orange.svg)](#-agentic-tool-ecosystem)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#-automated-testing)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> An enterprise-grade **Autonomous Agentic AI Platform** developed for **SafeX Solutions** industrial & facilities safety management. Equipped with dynamic intent recognition, multi-tool reasoning (ReAct), real-time telemetry inspection, automated emergency dispatch, safety compliance auditing, and an interactive glassmorphic web dashboard.

---

## 📌 Executive Summary for Evaluators & Recruiters

In industrial plants, construction hubs, and enterprise facilities, human operators face split-second safety emergencies. Traditional chatbot assistants are passive and limited to static text queries.

**SafeX Agentic Chatbot** is an **active autonomous agent**. When an operator types *"Ammonia leak detected in Sector 4!"*, the agent does not just give general advice — it:
1. **Parses the hazard level and location** using domain heuristics and LLM reasoning.
2. **Executes `dispatch_emergency_team`** to simulate alarms and calculate response unit ETAs.
3. **Executes `create_incident_ticket`** to register an auditable ticket (`INC-2026-XXXX`).
4. **Queries `safety_compliance_audit`** for OSHA/ISO chemical safety evacuation protocols.
5. **Streams Chain-of-Thought logs** directly to the operator's control center screen in real-time.

---

## 📸 Platform Interface & Screenshots

| Control Dashboard & Live Telemetry | Autonomous Tool Execution & Thought Drawer |
|:---:|:---:|
| ![Dashboard Overview](assets/dashboard-overview.png) | ![Tool Execution](assets/agentic-tool-execution.png) |
| *Glassmorphic Chat UI with Suggestion Pills & Telemetry Cards* | *Real-time Chain-of-Thought logs & Deterministic Tool Badges* |

*(Screenshots can be captured and placed in the [`assets/`](assets/) folder as outlined in [assets/README.md](assets/README.md)).*

---

## 🏗️ Architecture & ReAct Agent Loop

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

## ⚡ Core Capabilities

- 🤖 **Autonomous Multi-Tool Calling**: Executes deterministic system functions (health monitoring, incident filing, team dispatch) with parameter validation.
- 📋 **Safety Compliance Engine**: Instant OSHA 1910 and ISO 45001 safety audits for PPE, fire suppression, chemical storage, and electrical safety.
- 📊 **Real-Time Telemetry Dashboard**: Live updates on active environmental sensors, CPU load, and active incident tracking.
- 🔍 **Explainable Chain-of-Thought**: Visual expandable drawer revealing the agent's internal reasoning steps before taking action.
- 🚀 **Zero-Config Resilient Design**: Runs locally out-of-the-box with intelligent mock fallbacks even without external paid API keys.

---

## 🛠️ Project Structure

```
├── main.py                  # FastAPI server, REST API endpoints, static file mounting
├── agent/
│   ├── core.py              # SafeXAgent reasoning engine, ReAct loop, fallback logic
│   ├── tools.py             # Deterministic tool registry (health, compliance, dispatch)
│   └── knowledge.py         # Domain knowledge base (OSHA regulations, hazard protocols)
├── static/
│   ├── index.html           # Semantic HTML5 control center layout
│   ├── style.css            # Dark glassmorphism, responsive animations, CSS tokens
│   └── app.js               # Client controller, async polling, thought process renderer
├── assets/
│   └── README.md            # Guidelines for screenshot captures and visual assets
├── test_agent.py            # Automated test suite (tools, RAG, agent decision tests)
├── AGENTS.md                # System state, file creation rationale, and decision journal
├── IMPLEMENTATION_GUIDE.md  # Detailed technical implementation specification
├── requirements.txt         # Project Python dependencies
└── .agents/
    ├── rules/               # Agent workflow governance rules
    └── workflows/           # Knowledge graph and execution workflows
```

---

## 🚀 Quick Start & Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/AnasShahid0/Agentic-Chatbot-for-Safex-Solution.git
cd Agentic-Chatbot-for-Safex-Solution
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
python -m pytest test_agent.py -v
```

### 4. Launch Application Server
```bash
python main.py
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 🧪 Automated Testing

Run the full test suite with:
```bash
pytest test_agent.py -v
```

All tests assert:
1. `test_knowledge_search`: Accurate retrieval of safety protocols.
2. `test_tools_execution`: Proper argument handling and schema generation for all 4 tools.
3. `test_agent_reasoning`: Correct ReAct decision path when handling emergency requests.
4. `test_api_endpoints`: HTTP status code verification for `/api/status`, `/api/tools`, and `/api/chat`.

---

## 📖 Additional Documentation

- **[AGENTS.md](AGENTS.md)**: Architectural state, decision journal, and rationale for every file created.
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)**: Full API contracts, JSON schemas, and technical guide.
- **[assets/README.md](assets/README.md)**: Staging guide for UI captures and demo media.

---

*Developed as part of 100 Days of Code | SafeX Solutions Incident Management & Autonomous Systems.*
