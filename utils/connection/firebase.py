import firebase_admin
from firebase_admin import credentials, firestore

def get_firestore():
    cred = credentials.Certificate("config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
