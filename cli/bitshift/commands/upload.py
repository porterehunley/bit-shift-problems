import os
from bitshift.credentials import app
from firebase_admin import storage


def upload(problem_file):
  bucket = storage.bucket(app=app, name='staging.bitshift-406020.appspot.com')

  filename = os.path.basename(problem_file.name)

  blob = bucket.blob(filename)
  blob.upload_from_file(problem_file)
