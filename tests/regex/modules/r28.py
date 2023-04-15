from regex import Char, Concat, Plus, Union, Star

# (a|b|c)+d(e|f)*g
__regex__ = Concat(
    Plus(Union(Char('a'), Union(Char('b'), Char('c')))),
    Concat(Char('d'), Concat(Star(Union(Char('e'), Char('f'))), Char('g')))
)
