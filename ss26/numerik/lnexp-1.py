import matplotlib.pyplot as plt
import numpy as np

#x = np.linspace(-10e-13, 10e-13, 10000)
#y = (np.exp(x)-1)/np.exp(np.log(x))

#fig, ax = plt.subplots()
#ax.plot(x, y)
#plt.show()
###
z = np.linspace(-1e-6, 1e-6, 10000)
w = (np.exp(z)-1)/np.log(np.exp(z))

fig, ax = plt.subplots()
ax.plot(z, w)
plt.show()
