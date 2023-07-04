#!/usr/bin/env python3
import optparse
import sys
import importlib

from regex_parser import parse_regex

usage = "%prog [regex] [file]"

opt_parser = optparse.OptionParser(usage=usage)
opt_parser.add_option("-m", "--module", dest="module", action="store_true",
                      help="read the regular expression from a Python module")
opt_parser.add_option("-n", "--naive", dest="naive", action="store_true",
                      help="use the naive implementation to match against the regular expression")
opts, args = opt_parser.parse_args()

if len(args) < 1:
    opt_parser.print_help()
    exit(1)
elif len(args) > 2:
    print("ERROR: Too many arguments", file=sys.stderr)
    exit(1)
else:
    regex_arg = args[0]
    if opts.module:
        regex_module = importlib.import_module(regex_arg)
        regex = regex_module.__regex__
    else:
        regex = parse_regex(regex_arg)

    with open(args[1]) if len(args) == 2 else sys.stdin as input_file:
        for line in input_file:
            if opts.naive:
                matched = regex.naive_match(line.strip("\n"))
            else:
                matched = regex.match(line.strip("\n"))

            if matched:
                print(line, end="")
