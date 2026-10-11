"""
SafeX Solutions - Knowledge Base & Domain Intelligence
Contains curated company information, compliance protocols, cybersecurity standards, and incident response matrices.
"""

SAFEX_SERVICES = {
    "cybersecurity": {
        "title": "Cybersecurity & Managed SOC",
        "description": "24/7 Security Operations Center monitoring, vulnerability scanning, threat mitigation, penetration testing, and Zero-Trust architecture.",
        "sla": "99.99% uptime, <15 minute response for critical incidents",
        "compliance": ["ISO 27001", "SOC 2 Type II", "GDPR", "HIPAA"]
    },
    "workplace_safety": {
        "title": "Workplace Safety & HSE Management",
        "description": "AI-driven hazard analysis, digital safety permit auditing, OSHA compliance tracking, PPE adherence checks, and risk matrices.",
        "sla": "Immediate alert generation for Level 1/2 hazards",
        "compliance": ["OSHA 1910", "ISO 45001", "NEBOSH Guidelines"]
    },
    "cloud_infrastructure": {
        "title": "Cloud Solutions & Infrastructure",
        "description": "Multi-cloud architecture (AWS, Azure, GCP), automated backup redundancy, disaster recovery pipelines, and Kubernetes orchestration.",
        "sla": "RPO < 5 minutes, RTO < 15 minutes",
        "compliance": ["Cloud Security Alliance (CSA) STAR", "FedRAMP"]
    },
    "fleet_iot": {
        "title": "Smart Fleet & Industrial IoT Safety",
        "description": "Real-time telematics, auto-eject power solutions, temperature-controlled transport monitoring, and predictive failure analysis.",
        "sla": "Sub-second sensor streaming and telemetry ingestion",
        "compliance": ["DOT / FMCSA", "ISO 9001"]
    }
}

SAFETY_PROTOCOLS = {
    "chemical_spill": {
        "level": "Critical",
        "steps": [
            "Evacuate affected area immediately and seal air ventilation.",
            "Alert Emergency Response Coordinator and sound alarm code Amber.",
            "Deploy Level-A Hazmat team with neutralizers if safe.",
            "File formal Incident Report within 60 minutes."
        ]
    },
    "cyber_breach": {
        "level": "Urgent",
        "steps": [
            "Isolate compromised nodes and disable external network gateways.",
            "Preserve forensic disk snapshots and memory dumps.",
            "Notify SafeX CISO and trigger incident classification protocol.",
            "Begin failover to immutable air-gapped backups."
        ]
    },
    "equipment_failure": {
        "level": "Moderate",
        "steps": [
            "Initiate Lockout/Tagout (LOTO) procedure.",
            "Notify field maintenance engineer via automated dispatch.",
            "Run automated diagnostics on auxiliary components.",
            "Update equipment health log."
        ]
    },
    "fire_hazard": {
        "level": "Critical",
        "steps": [
            "Trigger automated suppression systems and audible facility alarm.",
            "Evacuate via primary designated assembly zones.",
            "Contact municipal emergency services (911).",
            "Perform digital head-count through RFID badge scanners."
        ]
    }
}

FAQ_DATA = [
    {
        "keywords": ["contact", "support", "helpdesk", "phone", "email"],
        "answer": "SafeX Solutions Support Desk operates 24/7/365. Reach our NOC/SOC at support@safexsolutions.io or call toll-free +1 (800) 555-SAFEX. For emergency escalations, dial extension #9."
    },
    {
        "keywords": ["compliance", "audit", "osha", "iso", "standards"],
        "answer": "SafeX Solution platforms adhere to ISO 27001 (Information Security), ISO 45001 (Occupational Health & Safety), SOC 2 Type II, and OSHA regulations with automated audit logging."
    },
    {
        "keywords": ["incident", "report", "ticket", "emergency"],
        "answer": "You can report any incident directly through this chatbot. Provide the title, severity level (Low, Medium, High, Critical), and description, and our agent will dispatch the appropriate response team immediately."
    },
    {
        "keywords": ["pricing", "cost", "quote", "tier"],
        "answer": "SafeX Solutions offers Enterprise, Professional, and Growth tiers. Custom enterprise deployments include dedicated SOC engineers and tailored SLA guarantees. Request a quote through sales@safexsolutions.io."
    }
]
