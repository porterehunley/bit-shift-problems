import firebase_admin
from firebase_admin import credentials, firestore
import os


cred = credentials.Certificate(os.path.abspath("bitshift/secrets/bitshift-406020-firebase-adminsdk-wnzq8-1327c18c86.json"))
app = firebase_admin.initialize_app(cred)
db = firestore.client()
