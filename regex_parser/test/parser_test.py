from regex_parser.our_parser import parse
from regex import Union, Char, Concat, Star

def test_union_of_char():
    regex = "a|b"
    result = parse(regex)
    assert isinstance(result, Union)
    assert isinstance(result.exp1, Char)
    assert isinstance(result.exp2, Char)
    assert result.exp1.char == 'a'
    assert result.exp2.char == 'b'

def test_concat_of_char():
    regex = "ab"
    result = parse(regex)
    assert isinstance(result, Concat)
    assert isinstance(result.exp1, Char)
    assert isinstance(result.exp2, Char)
    assert result.exp1.char == 'a'
    assert result.exp2.char == 'b'

def test_one_char_kleene():
    regex = "a*"
    result = parse(regex)
    assert isinstance(result, Star)
    assert isinstance(result.exp, Char)
    assert result.exp.char == 'a'

def test_many_char_kleene():
    regex = "ab*"
    result = parse(regex)
    assert isinstance(result, Concat)
    assert isinstance(result.exp1, Char)
    assert result.exp1.char == 'a'
    assert isinstance(result.exp2, Star)
    assert isinstance(result.exp2.exp, Char)
    assert result.exp2.exp.char == 'b'


def test_union_of_concat_of_chars(capsys):
    regex = "ab|cd"
    result = parse(regex)
    assert isinstance(result, Union)
    assert isinstance(result.exp1, Concat)
    assert isinstance(result.exp2, Concat)