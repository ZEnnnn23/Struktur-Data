"""
Tugas Rekursif - Algoritma Backtracking
Berisi 3 program:
  1. N-Queens Problem
  2. Knight's Tour Problem
  3. Knapsack Problem
"""

# ============================================================
# 1. N-QUEENS PROBLEM
# ============================================================

def is_safe_queens(board, row, col, n):
    """Cek apakah aman meletakkan ratu di posisi (row, col)."""
    # Cek kolom yang sama di baris sebelumnya
    for i in range(row):
        if board[i] == col:
            return False
    # Cek diagonal kiri atas
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i] == j:
            return False
        i -= 1
        j -= 1
    # Cek diagonal kanan atas
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i] == j:
            return False
        i -= 1
        j += 1
    return True


def solve_nqueens(board, row, n, solutions):
    """Rekursif backtracking untuk N-Queens."""
    if row == n:
        solutions.append(board[:])
        return
    for col in range(n):
        if is_safe_queens(board, row, col, n):
            board[row] = col
            solve_nqueens(board, row + 1, n, solutions)
            board[row] = -1  # backtrack


def print_queen_board(solution, n):
    """Cetak papan N-Queens dalam format visual."""
    print()
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[row] == col:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()


def nqueens_main():
    print("=" * 50)
    print("       N-QUEENS PROBLEM")
    print("=" * 50)
    try:
        n = int(input("Masukkan ukuran papan (N): "))
        if n < 1:
            print("Ukuran papan harus >= 1.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    board = [-1] * n
    solutions = []
    solve_nqueens(board, 0, n, solutions)

    if not solutions:
        print(f"\nTidak ada solusi untuk {n}-Queens.")
    else:
        print(f"\nDitemukan {len(solutions)} solusi untuk {n}-Queens.")
        print("\nMenunjukkan solusi pertama:")
        print_queen_board(solutions[0], n)
        print(f"Posisi ratu per baris: {[s + 1 for s in solutions[0]]}")


# ============================================================
# 2. KNIGHT'S TOUR PROBLEM
# ============================================================

# 8 kemungkinan gerakan kuda (dx, dy)
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def get_degree(board, x, y, n):
    """Heuristic Warnsdorff: hitung jumlah gerakan valid dari posisi (x,y)."""
    count = 0
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
            count += 1
    return count


def solve_knights_tour(board, x, y, move_num, n, path):
    """Rekursif backtracking dengan heuristic Warnsdorff untuk Knight's Tour."""
    if move_num == n * n:
        return True

    # Urutkan gerakan berdasarkan degree terkecil (Warnsdorff's heuristic)
    next_moves = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
            degree = get_degree(board, nx, ny, n)
            next_moves.append((degree, nx, ny))
    next_moves.sort()

    for _, nx, ny in next_moves:
        board[nx][ny] = move_num
        path.append((nx, ny))
        if solve_knights_tour(board, nx, ny, move_num + 1, n, path):
            return True
        # Backtrack
        board[nx][ny] = -1
        path.pop()
    return False


def print_knight_board(board, n):
    """Cetak papan Knight's Tour dengan nomor urut langkah."""
    print()
    for i in range(n):
        row_str = ""
        for j in range(n):
            row_str += f"{board[i][j]:3d} "
        print(row_str)
    print()


def knights_tour_main():
    print("=" * 50)
    print("       KNIGHT'S TOUR PROBLEM")
    print("=" * 50)
    try:
        n = int(input("Masukkan ukuran papan (disarankan 5-8): "))
        if n < 5:
            print("Ukuran papan minimal 5 agar solusi ada.")
            return
        start_row = int(input(f"Masukkan posisi baris awal kuda (0-{n-1}): "))
        start_col = int(input(f"Masukkan posisi kolom awal kuda (0-{n-1}): "))
        if not (0 <= start_row < n and 0 <= start_col < n):
            print("Posisi awal tidak valid.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    # Inisialisasi papan dengan -1 (belum dikunjungi)
    board = [[-1] * n for _ in range(n)]
    board[start_row][start_col] = 0
    path = [(start_row, start_col)]

    print(f"\nMencari solusi dari posisi ({start_row}, {start_col})...")
    found = solve_knights_tour(board, start_row, start_col, 1, n, path)

    if found:
        print("Solusi ditemukan!")
        print_knight_board(board, n)
        print("Urutan langkah kuda:")
        for step, (r, c) in enumerate(path):
            print(f"  Langkah {step:3d}: ({r}, {c})")
    else:
        print("Tidak ada solusi dari posisi ini.")


# ============================================================
# 3. KNAPSACK PROBLEM (0/1)
# ============================================================

def knapsack_recursive(items, index, remaining_capacity, current_items, best):
    """
    Rekursif backtracking untuk 0/1 Knapsack.
    Mencari kombinasi barang yang totalnya <= target dan semaksimal mungkin.
    """
    if index == len(items) or remaining_capacity == 0:
        current_total = sum(current_items)
        if current_total > best[0]:
            best[0] = current_total
            best[1] = current_items[:]
        return

    weight = items[index]

    # Pilihan 1: Masukkan barang ke knapsack (jika muat)
    if weight <= remaining_capacity:
        current_items.append(weight)
        knapsack_recursive(items, index + 1, remaining_capacity - weight, current_items, best)
        current_items.pop()  # backtrack

    # Pilihan 2: Lewati barang ini
    knapsack_recursive(items, index + 1, remaining_capacity, current_items, best)


def knapsack_main():
    print("=" * 50)
    print("       KNAPSACK PROBLEM")
    print("=" * 50)
    print("Contoh: berat target 30, barang: 2 5 6 9 12 14 20")
    print()

    try:
        target = int(input("Masukkan berat target knapsack: "))
        items_input = input("Masukkan berat barang (pisahkan dengan spasi): ")
        items = list(map(int, items_input.strip().split()))
        if not items:
            print("Daftar barang kosong.")
            return
        if any(w <= 0 for w in items):
            print("Berat barang harus positif.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    print(f"\nMencari kombinasi untuk target {target} dari {len(items)} barang...")

    best = [0, []]  # [total_terbaik, daftar_barang]
    knapsack_recursive(items, 0, target, [], best)

    if best[0] == 0:
        print("Tidak ada barang yang bisa dimasukkan ke knapsack.")
    else:
        print(f"\nSolusi terbaik ditemukan!")
        print(f"  Total berat   : {best[0]} (dari target {target})")
        print(f"  Sisa kapasitas: {target - best[0]}")
        print(f"  Barang dipilih: {sorted(best[1])}")


# ============================================================
# MENU UTAMA
# ============================================================

def main():
    print("\n" + "=" * 50)
    print("   TUGAS REKURSIF & BACKTRACKING")
    print("=" * 50)
    print("1. N-Queens Problem")
    print("2. Knight's Tour Problem")
    print("3. Knapsack Problem")
    print("0. Keluar")
    print("=" * 50)

    while True:
        choice = input("\nPilih program (0-3): ").strip()
        if choice == "1":
            nqueens_main()
        elif choice == "2":
            knights_tour_main()
        elif choice == "3":
            knapsack_main()
        elif choice == "0":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")


if __name__ == "__main__":
    main()
