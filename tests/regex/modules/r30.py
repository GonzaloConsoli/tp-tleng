from regex import Char, Union

# a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z
__regex__ = Union(Char('a'), Union(Char('b'), Union(Char('c'), Union(Char('d'), Union(Char('e'), Union(
    Char('f'), Union(Char('g'), Union(Char('h'), Union(Char('i'), Union(Char('j'), Union(
        Char('k'), Union(Char('l'), Union(Char('m'), Union(Char('n'), Union(Char('o'), Union(
            Char('p'), Union(Char('q'), Union(Char('r'), Union(Char('s'), Union(Char('t'), Union(
                Char('u'), Union(Char('v'), Union(Char('w'), Union(Char('x'), Union(
                    Char('y'), Char('z'))))))))))))))))))))))))))
