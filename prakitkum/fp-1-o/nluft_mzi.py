import numpy as np
import scipy.odr as odr
import matplotlib.pyplot as plt

# Messung 1
m1 = np.array([0, 10, 20, 30, 40, 50])
p1 = np.array([534, 629, 711, 779, 854, 943])

# Messung 2 
m2 = np.array([0, 10, 20, 30, 40, 50])
p2 = np.array([501, 586, 657, 744, 822, 884]) 

# Messung 3
m3 = np.array([0, 10, 20, 30, 40, 50, 60])
p3 = np.array([483, 543, 616, 685, 755, 848, 920])

# Unsicherheiten der Messgeräte
err_m = 1.0  # Ablesefehler Ringe (+- 1 Periode)
err_p1 = 0.002 * p1 + 1.0  # 0.2% + 1 hPa
err_p2 = 0.002 * p2 + 1.0
err_p3 = 0.002 * p3 + 1.0

datasets = [(m1, p1, err_p1, "Messung 1"), 
            (m2, p2, err_p2, "Messung 2"), 
            (m3, p3, err_p3, "Messung 3")]


def linear_func(B, x):
    return B[0] * x + B[1]

slopes = []
err_slopes_inner = []

for m, p_val, err_p, name in datasets:
    model = odr.Model(linear_func)
    data = odr.RealData(p_val, m, sx=err_p, sy=np.full_like(m, err_m))
    myodr = odr.ODR(data, model, beta0=[0.12, -60.0])
    output = myodr.run()
    
    slope = output.beta[0]
    err_slope = output.sd_beta[0]
    
    slopes.append(slope)
    err_slopes_inner.append(err_slope)
    #print(f"{name}: a = {slope:.5f} +/- {err_slope:.5f} 1/hPa")



slopes = np.array(slopes)
err_slopes_inner = np.array(err_slopes_inner)

# Da der systematische Unterschied zwischen den Messungen dominiert, 
# nutzen wir den äußeren Fehler (Standardabweichung des Mittelwerts)
mean_slope = np.mean(slopes)
err_slope_ext = np.std(slopes, ddof=1) / np.sqrt(len(slopes))

# Parameter der Apparatur
lambd = 520e-9        # Diodenlaser (Klasse 2) in m
s = 256.38e-3         # Küvettenlänge in m
err_s = 0.03e-3       # Fehler der Küvette in m
p_0 = 1013.25         # Standarddruck in hPa 


# Brechungsindex bei der gemessenen Raumtemperatur (20.3 °C)
delta_n = mean_slope * (lambd / s) * p_0

# Relative Fehler für Gauß
rel_err_a = err_slope_ext / mean_slope
rel_err_s = err_s / s

# Gaußsche Fehlerfortpflanzung
err_delta_n = delta_n * np.sqrt(rel_err_a**2 + rel_err_s**2)

#Umrechnung des Brechungsindex auf 20.0°C
# Temperaturwerte in Kelvin
T_meas = 20.3 + 273.15
T_target = 20.0 + 273.15

err_T_meas = 1.0 + 0.003 * 20.3   # Temperaturfehler: 0.3% + 1°C
err_T_meas_k = err_T_meas            # gleiche Größe in Kelvin

# Temperaturkorrekturfaktor
temp_factor = T_meas / T_target

# Ableitung des Faktors nach T_meas: df/dT = 1 / T_target
df_dT = 1.0 / T_target

# Fehler des Temperaturfaktors
err_temp_factor = abs(df_dT) * err_T_meas_k

# Umgerechneter Wert
delta_n_20C = delta_n * temp_factor

# Fehlerfortpflanzung:
err_delta_n_20C = np.sqrt((temp_factor * err_delta_n)**2 +(delta_n * err_temp_factor)**2)


#print(f"Mittlere Steigung (äußerer Fehler): {mean_slope:.5f} +/- {err_slope_ext:.5f} 1/hPa")
print(f"(n - 1) bei 20.3 °C: {delta_n:.7f} +/- {err_delta_n:.7f}")
print(f"n_Luft (20.3 °C): {(1 + delta_n):.7f} +/- {err_delta_n:.7f}")
print("\nUmrechnung auf 20.0 °C:")
print(f"(n - 1) bei 20.0 °C: {delta_n_20C:.7f} +/- {err_delta_n_20C:.7f}")
print(f"n_Luft (20.0 °C):     {1 + delta_n_20C:.7f} +/- {err_delta_n_20C:.7f}")


#plt.figure(figsize=(8, 5))
#messungen_x = [1, 2, 3]

# ODR-Punkte plotten
#plt.errorbar(messungen_x, slopes, yerr=err_slopes_inner, fmt='ko', 
#             capsize=5, markersize=8, label='Einzelmessungen (ODR innerer Fehler)')

# Mittelwert und äußerer Fehler als Band
#plt.axhline(mean_slope, color='red', linestyle='--', 
#            label=f'Mittelwert ({mean_slope:.5f})')
#plt.axhspan(mean_slope - err_slope_ext, mean_slope + err_slope_ext, 
#            color='red', alpha=0.2, label='Äußerer Fehler (Standardabw. d. Mittelwerts)')

#plt.xticks(messungen_x, ['Messung 1', 'Messung 2', 'Messung 3'])
#plt.ylabel('Steigung $\\Delta m / \\Delta p$ [1/hPa]', fontsize=12)
#plt.title('Mittelwert der Steigungen (äußerer Fehler)', fontsize=14)
#plt.grid(True, axis='y', linestyle=':', alpha=0.7)
#plt.legend(loc='best')
#plt.tight_layout()

#plt.show()