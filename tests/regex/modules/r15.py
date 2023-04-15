from regex import Plus, Char, Union

# a|b+
__regex__ = Union(Char('a'), Plus(Char('b')))
