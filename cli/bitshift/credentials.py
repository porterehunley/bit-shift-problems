import os

def get_db():
  try:
    import firebase_admin
    from firebase_admin import credentials, firestore
  except ImportError:
    msg = (
      "firebase_admin is not installed. "
      "To use admin functionality, please install the package as follows: "
      "pip install bitshift[admin]"
    )
    raise ImportError(msg)

  cred = credentials.Certificate(os.path.abspath("bitshift/secrets/bitshift-406020-firebase-adminsdk-wnzq8-1327c18c86.json"))
  app = firebase_admin.initialize_app(cred)
  db = firestore.client()
  return db

