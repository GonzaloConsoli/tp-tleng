#!/usr/bin/env python3
from os.path import dirname, basename, isfile, join
import glob
import optparse
import sys
import importlib
import subprocess
from timeit import default_timer as timer
from difflib import unified_diff


def bold(text):
    return f"\033[1m{text}\033[0m"


def gray(text):
    return f"\033[90m{text}\033[0m"


def yellow(text):
    return f"\033[93m{text}\033[0m"


def green(text):
    return f"\033[92m{text}\033[0m"


def red(text):
    return f"\033[91m{text}\033[0m"


usage = "%prog [program_to_test]"

opt_parser = optparse.OptionParser(usage=usage)
_, args = opt_parser.parse_args()

timeout = 1  # segundos

if len(args) > 0:
    cases = [
        basename(filename)[:-3]
        for filename in
        glob.glob(join(dirname(__file__), "tests/regex/modules/*.py"))
    ]
    cases.sort()
    input = join(dirname(__file__), "tests/input/strings.txt")
    results = []

    print(f"Testing {bold((' ').join(args))} ({len(cases)} test cases)")

    for case in cases:
        regex_module = importlib.import_module(f"tests.regex.modules.{case}")
        regex = regex_module.__regex__
        print(f"\n{gray(f'[{case}]')} Testing regex {yellow(regex)}...")

        try:
            # output is in files at tests/regex/output/*.txt
            with open(join(dirname(__file__), f"tests/regex/output/{case}.txt")) as f:
                expected_output = f.read()
            # timeit
            start = timer()
            actual_output = subprocess.check_output(
                [*args, "-m", f"tests.regex.modules.{case}", input],
                stderr=subprocess.STDOUT,
                timeout=timeout
            ).decode('utf-8')
            end = timer()
            time = f'{((end - start) * 1000):.1f}ms'

            if actual_output == expected_output:
                print(
                    f"  {green('OK')} {gray(f'({len(actual_output.splitlines())} matches, {time})')}")
                results.append(True)
            else:
                print(f"  {red('ERROR:')} {gray(f'({time})')}")
                for line in unified_diff(
                    actual_output.splitlines(),
                    expected_output.splitlines(),
                    fromfile="actual",
                    tofile="expected",
                    lineterm="",
                    n=0,
                ):
                    if line.startswith("+"):
                        print(f"    {green(line)}")
                    elif line.startswith("-"):
                        print(f"    {red(line)}")
                    else:
                        print(f"    {gray(line)}")
                results.append(False)
        except subprocess.TimeoutExpired:
            print(f"  {red('ERROR:')} Timeout expired")
            results.append(False)
            continue
        except subprocess.CalledProcessError as e:
            print(f"  {red('ERROR:')} {e.output.decode('utf-8')}")
            results.append(False)
            continue

    if all(results):
        print(f"\n{bold(green(f'All {len(results)} tests passed'))}")
        exit(0)
    else:
        print(
            f"\n{bold(red(f'{results.count(False)} out of {len(results)} tests failed'))}")
        exit(results.count(False))
else:
    print('ERROR: No program to test',
          file=sys.stderr)
    exit(1)
