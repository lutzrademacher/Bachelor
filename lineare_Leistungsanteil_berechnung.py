import csv
import numpy as np
import matplotlib.pyplot as plt
import parameter as p
from calculate_cp import load_cp_table_lambda, load_cp_table_v
from motor_power import compute_PAM
from P_W_vin1_P_b import compute_P_bmin, compute_P_Wv_inmin


# TSR-CP-Tabelle laden
cp_table_for_P_Wvinmin = load_cp_table_lambda("tsr_cp.csv")

# v-CP-Tabelle laden 
cp_table_for_P_ref = load_cp_table_v("v_cp.csv")

# Lineare Verteilung der Windgeschwindigkeiten von 2.4 m/s bis 3.0 m/s
wind_speeds = np.linspace(2.4, 3.0, num=50)

"Berechnung der Anteile von Motorleistung und Windleistung nach Kapitel 4.5"

# 2. Fester Referenzwert P_b (in Watt) für v_in0 = 3 m/s berechnen
P_b = compute_P_bmin(p.rho, p.R, p.v_in0, cp_table_for_P_ref)
print("Referenzleistung P_b (bei 3 m/s): {:.2f} kW".format(P_b / 1000))

# Berechnung der Leistungswerte
P_Wv_inmin_values = [compute_P_Wv_inmin(v, p.rho, p.R, p.omega_in0, cp_table_for_P_Wvinmin) for v in wind_speeds]
# Annahme: compute_PAM nimmt hier als einziges Argument die Windgeschwindigkeit v entgegen.
PAM_values = [compute_PAM(P_AW, P_b, p.eta_M) for P_AW in P_Wv_inmin_values]

# Ergebnisse plotten
plt.figure(figsize=(8,6))
plt.plot(wind_speeds, P_Wv_inmin_values, label="P_W(v_inmin)", marker='o')
plt.plot(wind_speeds, PAM_values, label="PAM", marker='x')
plt.xlabel("Windgeschwindigkeit (m/s)")
plt.ylabel("Leistung (W)")
plt.legend()
plt.grid(True)
plt.show()
