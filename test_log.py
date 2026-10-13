import os
from pathlib import Path

# 1. Wo liegt die Warframe-Logdatei auf Windows?
# in Windows gibt es die Umgebungsvariable LOCALAPPDATA (führt zu C:\Users\<DeinName\AppData\Local)
local_app_data = os.getenv("LOCALAPPDATA")

# 2. Den genauen Pfad zur EE.log zusammensetzen
log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

print("--- Warframe Buddy Scout ---")
print(f"Suche Log-Datei unter: {log_pfad}")

# 3. Prüfen, ob die Datei an diesem Ort wirklich existiert
if log_pfad.exists():
    groesse_in_kb = log_pfad.stat().st_size / 1024
    print(f"Gefunden! Die Datei ost aktuell {groesse_in_kb:.2f} KB groß.")
else:
    print("Datei nicht gefunden! Wurde Warframe auf diesem PC schon einmal gestartet?")