from automata.afnd import AFND, SpecialSymbol


def test_afnd_empty():
    aut1 = AFND()
    aut1.add_state(0)
    aut1.add_state(1, final=True)
    aut1.add_transition(0, 1, SpecialSymbol.Lambda)
    aut1.mark_initial_state(0)
    assert aut1.matches("")
    assert not aut1.matches("a")
    assert not aut1.matches("aa")
    assert not aut1.matches("b")


def test_afnd_a():
    aut1 = AFND()
    aut1.add_state(0)
    aut1.add_state(1, final=True)
    aut1.add_transition(0, 1, "a")
    aut1.mark_initial_state(0)
    aut1.normalize_states()
    assert aut1.matches("a")
    assert not aut1.matches("aa")
    assert not aut1.matches("b")
    assert not aut1.matches("")


def test_afnd_aa():
    aut1 = AFND()
    aut1.add_state(0)
    aut1.add_state(1)
    aut1.add_state(2, final=True)
    aut1.add_transition(0, 1, "a")
    aut1.add_transition(1, 2, "a")
    aut1.mark_initial_state(0)
    aut1.normalize_states()
    assert aut1.matches("aa")
    assert not aut1.matches("aaa")
    assert not aut1.matches("a")
    assert not aut1.matches("b")
    assert not aut1.matches("")


def test_afnd_lambda_aa():
    aut1 = AFND()
    aut1.add_state(0)
    aut1.add_state(1)
    aut1.add_state(2)
    aut1.add_state(3, final=True)
    aut1.add_transition(0, 1, SpecialSymbol.Lambda)
    aut1.add_transition(1, 2, "a")
    aut1.add_transition(2, 3, "a")
    aut1.mark_initial_state(0)
    aut1.normalize_states()
    assert aut1.matches("aa")
    assert not aut1.matches("aaa")
    assert not aut1.matches("aaaaaa")
    assert not aut1.matches("b")
    assert not aut1.matches("")
