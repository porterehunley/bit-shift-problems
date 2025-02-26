import functions_framework
from io import StringIO
import sys

def validate_input(input_type, input_value):
  if input_type in ["List[int]", "ListNode"]:
    if not input_value:
      return [] 

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

def add_loose_equals(code):
  loose_equals_def = '''
def loose_equals(a, b):
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if x != y:
                return False
        return True
    else:
        return a == b
'''

  return "\n" + loose_equals_def + "\n" + code

def construct_code_from_request(request_json, user_input):
  heading = request_json['header']
  truth_code = request_json['truth']
  function_name = heading.split()[1].split("(")[0]
  truth_name = function_name + "_truth"

  code = ""
  code += f"test={user_input}\n\n"
  if "auxiliary" in request_json:
    code += request_json["auxiliary"]
    code += "\n"

  if "input_transformer" in request_json:
    code += request_json["input_transformer"]
    code += "\n"
    input_transformer_name = request_json["input_transformer"].split("def ")[1].split("(")[0]
    code += f"\ntest={input_transformer_name}(**test)\n\n"

  code += add_loose_equals(code)
  code += "\n"

  code += request_json["code"]
  code += f"\noutput={function_name}(**test)\n\n"

  truth_code_modified = truth_code.replace(f"def {function_name}", f"def {truth_name}")
  code += truth_code_modified
  code += "\n"
  code += f"\nexpected={truth_name}(**test)\n"

  if "output_transformer" in request_json:
    code += "\n"
    code += request_json["output_transformer"]
    code += "\n"
    output_transformer_name = request_json["output_transformer"].split("def ")[1].split("(")[0]
    code += f"\nexpected={output_transformer_name}(expected)"
    code += f"\noutput={output_transformer_name}(output)"

  code += f"\nis_expected= loose_equals(output, expected)"
  code += "\nprint(is_expected)"
  
  return code

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
  if not request_json or 'code' not in request_json:
    return 'Invalid input', 400

  user_input = validate_inputs(request_json['input'])
  
  if 'input_validation' in request_json:
    input_validation_function = request_json['input_validation']
    input_validation_name = input_validation_function.split('def ')[1].split('(')[0]
    input_validation_code = input_validation_function
    input_validation_code += '\n'
    input_validation_code += f'test={user_input}'
    input_validation_code += '\n'
    input_validation_code += f'output={input_validation_name}(**test)'
    input_validation_code += '\n'
    input_validation_code += 'print(output)'

    namespace = {}
    buffer = StringIO()
    sys.stdout = buffer
    exec(input_validation_code, namespace)
    sys.stdout = sys.__stdout__
    validation_output = buffer.getvalue().strip()
    is_valid = validation_output == 'True'
    if not is_valid:
      return {"results": {
        "input_failed_validation": validation_output
      }}

  parse_errors = []
  for name, value in user_input.items():
    if value == False:
      parse_errors.append(name)

  if parse_errors:
    return {"results": {
      "parsing_errors": parse_errors
    }}

  results = []
  
  code = construct_code_from_request(request_json, user_input)

  namespace = {}
  buffer = StringIO()
  sys.stdout = buffer
  exec(code, namespace)
  sys.stdout = sys.__stdout__
  is_expected = buffer.getvalue().strip() == 'True'
  results.append(is_expected)

  return {"results": results}
