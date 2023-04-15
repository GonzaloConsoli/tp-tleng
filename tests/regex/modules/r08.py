from regex import Char, Concat, Union

# a|bc
__regex__ = Union(Char('a'), Concat(Char('b'), Char('c')))
