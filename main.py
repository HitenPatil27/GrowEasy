# main.py (full updated code: professional B&W theme, no white fillers, logo in sidebar small, fixed deprecation)
import streamlit as st
from user_auth import authenticate_user, create_user
from main_recommendation_ui import recommendation_ui
from main_chat_ui import chat_ui
from main_planner_ui import planner_ui
from config import GROQ_API_KEY
from groq import Groq
import json
from datetime import datetime

# Professional B&W CSS with animations, no white fillers
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background-color: #000;
        color: #fff;
    }
    .main-header {
        font-size: 3.5rem;
        color: #fff;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .sidebar-header {
        font-size: 1.8rem;
        color: #fff;
        margin-bottom: 1rem;
        animation: fadeInLeft 0.8s ease-out;
    }
    .advisor-welcome {
        background: linear-gradient(135deg, #333 0%, #111 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: #fff;
        text-align: center;
        animation: slideInUp 1s ease-out;
        margin-bottom: 2rem;
        border: 1px solid #555;
    }
    .nav-button {
        width: 100%;
        margin: 0.5rem 0;
        padding: 1rem;
        border-radius: 0.75rem;
        font-weight: 600;
        background: linear-gradient(135deg, #555 0%, #333 100%);
        color: #fff;
        border: 1px solid #777;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    .nav-button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(255,255,255,0.1);
        background: linear-gradient(135deg, #666 0%, #444 100%);
    }
    .feature-card {
        background: #111;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.8);
        animation: fadeInUp 0.8s ease-out;
        border-left: 4px solid #fff;
        border: 1px solid #333;
    }
    .item-hover {
        padding: 1rem;
        border-bottom: 1px solid #333;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: fadeInLeft 0.5s ease-out;
        background: #111;
        color: #fff;
    }
    .item-hover:hover {
        background: #222;
        transform: translateX(5px);
        border-left: 3px solid #fff;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #333;
        border-top: 3px solid #fff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="GrowEasy — Professional Mutual Fund Advisor", page_icon="💼", layout="wide")

# Sidebar for navigation and user management
with st.sidebar:
    # Logo in sidebar, small
    try:
        st.image("GrowEasy.png", width=100, use_container_width=False)  # Small logo in sidebar
    except:
        st.markdown('<h3 style="color: #fff; text-align: center;">GrowEasy</h3>', unsafe_allow_html=True)  # Fallback
    
    st.markdown('<div class="sidebar-header">💼 GrowEasy Advisor</div>', unsafe_allow_html=True)
    
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        # Login/Register in sidebar with animation
        st.markdown('<div class="advisor-welcome">Welcome to Your Personal Mutual Fund Advisor</div>', unsafe_allow_html=True)
        st.markdown("### Login to Start")
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            email = st.text_input("Email", key="login_email", placeholder="advisor@groweasy.com")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("🔐 Login", key="login_btn", help="Secure login for personalized advice"):
                success, result = authenticate_user(email, password)
                if success:
                    st.session_state.user_id = result[0]
                    st.session_state.user_name = result[1]
                    st.success(f"Welcome back, {st.session_state.user_name}! Your advisor is ready.")
                    st.rerun()
                else:
                    st.error(result)

        with tab2:
            name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
            email = st.text_input("Email", key="reg_email", placeholder="john@example.com")
            password = st.text_input("Password", type="password", key="reg_pass")
            if st.button("📝 Register", key="reg_btn", help="Start your advisory journey"):
                success, result = create_user(name, email, password)
                if success:
                    st.session_state.user_id = result[1]
                    st.session_state.user_name = result[2]
                    st.success(f"Account created for {st.session_state.user_name}! Let's plan your wealth.")
                    st.rerun()
                else:
                    st.error(result[0])
    else:
        # User info with advisor feel
        st.markdown(f'<div class="advisor-welcome">Hello, {st.session_state.user_name} 👋<br>Your Dedicated Wealth Advisor</div>', unsafe_allow_html=True)
        st.markdown(f"**Portfolio ID:** {st.session_state.user_id[:8]}...")
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            del st.session_state.user_id
            del st.session_state.user_name
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Advisory Services")
        
        # Feature buttons with animations
        if st.button("📈 Portfolio Recommendations", key="nav_rec", help="Get tailored fund suggestions"):
            st.session_state.active_feature = "recommendation"
            st.rerun()
        
        if st.button("💬 Advisor Chat", key="nav_chat", help="Ask your AI advisor questions"):
            st.session_state.active_feature = "chat"
            st.rerun()
        
        if st.button("📅 Investment Plan", key="nav_plan", help="Build a step-by-step plan"):
            st.session_state.active_feature = "planner"
            st.rerun()

# Main content area with professional layout
if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.markdown('<h1 class="main-header">Welcome to GrowEasy Advisor</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #ccc; animation: fadeInUp 1s ease-out;'>
    Your trusted partner for mutual fund investments. Get personalized advice, plans, and insights to grow your wealth securely.
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📈 **Recommendations**<br>AI-curated funds based on your goals.")
    with col2:
        st.info("💬 **Chat Advisor**<br>Ask questions, get instant financial tips.")
    with col3:
        st.info("📅 **Investment Plan**<br>Step-by-step roadmap for your portfolio.")
else:
    if "active_feature" not in st.session_state:
        st.session_state.active_feature = "recommendation"  # Default
    
    # Dashboard-like main area with cards
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: #fff;">Dashboard for {st.session_state.user_name}</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Two-column layout for features
    col1, col2 = st.columns([1, 3])
    
    if st.session_state.active_feature == "recommendation":
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Recent Recommendations")
            from recommendation import get_user_recommendations
            try:
                user_recs = get_user_recommendations(st.session_state.user_id, limit=10)
            except:
                user_recs = []
            if user_recs:
                for r in user_recs:
                    created = r.get("created_at", "Unknown")
                    summary = r.get('recommendation', '')[:100] + "..."
                    if st.button(f"**{created}**\n{summary}", key=f"rec_{r.get('id', hash(created))}", help="Load this recommendation", use_container_width=True):
                        st.session_state.selected_rec = r
                        st.rerun()
            else:
                st.info("No recommendations yet. Generate one!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown('<h2 style="color: #fff;">📈 Portfolio Recommendations</h2>', unsafe_allow_html=True)
            recommendation_ui()
            if "selected_rec" in st.session_state:
                st.markdown("### Loaded Recommendation")
                st.markdown(st.session_state.selected_rec.get('recommendation', ''))
                if st.button("Clear Selection"):
                    del st.session_state.selected_rec
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_feature == "chat":
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 💬 Recent Sessions")
            from chat import get_recent_chats
            try:
                recent_chats = get_recent_chats(st.session_state.user_id, limit=10)
            except:
                recent_chats = []
            if recent_chats:
                for chat in recent_chats[-5:]:
                    timestamp = chat.get("timestamp", "Unknown")
                    preview = chat.get("content", "")[:50] + "..." if len(chat.get("content", "")) > 50 else chat.get("content", "")
                    role_icon = "👤" if chat.get("role") == "user" else "🤖"
                    if st.button(f"{role_icon} {timestamp}\n{preview}", key=f"chat_{hash(str(timestamp) + preview)}", help="Load this session", use_container_width=True):
                        st.session_state.selected_chat = chat
                        st.rerun()
            else:
                st.info("No sessions yet. Start chatting!")
            
            st.markdown("---")
            if st.button("🆕 New Session", key="new_chat", use_container_width=True):
                if "chat_history" in st.session_state:
                    st.session_state.chat_history = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown('<h2 style="color: #fff;">💬 Advisor Chat</h2>', unsafe_allow_html=True)
            chat_ui()
            if "selected_chat" in st.session_state:
                st.markdown("### Loaded Session Preview")
                st.markdown(f"**{st.session_state.selected_chat.get('role').title()}:** {st.session_state.selected_chat.get('content')}")
                if st.button("Clear Selection"):
                    del st.session_state.selected_chat
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # planner
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Recent Plans")
            from planner import get_user_plans
            try:
                user_plans = get_user_plans(st.session_state.user_id, limit=5)
            except:
                user_plans = []
            if user_plans:
                for p in user_plans:
                    created = p.get("created_at", "Unknown")
                    fund = p.get("fund", "Unknown")
                    if st.button(f"**{fund}**\n{created}", key=f"plan_{p.get('id', hash(fund + str(created)))}", help="Load this plan", use_container_width=True):
                        st.session_state.selected_plan = p
                        st.rerun()
            else:
                st.info("No plans yet. Create one!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown('<h2 style="color: #fff;">📅 Investment Plan</h2>', unsafe_allow_html=True)
            planner_ui()
            if "selected_plan" in st.session_state:
                st.markdown("### Loaded Plan")
                st.markdown(st.session_state.selected_plan.get('plan', ''))
                if st.button("Clear Selection"):
                    del st.session_state.selected_plan
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)