import os
import argparse
from bitshift.commands.upload import upload
from bitshift.commands.generate import generate
from bitshift.commands.test import run_tests  # Import the run_tests function
from bitshift.commands.deploy import deploy  # Import the run_tests function


def parse_arguments():
  parser = argparse.ArgumentParser(description='Bitshift CLI')
  subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

  upload_parser = subparsers.add_parser('upload', help='Upload a target')
  upload_parser.add_argument(
    'target',
    type=lambda x: argparse.FileType('r')(os.path.abspath(x)),
    help='The problem target to upload'
  )

  generate_parser = subparsers.add_parser('generate', help='Generate by name')
  generate_parser.add_argument(
    'title',
    type=str,
    help='The name for generation'
  )
  
  _ = subparsers.add_parser('test', help='Run all unit tests')
  _ = subparsers.add_parser('deploy', help='Deploy the cloud function')

  args = parser.parse_args()
  return args


def main():
  args = parse_arguments()

  if args.command == 'upload':
    upload(args.target)
  elif args.command == 'generate':
    generate(args.title)
  elif args.command == 'test':
    run_tests()
  elif args.command == 'deploy':
    deploy()
  else:
    print('Invalid command')


if __name__ == '__main__':
  main()
