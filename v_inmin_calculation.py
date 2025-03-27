import csv
import numpy as np
import parameter as p
from calculate_cp import load_cp_table_lambda, get_cp_lambda


# Laden der Cp-Tabelle
cp_table_for_P_Wvin1 = load_cp_table_lambda('tsr_cp.csv')  # Ersetzen Sie 'cp_values.csv' durch den tatsächlichen Dateinamen


# Berechnung von lambda_0 und Cp0
lambda_0 = (p.R * p.omega_in0) / p.v_in0
Cp0 = get_cp_lambda(lambda_0, cp_table_for_P_Wvin1)

# Initialisierung
v_in1 = p.v_in0  # Startwert für v_in1
toleranz = 1e-6
max_iterationen = 1000

# Iterative Berechnung
for iteration in range(max_iterationen):
    # Berechnung von lambda_1 basierend auf v_in1
    lambda_1 = (p.R * p.omega_in0) / v_in1

    # Berechnung von Cp1 für lambda_1
    Cp1 = get_cp_lambda(lambda_1, cp_table_for_P_Wvin1)

    # Berechnung von v_in1_min
    v_in1_min = ((Cp0 / ((p.eta_M + 1) * Cp1)) ** (1/3)) * p.v_in0

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
