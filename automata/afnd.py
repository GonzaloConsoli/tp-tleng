from enum import StrEnum
from typing import Hashable

from automata.af import AF
from automata.afd import AFD
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

    def to_afd(self) -> AFD:
        def lambda_closure_states(T: set) -> frozenset:
            stack = deque(T)
            res = set(T)
            while stack:
                t = stack.pop()
                for u in self.transitions[t].get(SpecialSymbol.Lambda, {}):
                    if u not in res:
                        res.add(u)
                        stack.append(u)
            return frozenset(res)

        def move(T: set, a: str) -> set:
            res = set()
            for t in T:
                if self.transitions[t].get(a):
                    for s in self.transitions[t].get(a):
                        res.add(s)
            return res

        dtran = {}
        dstates = {}

        initial_state = set()
        initial_state.add(self.initial_state)
        initial_state_closure = lambda_closure_states(initial_state)
        dstates[initial_state_closure] = True

        while any(dstates.values()):
            truthies = dict(filter(lambda x: x[1], dstates.items()))
            for set_of_states, value in truthies.items():
                if value:
                    dstates[set_of_states] = False
                    for a in self.alphabet:
                        states_moves_to = lambda_closure_states(move(set_of_states, a))
                        if states_moves_to and states_moves_to not in dstates.keys():
                            dstates[states_moves_to] = True
                        dtran[set_of_states] = {a: states_moves_to} | (
                            dtran[set_of_states] if dtran.get(set_of_states) else {}
                        )

        afd = AFD()
        # Adding states
        for qi in dstates:
            is_final = bool(self.final_states.intersection(qi))
            if qi != initial_state_closure:
                afd.add_state(qi, final=is_final)
            else:
                afd.add_state(initial_state_closure, final=is_final)
                afd.mark_initial_state(initial_state_closure)

        # Adding transitions
        for qi in dstates:
            for a, qj in dtran[qi].items():
                if qj:
                    afd.add_transition(qi, qj, a)

        afd.normalize_states()
        return afd
