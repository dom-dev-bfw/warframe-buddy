import os
from pathlib import Path

# Pfad zur Logdatei bestimmen
local_app_data = os.getenv("LOCALAPPDATA")
log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

print("--- Warframe Buddy: Log-Inspektor ---")

# Wir öffnen die Datei sicher im Lesemodus
with open(log_pfad, "r", encoding="utf-8", errors="ignore") as datei:
    # Wir lesen Zeile für Zeile, hören aber nach 10 Zeilen auf
    for index, zeile in enumerate(datei):
        if index >= 10:
            break
        # .strip() schneidet überflüssige Leerzeilen am Ende ab
        print(f"Zeile {index + 1}: {zeile.strip()}")

print("--- Fertig! ---")