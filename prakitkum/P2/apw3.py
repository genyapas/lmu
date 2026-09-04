import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

t = np.array([18, 36, 64, 82])
T = np.array([-2.8, -3.0, -3.15, -3.25])

m, b = np.polyfit(t, T, 1)
fit_linie = m * t + b

plt.figure(figsize=(10, 6))
plt.scatter(t, T, label='Messpunkte', color='blue', zorder=5)
plt.plot(t, fit_linie, label=f'Lineare Anpassung\ny = {m:.4f}x + {b:.4f}', color='red')
plt.xlabel('Zeit $t$ [s]', fontsize=12)
plt.ylabel('Temperatur $T$ [°C]', fontsize=12)
plt.grid(True)
plt.legend()
#plt.savefig('Boyle_Mariotte_Diagramm.png')
plt.show()