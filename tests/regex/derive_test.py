import pytest
from automata.afnd import SpecialSymbol
from regex import Char, Concat, Empty, Lambda, Plus, Star, Union

class TestDerive:
    def test_only_one_char(self):
        all_regex = [
            Empty(), 
            Lambda(), 
            Char('a'),
            Concat(Char('a'), Char('a')),
            Union(Char('a'), Char('a')),
            Plus(Char('a')),
            Star(Char('a'))
        ]
        for regex in all_regex:
            self._derive_using_more_than_one_character(regex)

    def _derive_using_more_than_one_character(self, regex):
        with pytest.raises(ValueError) as error:
            regex.derive('aa')
        assert "Se debe derivar respecto a solo un caracter" == str(error.value)