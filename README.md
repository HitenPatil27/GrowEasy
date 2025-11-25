# GrowEasy – Agentic AI-based SIP Investment Assistant

GrowEasy is an **AI-powered SIP (Systematic Investment Plan) Assistant** designed to help Indian users start and manage investments easily through **WhatsApp or a lightweight mobile app**.  
The platform reduces the barrier to investing by providing **local-language guidance, goal-based planning, reminders, and progress tracking**.

---

## Problem Statement
A huge portion of India's urban population does not participate in formal investments due to:
- Low awareness of SIP options
- Language and accessibility barriers
- Lack of financial guidance or planning support
- Difficulty starting with small investment amounts (₹100–₹500)

> GrowEasy solves these challenges using conversational AI and automation.  
:contentReference[oaicite:1]{index=1}

---

## Proposed Solution
An **Agentic AI SIP Assistant** that:
- Helps users set financial goals in local languages
- Recommends SIP plans based on income, risk appetite & timeline
- Sends monthly WhatsApp reminders
- Tracks goal completion and provides motivational feedback

### Agentic Architecture
| Agent | Responsibility |
|-------|----------------|
| Planner Agent | Creates personalised SIP/goal plans |
| Reminder Agent | Sends scheduled monthly reminders to invest |
| Progress Tracker Agent | Monitors confirmations and tracks milestones |

> Final workflow: **Goal Planning → Monthly Reminder → Payment → Confirmation**  
:contentReference[oaicite:2]{index=2}

---

## Core Features
### Task Automation
- Auto goal creation from conversational input
- Auto-generated monthly reminders
- Goal progress updates

### Decision Making
- Recommends best SIP category (e.g., debt MF vs hybrid MF) based on income, risk appetite & timeline

### Learning & Adaptation
- Adjusts reminder frequency based on user response
- Suggests smaller/incremental goals if user frequently misses SIPs

:contentReference[oaicite:3]{index=3}

---

## Technology Stack

| Component | Technology |
|----------|------------|
| Frontend | WhatsApp API / Flutter App |
| Backend | Python (FastAPI), Firebase |
| Agentic Layer | LLM + LangChain / LangGraph + mfapi.in |
| Database | Firebase Realtime DB |

:contentReference[oaicite:4]{index=4}

---

## Ethical & Safety Considerations
- **No Auto-Debit** — user manually approves every payment
- **Only safe/curated SIPs recommended**
- **Privacy & Consent** — encrypted communication via WhatsApp
- **Transparent communication** — SIP details clearly shown in user’s local language with disclaimers

:contentReference[oaicite:5]{index=5}

---

## Future Scope
- Voice-based investment assistant
- Support for lump-sum and mutual fund comparisons
- AI savings coach with gamification

