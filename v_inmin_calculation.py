import csv
import numpy as np
from calculate_cp import load_cp_table, get_cp



# Laden der CP-Tabelle
cp_table = load_cp_table('tsr_cp.csv')  # Ersetzen Sie 'cp_values.csv' durch den tatsächlichen Dateinamen

# Konstanten
v_in0 = 3.0  # Konstante Eingangswindgeschwindigkeit in m/s
beta = 0.0  # Pitch-Winkel in Grad (konstant)
eta_M = 0.95  # Mechanischer Wirkungsgrad (konstant)
R = 63.0  # Rotor-Radius in Metern (konstant)
omega_in0 = 0.72  # Rotationsgeschwindigkeit in rad/s (konstant)

# Berechnung von lambda_0 und Cp0
lambda_0 = (R * omega_in0) / v_in0
Cp0 = get_cp(lambda_0, cp_table)

# Initialisierung
v_in1 = v_in0  # Startwert für v_in1
toleranz = 1e-6
max_iterationen = 1000

# Iterative Berechnung
for iteration in range(max_iterationen):
    # Berechnung von lambda_1 basierend auf v_in1
    lambda_1 = (R * omega_in0) / v_in1

    # Berechnung von Cp1 für lambda_1
    Cp1 = get_cp(lambda_1, cp_table)

    # Berechnung von v_in1_min
    v_in1_min = ((Cp0 / ((eta_M + 1) * Cp1)) ** (1/3)) * v_in0

    # Überprüfen der Konvergenz
    if abs(v_in1_min - v_in1) < toleranz:
        print(f'Konvergenz erreicht nach {iteration + 1} Iterationen.')
        v_in1 = v_in1_min
        break

    # Aktualisieren von v_in1 für die nächste Iteration
    v_in1 = v_in1_min

else:
    print('Maximale Anzahl an Iterationen erreicht. Keine Konvergenz.')

print(f'Berechnete Windgeschwindigkeit v_in1: {v_in1:.6f} m/s')
