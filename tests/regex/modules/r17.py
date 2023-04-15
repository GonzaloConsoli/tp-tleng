from regex import Char, Union, Star

# (a|b)*
__regex__ = Star(Union(Char('a'), Char('b')))
