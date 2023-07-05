
from regex_parser.lexer import tokenize_and_print

def basic_test():
    regex = "ab|cd"
    tokenize_and_print(regex)