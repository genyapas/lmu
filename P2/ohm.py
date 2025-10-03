import numpy as np
import matplotlib.pyplot as plt

u_V = np.array([1.99, 4.06, 6.10, 8.00, 9.91, 12.01, 13.89, 15.81, 17.84, 19.69])
i_mA = np.array([0.6, 1.23, 1.84, 2.43, 3.01, 3.65, 4.22, 4.81, 5.44, 6.00])

i_A = i_mA / 1000.0

#Voltmeter im 20V-Bereich (Auflösung 0.01V) -> 4dgt = 0.04V
delta_u = 0.009 * u_V + 0.04
#Amperemeter im 20mA-Bereich (Auflösung 0.01mA) -> 5dgt = 0.05mA
delta_i_mA = 0.01 * i_mA + 0.05
delta_i_A = delta_i_mA / 1000.0

m_optimal, b_optimal = np.polyfit(u_V, i_A, 1)
R_optimal = 1 / m_optimal

u_first_err_max = u_V[0] - delta_u[0]
i_first_err_max = i_A[0] + delta_i_A[0]
u_last_err_max = u_V[-1] + delta_u[-1]
i_last_err_max = i_A[-1] - delta_i_A[-1]

m_max = ( (i_A[-1] + delta_i_A[-1]) - (i_A[0] - delta_i_A[0]) ) / ( (u_V[-1] - delta_u[-1]) - (u_V[0] + delta_u[0]) )
m_min = ( (i_A[-1] - delta_i_A[-1]) - (i_A[0] + delta_i_A[0]) ) / ( (u_V[-1] + delta_u[-1]) - (u_V[0] - delta_u[0]) )
R_min = 1 / m_max
R_max = 1 / m_min
delta_R = (R_max - R_min) / 2

plt.figure(figsize=(12, 8))
plt.errorbar(u_V, i_A, yerr=delta_i_A, xerr=delta_u, fmt='o', color='blue', label='Messpunkte mit Unsicherheit', capsize=5)
u_fit = np.linspace(0, 21, 100)
i_fit = m_optimal * u_fit + b_optimal
plt.plot(u_fit, i_fit, color='red', label=f'Optimale Gerade ($I(U)$)')
plt.plot(u_fit, m_max * u_fit + b_optimal, 'g--', label='Maximale Steigung')
plt.plot(u_fit, m_min * u_fit + b_optimal, 'm--', label='Minimale Steigung')
plt.xlabel('Spannung $U$ [V]', fontsize=12)
plt.ylabel('Stromstärke $I$ [A]', fontsize=12)
plt.grid(True)
plt.legend()
plt.xlim(0, 21)
plt.ylim(0, max(i_A)*1.1)

ergebnis_text = (
    f"Aus der optimalen Geraden:\n"
    f"$m = (3.04 \\pm 0.05) \\times 10^{{-4}}$ A/V\n"
    f"$R = 1/m = {R_optimal:.1f} \\Omega$\n\n"
    f"Aus den Grenzgeraden:\n"
    f"$R_{{max}} = {R_max:.1f} \\Omega$\n"
    f"$R_{{min}} = {R_min:.1f} \\Omega$\n"
    f"$\\Delta R = (R_{{max}} - R_{{min}})/2 = {delta_R:.1f} \\Omega$\n\n"
    f"Ergebnis: $R = ({R_optimal:.1f} \\pm {delta_R:.1f}) \\Omega$")
m_err = (m_max - m_min) / 2
ergebnis_text_neu = (
    f"Aus der optimalen Geraden ($I = m \\cdot U + b$):\n"
    f"  Steigung $m = {m_optimal*1000:.3f} \\times 10^{{-3}}$ A/V\n"
    f"  $R = 1/m = {R_optimal:.1f} \\Omega$\n\n"
    f"Aus grafischer Fehlerabschätzung:\n"
    f"  $m_{{max}} = {m_max*1000:.3f} \\times 10^{{-3}}$ A/V  $\\rightarrow R_{{min}} = {R_min:.1f} \\Omega$\n"
    f"  $m_{{min}} = {m_min*1000:.3f} \\times 10^{{-3}}$ A/V  $\\rightarrow R_{{max}} = {R_max:.1f} \\Omega$\n"
    f"  Unsicherheit $\\Delta R = (R_{{max}} - R_{{min}})/2 = {delta_R:.1f} \\Omega$\n\n"
    f"Ergebnis: $R = ({R_optimal:.0f} \\pm {delta_R:.0f}) \\Omega$")

plt.text(1, 0.004, ergebnis_text_neu, fontsize=11, bbox=dict(facecolor='white', alpha=0.8))
plt.savefig('ohm_kennlinie.png')