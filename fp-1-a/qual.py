import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Daten (Alpha von 180° bis 0° in 10er Schritten)
alpha_deg = np.arange(180, -1, -10)

# Messreihen in mV aus den Bildern transkribiert
U_3680 = np.array([-136, -135, -120, -105, -84, -62, -40, -23, 15, 17, 43, 55, 69, 68, 69, 53, 72, 72, 78])
U_5130 = np.array([-171, -165, -145, -110, -66, -19, 28, 61, 82, 91, 93, 85, 68, 46, 23, 0, -17, -27, -32])
U_6270 = np.array([96, 86, 67, 29, 0, -33, -51, -57, -52, -36, -14, 9, 22, 26, 25, 20, 15, 11, 11])

#Umrechnung von Alpha in Theta
alpha_rad = np.radians(alpha_deg)
theta_rad = np.arccos(0.5 * np.cos(alpha_rad) - 0.5)
theta_deg = np.degrees(theta_rad)

#Fit-Funktionen
def fit_l2(theta, A, offset):
    # P2(cos(theta)) = 0.5 * (3 * cos^2(theta) - 1)
    x = np.cos(theta)
    P2 = 0.5 * (3 * x**2 - 1)
    return A * P2 + offset

def fit_l3(theta, A, offset):
    # P3(cos(theta)) = 0.5 * (5 * cos^3(theta) - 3 * cos(theta))
    x = np.cos(theta)
    P3 = 0.5 * (5 * x**3 - 3 * x)
    return A * P3 + offset

def fit_l4(theta, A, offset):
    # P4(cos(theta)) = 1/8 * (35 * cos^4(theta) - 30 * cos^2(theta) + 3)
    x = np.cos(theta)
    P4 = 0.125 * (35 * x**4 - 30 * x**2 + 3)
    return A * P4 + offset

popt_2, _ = curve_fit(fit_l2, theta_rad, U_3680, p0=[100, 0])
popt_3, _ = curve_fit(fit_l3, theta_rad, U_5130, p0=[150, 0])
popt_4, _ = curve_fit(fit_l4, theta_rad, U_6270, p0=[100, 0])

#X-Werte
theta_fit_rad = np.linspace(min(theta_rad), max(theta_rad), 200)
theta_fit_deg = np.degrees(theta_fit_rad)

plt.figure(figsize=(10, 6))

plt.plot(theta_deg, U_3680, 'bo', label='3680 Hz (Messung)')
plt.plot(theta_deg, U_5130, 'ro', label='5130 Hz (Messung)')
plt.plot(theta_deg, U_6270, 'go', label='6270 Hz (Messung)')

plt.plot(theta_fit_deg, fit_l2(theta_fit_rad, *popt_2), 'b-', label=f'Fit l=2 (A={popt_2[0]:.1f})')
plt.plot(theta_fit_deg, fit_l3(theta_fit_rad, *popt_3), 'r-', label=f'Fit l=3 (A={popt_3[0]:.1f})')
plt.plot(theta_fit_deg, fit_l4(theta_fit_rad, *popt_4), 'g-', label=f'Fit l=4 (A={popt_4[0]:.1f})')

plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.xlabel(r'Polarwinkel $\theta$ [Grad]', fontsize=12)
plt.ylabel('Amplitude [mV]', fontsize=12)
plt.title('Amplitudenverlauf und Fit der Legendrepolynome', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.4)

plt.tight_layout()
plt.show()