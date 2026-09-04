import numpy as np
import matplotlib.pyplot as plt

skt = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
U_V = np.array([0.01, 0.99, 1.98, 2.96, 3.95, 4.94, 5.93, 6.92, 7.91, 8.9, 9.81])

delta_skt = 0.3
delta_U_V = 0.009 * U_V + 0.04
m, b = np.polyfit(skt, U_V, 1)

plt.figure(figsize=(10, 7))
plt.errorbar(skt, U_V, xerr=delta_skt, yerr=delta_U_V, fmt='o', color='blue', label='Messpunkte mit Unsicherheit', capsize=5, zorder=10)
skt_fit = np.linspace(0, 1000, 200)
U_fit = m * skt_fit + b
plt.plot(skt_fit, U_fit, color='red', label='Lineare Regression')
plt.xlabel('Helipot-Einstellung [Skt]', fontsize=12)
plt.ylabel('Ausgangsspannung $U$ [V]', fontsize=12)
plt.grid(True)
plt.legend()
plt.xlim(-10, 1010)
plt.ylim(-0.1, 10.1)
plt.savefig('helipot_kennlinie.png')