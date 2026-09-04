import numpy as np
import matplotlib.pyplot as plt

# --- 1. Messdaten und Konstanten ---
# Temperaturen in Grad Celsius und Fehler
T_celsius = np.array([25.6, 50, 75, 100, 125, 150, 175, 200, 210, 220, 230, 240, 250])
delta_T_celsius = 0.5  # Fehler in °C

# Manometer-Druck (Überdruck) in bar und Fehler
p_gauge = np.array([0, 0, 0.2, 0.8, 2.2, 5.0, 9.6, 16, 20, 23.5, 29, 35, 42.5])
delta_p_gauge = 0.5  # Fehler in bar

# Umgebungsdruck in bar
p_ambient = 1.0

# --- 2. Datenaufbereitung und Fehlerfortpflanzung ---
# Umrechnung der Temperatur in Kelvin
# Der Fehler bleibt gleich: delta_T_kelvin = delta_T_celsius
T_kelvin = T_celsius + 273.15
delta_T_kelvin = delta_T_celsius

# Berechnung des absoluten Drucks in bar
# Der Fehler bleibt gleich, da p_ambient als exakt angenommen wird
p_abs = p_gauge + p_ambient
delta_p_abs = delta_p_gauge

# Berechnung der Werte für die x- und y-Achse
# x = -1/T
x_data = -1 / T_kelvin
# y = ln(p)
y_data = np.log(p_abs)

# Fehlerfortpflanzung nach Gauß
# delta_x = |(1/T^2)| * delta_T
delta_x = (1 / T_kelvin**2) * delta_T_kelvin
# delta_y = |(1/p)| * delta_p
delta_y = (1 / p_abs) * delta_p_abs

# --- 3. Lineare Regression (Geradenanpassung) ---
# Finde die Koeffizienten (Steigung m, y-Achsenabschnitt c) der Geraden y = mx + c
# polyfit gibt die Koeffizienten des Polynoms zurück, in diesem Fall Grad 1
params, cov = np.polyfit(x_data, y_data, 1, w=1/delta_y**2, cov=True)
m = params[0]  # Steigung
c = params[1]  # y-Achsenabschnitt

# Unsicherheit der Fit-Parameter
delta_m = np.sqrt(cov[0, 0])
delta_c = np.sqrt(cov[1, 1])

# Erzeuge y-Werte für die Fit-Gerade
fit_y = m * x_data + c

# --- 4. Grafische Darstellung ---
plt.figure(figsize=(10, 7))

# Plot der Messdaten mit Fehlerbalken
plt.errorbar(x_data, y_data, xerr=delta_x, yerr=delta_y, fmt='o',
             label='Messdaten', capsize=3, color='blue')

# Plot der Fit-Geraden
plt.plot(x_data, fit_y, '-', label=fr'Lineare Anpassung', color='red')
# Beschriftungen und Titel
plt.xlabel('$-1/T$  [$K^{-1}$]')
plt.ylabel(r'$\ln(p/\mathrm{bar})$')
plt.legend()
plt.grid(True)

plt.savefig('dampfdruckkurve_wasser.png')
plt.show()

print(f"Steigung m: {m:.4f} K")
print(f"Unsicherheit der Steigung delta_m: {delta_m:.4f} K")
print(f"Y-Achsenabschnitt c: {c:.4f}")
print(f"Unsicherheit des Y-Achsenabschnitts delta_c: {delta_c:.4f}")

k_B = 1.380649e-23 
e = 1.602176634e-19  

E_b_joule = m * k_B
delta_E_b_joule = delta_m * k_B

E_b_eV = E_b_joule / e
delta_E_b_eV = delta_E_b_joule / e

print(f"Eb = {E_b_joule:.4e} J")
print(f"Eb = {E_b_eV:.4f} ± {delta_E_b_eV:.4f} eV")            