import csv
import numpy as np
from calculate_cp import load_cp_table, get_cp 
import parameter as p

def compute_P_Wv_in1(v, rho, R, omega_in0, cp_table):
    """
    Berechnet die theoretische Basisleistung P_Wv_in1 (in Watt) für eine gegebene Windgeschwindigkeit v.
    P_Wv_in1 = 0.5 * rho * π * R² * v³ * CP,
    wobei CP über λ = (omega_in0 * R)/v interpoliert wird.
    """
    if v <= 0:
        return 0.0
    lambda_val = (p.omega_in0 * p.R) / v
    cp_val = get_cp(lambda_val, cp_table)
    P_Wv_in1 = 0.5 * p.rho * np.pi * p.R**2 * (v**3) * cp_val
    return P_Wv_in1

def compute_P_b(rho, R, v_in0, omega_in0, cp_table):
    """
    Berechnet den Referenzwert P_b (in Watt) bei einer festen Windgeschwindigkeit v_in0.
    Es gilt: 
      P_b = 0.5 * rho * π * R^2 * v_in0^3 * CP,
    wobei CP über die Interpolation berechnet wird:
      lambda_ref = (omega_in0 * R) / v_in0.
    """
    lambda_ref = (p.omega_in0 * p.R) / p.v_in0
    cp_val = get_cp(lambda_ref, cp_table)
    P_b = 0.5 * p.rho * np.pi * p.R**2 * (p.v_in0**3) * cp_val
    return P_b

def compute_P_ref(v, rho, R, omega_in0, cp_p_ref):
    """
    Berechnet die Referenzleistung P_ref (in Watt) für die Anlage ohne Motorunterstützung.
    Gibt 0 zurück, falls v unterhalb der Einschaltgeschwindigkeit liegt.
    """
    if v < p.v_in0:
        return 0.0
    lambda_ref = (p.omega_in0 * p.R) / v
    cp_val = get_cp(lambda_ref, cp_p_ref)
    P_ref = 0.5 * p.rho * np.pi * p.R**2 * v**3 * cp_val
    return P_ref



