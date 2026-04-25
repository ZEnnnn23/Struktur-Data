# 🗂️ Queue Visualizations — Struktur Data & Algoritma

Visualisasi animasi interaktif untuk **5 kasus implementasi Queue** dari materi kuliah Struktur Data & Algoritma.  
Setiap file adalah program Python mandiri yang menampilkan animasi menggunakan `matplotlib`.

---

## 📁 Struktur File

```
queue_visualizations/
├── kasus1_printer_queue.py     # Antrian Printer Bersama (FIFO)
├── kasus2_hot_potato.py        # Permainan Hot Potato (Circular Queue)
├── kasus3_antrian_rs.py        # Antrian Rumah Sakit (Priority Queue)
├── kasus4_bfs.py               # BFS Graph Traversal (Queue level-by-level)
├── kasus5_simulasi_bandara.py  # Simulasi Loket Tiket Bandara (Discrete Event)
└── README.md
```

---

## 🚀 Cara Menjalankan

### 1. Install dependency

```bash
pip install matplotlib numpy
```

### 2. Jalankan file yang diinginkan

```bash
python kasus1_printer_queue.py
python kasus2_hot_potato.py
python kasus3_antrian_rs.py
python kasus4_bfs.py
python kasus5_simulasi_bandara.py
```

Setiap script langsung membuka jendela animasi — tidak perlu input tambahan.

---

## 🎬 Detail Setiap Kasus

---

### Kasus 1 — Antrian Printer Bersama

**File:** `kasus1_printer_queue.py`

**Konsep:** Queue FIFO (First-In, First-Out) untuk mensimulasikan antrian dokumen yang dikirim ke satu printer bersama.

**Yang divisualisasikan:**
- Dokumen masuk satu per satu ke antrian (enqueue)
- Printer mengambil dokumen dari FRONT (dequeue) dan mencetak
- Tampilan FRONT/REAR bergerak seiring operasi
- Daftar dokumen yang sudah selesai dicetak

**Operasi Queue:** `enqueue()`, `dequeue()`, `isEmpty()`

---

### Kasus 2 — Permainan Hot Potato

**File:** `kasus2_hot_potato.py`

**Konsep:** Circular Queue — pemain duduk melingkar, mengoper objek sejumlah N kali, pemain yang memegang saat hitungan habis tersingkir.

**Yang divisualisasikan:**
- Pemain tersusun dalam lingkaran
- 🥔 Potato berpindah sesuai arah antrian
- Pemain yang tersingkir diberi tanda ❌ dan memudar
- Urutan antrian ditampilkan di bawah
- Animasi berlanjut sampai tersisa 1 pemenang 🏆

**Teknik kunci:** `dequeue()` → `enqueue()` untuk simulasi oper melingkar

---

### Kasus 3 — Antrian Rumah Sakit (Priority Queue)

**File:** `kasus3_antrian_rs.py`

**Konsep:** Bounded Priority Queue — pasien tidak dilayani murni FIFO, tapi berdasarkan tingkat urgensi (prioritas). Prioritas sama → FIFO.

**Level Prioritas:**
| Level | Label    | Warna |
|-------|----------|-------|
| 0     | KRITIS   | 🔴    |
| 1     | DARURAT  | 🟠    |
| 2     | MENENGAH | 🔵    |
| 3     | RINGAN   | 🟢    |

**Yang divisualisasikan:**
- Pasien masuk dengan prioritas masing-masing
- Antrian dikelompokkan per level prioritas
- Pasien dilayani dari prioritas tertinggi (0) terlebih dulu
- Daftar pasien yang sudah dilayani ditampilkan berurutan

---

### Kasus 4 — BFS (Breadth-First Search)

**File:** `kasus4_bfs.py`

**Konsep:** Queue sebagai struktur inti BFS — memastikan graf ditelusuri level demi level, menjamin jalur terpendek pada graf tanpa bobot.

**Yang divisualisasikan:**
- Graf dengan 8 node (A–H) ditampilkan di panel kiri
- Node diwarnai sesuai level BFS yang ditemukan
- Panel kanan menampilkan isi queue saat ini + urutan kunjungan
- Setiap langkah `enqueue()` dan `dequeue()` ditampilkan dengan keterangan

**Warna Level:**
- L0 🔴 → L1 🟠 → L2 🔵 → L3 🟣

---

### Kasus 5 — Simulasi Loket Tiket Bandara

**File:** `kasus5_simulasi_bandara.py`

**Konsep:** Discrete-event simulation — penumpang tiba secara acak setiap tick waktu, dilayani oleh agen tiket. Mengukur rata-rata waktu tunggu.

**Parameter default:**
| Parameter | Nilai |
|-----------|-------|
| Durasi simulasi | 20 menit |
| Jumlah agen | 2 |
| Waktu layanan | 3 menit/penumpang |
| Rata-rata interval kedatangan | 2 menit |

**Aturan simulasi (per tick):**
1. **R1** — Jika penumpang tiba (probabilistik) → `enqueue()`
2. **R3** — Jika agen selesai → tandai agen bebas
3. **R2** — Jika agen bebas & antrian tidak kosong → `dequeue()`, mulai layani

**Yang divisualisasikan:**
- Antrian penumpang real-time (bergerak tiap tick)
- Status tiap agen (sibuk / bebas + sisa waktu layanan)
- Statistik: jumlah dilayani, rata-rata tunggu
- Progress bar waktu simulasi
- Event log tiap tick

---

## 📚 Konsep Queue yang Digunakan

| Konsep | Kasus |
|--------|-------|
| FIFO Queue (Array/List) | 1, 5 |
| Circular Queue | 2 |
| Priority Queue | 3 |
| Queue untuk BFS | 4 |
| Discrete Event Simulation | 5 |

---

## 🛠️ Teknologi

- **Python 3.8+**
- **matplotlib** — animasi & visualisasi
- **numpy** — kalkulasi numerik (kasus 5)
- **collections.deque** — implementasi queue efisien

---

## 👤 Info

Dibuat sebagai bagian dari tugas mata kuliah **Struktur Data & Algoritma**.  
Materi referensi: _Queue: Representasi Array · Operasi Queue · Single Linked List · Double Linked List · Implementasi Kasus Nyata_
