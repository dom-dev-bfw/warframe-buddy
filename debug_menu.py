import os
import time
from pathlib import Path

local_app_data = os.getenv("LOCALAPPDATA")
log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

print("========================================")
print("      MENÜ-DETEKTIV GESTARTET           ")
print("========================================")
print("Gehe jetzt im Spiel an die SCHMIEDE oder öffne das Menü...")
print("Beenden mit Strg + C\n")

with open(log_pfad, "r", encoding="utf-8", errors="ignore") as datei:
    # Geh ans Ende der Datei
    datei.seek(0, os.SEEK_END)
    
    try:
        while True:
            zeile = datei.readline()
            if zeile:
                text = zeile.strip()
                # Wir suchen nach allen Benutzeroberflächen (.swf) oder Menü-Events
                if ".swf" in text.lower() or "menu" in text.lower() or "foundry" in text.lower() or "craft" in text.lower():
                    print(f"[GEFUNDEN]: {text}")
            else:
                time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nDetektiv beendet.")