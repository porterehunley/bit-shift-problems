import unittest
import tempfile
import shutil
import os
from pathlib import Path
from unittest import mock

from bitshift.commands.generate import generate, TEMPLATE_PATH

class TestGenerateCommand(unittest.TestCase):
  def setUp(self):
    # Create a temporary directory to simulate the project structure
    self.test_dir = tempfile.mkdtemp()
    
    # Paths
    self.templates_dir = Path(self.test_dir) / "cli" / "bitshift" / "templates"
    self.problems_dir = Path(self.test_dir) / "problems"
    self.templates_dir.mkdir(parents=True, exist_ok=True)
    self.problems_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a mock problem_template.md
    self.template_path = self.templates_dir / "problem_template.md"
    with open(self.template_path, 'w', encoding='utf-8') as f:
      f.write("# {{title}}\n\nProblem description goes here.")

    # Patch TEMPLATE_PATH to point to the mock template
    self.patcher = mock.patch('bitshift.commands.generate.TEMPLATE_PATH', self.template_path)
    self.patcher.start()
    
    # Change the current working directory to the temporary directory
    self.original_cwd = os.getcwd()
    os.chdir(self.test_dir)

  def tearDown(self):
    # Stop patching TEMPLATE_PATH
    self.patcher.stop()
    
    # Change back to the original working directory
    os.chdir(self.original_cwd)
    
    # Remove the temporary directory and all its contents
    shutil.rmtree(self.test_dir)

  def test_generate_creates_markdown_file_with_correct_content(self):
    # Define the input name
    name = "Sample Problem"

    # Expected slug and file path
    expected_slug = "sample-problem"
    expected_file = self.problems_dir / f"{expected_slug}.md"

    # Call the generate function
    generate(name)

    # Check if the file was created
    self.assertTrue(expected_file.exists(), f"The file {expected_file} was not created.")

    # Read the content of the created file
    with open(expected_file, 'r', encoding='utf-8') as f:
      content = f.read()

    # Check if the {{title}} placeholder was replaced correctly
    expected_content = f"# {name}\n\nProblem description goes here."
    self.assertEqual(content, expected_content, "The content of the markdown file is incorrect.")

  def test_generate_creates_problems_directory_if_not_exists(self):
    # Remove the problems directory
    shutil.rmtree(self.problems_dir)
    self.assertFalse(self.problems_dir.exists(), "Problems directory still exists.")

    # Define the input name
    name = "Another Sample Problem"

    # Call the generate function
    generate(name)

    # Check if the problems directory was recreated
    self.assertTrue(self.problems_dir.exists(), "Problems directory was not created.")

    # Check if the file was created
    expected_slug = "another-sample-problem"
    expected_file = self.problems_dir / f"{expected_slug}.md"
    self.assertTrue(expected_file.exists(), f"The file {expected_file} was not created.")

  def test_slugify_generates_correct_slug(self):
    # Assuming slugify is a separate function, we can test it directly
    from bitshift.commands.generate import slugify

    test_cases = {
      "Sample Problem": "sample-problem",
      "Another_Sample! Problem": "another_sample-problem",
      "Complex Title: With # Characters & Symbols": "complex-title-with-characters-symbols"
    }

    for input_title, expected_slug in test_cases.items():
      self.assertEqual(slugify(input_title), expected_slug, f"Slugify failed for input: {input_title}")

if __name__ == '__main__':
  unittest.main()
