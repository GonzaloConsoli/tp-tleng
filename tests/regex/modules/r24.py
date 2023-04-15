from regex import Char, Plus, Union, Concat

# (a|b)cc+
__regex__ = Concat(Concat(Union(Char('a'), Char('b')),
                   Char('c')), Plus(Char('c')))
