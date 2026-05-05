import matplotlib.pyplot as plt
import numpy as np

error = []

p = 1e8
qs = np.logspace(-10, 5, 1000)

for q in qs:
    x_instabil = p - np.sqrt(p**2 - q)
    x_stabil = q / (p + np.sqrt(p**2 - q))
    error.append(np.abs(x_instabil - x_stabil) / x_stabil)

fig, ax = plt.subplots()
ax.plot(qs, error)


plt.show()