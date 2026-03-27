# Big Integer ADT — Tugas Praktikum Struktur Data

Implementasi **Big Integer Abstract Data Type (ADT)** menggunakan dua pendekatan berbeda di Python: **Singly Link List** dan **Python List**. Proyek ini adalah bagian dari tugas praktikum mata kuliah Struktur Data.

\---

## Latar Belakang

Hardware komputer menyimpan integer dengan batasan ukuran (32-bit atau 64-bit). Pada arsitektur 64-bit, nilai integer terbatas pada kisaran −9.223.372.036.854.775.808 hingga 9.223.372.036.854.775.807. Jika kita membutuhkan angka yang lebih besar dari itu (lebih dari 19 digit), kita perlu mengimplementasikan Big Integer secara software.

Python sendiri sudah mendukung integer tak terbatas secara native, namun tugas ini bertujuan mempelajari cara mengimplementasikan struktur data tersebut dari nol menggunakan Link List dan List.

\---

## Struktur File

```
.
├── big\_integer.py   # Implementasi utama
└── README.md
```

\---

## Implementasi

### Soal 1a — `BigIntegerLinkedList` (Singly Link List)

Setiap digit disimpan dalam node tersendiri. Node-node diurutkan dari digit **paling tidak signifikan (least-significant)** ke yang paling signifikan.

Contoh angka **45.839** disimpan sebagai:

```
head → \[9] → \[3] → \[8] → \[5] → \[4] → None
         ^satuan        ^puluhan ribu
```

### Soal 1b — `BigIntegerList` (Python List)

Konsep penyimpanan sama, namun menggunakan Python list biasa.

Contoh angka **45.839** disimpan sebagai:

```python
self.\_digits = \[9, 3, 8, 5, 4]  # index 0 = least-significant
```

\---

## Operasi yang Didukung

### `toString()`

Mengembalikan representasi string dari big integer.

```python
a = BigIntegerLinkedList("45839")
print(a.toString())  # "45839"
```

### `comparable(other, op)` — Perbandingan

Operator yang didukung: `<`, `<=`, `>`, `>=`, `==`, `!=`

```python
a = BigIntegerLinkedList("45839")
b = BigIntegerLinkedList("12345")

a.comparable(b, '>')   # True
a.comparable(b, '==')  # False

# Atau menggunakan operator langsung:
a > b   # True
a == b  # False
```

### `arithmetic(rhsInt, op)` — Aritmatika

Operator yang didukung: `+`, `-`, `\*`, `//`, `%`, `\*\*`

```python
a = BigIntegerLinkedList("45839")
b = BigIntegerLinkedList("12345")

a.arithmetic(b, '+')   # BigIntegerLinkedList('58184')
a.arithmetic(b, '\*')   # BigIntegerLinkedList('565882455')

# Atau menggunakan operator langsung:
a + b   # 58184
a \* b   # 565882455
a \*\* BigIntegerLinkedList("2")  # 2101213921
```

### `bitwise\_ops(rhsInt, op)` — Bitwise

Operator yang didukung: `|`, `\&`, `^`, `<<`, `>>`

```python
a = BigIntegerLinkedList("45839")
b = BigIntegerLinkedList("12345")

a.bitwise\_ops(b, '|')   # BigIntegerLinkedList('45887')
a.bitwise\_ops(b, '<<')  # BigIntegerLinkedList('183356')  (shift 2 bit)

# Atau menggunakan operator langsung:
a | b   # 45887
a << BigIntegerLinkedList("2")  # 183356
```

### Soal 2 — Assignment Combo Operators

Semua operator assignment tersedia untuk kedua kelas.

|Operator|Aritmatika|Bitwise|
|-|-|-|
|`+=`|✅|—|
|`-=`|✅|—|
|`\*=`|✅|—|
|`//=`|✅|—|
|`%=`|✅|—|
|`\*\*=`|✅|—|
|`\|=`|—|✅|
|`\&=`|—|✅|
|`^=`|—|✅|
|`<<=`|—|✅|
|`>>=`|—|✅|

```python
x = BigIntegerLinkedList("1000")
y = BigIntegerLinkedList("250")

x += y   # x menjadi 1250
x -= y   # x menjadi 1000
x \*= y   # x menjadi 250000

x = BigIntegerLinkedList("60")
x |= BigIntegerLinkedList("15")  # x menjadi 63
x <<= BigIntegerLinkedList("2")  # x menjadi 252
```

\---

## Cara Menjalankan

```bash
# Clone repo
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# Jalankan tes bawaan
python big\_integer.py
```

Tidak ada dependensi eksternal — cukup Python 3.6+.

\---

## Contoh Output

```
============================================================
SOAL 1A — BigIntegerLinkedList
============================================================
a = 45839
b = 12345

-- toString --
  a.toString() = 45839

-- comparable --
  a > b  : True
  a < b  : False
  a == b : False
  a != b : True

-- arithmetic --
  a + b  = 58184
  a - b  = 33494
  a \* b  = 565882455
  a // b = 3
  a % b  = 8804
  a \*\* 2 = 2101213921

-- bitwise --
  a | b  = 45887
  a \& b  = 12297
  a ^ b  = 33590
  a << 2 = 183356
  a >> 2 = 11459

-- SOAL 2: Assignment combo operators --
  x=1000, y=250
  x += y  → 1250
  x -= y  → 1000
  x \*= y  → 250000
  x //= y → 1000
  x %= y  → 0
  2 \*\*= 10→ 1024
  60 |= 15  → 63
  ...
```

\---

