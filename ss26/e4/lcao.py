import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# Konstanten in SI (umgerechnet in eV für die Darstellung)
K = 27.2114          # eV  ( = e^2 / (4*pi*eps0*a0) )
E0 = -K/2            # -13.6057 eV

def S(x):
    """Überlappintegral S(R) = <phi_A|phi_B>"""
    return (1 + x + x**2/3) * np.exp(-x)

def E_s(x):
    """Energie des bindenden Zustands (symmetrisch) in eV"""
    Sx = S(x)
    term1 = -K/2 + (K/x) * (1 + x) * np.exp(-2*x)
    term2 = (-K/2 + K/x) * Sx - K * (1 + x) * np.exp(-x)
    return (term1 + term2) / (1 + Sx)

def E_a(x):
    """Energie des antibindenden Zustands (antisymmetrisch) in eV"""
    Sx = S(x)
    term1 = -K/2 + (K/x) * (1 + x) * np.exp(-2*x)
    term2 = (-K/2 + K/x) * Sx - K * (1 + x) * np.exp(-x)
    return (term1 - term2) / (1 - Sx)

# 1. Potentialkurven plotten (x von 0.2 bis 10)
x_werte = np.linspace(0.2, 10, 500)
Es = E_s(x_werte)
Ea = E_a(x_werte)

plt.figure(figsize=(9,6))
plt.plot(x_werte, Es, label=r'$\Phi_s$', linewidth=2)
plt.plot(x_werte, Ea, label=r'$\Phi_a$', linewidth=2)
plt.axhline(E0, color='k', linestyle='--', label=r'$E_0')
plt.xlabel(r'$x = R / a_0$', fontsize=12)
plt.ylabel('Energie / eV', fontsize=12)
plt.legend()
plt.grid(alpha=0.3)
plt.title('LCAO‑Potentialkurven des H$_2^+$')
plt.xlim(0.2, 8)
plt.ylim(-16, 5)
plt.show()

# 2. Numerische Minimierung von E_s(x)
# Zuerst grobe Suche im Bereich x in [1, 5] (das Minimum liegt dort)
res = minimize_scalar(E_s, bounds=(1.0, 5.0), method='bounded')
x_b = res.x
E_min = res.fun

# Bindungsenergie (negativ, da gebunden)
E_bind = E_min - E0

# Umrechnung auf SI-Längen
a0 = 5.29177e-11       # m
R_b = x_b * a0

print(f"Gleichgewichtsabstand x_b = {x_b:.4f}")
print(f"Gleichgewichtsabstand R_b = {R_b:.3e} m  ({R_b*1e10:.3f} Å)")
print(f"Energie am Minimum E_s(R_b) = {E_min:.4f} eV")
print(f"Bindungsenergie (gegenüber H-Atom) E_b = {E_bind:.4f} eV")
print(f"Vergleich: exakter Wert (aus Skript) R_b = 2.00 a0,  E_b = -2.79 eV")