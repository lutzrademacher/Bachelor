import csv
import numpy as np


def load_cp_table(csv_file):
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

def get_cp(lambda_val, cp_table):
    """
    Ermittelt den CP-Wert für einen gegebenen lambda-Wert mittels linearer Interpolation.
    Falls die Lambda-Werte in absteigender Reihenfolge vorliegen, werden sie umgekehrt.
    """
    lambdas = [row["lambda"] for row in cp_table]
    cps = [row["cp"] for row in cp_table]
    if lambdas[0] > lambdas[-1]:
        lambdas = lambdas[::-1]
        cps = cps[::-1]
    cp_interpolated = np.interp(lambda_val, lambdas, cps)
    # Debug-Ausgabe – kann entfernt werden:
    print("lambda_val:", lambda_val, "Interpolated CP:", cp_interpolated)
    return cp_interpolated