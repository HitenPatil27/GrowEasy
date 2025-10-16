# planner.py (updated to include rec_id parameter)
from firebase_utils import init_firestore
from config import PLANS_COL
from nav_utils import get_latest_nav_snapshot
from firebase_admin import firestore
import pandas as pd

db = init_firestore()

def save_plan(user_id, plan_text, selected_fund, details, rec_id=None):
    doc_ref = db.collection(PLANS_COL).document()
    doc_ref.set({
        "user_id": user_id,
        "plan": plan_text,
        "fund": selected_fund,
        "details": details,  # e.g., {"amount": 50000, "horizon": 5, ...}
        "rec_id": rec_id,  # Link back to recommendation
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id

def get_user_plans(user_id, limit=5):
    try:
        docs = db.collection(PLANS_COL).where("user_id", "==", user_id)\
            .order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).get()
        return [d.to_dict() for d in docs]
    except Exception as e:
        if "requires an index" in str(e):
            print(f"Index needed for plans: {e}")
            # Fallback: Fetch all and sort client-side
            all_docs = db.collection(PLANS_COL).where("user_id", "==", user_id).get()
            unsorted = [d.to_dict() for d in all_docs]
            sorted_docs = sorted(unsorted, key=lambda x: x.get("created_at").timestamp() if x.get("created_at") else 0, reverse=True)
            return sorted_docs[:limit]
        raise e