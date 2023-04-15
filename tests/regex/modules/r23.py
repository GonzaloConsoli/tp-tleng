from regex import Char, Union, Star, Concat

# (a|b)c*
__regex__ = Concat(Union(Char('a'), Char('b')), Star(Char('c')))
