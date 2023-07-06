from regex_parser.our_parser import parse
from regex import Union, Char, Concat, Star, Plus, Lambda
import pytest

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

def test_class_with_char():
    regex = "[a]"
    result = parse(regex)
    assert result.match('a')

def test_class_with_many_chars():
    regex = "[ab]"
    result = parse(regex)
    assert result.match('a')
    assert result.match('b')

def test_class_with_num():
    regex = "[2]"
    result = parse(regex)
    assert result.match('2')

def test_class_with_range():
    regex = "[a-e]"
    result = parse(regex)
    assert result.match('a')
    assert result.match('b')
    assert result.match('c')
    assert result.match('d')
    assert result.match('e')
    assert not result.match('f')
    assert not result.match('-')
    assert not result.match('')

def test_class_with_many_chars():
    regex = "[ab]"
    result = parse(regex)
    assert result.match('a')
    assert result.match('b')

def test_class_with_many_chars_ranges():
    regex = "[a-zA-Z]"
    result = parse(regex)
    assert result.match('b')
    assert result.match('B')

def test_class_with_number_range():
    regex = "[0-9]"
    result = parse(regex)
    assert result.match('0')
    assert result.match('1')
    assert result.match('2')
    assert result.match('3')
    assert result.match('4')
    assert result.match('5')
    assert result.match('6')
    assert result.match('7')
    assert result.match('8')
    assert result.match('9')

def test_special_class_d():
    regex = "\\d"
    result = parse(regex)
    assert result.match('0')
    assert result.match('1')
    assert result.match('2')
    assert result.match('3')
    assert result.match('4')
    assert result.match('5')
    assert result.match('6')
    assert result.match('7')
    assert result.match('8')
    assert result.match('9')
    
def test_special_class_w():
    regex = "\\w"
    result = parse(regex)
    assert result.match('b')
    assert result.match('B')
    assert result.match('1')
    assert result.match('_')

def test_non_special_class():
    regex = "\\x"
    result = parse(regex)
    assert result.match('\\x')

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

def test_kleene_kleene():
    regex = "a**"
    result = parse(regex)
    assert result is None

def test_class_positive_closure():
    regex = "[ab]+"
    result = parse(regex)
    assert result.match('a')
    assert result.match('b')
    assert result.match('aa')
    assert result.match('bb')
    assert result.match('ab')

def test_optional_positive_closure():
    regex = "(a+)?"
    result = parse(regex)
    assert result.match('')
    assert result.match('aaaaaa')

def test_question():
    regex = "\\?"
    result = parse(regex)
    assert result.match('?')

def test_union():
    regex = "\\|"
    result = parse(regex)
    assert result.match('|')

def test_empty():
    regex = ""
    result = parse(regex)
    assert result.match('')

def test_class_with_plus():
    regex = "[\\+]"
    result = parse(regex)
    assert result.match('+')
    
def test_class_with_char_num_and_positive():
    regex = "[a1\\+]"
    result = parse(regex)
    assert result.match('a')
    assert result.match('1')
    assert result.match('+')

def test_empty_class():
    regex = "[]"
    result = parse(regex)
    assert not result.match('')
    

def test_class_with_minus():
    regex = "[-]"
    result = parse(regex)
    assert result.match('-')

def test_cb_minus_cb():
    regex = "{-}"
    result = parse(regex)
    assert result.match('{-}')