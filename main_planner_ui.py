# main_planner_ui.py (updated: removed fixed 60/40 allocation, output based on user input SIP/horizon)
import streamlit as st
from recommendation import get_user_recommendations
from planner import save_plan, get_user_plans
from config import GROQ_API_KEY
from groq import Groq
import math
import pandas as pd

def planner_ui():
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("Please login first.")
        return

    st.subheader("📅 Investment Planner Agent")
    st.info("🤖 The Planner Agent creates a comprehensive investment plan based on your recommendation and user inputs. It includes SIP schedule, projections, milestones, tax tips, and reviews tailored to your SIP and horizon.")

    # Load user's recommendations
    try:
        user_recs = get_user_recommendations(st.session_state.user_id, limit=5)
    except:
        user_recs = []
    
    if not user_recs:
        st.warning("No recommendations found. Generate one in Recommendations first!")
        return

    # Select a recommendation
    rec_options = [(r.get("created_at", "Unknown"), r) for r in user_recs]
    selected_rec_option = st.selectbox(
        "Select a Recommendation",
        options=rec_options,
        format_func=lambda x: f"{x[0]} - {x[1].get('recommendation', '')[:100]}..."
    )
    selected_rec = selected_rec_option[1]

    # Extract funds
    rec_funds = selected_rec.get("funds", [])
    if not rec_funds:
        st.warning("No funds in this recommendation. Try another.")
        return

    # Fund selection (primary fund)
    fund_options = [(f["Fund Name"], f) for f in rec_funds]
    selected_fund_option = st.selectbox(
        "Pick Primary Fund from Recommendation",
        options=fund_options,
        format_func=lambda x: f"{x[0]} (₹{x[1].get('NAV', 0):.2f})"
    )
    selected_fund_info = selected_fund_option[1]

    # User details
    col1, col2 = st.columns(2)
    with col1:
        monthly_sip = st.number_input("Total Monthly SIP Amount (₹)", min_value=1000, step=1000, value=5000)
    with col2:
        horizon = st.number_input("Investment Horizon (Years)", min_value=1, max_value=30, value=5)

    if st.button("🚀 Generate Comprehensive Plan", type="primary", use_container_width=True):
        with st.spinner("Building your optimized investment plan..."):
            details = {
                "monthly_sip": monthly_sip,
                "horizon": horizon
            }
            rec_id = selected_rec.get("id", None)

            # Enhanced Prompt: Based on user input, no fixed allocation
            rec_summary = selected_rec.get("recommendation", "")[:300]
            other_funds = [f["Fund Name"] for f in rec_funds if f["Fund Name"] != selected_fund_info["Fund Name"]][:2]
            prompt = f"""
You are the Investment Planner Agent, creating a robust plan based on the user's recommendation: {rec_summary}

Primary Fund: '{selected_fund_info['Fund Name']}' (NAV: ₹{selected_fund_info.get('NAV', 0):.2f}).
Other Funds for Diversification: {', '.join(other_funds) if other_funds else 'None'}.

User: {st.session_state.user_name}, Total Monthly SIP: ₹{monthly_sip}, Horizon: {horizon} years.

Create a good, actionable plan based on user inputs with:

1. **Allocation**: Suggest allocation across funds based on SIP amount and recommendation (tailor to user input, e.g.).

2. **SIP Schedule**: Monthly breakdown for first year (e.g., Jan: ₹X to Fund A), then quarterly thereafter.

3. **Projections**: Year-wise corpus growth table (assume 10% avg return, step-up SIP 10% yearly).

4. **Milestones**: Key targets (e.g., Year 1: ₹X corpus, rebalance if needed).

5. **Risk & Tax**: Simple mitigations, LTCG tax (10% over ₹1L for equity after 1 year).

6. **Reviews**: Quarterly self-review tips, when to consult advisor.

Output structured with emojis, bullets, and a table for projections. Keep engaging, concise, and realistic.
"""
            
            plan_text = None
            try:
                client = Groq(api_key=GROQ_API_KEY)
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",  # Valid Groq model for full outputs
                    messages=[{"role": "system", "content": prompt}],
                    temperature=0.3,
                    max_tokens=3000  # High for full plan
                )
                plan_text = response.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"API Error: {e}")

            # Fallback: Basic plan text based on user input
            if not plan_text or len(plan_text) < 50:
                # Calculate projections with step-up
                step_up_rate = 0.10
                current_sip = monthly_sip
                yearly_corpus = []
                corpus = 0
                for year in range(1, horizon + 1):
                    annual_invest = current_sip * 12
                    corpus = (corpus + annual_invest) * 1.10  # 10% return
                    yearly_corpus.append(round(corpus))
                    current_sip *= (1 + step_up_rate)  # Step-up next year

                projections_table = "| Year | Corpus (₹) |\n|------|------------|\n" + "\n".join([f"| {y} | {c} |" for y, c in zip(range(1, horizon + 1), yearly_corpus)])
                
                other_fund_alloc = ', '.join(other_funds[:2]) if other_funds else "Secondary funds from rec"
                monthly_primary = monthly_sip * 0.7  # Example based on input, adjustable
                monthly_others = monthly_sip - monthly_primary
                
                plan_text = f"""
1. **Allocation**: Based on your SIP ₹{monthly_sip}, allocate to primary and diversified funds.
   - Primary ({selected_fund_info['Fund Name']}): ₹{monthly_primary:.0f}/month
   - Others ({other_fund_alloc}): ₹{monthly_others:.0f}/month

2. **SIP Schedule**: Monthly breakdown for first year (e.g., Jan: ₹X to Fund A), then quarterly thereafter.
   - Jan-Dec: ₹{monthly_primary:.0f} to primary + ₹{monthly_others:.0f} to others each month.
   - Year 2+: Quarterly: Q1 ₹{monthly_primary * 3 * 1.1:.0f} to primary, etc. (with 10% step-up).

3. **Projections**: Year-wise corpus growth table (assume 10% avg return, step-up SIP 10% yearly).
{projections_table}

4. **Milestones**: Key targets (e.g., Year 1: ₹X corpus, rebalance if needed).
   - Year 1: ₹{yearly_corpus[0]} corpus – Review allocation.
   - Year {horizon//2}: ₹{yearly_corpus[horizon//2 - 1] if horizon > 1 else yearly_corpus[0]} – Rebalance if drift >5%.
   - End: ₹{round(corpus)} – Achieve goal.

5. **Risk & Tax**: Simple mitigations, LTCG tax (10% over ₹1L for equity after 1 year).
   - Mitigations: Diversify, hold long-term, emergency fund separate.
   - Tax: LTCG 10% on gains > ₹1L (equity); indexation for debt.

6. **Reviews**: Quarterly self-review tips, when to consult advisor.
   - Quarterly: Track NAV vs benchmark, adjust if underperform >2%.
   - Consult advisor: Life changes (job, family), market crash, or annual.
                """

            st.subheader("📋 Your Comprehensive Investment Plan")
            st.markdown(plan_text)

            # Save
            plan_id = save_plan(st.session_state.user_id, plan_text, selected_fund_info["Fund Name"], details, rec_id)
            st.success(f"💾 Plan saved (ID: {plan_id}), linked to Rec ID: {rec_id}")

    # Recent plans
    st.markdown("---")
    st.subheader("📂 Your Recent Plans")
    try:
        user_plans = get_user_plans(st.session_state.user_id, limit=5)
    except:
        user_plans = []
    if user_plans:
        for p in user_plans:
            with st.expander(f"**{p.get('fund')}** - {p.get('details', {}).get('horizon', 'N/A')} yrs | SIP: ₹{p.get('details', {}).get('monthly_sip', 'N/A')} ({p.get('created_at')}) | Rec: {p.get('rec_id', 'N/A')}"):
                st.markdown(p.get('plan', ''))
    else:
        st.info("No plans yet. Generate one above!")