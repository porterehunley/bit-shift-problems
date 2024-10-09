import unittest
import sys
from pathlib import Path

def run_tests():
  """
  Discover and run all unit tests in the 'cli/tests' directory.
  """
  test_dir = Path(__file__).resolve().parent.parent.parent / "tests"
  
  if not test_dir.exists():
    print(f"Test directory {test_dir} does not exist.", file=sys.stderr)
    sys.exit(1)
  
  loader = unittest.TestLoader()
  suite = loader.discover(start_dir=test_dir, pattern="test_*.py")
  
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)
  
  if result.wasSuccessful():
    sys.exit(0)
  else:
    sys.exit(1)
