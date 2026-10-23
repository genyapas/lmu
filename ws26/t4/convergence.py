import numpy as np
import matplotlib.pyplot as plt

# Parameter setzen
N_max = 2000          # Maximale Anzahl an Schritten n
num_paths = 100       # Anzahl der zufälligen Pfade (Simulationen)
epsilon = 0.05        # Toleranzstreifen epsilon

# ---------------------------------------------------------------
# PROGRAMM 1: Fast sichere Konvergenz (1 einzelner Pfad)
# ---------------------------------------------------------------
# Wir simulieren Zufallsvariablen mit Mittelwert 0 (z.B. Gleichverteilung in [-1, 1])
np.random.seed(42)    # Für Reproduzierbarkeit
x_single = np.random.uniform(-1, 1, size=N_max)
n_array = np.arange(1, N_max + 1)

# Kumulativer Mittelwert X_n für n = 1 bis N_max
X_n_single = np.cumsum(x_single) / n_array

# Plot für Programm 1 (ähnlich Fig. 42.3 aus dem Buch)
plt.figure(figsize=(10, 4))
plt.plot(n_array, X_n_single, label=r'Stichprobenmittelwert $\bar{X}_n$', color='navy', lw=1)
plt.axhline(0, color='black', linestyle='--')
plt.axhspan(-epsilon, epsilon, color='gray', alpha=0.3, label=rf'Toleranzbereich $\pm\epsilon = {epsilon}$')
plt.xlabel('n (Stichprobengröße)')
plt.ylabel(r'$\bar{X}_n$')
plt.title('Fast sichere Konvergenz: Ein einzelner Pfad über n')
plt.ylim(-0.5, 0.5)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# ---------------------------------------------------------------
# PROGRAMM 2: Konvergenz in Wahrscheinlichkeit (100 Pfade & Ausreißer)
# ---------------------------------------------------------------
# Generiere 100 Pfade gleichzeitig (Matrix: 100 Zeilen, N_max Spalten)
X_all = np.random.uniform(-1, 1, size=(num_paths, N_max))
X_n_paths = np.cumsum(X_all, axis=1) / n_array  # Kumulativer Mittelwert pro Zeile

# Für jedes n bestimmen: Welcher Anteil der 100 Pfade ist ein Ausreißer (|X_n| > delta)?
delta = 0.05
# Abweichung > delta ergibt True (1) oder False (0), mean über die 100 Pfade gibt den Anteil
outlier_ratio = np.mean(np.abs(X_n_paths) > delta, axis=0)

# Plot für Programm 2
plt.figure(figsize=(10, 4))
plt.plot(n_array, outlier_ratio, color='crimson', lw=1.5, label=rf'Anteil Ausreißer ($|\bar{{X}}_n| > \delta={delta}$)')
plt.xlabel('n (Stichprobengröße)')
plt.ylabel('Anteil der Ausreißer-Pfade')
plt.title(f'Konvergenz in Wahrscheinlichkeit (Anteil von {num_paths} Pfaden außerhalb von $\pm\delta$)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()