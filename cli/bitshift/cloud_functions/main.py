import functions_framework
from typing import List
from io import StringIO
import sys

def validate_input(input_type, input_value):
  if input_type == "List[int]":
    try:
      values = list(map(int, input_value.split(',')))
      return values

    except ValueError:
      return False
    
  elif input_type == "str":
    if isinstance(input_value, str):
      return input_value
    else:
      return False

  elif input_type == "int":
    try:
      return int(input_value)
  
    except ValueError:
      return False

  else:
    return False


def validate_inputs(params):
  results = {}
  for name, input_vector in params.items():
    input_type, input_value = input_vector
    result = validate_input(input_type, input_value)
    results[name] = result
  
  return results


@functions_framework.http
def hello_http(request):
  """HTTP Cloud Function.
  Args:
    request (flask.Request): The request object.
    <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
  Returns:
    The response text, or any set of values that can be turned into a
    Response object using `make_response`
    <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
  """
  request_json = request.get_json()
  print(request_json)
  if not request_json or 'code' not in request_json:
    return 'Invalid input', 400

  heading = request_json['header']
  truth_code = request_json['truth']
  user_input = validate_inputs(request_json['input'])

  parse_errors = []
  for name, value in user_input.items():
    if value == False:
      parse_errors.append(name)

  if parse_errors:
    return {"results": {
      "parsing_errors": parse_errors
    }}

  function_name = heading.split()[1].split("(")[0]
  truth_name = function_name+"_truth"

  results = []

  code = ''
  if ('auxiliary' in request_json):
    print('Adding Auxiliary')
    print(request_json['auxiliary'])
    code += request_json['auxiliary']
    code += '\n'
  
  code += request_json['code']
  code += f'\ntest={user_input}'
  code += f'\noutput={function_name}(**test)'
  code += '\n'
  code += truth_code
  code += f'\nexpected={truth_name}(**test)'
  code += f'\nis_expected= output == expected'
  code += '\nprint(is_expected)'

  print("Executing Code")
  print(code)

  namespace = {} # Create a new namespace for the code to run in

  buffer = StringIO()
  sys.stdout = buffer
  exec(code, namespace) # Printed code goes to buffer 
  sys.stdout = sys.__stdout__
  is_expected = buffer.getvalue().strip() == 'True' # Print the captured output```
  results.append(is_expected)

  return {"results": results}
