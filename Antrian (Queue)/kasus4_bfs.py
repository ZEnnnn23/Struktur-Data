"""
Kasus 4: BFS (Breadth-First Search)
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

GRAPH = {
    "A":["B","C"],"B":["A","D","E"],"C":["A","F"],
    "D":["B"],    "E":["B","G"],    "F":["C","H"],
    "G":["E"],    "H":["F"],
}
# Posisi node dalam koordinat inci (ax_g xlim 0-8.5, ylim 0-7.2)
POS = {
    "A":(4.25,6.40),"B":(2.00,4.80),"C":(6.50,4.80),
    "D":(0.60,3.00),"E":(3.20,3.00),"F":(6.50,3.00),
    "G":(2.40,1.40),"H":(6.50,1.40),
}
LEVEL_COLOR = {0:"#E74C3C",1:"#F39C12",2:"#3498DB",3:"#9B59B6"}
START = "A"

def build_steps():
    vis,q,order,steps = {},deque(),[],[]
    q.append(START); vis[START]=0
    steps.append({"vis":dict(vis),"queue":list(q),"cur":None,"order":list(order),
                  "msg":f"BFS mulai dari '{START}'  ->  enqueue('{START}')","phase":"init"})
    while q:
        node=q.popleft(); order.append(node)
        steps.append({"vis":dict(vis),"queue":list(q),"cur":node,"order":list(order),
                      "msg":f"dequeue()  ->  proses '{node}'  (Level {vis[node]})","phase":"dequeue"})
        for nb in GRAPH[node]:
            if nb not in vis:
                vis[nb]=vis[node]+1; q.append(nb)
                steps.append({"vis":dict(vis),"queue":list(q),"cur":node,"order":list(order),
                              "msg":f"  enqueue('{nb}')  ->  Level {vis[nb]}","phase":"enqueue"})
    steps.append({"vis":dict(vis),"queue":[],"cur":None,"order":list(order),
                  "msg":f"BFS selesai!   Urutan: {' -> '.join(order)}","phase":"done"})
    return steps

steps = build_steps()

fig, (ax_g, ax_q) = plt.subplots(1, 2, figsize=(W_IN, H_IN), dpi=DPI,
                                   gridspec_kw={"width_ratios":[2,1]})
fig.patch.set_facecolor("#12131F")
for a in [ax_g, ax_q]:
    a.set_facecolor("#12131F"); a.axis("off")

def on_resize(event):
    fig.set_size_inches(W_IN, H_IN, forward=False)
fig.canvas.mpl_connect("resize_event", on_resize)

def draw_graph(ax, step):
    ax.clear(); ax.set_facecolor("#12131F")
    ax.set_xlim(-0.3, 8.5); ax.set_ylim(0, 7.2); ax.axis("off")
    ax.set_title("Graf", color="white", fontsize=12, fontweight="bold")
    vis=step["vis"]; cur=step["cur"]
    drawn=set()
    for node,nbs in GRAPH.items():
        for nb in nbs:
            key=tuple(sorted([node,nb]))
            if key not in drawn:
                x1,y1=POS[node]; x2,y2=POS[nb]
                c="#34495E" if not(node in vis and nb in vis) else "#5D6D7E"
                ax.plot([x1,x2],[y1,y2],color=c,lw=2,zorder=1)
                drawn.add(key)
    for node,(x,y) in POS.items():
        is_c=node==cur; is_v=node in vis
        if is_c:   col,ec,lw="#FFD700","#FFD700",4
        elif is_v: col,ec,lw=LEVEL_COLOR.get(vis[node],"#8E44AD"),"white",2
        else:      col,ec,lw="#1C2833","#5D6D7E",1.5
        ax.add_patch(plt.Circle((x,y),0.50,color=col,lw=lw,edgecolor=ec,zorder=2))
        ax.text(x,y,node,fontsize=14,ha="center",va="center",
                color="#1A1A2E" if is_c else "white",fontweight="bold",zorder=3)
        if is_v:
            lv=vis[node]
            ax.text(x+0.60,y+0.58,f"L{lv}",fontsize=8,
                    color=LEVEL_COLOR.get(lv,"white"),ha="center")
    # Legend
    for lv,col in LEVEL_COLOR.items():
        ax.add_patch(plt.Circle((0.35, 6.80-lv*0.55),0.18,color=col))
        ax.text(0.62, 6.80-lv*0.55,f"Level {lv}",fontsize=8.5,
                color="white",va="center")

def draw_panel(ax, step):
    ax.clear(); ax.set_facecolor("#12131F")
    ax.set_xlim(0,4.0); ax.set_ylim(0,7.2); ax.axis("off")
    ax.set_title("Queue  &  Urutan", color="white", fontsize=11, fontweight="bold")

    ax.text(2.0, 6.85, "Queue (front -> rear)", fontsize=9.5,
            ha="center", color="#BDC3C7")
    q_now=step["queue"]; vis=step["vis"]
    QCARD_H=0.58; QCARD_GAP=0.12; QTOP=6.55
    if q_now:
        for i,node in enumerate(q_now):
            y=QTOP - i*(QCARD_H+QCARD_GAP)
            lv=vis.get(node,0)
            col=LEVEL_COLOR.get(lv,"#8E44AD")
            ax.add_patch(mpatches.FancyBboxPatch(
                (0.35, y-QCARD_H), 3.30, QCARD_H,
                boxstyle="round,pad=0.05", lw=1.5,
                edgecolor="white", facecolor=col, alpha=0.85))
            ax.text(2.0, y-QCARD_H/2, f"{node}   (L{lv})",
                    fontsize=11, ha="center", va="center",
                    color="white", fontweight="bold")
        ax.text(0.50, QTOP-QCARD_H/2+0.32, "FRONT",
                fontsize=7.5, color="#F39C12", fontweight="bold")
        ax.text(0.50, QTOP-(len(q_now)-1)*(QCARD_H+QCARD_GAP)-QCARD_H/2-0.30,
                "REAR", fontsize=7.5, color="#E74C3C", fontweight="bold")
    else:
        ax.text(2.0, QTOP-0.8, "[ kosong ]", fontsize=10,
                ha="center", color="#2A2A4A")

    # Urutan kunjungan
    ax.axhline(y=3.80, color="#2C3E50", lw=1.2, linestyle="--",
               xmin=0.05, xmax=0.95)
    ax.text(2.0, 3.58, "Urutan Kunjungan :", fontsize=9.5,
            ha="center", color="#BDC3C7")

    order=step["order"]
    per_row=4; r=0.30; gap_x=0.82; gap_y=0.78
    start_x=0.55; start_y=3.25
    for j,node in enumerate(order):
        lv=vis.get(node,0); col=LEVEL_COLOR.get(lv,"#8E44AD")
        ox=start_x+(j%per_row)*gap_x; oy=start_y-(j//per_row)*gap_y
        ax.add_patch(plt.Circle((ox,oy),r,color=col,lw=1.5,edgecolor="white"))
        ax.text(ox,oy,node,fontsize=10,ha="center",va="center",
                color="white",fontweight="bold")
        if j>0 and (j-1)//per_row==j//per_row:
            px=start_x+((j-1)%per_row)*gap_x; py=start_y-((j-1)//per_row)*gap_y
            ax.annotate("",xy=(ox-r,oy),xytext=(px+r,py),
                        arrowprops=dict(arrowstyle="->",color="#5D6D7E",lw=1))

    pc={"init":"#3498DB","dequeue":"#FFD700","enqueue":"#F39C12","done":"#2ECC71"}
    ax.text(2.0,0.40,step["msg"],fontsize=7.5,ha="center",va="center",
            color=pc.get(step["phase"],"white"),
            bbox=dict(boxstyle="round,pad=0.25",facecolor="#0D1117",edgecolor="#2C3E50"))

def update(frame):
    step=steps[frame % len(steps)]
    draw_graph(ax_g, step)
    draw_panel(ax_q, step)
    fig.suptitle("Kasus 4 : BFS Traversal Graf  —  Queue menjamin Level demi Level",
                 color="white", fontsize=13, fontweight="bold", y=0.99)

ani = animation.FuncAnimation(fig, update, frames=len(steps),
                               interval=1400, repeat=True, repeat_delay=2500)
try:
    mng = plt.get_current_fig_manager()
    mng.resize(int(W_IN*DPI), int(H_IN*DPI))
    mng.window.resizable(False, False)
except Exception:
    pass

plt.tight_layout(pad=0.3)
plt.show()
