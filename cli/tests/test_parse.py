import unittest
import json
from pathlib import Path
from cli.bitshift.commands.parse import parse_problem_file

class TestParseProblemFile(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None  # To display full diff when tests fail
    self.data_dir = Path(__file__).parent / "test-problems"

  def read_markdown(self, filename):
    file_path = self.data_dir / filename
    return file_path.open('r', encoding='utf-8')

  def test_valid_markdown(self):
    with self.read_markdown("valid_markdown.md") as problem_file:
      expected_output = {
        "header_info": {"header_key": "header_value"},
        "title": "Sample Problem",
        "description": "This is a description of the sample problem.",
        "code_sections": {
          "problem": "def add(a: int, b: int) -> int:\n  return a + b",
          "truth": "def add(a: int, b: int) -> int:\n  return a + b",
        },
        "problem_header": "def add(a: int, b: int) -> int:",
        "parameters": [
          {"a": "int"},
          {"b": "int"}
        ],
        "tests": {
          "Test1": [
            {"a": 1, "b": 2},
            {"result": 3}
          ]
        }
      }
      result = parse_problem_file(problem_file)
      self.assertEqual(result, expected_output)

  def test_missing_header(self):
    with self.read_markdown("missing_header.md") as problem_file:
      with self.assertRaises(ValueError) as context:
        parse_problem_file(problem_file)
      self.assertIn("Problem must have the header at the top of file", str(context.exception))

  def test_invalid_code_language(self):
    with self.read_markdown("invalid_code_language.md") as problem_file:
      with self.assertRaises(ValueError) as context:
        parse_problem_file(problem_file)
      self.assertIn("Code must be labeled as Python", str(context.exception))

  def test_missing_truth_section(self):
    with self.read_markdown("missing_truth_section.md") as problem_file:
      with self.assertRaises(ValueError) as context:
        parse_problem_file(problem_file)
      self.assertIn("Failed to parse truth section", str(context.exception))

  def test_invalid_test_section(self):
    with self.read_markdown("invalid_test_section.md") as problem_file:
      with self.assertRaises(ValueError) as context:
        parse_problem_file(problem_file)
      self.assertIn("Test name invalid, not-bolded, or missing", str(context.exception))

  def test_multiple_tests(self):
    with self.read_markdown("multiple_tests.md") as problem_file:
      expected_output = {
        "header_info": {"header_key": "header_value"},
        "title": "Complex Problem",
        "description": "Detailed description here.",
        "code_sections": {
          "problem": "def multiply(a: int, b: int) -> int:\n  return a * b",
          "truth": '{"result": 6}'
        },
        "problem_header": "def multiply(a: int, b: int) -> int:",
        "parameters": [
          {"a": "int"},
          {"b": "int"}
        ],
        "tests": {
          "Test1": [
            {"a": 2, "b": 3},
            {"result": 6}
          ],
          "Test2": [
            {"a": 4, "b": 5},
            {"result": 20}
          ]
        }
      }
      result = parse_problem_file(problem_file)
      self.assertEqual(result, expected_output)

if __name__ == '__main__':
  unittest.main()