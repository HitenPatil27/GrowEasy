# main_chat_ui.py
import streamlit as st
from chat import save_chat, get_recent_chats
from recommendation import get_user_recommendations
from nav_utils import get_latest_nav_snapshot
from datetime import datetime
from config import GROQ_API_KEY
from groq import Groq

def chat_ui():
    nav_snapshot_df, _ = get_latest_nav_snapshot()
    
    # Chat container with better styling
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(content)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(content)
        else:
            st.info("Start a conversation with GrowBot!")

    # Chat input
    user_q = st.chat_input("Ask GrowBot anything about your finances...", key="chat_input")
    if user_q:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_q)
        
        save_chat(st.session_state.user_id, "user", user_q)
        st.session_state.chat_history.append({"role": "user", "content": user_q, "timestamp": datetime.utcnow()})

        # Prepare context
        last_msgs = st.session_state.chat_history[-6:]
        convo_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in last_msgs])

        try:
            recs_for_context = get_user_recommendations(st.session_state.user_id, limit=3)
        except:
            recs_for_context = []
        rec_text = ""
        if recs_for_context:
            rec_text = "\nUser's saved recommendations:\n"
            for r in recs_for_context:
                rec_text += f"- {r.get('recommendation')[:400]}\n"

        nav_text = ""
        if not nav_snapshot_df.empty:
            top5 = nav_snapshot_df.sort_values(by="NAV", ascending=False).head(5)
            nav_text = "\nLatest NAV snapshot (top 5):\n" + "\n".join([f"{i+1}. {r['Fund Name']} - ₹{r['NAV']:.2f}" for i, r in top5.iterrows()])

        chat_prompt = f"""
You are Growbot, a mutual fund advisor chatbot.
Do not re-scrape AMFI. Use NAV snapshot & saved recommendations.

{rec_text}
{nav_text}

Conversation:
{convo_text}

User: {user_q}

Answer concisely, reference saved recommendations if relevant, prefer funds in user's saved recommendations.
Use bullet points for lists, emojis for engagement.
"""
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Growbot is thinking..."):
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[{"role": "system", "content": chat_prompt}],
                        temperature=0.7,
                        max_tokens=1500
                    )
                    ai_reply = response.choices[0].message.content.strip()
                except Exception as e:
                    ai_reply = f"⚠️ Sorry, I'm having trouble responding: {str(e)[:100]}..."

                st.markdown(ai_reply)

        save_chat(st.session_state.user_id, "assistant", ai_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply, "timestamp": datetime.utcnow()})
        
        # Rerun to update container
        st.rerun()