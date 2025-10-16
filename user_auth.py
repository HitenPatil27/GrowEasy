import bcrypt
import base64
from firebase_utils import init_firestore
from config import USERS_COL
from firebase_admin import firestore

db = init_firestore()

def hash_password(raw_password: str) -> str:
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
    return base64.b64encode(hashed).decode("utf-8")

def check_password(raw_password, hashed_b64):
    hashed_bytes = base64.b64decode(hashed_b64.encode("utf-8"))
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_bytes)

def create_user(name, email, password):
    users_ref = db.collection(USERS_COL)
    q = users_ref.where("email", "==", email).get()
    if q:
        return False, ("Error", None)
    hashed = hash_password(password)
    doc = users_ref.document()
    doc.set({
        "name": name,
        "email": email,
        "password_hash": hashed,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return True, ("Success", doc.id, name)

def authenticate_user(email, password):
    users_ref = db.collection(USERS_COL)
    docs = users_ref.where("email", "==", email).limit(1).get()
    if not docs:
        return False, "No user found."
    u = docs[0]
    user_data = u.to_dict()
    stored_hash = user_data.get("password_hash", "")
    ok = check_password(password, stored_hash)
    if not ok:
        return False, "Incorrect password."
    return True, (u.id, user_data.get("name"))