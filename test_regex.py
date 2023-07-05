#!/usr/bin/env python3
from os.path import dirname, basename, isfile, join
import glob
import optparse
import sys
import importlib
import subprocess
from timeit import default_timer as timer

from tests.utils import bold, red, green, yellow, gray, print_diff


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
    input_file = join(dirname(__file__), "tests/input/strings.txt")
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
                [*args, "-m", f"tests.regex.modules.{case}", input_file],
                stderr=subprocess.STDOUT,
                timeout=timeout
            ).decode('utf-8')
            end = timer()
            time = f'{((end - start) * 1000):.1f}ms'

            # Reemplazamos los finales de línea Windows-style por UNIX-style
            # para que los tests funcionen en ambas plataformas
            actual_output = actual_output.replace("\r\n", "\n")

            if actual_output == expected_output:
                print(
                    f"  {green('OK')} {gray(f'({len(actual_output.splitlines())} matches, {time})')}")
                results.append(True)
            else:
                print(f"  {red('ERROR:')} {gray(f'({time})')}")
                print_diff(actual_output, expected_output)
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
# else:
#     print('ERROR: No program to test',
#           file=sys.stderr)
#     exit(1)
