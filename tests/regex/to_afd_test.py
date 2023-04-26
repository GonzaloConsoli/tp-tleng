from automata.afnd import AFND


def test_to_afd():
    afnd = AFND()
    afnd.add_state(0)
    afnd.mark_initial_state(0)
    afnd.add_state(1, final=True)
    afnd.add_state(2)

    afnd.add_transition(0, 0, "a")
    afnd.add_transition(0, 1, "a")
    afnd.add_transition(0, 2, "a")

    afnd.add_transition(1, 1, "b")

    afnd.add_transition(2, 1, "a")

    afnd.normalize_states()

    afd = afnd.to_afd()
    
    assert afd.matches('ab')
    assert afd.matches('a')
    assert not afd.matches('b')
    assert not afd.matches('')
    assert afd.matches('aaaab')
    assert afd.matches('aaaabbbb')

