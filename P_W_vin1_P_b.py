import csv
import numpy as np
from calculate_cp import load_cp_table, get_cp 

def compute_P_Wv_in1(v, rho, R, omega_in0, cp_table):
    """
    Berechnet die theoretische Basisleistung P_Wv_in1 (in Watt) für eine gegebene Windgeschwindigkeit v.
    P_Wv_in1 = 0.5 * rho * π * R² * v³ * CP,
    wobei CP über λ = (omega_in0 * R)/v interpoliert wird.
    """
    if v <= 0:
        return 0.0
    lambda_val = (omega_in0 * R) / v
    cp_val = get_cp(lambda_val, cp_table)
    P_Wv_in1 = 0.5 * rho * np.pi * R**2 * (v**3) * cp_val
    return P_Wv_in1

def compute_P_b(rho, R, v_ref, omega_in0, cp_table):
    """
    Berechnet den Referenzwert P_b (in Watt) bei einer festen Windgeschwindigkeit v_ref.
    Es gilt: 
      P_b = 0.5 * rho * π * R^2 * v_ref^3 * CP,
    wobei CP über die Interpolation berechnet wird:
      lambda_ref = (omega_in0 * R) / v_ref.
    """
    lambda_ref = (omega_in0 * R) / v_ref
    cp_val = get_cp(lambda_ref, cp_table)
    P_b = 0.5 * rho * np.pi * R**2 * (v_ref**3) * cp_val
    return P_b