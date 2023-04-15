from regex import Char, Concat, Union

# ab|cd
__regex__ = Union(Concat(Char('a'), Char('b')), Concat(Char('c'), Char('d')))
