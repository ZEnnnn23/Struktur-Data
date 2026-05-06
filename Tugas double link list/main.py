"""
main.py
-------
Demo lengkap aplikasi note-taking berbasis Advanced Linked Lists.

Mendemonstrasikan:
  1. addNote        – insert ke DLL kronologis, DLL alfabetikal, & tag chains
  2. getNotesByTime – traversal DLL kronologis (forward & reverse)
  3. getNotesByAlpha– traversal DLL alfabetikal
  4. getNotesByTag  – traversal multi-linked tag chain
  5. editNote       – update content & reposisi di chain kronologis
  6. addTagToNote   – tambah tag baru ke note yang sudah ada
  7. deleteNote     – hapus dari SEMUA chain sekaligus
  8. getRecentSyncChanges – baca circular buffer sync status
"""

from note_app import NoteApp


def separator(title: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def print_notes(notes: list, fields: list = None) -> None:
    if not notes:
        print("  (kosong)")
        return
    for n in notes:
        if fields:
            info = " | ".join(str(n.get(f, "-")) for f in fields)
        else:
            info = str(n)
        print(f"  • {info}")


def main():
    app = NoteApp(sync_capacity=10)

    # ------------------------------------------------------------------ #
    #  1. Tambah beberapa note                                            #
    # ------------------------------------------------------------------ #
    separator("1. Menambahkan Notes")

    app.addNote(
        title="Belajar Doubly Linked List",
        content="DLL memiliki pointer next dan prev pada setiap node.",
        timestamp=1_700_000,
        tags=["kuliah", "algoritma", "struktur-data"]
    )
    app.addNote(
        title="Resep Nasi Goreng",
        content="Bumbu: bawang merah, bawang putih, kecap, telur.",
        timestamp=1_600_000,
        tags=["hobi", "masakan"]
    )
    app.addNote(
        title="Agenda Rapat Mingguan",
        content="Bahas progres sprint dan review PR yang pending.",
        timestamp=1_750_000,
        tags=["kuliah", "kerja"]
    )
    app.addNote(
        title="Algoritma Graph BFS",
        content="BFS menggunakan queue, DFS menggunakan stack/rekursi.",
        timestamp=1_650_000,
        tags=["kuliah", "algoritma"]
    )
    app.addNote(
        title="Circular Linked List",
        content="Node terakhir menunjuk kembali ke node pertama.",
        timestamp=1_720_000,
        tags=["kuliah", "struktur-data"]
    )

    print(f"  Total note ditambahkan : {app.numNotes()}")
    print(f"  Tags tersedia          : {app.getAvailableTags()}")

    # ------------------------------------------------------------------ #
    #  2. View: Kronologis                                                #
    # ------------------------------------------------------------------ #
    separator("2. View Kronologis (oldest → newest)")
    notes = app.getNotesByTime()
    print_notes(notes, fields=["timestamp", "title"])

    separator("2b. View Kronologis Terbalik (newest → oldest)")
    notes = app.getNotesByTimeReverse()
    print_notes(notes, fields=["timestamp", "title"])

    # ------------------------------------------------------------------ #
    #  3. View: Alfabetikal                                               #
    # ------------------------------------------------------------------ #
    separator("3. View Alfabetikal (A → Z)")
    notes = app.getNotesByAlpha()
    print_notes(notes, fields=["title"])

    # ------------------------------------------------------------------ #
    #  4. View: Per Tag (Multi-Linked)                                    #
    # ------------------------------------------------------------------ #
    separator("4. View Per Tag: 'kuliah'")
    notes = app.getNotesByTag("kuliah")
    print_notes(notes, fields=["title", "tags"])

    separator("4b. View Per Tag: 'algoritma'")
    notes = app.getNotesByTag("algoritma")
    print_notes(notes, fields=["title"])

    separator("4c. View Per Tag: 'hobi'")
    notes = app.getNotesByTag("hobi")
    print_notes(notes, fields=["title"])

    # ------------------------------------------------------------------ #
    #  5. Edit Note                                                       #
    # ------------------------------------------------------------------ #
    separator("5. Edit Note: 'Resep Nasi Goreng'")
    print("  Sebelum edit – cek kronologis:")
    for n in app.getNotesByTime():
        print(f"    [{n['timestamp']}] {n['title']}")

    app.editNote(
        title="Resep Nasi Goreng",
        new_content="Bumbu lengkap + tambahkan saus tiram dan daun bawang.",
        new_timestamp=1_760_000   # timestamp diupdate → reposisi di chain
    )

    print("\n  Setelah edit – cek kronologis:")
    for n in app.getNotesByTime():
        print(f"    [{n['timestamp']}] {n['title']}")

    # ------------------------------------------------------------------ #
    #  6. Tambah Tag ke Note yang Sudah Ada                               #
    # ------------------------------------------------------------------ #
    separator("6. Tambah Tag 'resep' ke 'Resep Nasi Goreng'")
    app.addTagToNote("Resep Nasi Goreng", "resep")
    print("  Tags tersedia sekarang:", app.getAvailableTags())
    print("  Note dengan tag 'resep':")
    print_notes(app.getNotesByTag("resep"), fields=["title"])

    # ------------------------------------------------------------------ #
    #  7. Delete Note                                                     #
    # ------------------------------------------------------------------ #
    separator("7. Hapus Note: 'Agenda Rapat Mingguan'")
    print(f"  Jumlah note sebelum hapus : {app.numNotes()}")
    deleted = app.deleteNote("Agenda Rapat Mingguan")
    print(f"  Berhasil dihapus          : {deleted}")
    print(f"  Jumlah note setelah hapus : {app.numNotes()}")

    print("\n  Chain 'kuliah' setelah hapus:")
    print_notes(app.getNotesByTag("kuliah"), fields=["title"])

    print("\n  DLL Alfabetikal setelah hapus:")
    print_notes(app.getNotesByAlpha(), fields=["title"])

    # ------------------------------------------------------------------ #
    #  8. Sync Status – Circular Buffer                                   #
    # ------------------------------------------------------------------ #
    separator("8. Sync Status (Circular Buffer – 10 record terakhir)")
    changes = app.getRecentSyncChanges()
    for i, ch in enumerate(changes, 1):
        print(f"  [{i:02d}] action={ch['action']:<8} "
              f"ts={ch['timestamp']}  title={ch['noteTitle']!r}")

    print(f"\n  Perubahan terbaru : {app.getLatestChange()}")

    # ------------------------------------------------------------------ #
    #  Ringkasan akhir                                                    #
    # ------------------------------------------------------------------ #
    separator("Ringkasan Akhir")
    print(f"  {app}")


if __name__ == "__main__":
    main()
