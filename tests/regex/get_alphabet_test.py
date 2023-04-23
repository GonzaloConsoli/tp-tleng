from automata.afnd import SpecialSymbol
from regex import Char, Concat, Empty, Lambda, Plus, Star, Union

class TestGetAlphabet:
    def test_for_empty(self):
        regex = Empty()
        assert set() == regex.get_alphabet()

    def test_for_lambda(self):
        regex = Lambda()
        assert set([SpecialSymbol.Lambda]) == regex.get_alphabet()

    def test_for_char(self):
        regex = Char('a')
        assert set(['a']) == regex.get_alphabet()

    def test_for_concat(self):
        regex = Concat(Char('a'), Char('b'))
        assert set(['a', 'b']) == regex.get_alphabet()
    
    def test_for_union(self):
        regex = Union(Char('a'), Char('b'))
        assert set(['a', 'b']) == regex.get_alphabet()

    def test_for_star(self):
        regex = Star(Char('a'))
        assert set(['a']) == regex.get_alphabet()

    def test_for_plus(self):
        regex = Plus(Char('a'))
        assert set(['a']) == regex.get_alphabet()