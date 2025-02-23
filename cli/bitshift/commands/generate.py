#!/usr/bin/env python3
import os
from pathlib import Path

from bitshift.commands.parse import parse_problem_file
from bitshift.cloud_functions.main import construct_code_from_request, validate_inputs


def format_test_input(parameters, test_input):
  """Format test input similar to run_problem_tests."""
  def convert_to_string(value):
    if isinstance(value, list):
      return ','.join(map(str, value))
    return str(value)

  formatted_input = {}
  for param in parameters:
    name, param_type = next(iter(param.items()))
    value = test_input.get(name)
    formatted_input[name] = [param_type, convert_to_string(value)]
  return formatted_input


def generate(problem_file_path):
  """Generate a Python solution file from a problem markdown file."""
  with open(problem_file_path, 'r', encoding='utf-8') as file:
    parsed_problem = parse_problem_file(file)

  parameters = parsed_problem.get('parameters', [])
  tests = parsed_problem.get('tests', {})

  test_input = {}
  if tests:
    first_test = next(iter(tests.values()))
    test_input = first_test.get('input', {})

  formatted_input = format_test_input(parameters, test_input)

  payload = {
    "header": parsed_problem.get('problem_header', ''),
    "truth": parsed_problem.get('code_sections', {}).get('truth', ''),
    "input": formatted_input,
    "code": parsed_problem.get('code_sections', {}).get('problem', '')
  }

  code_sections = parsed_problem.get('code_sections', {})
  if 'auxiliary' in code_sections:
    payload['auxiliary'] = code_sections['auxiliary']
  if 'input_validation' in code_sections:
    payload['input_validation'] = code_sections['input_validation']

  user_input = validate_inputs(payload['input'])

  generated_code = construct_code_from_request(payload, user_input)

  base_name = os.path.basename(problem_file_path)
  func_name = os.path.splitext(base_name)[0]
  output_file = f"{func_name}.py"
  with open(output_file, 'w', encoding='utf-8') as out_file:
    out_file.write(generated_code)

  print(f"Generated code written to {output_file}")