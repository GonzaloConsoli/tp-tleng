from regex import Char, Union, Plus, Concat

# (a|b)cc+
__regex__ = Concat(Concat(Union(Char('a'), Char('b')),
                   Char('c')), Plus(Char('c')))
