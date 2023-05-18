from automata.afnd import AFND, SpecialSymbol
from automata.helpers import get_concat_automata, get_star_automata, get_union_automata,get_plus_automata
from regex import Char, Concat, Empty, Lambda, Plus, Star, Union, RegEx, regex_to_automata


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
    lambda_automata = AFND()
    lambda_automata.add_state(0)
    lambda_automata.add_state(1, final=True)
    lambda_automata.add_transition(0, 1, SpecialSymbol.Lambda)
    lambda_automata.mark_initial_state(0)
    lambda_automata.normalize_states()
    assert str(res) == str(lambda_automata)

def test_empty():
    afnd = regex_to_automata(Empty())
    afd = afnd.to_afd()
    assert not afd.matches('a')


def test_chr_a_str():
    res = regex_to_automata(Char("a"))
    char_automata = get_char_automata("a")
    assert str(res) == str(char_automata)


def test_chr_b_str():
    res = regex_to_automata(Char("b"))
    char_automata = get_char_automata("b")
    assert str(res) == str(char_automata)


def test_union_a_b():
    res = regex_to_automata(Union(Char("a"), Char("b")))
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_union = get_union_automata(aut_a, aut_b)
    assert str(res) == str(aut_union)


def test_concat_a_b():
    res = regex_to_automata(Concat(Char("a"), Char("b")))
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_union = get_concat_automata(aut_a, aut_b)
    assert str(res) == str(aut_union)


def test_star_a():
    res = regex_to_automata(Star(Char("a")))
    aut_a = get_char_automata("a")
    aut_a_star = get_star_automata(aut_a)
    assert str(res) == str(aut_a_star)

def test_plus_a():
    res = regex_to_automata(Plus(Char("a")))
    aut_a = get_char_automata("a")
    aut_a_plus = get_plus_automata(aut_a)
    assert str(res) == str(aut_a_plus)

def test_plus_concat():
    res = regex_to_automata(Plus(Concat(Char("a"), Char("b"))))
    aut_a = get_char_automata("a")
    aut_b = get_char_automata("b")
    aut_concat = get_concat_automata(aut_a, aut_b)
    aut_concat_plus = get_plus_automata(aut_concat)
    assert str(res) == str(aut_concat_plus)
