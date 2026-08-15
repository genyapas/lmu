import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parameter ---
v_x, v_y = 0.3, 0.15     # Geschwindigkeitsvektor (m/s)
q = 1.0                  # Ladung (+1: Feldlinien nach außen)
num_lines = 16           # Anzahl der Feldlinien
line_length = 6.0        # Länge der gezeichneten Feldlinien
num_frames = 200         # Frame-Anzahl
interval = 100           # Zeit pro Frame in ms (höher = langsamer)

# Startposition
x0, y0 = -4.0, -2.0

# --- Figuredesign ---
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect('equal')
ax.set_title("Geladene Masse bei konstanter Geschwindigkeit")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle="--", alpha=0.4)

# Visualisierungselemente
particle, = ax.plot([], [], 'ro', ms=12, zorder=3, label=f"Ladung q = {q}")
angles = np.linspace(0, 2 * np.pi, num_lines, endpoint=False)
lines = [ax.plot([], [], 'b-', lw=1.5, alpha=0.7)[0] for _ in range(num_lines)]

ax.legend(loc='upper right')

def init():
    particle.set_data([], [])
    for line in lines:
        line.set_data([], [])
    return [particle] + lines

def update(frame):
    t = frame * 0.1
    # Aktuelle Position r_q(t)
    x_q = x0 + v_x * t
    y_q = y0 + v_y * t
    
    particle.set_data([x_q], [y_q])
    
    # Feldlinien von der momentanen Position aus zeichnen
    for i, angle in enumerate(angles):
        x_end = x_q + line_length * np.cos(angle)
        y_end = y_q + line_length * np.sin(angle)
        lines[i].set_data([x_q, x_end], [y_q, y_end])
        
    return [particle] + lines

# Animation starten
ani = FuncAnimation(
    fig, update, frames=num_frames, init_func=init,
    interval=interval, blit=True, repeat=True
)

plt.show()