from regex import Char, Concat

# ab
__regex__ = Concat(Char('a'), Char('b'))
