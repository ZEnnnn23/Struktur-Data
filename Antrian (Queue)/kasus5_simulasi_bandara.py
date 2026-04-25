"""
Kasus 5: Simulasi Loket Tiket Bandara
Ukuran window FIXED 1280x720 px - tidak bisa di-resize
"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np
from collections import deque

DPI = 100
W_IN, H_IN = 12.80, 7.20

SEED=42; NUM_MINUTES=20; NUM_AGENTS=2; SERVICE_TIME=3; BETWEEN_TIME=2
rng = np.random.default_rng(SEED)

class Agent:
    def __init__(self,i): self.idx=i;self.busy=False;self.finish_at=0;self.passenger=None

def run_sim():
    queue=deque(); agents=[Agent(i) for i in range(NUM_AGENTS)]
    total_wait=0; num_served=0; snaps=[]; pid=[0]
    for t in range(NUM_MINUTES+1):
        events=[]
        if rng.random() < 1/BETWEEN_TIME:
            p=pid[0]; pid[0]+=1; queue.append((p,t))
            events.append(f"t={t}: Penumpang P{p} tiba  ->  enqueue()")
        for ag in agents:
            if ag.busy and t>=ag.finish_at:
                events.append(f"t={t}: Agen {ag.idx+1} selesai layani P{ag.passenger[0]}")
                ag.busy=False; ag.passenger=None
        for ag in agents:
            if not ag.busy and queue:
                p,arrive=queue.popleft(); wait=t-arrive
                total_wait+=wait; num_served+=1
                ag.busy=True; ag.finish_at=t+SERVICE_TIME; ag.passenger=(p,arrive)
                events.append(f"t={t}: Agen {ag.idx+1} layani P{p}  (tunggu {wait} mnt)")
        avg=total_wait/num_served if num_served else 0
        snaps.append({"t":t,"queue":list(queue),
                      "agents":[(ag.busy,ag.passenger,ag.finish_at) for ag in agents],
                      "served":num_served,"avg":avg,"events":events})
    return snaps

snaps = run_sim()

fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_facecolor("#12131F")
ax.set_facecolor("#12131F")
ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis("off")

def on_resize(event):
    fig.set_size_inches(W_IN, H_IN, forward=False)
fig.canvas.mpl_connect("resize_event", on_resize)

AGENT_COLS = ["#E74C3C", "#3498DB"]

# Layout konstanta (dalam inci)
# Kolom kiri: antrian (0 - 3.0)
# Kolom tengah: agen (3.2 - 8.6)
# Kolom kanan: statistik (8.8 - 12.5)
SEP1, SEP2 = 3.10, 8.70

CX, CW = 0.22, 2.70
CH, CGAP = 0.58, 0.12
CTOP = H_IN - 1.10
MAX_SHOW = 8

AX_START = 3.30
AW = 2.50; AH = 1.80
A_TOP = H_IN - 1.10

SX = 8.90; SW = 3.60

DONE_Y = 0.26; DONE_H = 0.55; DONE_W = 1.55
DONE_AREA_X = 3.30

def update(frame):
    ax.clear(); ax.set_facecolor("#12131F")
    ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis("off")
    fig.patch.set_facecolor("#12131F")

    snap=snaps[frame % len(snaps)]
    t=snap["t"]; q=snap["queue"]; ags=snap["agents"]
    served=snap["served"]; avg=snap["avg"]; events=snap["events"]

    ax.set_title(f"Kasus 5 : Simulasi Loket Tiket Bandara   |   Tick  t = {t}  menit",
                 color="white", fontsize=13, fontweight="bold", pad=8)

    # Garis pemisah
    for sx in [SEP1, SEP2]:
        ax.axvline(x=sx, color="#2C3E50", lw=2, linestyle="--",
                   ymin=0.02, ymax=0.96)

    # Header
    ax.text(CX+CW/2,       H_IN-0.50, "ANTRIAN\nPENUMPANG",
            color="#F39C12", fontsize=9.5, ha="center", fontweight="bold", linespacing=1.2)
    ax.text(AX_START+AW+0.10, H_IN-0.50, "LOKET  TIKET",
            color="#3498DB", fontsize=9.5, ha="center", fontweight="bold")
    ax.text(SX+SW/2,       H_IN-0.50, "STATISTIK",
            color="#BDC3C7", fontsize=9.5, ha="center", fontweight="bold")

    # ── Antrian (vertikal kiri) ───────────────────────────────────────────────
    show_q = q[:MAX_SHOW]
    for i,(pid2,arrive) in enumerate(show_q):
        y0 = CTOP - i*(CH+CGAP)
        ax.add_patch(mpatches.FancyBboxPatch(
            (CX, y0-CH), CW, CH,
            boxstyle="round,pad=0.06", lw=2,
            edgecolor="white", facecolor="#F39C12", alpha=0.85))
        ax.text(CX+0.20, y0-CH/2,
                f"P{pid2}", fontsize=10, va="center",
                color="white", fontweight="bold")
        ax.text(CX+0.20+1.20, y0-CH/2,
                f"t={arrive}", fontsize=8.5, va="center", color="#1A1A2E")
    if show_q:
        fy=CTOP-CH/2; ry=CTOP-(len(show_q)-1)*(CH+CGAP)-CH/2
        ax.text(CX+CW+0.08, fy, "FRONT", color="#F39C12",
                fontsize=7.5, va="center", fontweight="bold")
        ax.text(CX+CW+0.08, ry, "REAR",  color="#E74C3C",
                fontsize=7.5, va="center", fontweight="bold")
    elif not q:
        ax.text(CX+CW/2, CTOP-1.5, "( kosong )", fontsize=10,
                ha="center", color="#2A2A4A")
    if len(q) > MAX_SHOW:
        ax.text(CX+CW/2, CTOP-MAX_SHOW*(CH+CGAP)-0.25,
                f"+ {len(q)-MAX_SHOW} lagi...", fontsize=8,
                ha="center", color="#BDC3C7")

    # ── Agen tiket (tengah, vertikal) ─────────────────────────────────────────
    for i,(busy,passenger,finish_at) in enumerate(ags):
        ay0 = A_TOP - i*(AH+0.30)
        col = AGENT_COLS[i] if busy else "#1C2833"
        ec  = "white" if busy else "#5D6D7E"
        lw  = 2.5 if busy else 1.5
        ax.add_patch(mpatches.FancyBboxPatch(
            (AX_START, ay0-AH), AW, AH,
            boxstyle="round,pad=0.08", lw=lw,
            edgecolor=ec, facecolor=col, alpha=0.9))
        ax.text(AX_START+AW/2, ay0-0.28, f"AGEN  {i+1}",
                fontsize=11, ha="center", va="center",
                color="white", fontweight="bold")
        if busy and passenger:
            pid2,arrive2=passenger; rem=max(0,finish_at-t)
            ax.text(AX_START+AW/2, ay0-0.80, f"Pasien : P{pid2}",
                    fontsize=10, ha="center", va="center", color="white")
            ax.text(AX_START+AW/2, ay0-1.30, f"Sisa : {rem} menit",
                    fontsize=10, ha="center", va="center", color="#F1C40F")
        else:
            ax.text(AX_START+AW/2, ay0-0.80, "-- Bebas --",
                    fontsize=11, ha="center", va="center", color="#2A2A4A")

    # ── Statistik (kanan) ─────────────────────────────────────────────────────
    stats = [
        (f"Menit ke     :  {t} / {NUM_MINUTES}", "#ECF0F1"),
        (f"Antrian      :  {len(q)} orang",      "#F39C12"),
        (f"Dilayani     :  {served} orang",       "#2ECC71"),
        (f"Avg. tunggu  :  {avg:.2f} menit",      "#3498DB"),
        (f"Jml. agen    :  {NUM_AGENTS}",         "#BDC3C7"),
        (f"Waktu layanan:  {SERVICE_TIME} mnt",   "#BDC3C7"),
    ]
    for si,(label,col) in enumerate(stats):
        sy = H_IN-0.95 - si*0.72
        ax.add_patch(mpatches.FancyBboxPatch(
            (SX, sy-0.26), SW, 0.52,
            boxstyle="round,pad=0.05", lw=1.2,
            edgecolor="#2C3E50", facecolor="#1C2833"))
        ax.text(SX+0.18, sy, label, fontsize=9, va="center",
                color=col, fontweight="bold")

    # Progress bar
    ax.axhline(y=1.80, color="#2C3E50", lw=1.2, linestyle="--",
               xmin=0.02, xmax=0.98)
    pct = t/NUM_MINUTES
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.22, 1.55), W_IN-0.44, 0.24,
        boxstyle="round,pad=0.03", lw=1,
        edgecolor="#2C3E50", facecolor="#1C2833"))
    if pct > 0:
        ax.add_patch(mpatches.FancyBboxPatch(
            (0.22, 1.55), (W_IN-0.44)*pct, 0.24,
            boxstyle="round,pad=0.03", lw=0,
            edgecolor="none", facecolor="#3498DB"))
    ax.text(W_IN/2, 1.67, f"Waktu : {t} / {NUM_MINUTES} menit",
            fontsize=8.5, ha="center", va="center", color="white")

    # Event log
    ax.text(0.25, 1.38, "Event tick ini :", fontsize=8.5, color="#BDC3C7")
    for ei, ev in enumerate(events[:3]):
        ax.text(0.35, 1.10-ei*0.42, f"- {ev}", fontsize=8, color="#ECF0F1")
    if not events:
        ax.text(0.35, 1.10, "- (tidak ada event)", fontsize=8, color="#2A2A4A")

    if t == NUM_MINUTES:
        final = f"SELESAI!   Avg. tunggu: {avg:.2f} mnt   |   Dilayani: {served} penumpang"
        ax.text(W_IN/2, 0.22, final, fontsize=10.5, ha="center", va="center",
                color="#FFD700", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.32",
                          facecolor="#0D1117", edgecolor="#F39C12"))

ani = animation.FuncAnimation(fig, update, frames=len(snaps),
                               interval=1100, repeat=True, repeat_delay=3000)
try:
    mng = plt.get_current_fig_manager()
    mng.resize(int(W_IN*DPI), int(H_IN*DPI))
    mng.window.resizable(False, False)
except Exception:
    pass

plt.tight_layout(pad=0.5)
plt.show()
