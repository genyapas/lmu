import matplotlib.pyplot as plt 
import numpy as np 

x = np.linspace(-10e-14, 10e-14, 10000000)
y = (np.exp(x)-1)/x

fig, ax = plt.subplots()
ax.plot(x, y)
plt.savefig('bildexp-8.png')
# plt.show()
