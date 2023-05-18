from automata.afnd import AFND, SpecialSymbol


def get_union_automata(automata1: AFND, automata2: AFND) -> AFND:
    automata1.normalize_states("a")
    automata2.normalize_states("b")

    automata = AFND()
    automata.states = set(automata1.states | automata2.states)
    automata.transitions = dict(automata1.transitions | automata2.transitions)
    automata.alphabet = set(automata1.alphabet | automata2.alphabet)

    automata.add_state(0)
    automata.mark_initial_state(0)
    automata.add_transition(0, automata1.initial_state, SpecialSymbol.Lambda)
    automata.add_transition(0, automata2.initial_state, SpecialSymbol.Lambda)

    automata.add_state("f", final=True)

    for i in automata1.final_states:
        automata.add_transition(i, "f", SpecialSymbol.Lambda)
    for i in automata2.final_states:
        automata.add_transition(i, "f", SpecialSymbol.Lambda)

    automata.normalize_states()
    return automata


def get_concat_automata(automata1: AFND, automata2: AFND) -> AFND:
    automata1.normalize_states("a")
    automata2.normalize_states("b")

    automata = AFND()
    automata.states = automata1.states.union(automata2.states)
    automata.transitions = automata1.transitions | automata2.transitions
    automata.alphabet = automata1.alphabet.union(automata2.alphabet)
    # The initial state of the automata must be the same of aut1
    automata.mark_initial_state(automata1.initial_state)
    # The end state of aut1 and initial state of aut2 must be the same
    for i in automata1.final_states:
        automata.add_transition(i, automata2.initial_state, SpecialSymbol.Lambda)
    # The end state of the automata must be the same of aut2
    automata.add_state("f", final=True)
    for i in automata2.final_states:
        automata.add_transition(i, "f", SpecialSymbol.Lambda)

    automata.normalize_states()
    return automata


def get_star_automata(aut: AFND) -> AFND:
    for i in aut.final_states:
        aut.add_transition(i, aut.initial_state, SpecialSymbol.Lambda)
        aut.add_transition(aut.initial_state, i, SpecialSymbol.Lambda)
    aut.normalize_states()

    return aut


def get_plus_automata(aut: AFND) -> AFND:
    for i in aut.final_states:
        aut.add_transition(i, aut.initial_state, SpecialSymbol.Lambda)
    aut.normalize_states()
    
    return aut
