import os
import argparse
from bitshift.commands.upload import upload


def parse_arguments():
  parser = argparse.ArgumentParser(description='Bitshift CLI')

  parser.add_argument('command', type=str, help='The action of the CLI')
  parser.add_argument(
    'target',
    type=lambda x: argparse.FileType('r')(os.path.abspath(x)),
    help='The problem target')

  args = parser.parse_args()

  return args


def main():
  args = parse_arguments()

  if args.command == 'upload':
    upload(args.target)
  else:
    print('Invalid command')
