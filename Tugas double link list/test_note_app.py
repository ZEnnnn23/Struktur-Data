"""
test_note_app.py
----------------
Unit tests untuk NoteApp, NoteNode, dan SyncCircularBuffer.

Jalankan dengan:
    python -m pytest test_note_app.py -v
atau:
    python test_note_app.py
"""

import unittest
from note_node   import NoteNode
from sync_buffer import SyncCircularBuffer
from note_app    import NoteApp


# ====================================================================== #
#  Test: NoteNode                                                         #
# ====================================================================== #

class TestNoteNode(unittest.TestCase):

    def test_create_node(self):
        node = NoteNode("Judul", "Isi", 1000, ["tag1", "tag2"])
        self.assertEqual(node.title, "Judul")
        self.assertEqual(node.content, "Isi")
        self.assertEqual(node.timestamp, 1000)
        self.assertEqual(node.tags, ["tag1", "tag2"])

    def test_default_links_are_none(self):
        node = NoteNode("A", "B", 0)
        self.assertIsNone(node.nextByTime)
        self.assertIsNone(node.prevByTime)
        self.assertIsNone(node.nextByAlpha)
        self.assertIsNone(node.prevByAlpha)
        self.assertEqual(node.nextByTag, {})

    def test_default_tags_empty(self):
        node = NoteNode("X", "Y", 0)
        self.assertEqual(node.tags, [])


# ====================================================================== #
#  Test: SyncCircularBuffer                                               #
# ====================================================================== #

class TestSyncCircularBuffer(unittest.TestCase):

    def test_empty_buffer(self):
        buf = SyncCircularBuffer(5)
        self.assertTrue(buf.isEmpty())
        self.assertFalse(buf.isFull())
        self.assertEqual(buf.size(), 0)
        self.assertIsNone(buf.getLatestChange())
        self.assertEqual(buf.getRecentChanges(), [])

    def test_add_single(self):
        buf = SyncCircularBuffer(5)
        buf.addChange({"action": "create", "noteTitle": "A", "timestamp": 1})
        self.assertEqual(buf.size(), 1)
        self.assertFalse(buf.isEmpty())

    def test_add_up_to_capacity(self):
        buf = SyncCircularBuffer(3)
        for i in range(3):
            buf.addChange({"action": "create", "noteTitle": str(i), "timestamp": i})
        self.assertTrue(buf.isFull())
        self.assertEqual(buf.size(), 3)

    def test_overwrite_when_full(self):
        buf = SyncCircularBuffer(3)
        for i in range(5):   # masukkan 5 item ke buffer kapasitas 3
            buf.addChange({"action": "x", "noteTitle": str(i), "timestamp": i})
        # Hanya 3 terakhir yang tersimpan
        changes = buf.getRecentChanges()
        self.assertEqual(len(changes), 3)
        titles = [c["noteTitle"] for c in changes]
        self.assertEqual(titles, ["2", "3", "4"])

    def test_get_latest_change(self):
        buf = SyncCircularBuffer(5)
        buf.addChange({"action": "create", "noteTitle": "A", "timestamp": 1})
        buf.addChange({"action": "edit",   "noteTitle": "B", "timestamp": 2})
        latest = buf.getLatestChange()
        self.assertEqual(latest["noteTitle"], "B")

    def test_clear(self):
        buf = SyncCircularBuffer(5)
        buf.addChange({"action": "create", "noteTitle": "A", "timestamp": 1})
        buf.clear()
        self.assertTrue(buf.isEmpty())

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            SyncCircularBuffer(0)


# ====================================================================== #
#  Test: NoteApp – Insert & Traversal                                     #
# ====================================================================== #

class TestNoteAppInsertTraversal(unittest.TestCase):

    def setUp(self):
        self.app = NoteApp()
        self.app.addNote("Zebra Note",  "isi z", timestamp=3000, tags=["a"])
        self.app.addNote("Alpha Note",  "isi a", timestamp=1000, tags=["a", "b"])
        self.app.addNote("Medium Note", "isi m", timestamp=2000, tags=["b"])

    def test_num_notes(self):
        self.assertEqual(self.app.numNotes(), 3)

    def test_chrono_order(self):
        notes = self.app.getNotesByTime()
        timestamps = [n["timestamp"] for n in notes]
        self.assertEqual(timestamps, sorted(timestamps))

    def test_chrono_reverse_order(self):
        notes = self.app.getNotesByTimeReverse()
        timestamps = [n["timestamp"] for n in notes]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))

    def test_alpha_order(self):
        notes = self.app.getNotesByAlpha()
        titles = [n["title"].lower() for n in notes]
        self.assertEqual(titles, sorted(titles))

    def test_tag_chain_a(self):
        notes = self.app.getNotesByTag("a")
        self.assertEqual(len(notes), 2)

    def test_tag_chain_b(self):
        notes = self.app.getNotesByTag("b")
        self.assertEqual(len(notes), 2)

    def test_nonexistent_tag(self):
        notes = self.app.getNotesByTag("zzz")
        self.assertEqual(notes, [])


# ====================================================================== #
#  Test: NoteApp – Delete                                                 #
# ====================================================================== #

class TestNoteAppDelete(unittest.TestCase):

    def setUp(self):
        self.app = NoteApp()
        self.app.addNote("Note A", "isi a", timestamp=1000, tags=["x", "y"])
        self.app.addNote("Note B", "isi b", timestamp=2000, tags=["x"])
        self.app.addNote("Note C", "isi c", timestamp=3000, tags=["y"])

    def test_delete_existing(self):
        result = self.app.deleteNote("Note B")
        self.assertTrue(result)
        self.assertEqual(self.app.numNotes(), 2)

    def test_delete_nonexistent(self):
        result = self.app.deleteNote("Tidak Ada")
        self.assertFalse(result)
        self.assertEqual(self.app.numNotes(), 3)

    def test_delete_updates_chrono_chain(self):
        self.app.deleteNote("Note A")
        notes = self.app.getNotesByTime()
        titles = [n["title"] for n in notes]
        self.assertNotIn("Note A", titles)
        self.assertEqual(len(notes), 2)

    def test_delete_updates_alpha_chain(self):
        self.app.deleteNote("Note C")
        notes = self.app.getNotesByAlpha()
        titles = [n["title"] for n in notes]
        self.assertNotIn("Note C", titles)

    def test_delete_updates_tag_chain(self):
        self.app.deleteNote("Note A")
        notes_x = self.app.getNotesByTag("x")
        self.assertEqual(len(notes_x), 1)
        self.assertEqual(notes_x[0]["title"], "Note B")

    def test_delete_all_notes(self):
        self.app.deleteNote("Note A")
        self.app.deleteNote("Note B")
        self.app.deleteNote("Note C")
        self.assertEqual(self.app.numNotes(), 0)
        self.assertEqual(self.app.getNotesByTime(), [])
        self.assertEqual(self.app.getNotesByAlpha(), [])


# ====================================================================== #
#  Test: NoteApp – Edit                                                   #
# ====================================================================== #

class TestNoteAppEdit(unittest.TestCase):

    def setUp(self):
        self.app = NoteApp()
        self.app.addNote("Note A", "isi lama", timestamp=1000, tags=["t"])
        self.app.addNote("Note B", "isi b",    timestamp=3000, tags=["t"])

    def test_edit_content(self):
        self.app.editNote("Note A", "isi baru")
        # Cek lewat find internal (pakai alpha chain)
        notes = self.app.getNotesByAlpha()
        note_a = next(n for n in notes if n["title"] == "Note A")
        # Content tidak ada di view dict, jadi kita cek tidak error
        self.assertIsNotNone(note_a)

    def test_edit_timestamp_reorders_chrono(self):
        # Note A ada di ts=1000, Note B di ts=3000
        # Edit Note A ke ts=4000 → seharusnya jadi paling akhir
        self.app.editNote("Note A", "isi baru", new_timestamp=4000)
        notes = self.app.getNotesByTime()
        self.assertEqual(notes[-1]["title"], "Note A")

    def test_edit_nonexistent(self):
        result = self.app.editNote("Tidak Ada", "konten")
        self.assertFalse(result)


# ====================================================================== #
#  Test: NoteApp – AddTag                                                 #
# ====================================================================== #

class TestNoteAppAddTag(unittest.TestCase):

    def setUp(self):
        self.app = NoteApp()
        self.app.addNote("Note X", "isi x", timestamp=1000, tags=["a"])

    def test_add_new_tag(self):
        result = self.app.addTagToNote("Note X", "b")
        self.assertTrue(result)
        notes = self.app.getNotesByTag("b")
        self.assertEqual(len(notes), 1)

    def test_add_duplicate_tag(self):
        result = self.app.addTagToNote("Note X", "a")  # sudah ada
        self.assertFalse(result)

    def test_add_tag_to_nonexistent(self):
        result = self.app.addTagToNote("Tidak Ada", "c")
        self.assertFalse(result)


# ====================================================================== #
#  Test: Sync Buffer Integration                                          #
# ====================================================================== #

class TestSyncIntegration(unittest.TestCase):

    def test_add_records_sync(self):
        app = NoteApp()
        app.addNote("N1", "c1", timestamp=1000, tags=[])
        app.addNote("N2", "c2", timestamp=2000, tags=[])
        changes = app.getRecentSyncChanges()
        self.assertEqual(len(changes), 2)
        actions = [c["action"] for c in changes]
        self.assertEqual(actions, ["create", "create"])

    def test_delete_records_sync(self):
        app = NoteApp()
        app.addNote("N1", "c1", timestamp=1000, tags=[])
        app.deleteNote("N1")
        changes = app.getRecentSyncChanges()
        self.assertEqual(changes[-1]["action"], "delete")

    def test_edit_records_sync(self):
        app = NoteApp()
        app.addNote("N1", "c1", timestamp=1000, tags=[])
        app.editNote("N1", "c1 baru")
        changes = app.getRecentSyncChanges()
        self.assertEqual(changes[-1]["action"], "edit")


if __name__ == "__main__":
    unittest.main(verbosity=2)
