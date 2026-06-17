import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# 1. Definition des DGL-Systems (Optische Blochgleichungen für delta = 0)
def bloch_equations(y, t, Omega0, gamma):
    u, v, w = y
    
    # Die Blochgleichungen laut Blatt (mit delta = 0)
    dudt = -0.5 * gamma * u
    dvdt = -0.5 * gamma * v + Omega0 * w
    dwdt = -Omega0 * v - gamma * (w + 1)
    
    return [dudt, dvdt, dwdt]

# 2. Parameter und Zeitgitter aufsetzen
Omega0 = 1.0  # Wir normieren die Zeit auf Omega0 (t ist in Einheiten von 1/Omega0)
t = np.linspace(0, 25, 1000) # Zeitintervall

# Anfangsbedingungen: Atom ist zu 100% im Grundzustand
# u=0, v=0, w=-1 (da rho_11 = 1 und rho_22 = 0)
y0 = [0.0, 0.0, -1.0]

# 3. Fall 1: Schwache Dämpfung (gamma = Omega0 / 4)
gamma_weak = Omega0 / 4.0
solution_weak = odeint(bloch_equations, y0, t, args=(Omega0, gamma_weak))
w_weak = solution_weak[:, 2]          # Wir extrahieren nur die w-Komponente
rho22_weak = (w_weak + 1.0) / 2.0     # Umrechnung in Besetzungswahrscheinlichkeit

# 4. Fall 2: Starke Dämpfung (gamma = 2 * Omega0)
gamma_strong = 2.0 * Omega0
solution_strong = odeint(bloch_equations, y0, t, args=(Omega0, gamma_strong))
w_strong = solution_strong[:, 2]
rho22_strong = (w_strong + 1.0) / 2.0

# 5. Plotten der Ergebnisse
plt.figure(figsize=(10, 6))

plt.plot(t, rho22_weak, label=r'$\gamma = \Omega_0 / 4$ (Schwach gedämpft)', color='blue', linewidth=2)
plt.plot(t, rho22_strong, label=r'$\gamma = 2\Omega_0$ (Stark gedämpft)', color='red', linewidth=2)

# Asymptotische Linien (Stationäre Zustände aus Aufgabenteil g) für den Theorie-Check
S0_weak = (2 * Omega0**2) / (gamma_weak**2)
S0_strong = (2 * Omega0**2) / (gamma_strong**2)
plt.axhline(( -1/(1+S0_weak) + 1 ) / 2, color='blue', linestyle='--', alpha=0.5)
plt.axhline(( -1/(1+S0_strong) + 1 ) / 2, color='red', linestyle='--', alpha=0.5)

# Plot-Styling
plt.title('Besetzung des angeregten Zustands $\\rho_{22}(t)$', fontsize=14)
plt.xlabel('Zeit $t$ (in Einheiten von $1/\Omega_0$)', fontsize=12)
plt.ylabel(r'Besetzungswahrscheinlichkeit $\rho_{22}$', fontsize=12)
plt.ylim(0, 1)
plt.xlim(0, max(t))
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

plt.tight_layout()
plt.show()