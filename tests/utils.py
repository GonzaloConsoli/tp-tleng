from difflib import unified_diff


__all__ = ["bold", "gray", "yellow", "green", "red", "print_diff"]


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


def print_diff(actual_output, expected_output):
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
