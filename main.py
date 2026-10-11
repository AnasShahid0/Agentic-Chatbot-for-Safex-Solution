"""
SafeX Solution Agentic Chatbot - FastAPI Server
Exposes chat reasoning endpoints, live telemetry, and serves the high-fidelity UI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from typing import Optional

from agent.core import SafeXAgent
from agent.tools import (
    run_system_diagnostics,
    get_active_incidents,
    log_incident_ticket,
    assess_safety_compliance
)

app = FastAPI(
    title="SafeX Solution Agentic Chatbot",
    description="Enterprise Autonomous Safety & Security Agentic Chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate singleton agent
agent = SafeXAgent()

class ChatRequest(BaseModel):
    message: str

class IncidentCreateRequest(BaseModel):
    title: str
    severity: str
    description: str
    location: Optional[str] = "Facility Alpha"

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    result = agent.run(req.message)
    return result

@app.get("/api/status")
async def status_endpoint():
    return run_system_diagnostics()

@app.get("/api/incidents")
async def incidents_endpoint():
    return get_active_incidents()

@app.post("/api/incidents")
async def create_incident(req: IncidentCreateRequest):
    return log_incident_ticket(req.title, req.severity, req.description, req.location or "Facility Alpha")

@app.get("/api/tools")
async def get_tools():
    return {
        "tools": [
            {
                "name": "assess_safety_compliance",
                "description": "Evaluates hazards against OSHA 1910 and ISO 45001 standards with dynamic risk scores."
            },
            {
                "name": "log_incident_ticket",
                "description": "Generates formal P1-P4 tracking tickets and dispatches triage teams."
            },
            {
                "name": "run_system_diagnostics",
                "description": "Queries real-time telemetry from firewalls, SOC nodes, and industrial IoT gateways."
            },
            {
                "name": "dispatch_emergency_response",
                "description": "Initiates emergency broadcast, sirens, and warden routing."
            },
            {
                "name": "search_knowledge_base",
                "description": "Searches SafeX Solutions technical docs, protocols, and standard operating procedures."
            }
        ]
    }

# Mount static folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "SafeX Solution Agentic Chatbot API is operational."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
