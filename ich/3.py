import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parameter ---
c = 1.0            # Lichtgeschwindigkeit
v = 0.4            # Konstante Geschwindigkeit ab t=0
num_lines = 24     # Anzahl Feldlinien
line_length = 12.0 # Gesamtlänge der Linien
num_frames = 200
interval = 100     # Langsame Animation (ms)

# --- Figure Setup ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-5, 8)
ax.set_ylim(-6.5, 6.5)
ax.set_aspect('equal')
ax.set_title("Konstante Bewegung ab t=0: Feldlinien wandern starr mit")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle="--", alpha=0.3)

# Elemente
particle, = ax.plot([], [], 'ro', ms=10, zorder=4, label="Geladene Masse")
front = plt.Circle((0, 0), 0, color='r', fill=False, linestyle='--', alpha=0.7, label="Ausbreitungsfront (c·t)")
ax.add_patch(front)

angles = np.linspace(0, 2 * np.pi, num_lines, endpoint=False)
lines = [ax.plot([], [], 'b-', lw=1.3, alpha=0.8)[0] for _ in range(num_lines)]

ax.legend(loc='upper left')

def init():
    particle.set_data([], [])
    front.set_radius(0)
    for line in lines:
        line.set_data([], [])
    return [particle, front] + lines

def update(frame):
    t = frame * 0.08
    
    # 1. Momentane Position des Teilchens
    x_q = v * t if t > 0 else 0.0
    particle.set_data([x_q], [0])
    
    # 2. Radius der Signalausbreitung vom Startpunkt (0,0)
    R_front = c * t if t > 0 else 0.0
    front.set_radius(R_front)
    
    # 3. Feldlinienkonstruktion
    for i, theta in enumerate(angles):
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        
        if R_front == 0:
            # Zustand vor der Bewegung (statisch)
            x_pts = [0, line_length * cos_t]
            y_pts = [0, line_length * sin_t]
        else:
            # Punkt auf der Wellenfront R = c*t (wo das alte Feld verankert ist)
            P_kink = np.array([R_front * cos_t, R_front * sin_t])
            
            # Punkt weit außerhalb (verläuft radial vom Ursprung)
            P_far = np.array([line_length * cos_t, line_length * sin_t])
            
            # Inneres Segment: Verbindet die AKTUELLE Position x_q geradlinig mit dem Knick
            x_pts = [x_q, P_kink[0], P_far[0]]
            y_pts = [0, P_kink[1], P_far[1]]

        lines[i].set_data(x_pts, y_pts)
        
    return [particle, front] + lines

ani = FuncAnimation(
    fig, update, frames=num_frames, init_func=init,
    interval=interval, blit=True, repeat=True
)

plt.show()