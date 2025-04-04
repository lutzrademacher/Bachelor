Bachelorarbeit – Berechnung der Leistungsabgabe von Windkraftanlagen

Dieses Repository enthält Python-Skripte zur Berechnung und Analyse verschiedener Aspekte der Leistungsabgabe von Windkraftanlagen im Zusammenhang mit der Bachelorarbeit "Vergleich einer motorunterstützten Stall-regulierten Windkraftanlage mit einer Pitch-regulierten Windkraftanlage"

Skripte und Funktionen:


parameter.py 

Festlegung der Parameter für folgende Berechnungen. v_in1 über v_in1min_calculation.py bestimmen.


v_inmin_calculation.py

Berechnet die minimale effektive Einschaltgeschwindigkeit (Cut-in Speed) für die Anlage.


calculate_cp.py

Berechnet den Leistungsbeiwerts abhängig von verschiedenen Parametern der Windkraftanlage. Es muss eine .csv Datei mit den Leistungsbeiwerten in Abhängigkeit von den TSR und eine in Abhängigkeit von der Windgeschwindigkeit (z.B. mittels QBlade erstellen) im Arbeitsarchiv exisiteren.


P_W_vin1_P_b.py

Berechnet die abgegebene Leistung der Windkraftanlagen basierend auf variierenden Betriebsparametern.


motor_power.py

Ermittelt die benötigte Motorleistung zur Unterstützung der Anlage, abhängig von Windbedingungen und Anlagenparametern.


Leistungsanteile_berechnung.py

Führt eine Berechnung der Leistungsanteile von Motorleistung und Windkraft einer Windturbine bei unterschiedlichen Windgeschwindigkeiten durch.


windspeed_function.py

Berechnet die Leistungsabgabe der Windkraftanlage mit Motorunterstützung und ohne Motorunterstützung basierend auf einer Funktion zur Windgeschwindigkeitsverteilung.


tsr_cp.csv

Die für die Berechnungen genutzten Leistungsbeiwerte in Abhängigkeit von dem TSR 


v_cp.csv

Die für die Berechnungen genutzten Leistungsbeiwerte in Abhängigkeit von der Windgeschwindigkeit  


Begriffserklärung:

P_b = Leistungsabgabe der Windkraftanlage bei ursprünglicher Einschaltgeschwindigkeit

P_ref = Leistungsabgabe der Referrenzanlage 

P_W(v_in1) = Leistungsabgabe der Windkraftanlage mit optimierter Einschaltgeschwindigkeit

PAM = Leistungsabgabe des Motors 




