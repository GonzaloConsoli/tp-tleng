from regex import Concat, Star, Char, Union

# (a|b)*(c|a)*
__regex__ = Concat(Star(Union(Char('a'), Char('b'))),
                   Star(Union(Char('c'), Char('a'))))
