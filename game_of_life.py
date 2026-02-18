"""
GAME OF LIFE - Tugas Struktur Data
Nama: [Isi nama kamu]
NIM: [Isi NIM kamu]

Apa itu Game of Life?
- Game otomatis yang dibuat oleh John Conway
- Ada grid (kotak-kotak) yang isinya sel hidup atau mati
- Setiap generasi, sel berubah ikutin 4 aturan

4 Aturan:
1. Sel hidup + tetangga < 2 = mati (kesepian)
2. Sel hidup + tetangga 2-3 = tetap hidup
3. Sel hidup + tetangga > 3 = mati (sesak)
4. Sel mati + tetangga = 3 = jadi hidup (lahir)
"""

import tkinter as tk
import random

# Ukuran grid
UKURAN_SEL = 15
JUMLAH_KOLOM = 50
JUMLAH_BARIS = 35

# Warna
WARNA_HIDUP = "#00ff00"  # hijau
WARNA_MATI = "#000000"   # hitam
WARNA_GRID = "#333333"   # abu-abu gelap


# Fungsi buat grid kosong
def buat_grid_baru():
    """Buat grid 2D berisi angka 0 semua"""
    grid = []
    for i in range(JUMLAH_BARIS):
        baris = []
        for j in range(JUMLAH_KOLOM):
            baris.append(0)
        grid.append(baris)
    return grid


# Fungsi hitung tetangga
def hitung_tetangga(grid, baris, kolom):
    """Hitung berapa tetangga yang hidup di sekitar sel ini"""
    jumlah = 0
    
    # Cek 8 arah: atas, bawah, kiri, kanan, diagonal
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Jangan hitung sel itu sendiri
            if i == 0 and j == 0:
                continue
            
            # Posisi tetangga
            baris_tetangga = (baris + i) % JUMLAH_BARIS
            kolom_tetangga = (kolom + j) % JUMLAH_KOLOM
            
            # Tambah kalau tetangga hidup
            if grid[baris_tetangga][kolom_tetangga] == 1:
                jumlah = jumlah + 1
    
    return jumlah


# Fungsi update grid ke generasi berikutnya
def generasi_berikutnya(grid_lama):
    """Buat generasi baru berdasarkan aturan Game of Life"""
    # Buat grid baru
    grid_baru = buat_grid_baru()
    
    # Loop semua sel
    for baris in range(JUMLAH_BARIS):
        for kolom in range(JUMLAH_KOLOM):
            # Hitung tetangga
            tetangga = hitung_tetangga(grid_lama, baris, kolom)
            
            # Cek aturan
            if grid_lama[baris][kolom] == 1:  # Kalau sel hidup
                if tetangga == 2 or tetangga == 3:
                    grid_baru[baris][kolom] = 1  # Tetap hidup
                else:
                    grid_baru[baris][kolom] = 0  # Mati
            else:  # Kalau sel mati
                if tetangga == 3:
                    grid_baru[baris][kolom] = 1  # Lahir
                else:
                    grid_baru[baris][kolom] = 0  # Tetap mati
    
    return grid_baru


# Class untuk aplikasi
class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.root.title("Game of Life - Tugas Struktur Data")
        
        # Data
        self.grid = buat_grid_baru()
        self.jalan = False
        self.generasi = 0
        
        # Buat UI
        self.buat_tampilan()
        self.gambar_grid()
    
    def buat_tampilan(self):
        # Frame atas untuk tombol
        frame_atas = tk.Frame(self.root)
        frame_atas.pack(pady=10)
        
        # Tombol-tombol
        self.tombol_start = tk.Button(frame_atas, text="START", 
                                       command=self.start, width=10)
        self.tombol_start.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_atas, text="STOP", 
                  command=self.stop, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_atas, text="RESET", 
                  command=self.reset, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_atas, text="RANDOM", 
                  command=self.isi_random, width=10).pack(side=tk.LEFT, padx=5)
        
        # Label info
        frame_info = tk.Frame(self.root)
        frame_info.pack()
        
        self.label_gen = tk.Label(frame_info, text="Generasi: 0", 
                                  font=("Arial", 12))
        self.label_gen.pack()
        
        self.label_info = tk.Label(frame_info, 
                                   text="Klik kotak untuk hidupin/matikin sel", 
                                   font=("Arial", 10))
        self.label_info.pack()
        
        # Canvas untuk grid
        lebar = JUMLAH_KOLOM * UKURAN_SEL
        tinggi = JUMLAH_BARIS * UKURAN_SEL
        
        self.canvas = tk.Canvas(self.root, width=lebar, height=tinggi, 
                                bg=WARNA_MATI)
        self.canvas.pack(pady=10)
        
        # Event klik
        self.canvas.bind("<Button-1>", self.klik_canvas)
    
    def gambar_grid(self):
        """Gambar semua sel di canvas"""
        self.canvas.delete("all")
        
        for baris in range(JUMLAH_BARIS):
            for kolom in range(JUMLAH_KOLOM):
                x1 = kolom * UKURAN_SEL
                y1 = baris * UKURAN_SEL
                x2 = x1 + UKURAN_SEL
                y2 = y1 + UKURAN_SEL
                
                # Pilih warna
                if self.grid[baris][kolom] == 1:
                    warna = WARNA_HIDUP
                else:
                    warna = WARNA_MATI
                
                # Gambar kotak
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                             fill=warna, outline=WARNA_GRID)
    
    def klik_canvas(self, event):
        """Kalau canvas diklik, toggle sel"""
        kolom = event.x // UKURAN_SEL
        baris = event.y // UKURAN_SEL
        
        # Pastikan dalam batas
        if 0 <= baris < JUMLAH_BARIS and 0 <= kolom < JUMLAH_KOLOM:
            # Toggle: 0 jadi 1, 1 jadi 0
            if self.grid[baris][kolom] == 0:
                self.grid[baris][kolom] = 1
            else:
                self.grid[baris][kolom] = 0
            
            self.gambar_grid()
    
    def update(self):
        """Update satu generasi"""
        if self.jalan:
            self.grid = generasi_berikutnya(self.grid)
            self.generasi = self.generasi + 1
            self.label_gen.config(text=f"Generasi: {self.generasi}")
            self.gambar_grid()
            
            # Panggil lagi setelah 100ms
            self.root.after(100, self.update)
    
    def start(self):
        """Mulai simulasi"""
        if not self.jalan:
            self.jalan = True
            self.update()
    
    def stop(self):
        """Stop simulasi"""
        self.jalan = False
    
    def reset(self):
        """Reset semua"""
        self.stop()
        self.grid = buat_grid_baru()
        self.generasi = 0
        self.label_gen.config(text="Generasi: 0")
        self.gambar_grid()
    
    def isi_random(self):
        """Isi grid dengan sel random"""
        self.stop()
        self.generasi = 0
        
        for baris in range(JUMLAH_BARIS):
            for kolom in range(JUMLAH_KOLOM):
                # 30% chance jadi hidup
                if random.random() < 0.3:
                    self.grid[baris][kolom] = 1
                else:
                    self.grid[baris][kolom] = 0
        
        self.label_gen.config(text="Generasi: 0")
        self.gambar_grid()


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLife(root)
    root.mainloop()
