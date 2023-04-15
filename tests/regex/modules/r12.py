from regex import Char, Lambda, Union

# a|λ
__regex__ = Union(Char('a'), Lambda())
