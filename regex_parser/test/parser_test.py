from regex_parser.our_parser import parse
from regex import Union, Char, Concat, Star, Plus, Lambda

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

def test_one_char_positive():
    regex = "a+"
    result = parse(regex)
    assert isinstance(result, Plus)
    assert isinstance(result.exp, Char)
    assert result.exp.char == 'a'

def test_many_char_positive():
    regex = "ab+"
    result = parse(regex)
    assert isinstance(result, Concat)
    assert isinstance(result.exp1, Char)
    assert result.exp1.char == 'a'
    assert isinstance(result.exp2, Plus)
    assert isinstance(result.exp2.exp, Char)
    assert result.exp2.exp.char == 'b'

def test_one_char_question():
    regex = "a?"
    result = parse(regex)
    assert isinstance(result, Union)
    assert isinstance(result.exp1, Char)
    assert isinstance(result.exp2, Lambda)
    assert result.exp1.char == 'a'

def test_many_char_positive():
    regex = "ab?"
    result = parse(regex)
    assert isinstance(result, Concat)
    assert isinstance(result.exp1, Char)
    assert result.exp1.char == 'a'
    assert isinstance(result.exp2, Union)
    assert isinstance(result.exp2.exp1, Char)
    assert isinstance(result.exp2.exp2, Lambda)
    assert result.exp2.exp1.char == 'b'

def test_simple_quantifier():
    regex = "a{3}"
    result = parse(regex)
    assert result.match('aaa')

def test_double_quantifier():
    regex = "a{3,5}"
    result = parse(regex)
    assert not result.match('aa')
    assert result.match('aaa')
    assert result.match('aaaa')
    assert result.match('aaaaa')
    assert not result.match('aaaaaa')

def test_parenthesis():
    regex = "(a)"
    result = parse(regex)
    assert result.match('a')

def test_empty_parenthesis():
    regex = "()"
    result = parse(regex)
    assert result.match('')


def test_union_of_concat_of_twos_char_and_one_char():
    regex = "ab|c"
    result = parse(regex)
    assert isinstance(result, Union)
    assert isinstance(result.exp1, Concat)
    assert isinstance(result.exp2, Char)


def test_union_of_concat_of_one_char_and_two_chars():
    regex = "a|cd"
    result = parse(regex)
    assert isinstance(result, Union)
    assert isinstance(result.exp1, Char)
    assert isinstance(result.exp2, Concat)

def test_union_of_concat_of_chars():
    regex = "ab|cd"
    result = parse(regex)
    assert isinstance(result, Union)
    assert isinstance(result.exp1, Concat)
    assert isinstance(result.exp2, Concat)

# def test_special_class_d():
#     regex = "\d"
#     result = parse(regex)