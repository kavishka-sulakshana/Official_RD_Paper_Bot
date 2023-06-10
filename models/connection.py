import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
creds = credentials.Certificate('../googleCredentials.json')

app = firebase_admin.initialize_app(creds)

db = firestore.client()


