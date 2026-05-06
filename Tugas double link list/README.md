# 📝 Note-Taking App — Advanced Linked Lists

> **Tugas Struktur Data Lanjut — Chapter 9: Advanced Linked Lists**

Implementasi aplikasi note-taking sederhana yang mendemonstrasikan penggunaan **tiga jenis Advanced Linked List** sekaligus dalam satu sistem.

---

## 🎯 Latar Belakang

Proyek ini merupakan jawaban dari soal latihan pada materi *Chapter 9 — Advanced Linked Lists*:

> *"Rancang struktur data untuk aplikasi note-taking yang mendukung:*
> - *Multiple tags per note (multi-linked by tag)*
> - *Chronological dan alphabetical views (doubly linked sorted)*
> - *Sync status tracking (circular buffer for recent changes)"*

---

## 🏗️ Struktur Data yang Digunakan

| Kebutuhan | Struktur Data | Kompleksitas |
|---|---|---|
| Multiple tags per note | **Multi-Linked List** (`nextByTag` per tag) | Insert O(1), Traversal O(k) |
| Chronological view | **Doubly Linked List** sorted by timestamp | Insert O(n), Traversal O(n) |
| Alphabetical view | **Doubly Linked List** sorted by title | Insert O(n), Traversal O(n) |
| Sync status tracking | **Circular Buffer** (fixed-size array) | addChange O(1), read O(k) |

### Arsitektur Node

Satu `NoteNode` **secara bersamaan** menjadi anggota dari semua chain — tidak ada duplikasi data:

```
                        ┌─────────────────────────────────┐
                        │           NoteNode               │
                        │─────────────────────────────────│
                        │  title, content, timestamp, tags │
                        │─────────────────────────────────│
  DLL Kronologis ──────►│  nextByTime  │  prevByTime      │
  DLL Alfabetikal ─────►│  nextByAlpha │  prevByAlpha     │
  Multi-Linked Tag ────►│  nextByTag   { "kuliah": ...,   │
                        │               "algo"  : ... }   │
                        └─────────────────────────────────┘
```

---

## 📁 Struktur File

```
note-app-linked-list/
│
├── note_node.py        # Class NoteNode (elemen dasar semua chain)
├── sync_buffer.py      # Class SyncCircularBuffer (circular buffer)
├── note_app.py         # Class NoteApp (logika utama + semua operasi)
├── main.py             # Demo / runner lengkap
├── test_note_app.py    # 32 unit tests
└── README.md
```

---

## ▶️ Cara Menjalankan

**Requirements:** Python 3.10+  *(tidak ada library eksternal)*

### Jalankan Demo

```bash
python main.py
```

Output contoh:

```
=======================================================
  1. Menambahkan Notes
=======================================================
  Total note ditambahkan : 5
  Tags tersedia          : ['kuliah', 'algoritma', ...]

=======================================================
  2. View Kronologis (oldest → newest)
=======================================================
  • 1600000 | Resep Nasi Goreng
  • 1650000 | Algoritma Graph BFS
  • 1700000 | Belajar Doubly Linked List
  • 1720000 | Circular Linked List
  • 1750000 | Agenda Rapat Mingguan

=======================================================
  3. View Alfabetikal (A → Z)
=======================================================
  • Agenda Rapat Mingguan
  • Algoritma Graph BFS
  • Belajar Doubly Linked List
  • Circular Linked List
  • Resep Nasi Goreng
```

### Jalankan Unit Tests

```bash
python test_note_app.py
```

atau menggunakan pytest:

```bash
python -m pytest test_note_app.py -v
```

```
Ran 32 tests in 0.003s — OK
```

---

## 🔍 Penjelasan Implementasi

### 1. Doubly Linked List — Chronological & Alphabetical

Setiap `NoteNode` memiliki dua set pointer DLL:

```python
# DLL Kronologis
self.nextByTime = None
self.prevByTime = None

# DLL Alfabetikal
self.nextByAlpha = None
self.prevByAlpha = None
```

Insert dilakukan dengan **4 kasus**:
1. List kosong → node menjadi `head = tail`
2. Nilai terkecil → taruh di depan head
3. Nilai terbesar → taruh di belakang tail
4. Nilai di tengah → traversal, sisipkan di posisi yang tepat

Delete cukup dengan **2 operasi** (O(1) jika referensi node diketahui):
```python
node.prev.next = node.next
node.next.prev = node.prev
```

### 2. Multi-Linked List — Tag Chains

Setiap tag membentuk **partial chain** tersendiri melalui dict `nextByTag`:

```python
self.nextByTag = {}
# Contoh: { "kuliah": <NoteNode>, "algo": <NoteNode> }
```

- Satu `NoteNode` bisa masuk ke banyak chain tag sekaligus
- Insert di head setiap chain → O(1)
- Delete memerlukan traversal per chain → O(k)

### 3. Circular Buffer — Sync Status

Buffer berukuran tetap dengan logika **FIFO overwrite**:

```
Index: [0]  [1]  [2]  [3]  [4]
        ↑                   ↑
       head                tail
```

Ketika buffer penuh dan ada item baru masuk, `head` digeser maju otomatis:

```python
self._tail = (self._tail + 1) % self._capacity
if full:
    self._head = (self._head + 1) % self._capacity  # overwrite oldest
```

---

## 📊 Diagram Alur addNote()

```
addNote(title, content, timestamp, tags)
        │
        ├──► _insertChrono(node)   → DLL sorted by timestamp
        │
        ├──► _insertAlpha(node)    → DLL sorted by title
        │
        ├──► for tag in tags:
        │       _insertTag(node, tag) → Multi-linked tag chain
        │
        └──► syncBuffer.addChange(...)  → Circular buffer record
```

---

## 🧪 Cakupan Unit Test

| Test Class | Jumlah Test | Yang Diuji |
|---|---|---|
| `TestNoteNode` | 3 | Inisialisasi node & default values |
| `TestSyncCircularBuffer` | 7 | Empty, add, full, overwrite, clear, latest |
| `TestNoteAppInsertTraversal` | 7 | Urutan chrono, alpha, tag chain |
| `TestNoteAppDelete` | 6 | Hapus dari semua chain |
| `TestNoteAppEdit` | 3 | Edit konten & reposisi timestamp |
| `TestNoteAppAddTag` | 3 | Tambah tag baru & validasi duplikat |
| `TestSyncIntegration` | 3 | Rekaman sync untuk create/edit/delete |
| **Total** | **32** | |

---

## 📖 Referensi Materi

- **Chapter 9 — Advanced Linked Lists** (Struktur Data Lanjut)
- Goodrich, M. T., *Data Structures and Algorithms in Python*
- Konsep yang diterapkan:
  - Doubly Linked List & operasi insert/delete/traversal
  - Multi-Linked Lists dengan complete & partial chains
  - Circular Buffer untuk fixed-size FIFO storage
