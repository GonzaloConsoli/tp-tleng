from automata.afd import AFD


def test_minimization():
    aut1 = AFD()
    aut1.add_state(0)
    aut1.add_state(1)
    aut1.add_state(2)
    aut1.add_state(3, True)
    aut1.add_state(4, True)
    aut1.add_state(5, True)
    aut1.add_transition(0, 1, "a")
    aut1.add_transition(0, 0, "b")
    aut1.add_transition(1, 2, "a")
    aut1.add_transition(1, 0, "b")
    aut1.add_transition(2, 3, "a")
    aut1.add_transition(2, 0, "b")
    aut1.add_transition(3, 3, "a")
    aut1.add_transition(3, 4, "b")
    aut1.add_transition(3, 4, "b")
    aut1.add_transition(4, 4, "b")
    aut1.add_transition(4, 5, "a")
    aut1.add_transition(5, 3, "a")
    aut1.add_transition(5, 4, "b")
    aut1.mark_initial_state(0)

    obtained_min = aut1.minimize()

    expected_min = AFD()
    expected_min.add_state(1)
    expected_min.add_state(2)
    expected_min.add_state(3)
    expected_min.add_state(4, True)
    expected_min.add_transition(1, 2, "a")
    expected_min.add_transition(1, 1, "b")
    expected_min.add_transition(2, 1, "b")
    expected_min.add_transition(2, 3, "a")
    expected_min.add_transition(3, 4, "a")
    expected_min.add_transition(3, 1, "b")
    expected_min.add_transition(4, 4, "a")
    expected_min.add_transition(4, 4, "b")
    expected_min.mark_initial_state(1)

    assert obtained_min == expected_min