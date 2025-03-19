import numpy as np
import matplotlib.pyplot as plt
from motor_power_2 import compute_PAM
from calculate_cp import load_cp_table, get_cp
from P_W_vin1_P_b import compute_P_b, compute_P_Wv_in1

# Parameter definieren
rho = 1.225           # Luftdichte in kg/m³
R = 63                # Rotorradius in m 
omega_in0 = 0.72       # Eingangs-Drehzahl 
mu_M = 0.95           # Motoreffizienz
v_ref = 3             #Referenzgeschwnidigkeit v_ref
cp_table_path = "tsr_cp.csv"  # Pfad zur CP-Tabelle (anpassen!)


# CP-Tabelle laden
cp_table = load_cp_table(cp_table_path)





# Lineare Verteilung der Windgeschwindigkeiten von 2.4 m/s bis 3.0 m/s
wind_speeds = np.linspace(2.4, 3.0, num=50)


# 2. Fester Referenzwert P_b (in Watt) für v_ref = 3 m/s berechnen
P_b = compute_P_b(rho, R, v_ref, omega_in0, cp_table)
print("Referenzleistung P_b (bei 3 m/s): {:.2f} kW".format(P_b / 1000))


# Berechnung der Leistungswerte
P_Wv_in1_values = [compute_P_Wv_in1(v, rho, R, omega_in0, cp_table) for v in wind_speeds]
# Annahme: compute_PAM nimmt hier als einziges Argument die Windgeschwindigkeit v entgegen.
PAM_values = [compute_PAM(P_AW, P_b, mu_M) for P_AW in P_Wv_in1_values]


# Ergebnisse plotten
plt.figure(figsize=(8,6))
plt.plot(wind_speeds, P_Wv_in1_values, label="P_W(v_in1)", marker='o')
plt.plot(wind_speeds, PAM_values, label="PAM", marker='x')
plt.xlabel("Windgeschwindigkeit (m/s)")
plt.ylabel("Leistung (W)")
plt.legend()
plt.grid(True)
plt.show()
