import os
import time
from pathlib import Path

# Pfad zur Warframe-Logdatei
local_app_data = os.getenv("LOCALAPPDATA")
log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

print("========================================")
print("   WARFRAME BUDDY: LIVE-MONITOR GESTARTET")
print("========================================")
print("Lausche am Ende der Log-Datei auf neue Events...")
print("Zum Beenden druecke im Terminal einfach: Strg + C\n")

# Datei im Lesemodus oeffnen
with open(log_pfad, "r", encoding="utf-8", errors="ignore") as datei:
    # 1. Springe direkt an das Dateiende (0 Bytes vor dem Ende)
    # os.SEEK_END bedeutet: Geh ganz nach hinten!
    datei.seek(0, os.SEEK_END)

    try:
        while True:
            # Versuche eine neue Zeile zu lesen
            neue_zeile = datei.readline()
            
            if neue_zeile:
                text = neue_zeile.strip()
                
                # Filter: Hier filtern wir spannende Ereignisse heraus!
                # Wir suchen nach typischen Begriffen wie Dojo, Mission, Chat, Foundry etc.
                schluesselwoerter = ["dojo", "foundry", "recipe", "squad", "loading", "mission"]
                
                # Wenn irgendein Schluesselwort in der neuen Zeile steckt:
                if any(wort in text.lower() for wort in schluesselwoerter):
                    print(f"[LIVE-EVENT]: {text}")
            else:
                # Keine neue Zeile? Warte 0.5 Sekunden, bevor du wieder nachschaust
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        # Fängt das "Strg + C" ab, damit kein haesslicher Python-Fehler geworfen wird
        print("\nLive-Monitor sauber beendet. Auf Wiedersehen, Tenno!")