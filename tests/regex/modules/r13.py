from regex import Empty, Char, Union

# a|∅
__regex__ = Union(Char('a'), Empty())
