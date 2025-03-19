import csv
import numpy as np
from calculate_cp import load_cp_table, get_cp
from P_W_vin1_P_b import compute_P_b, compute_P_Wv_in1

# 1.1 CP-Tabelle laden
cp_table_for_P_Wvin1 = load_cp_table('tsr_cp.csv') # Name der .csv für die Leistungsbeiwerte der Stall-Anlage


def compute_PAM(P_AW, P_b, mu_M):
    """
    Berechnet den motorischen Leistungsbedarf PAM (in Watt) als Funktion der Differenz
    zwischen dem Referenzwert P_b (bei v_ref, z. B. 3 m/s) und der aktuellen Leistung PAW (P_AW).
    Falls P_AW unter P_b liegt, muss der Motor die Differenz liefern (aufgerechnet mit dem Wirkungsgrad).
    """
    if P_AW < P_b:
        return (P_b - P_AW) / mu_M
    else:
        return 0.0
    

