from regex import Char, Concat, Star

# (ab)*
__regex__ = Star(Concat(Char('a'), Char('b')))
