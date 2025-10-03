import numpy as np
import matplotlib.pyplot as plt

L_cm = np.array([5, 15, 20, 30, 37])
U_V = np.array([0.323, 0.983, 1.318, 1.981, 2.440])

L_m = L_cm / 100.0
delta_L_m = 0.3 / 100.0
delta_U_V = 0.009 * U_V + 0.004

L_m_reshaped = L_m[:, np.newaxis]
m, _, _, _ = np.linalg.lstsq(L_m_reshaped, U_V, rcond=None)
slope = m[0]

plt.figure(figsize=(10, 7))
plt.errorbar(L_m, U_V, xerr=delta_L_m, yerr=delta_U_V, fmt='o', color='blue', capsize=5)

L_fit = np.linspace(0, 0.4, 100)
U_fit = slope * L_fit
plt.plot(L_fit, U_fit, color='red')
plt.xlabel('Drahtlänge $L$ [m]', fontsize=12)
plt.ylabel('Spannungsabfall $U$ [V]', fontsize=12)
plt.grid(True)
plt.xlim(0)
plt.ylim(0)
plt.savefig('spannungsabfall_draht.png')