import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f_hz = np.array([99, 430, 755, 1017, 1424, 1722, 2086, 2508, 2872, 3106, 3496, 3916, 4442, 5012])
u_in = 3.15  # V
u_out = np.array([0.247, 1.01, 1.65, 1.97, 2.32, 2.5, 2.62, 2.74, 2.8, 2.82, 2.86, 2.89, 2.93, 2.97]) # V

G_messung = u_out / u_in

def high_pass_model(f, fg):
    f_safe = f + 1e-9
    ratio = f_safe / fg
    return ratio / np.sqrt(1 + ratio**2)

initial_guess_fg = 1300
popt, pcov = curve_fit(high_pass_model, f_hz, G_messung, p0=[initial_guess_fg])

fg_fit = popt[0]
fg_err = np.sqrt(np.diag(pcov))[0]

f_smooth = np.linspace(0, f_hz.max(), 500)
G_fit_smooth = high_pass_model(f_smooth, fg_fit)

plt.figure(figsize=(10, 6))
plt.scatter(f_hz, G_messung, label='Messpunkte', color='blue', zorder=5)
plt.plot(f_smooth, G_fit_smooth, label='Angepasste Kurve', color='green')
plt.xlabel('Frequenz $f$ [Hz]')
plt.ylabel('Übertragungsverhältnis $|G|$')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.ylim(bottom=0, top=1.1)
plt.xlim(left=0)
plt.savefig('hochpass_fit_linear.png')
plt.show()

print(f"Experimentell bestimmte Grenzfrequenz: fg = {fg_fit:.2f} +/- {fg_err:.2f} Hz")