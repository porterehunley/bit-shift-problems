# BitShift Problems
This is the problem repository for BitShift, an app for solving coding puzzles.

## How to Add Your Own Problem

1. Generate your problem template:
   Run: `bitshift generate problem_title`
2. Fill in the Template:
   Edit the generated file to include a full problem statement with constraints, input/output specifications, and examples.
3. Add Tests:
   Create test cases corresponding to your problem to verify its correctness.
4. Validate with Parse:
   Run: `bitshift parse <path_to_problem_file>` to ensure your problem file is correctly formatted and can be parsed.
5. Run Tests:
   Run: `bitshift run <directory_with_problem_files>` to ensure that all tests pass.
6. Create a Pull Request (PR):
   Once everything is working as expected, submit your PR with the new problem for review.


## CLI Commands

**generate**

`bitshift generate <title>`
- Generates a new problem from a template.
- Takes a title for the new problem.

**parse**

`bitshift parse <problem_file>`
- Parses a given problem file and outputs its JSON representation.
- Useful for validating the problem file format.

**run**

`bitshift run <directory>`
- Executes tests for all problems in the specified directory.
- Useful for ensuring that your problems' tests pass correctly.

**test**

`bitshift test`
- Runs all CLI unit tests to verify the functionality of the CLI commands.
- This tests any contributions made to the CLI.
