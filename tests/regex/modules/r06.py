from regex import Char, Union

# a|b|c
__regex__ = Union(Char('a'), Union(Char('b'), Char('c')))
