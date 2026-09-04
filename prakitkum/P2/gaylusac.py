import matplotlib.pyplot as plt
import numpy as np

temperaturen_C = np.array([0, 15, 30, 45, 60, 75, 90])
volumina_cm = np.array([5.7, 6.0, 6.4, 6.7, 7.0, 7.4, 7.65])
volumen_beginn = volumina_cm[0]
volumen_quotient = volumina_cm / volumen_beginn

m, b = np.polyfit(temperaturen_C, volumen_quotient, 1)
fit_linie = m * temperaturen_C + b

plt.figure(figsize=(10, 6))
plt.scatter(temperaturen_C, volumen_quotient, label='Messpunkte', color='green', zorder=5)
plt.plot(temperaturen_C, fit_linie, label=f'Lineare Anpassung\ny = {m:.5f}x + {b:.4f}', color='purple')
plt.xlabel('Temperatur $\\theta$ [$^°$C]', fontsize=12)
plt.ylabel('Volumenverhältnis $V/V_{beginn}$', fontsize=12)
plt.grid(True)
plt.legend()
plt.savefig('Gay_Lussac_Diagramm.png')

print(f"Die Steigung der Ausgleichsgeraden (alpha) beträgt: {m:.5f}")