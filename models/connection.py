import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import config

# Use a service account.
creds = credentials.Certificate('googleCredentials.json')

app = firebase_admin.initialize_app(creds, {
    'storageBucket': config.STORAGE_BUCKET
})

db = firestore.client()
bucket = storage.bucket()
