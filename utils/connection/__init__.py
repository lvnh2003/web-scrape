from .postgresql import get_db_connection
from .firebase import get_firestore

db_conn = get_db_connection()
firestore_db = get_firestore()