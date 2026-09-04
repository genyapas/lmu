import numpy as np
import matplotlib.pyplot as plt

def datenanalyse(time_s, voltage_v, time_scale_s, voltage_scale_v, probe_setting_label):
    #1. Unsicherheiten der Messgrößen berechnen
    delta_t = time_scale_s / 20.0
    delta_u = voltage_scale_v / 20.0

    #2. Daten linearisieren und Fehler fortpflanzen
    #y = ln(U)
    y_values = np.log(voltage_v)
    #Fehlerfortpflanzung: Δy = |d(lnU)/dU| * ΔU = (1/U) * ΔU
    delta_y = (1 / voltage_v) * delta_u

    #3. Gewichtete lineare Regression durchführen
    #Gewichtung w = 1 / (Fehler)^2
    weights = 1 / (delta_y**2)
    
    #polyfit mit Gewichtung und Kovarianzmatrix
    p, cov = np.polyfit(time_s, y_values, 1, w=weights, cov=True)
    m, b = p
    delta_m = np.sqrt(cov[0, 0])

    #Relaxazionszeit
    tau_c = -1 / m
    #Fehlerfortpflanzung: Δτ = |dτ/dm| * Δm = (1/m^2) * Δm
    delta_tau_c = (1 / (m**2)) * delta_m

    plt.figure(figsize=(10, 7))
    plt.errorbar(time_s, y_values, yerr=delta_y, xerr=delta_t, fmt='o', label='Messpunkte mit Fehlerbalken', capsize=5, color='blue', ecolor='darkblue', markerfacecolor='lightblue', markersize=8)
    fit_line = m * time_s + b
    plt.plot(time_s, fit_line, color='red', label='Lineare Anpassung (gewichtet)')
    plt.xlabel('Zeit $t$ [s]', fontsize=12)
    plt.ylabel('ln($U$ / V)', fontsize=12)
    plt.grid(True)
    legend_text = (
        rf'Steigung $m = ({m:.4f} \pm {delta_m:.4f})$ s$^{{-1}}$' + '\n' +rf'Relaxationszeit $\tau_C = ({tau_c:.4f} \pm {delta_tau_c:.4f})$ s')
    plt.legend(title=legend_text, fontsize='medium', title_fontsize='medium')
    filename = f'Entladekurve_{probe_setting_label.replace(" ", "_")}.png'
    plt.savefig(filename)    
    return tau_c, delta_tau_c

time_s = np.array([200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]) / 1000.0
time_skala_s = 200 / 1000.0 # 200 ms/div

#Analyse für Tastkopfeinstellung 1x
spannung_1x_v = np.array([4.59, 3.15, 2.16, 1.50, 1.06, 0.718, 0.505, 0.353, 0.273, 0.178])
spannung_skala_1x_v = 1.0 #1 V/div
tau_1x, delta_tau_1x = datenanalyse(time_s, spannung_1x_v, time_skala_s, spannung_skala_1x_v, 'Tastkopf 1x')

#Analyse für Tastkopfeinstellung 10x
spannung_10x_mv = np.array([642, 501, 399, 321, 252, 201, 159, 127, 98.5, 82.5])
spannung_10x_v = spannung_10x_mv / 1000.0 
spannung_skala_10x_v = 100 / 1000.0 #100 mV/div
tau_10x, delta_tau_10x = datenanalyse(time_s, spannung_10x_v, time_skala_s, spannung_skala_10x_v, 'Tastkopf 10x')