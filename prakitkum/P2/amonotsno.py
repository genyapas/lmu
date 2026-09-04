import matplotlib.pyplot as plt
import numpy as np

temperaturen_C = np.array([90, 75, 60, 45, 30, 15, 0])
druecke_mmHg = np.array([585.4, 567.9, 546.9, 525.4, 503.4, 481.9, 454.4])
druck_ende = druecke_mmHg[-1]
druck_quotient = druecke_mmHg / druck_ende

m, b = np.polyfit(temperaturen_C, druck_quotient, 1)
fit_linie = m * temperaturen_C + b

plt.figure(figsize=(10, 6))
plt.scatter(temperaturen_C, druck_quotient, label='Messpunkte', color='blue', zorder=5)
plt.plot(temperaturen_C, fit_linie, label=f'Lineare Anpassung\ny = {m:.4f}x + {b:.4f}', color='red')
plt.xlabel('Temperatur $\\theta$ [$^°$C]', fontsize=12)
plt.ylabel('Druckverhältnis $p/p_{end}$', fontsize=12)
plt.grid(True)
plt.legend()
plt.savefig('Amontons_Diagramm.png')

print(f"Die Steigung der Ausgleichsgeraden beträgt: {m:.4f}")