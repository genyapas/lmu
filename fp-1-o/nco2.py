import numpy as np

m_halbe = np.array([15, 16, 17])
m = m_halbe / 2.0  # Ergibt 7.5, 8.0, 8.5 Perioden

# Mittelwert und äußerer Fehler (Standardfehler des Mittelwerts)
mean_m = np.mean(m)
err_mean_m = np.std(m, ddof=1) / np.sqrt(len(m))

lambd = 520e-9         # Diodenlaser in m
s = 50e-3              # Küvettenlänge in m 

T_meas = 273.15 + 20.3 # Gemessene Raumtemperatur in K
err_T = 1.1            # Fehler des Thermometers in K
T_20 = 273.15 + 20.0   # Zieltemperatur 20°C in K

n_luft_20 = 1.000272   # Literaturwert für Luft bei 20°C


# Schritt A: Brechungsindex-Differenz bei 20.3°C
delta_n_meas = mean_m * (lambd / s)

rel_err_m = err_mean_m / mean_m
err_delta_n_mess = delta_n_meas * rel_err_m

# Schritt B: Temperaturkorrektur auf 20.0°C (Dichte-Anpassung)
delta_n_20 = delta_n_meas * (T_meas / T_20)

# Schritt C: Fehlerfortpflanzung
rel_err_T = err_T / T_meas

err_delta_n_20 = delta_n_20 * np.sqrt(rel_err_m**2 + rel_err_T**2)

# Schritt D: Absolutes Endergebnis bei 20°C
n_co2_20 = n_luft_20 + delta_n_20

print(f"Gemessenes Delta n (20.3°C): {delta_n_meas:.7f}+/- {err_delta_n_mess:.7f}")
print(f"Korrigiertes Delta n (20.0°C): {delta_n_20:.7f} +/- {err_delta_n_20:.7f}")
print(f"n_CO2 (20°C): {n_co2_20:.7f} +/- {err_delta_n_20:.7f}")