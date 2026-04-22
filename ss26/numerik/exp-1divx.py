import matplotlib.pyplot as plt 
import numpy as np 

x = np.linspace(-10e-14, 10e-14, 10000000)
y = (np.exp(x)-1)/x
print(max(y), min(y))
fig, ax = plt.subplots()
ax.plot(x, y)
#plt.show()
