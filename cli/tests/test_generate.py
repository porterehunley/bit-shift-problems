import os
import tempfile
import shutil
import unittest

from bitshift.commands.generate import generate


class TestGenerateCommand(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_generate_creates_output_file(self):
        current_dir = os.path.dirname(__file__)
        fixture_path = os.path.join(current_dir, "test-problems", "valid_with_auxiliary.md")
        problem_file = os.path.join(self.test_dir, "valid_with_auxiliary.md")
        
        shutil.copy(fixture_path, problem_file)

        generate(problem_file)

        output_file = os.path.join(self.test_dir, "valid_with_auxiliary.py")
        self.assertTrue(os.path.exists(output_file), "Output file valid_with_auxiliary.py should be created.")

        with open(output_file, 'r', encoding='utf-8') as f:
            generated_code = f.read()

        snapshot_file = os.path.join(current_dir, "snapshots", "valid_with_auxiliary.py")
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            expected_code = f.read()

        self.assertEqual(generated_code, expected_code, "The generated code should match the expected snapshot.")


if __name__ == '__main__':
    unittest.main() 