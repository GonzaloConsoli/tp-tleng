from enum import StrEnum
from typing import Hashable

from automata.af import AF
from collections import deque

__all__ = ["AFND"]


class SpecialSymbol(StrEnum):
    Lambda = "λ"


class AFND(AF):
    """Autómata finito no determinístico (con transiciones lambda)."""

    def add_transition(
        self, state1: Hashable, state2: Hashable, char: str | SpecialSymbol
    ):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        if char not in self.transitions[state1]:
            self.transitions[state1][char] = set()
        self.transitions[state1][char].add(state2)
        if char is not SpecialSymbol.Lambda:
            self.alphabet.add(char)

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if old_name in self.transitions[state][char]:
                    self.transitions[state][char].remove(old_name)
                    self.transitions[state][char].add(new_name)

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet) + [SpecialSymbol.Lambda]

    def _print_transitions(self, state: Hashable) -> dict[Hashable, str]:
        """Imprime las transiciones de un estado para cada símbolo."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = ",".join(self.transitions[state][char])
            else:
                transitions[char] = "-"
        return transitions

    def matches(self, string: str) -> bool:
        """Metodo para ver si un AFND acepta la cadena dada."""
        already_on = {x: False for x in self.states}
        # old_states, holds the "current" set of states
        old_states = deque()
        # new_states holds the "next" set of states
        new_states = deque()

        def add_state(s: Hashable):
            new_states.append(s)
            already_on[s] = True
            lambda_closure = self.transitions[s].get(SpecialSymbol.Lambda, {})
            for t in lambda_closure:
                if not already_on[t]:
                    add_state(t)

        add_state(self.initial_state)
        for s in list(new_states):
            new_states.pop()
            old_states.append(s)
            already_on[s] = False

        for c in string:
            for s in list(old_states):
                move_s_c = self.transitions[s].get(c, set())
                for t in move_s_c:
                    if not already_on[t]:
                        add_state(t)
                old_states.pop()
            for s in list(new_states):
                new_states.pop()
                old_states.append(s)
                already_on[s] = False

        return len(self.final_states.intersection(set(old_states))) > 0
