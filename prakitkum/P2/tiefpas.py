import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f_hz = np.array([180, 468, 733, 1017, 1372, 1720, 2155, 2451, 2813, 3302, 3760, 4096, 4487, 5010])
u_in = 29.2  # V
u_out = np.array([29.3, 27.2, 24.7, 21.7, 18.8, 16.5, 13.8, 12.5, 11.1, 9.72, 8.68, 7.96, 7.40, 6.64]) # V

G_messung = u_out / u_in
#Korrektur für Messschwankungen, |G| kann physikalisch nicht > 1 sein
G_messung[G_messung > 1] = 1

def low_pass_model(f, fg):
    return 1 / np.sqrt(1 + (f / fg)**2)

initial_guess_fg = 1200
popt, pcov = curve_fit(low_pass_model, f_hz, G_messung, p0=[initial_guess_fg])

fg_fit = popt[0]
fg_err = np.sqrt(np.diag(pcov))[0]

f_smooth = np.linspace(0, f_hz.max(), 500)
G_fit_smooth = low_pass_model(f_smooth, fg_fit)

plt.figure(figsize=(10, 6))
plt.scatter(f_hz, G_messung, label='Messpunkte', color='blue', zorder=5)
plt.plot(f_smooth, G_fit_smooth, label='Angepasste Kurve', color='green')

plt.xlabel('Frequenz $f$ [Hz]')
plt.ylabel('Übertragungsverhältnis $|G|$')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.ylim(bottom=0, top=1.1)
plt.xlim(left=0)
plt.savefig('tiefpass_fit_linear.png')
plt.show()
print(f"Experimentell bestimmte Grenzfrequenz: fg = {fg_fit:.2f} +/- {fg_err:.2f} Hz")