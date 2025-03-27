import csv
import numpy as np
from calculate_cp import load_cp_table_lambda
from P_W_vin1_P_b import compute_P_bmin, compute_P_Wv_inmin

# 1.1 CP-Tabelle laden
cp_table_for_P_Wvin1 = load_cp_table_lambda('tsr_cp.csv') # Name der .csv für die Leistungsbeiwerte der Stall-Anlage


def compute_PAM(P_Wv_inmin, P_bmin, mu_M):
    """
    Berechnet den motorischen Leistungsbedarf PAM (in Watt) als Funktion der Differenz
    zwischen dem Referenzwert P_b (bei v_in0, z. B. 3 m/s) und der aktuellen Leistung PAW (P_AW).
    Falls P_AW unter P_b liegt, muss der Motor die Differenz liefern (aufgerechnet mit dem Wirkungsgrad).
    """
    if P_Wv_inmin < P_bmin:
        return (P_bmin - P_Wv_inmin) / mu_M
    else:
        return 0.0
    

