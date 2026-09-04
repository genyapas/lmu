import numpy as np
import matplotlib.pyplot as plt
from scipy import odr

# --- 1. Daten aus den vorherigen Schritten ---
# Magnetfelder B in Tesla
B = np.array([0.39225, 0.45637, 0.51908, 0.59366, 0.65647])
B_err = np.array([0.01025, 0.01152, 0.01259, 0.01411, 0.01524])

# Halbe Wellenzahldifferenzen Delta k / 2 in 1/m (aktualisiert)
halbes_dk = np.array([20.42, 24.59, 27.49, 30.52, 31.94])
halbes_dk_err = np.array([0.85, 0.87, 0.88, 0.91, 0.92])  # Fehler in 1/m

# Proportionalitätsfaktor aus Gl. (21)[cite: 1]
faktor = 46.686  # in m^-1 T^-1[cite: 1]

# --- 2. ODR Ursprungsgeraden-Fit: y = beta[0] * x ---
def ursprung(beta, x):
    return beta[0] * x

model = odr.Model(ursprung)
data = odr.RealData(x=B, y=halbes_dk, sx=B_err, sy=halbes_dk_err)
odr_run = odr.ODR(data, model, beta0=[46.0]).run()

# Steigung und Fehler
steigung = odr_run.beta[0]
steigung_err = odr_run.sd_beta[0]

# Berechnung von g_{1->2}[cite: 1]
g_1_2 = steigung / faktor
g_1_2_err = steigung_err / faktor

print(f"Gefittete Steigung S: ({steigung:.3f} ± {steigung_err:.3f}) m^-1 T^-1")
print(f"Abstandsfaktor g_1->2: {g_1_2:.4f} ± {g_1_2_err:.4f}")
print(f"Theoriewert: 1.0000")
print(f"Abweichung: {abs(g_1_2 - 1.0) / 1.0 * 100:.2f} %")

# Plot
plt.figure(figsize=(8, 6))

# Messpunkte mit x- und y-Fehlerbalken
plt.errorbar(B, halbes_dk, xerr=B_err, yerr=halbes_dk_err, 
             fmt='o', color='black', ecolor='darkblue', elinewidth=1.2,
             capsize=4, label=r'Messwerte $(\Delta k/2)$ mit Unsicherheiten')

# Fit-Gerade
B_plot = np.linspace(0, max(B) * 1.1, 100)
plt.plot(B_plot, ursprung([steigung], B_plot), 'r-', linewidth=1.5,
         label=f'ODR-Fit: $y = ({steigung:.2f} \\pm {steigung_err:.2f})\\,\\mathrm{{m}}^{{-1}}\\mathrm{{T}}^{{-1}} \\cdot B$')

# Theorie-Gerade (mit g = 1)[cite: 1]
plt.plot(B_plot, ursprung([faktor], B_plot), 'k--', alpha=0.6,
         label=r'Theoriekurve ($g_{1\to2} = 1$)')

plt.title(r"Bestimmung des Abstandsfaktors $g_{1\to2}$ (Normaler Zeeman-Effekt)", fontsize=12, fontweight='bold')
plt.xlabel(r"Magnetische Flussdichte $B$ [$\mathrm{T}$]", fontsize=11)
plt.ylabel(r"Halber Wellenzahlunterschied $\Delta k / 2$ [$\mathrm{m}^{-1}$]", fontsize=11)
plt.xlim(0, max(B) * 1.08)
plt.ylim(0, max(halbes_dk) * 1.15)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=9, loc='upper left')

plt.tight_layout()
#plt.savefig("halbes_dk_vs_B_ODR.png", dpi=300)
plt.show()