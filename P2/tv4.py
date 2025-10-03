import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData

m_values = np.array([-0.113, -0.102, -0.076, -0.048, -0.016])
delta_m = np.array([0.0020, 0.0019, 0.0019, 0.0018, 0.0018])

U_mV = np.array([74, 70, 52, 30, 11])
delta_U_mV = np.array([1.5, 1.5, 1.5, 1.5, 1.5])

U_V = U_mV / 1000.0
delta_U_V = delta_U_mV / 1000.0

def linear_func(p, x):
    k, c = p
    return k * x + c

linear_model = Model(linear_func)
data = RealData(x=m_values, y=U_V, sx=delta_m, sy=delta_U_V)
odr = ODR(data, linear_model, beta0=[-0.7, 0.0])
output = odr.run()

k, c = output.beta
delta_k, delta_c = output.sd_beta

plt.figure(figsize=(10, 6))
plt.errorbar(m_values, U_V, yerr=delta_U_V, xerr=delta_m, fmt='o', color='blue', ecolor='lightblue', capsize=5, label='Messdaten')

x_line = np.linspace(np.min(m_values) - 0.01, 0, 100)
y_line = linear_func((k, c), x_line)
plt.plot(x_line, y_line, color='darkorange', linestyle='--', label='Linearer Fit (ODR)')

plt.xlabel(r'Steigung des Feldstroms $\frac{dI}{dt}$ [A/s]')
plt.ylabel(r'Induzierte Spannung $U_{ind}$ [V]')
plt.legend()
plt.grid(True)
plt.savefig('tv4_induktionsgesetz_fit.png')
plt.show()
print(f"Y-Achsenabschnitt c = {c:.4f} ± {delta_c:.4f} [V]")
print(f"Steigung k = {k:.4f} ± {delta_k:.4f} [V*s/A]")
