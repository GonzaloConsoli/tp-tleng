from regex import Char, Union, Star, Concat

# (a|b)*c
__regex__ = Concat(Star(Union(Char('a'), Char('b'))), Char('c'))
