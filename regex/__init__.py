from abc import ABC, abstractmethod
from automata.helpers import (
    get_concat_automata,
    get_plus_automata,
    get_star_automata,
    get_union_automata,
)
from automata.afnd import AFND, SpecialSymbol

__all__ = [
    "RegEx",
    "Empty",
    "Lambda",
    "Char",
    "Union",
    "Concat",
    "Star",
    "Plus"
]


class RegEx(ABC):
    def __init__(self):
        self._min_afd = None

    """Clase abstracta para representar expresiones regulares."""

    @abstractmethod
    def naive_match(self, word: str) -> bool:
        """
        Indica si la expresión regular acepta la cadena dada.
        Implementación recursiva, poco eficiente.
        """
        pass

    def match(self, word: str) -> bool:
        if (self._min_afd is None):
            self._min_afd = regex_to_automata(self).to_afd().minimize()
        return self._min_afd.matches(word)

    @abstractmethod
    def _atomic(self) -> bool:
        """
        (Interno) Indica si la expresión regular es atómica. Útil para
        implementar la función __str__.
        """
        pass

    @abstractmethod   
    def epsilon(self):
        """
        Retorna lambda si la expresion regular acepta lambda, vacio si no
        """
        pass

class Empty(RegEx):
    """Expresión regular que denota el lenguaje vacío (∅)."""

    def __init__(self):
        super().__init__()

    def naive_match(self, word: str):
        return False

    def _atomic(self):
        return True

    def __str__(self):
        return "∅"
    
    def epsilon(self):
        return Empty()


class Lambda(RegEx):
    """Expresión regular que denota el lenguaje de la cadena vacía (Λ)."""

    def __init__(self):
        super().__init__()

    def naive_match(self, word: str):
        return word == ""

    def _atomic(self):
        return True

    def __str__(self):
        return "λ"
    
    def epsilon(self):
        return Lambda()


class Char(RegEx):
    """Expresión regular que denota el lenguaje de un determinado carácter."""

    def __init__(self, char: str | None):
        super().__init__()
        assert len(char) == 1
        self.char = char

    def naive_match(self, word: str):
        return word == self.char

    def _atomic(self):
        return True

    def __str__(self):
        return self.char
        
    def epsilon(self):
        return Empty()

class Concat(RegEx):
    """Expresión regular que denota la concatenación de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        super().__init__()
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        for i in range(len(word) + 1):
            if self.exp1.naive_match(word[:i]) and self.exp2.naive_match(word[i:]):
                return True
        return False

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"

    def epsilon(self):
        return Empty()
        


class Union(RegEx):
    """Expresión regular que denota la unión de dos expresiones regulares."""
        
    def __init__(self, exp1: RegEx, exp2: RegEx):
        super().__init__()
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        return self.exp1.naive_match(word) or self.exp2.naive_match(word)

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"|{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"
    
    def epsilon(self):
        if self.exp1.epsilon() == Lambda() or self.exp2.epsilon() == Lambda():
            return Lambda()
        else:
            return Empty()

class Star(RegEx):
    """Expresión regular que denota la clausura de Kleene de otra expresión regular."""

    def __init__(self, exp: RegEx):
        super().__init__()
        self.exp = exp

    def naive_match(self, word: str):
        if word == "" or self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def _atomic(self):
        return False

    def __str__(self):
        return f"({self.exp})*" if not self.exp._atomic() else f"{self.exp}*"

    def epsilon(self):
        return Lambda()


class Plus(RegEx):
    """Expresión regular que denota la clausura positiva de otra expresión regular."""

    def __init__(self, exp: RegEx):
        super().__init__()
        self.exp = exp

    def naive_match(self, word: str):
        if self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def _atomic(self) -> bool:
        return False

    def __str__(self):
        return f"({self.exp})+" if not self.exp._atomic() else f"{self.exp}+"

    def epsilon(self):
        if self.exp.epsilon() == Lambda():
            return Lambda()
        else:
            return Empty()

def regex_to_automata(regex: RegEx) -> AFND:
    if isinstance(regex, Empty):
        automata = AFND()
        automata.add_state("q0")
        automata.mark_initial_state("q0")
        return automata

    if isinstance(regex, Lambda):
        automata = AFND()
        automata.add_state(0, final=True)
        automata.mark_initial_state(0)
        automata.normalize_states()
        return automata

    elif isinstance(regex, Char):
        automata = AFND()
        automata.add_state(0)
        automata.add_state(1, final=True)
        automata.add_transition(0, 1, str(regex))
        automata.mark_initial_state(0)
        automata.normalize_states()
        return automata

    elif isinstance(regex, Union):
        automata1 = regex_to_automata(regex.exp1)
        automata2 = regex_to_automata(regex.exp2)
        automata = get_union_automata(automata1, automata2)
        return automata

    elif isinstance(regex, Concat):
        automata1 = regex_to_automata(regex.exp1)
        automata2 = regex_to_automata(regex.exp2)
        automata = get_concat_automata(automata1, automata2)
        return automata

    elif isinstance(regex, Star):
        automata1 = regex_to_automata(regex.exp)
        automata = get_star_automata(automata1)
        return automata

    elif isinstance(regex, Plus):
        automata1 = regex_to_automata(regex.exp)
        automata = get_plus_automata(automata1)
        return automata
