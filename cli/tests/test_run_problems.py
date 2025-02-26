import unittest
import os
import sys
from pathlib import Path
from bitshift.commands.run import run_problem_tests

class TestRunProblems(unittest.TestCase):
  def setUp(self):
    self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'problems'))

  def test_run_all_problems(self):
    try:
      run_problem_tests(self.directory)
      exit_code = 0
    except SystemExit as e:
      exit_code = e.code

    self.assertEqual(exit_code, 0, "Some tests failed")

if __name__ == '__main__':
  unittest.main()

