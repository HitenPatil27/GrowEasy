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
<img width="1916" height="921" alt="Dashboard" src="https://github.com/user-attachments/assets/d0a72df4-1a67-4f22-b362-7485596babf8" />

2. Login / Register
<img width="1913" height="912" alt="login" src="https://github.com/user-attachments/assets/6a8637c0-d36a-4ce5-bb17-18145ac5649b" />

3. Select Goal, Risk Level & Monthly Income
<img width="1913" height="918" alt="user input " src="https://github.com/user-attachments/assets/dfe6ec1f-38e4-43ec-85f1-62c6dde0e755" />

4. SIP recommendations generated automatically
<img width="1917" height="923" alt="rec_output" src="https://github.com/user-attachments/assets/ba79969a-9040-41ff-af30-c47fa81c0a3f" />
<img width="1915" height="923" alt="user input_1" src="https://github.com/user-attachments/assets/be13470d-06bd-4049-a324-a2b80648805c" />

5. Chatbot answers queries
<img width="1897" height="905" alt="ChatBot" src="https://github.com/user-attachments/assets/80824071-70b5-494d-ab11-2c0708ecf7ea" />

6. Go to Planner Agent to set SIP schedule
<img width="1918" height="912" alt="planer output" src="https://github.com/user-attachments/assets/e90a08e6-1432-451b-a754-348c2aabcf2d" />
<img width="1913" height="918" alt="planer output1" src="https://github.com/user-attachments/assets/ef11c693-6ae7-412e-ba03-a3e644689b4b" />

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

