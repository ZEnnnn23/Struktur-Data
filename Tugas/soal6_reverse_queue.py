from llistqueue import Queue


def reverseQueue(q):
    """
    Membalik urutan item dalam queue.

    Cara kerja:
    - Langkah 1: Pindahkan semua item dari queue ke stack (list).
                 Stack bersifat LIFO, jadi item terakhir masuk akan keluar pertama.
    - Langkah 2: Pindahkan kembali dari stack ke queue.
                 Karena stack membalik urutan, queue kini berisi item yang terbalik.

    Hanya menggunakan operasi Queue ADT: enqueue, dequeue, isEmpty.
    Kompleksitas: O(n) waktu, O(n) ruang.
    """
    stack = []

    # Langkah 1: queue → stack
    while not q.isEmpty():
        stack.append(q.dequeue())

    # Langkah 2: stack → queue (urutan terbalik)
    while stack:
        q.enqueue(stack.pop())

    return q


# ── Contoh penggunaan ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    q = Queue()
    for v in [10, 20, 30, 40, 50]:
        q.enqueue(v)

    # Tampilkan isi sebelum
    before = []
    temp = Queue()
    while not q.isEmpty():
        item = q.dequeue()
        before.append(item)
        temp.enqueue(item)
    q = temp
    print("Sebelum (front → rear):", before)

    # Balik queue
    reverseQueue(q)

    # Tampilkan isi sesudah
    after = []
    while not q.isEmpty():
        after.append(q.dequeue())
    print("Sesudah  (front → rear):", after)
