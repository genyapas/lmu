import matplotlib.pyplot as plt
import numpy as np

def Sn(x, N):

    sum, z = 1, 1
    for k in range(1, N + 1):
        z = z * x / k
        sum += z

    return sum

x = -50
values = list()
for N in range (0, 81):
    values.append(Sn(x, N))

fig, ax = plt.subplots()

N = list(range(81))
ax.plot(N, values, label = f"x = {x}")
ax.legend()
plt.xlabel('N')
plt.ylabel(r'$S_N(x)$')
plt.show()