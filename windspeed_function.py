import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from motor_power import compute_PAM
from calculate_cp import load_cp_table, get_cp
from P_W_vin1_P_b import compute_P_Wv_in1, compute_P_b
import parameter as p


# 1.1 CP-Tabelle laden
cp_table_for_P_Wvin1 = load_cp_table('tsr_cp.csv') # Name der .csv für die Leistungsbeiwerte der Stall-Anlage

# 1.2 Zweite CP-Tabelle laden
cp_table_for_P_b = load_cp_table('tsr_cp.csv') # Name der .csv Datei füt die Leistungskoeffizienten der Pitch-Anlage

# 2. Fester Referenzwert P_b (in Watt) für v_ref = 3 m/s berechnen
P_b = compute_P_b(p.rho, p.R, p.v_ref, p.omega_in0, cp_table_for_P_b)
print("Referenzleistung P_b (bei 3 m/s): {:.2f} kW".format(P_b / 1000))

# 3. Windgeschwindigkeitsverteilung definieren (z.B. Sinusfunktion)
def wind_speed_formula(t, offset, amplitude, periode):
    return offset + amplitude * np.sin(2 * np.pi * t / periode)


# 4. Simulation: Zeitverlauf und variable Windgeschwindigkeiten
t = np.linspace(0, 3600, 3600)  # Zeit in Sekunden
wind_speeds = wind_speed_formula(t, offset=3.5, amplitude=2.0, periode=720)
wind_speeds = np.maximum(wind_speeds, 0)

"""
5. Für jeden Zeitpunkt: Berechne:
 - Theoretische Basisleistung P_Wv_in1(v_in1) (in Watt)
 - Operative Basisleistung P_Wv_in1(v_in1):
     v < 2.40 m/s: P_Wv_in1(v_in1) = 0 (Anlage aus)
     2.40 m/s ≤ v < 3 m/s: P_Wv_in1(v_in1) = P_b (Anlage liefert Referenzleistung)
     v ≥ 3 m/s: P_Wv_in1(v_in1) = P_Wv_in1(v_in1)
 - Motorleistung PAM: PAM = (P_b - P_Wv_in1v_in1)/mu_M (in Watt)
 - Korrigierte Leistung: P_Wv_in1(v_in1) - PAM (in Watt)
 - Referenzleistungskurve: 0 für v < 3 m/s, ansonsten P_Wv_in1v_in1 (in kW)"
"""

base_power_theo = []      # Theoretische Basisleistung P_Wv_in1(v_in1) in kW
base_power_op = []        # Operative Basisleistung P_Wv_in1v_in1 in kW
motor_power_list = []     # Motorleistung PAM in kW
corrected_power = []      # Korrigierte Leistung (P_Wv_in1(v_in1) - PAM) in kW
ref_curve = []            # Referenzleistungskurve: 0 für v < 3 m/s, sonst P_Wv_in1v_in1 (in kW)

for v in wind_speeds:
    P_Wv_in1v_in1 = compute_P_Wv_in1(v, p.rho, p.R, p.omega_in0, cp_table_for_P_Wvin1)  # in Watt
    if v < p.v_off:
        PAW_op = 0.0
        PAM = 0.0
        ref_val = 0.0
    elif v < p.v_ref:
        PAW_op = P_b
        PAM = compute_PAM(P_Wv_in1v_in1, P_b, p.eta_M)
        ref_val = 0.0
    else:
        PAW_op = P_Wv_in1v_in1
        PAM = compute_PAM(P_Wv_in1v_in1, P_b, p.eta_M)
        ref_val = P_Wv_in1v_in1
    base_power_theo.append(P_Wv_in1v_in1 / 1000)   # in kW
    base_power_op.append(PAW_op / 1000)         # in kW
    motor_power_list.append(PAM / 1000)         # in kW
    corrected_power.append((PAW_op - PAM) / 1000) # in kW
    ref_curve.append(ref_val / 1000)            # in kW

# 6. Integrierte Energie (über den Zeitraum) für jede Kurve in kWh
energy_op = np.trapz(base_power_op, t) / 3600
energy_motor = np.trapz(motor_power_list, t) / 3600
energy_corr = np.trapz(corrected_power, t) / 3600
energy_ref = np.trapz(ref_curve, t) / 3600

print("Gesamte Leistung (P_Wv_in1(vin1) mit Motoruntersützung): {:.2f} kWh".format(energy_op))
print("Gesamte Leistung (Motorleistung PAM): {:.2f} kWh".format(energy_motor))
print("Gesamte Leistung (P_Wv_in1(vin1) - PAM): {:.2f} kWh".format(energy_corr))
print("Gesamte Leistung (Pb, v>=3 m/s): {:.2f} kWh".format(energy_ref))

# Grafik 1: Obere Hälfte: Operative Basisleistung (PAW_op) und Motorleistung (PAM),
# untere Hälfte: Windgeschwindigkeit.
fig1 = plt.figure(figsize=(10, 6))
gs1 = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
ax1_upper = fig1.add_subplot(gs1[0])
ax1_lower = fig1.add_subplot(gs1[1], sharex=ax1_upper)

# Obere Achse in Grafik 1: Nur Linien (ohne Marker)
ax1_upper.plot(t, base_power_op, color='cyan', linestyle='-.', label="P_Wv_in1(v_in1) (kW)")
ax1_upper.plot(t, motor_power_list, color='magenta', linestyle=':', label="PAM (kW)")
ax1_upper.set_ylabel("Leistung (kW)")
ax1_upper.legend(loc="upper right")
plt.setp(ax1_upper.get_xticklabels(), visible=False)
# Textannotation: Integrierte Energie für PAW_op und PAM
ax1_upper.text(0.05, 0.90, f"P_Wv_in1(v_in1): {energy_op:.2f} kWh\nPAM: {energy_motor:.2f} kWh",
               transform=ax1_upper.transAxes, fontsize=12, bbox=dict(facecolor='wheat', alpha=0.5))

# Untere Achse in Grafik 1: Windgeschwindigkeit
ax1_lower.plot(t, wind_speeds, color='blue', linestyle='-', label="Windgeschwindigkeit (m/s)")
ax1_lower.set_xlabel("Zeit (s)")
ax1_lower.set_ylabel("Windgeschwindigkeit (m/s)")
ax1_lower.legend(loc="upper right")

plt.tight_layout()

# Grafik 2: Obere Hälfte: Korrigierte Leistung (PAW_op - PAM) und Referenzleistung (ref_curve),
# untere Hälfte: Windgeschwindigkeit.
fig2 = plt.figure(figsize=(10, 6))
gs2 = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
ax2_upper = fig2.add_subplot(gs2[0])
ax2_lower = fig2.add_subplot(gs2[1], sharex=ax2_upper)

# Obere Achse in Grafik 2: Nur Linien (ohne Marker)
ax2_upper.plot(t, corrected_power, color='green', linestyle='--', label="Nettoleistung P_Wv_in1(v_in1) - PAM (kW)")
ax2_upper.plot(t, ref_curve, color='black', linestyle=':', label="Vergleichsleistung P_b(v_in0) (kW)")
ax2_upper.set_ylabel("Leistung (kW)")
ax2_upper.legend(loc="upper right")
plt.setp(ax2_upper.get_xticklabels(), visible=False)
# Textannotation: Integrierte Energie für korrigierte und Referenzleistung
ax2_upper.text(0.05, 0.90, f"P_Wv_in1(v_in1) - PAM: {energy_corr:.2f} kWh\nP_b(v_in0): {energy_ref:.2f} kWh",
               transform=ax2_upper.transAxes, fontsize=12, bbox=dict(facecolor='wheat', alpha=0.5))

# Untere Achse in Grafik 2: Windgeschwindigkeit
ax2_lower.plot(t, wind_speeds, color='blue', linestyle='-', label="Windgeschwindigkeit (m/s)")
ax2_lower.set_xlabel("Zeit (s)")
ax2_lower.set_ylabel("Windgeschwindigkeit (m/s)")
ax2_lower.legend(loc="upper right")

plt.tight_layout()

# Beide Grafiken anzeigen
plt.show()
