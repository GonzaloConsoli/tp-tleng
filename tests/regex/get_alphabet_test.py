from regex import Empty

class GetAlphabetTest:
    def empty_alphabet_is_empty(self):
        regex = Empty()
        assert set() == regex.get_alphabet()