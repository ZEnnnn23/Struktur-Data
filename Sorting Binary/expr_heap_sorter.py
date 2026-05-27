"""
ExprHeapSorter — Implementasi Bab 13
Mencakup:
  1. Expression Tree Builder & Evaluator   (antrian token + rekursi)
  2. In-Place Max-Heap Construction        (sift-down dari bawah ke atas)
  3. Heapsort In-Place                     (extract + sift-down)
  4. Complete Tree Validator               (cek index array level-by-level)
"""

from typing import List, Optional
from collections import deque


class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr   = expr_str
        self.values: List[int] = []

    # =========================================================
    # 1. EXPRESSION TREE BUILDER & EVALUATOR
    # =========================================================

    def parse_and_evaluate(self) -> List[int]:
        """
        Membangun pohon ekspresi dari self.expr, mengevaluasi, mengembalikan
        list nilai integer (hasil evaluasi setiap subexpresi).
        """
        tokens = deque(self.expr.replace(" ", ""))   # hapus spasi, buat queue
        root   = self._build_tree(tokens)
        result = self._eval_tree(root)
        # _eval_tree mengembalikan satu nilai integer; bungkus dalam list
        self.values = [int(result)]
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Rekursif, mengikuti pola Listing 13.9:
          '(' → buat left child → baca operator → buat right child → ')' buang
          operand → buat leaf node
        Node direpresentasikan sebagai dict: {'val', 'left', 'right'}
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            # Buat node interior
            node = {'val': None, 'left': None, 'right': None}

            # Proses left subtree
            node['left'] = self._build_tree(tokens)

            # Token berikutnya pasti operator
            if not tokens:
                raise ValueError("Ekspresi tidak valid: operator tidak ditemukan")
            op = tokens.popleft()
            if op not in ('+', '-', '*', '/', '%'):
                raise ValueError(f"Token tidak valid sebagai operator: '{op}'")
            node['val'] = op

            # Proses right subtree
            node['right'] = self._build_tree(tokens)

            # Buang ')' penutup
            if not tokens:
                raise ValueError("Ekspresi tidak valid: ')' tidak ditemukan")
            closing = tokens.popleft()
            if closing != ')':
                raise ValueError(f"Diharapkan ')', ditemukan '{closing}'")

            return node

        else:
            # Token adalah operand (digit atau huruf variabel)
            return {'val': token, 'left': None, 'right': None}

    def _eval_tree(self, node: Optional[dict]):
        """
        Evaluasi postorder: rekursi ke kiri dan kanan dahulu, lalu terapkan operator.
        Mengembalikan nilai numerik (int atau float).
        Raise ValueError untuk pembagian nol atau variabel tidak terdefinisi.
        """
        if node is None:
            raise ValueError("Node kosong dalam pohon ekspresi")

        # Leaf node → operand
        if node['left'] is None and node['right'] is None:
            val = node['val']
            # Cek apakah digit
            if val.lstrip('-').isdigit():
                return int(val)
            # Cek apakah float
            try:
                return float(val)
            except ValueError:
                raise ValueError(f"Variabel '{val}' tidak terdefinisi")

        # Interior node → operator
        left_val  = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])
        op        = node['val']

        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Pembagian dengan nol")
            return left_val / right_val
        elif op == '%':
            if right_val == 0:
                raise ValueError("Modulo dengan nol")
            return left_val % right_val
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    # =========================================================
    # 2 & 3. HEAPSORT IN-PLACE
    # =========================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan arr secara ascending menggunakan in-place heapsort.
        Fase 1: Bangun max-heap dari bawah ke atas (sift-down dari n//2-1 s.d. 0).
        Fase 2: Ekstrak max berulang kali dengan swap root ↔ akhir, lalu sift-down.
        Tidak ada alokasi array tambahan — hanya variabel index.
        """
        n = len(arr)
        if n <= 1:
            return arr

        # --- Fase 1: Bangun max-heap in-place ---
        # Mulai dari node internal terakhir (index n//2 - 1) turun ke 0
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # --- Fase 2: Ekstrak elemen dari heap, tempatkan di akhir array ---
        for end in range(n - 1, 0, -1):
            # Swap root (max) ke posisi end
            arr[0], arr[end] = arr[end], arr[0]
            # Kurangi ukuran heap, pulihkan heap order
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Pindahkan arr[idx] ke bawah sampai heap order property terpenuhi.
        Gunakan rumus: left = 2*idx+1, right = 2*idx+2
        Hanya membandingkan dan menukar — O(1) ruang tambahan per panggilan.
        """
        while True:
            left    = 2 * idx + 1
            right   = 2 * idx + 2
            largest = idx           # asumsikan current node adalah terbesar

            # Bandingkan dengan anak kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # Bandingkan dengan anak kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # Jika node saat ini sudah yang terbesar → selesai
            if largest == idx:
                break

            # Tukar dan lanjutkan sift-down ke bawah
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    # =========================================================
    # 4. COMPLETE TREE VALIDATOR
    # =========================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Validasi apakah array arr merepresentasikan complete binary tree.

        Properti complete binary tree dalam pemetaan array:
          - Semua node indeks 0..n-1 harus terisi (tidak boleh ada 'lubang')
          - Untuk setiap node i:
              jika 2*i+1 >= n → node i adalah leaf (tidak punya anak kiri)
              jika 2*i+2 >= n → node i tidak punya anak kanan
          - Tidak boleh: node punya anak kanan tapi tidak punya anak kiri

        Karena array Python selalu mengisi indeks 0 s.d. n-1 secara berurutan,
        kita perlu memastikan tidak ada gap — artinya array adalah pemetaan valid
        dari complete binary tree jika memenuhi aturan berikut:
          Setelah ditemukan node pertama yang tidak punya anak kiri, semua node
          berikutnya harus leaf.
        """
        n = len(arr)
        if n == 0:
            return True

        # Flag: setelah bertemu node non-full (tidak punya 2 anak), semua
        # node berikutnya harus leaf
        found_non_full = False

        for i in range(n):
            left  = 2 * i + 1
            right = 2 * i + 2

            has_left  = left  < n
            has_right = right < n

            if found_non_full:
                # Setelah node non-full, tidak boleh ada anak lagi
                if has_left or has_right:
                    return False
            else:
                if has_left and has_right:
                    # Node penuh → lanjut
                    continue
                elif has_left and not has_right:
                    # Punya anak kiri tapi tidak kanan → node non-full terakhir valid
                    found_non_full = True
                elif not has_left and has_right:
                    # Tidak mungkin punya kanan tanpa kiri → bukan complete tree
                    return False
                else:
                    # Tidak punya anak sama sekali → leaf, set flag
                    found_non_full = True

        return True


# =========================================================
# Fungsi bantu: visualisasi pohon ekspresi (opsional, untuk debug)
# =========================================================
def print_tree(node, indent=0, label="ROOT"):
    if node is None:
        return
    print(" " * indent + f"[{label}] {node['val']}")
    if node['left'] or node['right']:
        print_tree(node['left'],  indent + 4, "L")
        print_tree(node['right'], indent + 4, "R")


# =========================================================
# Test / Demo
# =========================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. EXPRESSION TREE — ((8*5)+(9/(7-4)))")
    print("=" * 60)
    expr_str = "((8*5)+(9/(7-4)))"
    sorter   = ExprHeapSorter(expr_str)

    tokens_debug = deque(expr_str.replace(" ", ""))
    root_debug   = sorter._build_tree(tokens_debug)
    print("Struktur pohon:")
    print_tree(root_debug)
    result = sorter._eval_tree(root_debug)
    print(f"Hasil evaluasi: {result}  (expected: 8*5 + 9/3 = 40 + 3 = 43)")
    print(f"parse_and_evaluate() → {sorter.parse_and_evaluate()}")

    print()
    print("=" * 60)
    print("Uji ekspresi sederhana: (5+8)")
    print("=" * 60)
    s2 = ExprHeapSorter("(5+8)")
    print(f"Hasil: {s2.parse_and_evaluate()}  (expected: [13])")

    print()
    print("=" * 60)
    print("Uji pembagian nol: (9/(3-3))")
    print("=" * 60)
    s3 = ExprHeapSorter("(9/(3-3))")
    try:
        s3.parse_and_evaluate()
    except ValueError as e:
        print(f"ValueError tertangkap: {e}  ✓")

    print()
    print("=" * 60)
    print("2 & 3. HEAPSORT IN-PLACE")
    print("=" * 60)
    test_cases = [
        [10, 51, 2, 18, 4, 31, 13, 5, 23, 64, 29],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 3],
        [64, 51, 31, 18, 29, 2, 13, 5, 10, 4, 23],
    ]
    s4 = ExprHeapSorter("")
    for tc in test_cases:
        original = tc[:]
        result   = s4.heapsort_inplace(tc)
        expected = sorted(original)
        status   = "✓" if result == expected else "✗"
        print(f"  {status}  Input: {original}")
        print(f"     Output: {result}")
        print(f"     Expected: {expected}")

    print()
    print("=" * 60)
    print("4. COMPLETE TREE VALIDATOR")
    print("=" * 60)
    # Array terurut hasil heapsort bukan complete heap, tapi array itu sendiri
    # representasi array yang valid (semua indeks 0..n-1 terisi) → selalu complete tree
    arrays = [
        ([100, 84, 71, 60, 23, 12, 29, 1, 37, 4], True,  "max-heap valid"),
        ([1, 2, 3, 4, 5, 6, 7],                   True,  "complete binary tree sempurna"),
        ([1, 2, 3, 4, 5, 6],                       True,  "complete tree (level terakhir tidak penuh)"),
        ([],                                        True,  "array kosong"),
        ([42],                                      True,  "satu elemen"),
    ]
    s5 = ExprHeapSorter("")
    for arr, expected, desc in arrays:
        res    = s5.is_complete_tree(arr)
        status = "✓" if res == expected else "✗"
        print(f"  {status}  {desc}: arr={arr} → {res} (expected {expected})")
