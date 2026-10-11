# AGENTS.md — System State, Architectural Log & Decision Journal

> **Project**: SafeX Solutions Autonomous Agentic Chatbot & Incident Management Platform  
> **Repository**: [https://github.com/AnasShahid0/Agentic-Chatbot-for-Safex-Solution](https://github.com/AnasShahid0/Agentic-Chatbot-for-Safex-Solution)  
> **Last Updated**: 2026-10-11  
> **Status**: Production-Ready Architecture / Fully Operational  

---

## 1. System Vision & Purpose

SafeX Solutions is an industrial and technical infrastructure safety services provider. Traditional support bots only answer static FAQs and fail when urgent site incidents, compliance violations, or hazardous telemetry spikes occur.

This platform bridges that gap by deploying a true **Autonomous Agentic AI System** that:
1. **Understands Intent**: Parses natural language requests for guidance, incident reports, and system diagnostics.
2. **Plans & Reason**: Uses ReAct (Reason + Act) loop to select the appropriate specialized tools.
3. **Executes Real Actions**: Dispatches emergency teams, logs compliance audits, inspects environmental sensors, and registers persistent incident tickets.
4. **Maintains Traceability**: Exposes full Chain-of-Thought logs and telemetry to operators via an interactive glassmorphic dashboard.

---

## 2. File Manifest & Creation Rationale

Every file in this codebase exists for a clear, documented architectural reason:

| File Path | Creation Rationale & Core Purpose |
|---|---|
| **`main.py`** | **FastAPI Server Entry Point**: Houses REST API routes (`/api/chat`, `/api/status`, `/api/incidents`, `/api/tools`), mounts static frontend assets, and handles CORS. Configured with Uvicorn for asynchronous non-blocking I/O. |
| **`agent/core.py`** | **Agentic Brain & Orchestrator**: Implements `SafeXAgent` class with conversation history memory, dynamic prompt synthesis, tool calling execution loop, and intelligent fallback for zero-dependency local runs. |
| **`agent/tools.py`** | **Deterministic Tool Execution Registry**: Houses executable tools: `run_system_diagnostics` (telemetry/load), `assess_safety_compliance` (OSHA/ISO regulations), `log_incident_ticket` (ticket generation), and `dispatch_emergency_response` (emergency response). |
| **`agent/knowledge.py`** | **Domain Knowledge Base**: In-memory searchable knowledge base containing SafeX services, emergency protocols, hazardous chemical handling, fire safety steps, and PPE requirements. |
| **`static/index.html`** | **Frontend Application Structure**: Modern semantic HTML5 markup featuring dual-panel layout: chat interface with prompt suggestion pills on the left, live telemetry cards and incident logs on the right, plus an expandable Chain-of-Thought execution drawer. |
| **`static/style.css`** | **Design System & Styling**: Custom responsive CSS implementing dark-mode glassmorphism (`backdrop-filter: blur`), CSS variables, smooth glow animations, status badge indicators, and mobile break points. |
| **`static/app.js`** | **Client-side Application Controller**: Handles asynchronous fetch requests to `/api/chat`, dynamic rendering of agent messages with tool badges, periodic polling of `/api/status` and `/api/incidents`, and thought-process drawer animations. |
| **`test_agent.py`** | **Automated Test Suite**: Pytest/unittest verification asserting knowledge search accuracy, tool dispatch mechanics, emergency protocol handling, and HTTP status codes. |
| **`requirements.txt`** | **Dependency Manifest**: Locks lightweight, robust backend dependencies (`fastapi`, `uvicorn`, `pydantic`, `python-multipart`). |
| **`.gitignore`** | **Repository Cleanliness**: Prevents Python artifacts (`__pycache__`, `.venv`), IDE configurations, and local `.agents/skills/` mirrors from polluting the git tree. |
| **`assets/README.md`** | **Visual Assets Guide**: Instructs developers and users on capturing, naming, and staging UI screenshots (`dashboard-overview.png`, `agentic-tool-execution.png`) for portfolio presentation. |
| **`.agents/rules/agent_workflow.md`** | **Permanent Agent Rules**: Enforces continuous update of `AGENTS.md`, individual atomic file commits, descriptive GitHub metadata, and user screenshot workflows. |
| **`.agents/rules/graphify.md`** | **Knowledge Graph Navigation Rules**: Guides agents to query the graphify knowledge graph before scanning raw code. |
| **`.agents/workflows/graphify.md`** | **Knowledge Graph Workflow**: Defines step-by-step procedures to map codebase architectures into navigable AST subgraphs. |
| **`IMPLEMENTATION_GUIDE.md`** | **Technical Reference**: Deep-dive architecture and component integration manual for engineers and hiring evaluators. |
| **`README.md`** | **Public Showcase & Documentation**: Visual project overview with feature badges, architecture diagram, API references, and quickstart instructions. |

---

## 3. Project Conventions & Architecture Standards

### Coding Conventions & Style
- **Python Backend**: PEP 8 compliance, explicit type hinting (`typing`), Pydantic V2 models for all request/response boundaries.
- **Asynchronous Execution**: Async handlers for REST routes; non-blocking I/O for external tool integrations.
- **Frontend**: Vanilla JavaScript (ES6+), semantic HTML5, zero framework overhead (no React/Vue dependency needed for the control dashboard).
- **Styling**: Vanilla CSS with centralized CSS variables, CSS grid/flexbox layouts, responsive mobile breakpoints (`@media (max-width: 900px)`).
- **Error Handling**: Standard HTTP status codes (400 for malformed input, 404 for missing resources, 500 with sanitized error payloads).

### Testing Protocol & Verification Commands
- **Unit & Smoke Tests**:
  ```powershell
  python test_agent.py
  ```
- **Pytest Suite**:
  ```powershell
  python -m pytest test_agent.py -v
  ```
- **Local Server Launch**:
  ```powershell
  python main.py
  # Serves at: http://127.0.0.1:8000
  ```

---

## 4. Security & Compliance Requirements

1. **Zero Secret Leaks**:
   - Never commit `.env`, API tokens, private keys, or passwords.
   - Always provide `.env.example` with mock/sanitized placeholders.
2. **Input Sanitization & Injection Defense**:
   - Sanitize all inbound chat prompts to mitigate prompt injection and XSS in client-rendered messages.
   - Validate string lengths and enforce Pydantic type constraints.
3. **CORS & Network Security**:
   - Restrict CORS origins in production deployment (avoid blanket `allow_origins=["*"]` outside local development).
4. **Audit Traceability**:
   - Every emergency dispatch and incident ticket creation must produce an immutable audit log entry with timestamp and unique ID (`SFX-XXXXXX`).

---

## 5. Strict Policy: 100% Individual Atomic Commits (Always)

- **Absolute Prohibition on Monolithic / Batch Commits**: `git add .` or grouping multiple edited files into a single commit is strictly disallowed.
- **Single-File Commit Protocol**: Every single file created or modified MUST be committed individually in isolation:
  ```bash
  git add <exact-file-path>
  git commit -m "<type>(<scope>): <explicit explanation of change>"
  git push origin main
  ```
- **Traceability**: Each commit log entry must directly describe the change made to that specific file and the technical rationale behind it.

---

## 6. Installed Global & Workspace Skills

All 18 core competencies and 225 sub-skills are installed and active:
- **Architecture**: `graphify` (AST Knowledge Graph navigation)
- **Agent Frameworks**: `agent-skills`, `composio` (Tool calling & SaaS integrations)
- **Infrastructure**: Official Google Cloud skills (`gke-*`, `cloud-run-*`, `bigquery-*`, `google-cloud-waf-*`)
- **APIs & Testing**: `context7`, `playwright-agent`, `playwright-cli` (E2E browser tests)
- **Web Extraction**: `firecrawl` suite (Live web scraping & document ingestion)
- **Deployment**: `deploy-to-vercel`, `vercel-composition-patterns`
- **Observability**: `sentry-fix-issues`, `datadog-skills` (Error tracking & APM)
- **Databases**: `neon-branching` (PostgreSQL copy-on-write branching)
- **Language Patterns**: `fastapi-pro`, `react-modernization`
- **Security & QA**: `security-auditor-pro` (Vulnerability auditing & OWASP)
- **Demo & Video**: `video-shotcraft`, `ultrademo`, `motion-canvas-agent`, `screen-to-code-video`

---

## 7. Concise Implementation Plan

### Phase 1: Environment & Configuration Foundation
- **Objective**: Establish structured environment configuration and settings management.
- **Tasks**:
  1. Add `.env.example` documenting optional LLM keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ENVIRONMENT`, `PORT`).
  2. Implement configuration loader with fallback defaults.
- **Dependencies**: `python-dotenv` (optional), standard library `os`.
- **Acceptance Criteria**: System starts cleanly with zero environment variables and optionally loads `.env` when present.

### Phase 2: Hybrid LLM Adapter Integration
- **Objective**: Allow seamless toggling between deterministic local heuristics and external LLM APIs (Gemini / OpenAI).
- **Tasks**:
  1. Create `agent/llm_adapter.py` providing an abstract model interface.
  2. Support dynamic tool schema passing and structured output extraction.
  3. Retain heuristic fallback as primary safety net for offline/free runs.
- **Dependencies**: `httpx` for async API requests.
- **Acceptance Criteria**: If API key is valid, agent leverages external LLM; if absent or invalid, agent falls back gracefully to deterministic tool execution without raising 500 errors.

### Phase 3: Enhanced RAG & Document Ingestion
- **Objective**: Expand knowledge retrieval from static dictionary to searchable vector/fuzzy document store.
- **Tasks**:
  1. Extend `agent/knowledge.py` with expanded OSHA 1910, ISO 45001, and SafeX technical protocols.
  2. Add keyword/BM25 scoring or local embedding similarity search.
- **Dependencies**: In-memory lightweight index.
- **Acceptance Criteria**: Search queries match relevant SOPs with relevance scoring and confidence metrics.

### Phase 4: Production Hardening & E2E Testing
- **Objective**: Verify full UI flows and ensure production security posture.
- **Tasks**:
  1. Add Playwright E2E test script testing chat message flow, tool chip clicks, and telemetry modal.
  2. Implement request rate-limiting on `/api/chat`.
- **Dependencies**: `playwright`.
- **Acceptance Criteria**: All automated E2E tests pass headlessly; API rejects excessive burst requests.

---

## 8. Active Daemon & Execution State
- **Backend Daemon**: FastAPI (`http://127.0.0.1:8000`) running under Python 3.12.
- **Working Tree**: Clean (`main` branch synced with `origin/main`).
- **Next Immediate Task**: Task 1 of Implementation Plan (Create `.env.example` template).
