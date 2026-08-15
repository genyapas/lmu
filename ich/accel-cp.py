import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Physikalische Parameter ---
c = 1.0            # Lichtgeschwindigkeit (Simulationseinheiten)
v = 0.5            # Endgeschwindigkeit nach Beschleunigung (v < c)
dt_acc = 0.4       # Dauer der Beschleunigung
num_lines = 24     # Anzahl der Feldlinien
line_length = 12.0 # Maximale Ausbreitungslänge
num_frames = 200
interval = 90      # Langsame Animation (ms pro Frame)

# --- Figure Setup ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-6, 8)
ax.set_ylim(-7, 7)
ax.set_aspect('equal')
ax.set_title("Feldlinien einer beschleunigten Ladung (Strahlungsknick)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle="--", alpha=0.3)

# Visualisierungselemente
particle, = ax.plot([], [], 'ro', ms=10, zorder=4, label="Geladenes Teilchen")
wave_front = plt.Circle((0, 0), 0, color='r', fill=False, linestyle=':', alpha=0.6, label="Strahlungsfront (c·t)")
ax.add_patch(wave_front)

angles = np.linspace(0, 2 * np.pi, num_lines, endpoint=False)
lines = [ax.plot([], [], 'b-', lw=1.3, alpha=0.8)[0] for _ in range(num_lines)]

ax.legend(loc='upper left')

def init():
    particle.set_data([], [])
    wave_front.set_radius(0)
    for line in lines:
        line.set_data([], [])
    return [particle, wave_front] + lines

def update(frame):
    t = frame * 0.08  # Zeitfortschritt
    
    # 1. Trajektorie des Teilchens (Ruhe für t <= 0, Kurze Beschleunigung, dann v = const)
    if t <= 0:
        x_q = 0.0
    elif t <= dt_acc:
        # Gleichmäßige Beschleunigung
        a = v / dt_acc
        x_q = 0.5 * a * t**2
    else:
        # Konstante Endgeschwindigkeit
        x_acc = 0.5 * v * dt_acc
        x_q = x_acc + v * (t - dt_acc)
        
    particle.set_data([x_q], [0])
    
    # 2. Ausbreitung der Wellenfronten (Radius der Lichtkugeln)
    R_outer = c * t
    R_inner = max(0.0, c * (t - dt_acc))
    wave_front.set_radius(R_outer)

    # 3. Feldlinienverlauf konstruieren
    for i, theta in enumerate(angles):
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        
        if R_outer == 0:
            # Vor Beginn der Bewegung
            x_pts = [0, line_length * cos_t]
            y_pts = [0, line_length * sin_t]
        elif t <= dt_acc:
            # Während der Beschleunigungsphase bildet sich der Knick direkt am Teilchen
            P_out = np.array([R_outer * cos_t, R_outer * sin_t])
            P_far = np.array([line_length * cos_t, line_length * sin_t])
            x_pts = [x_q, P_out[0], P_far[0]]
            y_pts = [0, P_out[1], P_far[1]]
        else:
            # Nach der Beschleunigung: Inneres Segment + Knickschale + Äußeres Segment
            # Innerer Punkt (relativ zur Position nach der Beschleunigung)
            x_acc = 0.5 * v * dt_acc
            P_in = np.array([x_acc + v * (t - dt_acc) + R_inner * cos_t, R_inner * sin_t])
            
            # Äußerer Punkt (relativ zum Ursprung t=0)
            P_out = np.array([R_outer * cos_t, R_outer * sin_t])
            
            # Fernfeld-Punkt
            P_far = np.array([line_length * cos_t, line_length * sin_t])
            
            x_pts = [x_q, P_in[0], P_out[0], P_far[0]]
            y_pts = [0, P_in[1], P_out[1], P_far[1]]

        lines[i].set_data(x_pts, y_pts)
        
    return [particle, wave_front] + lines

ani = FuncAnimation(
    fig, update, frames=num_frames, init_func=init,
    interval=interval, blit=True, repeat=True
)

plt.show()