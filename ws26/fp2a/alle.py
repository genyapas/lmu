import numpy as np
import matplotlib.pyplot as plt

# Objektkatalog: Name -> (RA_deg, Dec_deg, Text_Offset_X, Text_Offset_Y)
objects = {
    'NGC7662': (351.475, 42.535, -1.1,  2.2),
    'NGC457':  (19.775,  58.333, -1.0,  2.2),
    'NGC891':  (35.650,  42.350, -0.9,  2.2),
    'NGC1501': (61.750,  60.917, -1.0,  2.2),
    'M1':      (83.633,  22.017, -0.6,  2.2),
    'NGC2158': (91.858,  24.100, -0.7, -4.5)
}

# Geografische Koordinaten München
lat_deg = 48.1375
phi = np.radians(lat_deg)

# LMST in München um 00:00 MEZ am 19.11.2026 (~3.703 h)
lmst_midnight_deg = 55.55  

# Zeitachse: Local Time relative to 00:00 MEZ (-12h bis +12h)
local_time = np.linspace(-12, 12, 1000)

plt.figure(figsize=(9.5, 5.5), dpi=150)

# Kurve für jedes Objekt berechnen und zeichnen
for name, (ra_deg, dec_deg, off_x, off_y) in objects.items():
    ha_deg = (lmst_midnight_deg + local_time * 15.04107 - ra_deg) % 360
    dec = np.radians(dec_deg)
    ha = np.radians(ha_deg)
    
    sin_alt = np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.cos(ha)
    alt_deg = np.degrees(np.arcsin(sin_alt))
    
    # Höhenkurve zeichnen
    plt.plot(local_time, alt_deg, color='salmon', linewidth=1.3)
    
    # Peak (Obere Kulmination) bestimmen & markieren
    idx_max = np.argmax(alt_deg)
    t_max = local_time[idx_max]
    alt_max = alt_deg[idx_max]
    
    plt.plot(t_max, alt_max, 'bo', markersize=3.5)
    plt.text(t_max + off_x, alt_max + off_y, name, color='blue', fontsize=8.5, fontweight='bold')

# Dämmerungsgrenzen (-18° Sonnenhöhe: ca. 18:15 MEZ und 05:45 MEZ)
plt.axvline(x=-5.75, color='black', linewidth=1.8)
plt.axvline(x=5.75, color='black', linewidth=1.8)

# Horizontale Orientierungslinie (30° Minima)
plt.axhline(y=30, color='gray', linestyle='-', linewidth=0.8, alpha=0.7)

# Achsenformatierung analog zum Referenzplot
plt.ylim(20, 95)
plt.xlim(-12, 12)
plt.xlabel('Local Time [h]', fontsize=13)
plt.ylabel('ALT [deg]', fontsize=13)
plt.title('Nebel & Sternhaufen – 19.11.2026 (München)', fontsize=15, pad=12)

plt.minorticks_on()
plt.tick_params(which='major', length=7, direction='in', top=True, right=True)
plt.tick_params(which='minor', length=3.5, direction='in', top=True, right=True)
plt.grid(True, which='both', linestyle=':', alpha=0.35)

plt.tight_layout()
plt.savefig('Altitude_Plot_19_11_26.png', dpi=300)
plt.show()