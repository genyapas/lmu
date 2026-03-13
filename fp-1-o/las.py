import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Messdaten
d = np.array([1.8, 3.5, 6.6, 7.6, 10.2])
P = np.array([1.0, 3.0, 5.4, 5.9, 6.2])

# Modellfunktion: P(d) = P_tot * (1 - exp(-d^2 / (2 * w^2)))
def gaussian_fit(d, P_tot, w):
    return P_tot * (1 - np.exp(-d**2 / (2 * w**2)))

# Curve Fit
popt, pcov = curve_fit(gaussian_fit, d, P, p0=[6.3, 3.0])

# Plotting
d_plot = np.linspace(0, 12, 100)
plt.scatter(d, P, color='red', label='Messwerte')
plt.plot(d_plot, gaussian_fit(d_plot, *popt), label=f'Gauß-Fit')
plt.xlabel('Blendendurchmesser d [mm]')
plt.ylabel('Leistung P [mW]')
plt.legend()
plt.grid(True)
plt.show()