import firebase_admin
from firebase_admin import credentials, db as firebase_db

# Inisialisasi Firebase sekali saja


if not firebase_admin._apps:
    cred = credentials.Certificate("quickstart-1583738730654-firebase-adminsdk-fbsvc-eb4f1eaad3.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://quickstart-1583738730654-default-rtdb.asia-southeast1.firebasedatabase.app',
    })