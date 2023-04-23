from automata.afnd import SpecialSymbol
from regex import Empty, Lambda

class TestGetAlphabet:
    def test_for_empty(self):
        regex = Empty()
        assert set() == regex.get_alphabet()

    def test_for_lambda(self):
        regex = Lambda()
        assert set([SpecialSymbol.Lambda]) == regex.get_alphabet()