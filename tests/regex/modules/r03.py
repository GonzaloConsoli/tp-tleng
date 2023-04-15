from regex import Char, Union

# a|b
__regex__ = Union(Char('a'), Char('b'))
