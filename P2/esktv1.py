import numpy as np
import matplotlib.pyplot as plt

i_mA = np.array([10.9, 15.3, 19.9, 24.5, 29.3, 33.9, 38.5, 42.6, 47.4, 51.0, 55.0])
u_V = np.array([1.352, 1.351, 1.349, 1.347, 1.345, 1.343, 1.341, 1.339, 1.336, 1.334, 1.332])

u_L_anfang = 1.359 
u_L_ende = 1.336 

i_A = i_mA / 1000.0
m, b = np.polyfit(i_A, u_V, 1)

innenwiderstand_R_i = -m
leerlaufspannung_U_q_extrapoliert = b

plt.figure(figsize=(10, 6))
plt.scatter(i_A, u_V, label='Messpunkte', color='blue', zorder=5)
plt.plot(i_A, m * i_A + b, label='Lineare Regression', color='red')
plt.xlabel('Belastungsstrom $I$ [A]', fontsize=12)
plt.ylabel('Klemmenspannung $U$ [V]', fontsize=12)
plt.grid(True)
plt.legend()
plt.savefig('kennlinie_galvanische_zelle.png')

print(f"Innenwiderstand R_i: {innenwiderstand_R_i:.4f} Ohm")
print(f"Extrapolierte Leerlaufspannung U_q: {leerlaufspannung_U_q_extrapoliert:.4f} V")