from regex import Lambda, Char, Concat

# abλ
__regex__ = Concat(Char('a'), Concat(Char('b'), Lambda()))
