from firebase_utils import init_firestore
from config import RECS_COL
from nav_utils import get_latest_nav_snapshot
from firebase_admin import firestore
import pandas as pd

db = init_firestore()

def save_recommendation(user_id, rec_text, recommended_funds):
    doc_ref = db.collection(RECS_COL).document()
    doc_ref.set({
        "user_id": user_id,
        "recommendation": rec_text,
        "funds": recommended_funds,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id

def get_user_recommendations(user_id, limit=5):
    try:
        docs = db.collection(RECS_COL).where("user_id", "==", user_id)\
            .order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).get()
        return [d.to_dict() for d in docs]
    except Exception as e:
        if "requires an index" in str(e):
            # Log or raise with link if needed
            print(f"Index needed: {e}")
            # Fallback: Fetch all for this user and sort client-side (inefficient for large data)
            all_docs = db.collection(RECS_COL).where("user_id", "==", user_id).get()
            unsorted = [d.to_dict() for d in all_docs]
            sorted_docs = sorted(unsorted, key=lambda x: x.get("created_at").timestamp() if x.get("created_at") else 0, reverse=True)
            return sorted_docs[:limit]
        raise e

def map_goal_risk_to_category(goal, risk):
    g = (goal or "").lower()
    r = (risk or "moderate").lower()
    if "wealth" in g or "growth" in g:
        if r == "high":
            return "Equity"
        elif r == "moderate":
            return "Hybrid"
        else:
            return "Debt"
    if "retire" in g or "retirement" in g:
        if r in ["moderate", "high"]:
            return "Balanced"
        else:
            return "Debt"
    if r == "low":
        return "Debt"
    if r == "high":
        return "Equity"
    return "Hybrid"

def rank_funds_by_category(df, category, top_k=10):
    if df.empty:
        return pd.DataFrame()
    mask = df['Fund Name'].str.contains(category, case=False, na=False)
    filtered = df[mask]
    if filtered.empty:
        filtered = df[df['Fund Name'].str.contains("fund|equity|debt|balanced|hybrid", case=False, na=False)]
    if filtered.empty:
        return pd.DataFrame()
    return filtered.sort_values(by="NAV", ascending=False).head(top_k)