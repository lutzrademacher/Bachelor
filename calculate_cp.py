import csv
import numpy as np

"Für den Leistungsbeiwert in Abhängigkeit von der Windgeschwindigkeit"

def load_cp_table_v(csv_file):
    """
    Lädt die CP-Tabelle aus einer CSV-Datei mithilfe von csv.DictReader.
    Erwartet wird, dass die CSV-Datei mindestens die Spalten 'v' und 'cp' enthält.
    Die Reihenfolge der Einträge wird beibehalten.
    """
    table = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            try:
                table.append({
                    "v": float(row.get("v")),
                    "cp": float(row.get("cp"))
                })
            except ValueError:
                print("Fehler bei der Umwandlung:", row)
    return table

def get_cp_v(v_val, cp_table):
    """
    Ermittelt den CP-Wert für einen gegebenen v-Wert mittels linearer Interpolation.
    Falls die v-Werte in absteigender Reihenfolge vorliegen, werden sie umgekehrt.
    """
    vs = [row["v"] for row in cp_table]
    cp1 = [row["cp"] for row in cp_table]
    
    # Überprüfe, ob die v-Werte absteigend sind und kehre sie gegebenenfalls um
    if vs[0] > vs[-1]:
        vs = vs[::-1]
        cp1 = cp1[::-1]
    
    # Interpolation des CP-Werts
    cp_interpolated = np.interp(v_val, vs, cp1)
        
    # Debug-Ausgabe – kann entfernt werden
    print("v_val:", v_val, "Cp_v_val:", cp_interpolated)
    
    
    return cp_interpolated


"Für den Leistungsbeiwert in Abhängigkeit von lambda"

def load_cp_table_lambda(csv_file):
    """
    Lädt die CP-Tabelle aus einer CSV-Datei mithilfe von csv.DictReader.
    Erwartet wird, dass die CSV-Datei mindestens die Spalten 'lambda' und 'cp' enthält.
    Die Reihenfolge der Einträge wird beibehalten.
    """
    table = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            try:
                table.append({
                    "lambda": float(row.get("lambda")),
                    "cp": float(row.get("cp"))
                })
            except ValueError:
                print("Fehler bei der Umwandlung:", row)
    return table

def get_cp_lambda(lambda_val, cp_table):
    """
    Ermittelt den CP-Wert für einen gegebenen lambda-Wert mittels linearer Interpolation.
    Falls die Lambda-Werte in absteigender Reihenfolge vorliegen, werden sie umgekehrt.
    """
    lambdas = [row["lambda"] for row in cp_table]
    cps = [row["cp"] for row in cp_table]
    
    # Überprüfe, ob die Lambda-Werte absteigend sind und kehre sie gegebenenfalls um
    if lambdas[0] > lambdas[-1]:
        lambdas = lambdas[::-1]
        cps = cps[::-1]
    
    # Interpolation des CP-Werts
    cp_interpolated2 = np.interp(lambda_val, lambdas, cps)
    
    # Runde den interpolierten CP-Wert auf 2 Dezimalstellen
    cp_interpolated = round(cp_interpolated2, 2)
    
    # Debug-Ausgabe – kann entfernt werden
    print("lambda_val:", lambda_val, "Cp_lambda:", cp_interpolated2)
    
    return cp_interpolated2

