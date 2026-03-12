import matplotlib.pyplot as plt
import numpy as np

# Daten für das Diagramm
categories = ['Beobachtung (Kosmologie)', 'Theorie (QFT)']
# Logarithmus (Basis 10) der Dichten in kg/m^3
# Beobachtung: ~10^-26 kg/m^3 -> log10 = -26
# Theorie: ~10^96 kg/m^3 -> log10 = 96
densities_log10 = [-26, 96]

# Farben für die Balken
colors = ['#4CAF50', '#F44336'] # Grün für Beobachtung, Rot für Theorie

# Erstellen des Balkendiagramms
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, densities_log10, color=colors)

# Achsenbeschriftungen und Titel
ax.set_ylabel('Dichte (log10(kg/m³))', fontsize=14)
ax.set_title('Vergleich: Beobachtete vs. Theoretische Vakuumenergiedichte', fontsize=16, fontweight='bold')

# Y-Achse logarithmisch darstellen, aber die Skala linear lassen, da wir bereits log-Werte plotten.
# Die logarithmische Natur wird durch die Werte (-26 bis 96) und die Achsenbeschriftung deutlich.
# Eine "echte" logarithmische Achse mit Werten wie 10^-26 und 10^96 würde bei einem Balkendiagramm
# mit negativen Werten nicht gut funktionieren. Daher plotten wir die Exponenten.

# Beschriftung der Balken mit den Werten
for bar, value in zip(bars, densities_log10):
    height = bar.get_height()
    label = f'$10^{{{value}}}$\nkg/m³'
    if value < 0:
        va = 'top' # Text unterhalb des Balkens für negative Werte
        y_pos = height - 5 # Kleiner Abstand
    else:
        va = 'bottom' # Text oberhalb des Balkens für positive Werte
        y_pos = height + 5 # Kleiner Abstand
    ax.text(bar.get_x() + bar.get_width() / 2, y_pos, label,
            ha='center', va=va, fontsize=12, fontweight='bold')

# Hervorhebung der Diskrepanz
discrepancy = densities_log10[1] - densities_log10[0] # 96 - (-26) = 122
ax.annotate(f'Diskrepanz: {discrepancy} Größenordnungen ($10^{{{discrepancy}}}$)',
            xy=(0.5, 0.5), xycoords='axes fraction',
            ha='center', va='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=2))

# Null-Linie für die Energie einzeichnen (entspricht log10(1) = 0)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')

# Layout verbessern
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Speichern des Diagramms als Bild
plt.savefig('vakuumenergie_diskrepanz.png', dpi=300, bbox_inches='tight')

# Anzeigen des Diagramms
plt.show()