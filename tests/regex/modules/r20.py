from regex import Star, Union, Char, Plus

# a*|b+
__regex__ = Union(Star(Char('a')), Plus(Char('b')))
