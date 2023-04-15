from regex import Char, Concat

# abc
__regex__ = Concat(Char('a'), Concat(Char('b'), Char('c')))
