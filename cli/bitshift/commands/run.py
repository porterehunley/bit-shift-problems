#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from io import BytesIO

from flask import Request
from bitshift.commands.parse import parse_problem_file
from bitshift.cloud_functions.main import hello_http


def convert_to_string(value):
    if isinstance(value, list):
        return ','.join(map(str, value))
    return str(value)


def format_test_input(parameters, test_input):
    formatted_input = {}
    for param in parameters:
        # Each param is a dict with one key-value pair
        name, param_type = next(iter(param.items()))
        value = test_input.get(name)
        formatted_input[name] = [param_type, convert_to_string(value)]
    return formatted_input


def run_problem_tests(problem_directory):
    problem_directory = os.path.abspath(problem_directory)
    print(f"Testing problems in {problem_directory}")
    problem_files = list(Path(problem_directory).glob('*.md'))
    print(f"Found {len(problem_files)} problem files")
    failures = 0
    
    for problem_file in problem_files:
        with problem_file.open('r', encoding='utf-8') as file:
            parsed_problem = parse_problem_file(file)
        title = parsed_problem.get('title', 'Untitled Problem')
        tests = parsed_problem.get('tests', {})
        for test_name, test_vals in tests.items():
            test_input = test_vals.get('input', {})
            expected_output = test_vals.get('output', {}).get('is_breaking', False)
            formatted_input = format_test_input(parsed_problem.get('parameters', []), test_input)
            
            payload = {
                "header": parsed_problem.get('problem_header', ''),
                "truth": parsed_problem.get('code_sections', {}).get('truth', ''),
                "input": formatted_input,
                "code": parsed_problem.get('code_sections', {}).get('problem', '')
            }
            if 'auxiliary' in parsed_problem.get('code_sections', {}):
                payload['auxiliary'] = parsed_problem.get('code_sections', {}).get('auxiliary')

            if 'input_validation' in parsed_problem.get('code_sections', {}):
                payload['input_validation'] = parsed_problem.get('code_sections', {}).get('input_validation')
            
            payload_bytes = json.dumps(payload).encode('utf-8')
            environ = {
                'CONTENT_TYPE': 'application/json',
                'CONTENT_LENGTH': str(len(payload_bytes)),
                'wsgi.input': BytesIO(payload_bytes)
            }
            
            request = Request(environ)
            response = hello_http(request)
            result = response['results'][0]
            
            if result != (not expected_output):
                print(f"Failed {title} - {test_name}: expected {not expected_output}, got {result}")
                failures += 1
            else:
                print(f"Passed {title} - {test_name}")
    
    if failures:
        print(f"{failures} test(s) failed.")
        exit(1)
    else:
        print("All tests passed!")
        exit(0)


def main():
    parser = argparse.ArgumentParser(description="Run problems from a given directory")
    parser.add_argument("directory", help="Directory containing problem .md files")
    args = parser.parse_args()
    run_problem_tests(args.directory)


if __name__ == '__main__':
    main()
