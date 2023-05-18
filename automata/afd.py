from typing import Hashable
from automata.af import AF

__all__ = ["AFD"]


class AFD(AF):
    """Autómata finito determinístico."""

    def add_transition(self, state1: Hashable, state2: Hashable, char: str):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        self.transitions[state1][char] = state2
        self.alphabet.add(char)

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if self.transitions[state][char] == old_name:
                    self.transitions[state][char] = new_name

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet)

    def _print_transitions(self, state: Hashable) -> dict[Hashable, str]:
        """Imprime las transiciones de un estado para cada símbolo."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = self.transitions[state][char]
            else:
                transitions[char] = "-"
        return transitions
        

    def matches(self, string: str) -> bool:
        q = self.initial_state
        for i in string:
            q = self.transitions.get(q, {}).get(i, {})
            if q == {}:
                return False
        return q in self.final_states

    def minimize(self):      
        self._complete()
        alphabet = self._get_extended_alphabet()
        equivalence_classes = self._get_initial_equivalence_classes()
        new_equivalence_classes = []
        table = {}

        while set(equivalence_classes) != set(new_equivalence_classes):
            if len(new_equivalence_classes) != 0:
                equivalence_classes = new_equivalence_classes
                new_equivalence_classes = []

            table = self._build_transitions_table(alphabet, equivalence_classes)
            for state in self.states:
                self._find_new_equivalence_class(equivalence_classes, new_equivalence_classes, table, state)
            self.rename_classes(equivalence_classes)
            self.rename_classes(new_equivalence_classes)

        return self._build_minimized_automata(new_equivalence_classes, table)

    def rename_classes(self, equivalence_classes):
        name = "I"
        for ec in equivalence_classes:
            ec._id = name
            name = name + "I"

    def _build_minimized_automata(self, new_equivalence_classes, table):
        minimized = AFD()
        for i in range(0, len(new_equivalence_classes)):
            is_final = False
            for final_state in self.final_states:
                if final_state in new_equivalence_classes[i]._states:
                    is_final = True
                    break
            minimized.add_state(i, is_final)

        for i in range(0, len(new_equivalence_classes)):
            is_initial = self.initial_state in new_equivalence_classes[i]._states
            if is_initial:
                minimized.mark_initial_state(i)

        for state in table:
            for symbol in table[state]:
                target_equivalence_class = table[state][symbol]
                source_equivalence_class = None
                for equivalence_class in new_equivalence_classes:
                    if state in equivalence_class._states:
                        source_equivalence_class = equivalence_class
                        break
                minimized.add_transition(source_equivalence_class.index(), target_equivalence_class.index(), symbol)

        return minimized

    def _get_initial_equivalence_classes(self):
        return [
            EquivalenceClass(self.states.difference(self.final_states), "I"),
            EquivalenceClass(self.final_states, "II")
        ]

    def _build_transitions_table(self, alphabet, equivalence_classes):
        table = {}
        for state in self.states:
            table[state] = {}
            for symbol in alphabet:
                next = self.transitions.get(state, {}).get(symbol, {})
                equivalence_class = self._find_equivalence_class(equivalence_classes, next)
                table[state][symbol] = equivalence_class
        return table

    def _find_new_equivalence_class(self, equivalence_classes, new_equivalence_classes, table, state):
        current_equivalence_class = None
        for equivalence_class in equivalence_classes:
            if state in equivalence_class._states:
                current_equivalence_class = equivalence_class
                break

        new_class_id = current_equivalence_class._id

        for symbol in table[state]:
            new_class_id = new_class_id + "-" + table[state][symbol]._id
            
        new_class = EquivalenceClass(set([state]), new_class_id)

        added = False     
        for i in range(0, len(new_equivalence_classes)):
            if new_equivalence_classes[i] == new_class:
                new_equivalence_classes[i].add_state(state)
                added = True

        if not added:
            new_equivalence_classes.append(new_class)

    def _find_equivalence_class(self, equivalence_classes, next):
        equivalence_class = None
        for ec in equivalence_classes:
            if ec.has_state(next):
                equivalence_class = ec
                break
            
        return equivalence_class
            
    def _complete(self):
        self.add_state("t")
        for symbol in self.alphabet:
            self.add_transition("t", "t", symbol)
        for state in self.transitions:
            for symbol in self.alphabet:
                if not symbol in self.transitions[state]:
                    self.add_transition(state, "t", symbol)


class EquivalenceClass:
    def __init__(self, states, id) -> None:
        self._id = id
        self._states = states

    def add_state(self, state):
        self._states.add(state)
    
    def has_state(self, state):
        return state in self._states
    
    def index(self):
        return len(self._id)-1

    def __eq__(self, __value: object) -> bool:
        return self._id == __value._id
    
    def __str__(self) -> str:
        return self._id
    
    def __repr__(self) -> str:
        return self._id
    
    def __hash__(self) -> int:
        return frozenset(self._states).__hash__()