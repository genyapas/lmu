import numpy as np
import matplotlib.pyplot as plt

# Konstanten (in SI-Einheiten)
E_d = 11.16 * 1.602e-19   # J
hbar = 1.05457e-34        # J s
omega_s = 4.096e14         # s^-1
ks = 1910                  # N/m
Re = 1.13e-10              # m
a = np.sqrt(ks / (2 * E_d))  # m^-1

# Energie des harmonischen Oszillators in eV
hbar_omega_ev = hbar * omega_s / 1.602e-19  # ~0.269 eV

# Potentiale (in eV)
R = np.linspace(0.5 * Re, 3.5 * Re, 500)
x = R - Re

V_harm = 0.5 * ks * x**2 / 1.602e-19
V_morse = E_d * (np.exp(-2 * a * x) - 2 * np.exp(-a * x)) / 1.602e-19

# Energieniveaus (in eV) für nu = 0, 10, 25, 40
nu_werte = [0, 10, 25, 40]
E_harm = []
E_morse = []

for nu in nu_werte:
    E_harm.append(hbar_omega_ev * (nu + 0.5) - E_d / 1.602e-19)
    E_morse.append(hbar_omega_ev * (nu + 0.5) - (hbar_omega_ev**2 / (4 * E_d / 1.602e-19)) * (nu + 0.5)**2 - E_d / 1.602e-19)

# Plot
plt.figure(figsize=(10, 7))
plt.plot(R / Re, V_harm, 'b-', label='Harmonisch')
plt.plot(R / Re, V_morse, 'r-', label='Morse')

# Energielevel für harmonisch
for i, nu in enumerate(nu_werte):
    plt.axhline(y=E_harm[i], color='blue', linestyle=':', alpha=0.5)
    plt.text(0.55, E_harm[i] + 0.1, f'ν={nu}', color='blue')

# Energielevel für Morse
for i, nu in enumerate(nu_werte):
    plt.axhline(y=E_morse[i], color='red', linestyle=':', alpha=0.5)
    plt.text(1.1, E_morse[i] + 0.1, f'ν={nu}', color='red')

plt.axhline(y=0, color='black', linestyle='--', label='Dissoziationsgrenze')
plt.xlabel(r'$R / R_e$')
plt.ylabel('Energie / eV')
plt.xlim(0.5, 3.5)
plt.ylim(-12, 5)
plt.legend()
plt.grid(alpha=0.3)
plt.title('Vergleich: Harmonisches vs. Morse-Potential für CO')
plt.show()