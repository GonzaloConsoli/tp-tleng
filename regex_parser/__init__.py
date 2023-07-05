from regex import RegEx
from our_parser import parse

__all__ = ["parse_regex"]


def parse_regex(regex_str: str) -> RegEx:
    return parse(regex_str)