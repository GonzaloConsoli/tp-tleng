from regex import Char, Concat, Plus

# (ab)+
__regex__ = Plus(Concat(Char('a'), Char('b')))
