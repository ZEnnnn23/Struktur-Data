# Tugas Struktur Data - Python

Repository ini berisi implementasi tugas mata kuliah Struktur Data menggunakan Python.

## 📚 Daftar Tugas

### 1. Game of Life
Implementasi Conway's Game of Life - simulasi cellular automaton dengan GUI menggunakan Tkinter.

**File:** `game_of_life.py`

**Cara Menjalankan:**
```bash
python game_of_life.py
```

**Fitur:**
- GUI interaktif dengan Tkinter
- Klik untuk toggle sel hidup/mati
- Tombol START/STOP untuk kontrol simulasi
- Tombol RANDOM untuk generate pola acak
- Tombol RESET untuk clear grid

**Konsep:**
- Struktur Data: Array 2D (list of lists)
- 4 Aturan Conway untuk update generasi
- Double buffering untuk update serentak

---

### 2. Latihan Soal - Sets & Dictionaries
Kumpulan 5 soal latihan tentang penggunaan Set dan Dictionary di Python.

**File:** `latihan_soal.py`

**Cara Menjalankan:**
```bash
python latihan_soal.py
```

**Soal yang Dikerjakan:**

#### Soal 1: Deduplikasi
Menghapus duplikat dari list dengan mempertahankan urutan kemunculan pertama.
```python
Input:  [1, 2, 3, 2, 1, 4]
Output: [1, 2, 3, 4]
```

#### Soal 2: Intersection Dua Array
Mengembalikan elemen yang muncul di kedua list.
```python
Input:  [1, 2, 3, 4], [2, 4, 6]
Output: [2, 4]
```

#### Soal 3: Anagram Check
Mengecek apakah dua string adalah anagram (punya huruf yang sama).
```python
is_anagram("listen", "silent")  # True
is_anagram("hello", "world")    # False
```

#### Soal 4: First Recurring Character
Menemukan karakter pertama yang muncul lebih dari sekali dalam string.
```python
first_recurring("abcadb")  # 'a'
first_recurring("abcdef")  # None
```

#### Soal 5: Simulasi Buku Telepon
Program interaktif untuk mengelola kontak dengan fitur:
- Tambah kontak
- Cari kontak
- Tampilkan semua kontak
- Keluar

---

## 🛠️ Requirements

- Python 3.6+
- Tkinter (sudah built-in di Python)

**Cek instalasi:**
```bash
python --version
```

---

## 📖 Penjelasan Struktur Data

### Array 2D (List of Lists)
Digunakan di Game of Life untuk merepresentasikan grid.
```python
grid = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]
```

### Set
Digunakan untuk:
- Deduplikasi (hapus duplikat)
- Cek keanggotaan dengan cepat O(1)
- First recurring character

### Dictionary
Digunakan untuk:
- Hitung frekuensi karakter (anagram check)
- Simpan pasangan key-value (buku telepon)
- Lookup cepat O(1)

---

## 📝 Cara Penggunaan

### Clone Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### Jalankan Program
```bash
# Game of Life
python game_of_life.py

# Latihan Soal
python latihan_soal.py
```

---

## 👤 Author

**Nama:** [Isi nama kamu]  
**NIM:** [Isi NIM kamu]  
**Kelas:** [Isi kelas kamu]

---

## 📄 License

Tugas ini dibuat untuk keperluan akademis - Mata Kuliah Struktur Data.
