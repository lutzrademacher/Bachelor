# Parameter für die Berechnungen
v_ref = 3.0        # Bei v >= 3 m/s: Operative Leistung entspricht theoretischer Leistung, sonst P_b (oder 0)
v_in0 = 3.0        # urspürngliche Einschaltgeschwindigkeit 
v_off = 2.41       # Bei v < 2,40 m/s wird die Anlage nicht betrieben (PAW_op = 0)
rho = 1.225        # Luftdichte (kg/m³)
R = 63             # Turbinenradius (m)
omega_in0 = 0.72   # Eingangs-Drehzahl (rad/s)
eta_M = 0.95        # Wirkungsgrad des Motors
beta = 0.0  # Pitch-Winkel in Grad (konstant)
