# 🧩 Maze Solver — Stack + Backtracking

> **Tugas Struktur Data — Bab 7: Tumpukan (Stacks)**  
> Implementasi pemecahan labirin menggunakan **Stack (Tumpukan)** berbasis Linked List dan algoritma **Backtracking**.

---

## 📁 Struktur File

```
maze-solver/
├── main.py     # Semua kode dalam 1 file
└── README.md
```

`main.py` terdiri dari 4 bagian:

| Bagian | Isi |
|--------|-----|
| Bagian 1 | Stack ADT — Linked List (`_StackNode`, `Stack`) |
| Bagian 2 | Warna ANSI untuk tampilan terminal |
| Bagian 3 | Maze ADT — generate & solve |
| Bagian 4 | Program utama & menu interaktif |

---

## 🚀 Cara Jalankan

Tidak butuh library eksternal — cukup Python 3.7+.

```bash
python main.py          # mode interaktif (pilih ukuran & kecepatan)
python main.py --demo   # demo langsung 11×11 tanpa input
```

---

## 🎮 Cara Penggunaan

Saat dijalankan, pilih ukuran labirin dan kecepatan animasi:

```
[1] Kecil   – 11×11
[2] Sedang  – 15×15
[3] Besar   – 21×21
[4] Kustom
[5] Keluar
```

Lalu pilih kecepatan:

```
[1] Lambat  – 0.20 detik/langkah
[2] Normal  – 0.05 detik/langkah
[3] Cepat   – 0.01 detik/langkah
[4] Instan  – tanpa animasi
```

### Legenda

| Simbol | Arti |
|--------|------|
| `S` | Start — posisi awal |
| `E` | Exit — pintu keluar |
| `x` | Jalur aktif (hasil `push`) |
| `o` | Jalan buntu (hasil `pop` / backtrack) |
| `##` | Dinding |
| `  ` | Lorong terbuka |

---

## 🧠 Penjelasan Algoritma

### Generate Labirin — Recursive Backtracking

Labirin dibuat secara acak menggunakan DFS rekursif:
1. Mulai dari sel `(1,1)`, tandai sebagai lorong
2. Pilih arah acak ke tetangga yang belum dikunjungi (loncat 2 sel)
3. Buka dinding di antara keduanya, lalu rekursi
4. Hasilnya: **perfect maze** — satu jalur unik antara setiap dua sel

### Solve Labirin — Stack + Backtracking (Bab 7)

```
1. Push posisi START ke stack
2. Selama stack tidak kosong:
   a. Peek posisi teratas
   b. Jika posisi == EXIT → selesai, return True
   c. Coba 4 arah (kanan, bawah, kiri, atas):
      - Ada arah valid  → push, tandai x
      - Semua buntu     → tandai o, pop() → backtrack
3. Stack kosong → tidak ada jalur, return False
```

**push()** = bergerak maju ke sel baru  
**pop()** = mundur (backtrack) saat jalan buntu

---

## 📚 Stack ADT — Operasi

Diimplementasikan dengan **Linked List**, bukan Python list, sehingga semua operasi O(1) kasus terburuk.

| Operasi | Kompleksitas | Keterangan |
|---------|-------------|------------|
| `Stack()` | O(1) | Buat tumpukan kosong |
| `isEmpty()` | O(1) | Cek apakah kosong |
| `len()` | O(1) | Jumlah item |
| `peek()` | O(1) | Lihat item teratas tanpa hapus |
| `push(item)` | O(1) | Tambah item ke puncak |
| `pop()` | O(1) | Hapus & kembalikan item teratas |

---

## 📸 Contoh Output

```
+---------------------+
|##########################|
|## S  x  x ##  x  x ##|
|######  x ## x ##  x ##|
|##      x ## x ## x  x ##|
|##  ## ## x ########  x ##|
|##      x  x  x  x  x ##|
|##  ############ x ######|
|##  x  x  x  x  x  x ##|
|##########################|
|##  x  x  x  x  x  E ##|
|##########################|
+---------------------+

=============================================
  STATISTIK PENCARIAN JALUR
=============================================
  Status           : DITEMUKAN ✓
  Panjang jalur    : 25 sel
  Total push()     : 31  (langkah maju)
  Total pop()      : 6   (backtrack)
  Stack size maks  : 28
  Ukuran labirin   : 11x11
=============================================
```

---

## ⏱️ Kompleksitas Waktu

| Operasi | Kompleksitas |
|---------|-------------|
| Generate labirin N×N | O(N²) |
| Solve (semua kasus) | O(N²) |
| Setiap operasi Stack | O(1) |

---

## 👨‍💻 Informasi

Dibuat untuk memenuhi tugas mata kuliah **Struktur Data** — Bab 7: Tumpukan (Stacks).  
Referensi: Materi perkuliahan Bab 7 — *Stack ADT, Implementasi Linked List, Aplikasi Pemecahan Labirin*.
