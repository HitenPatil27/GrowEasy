# GrowEasy — Agentic AI SIP Investment Assistant

GrowEasy is an **Agentic AI-powered SIP (Systematic Investment Plan) advisory platform** that helps new investors set financial goals, receive SIP recommendations, and learn investing through an interactive chatbot interface.

This project simplifies financial planning using **reasoning-based AI agents, verified fund data, and an intuitive dashboard built on Streamlit**.  

---

## Executive Summary
A large portion of India's urban population stays away from formal investments due to:
- Lack of financial awareness
- Language & accessibility barriers
- Misconception that investing requires high capital

GrowEasy bridges this gap using an **AI chatbot + SIP recommendation engine** that guides users in selecting SIP plans based on income, risk appetite, and financial goals.  

---

## Vision Statement
> Democratize financial planning by enabling every individual to invest confidently through accessible, AI-driven guidance.

GrowEasy aims to provide a **multilingual, ethical, and intuitive SIP advisory system** for first-time investors.  

---

## MVP Description
The current MVP (built on Streamlit) enables users to:
- Enter financial goals
- Receive AI-based SIP recommendations
- Chat with a financial advisory chatbot to learn and clarify doubts  
:contentReference[oaicite:4]{index=4}

*Reminder Agent & real-time notification system planned for the next version.*

---

## Core MVP Modules
| Module | Description |
|--------|-------------|
| Planner Agent | Converts goals into structured SIP plans |
| Recommendation Agent | Suggests SIPs using mutual fund APIs |
| Chatbot Interface | Natural language conversation for guidance |

---

## Feature List
| Category | Details |
|---------|---------|
| Goal Planning | Planner Agent structures long-term goals |
| SIP Recommendation | Fund suggestions based on risk & duration |
| Interactive Chat | AI chatbot for guidance and education |
| Live Fund Data | Integration with AMFI (latest NAV & SIP portfolio) |
| Data Storage | Firebase store for user plans & recommendations |
| Expansion | Reminder & tracking modules (in development) |


---

## User Flow
1. Launch the GrowEasy Streamlit App  
2. Login / Register  
3. Select Goal, Risk Level & Monthly Income  
4. SIP recommendations generated automatically  
5. Chatbot answers queries  
6. Go to Planner Agent to set SIP schedule  
7. User can adjust inputs anytime  
---

## Developer Documentation
### Backend Architecture
- **FastAPI manages communication** between Streamlit and Firebase  
- **LangChain-based Agentic AI layer** handles reasoning & financial decision making  

### Modules Overview
- **Data Layer:** Firebase Realtime DB  
- **AI/Agent Layer:** Planner + Recommendation + Chatbot  
- **API Layer:** AMFI mutual fund data (NAV + SIP schemes)  
- **Frontend:** Streamlit dashboard + chat UI  
- **Deployment:** hosted on Streamlit Cloud  
---

## Technology Stack
| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI (Python) |
| Database | Firebase Realtime DB |
| AI Layer | LangChain / LangGraph |
| External API | Groq API / AMFI |
| Hosting | Streamlit Cloud / Render |
| Visualization | Matplotlib / Plotly |
| Version Control | GitHub |


---


## Future Enhancements
- Automated SIP reminders (WhatsApp / email)
- Goal progress tracker with SIP performance graphs
- End-to-end WhatsApp conversational interface
- Investment comparison dashboards
- Bank payment API integration  

---

## Ethical Considerations
- No auto-debits — user manually confirms each SIP
- Promotes only safe and verified investments
- Recommendations sourced from official APIs
- Encryption ensures user data confidentiality
- Educates users before recommending plans  

---

## Author
**Hiten Patil**

---

## ⭐ Support the Project
If GrowEasy inspires you, please ⭐ the repository to support its development!

