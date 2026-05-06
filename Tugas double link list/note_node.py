"""
note_node.py
------------
Definisi class NoteNode yang menjadi elemen dasar dari semua struktur
linked list dalam aplikasi note-taking ini.

Setiap NoteNode sekaligus menjadi anggota dari:
  - Doubly Linked List kronologis  (nextByTime  / prevByTime)
  - Doubly Linked List alfabetikal (nextByAlpha / prevByAlpha)
  - Multi-Linked chain per tag     (nextByTag   – dict)
"""


class NoteNode:
    """
    Satu node yang merepresentasikan sebuah catatan (note).

    Attributes
    ----------
    title     : str   – judul catatan
    content   : str   – isi catatan
    timestamp : int   – waktu pembuatan / modifikasi (Unix epoch)
    tags      : list  – daftar tag string yang melekat pada note ini

    Link fields (Multi-Linked List)
    --------------------------------
    nextByTime, prevByTime   : link untuk DLL kronologis
    nextByAlpha, prevByAlpha : link untuk DLL alfabetikal
    nextByTag                : dict { tag_name -> NoteNode }
                               link ke node berikutnya dalam chain tag
    """

    def __init__(self, title: str, content: str, timestamp: int, tags: list = None):
        self.title     = title
        self.content   = content
        self.timestamp = timestamp
        self.tags      = tags if tags is not None else []

        # Chain 1: Doubly Linked – urut berdasarkan timestamp
        self.nextByTime: "NoteNode | None" = None
        self.prevByTime: "NoteNode | None" = None

        # Chain 2: Doubly Linked – urut berdasarkan title (alfabetikal)
        self.nextByAlpha: "NoteNode | None" = None
        self.prevByAlpha: "NoteNode | None" = None

        # Chain 3: Multi-Linked – satu link per tag
        # Format: { "python": <NoteNode>, "algo": <NoteNode>, ... }
        self.nextByTag: dict = {}

    def __repr__(self) -> str:
        return (
            f"NoteNode(title={self.title!r}, "
            f"timestamp={self.timestamp}, "
            f"tags={self.tags})"
        )
