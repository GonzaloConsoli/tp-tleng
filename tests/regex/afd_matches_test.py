from automata.afd import AFD


def test_afd_empty():
    aut1 = AFD()
    aut1.add_state(0)
    aut1.mark_initial_state(0)
    assert not aut1.matches('a')
    assert not aut1.matches('aa')
    assert not aut1.matches('b')
    assert not aut1.matches('')


def test_afd_a():
    aut1 = AFD()
    aut1.add_state(0)
    aut1.add_state(1, final=True)
    aut1.add_transition(0, 1, "a")
    aut1.mark_initial_state(0)
    aut1.normalize_states()
    assert aut1.matches('a')
    assert not aut1.matches('aa')
    assert not aut1.matches('b')
    assert not aut1.matches('')



def test_afd_as():
    aut1 = AFD()
    aut1.add_state(0)
    aut1.add_state(1, final=True)
    aut1.add_transition(0, 1, "a")
    aut1.add_transition(1, 1, "a")
    aut1.mark_initial_state(0)
    aut1.normalize_states()
    assert aut1.matches('a')
    assert aut1.matches('aa')
    assert aut1.matches('aaaaaaaa')
    assert not aut1.matches('b')
    assert not aut1.matches('')