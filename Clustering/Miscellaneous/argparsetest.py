#!/usr/bin/python3

import argparse
parser = argparse.ArgumentParser()

# add an argument
parser.add_argument("-a", "--add", nargs="+", help="Creates a local Linux Account")

args = parser.parse_args() # reads in argument

if args.add:
    for u in args.add:
        print("Creating user " + u)
