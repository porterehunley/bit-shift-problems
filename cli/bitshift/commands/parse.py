import re
import json
import yaml
from typing import List, Tuple
from mistletoe import Document, ast_renderer

def parse_parameters(header: str) -> List[Tuple[str, str]]:
  pattern = r'\((.*?)\)'
  match = re.search(pattern, header)
  if not match:
    raise ValueError("Invalid function header format")
  
  params_str = match.group(1)
  params = params_str.split(',')
  parsed_params = []
  
  for param in params:
    name, param_type = param.split(':')
    parsed_params.append({name.strip(): param_type.strip()})
  
  return parsed_params

def is_code_section(node):
  return (node['type'] == 'Paragraph' and 
      node['children'][0]['type'] == 'Strong' and
      node['children'][0]['children'][0]['content'] in ['Problem', 'Truth', 'Auxiliary'])

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

def parse_problem_file(problem_file):
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
  if not header_info:
    raise ValueError("Problem must have a header at the top of file")

  doc = Document(problem_file)
  renderer = ast_renderer.ASTRenderer()
  string = renderer.render(token=doc)
  ast = json.loads(string)

  if not ast['children'] or ast['children'][0].get('type', None) != 'Heading':
    raise ValueError("Problem must have title")
  
  title = ast['children'][0]['children'][0]['content']
  print(f'Title: {title}')

  if len(ast['children']) < 2 or ast['children'][1].get('type', None) != 'Paragraph':
    raise ValueError("Problem must have description following header")
  
  description = ast['children'][1]['children'][0]['content']
  print(f'Description: {description}')

  if (len(ast['children']) < 3 or
    ast['children'][2]['type'] != 'Heading' or
    ast['children'][2]['level'] != 2 or 
    ast['children'][2]['children'][0]['content'] != 'Code'):
    raise ValueError("Problem must have a valid Code section following description")  

  child_idx = 3
  code_sections = {}
  problem_header = None

  # Auxiliary section
  if child_idx < len(ast['children']) and is_code_section(ast['children'][child_idx]):
    code_section_type = ast['children'][child_idx]['children'][0]['children'][0]['content']
    if code_section_type == 'Auxiliary':
      if validate_code_section(ast['children'][child_idx+1]):
        code = ast['children'][child_idx+1]['children'][0]['content']
        code_sections['auxiliary'] = code
        child_idx += 2
      else:
        raise ValueError("Invalid Auxiliary code section")

  # Problem section
  if child_idx < len(ast['children']) and is_code_section(ast['children'][child_idx]):
    code_section_type = ast['children'][child_idx]['children'][0]['children'][0]['content']
    if code_section_type != 'Problem':
      raise ValueError("Problem must have a Problem code sub-section followed by Truth")

    if validate_code_section(ast['children'][child_idx+1]):
      code = ast['children'][child_idx+1]['children'][0]['content']
      code_sections['problem'] = code
      problem_header = code.split('\n')[0]

  if not problem_header:
    raise ValueError("Error parsing problem function header")
  
  child_idx += 2

  # Truth section
  if child_idx < len(ast['children']) and is_code_section(ast['children'][child_idx]):
    code_section_type = ast['children'][child_idx]['children'][0]['children'][0]['content']
    if code_section_type != 'Truth':
      raise ValueError("Problem must have a Problem code sub-section followed by Truth")

    if validate_code_section(ast['children'][child_idx+1]):
      code = ast['children'][child_idx+1]['children'][0]['content']
      code_sections['truth'] = code

  if 'truth' not in code_sections.keys():
    raise ValueError("Failed to parse truth section")

  child_idx += 2

  print('Header', problem_header)

  parameters = parse_parameters(problem_header)
  print('Parameters:', parameters)

  print('Code', code_sections)

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
      raise ValueError(f'Missing or invalid output section for test {test_name}')
    
    test_output = json.loads(ast['children'][child_idx+2]['children'][0]['content'])

    tests[test_name] = [test_input, test_output]

    child_idx += 3

  print('tests', tests)
  if not tests:
    raise ValueError('Problem must have at least one test')

  return {
    "header_info": header_info,
    "title": title,
    "description": description,
    "code_sections": code_sections,
    "problem_header": problem_header,
    "parameters": parameters,
    "tests": tests
  }
