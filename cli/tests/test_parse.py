import unittest
from pathlib import Path
from bitshift.commands.parse import parse_problem_file

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
          "problem": "def add(a: int, b: int) -> int:\n  return a + b\n",
          "truth": "def add(a: int, b: int) -> int:\n  return a + b\n",
        },
        "problem_header": "def add(a: int, b: int) -> int:",
        "parameters": [
          {"a": "int"},
          {"b": "int"}
        ],
        "examples": {
          "Test1": [
            {"a": 1, "b": 2},
            {"result": 3}
          ]
        },
        "tests": {
          "Breaking Input": [
            {"a": 1, "b": 2},
            {"is_breaking": True}
          ],
          "Non-Breaking Input": [
            {"a": 0, "b": 0},
            {"is_breaking": False}
          ]
        }
      }
      result = parse_problem_file(problem_file)

      self.assertEqual(result['header_info'], expected_output['header_info'])
      self.assertEqual(result['title'], expected_output['title'])
      self.assertEqual(result['description'], expected_output['description'])
      self.assertEqual(result['code_sections'], expected_output['code_sections'])
      self.assertEqual(result['problem_header'], expected_output['problem_header'])
      self.assertEqual(result['parameters'], expected_output['parameters'])
      self.assertEqual(result['examples'], expected_output['examples'])
      self.assertEqual(result['tests'], expected_output['tests'])

  def test_missing_header(self):
    with self.read_markdown("missing_header.md") as problem_file:
      with self.assertRaises(ValueError) as context:
        parse_problem_file(problem_file)
      self.assertIn("Problem must have a header at the top of file", str(context.exception))

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

  def test_invalid_examples_section(self):
    with self.read_markdown("invalid_examples_section.md") as problem_file:
      with self.assertRaises(ValueError) as context:
        parse_problem_file(problem_file)

      self.assertIn("Example name invalid, not-bolded, or missing", str(context.exception))

  def test_auxiliary_section(self):
    with self.read_markdown("valid_with_auxiliary.md") as problem_file:
      result = parse_problem_file(problem_file)
      expected_output = {
        "header_info": {"header_key": "header_value"},
        "title": "Sample Problem",
        "description": "This is a description of the sample problem.",
        "code_sections": {
          "auxiliary": "def helper(a: int) -> int:\n  return a * 2\n",
          "problem": "def add(a: int, b: int) -> int:\n  return a + b\n",
          "truth": "def add(a: int, b: int) -> int:\n  return a + b\n"
        },
        "problem_header": "def add(a: int, b: int) -> int:",
        "parameters": [
          {"a": "int"},
          {"b": "int"}
        ],
        "examples": {
          "Test1": [
            {"a": 1, "b": 2},
            {"result": 3}
          ]
        }
      }

      self.assertEqual(result['header_info'], expected_output['header_info'])
      self.assertEqual(result['title'], expected_output['title'])
      self.assertEqual(result['description'], expected_output['description'])
      self.assertEqual(result['code_sections'], expected_output['code_sections'])
      self.assertEqual(result['problem_header'], expected_output['problem_header'])
      self.assertEqual(result['parameters'], expected_output['parameters'])
      self.assertEqual(result['examples'], expected_output['examples'])


if __name__ == '__main__':
  unittest.main()