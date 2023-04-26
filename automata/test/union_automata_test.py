from automata.afnd import AFND
from automata.helpers import get_union_automata


# TODO: Cuando tengamos para recorrer un automata mejorar estos tests.
def test_union_automata():
    aut1 = AFND()
    aut1.add_state(0)
    aut1.add_state(1, final=True)
    aut1.add_transition(0, 1, "a")
    aut1.mark_initial_state(0)
    aut1.normalize_states()

    aut2 = AFND()
    aut2.add_state(0)
    aut2.add_state(1, final=True)
    aut2.add_transition(0, 1, "b")
    aut2.mark_initial_state(0)
    aut2.normalize_states()

    aut_union = get_union_automata(aut1, aut2)

    assert aut_union.alphabet == {"a", "b"}
