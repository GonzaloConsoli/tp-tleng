from automata.afnd import AFND
from automata.afnd import SpecialSymbol


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

def test_nd_to_d():
    afnd = AFND()
    afnd.add_state(0)
    afnd.mark_initial_state(0)
    afnd.add_state(3, final=True)
    afnd.add_state(2)
    afnd.add_state(1)

    afnd.add_transition(0, 0, "a")
    afnd.add_transition(0, 0, "b")
    afnd.add_transition(2, 3, "c")
    afnd.add_transition(3, 3, "c")
    afnd.add_transition(1, 2, "b")
    afnd.add_transition(0, 1, "a")

    afnd.normalize_states()

    afd = afnd.to_afd()
    
    assert not afd.matches('ab')
    assert not afd.matches('a')
    assert afd.matches('abc')
    assert not afd.matches('abbc')
    assert afd.matches('aaabc')
    assert afd.matches('abbbabccc')

def test_conLambda():
    afnd = AFND()
    afnd.add_state(0)
    afnd.mark_initial_state(0)
    afnd.add_state(2, final=True)
    afnd.add_state(1)


    afnd.add_transition(0, 0, "a")
    afnd.add_transition(0, 0, "b")
    afnd.add_transition(0, 1, "c")
    afnd.add_transition(1, 1, "c")
    afnd.add_transition(1, 2, SpecialSymbol.Lambda)
    afnd.add_transition(2, 2, "a")
    afnd.add_transition(2, 2, "b")

    afnd.normalize_states()

    afd = afnd.to_afd()
    
    assert not afd.matches('ab')
    assert not afd.matches('a')
    assert afd.matches('abc')
    assert afd.matches('abbc')
    assert afd.matches('aaabc')
    assert afd.matches('abbbabccc')
    assert not afd.matches('abcccabc')
 