import os
from pathlib import Path

# Pfad zur Logdatei
local_app_data = os.getenv("LOCALAPPDATA")
log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

# Wonach wollen wir suchen?
# Wir testen zuerst, ob wir Einträge zum Dojo oder zur Schmiede (Foundry) finden!
SUCHBEGRIFF = "Dojo"

print(f"--- Suche nach '{SUCHBEGRIFF}' in EE.log ---")

treffer_anzahl = 0

with open(log_pfad, "r", encoding="utf-8", errors="ignore") as datei:
    for zeilennummer, zeile in enumerate(datei, start=1):
        # case-insensitive Suche: .lower() wandelt alles in Kleinbuchstaben um,
        # damit "dojo", "Dojo" und "DOJO" gleichermaßen gefunden werden.
        if SUCHBEGRIFF.lower() in zeile.lower():
            treffer_anzahl += 1
            # Wir zeigen die Zeilennummer und die Zeile an (maximal 5 Treffer für den Überblick)
            if treffer_anzahl <= 5:
                print(f"[Zeile {zeilennummer}] {zeile.strip()}")

print("------------------------------------------")
print(f"Suche abgeschlossen. Insgesamt {treffer_anzahl} Treffer gefunden.")