import matplotlib.pyplot as plt
import numpy as np
from scipy.odr import ODR, Model, RealData

# Messdaten
I = np.array([2.12, 4.04, 6.18, 8.05, 10.05])  # Stromstärke in A
dI = np.array([0.02, 0.03, 0.04, 0.04, 0.05])  # Fehler Stromstärke in A

B = np.array([135.0, 264.0, 405.0, 528.0, 630.0])  # Magnetfeld in mT
dB = np.array([3.0, 5.0, 8.0, 11.0, 13.0])  # Fehler Magnetfeld in mT


# Fit-Funktion für ODR
def linear_func(p, x):
    m, c = p
    return m * x + c


# 3. ODR Setup und Fit durchführen
linear_model = Model(linear_func)
data = RealData(I, B, sx=dI, sy=dB) 
odr = ODR(data, linear_model, beta0=[65.0, 0.0])
output = odr.run()

# Fit-Parameter und Unsicherheiten
m_fit, c_fit = output.beta
dm_fit, dc_fit = output.sd_beta

print(f"Steigung m:        ({m_fit:.3f} +/- {dm_fit:.3f}) mT/A")
print(f"Achsenabschnitt c: ({c_fit:.3f} +/- {dc_fit:.3f}) mT")

# Plot
plt.figure(figsize=(8, 5))

# Messpunkte mit Fehlerbalken
plt.errorbar(
    I,
    B,
    xerr=dI,
    yerr=dB,
    fmt="o",
    color="navy",
    ecolor="darkred",
    capsize=3,
    label="Messdaten mit Fehler",
)

# Ausgleichsgerade 
I_line = np.linspace(0, 11, 200)
B_line = linear_func([m_fit, c_fit], I_line)

plt.plot(I_line, B_line, "k--")

plt.xlabel("Stromstärke $I$ / A")
plt.ylabel("Magnetische Flussdichte $B$ / mT")
plt.title("Ausgleichsgerade für Magnetfeld vs. Stromstärke")
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim(0, 11)
plt.ylim(0, 700)
plt.legend()
plt.tight_layout()

plt.savefig("kalibrierung_magnetfeld.png", dpi=300)
