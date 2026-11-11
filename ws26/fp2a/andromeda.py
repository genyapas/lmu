import numpy as np

MT = np.zeros(365)

for i in range(365):
    MT[i] = (1.5 - 24 * i / 365.25) % 24
LT = 21
PHI = 48
DEC = 40
ALT = 90 - PHI + DEC
for i in range(365):
    dt = min(24 - abs(LT - MT[i]), abs(LT - MT[i]))
    h = ALT - dt * 6
    if h > 30:
        print(f"Tag {(80 + i) % 365}: Höhe = {h:.2f}°")
