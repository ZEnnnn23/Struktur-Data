# ============================================================
# LATIHAN SOAL 8 - Python Sets & Dictionaries
# Nama: (isi nama kamu)
# NIM: (isi NIM kamu)
# ============================================================


# ============================================================
# 1. DEDUPLIKASI
# ============================================================
def deduplikasi(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# ============================================================
# 2. INTERSECTION DUA ARRAY
# ============================================================
def intersection(list1, list2):
    set2 = set(list2)
    result = []
    for item in list1:
        if item in set2:
            result.append(item)
    return result


# ============================================================
# 3. ANAGRAM CHECK
# ============================================================
def is_anagram(str1, str2):
    if len(str1) != len(str2):
        return False
    
    count = {}
    for char in str1:
        count[char] = count.get(char, 0) + 1
    
    for char in str2:
        count[char] = count.get(char, 0) - 1
    
    for value in count.values():
        if value != 0:
            return False
    
    return True


# ============================================================
# 4. FIRST RECURRING CHARACTER
# ============================================================
def first_recurring(s):
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None


# ============================================================
# 5. SIMULASI BUKU TELEPON
# ============================================================
def buku_telepon():
    kontak = {}
    
    while True:
        print("\n=== BUKU TELEPON ===")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Tampilkan Semua")
        print("4. Keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            nama = input("Nama: ")
            nomor = input("Nomor: ")
            kontak[nama] = nomor
            print(f"Kontak '{nama}' berhasil ditambahkan!")
        
        elif pilihan == "2":
            nama = input("Cari nama: ")
            if nama in kontak:
                print(f"{nama} -> {kontak[nama]}")
            else:
                print("Kontak tidak ditemukan.")
        
        elif pilihan == "3":
            if kontak:
                print("\nDaftar Kontak:")
                for nama, nomor in kontak.items():
                    print(f"  {nama} -> {nomor}")
            else:
                print("Buku telepon masih kosong.")
        
        elif pilihan == "4":
            print("Keluar...")
            break
        
        else:
            print("Pilihan tidak valid!")


# ============================================================
# TESTING SEMUA FUNGSI
# ============================================================
if __name__ == "__main__":
    print("=" * 40)
    print("1. DEDUPLIKASI")
    print("=" * 40)
    print(deduplikasi([1, 2, 3, 2, 1, 4]))        # [1, 2, 3, 4]
    print(deduplikasi(['a', 'b', 'a', 'c']))       # ['a', 'b', 'c']
    
    print("\n" + "=" * 40)
    print("2. INTERSECTION DUA ARRAY")
    print("=" * 40)
    print(intersection([1, 2, 3, 4], [2, 4, 6]))           # [2, 4]
    print(intersection(['a', 'b', 'c'], ['b', 'c', 'd']))  # ['b', 'c']
    
    print("\n" + "=" * 40)
    print("3. ANAGRAM CHECK")
    print("=" * 40)
    print(is_anagram("listen", "silent"))  # True
    print(is_anagram("hello", "world"))    # False
    
    print("\n" + "=" * 40)
    print("4. FIRST RECURRING CHARACTER")
    print("=" * 40)
    print(first_recurring("abcadb"))  # a
    print(first_recurring("abcdef"))  # None
    
    print("\n" + "=" * 40)
    print("5. SIMULASI BUKU TELEPON")
    print("=" * 40)
    buku_telepon()
