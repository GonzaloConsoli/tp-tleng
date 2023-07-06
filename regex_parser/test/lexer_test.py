
from regex_parser.lexer import tokenize_and_print

def test_basic_char(capsys):
    regex = "a|b"
    tokenize_and_print(regex)
    captured = capsys.readouterr()
    assert captured.out == "[('CHAR', 'a'), ('UNION', '|'), ('CHAR', 'b')]\n"

def test_basic_chars(capsys):
    regex = "ab|cd"
    tokenize_and_print(regex)
    captured = capsys.readouterr()
    assert captured.out == "[('CHAR', 'a'), ('CHAR', 'b'), ('UNION', '|'), ('CHAR', 'c'), ('CHAR', 'd')]\n"