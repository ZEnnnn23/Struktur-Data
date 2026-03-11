# Chapter 5 — Searching & Sorting

> Praktikum **Data Structures & Algorithms** — implementasi dan analisis algoritma pencarian & pengurutan dalam Python.

---

## Daftar Soal

| # | Topik | Kompleksitas |
|---|-------|-------------|
| 1 | Modified Binary Search — `countOccurrences` | O(log n) |
| 2 | Bubble Sort dengan Analisis Langkah | O(n²) / O(n) best |
| 3 | Hybrid Sort — Insertion + Selection | O(n²) |
| 4 | Merge Tiga Sorted Lists | O(n) |
| 5 | Inversions Counter — Naive & Merge Sort | O(n²) / O(n log n) |

---

## Soal 1 — `countOccurrences` (Modified Binary Search)

Menghitung berapa kali sebuah nilai muncul dalam sorted list dalam waktu **O(log n)**.

**Pendekatan:** Dua kali binary search — satu untuk menemukan indeks kemunculan **pertama** (batas kiri), satu lagi untuk kemunculan **terakhir** (batas kanan). Hasilnya adalah `right - left + 1`.

```python
countOccurrences([1, 2, 4, 4, 4, 4, 7, 9, 12], 4)  # → 4
countOccurrences([1, 2, 4, 4, 4, 4, 7, 9, 12], 5)  # → 0
```

---

## Soal 2 — Bubble Sort dengan Analisis Langkah

Modifikasi `bubbleSort()` agar:
- Mengembalikan tuple `(sorted_list, total_comparisons, total_swaps, passes_used)`
- Mengimplementasikan **early termination** (berhenti jika tidak ada swap dalam satu pass)
- Mencetak state array setelah setiap pass

**Hasil uji:**

```
Input: [5, 1, 4, 2, 8]
  Pass 1: [1, 4, 2, 5, 8]
  Pass 2: [1, 2, 4, 5, 8]
  Pass 3: [1, 2, 4, 5, 8]   ← early termination
  Passes used: 3

Input: [1, 2, 3, 4, 5]
  Pass 1: [1, 2, 3, 4, 5]   ← early termination
  Passes used: 1
```

> **Mengapa jumlah pass berbeda?** Array yang sudah terurut tidak menghasilkan satu pun swap pada pass pertama, sehingga early termination langsung aktif. Array acak membutuhkan lebih banyak pass karena banyak elemen yang belum pada posisi yang benar.

---

## Soal 3 — Hybrid Sort

Fungsi `hybridSort(theSeq, threshold=10)` yang menggunakan:
- **Insertion sort** jika panjang sub-array ≤ threshold
- **Selection sort** jika lebih besar

Perbandingan total operasi (comparisons + swaps) pada array random:

| Ukuran | Hybrid | Pure Insertion | Pure Selection |
|--------|--------|---------------|----------------|
| 50     | ~1.500 | ~1.100        | ~1.300         |
| 100    | ~5.600 | ~5.500        | ~5.000         |
| 500    | ~128.000 | ~125.000    | ~125.000       |

> Hybrid sort menggabungkan keunggulan keduanya: insertion sort efisien untuk data kecil (adaptif terhadap data hampir terurut), sedangkan selection sort meminimalkan jumlah swap.

---

## Soal 4 — `mergeThreeSortedLists`

Menggabungkan tiga sorted list menjadi satu sorted list dalam **O(n)** menggunakan **tiga pointer dalam satu pass** (tanpa memanggil merge dua list secara bertahap).

```python
mergeThreeSortedLists([1, 5, 9], [2, 6, 10], [3, 4, 7])
# → [1, 2, 3, 4, 5, 6, 7, 9, 10]
```

**Cara kerja:** Setiap iterasi membandingkan nilai terdepan dari ketiga list (menggunakan `float('inf')` jika suatu list sudah habis), memilih yang terkecil, menambahkannya ke result, lalu memajukan pointer yang bersangkutan.

---

## Soal 5 — Inversions Counter

Sebuah *inversion* adalah pasangan indeks `(i, j)` di mana `i < j` tetapi `arr[i] > arr[j]` — mengukur seberapa "tidak terurut" sebuah array.

### a) `countInversionsNaive` — O(n²)
Brute force: bandingkan setiap pasangan `(i, j)` dengan dua loop bersarang.

### b) `countInversionsSmart` — O(n log n)
Modifikasi merge sort: saat menggabungkan dua sub-array terurut, jika `right[j] < left[i]`, maka seluruh `left[i:]` membentuk inversion dengan `right[j]`, sehingga kita langsung menambahkan `len(left) - i` sekaligus.

**Perbandingan waktu eksekusi:**

| Ukuran | Naive (s) | Smart (s) |
|--------|-----------|-----------|
| 1.000  | ~0.021    | ~0.002    |
| 5.000  | ~0.560    | ~0.009    |
| 10.000 | ~2.250    | ~0.026    |

> Smart ~85× lebih cepat pada n=10.000 karena O(n log n) vs O(n²).

---

## Cara Menjalankan

Tidak ada dependensi eksternal — hanya menggunakan library standar Python.

```bash
python praktikum_searching_sorting.py
```

**Persyaratan:** Python 3.7+

---

## Struktur File

```
.
├── praktikum_searching_sorting.py   # Semua implementasi + uji
└── README.md
```

---

## Referensi Kompleksitas

| Algoritma | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge (3 lists) | O(n) | O(n) | O(n) | O(n) |
| Inversions Naive | O(n²) | O(n²) | O(n²) | O(1) |
| Inversions Smart | O(n log n) | O(n log n) | O(n log n) | O(n) |
