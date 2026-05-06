"""
note_app.py
-----------
Implementasi utama aplikasi note-taking menggunakan Advanced Linked Lists.

Struktur data yang digunakan (sesuai materi Chapter 9):
  ┌─────────────────────────────────────────────────────────────────┐
  │  Doubly Linked List (Chronological) – urut berdasarkan timestamp│
  │  Doubly Linked List (Alphabetical)  – urut berdasarkan judul    │
  │  Multi-Linked List  (By Tag)        – chain terpisah tiap tag   │
  │  Circular Buffer    (Sync Status)   – N perubahan terbaru       │
  └─────────────────────────────────────────────────────────────────┘

Satu NoteNode secara bersamaan menjadi anggota ketiga chain DLL
dan semua chain tag-nya — tidak ada duplikasi data.
"""

import time
from note_node   import NoteNode
from sync_buffer import SyncCircularBuffer


class NoteApp:
    """
    Aplikasi note-taking berbasis Advanced Linked Lists.

    Parameters
    ----------
    sync_capacity : int – kapasitas circular buffer sync (default 10)
    """

    def __init__(self, sync_capacity: int = 10):
        # ── Doubly Linked List: Chronological ─────────────────────────
        self._chronoHead: NoteNode | None = None
        self._chronoTail: NoteNode | None = None

        # ── Doubly Linked List: Alphabetical ──────────────────────────
        self._alphaHead: NoteNode | None = None
        self._alphaTail: NoteNode | None = None

        # ── Multi-Linked: Tag chains ──────────────────────────────────
        # Format: { "tag_name": NoteNode (head of that tag chain) }
        self._tagHeads: dict = {}

        # ── Circular Buffer: Sync Status ──────────────────────────────
        self._syncBuffer = SyncCircularBuffer(capacity=sync_capacity)

        self._numNotes: int = 0

    # ================================================================== #
    #  PUBLIC: CRUD Operations                                            #
    # ================================================================== #

    def addNote(self, title: str, content: str,
                timestamp: int = None, tags: list = None) -> NoteNode:
        """
        Tambahkan note baru ke semua chain yang relevan.

        Parameters
        ----------
        title     : str  – judul note (harus unik)
        content   : str  – isi note
        timestamp : int  – Unix epoch; jika None, pakai waktu sekarang
        tags      : list – daftar tag string

        Returns
        -------
        NoteNode yang baru dibuat
        """
        if timestamp is None:
            timestamp = int(time.time())
        if tags is None:
            tags = []

        newNote = NoteNode(title, content, timestamp, tags)

        # Masukkan ke ketiga chain
        self._insertChrono(newNote)
        self._insertAlpha(newNote)
        for tag in tags:
            self._insertTag(newNote, tag)

        # Catat ke circular buffer
        self._syncBuffer.addChange({
            "action"   : "create",
            "noteTitle": title,
            "timestamp": timestamp,
        })

        self._numNotes += 1
        return newNote

    def deleteNote(self, title: str) -> bool:
        """
        Hapus note berdasarkan judul dari SEMUA chain.

        Returns True jika berhasil ditemukan dan dihapus, False jika tidak ada.
        """
        node = self._findByTitle(title)
        if node is None:
            return False

        self._removeChrono(node)
        self._removeAlpha(node)
        for tag in node.tags:
            self._removeTag(node, tag)

        self._syncBuffer.addChange({
            "action"   : "delete",
            "noteTitle": title,
            "timestamp": int(time.time()),
        })

        self._numNotes -= 1
        return True

    def editNote(self, title: str, new_content: str,
                 new_timestamp: int = None) -> bool:
        """
        Edit isi note. Jika timestamp baru diberikan, node akan
        diposisikan ulang dalam chain kronologis.

        Returns True jika berhasil, False jika note tidak ditemukan.
        """
        node = self._findByTitle(title)
        if node is None:
            return False

        node.content = new_content

        if new_timestamp is not None and new_timestamp != node.timestamp:
            # Reposisi di chain kronologis
            self._removeChrono(node)
            node.timestamp = new_timestamp
            self._insertChrono(node)

        self._syncBuffer.addChange({
            "action"   : "edit",
            "noteTitle": title,
            "timestamp": int(time.time()),
        })
        return True

    def addTagToNote(self, title: str, tag: str) -> bool:
        """Tambahkan tag baru ke note yang sudah ada."""
        node = self._findByTitle(title)
        if node is None or tag in node.tags:
            return False

        node.tags.append(tag)
        self._insertTag(node, tag)

        self._syncBuffer.addChange({
            "action"   : "tag",
            "noteTitle": title,
            "timestamp": int(time.time()),
        })
        return True

    # ================================================================== #
    #  PUBLIC: Traversal / Views                                          #
    # ================================================================== #

    def getNotesByTime(self) -> list:
        """
        Kembalikan semua note urut kronologis (oldest → newest).

        Returns
        -------
        list of dict  { "timestamp": int, "title": str, "tags": list }
        """
        result = []
        cur    = self._chronoHead
        while cur is not None:
            result.append({
                "timestamp": cur.timestamp,
                "title"    : cur.title,
                "tags"     : cur.tags,
            })
            cur = cur.nextByTime
        return result

    def getNotesByTimeReverse(self) -> list:
        """Kembalikan semua note urut kronologis terbalik (newest → oldest)."""
        result = []
        cur    = self._chronoTail
        while cur is not None:
            result.append({
                "timestamp": cur.timestamp,
                "title"    : cur.title,
                "tags"     : cur.tags,
            })
            cur = cur.prevByTime
        return result

    def getNotesByAlpha(self) -> list:
        """Kembalikan semua note urut alfabetikal (A → Z)."""
        result = []
        cur    = self._alphaHead
        while cur is not None:
            result.append({
                "title"    : cur.title,
                "timestamp": cur.timestamp,
                "tags"     : cur.tags,
            })
            cur = cur.nextByAlpha
        return result

    def getNotesByTag(self, tag: str) -> list:
        """
        Kembalikan semua note yang memiliki tag tertentu
        via partial Multi-Linked chain.

        Parameters
        ----------
        tag : str – nama tag yang dicari

        Returns
        -------
        list of dict
        """
        result = []
        cur    = self._tagHeads.get(tag, None)
        while cur is not None:
            result.append({
                "title"    : cur.title,
                "timestamp": cur.timestamp,
                "tags"     : cur.tags,
            })
            cur = cur.nextByTag.get(tag, None)
        return result

    def getAvailableTags(self) -> list:
        """Kembalikan semua tag yang terdaftar."""
        return list(self._tagHeads.keys())

    def getRecentSyncChanges(self) -> list:
        """Kembalikan daftar perubahan terbaru dari circular buffer."""
        return self._syncBuffer.getRecentChanges()

    def getLatestChange(self) -> dict | None:
        """Kembalikan perubahan paling baru."""
        return self._syncBuffer.getLatestChange()

    def numNotes(self) -> int:
        return self._numNotes

    # ================================================================== #
    #  PRIVATE: Insert helpers                                            #
    # ================================================================== #

    def _insertChrono(self, newNote: NoteNode) -> None:
        """Insert ke DLL kronologis (sorted by timestamp ascending)."""

        # Reset link baru
        newNote.nextByTime = None
        newNote.prevByTime = None

        # Case 1: List kosong
        if self._chronoHead is None:
            self._chronoHead = self._chronoTail = newNote
            return

        # Case 2: Taruh di depan (timestamp terkecil)
        if newNote.timestamp <= self._chronoHead.timestamp:
            newNote.nextByTime          = self._chronoHead
            self._chronoHead.prevByTime = newNote
            self._chronoHead            = newNote
            return

        # Case 3: Taruh di belakang (timestamp terbesar)
        if newNote.timestamp >= self._chronoTail.timestamp:
            newNote.prevByTime          = self._chronoTail
            self._chronoTail.nextByTime = newNote
            self._chronoTail            = newNote
            return

        # Case 4: Sisipkan di tengah
        cur = self._chronoHead
        while cur is not None and cur.timestamp < newNote.timestamp:
            cur = cur.nextByTime

        prev               = cur.prevByTime
        newNote.nextByTime = cur
        newNote.prevByTime = prev
        prev.nextByTime    = newNote
        cur.prevByTime     = newNote

    def _insertAlpha(self, newNote: NoteNode) -> None:
        """Insert ke DLL alfabetikal (sorted by title ascending)."""

        newNote.nextByAlpha = None
        newNote.prevByAlpha = None

        if self._alphaHead is None:
            self._alphaHead = self._alphaTail = newNote
            return

        if newNote.title.lower() <= self._alphaHead.title.lower():
            newNote.nextByAlpha         = self._alphaHead
            self._alphaHead.prevByAlpha = newNote
            self._alphaHead             = newNote
            return

        if newNote.title.lower() >= self._alphaTail.title.lower():
            newNote.prevByAlpha         = self._alphaTail
            self._alphaTail.nextByAlpha = newNote
            self._alphaTail             = newNote
            return

        cur = self._alphaHead
        while cur is not None and cur.title.lower() < newNote.title.lower():
            cur = cur.nextByAlpha

        prev                = cur.prevByAlpha
        newNote.nextByAlpha = cur
        newNote.prevByAlpha = prev
        prev.nextByAlpha    = newNote
        cur.prevByAlpha     = newNote

    def _insertTag(self, newNote: NoteNode, tag: str) -> None:
        """
        Insert ke partial chain tag tertentu.
        Node baru diletakkan di HEAD chain tag (unsorted).
        """
        newNote.nextByTag[tag]  = self._tagHeads.get(tag, None)
        self._tagHeads[tag]     = newNote

    # ================================================================== #
    #  PRIVATE: Remove helpers                                            #
    # ================================================================== #

    def _removeChrono(self, node: NoteNode) -> None:
        """Hapus node dari DLL kronologis."""
        if node.prevByTime is not None:
            node.prevByTime.nextByTime = node.nextByTime
        else:
            self._chronoHead = node.nextByTime

        if node.nextByTime is not None:
            node.nextByTime.prevByTime = node.prevByTime
        else:
            self._chronoTail = node.prevByTime

        node.nextByTime = node.prevByTime = None

    def _removeAlpha(self, node: NoteNode) -> None:
        """Hapus node dari DLL alfabetikal."""
        if node.prevByAlpha is not None:
            node.prevByAlpha.nextByAlpha = node.nextByAlpha
        else:
            self._alphaHead = node.nextByAlpha

        if node.nextByAlpha is not None:
            node.nextByAlpha.prevByAlpha = node.prevByAlpha
        else:
            self._alphaTail = node.prevByAlpha

        node.nextByAlpha = node.prevByAlpha = None

    def _removeTag(self, node: NoteNode, tag: str) -> None:
        """
        Hapus node dari chain tag tertentu.
        Perlu traversal karena ini singly linked (partial chain).
        """
        if tag not in self._tagHeads:
            return

        # Jika node adalah head chain tag
        if self._tagHeads[tag] is node:
            self._tagHeads[tag] = node.nextByTag.get(tag, None)
            if self._tagHeads[tag] is None:
                del self._tagHeads[tag]
            node.nextByTag.pop(tag, None)
            return

        # Traversal cari predecessor
        cur = self._tagHeads[tag]
        while cur is not None:
            nxt = cur.nextByTag.get(tag, None)
            if nxt is node:
                cur.nextByTag[tag] = node.nextByTag.get(tag, None)
                node.nextByTag.pop(tag, None)
                return
            cur = nxt

    # ================================================================== #
    #  PRIVATE: Search helper                                             #
    # ================================================================== #

    def _findByTitle(self, title: str) -> NoteNode | None:
        """
        Cari node berdasarkan judul menggunakan alpha chain (sorted).
        Memanfaatkan early termination karena chain sudah terurut.
        """
        cur = self._alphaHead
        while cur is not None:
            if cur.title == title:
                return cur
            # Early termination: sudah melewati posisi alfabetikal
            if cur.title.lower() > title.lower():
                return None
            cur = cur.nextByAlpha
        return None

    # ================================================================== #
    #  Display helper                                                     #
    # ================================================================== #

    def __repr__(self) -> str:
        return (
            f"NoteApp(numNotes={self._numNotes}, "
            f"tags={list(self._tagHeads.keys())}, "
            f"syncBuffer={self._syncBuffer})"
        )
