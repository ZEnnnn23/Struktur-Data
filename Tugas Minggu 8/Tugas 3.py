# ============================================================
# PRAKTIKUM — Chapter 5: Searching & Sorting
# Data Structures & Algorithms
# ============================================================

import random
import time


# ============================================================
# SOAL 1 — Modified Binary Search: countOccurrences
# ============================================================
# Menghitung berapa kali sebuah nilai muncul dalam sorted list.
# Kompleksitas: O(log n) menggunakan dua binary search.

def countOccurrences(sortedList, target):
    """Menghitung jumlah kemunculan target dalam sortedList (O log n)."""

    def findLeft(lst, val):
        """Cari indeks paling kiri kemunculan val."""
        lo, hi, result = 0, len(lst) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if lst[mid] == val:
                result = mid
                hi = mid - 1   # terus cari ke kiri
            elif lst[mid] < val:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    def findRight(lst, val):
        """Cari indeks paling kanan kemunculan val."""
        lo, hi, result = 0, len(lst) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if lst[mid] == val:
                result = mid
                lo = mid + 1   # terus cari ke kanan
            elif lst[mid] < val:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    left = findLeft(sortedList, target)
    if left == -1:
        return 0   # target tidak ditemukan
    right = findRight(sortedList, target)
    return right - left + 1


# --- Uji Soal 1 ---
print("=" * 55)
print("SOAL 1 — countOccurrences (Modified Binary Search)")
print("=" * 55)
arr = [1, 2, 4, 4, 4, 4, 7, 9, 12]
print(f"Array  : {arr}")
print(f"countOccurrences(..., 4)  → {countOccurrences(arr, 4)}  (expected: 4)")
print(f"countOccurrences(..., 5)  → {countOccurrences(arr, 5)}  (expected: 0)")
print(f"countOccurrences(..., 1)  → {countOccurrences(arr, 1)}  (expected: 1)")
print(f"countOccurrences(..., 12) → {countOccurrences(arr, 12)}  (expected: 1)")
print()


# ============================================================
# SOAL 2 — Bubble Sort dengan Analisis Langkah
# ============================================================
# Modifikasi bubbleSort agar:
#   • Mengembalikan tuple (sorted_list, total_comparisons, total_swaps, passes_used)
#   • Early termination jika tidak ada swap dalam satu pass
#   • Mencetak state array setelah setiap pass

def bubbleSort(theSeq):
    """
    Bubble sort dengan early termination dan analisis langkah.
    Returns: (sorted_list, total_comparisons, total_swaps, passes_used)
    """
    seq = list(theSeq)   # salin agar tidak mengubah asli
    n = len(seq)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            total_comparisons += 1
            if seq[j] > seq[j + 1]:
                seq[j], seq[j + 1] = seq[j + 1], seq[j]
                total_swaps += 1
                swapped = True
        passes_used += 1
        print(f"  Pass {passes_used}: {seq}")
        if not swapped:   # early termination
            break

    return (seq, total_comparisons, total_swaps, passes_used)


# --- Uji Soal 2 ---
print("=" * 55)
print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
print("=" * 55)

for test_input in ([5, 1, 4, 2, 8], [1, 2, 3, 4, 5]):
    print(f"\nInput: {test_input}")
    result, comps, swaps, passes = bubbleSort(test_input)
    print(f"  Sorted       : {result}")
    print(f"  Comparisons  : {comps}")
    print(f"  Swaps        : {swaps}")
    print(f"  Passes used  : {passes}")

print("""
Penjelasan perbedaan jumlah pass:
  [5, 1, 4, 2, 8] → membutuhkan lebih banyak pass karena elemen
    banyak yang tidak pada posisi benar; swap terjadi di hampir
    setiap pass.
  [1, 2, 3, 4, 5] → sudah terurut; pass pertama tidak menghasilkan
    swap sama sekali, sehingga early termination langsung aktif
    dan algoritma berhenti setelah 1 pass saja.
""")


# ============================================================
# SOAL 3 — Hybrid Sort
# ============================================================
# Gunakan insertion sort jika panjang sub-array <= threshold,
# selection sort jika lebih besar.
# Bandingkan jumlah total operasi pada array random 50, 100, 500 elemen.

def insertionSortCount(seq):
    """Insertion sort, returns (sorted, comparisons, swaps)."""
    a = list(seq)
    comps = swaps = 0
    for i in range(1, len(a)):
        value = a[i]
        pos = i
        while pos > 0:
            comps += 1
            if value < a[pos - 1]:
                a[pos] = a[pos - 1]
                swaps += 1
                pos -= 1
            else:
                break
        a[pos] = value
    return a, comps, swaps


def selectionSortCount(seq):
    """Selection sort, returns (sorted, comparisons, swaps)."""
    a = list(seq)
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        minIdx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[minIdx]:
                minIdx = j
        if minIdx != i:
            a[i], a[minIdx] = a[minIdx], a[i]
            swaps += 1
    return a, comps, swaps


def hybridSort(theSeq, threshold=10):
    """
    Hybrid sort: insertion sort jika len(sub-array) <= threshold,
    selection sort jika lebih besar.
    Returns: (sorted_list, total_comparisons, total_swaps)
    """
    seq = list(theSeq)
    n = len(seq)
    total_comps = total_swaps = 0

    if n <= threshold:
        seq, c, s = insertionSortCount(seq)
    else:
        # Bagi menjadi blok-blok berukuran threshold
        # Sortir tiap blok dengan insertion sort
        for start in range(0, n, threshold):
            end = min(start + threshold, n)
            block = seq[start:end]
            sorted_block, c, s = insertionSortCount(block)
            seq[start:end] = sorted_block
            total_comps += c
            total_swaps += s

        # Merge blok-blok yang sudah terurut menggunakan selection sort
        # (sederhana: lakukan selection sort pada keseluruhan array,
        #  tapi karena blok sudah terurut, jumlah operasinya berkurang)
        # Alternatif: gunakan selection sort langsung pada full array
        # sesuai soal ("selection sort jika lebih besar")
        full_sorted, c, s = selectionSortCount(seq)
        seq = full_sorted
        total_comps += c
        total_swaps += s

    return seq, total_comps, total_swaps


# --- Uji Soal 3 ---
print("=" * 55)
print("SOAL 3 — Hybrid Sort: Perbandingan Operasi")
print("=" * 55)
print(f"\n{'Ukuran':>8} | {'Hybrid':>14} | {'Insertion':>14} | {'Selection':>14}")
print("-" * 58)

for size in [50, 100, 500]:
    arr = random.sample(range(size * 10), size)
    _, hc, hs = hybridSort(arr[:], threshold=10)
    _, ic, is_ = insertionSortCount(arr[:])
    _, sc, ss = selectionSortCount(arr[:])
    hybrid_total = hc + hs
    insert_total = ic + is_
    select_total = sc + ss
    print(f"{size:>8} | {hybrid_total:>14,} | {insert_total:>14,} | {select_total:>14,}")

print("\n(nilai = total comparisons + swaps)")
print()


# ============================================================
# SOAL 4 — Merge Tiga Sorted Lists
# ============================================================
# Gabungkan tiga sorted list menjadi satu sorted list dalam O(n)
# menggunakan tiga pointer dalam satu pass.

def mergeThreeSortedLists(listA, listB, listC):
    """
    Merge tiga sorted list dalam O(n) menggunakan tiga pointer.
    Tidak boleh memanggil merge dua list secara bertahap.
    """
    result = []
    i = j = k = 0
    lenA, lenB, lenC = len(listA), len(listB), len(listC)

    while i < lenA or j < lenB or k < lenC:
        # Ambil nilai saat ini (infinity jika pointer sudah habis)
        a = listA[i] if i < lenA else float('inf')
        b = listB[j] if j < lenB else float('inf')
        c = listC[k] if k < lenC else float('inf')

        minimum = min(a, b, c)
        result.append(minimum)

        # Majukan pointer yang nilainya dipilih
        # (jika ada duplikat, majukan hanya satu pointer)
        if minimum == a:
            i += 1
        elif minimum == b:
            j += 1
        else:
            k += 1

    return result


# --- Uji Soal 4 ---
print("=" * 55)
print("SOAL 4 — mergeThreeSortedLists")
print("=" * 55)

test_cases = [
    ([1, 5, 9], [2, 6, 10], [3, 4, 7]),
    ([2, 8, 15, 23], [4, 6, 20], [1, 9, 11]),
    ([], [1, 2], [3]),
    ([5], [3], [1]),
]

for a, b, c in test_cases:
    result = mergeThreeSortedLists(a, b, c)
    print(f"  {a} + {b} + {c}")
    print(f"  → {result}\n")


# ============================================================
# SOAL 5 — Inversions Counter
# ============================================================
# Inversion: pasangan (i, j) di mana i < j tapi arr[i] > arr[j].
# a) countInversionsNaive  — brute force O(n²)
# b) countInversionsSmart — modifikasi merge sort O(n log n)

def countInversionsNaive(arr):
    """Hitung inversions dengan brute force O(n²)."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def countInversionsSmart(arr):
    """Hitung inversions menggunakan modifikasi merge sort O(n log n)."""

    def mergeCount(left, right):
        result = []
        inversions = 0
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                # Semua elemen left[i:] lebih besar dari right[j]
                result.append(right[j])
                inversions += len(left) - i
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result, inversions

    def sortCount(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, lc = sortCount(a[:mid])
        right, rc = sortCount(a[mid:])
        merged, sc = mergeCount(left, right)
        return merged, lc + rc + sc

    _, total = sortCount(list(arr))
    return total


# --- Uji Soal 5: kebenaran ---
print("=" * 55)
print("SOAL 5 — Inversions Counter")
print("=" * 55)

test_arrs = [
    [2, 4, 1, 3, 5],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [3, 1, 2],
]

print("\nVerifikasi kebenaran hasil:")
for a in test_arrs:
    naive = countInversionsNaive(a)
    smart = countInversionsSmart(a)
    status = "✓" if naive == smart else "✗ MISMATCH"
    print(f"  {str(a):35} Naive={naive:3}  Smart={smart:3}  {status}")

# --- Uji Soal 5: perbandingan waktu ---
print("\nPerbandingan waktu eksekusi:")
print(f"{'Ukuran':>8} | {'Naive (s)':>12} | {'Smart (s)':>12}")
print("-" * 38)

for size in [1000, 5000, 10000]:
    arr = random.sample(range(size * 2), size)

    start = time.perf_counter()
    countInversionsNaive(arr)
    t_naive = time.perf_counter() - start

    start = time.perf_counter()
    countInversionsSmart(arr)
    t_smart = time.perf_counter() - start

    print(f"{size:>8} | {t_naive:>12.4f} | {t_smart:>12.4f}")

print("""
Penjelasan mengapa merge sort lebih cepat:
  countInversionsNaive: O(n²) — membandingkan setiap pasangan (i, j),
    sehingga untuk n=10.000 terdapat ~50 juta perbandingan.

  countInversionsSmart: O(n log n) — saat merge sort menggabungkan
    dua sub-array yang sudah terurut, jika elemen kanan lebih kecil
    dari elemen kiri, seluruh sisa sub-array kiri pasti membentuk
    inversion dengan elemen kanan tersebut. Kita langsung menambahkan
    len(left) - i tanpa iterasi satu per satu, sehingga jumlah operasi
    jauh lebih kecil.
""")