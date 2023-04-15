from regex import Empty, Char, Concat

# ∅a
__regex__ = Concat(Empty(), Char('a'))
