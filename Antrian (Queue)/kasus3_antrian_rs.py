"""
Kasus 3: Antrian Rumah Sakit (Priority Queue)
Ukuran window FIXED 1280x720 px - tidak bisa di-resize
"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from collections import deque

DPI = 100
W_IN, H_IN = 12.80, 7.20

PRIORITY_LABELS = {0:"KRITIS", 1:"DARURAT", 2:"MENENGAH", 3:"RINGAN"}
PRIORITY_COLORS = {0:"#E74C3C", 1:"#F39C12", 2:"#3498DB",  3:"#2ECC71"}

INCOMING = [
    ("Budi",3),("Ani",0),("Citra",2),
    ("Dedi",0),("Eka",1),("Fajar",2),("Gita",3),
]

class BPQ:
    def __init__(self, lv): self._q = [deque() for _ in range(lv)]
    def enqueue(self, item, p): self._q[p].append(item)
    def dequeue(self):
        for l in self._q:
            if l: return l.popleft()
    def isEmpty(self): return all(len(l)==0 for l in self._q)
    def snapshot(self):
        return [(nm,p) for p,l in enumerate(self._q) for nm in l]

def build_steps():
    pq=BPQ(4); steps=[]; served=[]
    steps.append({"snap":[],"served":[],"msg":"Antrian RS siap","phase":"info","hl":None})
    for nm,p in INCOMING:
        pq.enqueue(nm,p)
        steps.append({"snap":pq.snapshot(),"served":list(served),
                      "msg":f"{nm} tiba  --  Prioritas: {PRIORITY_LABELS[p]}",
                      "phase":"arrive","hl":(nm,p)})
    while not pq.isEmpty():
        snap=pq.snapshot(); nm0,p0=snap[0]; pq.dequeue()
        served.append((nm0,p0))
        steps.append({"snap":pq.snapshot(),"served":list(served),
                      "msg":f"Dipanggil: {nm0}  ({PRIORITY_LABELS[p0]})",
                      "phase":"serve","hl":(nm0,p0)})
    steps.append({"snap":[],"served":list(served),
                  "msg":"Semua pasien sudah dilayani!","phase":"done","hl":None})
    return steps

steps = build_steps()

fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_facecolor("#12131F")
ax.set_facecolor("#12131F")
ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis("off")

def on_resize(event):
    fig.set_size_inches(W_IN, H_IN, forward=False)
fig.canvas.mpl_connect("resize_event", on_resize)

# 4 kolom prioritas
COL_X = [0.30, 3.40, 6.50, 9.60]
COL_W = 2.70
HDR_Y  = H_IN - 1.20   # batas bawah header
CARD_H = 0.68
CARD_GAP = 0.14
CARD_TOP = HDR_Y - 0.12

DONE_Y = 0.28
DONE_H = 0.58
DONE_W = 1.62

def update(frame):
    ax.clear()
    ax.set_facecolor("#12131F")
    ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis("off")
    fig.patch.set_facecolor("#12131F")

    step = steps[frame % len(steps)]
    snap,served,msg,phase,hl = step["snap"],step["served"],step["msg"],step["phase"],step["hl"]

    ax.set_title("Kasus 3 : Antrian Rumah Sakit  —  Priority Queue",
                 color="white", fontsize=13, fontweight="bold", pad=8)

    # Header kolom
    for p in range(4):
        lx = COL_X[p]
        ax.add_patch(mpatches.FancyBboxPatch(
            (lx, H_IN-1.15), COL_W, 0.72,
            boxstyle="round,pad=0.06", lw=2,
            edgecolor="white", facecolor=PRIORITY_COLORS[p], alpha=0.9))
        ax.text(lx+COL_W/2, H_IN-0.79,
                f"P{p}  |  {PRIORITY_LABELS[p]}",
                fontsize=10, ha="center", va="center",
                color="white", fontweight="bold")

    ax.axhline(y=H_IN-1.18, color="#2C3E50", lw=1.5, xmin=0.02, xmax=0.98)

    # Isi kolom
    by_level = {0:[],1:[],2:[],3:[]}
    for nm,p in snap: by_level[p].append(nm)

    for p in range(4):
        lx  = COL_X[p]
        col = PRIORITY_COLORS[p]
        pats = by_level[p]
        for i, nm in enumerate(pats):
            y0  = CARD_TOP - i*(CARD_H+CARD_GAP)
            is_hl = hl and hl[0]==nm and hl[1]==p
            ax.add_patch(mpatches.FancyBboxPatch(
                (lx+0.14, y0-CARD_H), COL_W-0.28, CARD_H,
                boxstyle="round,pad=0.06", lw=3.5 if is_hl else 1.5,
                edgecolor="#FFD700" if is_hl else "white",
                facecolor=col, alpha=0.92))
            ax.text(lx+COL_W/2, y0-CARD_H/2,
                    nm, fontsize=11, ha="center", va="center",
                    color="white", fontweight="bold")
        if not pats:
            ax.text(lx+COL_W/2, CARD_TOP-0.55,
                    "(kosong)", fontsize=9, ha="center", color="#2A2A4A")

    # Pemisah bawah
    ax.axhline(y=1.82, color="#2C3E50", lw=1.5, linestyle="--",
               xmin=0.02, xmax=0.98)
    ax.text(0.30, 1.60, "SUDAH DILAYANI (urutan) :",
            color="#2ECC71", fontsize=9.5, fontweight="bold")

    for j,(nm,p) in enumerate(served):
        sx = 0.35 + j*(DONE_W+0.18)
        ax.add_patch(mpatches.FancyBboxPatch(
            (sx, DONE_Y), DONE_W, DONE_H,
            boxstyle="round,pad=0.05", lw=1.5,
            edgecolor="#2ECC71", facecolor=PRIORITY_COLORS[p], alpha=0.55))
        ax.text(sx+0.18, DONE_Y+DONE_H/2, "v",
                fontsize=9, va="center", color="#2ECC71", fontweight="bold")
        ax.text(sx+0.28+(DONE_W-0.28)/2, DONE_Y+DONE_H/2,
                nm, fontsize=8.5, ha="center", va="center",
                color="white", fontweight="bold")

    # Pesan
    pc = {"info":"#BDC3C7","arrive":"#F39C12","serve":"#2ECC71","done":"#FFD700"}
    ax.text(W_IN/2, 1.20, msg, fontsize=10.5, ha="center", va="center",
            color=pc.get(phase,"white"), fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.30",
                      facecolor="#0D1117", edgecolor="#2C3E50"))

ani = animation.FuncAnimation(fig, update, frames=len(steps),
                               interval=1300, repeat=True, repeat_delay=2000)
try:
    mng = plt.get_current_fig_manager()
    mng.resize(int(W_IN*DPI), int(H_IN*DPI))
    mng.window.resizable(False, False)
except Exception:
    pass

plt.tight_layout(pad=0.5)
plt.show()
