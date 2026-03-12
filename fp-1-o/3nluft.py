import numpy as np
import scipy.odr as odr
import matplotlib.pyplot as plt

# --- Messdaten ---
m1 = np.array([0, 10, 20, 30, 40, 50], dtype=float)
p1 = np.array([534, 629, 711, 779, 854, 943], dtype=float)

m2 = np.array([0, 10, 20, 30, 40, 50], dtype=float)
p2 = np.array([501, 586, 657, 744, 822, 884], dtype=float)

m3 = np.array([0, 10, 20, 30, 40, 50, 60], dtype=float)
p3 = np.array([483, 543, 616, 685, 755, 848, 920], dtype=float)

err_m = 1.0  # Ablesefehler Ringe (+- 1 Periode)
err_p1 = 0.002 * p1 + 1.0
err_p2 = 0.002 * p2 + 1.0
err_p3 = 0.002 * p3 + 1.0

datasets = [
    (m1, p1, err_p1, "Messung 1"),
    (m2, p2, err_p2, "Messung 2"),
    (m3, p3, err_p3, "Messung 3"),
]

def linear_func(B, x):
    return B[0] * x + B[1]

slopes = []
slope_errs = []

for m, p_vals, err_p, name in datasets:
    m = np.asarray(m, dtype=float)
    p_vals = np.asarray(p_vals, dtype=float)
    err_p = np.asarray(err_p, dtype=float)

    model = odr.Model(linear_func)
    data = odr.RealData(p_vals, m, sx=err_p, sy=np.full_like(m, err_m))
    myodr = odr.ODR(data, model, beta0=[0.12, -60.0])
    out = myodr.run()

    a = out.beta[0]
    a_err = out.sd_beta[0]

    slopes.append(a)
    slope_errs.append(a_err)

    print(f"{name}: a = {a:.6e} +/- {a_err:.6e} 1/hPa")

slopes = np.array(slopes)
slope_errs = np.array(slope_errs)

# --- Gewichteter Mittelwert (nur innerer ODR-Fehler) ---
# Gewichte w_i = 1 / sigma_i^2
weights = 1.0 / (slope_errs ** 2)
sum_w = np.sum(weights)

mean_slope = np.sum(weights * slopes) / sum_w
err_mean_slope = np.sqrt(1.0 / sum_w)

print()
print(f"Gewichteter Mittelwert der Steigung: {mean_slope:.6e} 1/hPa")
print(f"Fehler des gewichteten Mittelwerts:  {err_mean_slope:.6e} 1/hPa")

# --- Apparatur-Parameter ---
lambd = 520e-9        # m
s = 256.38e-3         # m
err_s = 0.03e-3       # m
p_0 = 1013.25         # hPa

# --- Brechungsindex-Berechnung ---
delta_n = mean_slope * (lambd / s) * p_0

# relative Fehler (nur aus Fehler des Mittelwerts und s)
rel_err_a = (err_mean_slope / mean_slope) if mean_slope != 0 else 0.0
rel_err_s = err_s / s

err_delta_n = abs(delta_n) * np.sqrt(rel_err_a**2 + rel_err_s**2)

print()
print(f"Delta n (bei {p_0} hPa): {delta_n:.7e} +/- {err_delta_n:.7e}")
print(f"n_Luft: {1 + delta_n:.7e} +/- {err_delta_n:.7e}")

# --- Plot ---
plt.figure(figsize=(8, 5))
x_pos = np.arange(1, len(slopes) + 1)

plt.errorbar(x_pos, slopes, yerr=slope_errs, fmt='ko', capsize=5, markersize=6,
             label='Einzelmessungen (ODR innerer Fehler)')
plt.axhline(mean_slope, color='red', linestyle='--',
            label=f'Gewichteter Mittelwert = {mean_slope:.5f}')
plt.fill_between([0.5, len(slopes) + 0.5], mean_slope - err_mean_slope, mean_slope + err_mean_slope,
                 color='red', alpha=0.2, label='Fehler des gewichteten Mittelwerts')

plt.xticks(x_pos, ['Messung 1', 'Messung 2', 'Messung 3'])
plt.ylabel('Steigung Δm / Δp [1/hPa]', fontsize=12)
plt.title('Gewichteter Mittelwert der Steigungen (innerer Fehler)', fontsize=14)
plt.grid(True, axis='y', linestyle=':', alpha=0.7)
plt.legend(loc='best')
plt.tight_layout()
plt.show()
