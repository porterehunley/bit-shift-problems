import subprocess
import os
import sys

def deploy():
  """
  Deploys the main.py Cloud Function to Google Cloud Functions.
  """

  function_name = 'bitshift-test'
  region = 'northamerica-northeast1'
  runtime = 'python312'
  source_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cloud_functions'))

  # Construct the gcloud command
  cmd = [
    'gcloud', 'functions', 'deploy', function_name,
    '--runtime', runtime,
    '--trigger-http',
    '--allow-unauthenticated',
    '--source', source_directory,
    '--entry-point', 'hello_http',
    '--region', region
  ]

  try:
    print(f"Deploying function '{function_name}' to region '{region}'...")
    subprocess.run(cmd, check=True)
    print(f"Function '{function_name}' deployed successfully.")
  except subprocess.CalledProcessError as e:
    print(f"Error deploying function: {e}", file=sys.stderr)
    sys.exit(1)
