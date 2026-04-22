import matplotlib.pyplot as plt
import numpy as np

sum = []

p = 1e8
qs = np.logspace(-10, 5, 1000)

for q in qs:
    x = q / (p + np.sqrt(p**2 - q))
    sum.append(x**2 - 2*p*x + q)

fig, ax = plt.subplots()
ax.plot(sum)

plt.show()