import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Parameter & Konstanten laut Skript
d = 3e-3          # Plattenabstand FPI in m
n = 1.45          # Brechungsindex Quarzglas
faktor_2dn = 2 * d * n  # 8.7e-3 m

# Radius-Unsicherheit: realistisch für Motic 3-Punkt-Kreise (ca. 50 µm)
r_err = 50e-6     

# Ringindizes p
p = np.array([1, 2, 3, 4], dtype=float)

# berechnete Magnetfeldstärken aus TV1
B_texte = [
    "B1 = (392.25 ± 10.25) mT",
    "B2 = (456.37 ± 11.52) mT",
    "B3 = (519.08 ± 12.59) mT",
    "B4 = (593.66 ± 14.11) mT",
    "B5 = (656.47 ± 15.24) mT"
]

# Gemessene Radien in Metern
r_in = np.array([
    [4855.08, 9845.92, 12971.05, 15412.45],  # Messung 1
    [4651.26, 9767.54, 12887.85, 15385.42],  # Messung 2
    [4468.59, 9637.60, 12828.53, 15305.57],  # Messung 3
    [4349.13, 9592.45, 12734.37, 15326.47],  # Messung 4
    [4287.62, 9570.36, 12777.98, 15209.38]   # Messung 5
]) * 1e-6

r_out = np.array([
    [6988.72, 11062.65, 13889.25, 16220.20], # Messung 1
    [7199.90, 11139.57, 13971.76, 16270.98], # Messung 2
    [7350.79, 11198.02, 14067.30, 16347.00], # Messung 3
    [7470.67, 11314.67, 14012.22, 16360.22], # Messung 4
    [7577.91, 11382.68, 14177.79, 16391.10]  # Messung 5
]) * 1e-6

def f_lin(x, m, c):
    return m * x + c

def fit_ring(p_arr, r_arr):
    y = r_arr**2
    sy = 2 * r_arr * r_err  # Gaußsche Fehlerfortpflanzung: d(r^2) = 2*r*dr
    
    # absolute_sigma=True sorgt dafür, dass r_err als absolute Unsicherheit verwendet wird!
    popt, pcov = curve_fit(f_lin, p_arr, y, sigma=sy, absolute_sigma=True)
    m, c = popt[0], popt[1]
    
    var_m = pcov[0, 0]
    var_c = pcov[1, 1]
    cov_mc = pcov[0, 1]
    
    # Schnittpunkt p0 = -c / m (Gl. 33)[cite: 1]
    p0 = -c / m
    
    # Partielle Ableitungen nach c und m
    dp0_dc = -1.0 / m
    dp0_dm = c / (m**2)
    
    # Gaußsche Fehlerfortpflanzung mit Kovarianz
    var_p0 = (dp0_dc**2) * var_c + (dp0_dm**2) * var_m + 2.0 * dp0_dc * dp0_dm * cov_mc
    p0_err = np.sqrt(var_p0)
    
    return m, c, p0, p0_err

# Auswertung & Plots
fig, axes = plt.subplots(3, 2, figsize=(13, 14))
axes = axes.flatten()

print(f"{'Messung':<10} | {'p0 (innen)':<18} | {'p0 (aussen)':<18} | {'Delta p0':<18} | {'Delta k / 2 [1/m]'}")

for i in range(5):
    m_in, c_in, p0_in, dp0_in = fit_ring(p, r_in[i])
    m_out, c_out, p0_out, dp0_out = fit_ring(p, r_out[i])
    
    delta_p0 = abs(p0_out - p0_in)
    delta_p0_err = np.sqrt(dp0_in**2 + dp0_out**2)
    
    # Gl. (37): Delta k = Delta p0 / (2 * d * n)[cite: 1]
    delta_k = delta_p0 / faktor_2dn
    delta_k_err = delta_p0_err / faktor_2dn
    
    halbes_dk = delta_k / 2
    halbes_dk_err = delta_k_err / 2
    
    print(f"Messung {i+1:<2} | {p0_in:7.4f} ± {dp0_in:6.4f} | {p0_out:7.4f} ± {dp0_out:6.4f} | "
          f"{delta_p0:7.4f} ± {delta_p0_err:6.4f} | {halbes_dk:6.2f} ± {halbes_dk_err:4.2f}")
    
    # Plotting
    ax = axes[i]
    ax.errorbar(p, (r_in[i]**2)*1e6, yerr=(2*r_in[i]*r_err)*1e6, fmt='bo', capsize=3, label=r'Innen ($\sigma^-$)')
    ax.errorbar(p, (r_out[i]**2)*1e6, yerr=(2*r_out[i]*r_err)*1e6, fmt='ro', capsize=3, label=r'Außen ($\sigma^+$)')
    
    p_lin = np.linspace(0, 4.5, 100)
    ax.plot(p_lin, (m_in * p_lin + c_in)*1e6, 'b--', label=f'Fit Innen ($p_0={p0_in:.2f}$)')
    ax.plot(p_lin, (m_out * p_lin + c_out)*1e6, 'r--', label=f'Fit Außen ($p_0={p0_out:.2f}$)')
    
    ax.set_title(f"Messung {i+1}: {B_texte[i]}", fontsize=11, fontweight='bold')
    ax.set_xlabel("Ringindex $p$")
    ax.set_ylabel(r"$r_m^2$ [$\mathrm{mm}^2$]")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=8, loc='upper left')

fig.delaxes(axes[5])

plt.tight_layout()
plt.savefig("r^2_vs_p_Fit.png", dpi=300)
plt.show()