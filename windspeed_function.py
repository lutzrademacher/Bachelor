import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import trapezoid
from motor_power import compute_PAM
from calculate_cp import load_cp_table_v, load_cp_table_lambda
from P_W_vin1_P_b import compute_P_Wv_in1, compute_P_bmin, compute_P_ref, compute_P_Wv_inmin
import parameter as p


# 1.1 CP-Tabelle laden
cp_table_for_P_Wv_in1 = load_cp_table_v('v_cp.csv') # Name der .csv für die Leistungsbeiwerte der Stall-Anlage

# 1.2 Zweite CP-Tabelle laden
cp_table_for_P_ref = load_cp_table_v('v_cp.csv') # Name der .csv Datei füt die Leistungskoeffizienten der Pitch-Anlage

cp_table_for_lambda = load_cp_table_lambda('tsr_cp.csv')

# 2. Fester Referenzwert P_b (in Watt) für v = 3 m/s berechnen
P_b = compute_P_bmin(p.rho, p.R, p.v_in0, cp_table_for_P_ref)
print("Referenzleistung P_b (bei 3 m/s): {:.2f} kW".format(P_b / 1000))

# 3. Windgeschwindigkeitsverteilung definieren (z.B. Sinusfunktion)
def wind_speed_formula(t, v_ref, v_amp, periode):
    return v_ref + v_amp * np.sin(2 * np.pi * t / periode)


# 4. Simulation: Zeitverlauf und variable Windgeschwindigkeiten
t = np.linspace(0, 3600, 3600)  # Zeit in Sekunden
wind_speeds = wind_speed_formula(t, v_ref=6.9, v_amp=4.5, periode=720)
wind_speeds = np.maximum(wind_speeds, 0)



"""
5. Für jeden Zeitpunkt: Berechne:
 - Operative Basisleistung P_W(v_in1):
     v < 2.40 m/s: P_W(v_in1) = 0 (Anlage aus)
     2.40 m/s ≤ v < 3 m/s: P_W(v_in1) = P_bmin (Anlage liefert Referenzleistung)
     v ≥ 3 m/s: P_W(v_in1) = P_W(v_in1)
 - Motorleistung PAM: PAM = (P_bmin - P_W(vmin)/mu_M (in Watt)
 - Korrigierte Leistung: P_W(v_in1) - PAM (in Watt)
 - Referenzleistungskurve: 0 für v < 3 m/s, ansonsten P_ref (in kW)"
"""

base_power_op = []        # Operative Basisleistung P_W(v_in1) in kW
motor_power_list = []     # Motorleistung PAM in kW
corrected_power = []      # Korrigierte Leistung (P_W(v_in1) - PAM) in kW
P_ref = []                # Leistungsababe Referenzanlage

for v in wind_speeds:
    P_Wv_in1 = compute_P_Wv_in1(v, p.rho, p.R, cp_table_for_P_Wv_in1)  # in Watt
    P_Wv_inmin = compute_P_Wv_inmin(v, p.rho, p.R, p.omega_in0, cp_table_for_lambda)
    P_bmin = compute_P_bmin(p.rho, p.R, p.v_in0, cp_table_for_P_ref)

    if v < p.v_off:
        PAW_op = 0.0
        PAM = 0.0
        ref_val = 0.0
    elif v < p.v_in0:
        PAW_op = P_bmin
        PAM = compute_PAM(P_Wv_inmin, P_bmin, p.eta_M)
        ref_val = 0.0
    else:
        PAW_op = P_Wv_in1
        PAM = compute_PAM(P_Wv_inmin, P_bmin, p.eta_M)
        ref_val = P_Wv_in1
    if v < p.v_in0:
        P_ref_val = 0.0
    else:
        P_ref_val = compute_P_ref(v, p.rho, p.R, cp_table_for_P_ref)

    base_power_op.append(PAW_op / 1000)         # in kW
    motor_power_list.append(PAM / 1000)         # in kW
    corrected_power.append((PAW_op - PAM) / 1000) # in kW
    P_ref.append(ref_val / 1000)            # in kW

# 6. Integrierte Energie (über den Zeitraum) für jede Kurve in kWh
energy_op = np.trapezoid(base_power_op, t) / 3600
energy_motor = np.trapezoid(motor_power_list, t) / 3600
energy_corr = np.trapezoid(corrected_power, t) / 3600
energy_ref = np.trapezoid(P_ref, t) / 3600

print("Gesamte Energie E_op(P_Wv_in1) mit Motoruntersützung): {:.2f} kWh".format(energy_op))
print("Gesamte Energie E_M(Motorleistung PAM): {:.2f} kWh".format(energy_motor))
print("Gesamte Energie E_korr(P_Wv_in1 - PAM): {:.2f} kWh".format(energy_corr))
print("Gesamte Energie E_ref(P_ref): {:.2f} kWh".format(energy_ref))

# Grafik 1: Obere Hälfte: Operative Basisleistung (PAW_op) und Motorleistung (PAM),
# untere Hälfte: Windgeschwindigkeit.
fig1 = plt.figure(figsize=(10, 6))
gs1 = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
ax1_upper = fig1.add_subplot(gs1[0])
ax1_lower = fig1.add_subplot(gs1[1], sharex=ax1_upper)

# Obere Achse in Grafik 1: Nur Linien (ohne Marker)
ax1_upper.plot(t, base_power_op, color='cyan', linestyle='-.', label="P_W(v_in1) (kW)")
ax1_upper.plot(t, motor_power_list, color='magenta', linestyle=':', label="PAM (kW)")
ax1_upper.set_ylabel("Leistung (kW)")
ax1_upper.legend(loc="upper right")
plt.setp(ax1_upper.get_xticklabels(), visible=False)
# Textannotation: Integrierte Energie für PAW_op und PAM
ax1_upper.text(0.00, 1.05, f"Energieabgabe: P_W(v_in1) * 1h: {energy_op:.2f} kWh\nEnergieabgabe: PAM * 1h: {energy_motor:.2f} kWh",
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
ax2_upper.plot(t, corrected_power, color='green', linestyle='--', label="Nettoleistung P_W(v_in1) - PAM (kW)")
ax2_upper.plot(t, P_ref, color='black', linestyle=':', label="Referenzleistung P_ref (kW)")
ax2_upper.set_ylabel("Leistung (kW)")
ax2_upper.legend(loc="upper right")
plt.setp(ax2_upper.get_xticklabels(), visible=False)
# Textannotation: Integrierte Energie für korrigierte und Referenzleistung
ax2_upper.text(0.00, 1.05, f"Energieabgabe: (P_W(v_in1) - PAM) * 1h: {energy_corr:.2f} kWh\nEnergieabgabe: P_ref * 1h: {energy_ref:.2f} kWh",
               transform=ax2_upper.transAxes, fontsize=12, bbox=dict(facecolor='wheat', alpha=0.5))

# Untere Achse in Grafik 2: Windgeschwindigkeit
ax2_lower.plot(t, wind_speeds, color='blue', linestyle='-', label="Windgeschwindigkeit (m/s)")
ax2_lower.set_xlabel("Zeit (s)")
ax2_lower.set_ylabel("Windgeschwindigkeit (m/s)")
ax2_lower.legend(loc="upper right")


# Beide Grafiken anzeigen
plt.show()
