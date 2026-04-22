import matplotlib.pyplot as plt
import numpy as np

sum = []

p = 1e8
qs = np.logspace(-10, 5, 1000)

for q in qs:
    x = p - np.sqrt(p**2 - q)
    sum.append(x**2 - 2*p*x + q)

fig, ax = plt.subplots()
ax.plot(sum)
if sum.index(max(sum)) > abs(sum.index(min(sum))):
    print(qs[sum.index(max(sum))])
else:
    print(qs[sum.index(min(sum))])

plt.show()