from abc import ABC, abstractmethod

from automata import AFND
from automata.afnd import SpecialSymbol


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
    """Clase abstracta para representar expresiones regulares."""

    @abstractmethod
    def naive_match(self, word: str) -> bool:
        """
        Indica si la expresión regular acepta la cadena dada.
        Implementación recursiva, poco eficiente.
        """
        pass

    def match(self, word: str) -> bool:
        """Indica si la expresión regular acepta la cadena dada."""
        raise NotImplementedError

    @abstractmethod
    def _atomic(self) -> bool:
        """
        (Interno) Indica si la expresión regular es atómica. Útil para
        implementar la función __str__.
        """
        pass

    @abstractmethod
    def get_alphabet(self) -> set:
        """
        Retorna el alfabeto asociado a una expresion regular
        """
        pass

    def derive(self, char):
        """
        Retorna la derivada de la expresion regular respecto de un simbolo
        """
        if (len(char) > 1):
            raise ValueError("Se debe derivar respecto a solo un caracter")

    @abstractmethod   
    def epsilon(self):
        """
        Retorna lambda si la expresion regular acepta lambda, vacio si no
        """
        pass

class Empty(RegEx):
    """Expresión regular que denota el lenguaje vacío (∅)."""

    def naive_match(self, word: str):
        return False

    def _atomic(self):
        return True

    def __str__(self):
        return "∅"
    
    def get_alphabet(self) -> set:
        return set()
    
    def derive(self, char):
        super().derive(char)

        return self
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(self, __value.__class__)
    
    def epsilon(self):
        return Empty()


class Lambda(RegEx):
    """Expresión regular que denota el lenguaje de la cadena vacía (Λ)."""

    def naive_match(self, word: str):
        return word == ""

    def _atomic(self):
        return True

    def __str__(self):
        return "λ"
    
    def get_alphabet(self) -> set:
        return set([SpecialSymbol.Lambda])
    
    def derive(self, char):
        super().derive(char)

        return Empty()

    def __eq__(self, __value: object) -> bool:
        return isinstance(self, __value.__class__)
    
    def epsilon(self):
        return Lambda()


class Char(RegEx):
    """Expresión regular que denota el lenguaje de un determinado carácter."""

    def __init__(self, char: str | None):
        assert len(char) == 1
        self.char = char

    def naive_match(self, word: str):
        return word == self.char

    def _atomic(self):
        return True

    def __str__(self):
        return self.char

    def get_alphabet(self) -> set:
        return set(self.char)
    
    def derive(self, char):
        super().derive(char)

        if char == self.char:
            return Lambda()
        else:
            return Empty()
        
    def epsilon(self):
        return Empty()
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(self, __value.__class__) and self.char == __value.char

class Concat(RegEx):
    """Expresión regular que denota la concatenación de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
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
    
    def get_alphabet(self) -> set:
        return set.union(self.exp1.get_alphabet(), self.exp2.get_alphabet())
    
    def derive(self, char):
        super().derive(char)

        return Union(Concat(self.exp1.derive(char), self.exp2), Concat(self.exp1.epsilon(), self.exp2.derive(char)))

    def epsilon(self):
        return Empty()
    
    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)


class Union(RegEx):
    """Expresión regular que denota la unión de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        return self.exp1.naive_match(word) or self.exp2.naive_match(word)

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"|{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"
    
    def get_alphabet(self) -> set:
        return set.union(self.exp1.get_alphabet(), self.exp2.get_alphabet())
    
    def epsilon(self):
        if self.exp1.epsilon() == Lambda() or self.exp2.epsilon() == Lambda():
            return Lambda()
        else:
            return Empty()

class Star(RegEx):
    """Expresión regular que denota la clausura de Kleene de otra expresión regular."""

    def __init__(self, exp: RegEx):
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
    
    def get_alphabet(self) -> set:
        return self.exp.get_alphabet()

    def epsilon(self):
        return Lambda()


class Plus(RegEx):
    """Expresión regular que denota la clausura positiva de otra expresión regular."""

    def __init__(self, exp: RegEx):
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
    
    def get_alphabet(self) -> set:
        return self.exp.get_alphabet()

    def epsilon(self):
        if self.exp.epsilon() == Lambda():
            return Lambda()
        else:
            return Empty()
