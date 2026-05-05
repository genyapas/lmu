import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1e-17, 2e-15, 100000)
y = (np.exp(x)-1)/np.exp(np.log(x))

fig, ax = plt.subplots()
ax.plot(x, y)

w = (np.exp(x)-1)/np.log(np.exp(x))

ax.plot(x, w)

plt.show()
