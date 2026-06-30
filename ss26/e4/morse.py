import numpy as np
import matplotlib.pyplot as plt

# ---- Konstanten ----
E_d_ev = 11.16                     # Dissoziationsenergie in eV
E_d = E_d_ev * 1.602e-19           # in Joule
hbar = 1.05457e-34                 # J s
omega_s = 4.096e14                 # s^-1 (aus Aufgabe 32a)
ks = 1910                          # N/m (aus Aufgabe 32a)
Re = 1.13e-10                      # m
a = np.sqrt(ks / (2 * E_d))        # m^-1

# ---- Energien in eV ----
hbar_omega_ev = hbar * omega_s / 1.602e-19   # ~0.269 eV

# ---- Potentiale (eV) ----
R = np.linspace(0.5 * Re, 3.5 * Re, 1000)
x = R - Re

# BEIDE Potentiale haben Nullpunkt bei R->inf (Dissoziationsgrenze)
V_harm = 0.5 * ks * x**2 / 1.602e-19 - E_d_ev
V_morse = E_d * (np.exp(-2 * a * x) - 2 * np.exp(-a * x)) / 1.602e-19

# ---- Energielevel (eV) ----
nu_werte = [0, 10, 25, 40]

# Harmonisch: Nullpunkt bei Dissoziationsgrenze
E_harm = [hbar_omega_ev * (nu + 0.5) - E_d_ev for nu in nu_werte]

# Morse: Nullpunkt bei Dissoziationsgrenze
E_morse = [
    hbar_omega_ev * (nu + 0.5) - (hbar_omega_ev**2 / (4 * E_d_ev)) * (nu + 0.5)**2 - E_d_ev
    for nu in nu_werte
]

# ---- Plot ----
plt.figure(figsize=(10, 7))

# Potentiale
plt.plot(R / Re, V_harm, 'b-', label='Harmonisch', linewidth=2)
plt.plot(R / Re, V_morse, 'r-', label='Morse', linewidth=2)

# Dissoziationsgrenze
plt.axhline(y=0, color='black', linestyle='--', linewidth=1.5, label='Dissoziation')

# Energielevel
colors_h = ['blue'] * len(nu_werte)
colors_m = ['red'] * len(nu_werte)

for i, nu in enumerate(nu_werte):
    # Harmonische Level
    plt.axhline(y=E_harm[i], color='blue', linestyle=':', alpha=0.7)
    plt.text(0.6, E_harm[i] + 0.1, f'ν={nu}', color='blue', fontsize=10)
    
    # Morse-Level
    plt.axhline(y=E_morse[i], color='red', linestyle=':', alpha=0.7)
    plt.text(1.1, E_morse[i] + 0.1, f'ν={nu}', color='red', fontsize=10)

# Achsen
plt.xlabel(r'$R / R_e$', fontsize=12)
plt.ylabel('Energie / eV', fontsize=12)
plt.xlim(0.5, 3.5)
plt.ylim(-12, 5)
plt.legend(loc='upper right')
plt.grid(alpha=0.3)
plt.title('Harmonisches vs. Morse-Potential für CO', fontsize=12)

plt.tight_layout()
plt.show()