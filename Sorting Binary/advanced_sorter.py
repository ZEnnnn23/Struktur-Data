"""
AdvancedSorter — Implementasi Bab 12
Mencakup:
  1. Array Merge Sort  (virtual sublists + single tmpArray)
  2. Linked List Merge Sort (fast-slow pointer + dummy merge)
  3. Quick Sort          (median-of-three pivot + depth-limit fallback)
"""

import math
from typing import List, Optional


class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)          # satu alokasi, dipakai semua rekursi
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Gabungkan dua virtual sublist arr[left_start..mid] dan arr[mid+1..right_end].
        Hasil disimpan sementara di tmp_array lalu disalin kembali ke arr.
        Operasi STABLE: elemen sama dari sublist kiri diambil lebih dulu (pakai <=).
        """
        a = left_start          # pointer sublist kiri
        b = mid + 1             # pointer sublist kanan
        m = 0                   # pointer ke tmp_array

        # Merge selama kedua sublist masih punya elemen
        while a <= mid and b <= right_end:
            # <= menjamin stabilitas: elemen kiri diprioritaskan jika sama
            if arr[a] <= arr[b]:
                tmp_array[m] = arr[a]
                a += 1
            else:
                tmp_array[m] = arr[b]
                b += 1
            m += 1

        # Sisakan elemen sublist kiri
        while a <= mid:
            tmp_array[m] = arr[a]
            a += 1
            m += 1

        # Sisakan elemen sublist kanan
        while b <= right_end:
            tmp_array[m] = arr[b]
            b += 1
            m += 1

        # Salin hasil merge kembali ke arr
        for i in range(right_end - left_start + 1):
            arr[left_start + i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Base case: 0 atau 1 node → sudah terurut
        if head is None or head.next is None:
            return head

        # Pisah menjadi dua sublist
        right_head = self._split_linked_list(head)
        left_head  = head

        # Rekursi pada masing-masing sublist
        left_sorted  = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        # Gabungkan dua sublist terurut
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Temukan midpoint menggunakan fast-slow pointer (satu traversal).
          - midPoint  : bergerak 1 langkah per iterasi
          - curNode   : bergerak 2 langkah per iterasi
        Ketika curNode jatuh ke None, midPoint ada di node terakhir sublist kiri.
        Putus link, kembalikan head sublist kanan.
        """
        mid_point = head
        cur_node  = head.next       # curNode mulai 1 langkah di depan

        while cur_node is not None and cur_node.next is not None:
            cur_node  = cur_node.next.next   # maju 2
            mid_point = mid_point.next       # maju 1

        # mid_point sekarang = node terakhir sublist kiri
        right_head        = mid_point.next
        mid_point.next    = None            # putus rantai
        return right_head

    def _merge_linked_lists(self,
                             listA: Optional[ListNode],
                             listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Gabungkan dua sorted linked list secara STABLE.
        Gunakan dummy node untuk menghindari kasus khusus head.
        Hanya memodifikasi pointer .next — tidak ada alokasi node baru.
        """
        dummy = ListNode(0)         # node sementara, bukan bagian data final
        tail  = dummy

        while listA is not None and listB is not None:
            # <= menjamin stabilitas
            if listA.data <= listB.data:
                tail.next = listA
                listA     = listA.next
            else:
                tail.next = listB
                listB     = listB.next
            tail      = tail.next
            tail.next = None        # isolasi node yang baru disambung

        # Sambung sisa sublist yang belum habis (tidak perlu iterasi)
        if listA is not None:
            tail.next = listA
        else:
            tail.next = listB

        return dummy.next           # lewati dummy, kembalikan head asli

    # =========================================================
    # 3. QUICK SORT (Median-of-Three + Depth-Limit Fallback)
    # =========================================================

    def quick_sort(self, arr: List[int]) -> List[int]:
        """Entry point quick sort dengan depth-limit fallback ke merge sort."""
        n = len(arr)
        if n <= 1:
            return arr
        limit = int(2 * math.log2(n)) if n > 1 else 1
        self._quick_sort_recursive(arr, 0, n - 1, limit, 0)
        return arr

    def _quick_sort_recursive(self, arr, first, last, limit, depth):
        if first >= last:
            return

        # Fallback ke merge sort jika kedalaman melebihi batas
        if depth > limit:
            sub = arr[first:last + 1]
            self.sort_array(sub)
            arr[first:last + 1] = sub
            return

        pos = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pos - 1, limit, depth + 1)
        self._quick_sort_recursive(arr, pos + 1, last, limit, depth + 1)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Pilih pivot menggunakan Median-of-Three:
          Kandidat: arr[first], arr[mid], arr[last]
          Tukar agar median berada di arr[first], lalu jalankan partisi standar.

        Catatan stabilitas: partisi in-place dengan two-pointer tidak menjamin
        stabilitas penuh karena swap bisa mengubah urutan relatif elemen sama.
        Stabilitas tidak diwajibkan pada quick sort (hanya merge sort).
        """
        mid = (first + last) // 2

        # --- Pilih median dari tiga kandidat ---
        # Langkah: urutkan ketiga indeks sehingga arr[first] = median
        # Trick: bawa nilai terkecil ke first, terbesar ke last, sisanya = median
        if arr[mid] < arr[first]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[last] < arr[first]:
            arr[first], arr[last] = arr[last], arr[first]
        # Sekarang arr[first] = terkecil dari tiga; bandingkan mid vs last
        if arr[mid] < arr[last]:
            # Urutan: first ≤ mid ≤ last  →  median = mid
            arr[first], arr[mid] = arr[mid], arr[first]
        else:
            # Urutan: first ≤ last ≤ mid  →  median = last
            arr[first], arr[last] = arr[last], arr[first]
        # arr[first] sekarang berisi median = pivot

        # --- Partisi standar (Listing 12.5) ---
        pivot = arr[first]
        left  = first + 1
        right = last

        while left <= right:
            # Geser left ke kanan sampai temukan elemen >= pivot
            while left <= right and arr[left] < pivot:
                left += 1
            # Geser right ke kiri sampai temukan elemen <= pivot
            while right >= left and arr[right] >= pivot:
                right -= 1
            # Tukar jika belum cross
            if left < right:
                arr[left], arr[right] = arr[right], arr[left]

        # Tempatkan pivot ke posisi akhirnya
        if right != first:
            arr[first], arr[right] = arr[right], arr[first]

        return right


# =========================================================
# Helper: cetak linked list
# =========================================================
def list_to_ll(lst):
    if not lst:
        return None
    head = ListNode(lst[0])
    cur  = head
    for v in lst[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head

def ll_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result


# =========================================================
# Test / Demo
# =========================================================
if __name__ == "__main__":
    sorter = AdvancedSorter()

    print("=" * 55)
    print("1. ARRAY MERGE SORT (virtual sublist + single tmpArray)")
    print("=" * 55)
    arr1 = [10, 23, 51, 18, 4, 31, 13, 5]
    print(f"  Input  : {arr1}")
    sorter.sort_array(arr1)
    print(f"  Output : {arr1}")

    arr2 = [5, 4, 3, 2, 1]             # reverse-sorted (worst case quick sort)
    print(f"  Input  : {arr2}")
    sorter.sort_array(arr2)
    print(f"  Output : {arr2}")

    arr3 = [3, 1, 4, 1, 5, 9, 2, 6]   # ada duplikat
    print(f"  Input  : {arr3}")
    sorter.sort_array(arr3)
    print(f"  Output : {arr3}")

    print()
    print("=" * 55)
    print("2. LINKED LIST MERGE SORT (fast-slow + dummy merge)")
    print("=" * 55)
    ll1 = list_to_ll([23, 51, 2, 18, 4, 31])
    print(f"  Input  : {ll_to_list(ll1)}")
    ll1 = sorter.sort_linked_list(ll1)
    print(f"  Output : {ll_to_list(ll1)}")

    ll2 = list_to_ll([5, 5, 3, 3, 1])   # duplikat
    print(f"  Input  : {ll_to_list(ll2)}")
    ll2 = sorter.sort_linked_list(ll2)
    print(f"  Output : {ll_to_list(ll2)}")

    print()
    print("=" * 55)
    print("3. QUICK SORT (median-of-three + depth-limit fallback)")
    print("=" * 55)
    arr4 = [10, 23, 51, 18, 4, 31, 13, 5]
    print(f"  Input  : {arr4}")
    sorter.quick_sort(arr4)
    print(f"  Output : {arr4}")

    arr5 = list(range(20, 0, -1))       # descending — worst case pivot pertama
    print(f"  Input  : {arr5}")
    sorter.quick_sort(arr5)
    print(f"  Output : {arr5}")

    arr6 = [7, 2, 9, 2, 7, 4]          # duplikat
    print(f"  Input  : {arr6}")
    sorter.quick_sort(arr6)
    print(f"  Output : {arr6}")
