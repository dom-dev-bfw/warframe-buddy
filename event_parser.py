import os
import time
from pathlib import Path

# Pfad zur Warframe-Logdatei
local_app_data = os.getenv("LOCALAPPDATA")
log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

print("========================================")
print("   WARFRAME BUDDY: SMART PARSER AKTIV   ")
print("========================================")
print("Filtert jetzt relevante Ereignisse heraus...\n")

def parse_zeile(zeile: str):
    """
    Diese Funktion prueft eine einzelne Log-Zeile
    und gibt ein sauberes Ereignis zurueck, wenn etwas Wichtiges passiert ist.
    """
    # 1. Spielername erkennen
    if "AddSquadMember:" in zeile:
        # Schneidet den Namen nach 'AddSquadMember: ' heraus
        teile = zeile.split("AddSquadMember:")
        if len(teile) > 1:
            spieler_name = teile[1].split(",")[0].strip()
            return f"👤 Spieler erkannt: {spieler_name}"

    # 2. Betreten des Dojos
    if "InitiateDojoVisit()" in zeile:
        return "🏯 Betrete Clan-Dojo..."

    # 3. Forschungs-Terminal geoeffnet
    if "ResearchSelection.swf" in zeile:
        return "🔬 Forschungskonsole im Dojo geoeffnet!"

    # 4. Zurueck im Raumschiff (Orbiter)
    if "PlayerShip" in zeile and "finished loading resources" in zeile:
        return "🚀 Zurueck im Orbiter."

    # 5. Schmiede / Foundry Aktivitaet
    if "Foundry" in zeile and "Created" in zeile:
        return "🔨 Schmiede im Orbiter geoeffnet!"

    return None


# Hauptprogramm
with open(log_pfad, "r", encoding="utf-8", errors="ignore") as datei:
    datei.seek(0, os.SEEK_END)
    
    try:
        while True:
            zeile = datei.readline()
            if zeile:
                ereignis = parse_zeile(zeile)
                if ereignis:
                    timestamp = time.strftime("%H:%M:%S")
                    print(f"[{timestamp}] {ereignis}")
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nParser beendet.")