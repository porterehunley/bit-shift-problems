import os
import yaml
import json
import random

from mistletoe import Document, ast_renderer
from bitshift.credentials import app, db
from firebase_admin import firestore 
from typing import List, Tuple

from .parse import parse_problem_file  # Import the parsing function

def upload(problem_file):
  # Parse the problem file using the parse_problem_file function
  parsed_data = parse_problem_file(problem_file)

  header_info = parsed_data['header_info']
  title = parsed_data['title']
  description = parsed_data['description']
  code_sections = parsed_data['code_sections']
  problem_header = parsed_data['problem_header']
  parameters = parsed_data['parameters']
  examples = parsed_data['examples']
  tests = parsed_data['tests']

  title_postfixes = random.sample(['1', '2'], 2)
  title_one = title + '-' + title_postfixes[0]

  doc_ref = db.collection('problems').document(f'{title_one.replace(" ","_")}')
  upload_data = {
    "code": code_sections['problem'],
    "truth": code_sections['truth'],
    "description": description,
    "header": problem_header,
    "tags": header_info['tags'],
    "difficulty": header_info['difficulty'],
    "title": title_one,
    "parameters": parameters
  }

  if 'auxiliary' in code_sections:
    upload_data["auxiliary"] = code_sections['auxiliary']

  doc_ref.set(upload_data)

  for example_name in examples.keys():
    examples_ref = db.collection('problems').document(f'{title_one.replace(" ","_")}').collection('examples').document(example_name)
    examples_ref.set({
      "input": examples[example_name][0],
      "output": examples[example_name][1]
    })

  print("Examples uploaded")

  variant_title = f"{title}-{title_postfixes[-1]}"
  variant_doc_ref = db.collection('problems').document(f'{variant_title.replace(" ","_")}')
  variant_upload_data = {
    "code": code_sections['truth'],
    "truth": code_sections['truth'],
    "is_truth": True,
    "description": description,
    "header": problem_header,
    "tags": header_info['tags'],
    "difficulty": header_info['difficulty'],
    "title": variant_title,
    "parameters": parameters
  }

  if 'auxiliary' in code_sections:
    variant_upload_data["auxiliary"] = code_sections['auxiliary']

  variant_doc_ref.set(variant_upload_data)

  for example_name in examples.keys():
    examples_ref = db.collection('problems').document(f'{variant_title.replace(" ","_")}').collection('examples').document(example_name)
    examples_ref.set({
      "input": examples[example_name][0],
      "output": examples[example_name][1]
    })

  print("Examples uploaded")
  print("Truth uploaded")
