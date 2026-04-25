"""
Kasus 1: Antrian Printer Bersama
Fixed 1280x720 px — tidak bisa di-resize
Layout: kolom kiri=antrian, kolom kanan atas=printer, kolom kanan bawah=selesai
"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from collections import deque

DPI = 100
W_IN, H_IN = 12.80, 7.20

DOCUMENTS = [
    ("laporan.pdf",     "#E74C3C"),
    ("tugas.docx",      "#3498DB"),
    ("foto.jpg",        "#2ECC71"),
    ("presentasi.pptx", "#F39C12"),
    ("data.xlsx",       "#9B59B6"),
]

steps = []
for doc in DOCUMENTS:
    steps.append(("enqueue", doc))
for _ in range(len(DOCUMENTS)):
    steps.append(("start_print", None))
    steps.append(("finish_print", None))
steps.append(("done", None))

state = {"queue": deque(), "printed": [], "printing": None, "done": False}

fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_facecolor("#12131F")
ax.set_facecolor("#12131F")
ax.set_xlim(0, W_IN)
ax.set_ylim(0, H_IN)
ax.axis("off")

def on_resize(event):
    fig.set_size_inches(W_IN, H_IN, forward=False)
fig.canvas.mpl_connect("resize_event", on_resize)

# ── Layout (dalam inci) ───────────────────────────────────────────────────────
SEP       = 3.80          # garis vertikal pemisah

# Kolom kiri: antrian
CX, CW    = 0.30, 3.20   # x kiri, lebar kartu
CH, CGAP  = 0.70, 0.15   # tinggi kartu, gap antar kartu
CTOP      = 6.45          # y atas kartu #1 (bawah header)

# Kolom kanan atas: printer
PX, PW    = 4.10, 8.30   # x kiri, lebar
PY, PH    = 2.90, 3.80   # y bawah, tinggi

# Kolom kanan bawah: sudah dicetak
DONE_Y    = 0.22          # y bawah kartu done
DONE_H    = 0.62
DONE_W    = 1.75
DONE_X0   = 4.10          # x mulai kartu done pertama

# Info / status
INFO_Y    = 1.05          # y teks info bar

def draw(action, doc):
    ax.clear()
    ax.set_facecolor("#12131F")
    ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN)
    ax.axis("off")
    fig.patch.set_facecolor("#12131F")

    # Judul
    ax.set_title("Kasus 1 : Antrian Printer Bersama  —  Queue FIFO",
                 color="white", fontsize=13, fontweight="bold", pad=8)

    # Garis pemisah vertikal
    ax.axvline(x=SEP, color="#2C3E50", lw=2, linestyle="--",
               ymin=0.02, ymax=0.97)

    # ── Header area ───────────────────────────────────────────────────────────
    ax.text(CX + CW/2, 7.02,
            "ANTRIAN  DOKUMEN",
            color="#F39C12", fontsize=10.5, ha="center", fontweight="bold")
    ax.text(PX + PW/2, 7.02,
            "PRINTER",
            color="#3498DB", fontsize=10.5, ha="center", fontweight="bold")

    # ── Queue vertikal (kiri) ─────────────────────────────────────────────────
    q = list(state["queue"])
    for i, (name, color) in enumerate(q):
        y0 = CTOP - i * (CH + CGAP)
        ax.add_patch(mpatches.FancyBboxPatch(
            (CX, y0 - CH), CW, CH,
            boxstyle="round,pad=0.07", lw=2,
            edgecolor="white", facecolor=color, alpha=0.92))
        ax.text(CX + 0.22, y0 - CH/2,
                f"#{i+1}", fontsize=9, va="center", color="white", alpha=0.7)
        ax.text(CX + 0.50 + (CW - 0.50)/2, y0 - CH/2,
                name, fontsize=10, ha="center", va="center",
                color="white", fontweight="bold")

    if q:
        fy = CTOP - CH/2
        ry = CTOP - (len(q) - 1)*(CH + CGAP) - CH/2
        # Label FRONT / REAR (di kiri garis pemisah, cukup ruang)
        ax.text(SEP - 0.12, fy, "FRONT",
                color="#F39C12", fontsize=8, va="center",
                ha="right", fontweight="bold")
        ax.text(SEP - 0.12, ry, "REAR",
                color="#E74C3C", fontsize=8, va="center",
                ha="right", fontweight="bold")
    else:
        ax.text(CX + CW/2, CTOP - 1.6,
                "(antrian kosong)",
                fontsize=11, ha="center", color="#2A2A4A")

    # ── Printer box (kanan atas) ───────────────────────────────────────────────
    ax.add_patch(mpatches.FancyBboxPatch(
        (PX, PY), PW, PH,
        boxstyle="round,pad=0.10", lw=2.5,
        edgecolor="#5D6D7E", facecolor="#1C2833"))
    ax.text(PX + PW/2, PY + PH - 0.40,
            "[ PRINTER ]",
            fontsize=12, ha="center", va="center",
            color="#5D6D7E", fontweight="bold")

    if state["printing"]:
        nm, col = state["printing"]
        # Kartu dokumen yang sedang dicetak
        ax.add_patch(mpatches.FancyBboxPatch(
            (PX + 0.80, PY + 1.20), PW - 1.60, 0.80,
            boxstyle="round,pad=0.06", lw=2.5,
            edgecolor="white", facecolor=col, alpha=0.95))
        ax.text(PX + PW/2, PY + 1.60,
                nm,
                fontsize=12, ha="center", va="center",
                color="white", fontweight="bold")
        ax.text(PX + PW/2, PY + 0.55,
                ">>  Sedang mencetak ...",
                fontsize=13, ha="center", va="center",
                color="#F1C40F", fontweight="bold")
    else:
        ax.text(PX + PW/2, PY + 1.00,
                "--  Idle  --",
                fontsize=14, ha="center", va="center",
                color="#2A2A4A")

    # ── Garis pemisah horizontal bawah ────────────────────────────────────────
    ax.axhline(y=1.68, color="#2C3E50", lw=1.5, linestyle="--",
               xmin=0.29, xmax=0.99)

    # ── Sudah dicetak (kanan bawah) ───────────────────────────────────────────
    ax.text(PX + PW/2, 1.52,
            "SUDAH DICETAK :",
            color="#2ECC71", fontsize=9, ha="center", fontweight="bold")

    for j, (nm, col) in enumerate(state["printed"]):
        dx = DONE_X0 + j * (DONE_W + 0.18)
        ax.add_patch(mpatches.FancyBboxPatch(
            (dx, DONE_Y), DONE_W, DONE_H,
            boxstyle="round,pad=0.05", lw=1.5,
            edgecolor="#2ECC71", facecolor=col, alpha=0.55))
        ax.text(dx + 0.18, DONE_Y + DONE_H/2,
                "OK", fontsize=8, va="center",
                color="#2ECC71", fontweight="bold")
        ax.text(dx + 0.32 + (DONE_W - 0.32)/2, DONE_Y + DONE_H/2,
                nm, fontsize=8, ha="center", va="center",
                color="white", fontweight="bold")
    if not state["printed"]:
        ax.text(PX + PW/2, DONE_Y + DONE_H/2,
                "(belum ada)",
                fontsize=9, ha="center", color="#2A2A4A")

    # ── Info bar (kiri bawah, di bawah antrian) ────────────────────────────────
    info = (f"Antrian : {len(state['queue'])} dok    "
            f"|    Printer : {'SIBUK' if state['printing'] else 'idle'}    "
            f"|    Selesai : {len(state['printed'])} dok")
    ax.text(CX + CW/2, INFO_Y, info,
            fontsize=8.5, ha="center", va="center", color="#BDC3C7",
            bbox=dict(boxstyle="round,pad=0.28",
                      facecolor="#0D1117", edgecolor="#2C3E50"))

    # ── Pesan operasi (atas tengah kanan) ─────────────────────────────────────
    if state["done"]:
        msg, mc = "Semua dokumen selesai dicetak!", "#2ECC71"
    elif action == "enqueue" and doc:
        msg, mc = f"enqueue( '{doc[0]}' )  -->  masuk ke REAR antrian", "#3498DB"
    elif action == "start_print" and state["printing"]:
        msg, mc = f"dequeue()  -->  printer mulai cetak  '{state['printing'][0]}'", "#F39C12"
    elif action == "finish_print":
        msg, mc = "Dokumen selesai  —  printer siap untuk berikutnya", "#2ECC71"
    else:
        msg, mc = "", "white"

    if msg:
        ax.text(PX + PW/2, PY + PH + 0.32,
                msg,
                fontsize=10.5, ha="center", va="center",
                color=mc, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.28",
                          facecolor="#0D1117", edgecolor="#2C3E50"))

def update(frame):
    action, doc = steps[frame % len(steps)]
    if action == "enqueue" and doc:
        state["queue"].append(doc)
    elif action == "start_print":
        if state["queue"]:
            state["printing"] = state["queue"].popleft()
    elif action == "finish_print":
        if state["printing"]:
            state["printed"].append(state["printing"])
            state["printing"] = None
    elif action == "done":
        state["done"] = True
    draw(action, doc)

ani = animation.FuncAnimation(
    fig, update, frames=len(steps),
    interval=1400, repeat=True, repeat_delay=3000)

try:
    mng = plt.get_current_fig_manager()
    mng.resize(int(W_IN*DPI), int(H_IN*DPI))
    mng.window.resizable(False, False)
except Exception:
    pass

plt.tight_layout(pad=0.4)
plt.show()
