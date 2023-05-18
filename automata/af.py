from abc import ABC, abstractmethod
from tabulate import tabulate
from typing import Hashable


__all__ = ["AF"]


class AF(ABC):
    """Clase abstracta que representa un autómata finito."""

    def __init__(self):
        self.states = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}
        self.alphabet = set()

    def add_state(self, state: Hashable, final: bool = False):
        """
        Agrega un estado al autómata.
        El estado puede ser cualquier cosa, siempre y cuando sea hashable
        (https://docs.python.org/3.11/glossary.html#term-hashable)
        """
        if state in self.states:
            raise ValueError(f"El estado {state} ya pertenece al autómata.")
        self.states.add(state)
        self.transitions[state] = {}
        if final:
            self.final_states.add(state)

    def mark_initial_state(self, state: Hashable, final: bool = False):
        """Marca un estado del autómata como inicial."""
        if state not in self.states:
            raise ValueError(f"El estado {state} no pertenece al autómata.")
        self.initial_state = state

    def normalize_states(self, append_str = ""):
        """
        Normaliza los nombres de los estados según la convención q0, q1, q2, ...

        Modifica el autómata (no crea una copia) y devuelve el autómata modificado.
        """
        new_names = {}
        if self.initial_state is not None:
            new_names[self.initial_state] = "q0" + append_str
        for i, state in enumerate(self.states - {self.initial_state}):
            if state not in new_names:
                new_names[state] = f"q{i + 1}" + append_str

        # Ordenamos los estados para hacer el renombre sin pisar ninguno
        ordered_new_names = []
        while len(new_names) > 0:
            for old_name, new_name in new_names.items():
                if old_name == new_name or new_name not in new_names.keys():
                    ordered_new_names.append([old_name, new_name, False])
                    del new_names[old_name]
                    break
            else:
                # Detectamos un loop entre las operaciones de renombre
                # Hay que usar un nombre temporal
                old_name, new_name = next(iter(new_names.items()))
                ordered_new_names.append([old_name, new_name, True])
                del new_names[old_name]

        # Realizamos el renombre
        for old_name, new_name, use_temp in ordered_new_names:
            if use_temp:
                while new_name in self.states:
                    new_name = f"temp:{new_name}"
            self._rename_state(old_name, new_name)

        # Eliminamos los nombres temporales
        for state in self.states:
            if state.startswith("temp:"):
                self._rename_state(state, state.split(":")[-1])

        return self

    def transitions_table(self):
        """Genera una tabla con las transiciones del autómata."""

        header = ["Estado"] + self._get_extended_alphabet()
        table = []
        for state in self.transitions:
            row = [
                f"{state}{'*' if state in self.final_states else ('^' if state == self.initial_state else '')}"
            ]
            row.extend(self._print_transitions(state).values())
            table.append(row)
        return tabulate(table, header, tablefmt="fancy_grid")

    def __str__(self):
        """Imprime el autómata."""
        return f"{self.__class__.__name__}<{self.states}, {self.alphabet}, δ, {self.initial_state}, {self.final_states}>"

    def _rename_state(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado del autómata."""
        if old_name != new_name:
            self.states.remove(old_name)
            self.states.add(new_name)
            if old_name == self.initial_state:
                self.initial_state = new_name
            if old_name in self.final_states:
                self.final_states.remove(old_name)  
                self.final_states.add(new_name)
            self._rename_state_in_transitions(old_name, new_name)

    @abstractmethod
    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        pass

    @abstractmethod
    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        pass

    @abstractmethod
    def _print_transitions(self, state: Hashable) -> dict[Hashable, str]:
        """Imprime las transiciones de un estado para cada símbolo."""
        pass

    @abstractmethod
    def matches(self, string: str) -> bool:
        pass
