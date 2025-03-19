Bachelorarbeit – Berechnung der Leistungsabgabe von Windkraftanlagen

Dieses Repository enthält Python-Skripte zur Berechnung und Analyse verschiedener Aspekte der Leistungsabgabe von Windkraftanlagen im Kontext der "Vergleich einer motorunterstützten Stall-regulierten WIndkraftanalge mit einer Pitch-regulierten Windkraftanlage bezüglich ihrer Leistugsabgabe"

Skripte und Funktionen:

parameter.py 

Festlegung der Parameter für folgende Berechnungen. v_in1 über v_in1min_calculation.py bestimmen.


v_inmin_calculation.py

Berechnet die minimale effektive Einschaltgeschwindigkeit (Cut-in Speed) für die Anlage.


calculate_cp.py

Berechnet den Leistungsbeiwerts abhängig von verschiedenen Parametern der Windkraftanlage. Es muss eine .csv Datei mit den Leistungsbeiwerten in Abhängigkeit von den TSR (z.B. mittels QBlade erstellen) im Arbeitsarchiv exisiteren.


P_W_vin1_P_b.py

Berechnet die abgegebene Leistung der Windkraftanlagen basierend auf variierenden Betriebsparametern.


motor_power.py

Ermittelt die benötigte Motorleistung zur Unterstützung der Anlage, abhängig von Windbedingungen und Anlagenparametern.


Leistungsanteile_berechnung.py

Führt eine Berechnung der Leistungsanteile von Motorleistung und Windkraft einer Windturbine bei unterschiedlichen Windgeschwindigkeiten durch.


windspeed_distribution.py

Berechnet die Leistungsabgabe der Windkraftanlage mit Motorunterstützung und ohne Motorunterstützung basierend auf eine Wahrschienlihckeitsverteilung der Windgeschwindigkeiten.


windspeed_function.py

Berechnet die Leistungsabgabe der Windkraftanlage mit Motorunterstützung und ohne Motorunterstützung basierend auf einer Funktion zur Windgeschwindigkeitsverteilung.


tsr_cp.csv

Die für die Berechnungen in der Abschlussarbeit genutzten Leistungsbeiwerte in Abhängigkeit von den TSR 

Begriffserklärung:

P_b = Leistungsabgabe der Windkraftanlage bei ursprünglicher Einschaltgeschwindigkeit

P_ref = Leistungsabgabe der Referrenzanlage 

P_W(v_in1) = Leistungsabgabe der Windkraftanlage mit optimierter Einschaltgeschwidigkeit

PAM = Leistungsabgabe des Motors 




