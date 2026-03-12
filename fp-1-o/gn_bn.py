import numpy as np
import matplotlib.pyplot as plt

# Messdaten
g = np.array([23.65, 24.05, 24.75, 25.65, 28.55])
b = np.array([107.5, 100.6, 91.8, 80.2, 62.0])
err = 0.1  # Fehler für g und b in cm

# 1. Schnittpunkte aller Geradenkombinationen berechnen
intersections_x = []
intersections_y = []

# Kombinatorik für alle Paare (i, j)
for i in range(len(g)):
    for j in range(i+1, len(g)):
        # Geradengleichung y = m*x + c
        # Steigung m = -b/g, y-Achsenabschnitt c = b
        m1, c1 = -b[i]/g[i], b[i]
        m2, c2 = -b[j]/g[j], b[j]
        
        # Schnittpunkt x = (c2 - c1) / (m1 - m2)
        x_int = (c2 - c1) / (m1 - m2)
        y_int = m1 * x_int + c1
        
        intersections_x.append(x_int)
        intersections_y.append(y_int)

# Bereich der Brennweite aus den Schnittpunkten ermitteln
x_min, x_max = np.min(intersections_x), np.max(intersections_x)
y_min, y_max = np.min(intersections_y), np.max(intersections_y)

print(f"Bereich auf X-Achse: {x_min:.2f} cm bis {x_max:.2f} cm")
print(f"Bereich auf Y-Achse: {y_min:.2f} cm bis {y_max:.2f} cm")

# Analytische Berechnung der mittleren Brennweite f
f_einzeln = (g * b) / (g + b)
f_mean = np.mean(f_einzeln)
print(f"Mittlere berechnete Brennweite f: {f_mean:.2f} cm")

# 2. Plotting (Vollansicht und Vergrößerung)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

x_vals = np.linspace(0, 35, 400)

for i in range(len(g)):
    # Hauptgerade
    m = -b[i]/g[i]
    c = b[i]
    y_vals = m * x_vals + c
    
    # Fehlerbänder
    # Flachste Gerade: g maximal, b minimal
    m_min = -(b[i]-err)/(g[i]+err)
    c_min = b[i]-err
    y_vals_min = m_min * x_vals + c_min
    
    # Steilste Gerade: g minimal, b maximal
    m_max = -(b[i]+err)/(g[i]-err)
    c_max = b[i]+err
    y_vals_max = m_max * x_vals + c_max
    
    # Vollansicht
    ax1.plot(x_vals, y_vals, label=f'g={g[i]} cm, b={b[i]} cm')
    
    # Detailansicht
    ax2.plot(x_vals, y_vals)
    ax2.fill_between(x_vals, y_vals_min, y_vals_max, alpha=0.15) # Schattierung des Fehlers

# Formatierung Ax1: Vollansicht
ax1.set_xlim(0, 32)
ax1.set_ylim(0, 115)
ax1.set_xlabel('Gegenstandsweite g [cm]')
ax1.set_ylabel('Bildweite b [cm]')
ax1.set_title('Graphische Bestimmung der Brennweite (Vollansicht)')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# Formatierung Ax2: Detailansicht (Zoom)
zoom_margin = 1.0
ax2.set_xlim(x_min - zoom_margin, x_max + zoom_margin)
ax2.set_ylim(y_min - zoom_margin, y_max + zoom_margin)
ax2.set_xlabel('Gegenstandsweite g [cm]')
ax2.set_ylabel('Bildweite b [cm]')
ax2.set_title('Schnittpunktbereich inkl. Fehlerbänder')
ax2.grid(True, linestyle='--', alpha=0.7)

# Schnittpunkte einzeichnen
ax2.scatter(intersections_x, intersections_y, color='red', zorder=5, label='Schnittpunkte')
ax2.plot(f_mean, f_mean, marker='*', color='green', markersize=15, 
         zorder=6, label=f'Theor. Punkt (f,f) = ({f_mean:.2f}, {f_mean:.2f})')
ax2.legend()

plt.tight_layout()
plt.savefig('brennweite_graphisch.png', dpi=300)