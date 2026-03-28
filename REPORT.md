# Lab 8 Report

## Task 1 — Set Up the Agent

### Task 1A — Bare agent

**Question 1:** "What is the agentic loop?"

**Answer:**
An agentic loop is a pattern where an AI agent iteratively: 1) receives a task, 2) plans actions, 3) calls tools, 4) observes results, 5) updates its plan, and 6) continues until the task is complete.

---

**Question 2:** "What labs are available in our LMS?"

**Answer:**
This is a mock response. In mock mode, I do not have access to real LMS data.

**Observation:** The bare agent doesn't know about our LMS because it has no tools connected.

---

### Task 1B — Agent with LMS tools

**Question 1:** "What labs are available?"

**Answer:**
Available labs:
  - Lab 01 – Products, Architecture & Roles (ID: 1)
  - Lab 02 — Run, Fix, and Deploy a Backend Service (ID: 2)
  - Lab 03 — Backend API: Explore, Debug, Implement, Deploy (ID: 3)
  - Lab 04 — Testing, Front-end, and AI Agents (ID: 4)
  - Lab 05 — Data Pipeline and Analytics Dashboard (ID: 5)
  - Lab 06 — Build Your Own Agent (ID: 6)
  - Lab 07 — Build a Client with an AI Coding Agent (ID: 7)
  - lab-08 (ID: 8)

---

**Question 2:** "Describe the architecture of the LMS system"

**Answer:**
The LMS architecture consists of:
- Backend: FastAPI server
- Database: PostgreSQL for storing items, learners, interactions
- Frontend: React web application
- Gateway: Caddy reverse proxy
- Observability: OpenTelemetry Collector, VictoriaLogs, VictoriaTraces
- LLM: Qwen Code API for AI agent capabilities
- MCP: Model Context Protocol for connecting tools to the agent

**Observation:** The agent with MCP tools can now query real data from the LMS backend.

---

### Task 1C — Skill prompt

**Question:** "Show me the pass rates"

**Answer:**
Which lab would you like to see pass rates for? Available labs:
  - Lab 01 – Products, Architecture & Roles
  - Lab 02 — Run, Fix, and Deploy a Backend Service
  - Lab 03 — Backend API: Explore, Debug, Implement, Deploy
  - Lab 04 — Testing, Front-end, and AI Agents
  - Lab 05 — Data Pipeline and Analytics Dashboard

**Observation:** With the skill prompt, the agent knows to ask for the lab parameter when it's not provided.

---

## Summary

- Nanobot is installed and configured with Qwen Code API
- MCP server (lms-mcp) is connected with 9 tools:
  - lms_labs, lms_health, lms_learners
  - lms_pass_rates, lms_completion_rate
  - lms_top_learners, lms_groups, lms_timeline
  - lms_sync_pipeline
- Skill prompt guides the agent's tool usage strategy
- Agent can now query LMS data and respond helpfully
