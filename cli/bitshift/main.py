import os
import argparse
from bitshift.commands.upload import upload
from bitshift.commands.generate import generate
from bitshift.commands.test import run_tests  # Import the run_tests function
from bitshift.commands.deploy import deploy  # Import the run_tests function
from bitshift.commands.parse import parse_problem_file
from bitshift.commands.run import run_problem_tests


def parse_arguments():
  parser = argparse.ArgumentParser(description='Bitshift CLI')
  subparsers = parser.add_subparsers(dest='command', help='Available commands')

  upload_parser = subparsers.add_parser('upload', help='Upload a problem filed to the database (admin)')
  upload_parser.add_argument(
    'target',
    type=lambda x: argparse.FileType('r')(os.path.abspath(x)),
    help='The problem target to upload'
  )

  generate_parser = subparsers.add_parser('generate', help='Generate a new problem from a template')
  generate_parser.add_argument(
    'title',
    type=str,
    help='The name for generation'
  )
  
  _ = subparsers.add_parser('test', help='Run all CLI unit tests')
  _ = subparsers.add_parser('deploy', help='Deploy the running cloud function (admin)')
  run_parser = subparsers.add_parser('run', help='Run problems from a given directory')
  run_parser.add_argument('directory', type=str, help='Directory containing problem .md files')
  parse_parser = subparsers.add_parser('parse', help='Try and parse a problem file and output its parsed JSON')
  parse_parser.add_argument('problem_file', type=lambda x: argparse.FileType('r')(os.path.abspath(x)), help='The problem file to parse')

  args = parser.parse_args()
  if not args.command:
      parser.print_help()
      exit(0)
  return args


def main():
  args = parse_arguments()

  if args.command == 'upload':
    upload(args.target)
  elif args.command == 'generate':
    generate(args.title)
  elif args.command == 'parse':
    try:
      result = parse_problem_file(args.problem_file)
      import json
      print(json.dumps(result, indent=2))
      print("Successfully parsed problem file")
    except Exception as e:
      print("Error while parsing problem file:", e)

  elif args.command == 'test':
    run_tests()
  elif args.command == 'deploy':
    deploy()
  elif args.command == 'run':
    run_problem_tests(args.directory)
  else:
    print('Invalid command')


if __name__ == '__main__':
  main()
