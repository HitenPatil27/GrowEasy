import requests
import pandas as pd
import streamlit as st
from firebase_utils import init_firestore
from config import NAV_SNAP_COL, AMFI_NAV_URL
from datetime import datetime
from firebase_admin import firestore

db = init_firestore()

@st.cache_data(show_spinner=False)
def scrape_amfi_data_once():
    try:
        response = requests.get(AMFI_NAV_URL, timeout=15)
        if response.status_code != 200:
            return pd.DataFrame()
        lines = response.text.split("\n")[1:]
        data = []
        for line in lines:
            cols = line.split(";")
            if len(cols) < 5:
                continue
            try:
                nav_val = cols[4].strip().replace(",", "")
                nav_value = float(nav_val) if nav_val.replace('.', '', 1).isdigit() else None
                if nav_value is None:
                    continue
                data.append({
                    "Scheme Code": cols[0].strip(),
                    "Fund Name": cols[3].strip(),
                    "NAV": nav_value,
                    "Date": cols[7].strip() if len(cols) > 7 else ""
                })
            except Exception:
                continue
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()

def save_nav_snapshot(nav_df: pd.DataFrame, chunk_size=500):
    payload = nav_df.to_dict(orient="records")
    doc_ids = []
    for i in range(0, len(payload), chunk_size):
        chunk = payload[i:i+chunk_size]
        doc_ref = db.collection(NAV_SNAP_COL).document()
        doc_ref.set({
            "created_at": firestore.SERVER_TIMESTAMP,
            "snapshot": chunk,
            "chunk_index": i // chunk_size
        })
        doc_ids.append(doc_ref.id)
    return doc_ids

def get_latest_nav_snapshot():
    docs = db.collection(NAV_SNAP_COL).order_by("created_at", direction=firestore.Query.DESCENDING).limit(10).get()
    all_data = []
    doc_ids = []
    if not docs:
        return pd.DataFrame(), []
    # Get the most recent snapshot by taking the first doc's time, then all chunks with that time
    latest_time = docs[0].to_dict().get("created_at")
    relevant_docs = [d for d in docs if d.to_dict().get("created_at") == latest_time]
    chunks = sorted([d.to_dict() for d in relevant_docs], key=lambda x: x.get("chunk_index", 0))
    for chunk in chunks:
        all_data.extend(chunk.get("snapshot", []))
    doc_ids = [d.id for d in relevant_docs]
    return pd.DataFrame(all_data), doc_ids