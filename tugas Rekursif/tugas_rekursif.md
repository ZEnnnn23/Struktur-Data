# Tugas Rekursif & Backtracking

**Mata Kuliah:** Algoritma dan Pemrograman  
**Bahasa:** Python 3  
**Topik:** Algoritma Rekursif dan Backtracking

---

## Daftar Isi
1. [N-Queens Problem](#1-n-queens-problem)
2. [Knight's Tour Problem](#2-knights-tour-problem)
3. [Knapsack Problem](#3-knapsack-problem)
4. [Cara Menjalankan Program](#cara-menjalankan-program)

---

## 1. N-Queens Problem

### Deskripsi

Masalah N-Queens adalah menempatkan **N buah ratu** pada papan catur berukuran **N×N** sedemikian rupa sehingga tidak ada dua ratu yang saling menyerang. Dua ratu saling menyerang jika berada pada baris, kolom, atau diagonal yang sama.

### Konsep Algoritma

Algoritma menggunakan **backtracking rekursif**:
- Tempatkan ratu satu per satu, baris demi baris.
- Sebelum menempatkan ratu di kolom tertentu, cek apakah posisi aman (`is_safe_queens`).
- Jika aman, tempatkan ratu dan lanjut ke baris berikutnya (rekursi).
- Jika tidak ada kolom yang aman, **backtrack** ke baris sebelumnya dan coba kolom lain.

### Diagram Cara Kerja

```
Baris 0: coba kolom 0, 1, 2, ... → pilih yang aman
Baris 1: coba kolom 0, 1, 2, ... → pilih yang aman
...
Baris N-1: semua ratu ditempatkan → SOLUSI DITEMUKAN
                                  ↓ (jika tidak ada) → BACKTRACK
```

### Implementasi

```python
def is_safe_queens(board, row, col, n):
    # Cek kolom yang sama di baris sebelumnya
    for i in range(row):
        if board[i] == col:
            return False
    # Cek diagonal kiri atas
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i] == j:
            return False
        i -= 1; j -= 1
    # Cek diagonal kanan atas
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i] == j:
            return False
        i -= 1; j += 1
    return True


def solve_nqueens(board, row, n, solutions):
    if row == n:                          # Basis: semua ratu ditempatkan
        solutions.append(board[:])
        return
    for col in range(n):
        if is_safe_queens(board, row, col, n):
            board[row] = col
            solve_nqueens(board, row + 1, n, solutions)  # Rekursi
            board[row] = -1              # Backtrack
```

### Contoh Output (N=4)

```
Papan 4x4 - Solusi 1:

 .  Q  .  . 
 .  .  .  Q 
 Q  .  .  . 
 .  .  Q  . 

Posisi ratu per baris: [2, 4, 1, 3]
```

> Artinya: Ratu baris 1 di kolom 2, baris 2 di kolom 4, dst.

### Kompleksitas

| Aspek | Nilai |
|-------|-------|
| Waktu (worst case) | O(N!) |
| Ruang (rekursi) | O(N) |

---

## 2. Knight's Tour Problem

### Deskripsi

Tur Kuda adalah teka-teki papan catur di mana sebuah kuda harus **mengunjungi setiap petak tepat satu kali** menggunakan gerakan sah kuda (huruf L).

### Gerakan Sah Kuda

```
Kuda di posisi (x, y) dapat bergerak ke:
(x±2, y±1) atau (x±1, y±2)

Diagram (K = kuda, * = gerakan yang mungkin):
 .  *  .  *  .
 *  .  .  .  *
 .  .  K  .  .
 *  .  .  .  *
 .  *  .  *  .
```

### Konsep Algoritma

Menggunakan **backtracking rekursif** dengan optimasi **Warnsdorff's Heuristic**:
- Selalu pilih gerakan berikutnya ke petak dengan **jumlah gerakan valid terkecil** (degree terkecil).
- Heuristik ini sangat mempercepat pencarian solusi.
- Jika tidak ada gerakan valid → backtrack.

### Implementasi

```python
KNIGHT_MOVES = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

def get_degree(board, x, y, n):
    """Heuristic Warnsdorff: hitung jumlah gerakan valid dari (x,y)."""
    count = 0
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
            count += 1
    return count


def solve_knights_tour(board, x, y, move_num, n, path):
    if move_num == n * n:                # Basis: semua petak dikunjungi
        return True

    # Urutkan gerakan (Warnsdorff: degree terkecil lebih dulu)
    next_moves = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
            degree = get_degree(board, nx, ny, n)
            next_moves.append((degree, nx, ny))
    next_moves.sort()

    for _, nx, ny in next_moves:
        board[nx][ny] = move_num
        path.append((nx, ny))
        if solve_knights_tour(board, nx, ny, move_num + 1, n, path):  # Rekursi
            return True
        board[nx][ny] = -1              # Backtrack
        path.pop()
    return False
```

### Contoh Output (Papan 5×5, start: (0,0))

```
Papan 5×5 (angka = urutan langkah):

  0  19   8  13   2 
  9  14   1  18  23 
 20   7  22   3  12 
 15  10   5  24  17 
  6  21  16  11   4 
```

### Kompleksitas

| Aspek | Nilai |
|-------|-------|
| Waktu (tanpa heuristik) | O(8^(N²)) |
| Waktu (dengan Warnsdorff) | ~O(N²) praktis |
| Ruang | O(N²) |

> **Catatan:** Papan yang didukung: N ≥ 5. Papan kecil (N < 5) tidak memiliki solusi Tur Kuda.

---

## 3. Knapsack Problem

### Deskripsi

Masalah Knapsack (0/1): diberikan **knapsack dengan kapasitas target** dan sekumpulan barang dengan berat tertentu. Tujuannya adalah menemukan kombinasi barang yang **total beratnya mendekati atau sama dengan target** tanpa melebihi batas.

- Setiap barang hanya bisa dipilih **0 (tidak diambil) atau 1 (diambil)**.
- Total berat **tidak boleh melebihi target**.
- Maksimalkan total berat yang bisa diisi.

### Konsep Algoritma

Menggunakan **rekursi dengan dua pilihan** untuk setiap barang:

```
Untuk setiap barang[i]:
  ├── Pilihan A: MASUKKAN ke knapsack (jika berat ≤ sisa kapasitas)
  │     → rekursi ke barang[i+1] dengan kapasitas berkurang
  └── Pilihan B: LEWATI barang ini
        → rekursi ke barang[i+1] dengan kapasitas tetap
```

Simpan kombinasi terbaik (total terbesar ≤ target).

### Implementasi

```python
def knapsack_recursive(items, index, remaining_capacity, current_items, best):
    # Basis: semua barang sudah dicek atau kapasitas habis
    if index == len(items) or remaining_capacity == 0:
        current_total = sum(current_items)
        if current_total > best[0]:      # Simpan jika lebih baik
            best[0] = current_total
            best[1] = current_items[:]
        return

    weight = items[index]

    # Pilihan 1: Masukkan barang (jika muat)
    if weight <= remaining_capacity:
        current_items.append(weight)
        knapsack_recursive(items, index + 1,
                           remaining_capacity - weight,
                           current_items, best)
        current_items.pop()              # Backtrack

    # Pilihan 2: Lewati barang ini
    knapsack_recursive(items, index + 1, remaining_capacity,
                       current_items, best)
```

### Contoh Output

```
Input:
  Target      : 30
  Barang      : [2, 5, 6, 9, 12, 14, 20]

Output:
  Total berat   : 30 (dari target 30)
  Sisa kapasitas: 0
  Barang dipilih: [2, 5, 9, 14]
```

### Pohon Rekursi (Ilustrasi Sederhana)

```
knapsack([2,5,6,...], target=30)
├── Ambil 2 → knapsack([5,6,...], sisa=28)
│   ├── Ambil 5 → knapsack([6,...], sisa=23)
│   │   ├── Ambil 6 → ...
│   │   └── Skip 6 → ...
│   └── Skip 5 → ...
└── Skip 2 → knapsack([5,6,...], sisa=30)
    └── ...
```

### Kompleksitas

| Aspek | Nilai |
|-------|-------|
| Waktu (worst case) | O(2^N) |
| Ruang (rekursi) | O(N) |

> **Catatan:** Untuk N sangat besar (ribuan barang), gunakan pendekatan **Dynamic Programming** yang lebih efisien (O(N × W)).

---

## Cara Menjalankan Program

### Persyaratan

- Python 3.6 ke atas
- Tidak memerlukan library eksternal

### Menjalankan

```bash
python3 tugas_rekursif.py
```

### Menu Program

```
==================================================
   TUGAS REKURSIF & BACKTRACKING
==================================================
1. N-Queens Problem
2. Knight's Tour Problem
3. Knapsack Problem
0. Keluar
==================================================
```

### Contoh Sesi Interaktif

**N-Queens:**
```
Masukkan ukuran papan (N): 4
Ditemukan 2 solusi untuk 4-Queens.
```

**Knight's Tour:**
```
Masukkan ukuran papan (disarankan 5-8): 6
Masukkan posisi baris awal kuda (0-5): 0
Masukkan posisi kolom awal kuda (0-5): 0
```

**Knapsack:**
```
Masukkan berat target knapsack: 30
Masukkan berat barang (pisahkan dengan spasi): 2 5 6 9 12 14 20
```

---

## Ringkasan Perbandingan

| Problem | Strategi | Waktu | Kunci Optimasi |
|---------|----------|-------|----------------|
| N-Queens | Backtracking | O(N!) | Cek aman per baris/kolom/diagonal |
| Knight's Tour | Backtracking + Heuristik | ~O(N²) | Warnsdorff's Heuristic |
| Knapsack | Backtracking | O(2^N) | Pruning jika berat melebihi target |

---

*Tugas dikerjakan menggunakan bahasa Python dengan konsep rekursi dan backtracking.*
