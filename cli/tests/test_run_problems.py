import unittest
import json
from io import BytesIO
from pathlib import Path
import os
from flask import Request
from bitshift.commands.parse import parse_problem_file
from bitshift.cloud_functions.main import hello_http

class TestRunProblems(unittest.TestCase):
  def setUp(self):
    self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'problems'))
    self.parser = parse_problem_file

  def convert_to_string(self, value):
    if isinstance(value, list):
      return ','.join(map(str, value))
    return str(value)

  def format_test_input(self, parameters, test_input):
    formatted_input = {}
    for param in parameters:
      name, param_type = next(iter(param.items()))
      value = test_input.get(name)
      formatted_input[name] = [param_type, self.convert_to_string(value)]
    return formatted_input

  def test_run_all_problems(self):
    print(f'Testing problems in {self.directory}')
    problem_files = list(Path(self.directory).glob('*.md'))
    print(f'Found {len(list(problem_files))} problem files')
    
    for problem_file in problem_files:
      with problem_file.open('r', encoding='utf-8') as file:
        parsed_problem = self.parser(file)
      
      title = parsed_problem['title']
      tests = parsed_problem['tests']
      
      for test_name, test_vals in tests.items():
        test_input = test_vals['input']
        expected_output = test_vals['output']['is_breaking']
        formatted_input = self.format_test_input(parsed_problem['parameters'], test_input)
        with self.subTest(problem=title, test=test_name):
          payload = {
            "header": parsed_problem['problem_header'],
            "truth": parsed_problem['code_sections']['truth'],
            "input": formatted_input,
            "code": parsed_problem['code_sections']['problem']
          }
          
          if 'auxiliary' in parsed_problem['code_sections']:
            payload['auxiliary'] = parsed_problem['code_sections']['auxiliary']
          
          payload_bytes = json.dumps(payload).encode('utf-8')
          
          environ = {
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': str(len(payload_bytes)),
            'wsgi.input': BytesIO(payload_bytes)
          }
          
          request = Request(environ)
          
          response = hello_http(request)
          result = response['results'][0]
          
          self.assertEqual(result, expected_output, f"Failed {title} - {test_name}")

if __name__ == '__main__':
  unittest.main()

