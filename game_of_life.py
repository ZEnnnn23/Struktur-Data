# Game of Life - Tugas Struktur Data
# Nama: (isi nama kamu)
# NIM: (isi nim kamu)

import tkinter as tk
import random

# Pengaturan
ukuran_kotak = 20
banyak_kolom = 40
banyak_baris = 30

# Grid - pakai list 2D
grid = []
for i in range(banyak_baris):
    baris = []
    for j in range(banyak_kolom):
        baris.append(0)  # 0 = mati, 1 = hidup
    grid.append(baris)

# Variabel
sedang_jalan = False
generasi = 0


# Fungsi hitung tetangga
def hitung_tetangga(baris, kolom):
    total = 0
    
    # Cek 8 kotak di sekitar
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # skip kotak sendiri
            
            baris_cek = (baris + i) % banyak_baris
            kolom_cek = (kolom + j) % banyak_kolom
            
            if grid[baris_cek][kolom_cek] == 1:
                total = total + 1
    
    return total


# Fungsi update grid
def update_grid():
    global grid, generasi
    
    # Buat grid baru
    grid_baru = []
    for i in range(banyak_baris):
        baris = []
        for j in range(banyak_kolom):
            baris.append(0)
        grid_baru.append(baris)
    
    # Isi grid baru pakai aturan
    for i in range(banyak_baris):
        for j in range(banyak_kolom):
            tetangga = hitung_tetangga(i, j)
            
            # Aturan Game of Life
            if grid[i][j] == 1:  # kalau hidup
                if tetangga == 2 or tetangga == 3:
                    grid_baru[i][j] = 1
                else:
                    grid_baru[i][j] = 0
            else:  # kalau mati
                if tetangga == 3:
                    grid_baru[i][j] = 1
                else:
                    grid_baru[i][j] = 0
    
    grid = grid_baru
    generasi = generasi + 1
    gambar_grid()
    label_gen.config(text="Generasi: " + str(generasi))
    
    if sedang_jalan:
        window.after(100, update_grid)


# Fungsi gambar grid
def gambar_grid():
    canvas.delete("all")
    
    for i in range(banyak_baris):
        for j in range(banyak_kolom):
            x1 = j * ukuran_kotak
            y1 = i * ukuran_kotak
            x2 = x1 + ukuran_kotak
            y2 = y1 + ukuran_kotak
            
            if grid[i][j] == 1:
                warna = "green"
            else:
                warna = "black"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=warna, outline="gray")


# Fungsi tombol start
def tombol_start():
    global sedang_jalan
    sedang_jalan = True
    update_grid()


# Fungsi tombol stop
def tombol_stop():
    global sedang_jalan
    sedang_jalan = False


# Fungsi tombol reset
def tombol_reset():
    global grid, generasi, sedang_jalan
    sedang_jalan = False
    generasi = 0
    
    for i in range(banyak_baris):
        for j in range(banyak_kolom):
            grid[i][j] = 0
    
    gambar_grid()
    label_gen.config(text="Generasi: 0")


# Fungsi tombol random
def tombol_random():
    global grid, generasi, sedang_jalan
    sedang_jalan = False
    generasi = 0
    
    for i in range(banyak_baris):
        for j in range(banyak_kolom):
            if random.random() < 0.3:
                grid[i][j] = 1
            else:
                grid[i][j] = 0
    
    gambar_grid()
    label_gen.config(text="Generasi: 0")


# Fungsi klik canvas
def klik(event):
    kolom = event.x // ukuran_kotak
    baris = event.y // ukuran_kotak
    
    if baris >= 0 and baris < banyak_baris and kolom >= 0 and kolom < banyak_kolom:
        if grid[baris][kolom] == 0:
            grid[baris][kolom] = 1
        else:
            grid[baris][kolom] = 0
        gambar_grid()


# Buat window
window = tk.Tk()
window.title("Game of Life")

# Label
label_gen = tk.Label(window, text="Generasi: 0", font=("Arial", 14))
label_gen.pack(pady=5)

# Tombol-tombol
frame_tombol = tk.Frame(window)
frame_tombol.pack(pady=5)

tk.Button(frame_tombol, text="START", command=tombol_start, width=10).pack(side=tk.LEFT, padx=5)
tk.Button(frame_tombol, text="STOP", command=tombol_stop, width=10).pack(side=tk.LEFT, padx=5)
tk.Button(frame_tombol, text="RESET", command=tombol_reset, width=10).pack(side=tk.LEFT, padx=5)
tk.Button(frame_tombol, text="RANDOM", command=tombol_random, width=10).pack(side=tk.LEFT, padx=5)

# Canvas
lebar = banyak_kolom * ukuran_kotak
tinggi = banyak_baris * ukuran_kotak
canvas = tk.Canvas(window, width=lebar, height=tinggi, bg="black")
canvas.pack(pady=5)
canvas.bind("<Button-1>", klik)

# Label petunjuk
label_info = tk.Label(window, text="Klik kotak untuk hidupin/matikin sel", font=("Arial", 10))
label_info.pack(pady=5)

# Gambar pertama kali
gambar_grid()

# Jalankan
window.mainloop()
