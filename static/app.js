/**
 * SafeX Solution Agentic Chatbot - Client Application
 * Handles reactive UI, agent reasoning step disclosure, telemetry updates, and chat stream.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const chatMessages = document.getElementById("chat-messages");
  const chatViewport = document.getElementById("chat-viewport");
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const welcomeHero = document.getElementById("welcome-hero");
  const clearChatBtn = document.getElementById("clear-chat-btn");
  const quickDiagnosticsBtn = document.getElementById("quick-diagnostics-btn");
  const quickEmergencyBtn = document.getElementById("quick-emergency-btn");
  const refreshTelemetryBtn = document.getElementById("refresh-telemetry-btn");
  const viewAllIncidentsBtn = document.getElementById("view-all-incidents-btn");
  const incidentModal = document.getElementById("incident-modal");
  const modalClose = document.getElementById("modal-close");
  const modalBody = document.getElementById("modal-body");
  const mobileToggle = document.getElementById("mobile-toggle");
  const sidebar = document.getElementById("sidebar");
  const incidentListSidebar = document.getElementById("incident-list-sidebar");

  // Metrics elements
  const metricHealth = document.getElementById("metric-health");
  const metricThreats = document.getElementById("metric-threats");
  const metricSoc = document.getElementById("metric-soc");
  const metricTickets = document.getElementById("metric-tickets");

  // State
  let isProcessing = false;

  // Initialize
  fetchTelemetry();
  fetchIncidents();

  // Auto-resize textarea
  userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 160) + "px";
  });

  // Handle Enter (without Shift)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event("submit"));
    }
  });

  // Mobile sidebar toggle
  if (mobileToggle) {
    mobileToggle.addEventListener("click", () => {
      sidebar.classList.toggle("mobile-open");
    });
  }

  // Clear chat
  clearChatBtn.addEventListener("click", () => {
    chatMessages.innerHTML = "";
    if (welcomeHero) {
      chatMessages.appendChild(welcomeHero);
      welcomeHero.style.display = "flex";
    }
  });

  // Quick prompt chips
  document.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (chip) {
      const prompt = chip.getAttribute("data-prompt");
      if (prompt) {
        submitQuery(prompt);
      }
    }
  });

  // Tool items click in sidebar
  document.querySelectorAll(".tool-item").forEach(item => {
    item.addEventListener("click", () => {
      const tool = item.getAttribute("data-tool");
      if (tool === "assess_safety_compliance") {
        submitQuery("Assess safety compliance for high-voltage industrial machinery operation");
      } else if (tool === "log_incident_ticket") {
        submitQuery("Log an urgent incident ticket: Suspicious unauthorized login attempt on SOC portal");
      } else if (tool === "run_system_diagnostics") {
        submitQuery("Run full system diagnostics on SafeX network nodes and IoT sensors");
      } else if (tool === "dispatch_emergency_response") {
        submitQuery("Emergency: Immediate evacuation protocol for Facility Zone A");
      } else if (tool === "search_knowledge_base") {
        submitQuery("What are the standard operating procedures for chemical hazard containment?");
      }
    });
  });

  // Quick buttons in topbar
  quickDiagnosticsBtn.addEventListener("click", () => {
    submitQuery("Run real-time diagnostics on firewall, SOC nodes, and IoT sensors");
  });

  quickEmergencyBtn.addEventListener("click", () => {
    submitQuery("Emergency: Trigger emergency dispatch and safety evacuation for Zone B");
  });

  refreshTelemetryBtn.addEventListener("click", () => {
    refreshTelemetryBtn.classList.add("fa-spin");
    fetchTelemetry().finally(() => {
      setTimeout(() => refreshTelemetryBtn.classList.remove("fa-spin"), 500);
    });
  });

  // Incident Modal
  viewAllIncidentsBtn.addEventListener("click", () => {
    openIncidentsModal();
  });

  modalClose.addEventListener("click", () => {
    incidentModal.classList.remove("active");
  });

  window.addEventListener("click", (e) => {
    if (e.target === incidentModal) {
      incidentModal.classList.remove("active");
    }
  });

  // Form submit
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query || isProcessing) return;
    submitQuery(query);
  });

  async function submitQuery(queryText) {
    if (isProcessing) return;
    isProcessing = true;
    sendBtn.disabled = true;

    // Hide welcome hero if still visible
    if (welcomeHero && welcomeHero.parentNode === chatMessages) {
      welcomeHero.style.display = "none";
    }

    // Append User Message
    appendUserMessage(queryText);
    userInput.value = "";
    userInput.style.height = "auto";
    scrollToBottom();

    // Append Agent Typing / Reasoning placeholder
    const typingId = "typing-" + Date.now();
    appendTypingIndicator(typingId);
    scrollToBottom();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: queryText })
      });

      if (!res.ok) {
        throw new Error(`Server returned HTTP ${res.status}`);
      }

      const data = await res.json();
      removeElement(typingId);

      // Append Full Agent Message with Chain of Thought
      appendAgentResponse(data);
      scrollToBottom();

      // Refresh telemetry & incidents in case new ticket was created
      fetchTelemetry();
      fetchIncidents();
    } catch (err) {
      console.error("Chat error:", err);
      removeElement(typingId);
      appendAgentResponse({
        response: `⚠️ **Connection Error**: Unable to reach SafeX Agent Core. Please ensure the backend server is running.\n\n*Details: ${err.message}*`,
        steps: []
      });
      scrollToBottom();
    } finally {
      isProcessing = false;
      sendBtn.disabled = false;
      userInput.focus();
    }
  }

  function appendUserMessage(text) {
    const row = document.createElement("div");
    row.className = "message-row user";
    row.innerHTML = `
      <div class="message-content-wrapper">
        <div class="user-bubble">${escapeHtml(text)}</div>
      </div>
      <div class="message-avatar user-avatar">
        <i class="fa-solid fa-user"></i>
      </div>
    `;
    chatMessages.appendChild(row);
  }

  function appendTypingIndicator(id) {
    const row = document.createElement("div");
    row.className = "message-row";
    row.id = id;
    row.innerHTML = `
      <div class="message-avatar agent-avatar">
        <i class="fa-solid fa-shield-halved"></i>
      </div>
      <div class="message-content-wrapper">
        <div class="agent-bubble">
          <div class="typing-indicator">
            <span style="font-size:0.8rem; color:var(--cyan-primary); font-weight:600; margin-right:6px;">
              <i class="fa-solid fa-brain"></i> Agentic reasoning in progress...
            </span>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
          </div>
        </div>
      </div>
    `;
    chatMessages.appendChild(row);
  }

  function appendAgentResponse(data) {
    const row = document.createElement("div");
    row.className = "message-row";

    // Build Chain of Thought drawer if steps exist
    let cotHtml = "";
    if (data.steps && data.steps.length > 0) {
      const stepItems = data.steps.map(step => {
        const typeClass = step.type || "thought";
        const detailsStr = typeof step.details === "object" 
          ? JSON.stringify(step.details, null, 2) 
          : String(step.details);

        return `
          <div class="cot-step-item ${typeClass}">
            <div class="cot-step-header">
              <i class="fa-solid ${getStepIcon(step.type)}"></i> ${escapeHtml(step.title || step.type)}
            </div>
            <div class="cot-step-body">${escapeHtml(detailsStr)}</div>
          </div>
        `;
      }).join("");

      cotHtml = `
        <div class="cot-drawer open">
          <div class="cot-header" onclick="this.parentElement.classList.toggle('open')">
            <div class="cot-title">
              <i class="fa-solid fa-diagram-project"></i>
              <span>Agentic Reasoning Trace (${data.steps.length} Steps)</span>
            </div>
            <i class="fa-solid fa-chevron-down cot-toggle-icon"></i>
          </div>
          <div class="cot-steps">
            ${stepItems}
          </div>
        </div>
      `;
    }

    const formattedContent = parseMarkdown(data.response || "");

    row.innerHTML = `
      <div class="message-avatar agent-avatar">
        <i class="fa-solid fa-shield-halved"></i>
      </div>
      <div class="message-content-wrapper">
        ${cotHtml}
        <div class="agent-bubble">
          ${formattedContent}
        </div>
      </div>
    `;

    chatMessages.appendChild(row);
  }

  function getStepIcon(type) {
    switch (type) {
      case "tool_call": return "fa-wrench";
      case "observation": return "fa-eye";
      case "thought": return "fa-lightbulb";
      default: return "fa-circle-check";
    }
  }

  // Markdown formatter
  function parseMarkdown(md) {
    let html = escapeHtml(md);

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^# (.*$)/gim, '<h3>$1</h3>');

    // Bold & Italics
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bullet lists
    html = html.replace(/^\s*• (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^\s*[\-\*] (.*$)/gim, '<li>$1</li>');

    // Numbered lists
    html = html.replace(/^\s*\d+\.\s+(.*$)/gim, '<li>$1</li>');

    // Wrap consecutive <li> into <ul>
    html = html.replace(/(<li>.*?<\/li>(\s*<li>.*?<\/li>)*)/gs, '<ul>$1</ul>');

    // Paragraph breaks
    html = html.replace(/\n{2,}/g, '</p><p>');
    html = '<p>' + html + '</p>';
    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/<p>(<h3>.*?<\/h3>)<\/p>/g, '$1');
    html = html.replace(/<p>(<ul>.*?<\/ul>)<\/p>/g, '$1');

    return html;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
  }

  function scrollToBottom() {
    chatViewport.scrollTop = chatViewport.scrollHeight;
  }

  function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  // Telemetry Fetcher
  async function fetchTelemetry() {
    try {
      const res = await fetch("/api/status");
      if (!res.ok) return;
      const data = await res.json();
      if (data.systems) {
        if (data.systems.network_firewall) {
          metricThreats.innerText = data.systems.network_firewall.blocked_attacks_24h || 142;
        }
        if (data.systems.soc_monitoring) {
          metricSoc.innerText = data.systems.soc_monitoring.agents_connected || 48;
        }
        if (data.systems.industrial_iot_gateway) {
          metricHealth.innerText = data.systems.industrial_iot_gateway.sensor_health || "99.8%";
        }
      }
    } catch (e) {
      console.warn("Telemetry fetch error:", e);
    }
  }

  // Incidents Fetcher
  async function fetchIncidents() {
    try {
      const res = await fetch("/api/incidents");
      if (!res.ok) return;
      const incidents = await res.json();

      metricTickets.innerText = incidents.length;

      if (!incidentListSidebar) return;
      incidentListSidebar.innerHTML = "";

      incidents.slice(0, 3).forEach(inc => {
        const item = document.createElement("div");
        item.className = `incident-card-sm ${inc.severity}`;
        item.innerHTML = `
          <div class="incident-top">
            <span class="incident-id">${inc.id}</span>
            <span class="incident-badge ${inc.severity}">${inc.severity}</span>
          </div>
          <span class="incident-title-sm">${escapeHtml(inc.title)}</span>
        `;
        item.addEventListener("click", () => {
          submitQuery(`Show details and actions for incident ${inc.id}`);
        });
        incidentListSidebar.appendChild(item);
      });
    } catch (e) {
      console.warn("Incidents fetch error:", e);
    }
  }

  // Incidents Full Modal View
  async function openIncidentsModal() {
    incidentModal.classList.add("active");
    modalBody.innerHTML = `<div style="text-align:center; padding:1.5rem;"><i class="fa-solid fa-spinner fa-spin"></i> Loading tickets...</div>`;

    try {
      const res = await fetch("/api/incidents");
      const incidents = await res.json();

      if (!incidents.length) {
        modalBody.innerHTML = `<p>No active incidents found.</p>`;
        return;
      }

      modalBody.innerHTML = incidents.map(inc => `
        <div style="background:var(--bg-card); padding:1rem; border-radius:10px; border-left:4px solid var(--cyan-primary);">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
            <strong style="color:var(--cyan-primary); font-family:var(--font-mono);">${inc.id}</strong>
            <span class="incident-badge ${inc.severity}">${inc.severity}</span>
          </div>
          <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.25rem;">${escapeHtml(inc.title)}</div>
          <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.5rem;">${escapeHtml(inc.description || 'No description provided')}</div>
          <div style="font-size:0.75rem; color:var(--text-secondary); display:flex; justify-content:space-between;">
            <span><i class="fa-solid fa-user-shield"></i> ${escapeHtml(inc.assigned_to)}</span>
            <span><i class="fa-solid fa-clock"></i> ${inc.timestamp}</span>
          </div>
        </div>
      `).join("");
    } catch (e) {
      modalBody.innerHTML = `<p style="color:var(--red-primary);">Failed to load incident vault.</p>`;
    }
  }
});
