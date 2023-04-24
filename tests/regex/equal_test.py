from automata.afnd import SpecialSymbol
from regex import Char, Concat, Empty, Lambda, Plus, Star, Union

class TestEqual:
    def test_for_empty(self):
        assert Empty() == Empty() 

    def test_for_lambda(self):
        assert Lambda() == Lambda() 

    def test_for_char(self):
        assert Char('a') == Char('a')
        assert Char('b') != Char('a')
        assert Char('b') != Lambda() 
        assert Char('b') != Empty()
        assert Char('b') != Concat(Char('a'), Char('b'))

    def test_for_concat(self):
        assert Concat(Char('a'), Char('b')) == Concat(Char('a'), Char('b'))
        assert Concat(Char('a'), Char('b')) != Concat(Char('b'), Char('a'))
        assert Concat(Char('a'), Lambda()) == Char('a')
        assert Concat(Lambda(), Char('a')) == Char('a')
        assert Concat(Lambda(), Lambda()) == Lambda()
        assert Concat(Char('a'), Empty()) == Empty()
        assert Concat(Lambda(), Empty()) == Empty()
        assert Concat(Char('a'), Char('b')) == Union(Concat(Char('a'), Char('b')), Empty())
        assert Concat(Char('a'), Char('b')) != Union(Concat(Char('a'), Char('b')), Lambda())
     
    def test_for_union(self):
        assert Union(Char('a'), Char('b')) == Union(Char('a'), Char('b'))
        assert Union(Char('a'), Char('b')) == Union(Char('b'), Char('a'))
        assert Union(Char('a'), Lambda()) != Char('a')
        assert Union(Lambda(), Char('a')) != Char('a')
        assert Union(Lambda(), Lambda()) == Lambda()
        assert Union(Char('a'), Empty()) == Char('a')
        assert Union(Lambda(), Empty()) == Lambda()
        assert Union(Empty(), Empty()) == Empty()
        assert Union(Char('a'), Empty()) != Empty()
        assert Union(Char('a'),Char('a')) == Char('a')
        assert Union(Char('a'),Char('a')) == Concat(Char('a'), Lambda())

    # def test_for_star(self):
    #     assert Star(Char('a')) == Union(Plus(Char('a')), Lambda())

    # def test_for_plus(self):
    #     assert Plus(Char('a')) == Plus(Char('a'))
    #     assert Plus(Char('a')) != Plus(Char('b'))