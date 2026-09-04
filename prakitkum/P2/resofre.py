import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f_khz = np.array([3.01, 3.3, 3.57, 3.68, 3.79, 3.91, 4.02, 4.08, 4.45, 5.14, 6.01]) 
u2_mv = np.array([407, 620, 1130, 1530, 1840, 1700, 1460, 1270, 728, 379, 238])

R_M = 340.0     
f_hz = f_khz * 1000 
u2_v = u2_mv / 1000  
strom_a = u2_v / R_M

def custom_resonance_model(f, a, b, fr):
    term = (b / f) * (f**2 - fr**2)
    return a / np.sqrt(1 + term**2)

a_guess = np.max(strom_a)
fr_guess = f_hz[np.argmax(strom_a)]
b_guess = 1e-5 

initial_guesses = [a_guess, b_guess, fr_guess]

popt, pcov = curve_fit(custom_resonance_model, f_hz, strom_a, p0=initial_guesses, maxfev=5000)

a_fit, b_fit, fr_fit = popt
perr = np.sqrt(np.diag(pcov))
a_err, b_err, fr_err = perr

f_smooth = np.linspace(f_hz.min(), f_hz.max(), 500)
strom_fit_smooth = custom_resonance_model(f_smooth, a_fit, b_fit, fr_fit) * 1000 # in mA

plt.figure(figsize=(10, 6))
plt.scatter(f_hz, strom_a * 1000, label='Messpunkte', color='blue', zorder=5)
plt.plot(f_smooth, strom_fit_smooth, label='Angepasste Kurve', color='darkred')
plt.xlabel('Frequenz $f$ [Hz]')
plt.ylabel('Strom $I$ [mA]')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.savefig('resonanzkurve_custom_fit.png')
plt.show()

print(f"Resonanzfrequenz fr = ({fr_fit:.1f} +/- {fr_err:.1f}) Hz")