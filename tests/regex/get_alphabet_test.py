from regex import Empty

class TestGetAlphabet:
    def test_for_empty(self):
        regex = Empty()
        assert set() == regex.get_alphabet()