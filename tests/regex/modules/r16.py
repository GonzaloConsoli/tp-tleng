from regex import Char, Plus, Union

# (a|b)+
__regex__ = Plus(Union(Char('a'), Char('b')))
