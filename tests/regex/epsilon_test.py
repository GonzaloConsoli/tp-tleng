from automata.afnd import SpecialSymbol
from regex import Char, Concat, Empty, Lambda, Plus, Star, Union

class TestEpsilon:
    def test_for_empty(self):
        assert Empty() == Empty().epsilon()

    def test_for_lambda(self):
        assert Lambda() == Lambda().epsilon()

    def test_for_char(self):
        assert Empty() == Char('a').epsilon()

    def test_for_concat(self):
        assert Empty() == Concat(Char('a'), Char('b')).epsilon()
    
    def test_for_union(self):
        assert Empty() == Union(Char('a'), Char('b')).epsilon()
        assert Lambda() == Union(Char('a'), Lambda()).epsilon()

    def test_for_star(self):
        assert Lambda() == Star(Char('a')).epsilon()

    def test_for_plus(self):
        assert Empty() == Plus(Char('a')).epsilon()
        assert Lambda() == Plus(Union(Char('a'), Lambda())).epsilon()