from automata.afnd import AFND
from automata.helpers import get_concat_automata, get_union_automata,get_plus_automata
from regex import Char, Concat, Lambda, Plus, Star, regex_to_automata


def get_char_automata(char: str) -> AFND:
    char_automata = AFND()
    char_automata.add_state(0)
    char_automata.add_state(1, final=True)
    char_automata.add_transition(0, 1, char)
    char_automata.mark_initial_state(0)
    char_automata.normalize_states()
    return char_automata


def test_lambda_str():
    res = regex_to_automata(Lambda())
    assert res.matches('')
    assert not res.matches('a')


def test_chr_a_str():
    res = regex_to_automata(Char("a"))
    char_automata = get_char_automata("a")
    assert str(res) == str(char_automata)


def test_chr_b_str():
    res = regex_to_automata(Char("b"))
    char_automata = get_char_automata("b")
    assert str(res) == str(char_automata)


def test_union_a_b():
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_union = get_union_automata(aut_a, aut_b)

    assert aut_union.matches('a')
    assert aut_union.matches('b')
    assert not aut_union.matches('c')


def test_concat_a_b():
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_union = get_concat_automata(aut_a, aut_b)

    assert aut_union.matches('ab')
    assert not aut_union.matches('ba')
    assert not aut_union.matches('c')


def test_star_a():
    regex = Star(Char("a"))
    assert regex.naive_match('')
    assert regex.naive_match('a')
    assert regex.naive_match('aa')
    assert not regex.naive_match('b')

    automata = regex_to_automata(regex)
    assert automata.matches('')
    assert automata.matches('a')
    assert automata.matches('aa')
    assert not automata.matches('b')

def test_plus_a():
    res = regex_to_automata(Plus(Char("a")))

    assert res.matches('a')
    assert res.matches('aa')
    assert not res.matches('b')

def test_plus_union():
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_concat = get_union_automata(aut_a, aut_b)
    aut_concat_plus = get_plus_automata(aut_concat)

    assert aut_concat_plus.matches("aa")
    assert aut_concat_plus.matches("bb")
    assert aut_concat_plus.matches("abab")
    assert aut_concat_plus.matches("baba")



def test_plus_concat():
    res = regex_to_automata(Plus(Concat(Char("a"), Char("b"))))
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_concat = get_concat_automata(aut_a, aut_b)
    aut_concat_plus = get_plus_automata(aut_concat)
    assert str(res) == str(aut_concat_plus)
