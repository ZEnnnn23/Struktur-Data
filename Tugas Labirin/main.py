#!/usr/bin/env python3
# ============================================================
#  main.py  –  Maze Solver dengan Stack + Backtracking
#  Struktur Data – Bab 7: Tumpukan (Stacks)
# ============================================================

import random
import time
import sys


# ============================================================
#  BAGIAN 1: STACK ADT (Linked List)
#  Kompleksitas O(1) untuk semua operasi (kasus terburuk)
# ============================================================

class _StackNode:
    """Node internal untuk Linked List Stack."""
    def __init__(self, item, link):
        self.item = item
        self.next = link


class Stack:
    """
    Implementasi Stack (Tumpukan) menggunakan Linked List.
    Prinsip LIFO – Last In, First Out.
    Awal linked list = bagian ATAS (TOP) tumpukan.
    """
    def __init__(self):
        self._top  = None
        self._size = 0

    def isEmpty(self):
        return self._top is None

    def __len__(self):
        return self._size

    def peek(self):
        assert not self.isEmpty(), "Peek pada tumpukan kosong!"
        return self._top.item

    def push(self, item):
        self._top  = _StackNode(item, self._top)
        self._size += 1

    def pop(self):
        assert not self.isEmpty(), "Pop pada tumpukan kosong!"
        node       = self._top
        self._top  = self._top.next
        self._size -= 1
        return node.item


# ============================================================
#  BAGIAN 2: WARNA ANSI
# ============================================================

class Color:
    RESET = "\033[0m"
    WALL  = "\033[90m"
    OPEN  = "\033[37m"
    START = "\033[1;92m"
    EXIT  = "\033[1;91m"
    PATH  = "\033[1;94m"
    TRIED = "\033[33m"
    TITLE = "\033[1;96m"
    INFO  = "\033[96m"
    STAT  = "\033[1;93m"
    DIM   = "\033[2m"


# ============================================================
#  BAGIAN 3: MAZE ADT
# ============================================================

WALL  = "*"
OPEN  = " "
START = "S"
EXIT  = "E"
PATH  = "x"
TRIED = "o"


class Maze:
    """
    Maze ADT – Labirin berbasis grid 2D.

    Generate : Recursive Backtracking (DFS) → labirin acak sempurna
    Solve    : Stack + Backtracking (sesuai materi Bab 7)

    Token sel:
        * = dinding     S = start     E = exit
        x = jalur aktif (push)        o = jalan buntu (pop)
    """

    def __init__(self, numRows, numCols):
        assert numRows >= 5 and numCols >= 5, "Labirin minimal 5x5"
        assert numRows % 2 == 1 and numCols % 2 == 1, \
            "Gunakan ukuran ganjil (5,7,9,...)"
        self._numRows   = numRows
        self._numCols   = numCols
        self._grid      = [[WALL] * numCols for _ in range(numRows)]
        self._startCell = None
        self._exitCell  = None
        self._pushCount = 0
        self._popCount  = 0
        self._maxStack  = 0
        self._solved    = False
        self._pathLen   = 0

    def numRows(self): return self._numRows
    def numCols(self): return self._numCols

    # ── generate labirin acak ────────────────────────────────
    def generate(self):
        """Generate labirin acak menggunakan Recursive Backtracking."""
        for r in range(self._numRows):
            for c in range(self._numCols):
                self._grid[r][c] = WALL

        def carve(r, c):
            self._grid[r][c] = OPEN
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 < nr < self._numRows - 1 and
                        0 < nc < self._numCols - 1 and
                        self._grid[nr][nc] == WALL):
                    self._grid[r + dr // 2][c + dc // 2] = OPEN
                    carve(nr, nc)

        carve(1, 1)
        self._setStart(1, 1)
        self._setExit(self._numRows - 2, self._numCols - 2)

    def _setStart(self, r, c):
        self._startCell = (r, c)
        self._grid[r][c] = START

    def _setExit(self, r, c):
        self._exitCell = (r, c)
        self._grid[r][c] = EXIT

    # ── cari jalur dengan Stack + Backtracking (Bab 7) ──────
    def findPath(self, animate=False, delay=0.05):
        """
        Algoritma pencarian jalur (sesuai Bab 7 PPT):

          1. Push posisi START ke stack
          2. Selama stack tidak kosong:
             a. Peek posisi teratas
             b. Jika posisi == EXIT → selesai, return True
             c. Coba 4 arah:
                - Ada arah valid → push, tandai PATH (x)
                - Semua buntu   → tandai TRIED (o), pop() backtrack
          3. Stack kosong → tidak ada jalur, return False
        """
        self.reset()
        self._pushCount = 0
        self._popCount  = 0
        self._maxStack  = 0
        self._solved    = False

        stack   = Stack()
        visited = [[False] * self._numCols for _ in range(self._numRows)]

        sr, sc = self._startCell
        stack.push((sr, sc))
        visited[sr][sc] = True
        self._pushCount = 1
        self._maxStack  = 1

        dirs     = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        step_num = 0

        while not stack.isEmpty():
            row, col = stack.peek()
            step_num += 1

            if animate:
                self.draw(clear_screen=True)
                self._printLive(stack, step_num)
                time.sleep(delay)

            # cek exit
            if (row, col) == self._exitCell:
                self._solved  = True
                self._pathLen = len(stack)
                if animate:
                    self.draw(clear_screen=True)
                    self._printLive(stack, step_num)
                return True

            # coba 4 arah
            moved = False
            for dr, dc in dirs:
                nr, nc = row + dr, col + dc
                if (0 <= nr < self._numRows and
                        0 <= nc < self._numCols and
                        not visited[nr][nc] and
                        self._grid[nr][nc] != WALL):
                    visited[nr][nc] = True
                    stack.push((nr, nc))
                    self._pushCount += 1
                    if len(stack) > self._maxStack:
                        self._maxStack = len(stack)
                    if self._grid[nr][nc] == OPEN:
                        self._grid[nr][nc] = PATH
                    moved = True
                    break

            if not moved:   # jalan buntu → backtrack
                stack.pop()
                self._popCount += 1
                if self._grid[row][col] == PATH:
                    self._grid[row][col] = TRIED

        return False

    # ── reset ────────────────────────────────────────────────
    def reset(self):
        for r in range(self._numRows):
            for c in range(self._numCols):
                if self._grid[r][c] in (PATH, TRIED):
                    self._grid[r][c] = OPEN
        if self._startCell:
            sr, sc = self._startCell
            self._grid[sr][sc] = START
        if self._exitCell:
            er, ec = self._exitCell
            self._grid[er][ec] = EXIT

    # ── tampilkan labirin ────────────────────────────────────
    def draw(self, clear_screen=False):
        if clear_screen:
            print("\033[H\033[J", end="")

        color_map = {
            WALL : Color.WALL,
            OPEN : Color.OPEN,
            START: Color.START,
            EXIT : Color.EXIT,
            PATH : Color.PATH,
            TRIED: Color.TRIED,
        }
        char_map = {
            WALL : "##", OPEN : "  ", START: " S",
            EXIT : " E", PATH : " x", TRIED: " o",
        }

        print(Color.DIM + "+" + "-" * (self._numCols * 2 - 1) + "+" + Color.RESET)
        for r in range(self._numRows):
            row_str = Color.DIM + "|" + Color.RESET
            for c in range(self._numCols):
                t = self._grid[r][c]
                row_str += f"{color_map[t]}{char_map[t]}{Color.RESET}"
            print(row_str + Color.DIM + "|" + Color.RESET)
        print(Color.DIM + "+" + "-" * (self._numCols * 2 - 1) + "+" + Color.RESET)

    def _printLive(self, stack, step):
        top = stack.peek() if not stack.isEmpty() else "-"
        print(f"\n{Color.INFO}Langkah : {Color.STAT}{step}{Color.RESET}  |  "
              f"{Color.INFO}Stack size : {Color.STAT}{len(stack)}{Color.RESET}  |  "
              f"{Color.INFO}TOP : {Color.STAT}{top}{Color.RESET}")
        print(f"{Color.INFO}Push : {Color.STAT}{self._pushCount}{Color.RESET}  |  "
              f"{Color.INFO}Pop (backtrack) : {Color.STAT}{self._popCount}{Color.RESET}  |  "
              f"{Color.INFO}Max stack : {Color.STAT}{self._maxStack}{Color.RESET}")

    def stats(self):
        print(f"\n{Color.TITLE}{'='*45}{Color.RESET}")
        print(f"{Color.TITLE}  STATISTIK PENCARIAN JALUR{Color.RESET}")
        print(f"{Color.TITLE}{'='*45}{Color.RESET}")
        status = (f"{Color.START}DITEMUKAN ✓{Color.RESET}" if self._solved
                  else f"{Color.EXIT}TIDAK ADA JALUR ✗{Color.RESET}")
        print(f"  Status           : {status}")
        if self._solved:
            print(f"  Panjang jalur    : {Color.STAT}{self._pathLen} sel{Color.RESET}")
        print(f"  Total push()     : {Color.STAT}{self._pushCount}{Color.RESET}  (langkah maju)")
        print(f"  Total pop()      : {Color.STAT}{self._popCount}{Color.RESET}  (backtrack)")
        print(f"  Stack size maks  : {Color.STAT}{self._maxStack}{Color.RESET}")
        print(f"  Ukuran labirin   : {Color.STAT}{self._numRows}x{self._numCols}{Color.RESET}")
        print(f"{Color.TITLE}{'='*45}{Color.RESET}\n")


# ============================================================
#  BAGIAN 4: PROGRAM UTAMA
# ============================================================

BANNER = f"""
{Color.TITLE}╔══════════════════════════════════════════════════════╗
║        MAZE SOLVER  –  Stack + Backtracking          ║
║        Struktur Data  |  Bab 7: Tumpukan             ║
╚══════════════════════════════════════════════════════╝{Color.RESET}

{Color.INFO}Legenda:{Color.RESET}
  {Color.START} S {Color.RESET} = Start      {Color.EXIT} E {Color.RESET} = Exit
  {Color.PATH} x {Color.RESET} = Jalur aktif {Color.TRIED} o {Color.RESET} = Jalan buntu
  {Color.DIM}## {Color.RESET} = Dinding     {Color.RESET}   {Color.RESET} = Lorong
"""


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"  Masukkan angka {lo}–{hi}.")
        except ValueError:
            print("  Input tidak valid.")


def main():
    print(BANNER)

    # mode demo langsung
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        m = Maze(11, 11)
        m.generate()
        print(f"{Color.DIM}Labirin yang di-generate:{Color.RESET}\n")
        m.draw()
        print(f"\n{Color.INFO}Mencari jalur ...{Color.RESET}\n")
        m.findPath(animate=False)
        m.draw()
        m.stats()
        return

    # menu utama
    while True:
        print(f"{Color.INFO}Pilih ukuran labirin:{Color.RESET}")
        print("  [1] Kecil   – 11×11")
        print("  [2] Sedang  – 15×15")
        print("  [3] Besar   – 21×21")
        print("  [4] Kustom")
        print("  [5] Keluar")
        pilihan = get_int("Pilihan: ", 1, 5)

        if pilihan == 5:
            print(f"\n{Color.DIM}Sampai jumpa!{Color.RESET}\n")
            break

        size_map = {1: 11, 2: 15, 3: 21}
        if pilihan in size_map:
            n = size_map[pilihan]
            rows, cols = n, n
        else:
            print("\nUkuran harus ganjil (contoh: 11, 15, 21)")
            rows = get_int("Jumlah baris (5–41): ", 5, 41)
            cols = get_int("Jumlah kolom (5–41): ", 5, 41)
            rows = rows if rows % 2 == 1 else rows + 1
            cols = cols if cols % 2 == 1 else cols + 1

        print(f"\n{Color.INFO}Pilih kecepatan animasi:{Color.RESET}")
        print("  [1] Lambat  – 0.20 detik/langkah")
        print("  [2] Normal  – 0.05 detik/langkah")
        print("  [3] Cepat   – 0.01 detik/langkah")
        print("  [4] Instan  – tanpa animasi")
        kecepatan = get_int("Pilihan: ", 1, 4)
        delay_map = {1: 0.20, 2: 0.05, 3: 0.01, 4: 0.0}
        delay     = delay_map[kecepatan]
        animate   = delay > 0.0

        print(f"\n{Color.INFO}Generating labirin {rows}×{cols} ...{Color.RESET}\n")
        m = Maze(rows, cols)
        m.generate()

        if not animate:
            m.draw()
            print(f"\n{Color.INFO}Mencari jalur ...{Color.RESET}\n")

        m.findPath(animate=animate, delay=delay)

        if not animate:
            m.draw()

        m.stats()

        lagi = input(f"{Color.INFO}Generate labirin baru? (y/n): {Color.RESET}").strip().lower()
        if lagi != "y":
            print(f"\n{Color.DIM}Sampai jumpa!{Color.RESET}\n")
            break
        print()


if __name__ == "__main__":
    main()
