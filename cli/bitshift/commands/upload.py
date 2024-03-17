import os
import yaml
import json

from mistletoe import Document, ast_renderer
from bitshift.credentials import app, db
from firebase_admin import firestore 


def is_variant_section(node):
  return (node['type'] == 'Paragraph' and 
          node['children'][0]['type'] == 'Strong' and
          node['children'][0]['children'][0]['content'] in ['Debugging', 'Missing Logic'])


def validate_code_section(node):
  if node['type'] != 'CodeFence':
    raise ValueError('Variant declaration must be followed by code')
  
  if node['language'] != 'python':
    raise ValueError('Code must be labeled as Python')
  
  return True


def validate_input_section(node):
  validate_code_section(node)

  code_str = node['children'][0]['content']
  print('-----')
  print(code_str)
  function_input = json.loads(code_str)

  return function_input


def upload(problem_file):
  client = firestore.client(app=app)

  yaml_content = ""
  separator_count = 0
  for line in problem_file:
    if line.strip() == '---':
      separator_count += 1
    else:
      yaml_content += line

    if separator_count == 2:
      break

  header_info = yaml.safe_load(yaml_content)
  doc = Document(problem_file)
  renderer = ast_renderer.ASTRenderer()
  string = renderer.render(token=doc)
  ast = json.loads(string)

  if not ast['children'] or ast['children'][0].get('type', None) != 'Heading':
    raise ValueError("Problem must have the header at the top of file")
  
  title = ast['children'][0]['children'][0]['content']
  print(f'Title: {title}')

  if len(ast['children']) < 2 or ast['children'][1].get('type', None) != 'Paragraph':
    raise ValueError("Problem must have description following header")
  
  description = ast['children'][1]['children'][0]['content']
  print(f'Description: {description}')

  if (len(ast['children']) < 3 or
    ast['children'][2]['type'] != 'Heading' or
    ast['children'][2]['level'] != 2 or 
    ast['children'][2]['children'][0]['content'] != 'Variants'):
    raise ValueError("Problem must have a valid variants section follwing description")  
  
  child_idx = 3
  variants = {}
  problem_header = None
  while child_idx < len(ast['children']) and is_variant_section(ast['children'][child_idx]):
    variant_type = ast['children'][child_idx]['children'][0]['children'][0]['content']
    if validate_code_section(ast['children'][child_idx+1]): # Will raise error
      code = ast['children'][child_idx+1]['children'][0]['content']
      variants[variant_type] = code
      problem_header = code.split('\n')[0]

    child_idx += 2

  print('Header', problem_header)
  print('Variants', variants)

  # Now do the tests section
  if (child_idx >= len(ast['children']) or
    ast['children'][child_idx]['type'] != 'Heading' or 
    ast['children'][child_idx]['level'] != 2 or 
    ast['children'][child_idx]['children'][0]['content'] != 'Tests'):
    raise ValueError('Problem must have a valid Tests section following variants')
  
  child_idx += 1

  tests = {}
  while child_idx < len(ast['children']): # Final part of problem
    if ast['children'][child_idx]['children'][0]['type'] != 'Strong':
      raise ValueError('Test name invalid, not-bolded, or missing')
    
    test_name = ast['children'][child_idx]['children'][0]['children'][0]['content']
    if child_idx+1 >= len(ast['children']) or not validate_input_section(ast['children'][child_idx+1]):
      raise ValueError(f'Missing or invalid input section for test {test_name}')
    
    test_input = json.loads(ast['children'][child_idx+1]['children'][0]['content'])

    if child_idx+2 >= len(ast['children']) or not validate_code_section(ast['children'][child_idx+2]):
      raise ValueError(f'Missing or invalud output section for test {test_name}')
    
    test_output = json.loads(ast['children'][child_idx+2]['children'][0]['content'])

    tests[test_name] = [test_input, test_output]

    child_idx += 3

  print('tests', tests)

  for variant, code in variants.items():
    doc_ref = db.collection('problems').document(f'{title.replace(" ","_")}--{variant}')
    doc_ref.set({
      "code": code,
      "description": description,
      "header": problem_header,
      "tags": header_info['tags'],
      "difficulty": header_info['difficulty'],
      "title": title,
      "type": variant
    })

    for test_name in tests.keys():
      tets_ref = db.collection('problems').document(f'{title.replace(" ","_")}--{variant}').collection('tests').document(test_name)
      tets_ref.set({
        "input": tests[test_name][0],
        "output": tests[test_name][1]
      })

  print("Tests uploaded")



