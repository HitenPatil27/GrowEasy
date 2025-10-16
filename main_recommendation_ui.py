# main_recommendation_ui.py
import streamlit as st
from nav_utils import scrape_amfi_data_once, save_nav_snapshot
from recommendation import save_recommendation, map_goal_risk_to_category, rank_funds_by_category
from chat import save_chat
import json
import pandas as pd

def recommendation_ui():
    # Professional form layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        goal = st.text_input("Investment Goal", placeholder="e.g., Wealth creation for 10 years", help="Describe your objective")
    
    with col2:
        risk = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"], help="Your tolerance for market volatility")
    
    with col3:
        income = st.number_input("Monthly Income (₹)", min_value=0, step=1000, value=50000, help="For SIP calculation")
    
    if st.button("🔍 Generate Recommendations", type="primary", use_container_width=True, help="Scrape latest NAV & get AI advice"):
        with st.spinner("Fetching latest NAV data and generating personalized recommendations..."):
            nav_df = scrape_amfi_data_once()
            if nav_df.empty:
                st.error("❌ Failed to fetch NAV data. Please try again.")
                return
            else:
                snap_ids = save_nav_snapshot(nav_df)
                st.success(f"✅ NAV snapshot saved ({len(snap_ids)} chunks).")

                # Categorize and rank
                category = map_goal_risk_to_category(goal, risk)
                top_funds = rank_funds_by_category(nav_df, category, top_k=10)
                if top_funds.empty:
                    top_funds = nav_df.sort_values(by="NAV", ascending=False).head(10)
                    category = "Top NAV Funds"

                # Display top funds table
                st.subheader(f"📊 Top Funds in '{category}' Category")
                st.dataframe(
                    top_funds[['Fund Name', 'NAV', 'Date']].style.format({'NAV': '{:.2f}'}), 
                    use_container_width=True,
                    hide_index=True
                )

                # AI Recommendation
                fund_list = top_funds[['Fund Name', 'NAV']].head(5).to_dict(orient="records")  # Top 5 for prompt
                prompt = f"""
You are Growbot — expert mutual fund advisor.
User: {st.session_state.user_name}, Goal: {goal}, Risk: {risk}, Income: ₹{income:,}

Top funds (latest NAV):
{json.dumps(fund_list, indent=2)}

Provide:
- 3 fund recommendations with reasons (1-2 sentences each)
- Suggested SIP amount based on income (10-20% allocation)
- Brief risk summary
- Overall portfolio advice

Use emojis, bullets, and keep engaging & concise.
"""
                
                from config import GROQ_API_KEY
                from groq import Groq
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[{"role": "system", "content": prompt}],
                        temperature=0.6,
                        max_tokens=1500
                    )
                    ai_reply = response.choices[0].message.content.strip()
                except Exception as e:
                    ai_reply = f"⚠️ AI generation error: {str(e)[:100]}..."

                st.subheader("🤖 Growbot's Personalized Advice")
                st.markdown(ai_reply)

                # Save
                rec_id = save_recommendation(st.session_state.user_id, ai_reply, fund_list)
                st.caption(f"💾 Saved as Recommendation ID: {rec_id}")
                save_chat(st.session_state.user_id, "assistant", f"[New Recommendation ID:{rec_id}] {ai_reply}")
                
                st.balloons()  # Fun interactive element

    # Recent recs already handled in main.py sidebar