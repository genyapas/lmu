import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

p0 = 725.9
x = np.array([7.2, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.8, 9.0])
p = np.array([725.9, 705.9, 688.4, 671.4, 654.9, 638.4, 625.4, 611.9, 593.9, 585.4])
druck_quotient = p0 / p

m, b = np.polyfit(x, druck_quotient, 1)
fit_linie = m * x + b

plt.figure(figsize=(10, 6))
plt.scatter(x, druck_quotient, label='Messpunkte', color='blue', zorder=5)
plt.plot(x, fit_linie, label=f'Lineare Anpassung\ny = {m:.4f}x + {b:.4f}', color='red')
plt.xlabel('Kolbenposition $x$ [cm]', fontsize=12)
plt.ylabel('Druckverhältnis $p_0/p$', fontsize=12)
plt.grid(True)
plt.legend()
plt.savefig('Boyle_Mariotte_Diagramm.png')
plt.show()