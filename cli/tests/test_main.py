import unittest
import json
from io import BytesIO
from flask import Request
from bitshift.cloud_functions.main import hello_http

class TestHelloHttpFunction(unittest.TestCase):
  def setUp(self):
    self.app = Request.environ = {}

  def test_hello_http_with_auxiliary(self):
    payload = {
      "header": "def multiply(a, b):",
      "truth": "def multiply_truth(a, b): return a * b",
      "input": {
        "a": ["int", "4"],
        "b": ["int", "5"]
      },
      "code": "def multiply(a, b):\n  helper = helper_function()\n  return a * b",
      "auxiliary": "def helper_function():\n  return 'Auxiliary function executed'"
    }
    
    payload_bytes = json.dumps(payload).encode('utf-8')
        
    environ = {
      'CONTENT_TYPE': 'application/json',
      'CONTENT_LENGTH': str(len(payload_bytes)),
      'wsgi.input': BytesIO(payload_bytes)
    }
    
    request = Request(environ)
    
    response = hello_http(request)
    
    self.assertIn("results", response)
    self.assertTrue(response["results"][0])
  
  def test_hello_http_valid_input(self):
    payload = {
      "header": "def add(a, b):",
      "truth": "def add_truth(a, b): return a + b",
      "input": {
        "a": ["int", "2"],
        "b": ["int", "3"]
      },
      "code": "def add(a, b):\n  return a + b"
    }
    
    payload_bytes = json.dumps(payload).encode('utf-8')
        
    environ = {
      'CONTENT_TYPE': 'application/json',
      'CONTENT_LENGTH': str(len(payload_bytes)),
      'wsgi.input': BytesIO(payload_bytes)
    }
    
    request = Request(environ)
    
    response = hello_http(request)
    
    self.assertIn("results", response)
    self.assertTrue(response["results"][0])

  def test_hello_http_invalid_input(self):
    payload = {
      "header": "def add(a, b):",
      "truth": "def add_truth(a, b): return a + b",
      "input": {
        "a": ["int", "2"],
        "b": ["int", "three"]
      }
      # 'code' key is missing
    }
    
    payload_bytes = json.dumps(payload).encode('utf-8')
        
    environ = {
      'CONTENT_TYPE': 'application/json',
      'CONTENT_LENGTH': str(len(payload_bytes)),
      'wsgi.input': BytesIO(payload_bytes)
    }
    
    request = Request(environ)
    
    response = hello_http(request)
    
    self.assertEqual(response[1], 400)
    self.assertEqual(response[0], 'Invalid input')

if __name__ == '__main__':
  unittest.main()

