import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Setup ---
L = 1.0       # Länge der Saite (z.B. 1m)
y0 = 0.1      # Maximale Amplitude
n_modes = [1, 3, 5]
amplitudes = [y0/1, -y0/9, y0/25]
k = [(n * np.pi / L) for n in n_modes]
omega = [n * 1.0 for n in n_modes] # Wir setzen omega_1 = 1.0 für die Animation

# --- Die Funktion y(x,t) ---
def y_string(x, t):
    y = np.zeros_like(x)
    for i in range(len(n_modes)):
        y += amplitudes[i] * np.sin(k[i] * x) * np.cos(omega[i] * t)
    return y

# --- Plot-Vorbereitung ---
x = np.linspace(0, L, 200)
fig, ax = plt.subplots()
line, = ax.plot(x, y_string(x, 0.0), 'r-', lw=2) # Startlinie bei t=0
ax.set_ylim(-y0*1.2, y0*1.2)
ax.set_xlim(0, L)
ax.set_title("Schwingende Saite (Moden n=1, 3, 5)")
ax.set_xlabel("x (Position)")
ax.set_ylabel("y (Auslenkung)")
ax.grid(True)
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# --- Animationsfunktion ---
# Diese Funktion wird für jeden Frame aufgerufen
def animate(t):
    line.set_ydata(y_string(x, t))
    time_text.set_text(f't = {t/(2*np.pi):.2f} T_1')
    return line, time_text

# --- Animation erstellen ---
# Wir animieren über eine Periode (T_1 = 2*pi/omega_1 = 2*pi)
ani = FuncAnimation(fig, animate, frames=np.linspace(0, 2*np.pi, 100),
                    interval=50, blit=True)

plt.show()

