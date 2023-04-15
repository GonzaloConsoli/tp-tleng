from regex import Char, Union, Plus, Concat

# (a|b)+c
__regex__ = Concat(Plus(Union(Char('a'), Char('b'))), Char('c'))
