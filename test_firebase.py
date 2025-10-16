import os
from firebase_admin import credentials, initialize_app, firestore

sa = os.environ.get("FIREBASE_SA_PATH") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate('D:/NUV/7th SEM/Agentic AI/GrowEasy/groweasy-da981-firebase-adminsdk-fbsvc-9501928c72.json')
initialize_app(cred)
db = firestore.client()
print("Success, collections:", [c.id for c in db.collections()])
