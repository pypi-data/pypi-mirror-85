#!/usr/bin/env python
from argparse import ArgumentParser

from jamd import jamd_viewer


def parse_arguments():
    arguments = ArgumentParser()
    arguments.add_argument('path', help='Markdown file to be opened')

    return arguments.parse_args()


def main():
    arguments = parse_arguments()
    jamd_viewer.run(arguments.path)


if __name__ == '__main__':
    main()
