import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

alpha_deg = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
beta_raw = np.array([274, 292, 311, 327.5, 347, 4, 16.5, 30.5, 39])
beta0 = 253.5

delta_alpha_deg = 1.0
delta_beta_deg = 0.5
delta_beta0_deg = 0.5

beta_corr = np.copy(beta_raw)
beta_corr[beta_raw < 100] += 360

phi = alpha_deg - (beta_corr - beta0)
phi_abs = np.abs(phi)

delta_phi_const = np.sqrt(delta_alpha_deg**2 + delta_beta_deg**2 + delta_beta0_deg**2)
delta_phi_array = np.full_like(phi_abs, delta_phi_const)

sin_alpha = np.sin(np.deg2rad(alpha_deg))

def linear_func(x, m, c):
    return m * x + c

popt, pcov = curve_fit(linear_func, sin_alpha, phi_abs, sigma=delta_phi_array, absolute_sigma=True)
m, c = popt
delta_m, delta_c = np.sqrt(np.diag(pcov))

plt.figure(figsize=(10, 6))

plt.errorbar(sin_alpha, phi_abs, yerr=delta_phi_const, fmt='o', color='blue', ecolor='lightblue', capsize=5, label='Messdaten mit Fehlerkreuzen')

x_line = np.linspace(0, 1.05, 100)
y_line = linear_func(x_line, m, c)
plt.plot(x_line, y_line, color='darkorange', linestyle='--', label='Gewichteter linearer Fit')

plt.xlabel(r'$\sin(\alpha)$')
plt.ylabel(r'$|\varphi|$ [°]')
plt.legend()
plt.xlim(0, 1.05)
plt.ylim(0, max(phi_abs) + 5)
plt.grid(True)
plt.savefig('torsionswinkel_vs_sin_alpha_fehlerkreuze.png')
plt.show()

print(f"y = ({m:.2f} ± {delta_m:.2f}) * x + ({c:.2f} ± {delta_c:.2f})")
print(f"Steigung m = {m:.4f} ± {delta_m:.4f} [V*s/A]")