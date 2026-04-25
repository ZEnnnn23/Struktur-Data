"""
Kasus 2: Permainan Hot Potato
Ukuran window FIXED 900x900 px - tidak bisa di-resize
"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np
from collections import deque

DPI = 100
W_IN, H_IN = 9.0, 9.0   # 900x900 px

NAMES  = ["Andi", "Budi", "Citra", "Dedi", "Eka", "Fajar"]
COLORS = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"]
NUM_PASS = 3

def build_steps(names, num_pass):
    q = deque(range(len(names)))
    steps, elim = [], []
    steps.append({"queue": list(q), "holder": q[0], "elim": list(elim),
                  "msg": "MULAI!  Semua pemain masuk antrian", "phase": "start"})
    while len(q) > 1:
        for i in range(num_pass):
            front = q[0]
            steps.append({"queue": list(q), "holder": front, "elim": list(elim),
                          "msg": f"Oper ke-{i+1} : {names[front]} mengoper bola",
                          "phase": "pass"})
            q.rotate(-1)
        out = q.popleft(); elim.append(out)
        steps.append({"queue": list(q), "holder": None, "elim": list(elim),
                      "msg": f"TERSINGKIR : {names[out]}!", "phase": "eliminate"})
    winner = q[0]
    steps.append({"queue": [winner], "holder": winner, "elim": elim,
                  "msg": f"*** PEMENANG : {names[winner]} ***", "phase": "win"})
    return steps

steps = build_steps(NAMES, NUM_PASS)

fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_facecolor("#12131F")
ax.set_facecolor("#12131F")
ax.set_aspect("equal")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.5, 2.6); ax.axis("off")

def on_resize(event):
    fig.set_size_inches(W_IN, H_IN, forward=False)
fig.canvas.mpl_connect("resize_event", on_resize)

def player_pos(idx, n, r=1.30):
    angle = np.pi/2 + 2*np.pi*idx/n
    return r*np.cos(angle), r*np.sin(angle)

def update(frame):
    ax.clear()
    ax.set_facecolor("#12131F")
    ax.set_aspect("equal")
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.5, 2.6); ax.axis("off")
    fig.patch.set_facecolor("#12131F")

    step   = steps[frame % len(steps)]
    q_now  = step["queue"]
    elim   = step["elim"]
    holder = step["holder"]
    msg    = step["msg"]
    phase  = step["phase"]
    n      = len(NAMES)

    for i in range(n):
        x1, y1 = player_pos(i, n)
        x2, y2 = player_pos((i+1)%n, n)
        ax.plot([x1,x2],[y1,y2], color="#2C3E50", lw=1.5, zorder=0)

    for idx in range(n):
        x, y  = player_pos(idx, n)
        is_el = idx in elim
        is_h  = idx == holder
        alpha = 0.20 if is_el else 1.0
        ec    = "#FFD700" if is_h else ("white" if not is_el else "#444444")
        lw    = 5 if is_h else 2

        c = plt.Circle((x, y), 0.26, color=COLORS[idx], alpha=alpha,
                        linewidth=lw, edgecolor=ec, zorder=2)
        ax.add_patch(c)
        ax.text(x, y, "X" if is_el else NAMES[idx][0],
                fontsize=14, ha="center", va="center",
                color="white", fontweight="bold", zorder=3, alpha=alpha)
        ax.text(x, y - 0.43, NAMES[idx], fontsize=9.5, ha="center", va="center",
                color="#BDC3C7" if not is_el else "#E74C3C",
                alpha=alpha, zorder=3)

    if holder is not None and phase not in ("eliminate",):
        hx, hy = player_pos(holder, n)
        ball = plt.Circle((hx, hy + 0.62), 0.15, color="#F1C40F",
                           linewidth=2, edgecolor="white", zorder=4)
        ax.add_patch(ball)
        ax.text(hx, hy + 0.62, "o", fontsize=8, ha="center", va="center",
                color="#1A1A2E", fontweight="bold", zorder=5)

    # Urutan antrian
    ax.text(0, -1.82, "Urutan antrian :", fontsize=9.5, ha="center", color="#BDC3C7")
    q_str = " -> ".join([NAMES[i] for i in q_now])
    ax.text(0, -2.10, q_str, fontsize=9, ha="center", color="#F1C40F",
            bbox=dict(boxstyle="round,pad=0.22",
                      facecolor="#1A1A2E", edgecolor="#2C3E50"))

    ax.set_title(f"Kasus 2 : Permainan Hot Potato   (oper {NUM_PASS}x  ->  tersingkir)",
                 color="white", fontsize=12, fontweight="bold", pad=8)

    pc = {"start":"#3498DB","pass":"#F39C12","eliminate":"#E74C3C","win":"#2ECC71"}
    ax.text(0, 2.28, msg, fontsize=12, ha="center", va="center",
            color=pc.get(phase, "white"), fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.30",
                      facecolor="#1A1A2E", edgecolor="#2C3E50"))

ani = animation.FuncAnimation(fig, update, frames=len(steps),
                               interval=1000, repeat=True, repeat_delay=2000)
try:
    mng = plt.get_current_fig_manager()
    mng.resize(int(W_IN*DPI), int(H_IN*DPI))
    mng.window.resizable(False, False)
except Exception:
    pass

plt.tight_layout()
plt.show()
