#!/usr/bin/env python3

from argparse import ArgumentParser

if __name__ == '__main__':
    args_parser = ArgumentParser(description='test github-actions')
    args_parser.add_argument('--print', help='print this argument', default=None)
    args = args_parser.parse_args()
    if args.print is not None:
        print(args.print)
