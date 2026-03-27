# ============================================================
#  Big Integer ADT  —  Tugas Praktikum Struktur Data
# ============================================================
#  Soal 1a : implementasi dengan Singly Link List
#  Soal 1b : implementasi dengan Python list
#  Soal 2  : assignment combo operators untuk kedua kelas
# ============================================================


# ==============================================================
#  SOAL 1A — BigIntegerLinkList  (Singly Link List)
# ==============================================================

class _Node:
    """Satu node dalam singly link list, menyimpan satu digit."""
    def __init__(self, digit):
        self.digit = digit   # int 0-9
        self.next  = None


class BigIntegerLinkList:
    """
    Big Integer ADT menggunakan Singly Link List.

    Digit disimpan dari yang paling tidak signifikan (least-significant)
    ke yang paling signifikan.  Contoh: 45839 disimpan sebagai
        head -> 9 -> 8 -> 3 -> 5 -> 4 -> None

    Tanda negatif disimpan dalam atribut boolean self._negative.
    """

    # ------------------------------------------------------------------ #
    #  Konstruktor                                                         #
    # ------------------------------------------------------------------ #
    def __init__(self, initValue="0"):
        self._head     = None
        self._negative = False
        self._build_from_string(str(initValue))

    def _build_from_string(self, s: str):
        """Membangun link list dari string angka."""
        s = s.strip()
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        s = s.lstrip('0') or '0'          # hapus leading zero, jaga "0"

        # Masukkan digit dari kiri ke kanan (most-significant dulu),
        # lalu prepend ke head sehingga head akhirnya menunjuk least-significant.
        self._head = None
        for ch in s:                   # kiri = most-significant
            node      = _Node(int(ch))
            node.next = self._head     # prepend → head selalu = least-significant
            self._head = node

    # ------------------------------------------------------------------ #
    #  toString                                                            #
    # ------------------------------------------------------------------ #
    def toString(self) -> str:
        """Mengembalikan representasi string dari big integer ini."""
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        result = ''.join(reversed(digits)) or '0'
        return ('-' + result) if self._negative else result

    def __repr__(self):
        return f"BigIntegerLinkList('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ------------------------------------------------------------------ #
    #  Helper: konversi ke/dari int Python                                 #
    # ------------------------------------------------------------------ #
    def _to_int(self) -> int:
        return int(self.toString())

    @classmethod
    def _from_int(cls, value: int) -> "BigIntegerLinkList":
        return cls(str(value))

    # ------------------------------------------------------------------ #
    #  comparable  (<, <=, >, >=, ==, !=)                                 #
    # ------------------------------------------------------------------ #
    def comparable(self, other: "BigIntegerLinkList", op: str) -> bool:
        """
        Membandingkan self dengan other menggunakan operator op.
        op dapat berupa: '<', '<=', '>', '>=', '==', '!='
        """
        a, b = self._to_int(), other._to_int()
        ops = {
            '<' : a <  b,
            '<=': a <= b,
            '>' : a >  b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return ops[op]

    def __lt__ (self, other): return self.comparable(other, '<' )
    def __le__ (self, other): return self.comparable(other, '<=')
    def __gt__ (self, other): return self.comparable(other, '>' )
    def __ge__ (self, other): return self.comparable(other, '>=')
    def __eq__ (self, other): return self.comparable(other, '==')
    def __ne__ (self, other): return self.comparable(other, '!=')

    # ------------------------------------------------------------------ #
    #  arithmetic  (+, -, *, //, %, **)                                   #
    # ------------------------------------------------------------------ #
    def arithmetic(self, rhsInt: "BigIntegerLinkList", op: str) -> "BigIntegerLinkList":
        """
        Mengembalikan BigIntegerLinkList baru hasil operasi aritmatika.
        op dapat berupa: '+', '-', '*', '//', '%', '**'
        """
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '+' : a +  b,
            '-' : a -  b,
            '*' : a *  b,
            '//': a // b,
            '%' : a %  b,
            '**': a ** b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return self._from_int(ops[op])

    def __add__ (self, o): return self.arithmetic(o, '+' )
    def __sub__ (self, o): return self.arithmetic(o, '-' )
    def __mul__ (self, o): return self.arithmetic(o, '*' )
    def __floordiv__(self, o): return self.arithmetic(o, '//')
    def __mod__ (self, o): return self.arithmetic(o, '%' )
    def __pow__ (self, o): return self.arithmetic(o, '**')

    # ------------------------------------------------------------------ #
    #  bitwise  (|, &, ^, <<, >>)                                         #
    # ------------------------------------------------------------------ #
    def bitwise_ops(self, rhsInt: "BigIntegerLinkList", op: str) -> "BigIntegerLinkList":
        """
        Mengembalikan BigIntegerLinkList baru hasil operasi bitwise.
        op dapat berupa: '|', '&', '^', '<<', '>>'
        """
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '|' : a |  b,
            '&' : a &  b,
            '^' : a ^  b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return self._from_int(ops[op])

    def __or__       (self, o): return self.bitwise_ops(o, '|' )
    def __and__      (self, o): return self.bitwise_ops(o, '&' )
    def __xor__      (self, o): return self.bitwise_ops(o, '^' )
    def __lshift__   (self, o): return self.bitwise_ops(o, '<<')
    def __rshift__   (self, o): return self.bitwise_ops(o, '>>')

    # ------------------------------------------------------------------ #
    #  SOAL 2 — Assignment combo operators                                 #
    #  (+=, -=, *=, //=, %=, **=, <<=, >>=, |=, &=, ^=)                 #
    # ------------------------------------------------------------------ #
    def __iadd__     (self, o): return self + o
    def __isub__     (self, o): return self - o
    def __imul__     (self, o): return self * o
    def __ifloordiv__(self, o): return self // o
    def __imod__     (self, o): return self % o
    def __ipow__     (self, o): return self ** o
    def __ilshift__  (self, o): return self << o
    def __irshift__  (self, o): return self >> o
    def __ior__      (self, o): return self | o
    def __iand__     (self, o): return self & o
    def __ixor__     (self, o): return self ^ o


# ==============================================================
#  SOAL 1B — BigIntegerList  (Python list)
# ==============================================================

class BigIntegerList:
    """
    Big Integer ADT menggunakan Python list.

    Digit disimpan dari yang paling tidak signifikan (least-significant)
    ke yang paling signifikan.  Contoh: 45839 disimpan sebagai
        self._digits = [9, 8, 3, 5, 4]

    Tanda negatif disimpan dalam atribut boolean self._negative.
    """

    # ------------------------------------------------------------------ #
    #  Konstruktor                                                         #
    # ------------------------------------------------------------------ #
    def __init__(self, initValue="0"):
        self._digits   = []
        self._negative = False
        self._build_from_string(str(initValue))

    def _build_from_string(self, s: str):
        s = s.strip()
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        s = s.lstrip('0') or '0'
        # Simpan digit dari least-significant ke most-significant
        self._digits = [int(ch) for ch in reversed(s)]

    # ------------------------------------------------------------------ #
    #  toString                                                            #
    # ------------------------------------------------------------------ #
    def toString(self) -> str:
        result = ''.join(str(d) for d in reversed(self._digits)) or '0'
        return ('-' + result) if self._negative else result

    def __repr__(self):
        return f"BigIntegerList('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ------------------------------------------------------------------ #
    #  Helper                                                              #
    # ------------------------------------------------------------------ #
    def _to_int(self) -> int:
        return int(self.toString())

    @classmethod
    def _from_int(cls, value: int) -> "BigIntegerList":
        return cls(str(value))

    # ------------------------------------------------------------------ #
    #  comparable                                                          #
    # ------------------------------------------------------------------ #
    def comparable(self, other: "BigIntegerList", op: str) -> bool:
        a, b = self._to_int(), other._to_int()
        ops = {
            '<' : a <  b,
            '<=': a <= b,
            '>' : a >  b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return ops[op]

    def __lt__ (self, other): return self.comparable(other, '<' )
    def __le__ (self, other): return self.comparable(other, '<=')
    def __gt__ (self, other): return self.comparable(other, '>' )
    def __ge__ (self, other): return self.comparable(other, '>=')
    def __eq__ (self, other): return self.comparable(other, '==')
    def __ne__ (self, other): return self.comparable(other, '!=')

    # ------------------------------------------------------------------ #
    #  arithmetic                                                          #
    # ------------------------------------------------------------------ #
    def arithmetic(self, rhsInt: "BigIntegerList", op: str) -> "BigIntegerList":
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '+' : a +  b,
            '-' : a -  b,
            '*' : a *  b,
            '//': a // b,
            '%' : a %  b,
            '**': a ** b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return self._from_int(ops[op])

    def __add__      (self, o): return self.arithmetic(o, '+' )
    def __sub__      (self, o): return self.arithmetic(o, '-' )
    def __mul__      (self, o): return self.arithmetic(o, '*' )
    def __floordiv__ (self, o): return self.arithmetic(o, '//')
    def __mod__      (self, o): return self.arithmetic(o, '%' )
    def __pow__      (self, o): return self.arithmetic(o, '**')

    # ------------------------------------------------------------------ #
    #  bitwise                                                             #
    # ------------------------------------------------------------------ #
    def bitwise_ops(self, rhsInt: "BigIntegerList", op: str) -> "BigIntegerList":
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '|' : a |  b,
            '&' : a &  b,
            '^' : a ^  b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return self._from_int(ops[op])

    def __or__    (self, o): return self.bitwise_ops(o, '|' )
    def __and__   (self, o): return self.bitwise_ops(o, '&' )
    def __xor__   (self, o): return self.bitwise_ops(o, '^' )
    def __lshift__(self, o): return self.bitwise_ops(o, '<<')
    def __rshift__(self, o): return self.bitwise_ops(o, '>>')

    # ------------------------------------------------------------------ #
    #  SOAL 2 — Assignment combo operators                                 #
    # ------------------------------------------------------------------ #
    def __iadd__     (self, o): return self + o
    def __isub__     (self, o): return self - o
    def __imul__     (self, o): return self * o
    def __ifloordiv__(self, o): return self // o
    def __imod__     (self, o): return self % o
    def __ipow__     (self, o): return self ** o
    def __ilshift__  (self, o): return self << o
    def __irshift__  (self, o): return self >> o
    def __ior__      (self, o): return self | o
    def __iand__     (self, o): return self & o
    def __ixor__     (self, o): return self ^ o


# ==============================================================
#  TESTING — Demo semua operasi
# ==============================================================

def run_tests():
    sep = "=" * 60

    # ---- Soal 1a: Link List ----
    print(sep)
    print("SOAL 1A — BigIntegerLinkList")
    print(sep)

    a = BigIntegerLinkList("45839")
    b = BigIntegerLinkList("12345")

    print(f"a = {a}")
    print(f"b = {b}")

    print("\n-- toString --")
    print(f"  a.toString() = {a.toString()}")

    print("\n-- comparable --")
    print(f"  a > b  : {a.comparable(b, '>')}")
    print(f"  a < b  : {a.comparable(b, '<')}")
    print(f"  a == b : {a.comparable(b, '==')}")
    print(f"  a != b : {a.comparable(b, '!=')}")

    print("\n-- arithmetic --")
    print(f"  a + b  = {a + b}")
    print(f"  a - b  = {a - b}")
    print(f"  a * b  = {a * b}")
    print(f"  a // b = {a // b}")
    print(f"  a % b  = {a % b}")
    print(f"  a ** 2 = {a ** BigIntegerLinkList('2')}")

    print("\n-- bitwise --")
    print(f"  a | b  = {a | b}")
    print(f"  a & b  = {a & b}")
    print(f"  a ^ b  = {a ^ b}")
    print(f"  a << 2 = {a << BigIntegerLinkList('2')}")
    print(f"  a >> 2 = {a >> BigIntegerLinkList('2')}")

    print("\n-- SOAL 2: Assignment combo operators --")
    x = BigIntegerLinkList("1000")
    y = BigIntegerLinkList("250")
    print(f"  x={x}, y={y}")
    x += y;  print(f"  x += y  → {x}")
    x -= y;  print(f"  x -= y  → {x}")
    x *= y;  print(f"  x *= y  → {x}")
    x //= y; print(f"  x //= y → {x}")
    x %= y;  print(f"  x %= y  → {x}")
    x = BigIntegerLinkList("2")
    x **= BigIntegerLinkList("10"); print(f"  2 **= 10→ {x}")
    x = BigIntegerLinkList("60")
    x |=  BigIntegerLinkList("15"); print(f"  60 |= 15  → {x}")
    x &=  BigIntegerLinkList("12"); print(f"  x  &= 12  → {x}")
    x ^=  BigIntegerLinkList("5");  print(f"  x  ^= 5   → {x}")
    x <<= BigIntegerLinkList("2");  print(f"  x  <<= 2  → {x}")
    x >>= BigIntegerLinkList("1");  print(f"  x  >>= 1  → {x}")

    print()
    # ---- Soal 1b: Python List ----
    print(sep)
    print("SOAL 1B — BigIntegerList")
    print(sep)

    a2 = BigIntegerList("45839")
    b2 = BigIntegerList("12345")

    print(f"a = {a2}")
    print(f"b = {b2}")
    print(f"  internal digits (LSB first): {a2._digits}")

    print("\n-- arithmetic --")
    print(f"  a + b  = {a2 + b2}")
    print(f"  a - b  = {a2 - b2}")
    print(f"  a * b  = {a2 * b2}")
    print(f"  a // b = {a2 // b2}")
    print(f"  a % b  = {a2 % b2}")

    print("\n-- SOAL 2: Assignment combo operators --")
    x2 = BigIntegerList("500")
    y2 = BigIntegerList("150")
    x2 += y2; print(f"  500 += 150 → {x2}")
    x2 -= y2; print(f"  x  -= 150  → {x2}")
    x2 *= y2; print(f"  x  *= 150  → {x2}")
    x2 //= y2;print(f"  x  //= 150 → {x2}")

    print()
    print(sep)
    print("Semua tes selesai!")
    print(sep)


if __name__ == "__main__":
    run_tests()
