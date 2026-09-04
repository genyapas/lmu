import numpy as np
import scipy.odr as odr
import matplotlib.pyplot as plt

# --- Messdaten ---
m1 = np.array([0, 10, 20, 30, 40, 50])
p1 = np.array([534, 629, 711, 779, 854, 943])

m2 = np.array([0, 10, 20, 30, 40, 50])
p2 = np.array([501, 586, 657, 744, 822, 884])

m3 = np.array([0, 10, 20, 30, 40, 50, 60])
p3 = np.array([483, 543, 616, 685, 755, 848, 920])

# --- Fehler der Druckmessung ---
err_p1 = 0.002 * p1 + 1.0
err_p2 = 0.002 * p2 + 1.0
err_p3 = 0.002 * p3 + 1.0

err_m = 1.0  # Fehler der Ringablesung

datasets = [
    (m1, p1, err_p1, "Messung 1", "o"),
    (m2, p2, err_p2, "Messung 2", "s"),
    (m3, p3, err_p3, "Messung 3", "^"),
]

# --- ODR Modell ---
def linear_func(B, x):
    return B[0] * x + B[1]

plt.figure(figsize=(8, 5))

# --- Plot + ODR ---
for m, p, err_p, label, marker in datasets:
    # Rohdaten
    plt.errorbar(m, p, yerr=err_p, xerr=err_m, fmt=marker,
                 capsize=4, markersize=6, label=label)

    # ODR Fit
    model = odr.Model(linear_func)
    data = odr.RealData(m, p, sx=np.full_like(m, err_m), sy=err_p)
    fit = odr.ODR(data, model, beta0=[1, 0]).run()

    a, b = fit.beta

    # Fit-Linie
    x_fit = np.linspace(min(m), max(m), 200)
    y_fit = a * x_fit + b
    plt.plot(x_fit, y_fit, linewidth=1.5)

plt.xlabel("m (Ringe)")
plt.ylabel("p (hPa)")
plt.title("Rohdaten der Messreihen mit ODR-Ausgleichsgeraden")
plt.grid(True, linestyle=":", alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
