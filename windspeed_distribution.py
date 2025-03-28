import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd 
import parameter as p
from motor_power import compute_PAM
from calculate_cp import load_cp_table, get_cp
from P_W_vin1_P_b import compute_P_Wv_in1, compute_P_b


# 1. CP-Tabelle laden (für Berechnung von P_W)
cp_table_for_P_Wvin1 = load_cp_table('tsr_cp.csv')

# 1.2 Zweite CP-Tabelle laden
cp_table_for_P_ref = load_cp_table('tsr_cp.csv')

# 2. Fester Referenzwert P_b (in Watt) für v_in0 = 3 m/s berechnen
# Hier wird die zweite CP-Tabelle verwendet, sodass der cp-Wert für P_b anhand der zweiten Tabelle interpoliert wird.
P_b = compute_P_b(p.rho, p.R, p.v_in0, p.omega_in0, cp_table_for_P_ref)
print("Referenzleistung P_b (bei 3 m/s): {:.2f} kW".format(P_b / 1000))

# 3. Windgeschwindigkeitsverteilung definieren (statistische Verteilung)
def wind_speed_statistical(t, probs=[7.6, 13.4, 17.5, 17.8, 14.8, 11.0, 7.5, 4.6, 2.7, 1.5, 0.8]):
    n = len(t)
    # Hier 11 Intervalle (Beispielintervalle) – passe diese ggf. an deine Daten an
    intervals = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                 (6, 7), (7, 8), (8, 9), (9, 10), (10, 11)]
    norm_probs = np.array(probs) / np.sum(probs)
    ws = np.zeros(n)
    for i in range(n):
        idx = np.random.choice(len(intervals), p=norm_probs)
        a, b = intervals[idx]
        ws[i] = np.random.uniform(a, b)
    return ws



# 5. Simulation: 100-maliger Lauf mit statistischer Windgeschwindigkeitsverteilung
t = np.linspace(0, 3600, 1000)  # Zeit in Sekunden

# Listen, in denen die Zeitreihen aus allen Simulationen gespeichert werden
all_base_power_op = []      # Operative Leistung (P_W(vin1)) als Array pro Lauf (in kW)
all_motor_power_list = []   # Motorleistung (PAM) als Array pro Lauf (in kW)
all_corrected_power = []    # Korrigierte Leistung (P_W(vin1) - PAM) als Array pro Lauf (in kW)
all_ref_power = []          # Referenzleistung P_ref als Array pro Lauf (in kW)
all_wind_speeds = []        # Die in jedem Lauf generierten Windgeschwindigkeiten

# Neue Listen für integrierte Energien (als Skalarwerte pro Lauf)
all_energy_op = []      
all_energy_motor = []
all_energy_corr = []
all_energy_ref = []

n_runs = 100  # Anzahl der Simulationen
for run in range(n_runs):
    # Für jeden Simulationslauf wird ein eigener Windgeschwindigkeitsverlauf generiert.
    wind_speeds = wind_speed_statistical(t)  # Verwende die statistische Verteilung
    all_wind_speeds.append(wind_speeds)  # Speichern des Windgeschwindigkeitsarrays dieses Laufs
    
    # Initialisiere leere Listen für diesen Lauf (Zeitreihen)
    base_power_op = []     # Operative Leistung pro Zeitschritt
    motor_power_list = []  # Motorleistung pro Zeitschritt
    corrected_power = []   # Korrigierte Leistung pro Zeitschritt
    ref_power = []                # Leistungsababe Referenzanlage
    
    # Für jeden Zeitschritt (bzw. jeden Windgeschwindigkeitswert) werden die Leistungsgrößen berechnet
    for v in wind_speeds:
        # Berechnung von Lambda und Cp für den aktuellen Windwert
        if v > 0:
            lam = (p.omega_in0 * p.R) / v
            cp_val = get_cp(lam, cp_table_for_P_Wvin1)
        else:
            lam = 0.0
            cp_val = 0.0

        # Berechnung der theoretischen Basisleistung P_Wv_in1 (in Watt)
        P_Wv_in1 = compute_P_Wv_in1(v, p.rho, p.R, p.omega_in0, cp_table_for_P_Wvin1)
        
        """
5. Für jeden Zeitpunkt: Berechne:
 - Theoretische Basisleistung P_W(v_in1) (in Watt)
 - Operative Basisleistung P_W(v_in1):
     v < 2.40 m/s: P_W(v_in1) = 0 (Anlage aus)
     2.40 m/s ≤ v < 3 m/s: P_W(v_in1) = P_b (Anlage liefert Referenzleistung)
     v ≥ 3 m/s: P_W(v_in1) = P_W(v_in1)
 - Motorleistung PAM: PAM = (P_b - P_W(v_in1)/mu_M (in Watt)
 - Korrigierte Leistung: P_W(v_in1) - PAM (in Watt)
 - Referenzleistungskurve: 0 für v < 3 m/s, ansonsten P_ref (in kW)"
"""

        # Bestimmen der operativen Leistung und weiterer Größen abhängig von v
        if v < p.v_off:
            PAW_op = 0.0
            PAM = 0.0
            ref_val = 0.0
        elif v < p.v_in0:
            PAW_op = P_b
            PAM = compute_PAM(P_Wv_in1, P_b, p.eta_M)
            ref_val = 0.0
        else:
            PAW_op = P_Wv_in1
            PAM = compute_PAM(P_Wv_in1, P_b, p.eta_M)
            ref_val = P_Wv_in1

        # Umwandeln in kW und speichern
        base_power_op.append(PAW_op / 1000)
        motor_power_list.append(PAM / 1000)
        corrected_power.append((PAW_op - PAM) / 1000)
        ref_power.append(ref_val / 1000)
    
    # Speichern der Zeitreihen dieses Laufs (als NumPy-Array) in den globalen Listen
    all_base_power_op.append(np.array(base_power_op))
    all_motor_power_list.append(np.array(motor_power_list))
    all_corrected_power.append(np.array(corrected_power))
    all_ref_power.append(np.array(ref_power))
    
    # 7. Integrierte Energie (über den Zeitraum) für diesen Lauf in kWh berechnen
    energy_op = np.trapz(base_power_op, t) / 3600
    energy_motor = np.trapz(motor_power_list, t) / 3600
    energy_corr = np.trapz(corrected_power, t) / 3600
    energy_ref = np.trapz(ref_power, t) / 3600
    
    # Integrierte Energien in separaten Listen speichern (als Skalarwerte)
    all_energy_op.append(energy_op)
    all_energy_motor.append(energy_motor)
    all_energy_corr.append(energy_corr)
    all_energy_ref.append(energy_ref)

# Mittelwerte der integrierten Energien über alle Simulationen berechnen
mean_energy_op = np.mean(all_energy_op)
mean_energy_motor = np.mean(all_energy_motor)
mean_energy_corr = np.mean(all_energy_corr)
mean_energy_ref = np.mean(all_energy_ref)

print("Mittlere Energie (operative Basisleistung PAW_op): {:.2f} kWh".format(mean_energy_op))
print("Mittlere Energie (Motorleistung PAM): {:.2f} kWh".format(mean_energy_motor))
print("Mittlere Energie (korrigierte Leistung PAW_op - PAM): {:.2f} kWh".format(mean_energy_corr))
print("Mittlere Energie (Referenzleistung, v>=3 m/s): {:.2f} kWh".format(mean_energy_ref))

# Berechnung der durchschnittlichen Zeitreihen über alle Simulationen
avg_base_power_op    = np.mean(np.array(all_base_power_op), axis=0)
avg_motor_power_list = np.mean(np.array(all_motor_power_list), axis=0)
avg_corrected_power  = np.mean(np.array(all_corrected_power), axis=0)
avg_ref_curve        = np.mean(np.array(all_ref_power), axis=0)
avg_wind_speeds      = np.mean(np.array(all_wind_speeds), axis=0)

# ---- Grafik 1: Operative Leistung und Motorleistung + Windgeschwindigkeit ----
fig1 = plt.figure(figsize=(10, 6))
gs1 = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
ax1_upper = fig1.add_subplot(gs1[0])
# Plot der durchschnittlichen operativen Leistung und Motorleistung
ax1_upper.plot(t, avg_base_power_op, color='cyan', linestyle='-.', label="P_W(vin1) inklusive PAM (kW)")
ax1_upper.plot(t, avg_motor_power_list, color='magenta', linestyle=':', label="Motorleistung PAM (kW)")
ax1_upper.set_ylabel("Leistung (kW)")
ax1_upper.legend(loc="upper right")
plt.setp(ax1_upper.get_xticklabels(), visible=False)
# Textannotation mit den integrierten Energiewerten (Durchschnittswerte)
ax1_upper.text(0.05, 0.90, f"Energie PAW_op: {mean_energy_op:.2f} kWh\nEnergie PAM: {mean_energy_motor:.2f} kWh",
               transform=ax1_upper.transAxes, fontsize=12, bbox=dict(facecolor='wheat', alpha=0.5))

ax1_lower = fig1.add_subplot(gs1[1], sharex=ax1_upper)
ax1_lower.plot(t, avg_wind_speeds, color='blue', linestyle='-', label="Windgeschwindigkeit (m/s)")
ax1_lower.set_xlabel("Zeit (s)")
ax1_lower.set_ylabel("Windgeschwindigkeit (m/s)")
ax1_lower.legend(loc="upper right")

plt.tight_layout()

# ---- Grafik 2: Korrigierte Leistung und Referenzleistung + Windgeschwindigkeit ----
fig2 = plt.figure(figsize=(10, 6))
gs2 = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
ax2_upper = fig2.add_subplot(gs2[0])
ax2_upper.plot(t, avg_corrected_power, color='green', linestyle='--', label="Nettoeistung (P_W(vin1) - PAM) (kW)")
ax2_upper.plot(t, avg_ref_curve, color='black', linestyle=':', label="Referenzleistung P_ref (kW)")
ax2_upper.set_ylabel("Leistung (kW)")
ax2_upper.legend(loc="upper right")
plt.setp(ax2_upper.get_xticklabels(), visible=False)
ax2_upper.text(0.05, 0.90, f"Energie korr.: {mean_energy_corr:.2f} kWh\nEnergie Ref: {mean_energy_ref:.2f} kWh",
               transform=ax2_upper.transAxes, fontsize=12, bbox=dict(facecolor='wheat', alpha=0.5))

ax2_lower = fig2.add_subplot(gs2[1], sharex=ax2_upper)
ax2_lower.plot(t, avg_wind_speeds, color='blue', linestyle='-', label="Windgeschwindigkeit (m/s)")
ax2_lower.set_xlabel("Zeit (s)")
ax2_lower.set_ylabel("Windgeschwindigkeit (m/s)")
ax2_lower.legend(loc="upper right")

plt.tight_layout()

plt.show()
