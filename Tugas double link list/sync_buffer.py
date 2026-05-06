"""
sync_buffer.py
--------------
Implementasi Circular Buffer untuk melacak perubahan (sync status)
pada aplikasi note-taking.

Konsep:
  - Buffer berukuran tetap (capacity)
  - Ketika penuh, entri paling lama otomatis ditimpa (FIFO overwrite)
  - Operasi addChange dan getRecentChanges keduanya O(1) / O(k)

Struktur internal:
  _buffer   : list statis berukuran capacity
  _head     : index elemen paling lama (untuk read)
  _tail     : index slot kosong berikutnya (untuk write)
  _size     : jumlah elemen aktif saat ini
"""


class SyncCircularBuffer:
    """
    Circular Buffer yang menyimpan N perubahan terbaru pada note-taking app.

    Parameters
    ----------
    capacity : int – maksimum jumlah record yang disimpan (default 10)
    """

    def __init__(self, capacity: int = 10):
        if capacity < 1:
            raise ValueError("Capacity harus minimal 1.")
        self._buffer   = [None] * capacity
        self._capacity = capacity
        self._head     = 0   # index baca (oldest entry)
        self._tail     = 0   # index tulis (next write slot)
        self._size     = 0

    # ------------------------------------------------------------------ #
    #  Write                                                               #
    # ------------------------------------------------------------------ #

    def addChange(self, change_record: dict) -> None:
        """
        Tambahkan satu record perubahan ke buffer.

        Jika buffer sudah penuh, entri paling lama (head) ditimpa
        dan head digeser maju — inilah ciri khas circular buffer.

        Parameters
        ----------
        change_record : dict
            Contoh format:
            {
                "action"   : "edit",          # "create" | "edit" | "delete" | "tag"
                "noteTitle": "Belajar Python",
                "timestamp": 1700000000
            }
        """
        self._buffer[self._tail] = change_record
        self._tail = (self._tail + 1) % self._capacity

        if self._size < self._capacity:
            self._size += 1
        else:
            # Buffer penuh → geser head agar slot lama tertimpa
            self._head = (self._head + 1) % self._capacity

    # ------------------------------------------------------------------ #
    #  Read                                                                #
    # ------------------------------------------------------------------ #

    def getRecentChanges(self) -> list:
        """
        Kembalikan semua record perubahan dari yang paling lama
        ke yang paling baru.

        Returns
        -------
        list of dict
        """
        result = []
        idx    = self._head
        for _ in range(self._size):
            result.append(self._buffer[idx])
            idx = (idx + 1) % self._capacity
        return result

    def getLatestChange(self) -> dict | None:
        """Kembalikan record perubahan paling baru, atau None jika kosong."""
        if self._size == 0:
            return None
        latest_idx = (self._tail - 1) % self._capacity
        return self._buffer[latest_idx]

    # ------------------------------------------------------------------ #
    #  Status helpers                                                      #
    # ------------------------------------------------------------------ #

    def isEmpty(self) -> bool:
        return self._size == 0

    def isFull(self) -> bool:
        return self._size == self._capacity

    def size(self) -> int:
        return self._size

    def capacity(self) -> int:
        return self._capacity

    def clear(self) -> None:
        """Reset buffer ke kondisi kosong."""
        self._buffer = [None] * self._capacity
        self._head   = 0
        self._tail   = 0
        self._size   = 0

    def __repr__(self) -> str:
        return (
            f"SyncCircularBuffer(size={self._size}, "
            f"capacity={self._capacity}, "
            f"full={self.isFull()})"
        )
