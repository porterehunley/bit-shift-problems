import os
import argparse
from bitshift.commands.upload import upload
from bitshift.commands.generate import generate


def parse_arguments():
  parser = argparse.ArgumentParser(description='Bitshift CLI')
  subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

  # Upload command parser
  upload_parser = subparsers.add_parser('upload', help='Upload a target')
  upload_parser.add_argument(
    'target',
    type=lambda x: argparse.FileType('r')(os.path.abspath(x)),
    help='The problem target to upload'
  )

  # Generate command parser
  generate_parser = subparsers.add_parser('generate', help='Generate by name')
  generate_parser.add_argument(
    'title',
    type=str,
    help='The name for generation'
  )

  args = parser.parse_args()
  return args


def main():
  args = parse_arguments()

  if args.command == 'upload':
    upload(args.target)
  elif args.command == 'generate':
    generate(args.title)
  else:
    print('Invalid command')
