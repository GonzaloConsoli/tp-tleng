from automata.afnd import AFND, SpecialSymbol
from automata.helpers import (
    get_concat_automata,
    get_plus_automata,
    get_star_automata,
    get_union_automata,
)
from regex import Char, Concat, Empty, Lambda, Plus, Star, Union, RegEx


def regex_to_automata(regex: RegEx) -> AFND:
    if isinstance(regex, Empty):
        automata = AFND()
        automata.add_state("q0")
        automata.mark_initial_state("q0")
        return automata

    if isinstance(regex, Lambda):
        automata = AFND()
        automata.add_state(0)
        automata.add_state(1, final=True)
        automata.add_transition(0, 1, SpecialSymbol.Lambda)
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
