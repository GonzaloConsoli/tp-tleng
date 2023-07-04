#!/usr/bin/env python3
from os.path import dirname, basename, isfile, join
import glob
import optparse
import sys
import importlib
import subprocess
from timeit import default_timer as timer

from tests.utils import bold, red, green, yellow, gray, print_diff
from tests.parser import test_cases

usage = "%prog [program_to_test]"

opt_parser = optparse.OptionParser(usage=usage)
_, args = opt_parser.parse_args()

timeout = 1  # segundos


if len(args) > 0:
    input_file = join(dirname(__file__), "tests/input/strings.txt")
    results = []

    print(f"Testing {bold((' ').join(args))} ({len(test_cases)} test cases)")

    for i in range(len(test_cases)):
        [test_string, expected_output] = test_cases[i]
        print(
            f"\n{gray(f'[{i}]')} Testing string \"{yellow(test_string)}\"...")

        expected_output = False if expected_output == False else "".join(
            map(lambda x: x + '\n', expected_output))

        try:
            # timeit
            start = timer()

            actual_output = subprocess.check_output(
                [*args, test_string, '--', input_file]
                if test_string.startswith('--')
                else [*args, test_string, input_file],
                stderr=subprocess.STDOUT,
                timeout=timeout
            ).decode('utf-8')
            end = timer()
            time = f'{((end - start) * 1000):.1f}ms'

            # Reemplazamos los finales de línea Windows-style por UNIX-style
            # para que los tests funcionen en ambas plataformas
            actual_output = actual_output.replace("\r\n", "\n")

            if expected_output == False:
                print(
                    f"  {red('ERROR:')} Parsing error expected {gray(f'({time})')}")
                results.append(False)
                continue
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
            if (expected_output == False):
                print(
                    f"  {green('OK')} {gray(f'(Parsing error, {time})')}")
                results.append(True)
                continue
            else:
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
