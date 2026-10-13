import os
import re
import sys
import time
import requests
from datetime import datetime, timezone
from pathlib import Path
from supabase import create_client, Client

# ==========================================
# KONFIGURATION & CLOUD-VERBINDUNG
# ==========================================
SUPABASE_URL = "https://cvtdjitedrlfgzxkzjaj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2dGRqaXRlZHJsZmd6eGt6amFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA4NDk4NjYsImV4cCI6MjEwNjQyNTg2Nn0.i4VJ-7aLcoGCPiPUwQBwKzTQrccr6fFfY0fSSPFYyko"

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1555479757494157342/1D_qLZ8VQH3r7kZw4ipP9BcQzETcYp2gdRX0XZ5_qeby-oPkqIxVDUFd_WdDuuU8WMdU"
DASHBOARD_URL = "https://dom-dev-bfw.github.io/warframe-buddy/"

print("========================================")
print("     WARFRAME BUDDY: SYNC AGENT AKTIV   ")
print("========================================")

# 1. Lokalen Log-Pfad ermitteln
local_app_data = os.getenv("LOCALAPPDATA")
if not local_app_data:
    print("❌ Konnte LOCALAPPDATA-Verzeichnis nicht finden.")
    input("Drücke Enter zum Beenden...")
    sys.exit(1)

log_pfad = Path(local_app_data) / "Warframe" / "EE.log"

if not log_pfad.exists():
    print(f"⚠️ Warframe EE.log nicht gefunden unter: {log_pfad}")
    print("Hinweis: Warframe muss mindestens einmal auf diesem PC gestartet worden sein.")
    input("Drücke Enter zum Beenden...")
    sys.exit(1)

# Prozess-Check: Prüft, ob Warframe tatsächlich im Windows-Taskmanager läuft
def ist_warframe_aktiv() -> bool:
    try:
        output = os.popen('tasklist /FI "IMAGENAME eq Warframe.x64.exe" /NH').read()
        return "Warframe.x64.exe" in output
    except Exception:
        return True

# 2. Automatische Erkennung des Spielernamens aus dem Log
def ermittle_ingame_namen(log_datei_pfad) -> str:
    try:
        with open(log_datei_pfad, "r", encoding="utf-8", errors="ignore") as f:
            for zeile in f:
                m = re.search(r'setting owner player to\s+([a-zA-Z0-9_\-]+)', zeile, re.IGNORECASE)
                if m:
                    return m.group(1).strip()
                m2 = re.search(r'generated boosts for\s+([a-zA-Z0-9_\-]+)', zeile, re.IGNORECASE)
                if m2:
                    return m2.group(1).strip()
                m3 = re.search(r'nickname:\s*([a-zA-Z0-9_\-]+)', zeile, re.IGNORECASE)
                if m3:
                    return m3.group(1).strip()
    except Exception:
        pass
    return None

erkannter_name = ermittle_ingame_namen(log_pfad)

if erkannter_name:
    PLAYER_NAME = erkannter_name
    print(f"✓ Spielername automatisch aus EE.log erkannt: {PLAYER_NAME}\n")
else:
    print("⚠️ Spielername konnte nicht automatisch aus dem Log gelesen werden.")
    eingabe = input("Bitte Ingame-Namen eingeben (Enter für 'Nexes92'): ").strip()
    PLAYER_NAME = eingabe if eingabe else "Nexes92"
    print(f"✓ Verwende Namen: {PLAYER_NAME}\n")

# 3. Supabase Client starten
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Verbindung zur Supabase Cloud aktiv.")
except Exception as e:
    print(f"❌ Fehler bei Supabase-Verbindung: {e}")
    input("Drücke Enter zum Beenden...")
    sys.exit(1)

# 4. Discord Benachrichtigungs-Funktion
def sende_discord_meldung(titel: str, beschreibung: str, farbe: int = 0x00e5ff):
    if not DISCORD_WEBHOOK_URL or "HIER_" in DISCORD_WEBHOOK_URL:
        return

    payload = {
        "username": "Cephalon Ordis",
        "avatar_url": "https://static.wikia.nocookie.net/warframe/images/c/c7/CephalonOrdis_Portrait.png",
        "embeds": [{
            "title": titel,
            "description": beschreibung,
            "color": farbe,
            "fields": [
                {"name": "Operator", "value": f"**{PLAYER_NAME}**", "inline": True},
                {"name": "Live Hub", "value": f"[Dashboard öffnen]({DASHBOARD_URL})", "inline": True}
            ],
            "footer": {
                "text": "Warframe Co-Op Live Link • The Lost Primarchs"
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Discord-Webhook Fehler: {e}")

# 5. Quest-Zuordnung für Story-Fortschritt
QUEST_MAP = {
    "VorsPrize": ("Vors Preis", "Einmal erwacht"),
    "OnceAwake": ("Einmal erwacht", "Das Herz von Deimos"),
    "DeimosQuest": ("Das Herz von Deimos", "Das Archwing"),
    "ArchwingQuest": ("Das Archwing", "Natah"),
    "NatahQuest": ("Natah", "Der Zweite Traum"),
    "SecondDream": ("Der Zweite Traum", "Der Innere Krieg"),
    "WarWithin": ("Der Innere Krieg", "Ketten von Harrow"),
    "ChainsOfHarrow": ("Ketten von Harrow", "Apostesie-Prolog"),
    "Apostasy": ("Apostesie-Prolog", "Das Opfer"),
    "Sacrifice": ("Das Opfer", "Präludium zum Krieg"),
    "PreludeToWar": ("Präludium zum Krieg", "Der Neue Krieg"),
    "TheNewWar": ("Der Neue Krieg", "Engel des Zariman"),
    "ZarimanQuest": ("Engel des Zariman", "Flüstern in den Wänden"),
    "WhispersInTheWalls": ("Flüstern in den Wänden", "Warframe: 1999"),
    "Warframe1999": ("Warframe: 1999", "Story-Endstand erreicht 🎉")
}

# Status-Speicher gegen Spam
aktueller_ort = "Unbekannt"
offline_counter = 0

def update_status(location: str, activity: str, discord_info=None):
    global aktueller_ort
    timestamp_log = time.strftime("%H:%M:%S")
    jetzt_iso = datetime.now(timezone.utc).isoformat()
    
    # Supabase bekommt jeden Heartbeat zur Aktualisierung des 75s-Timers
    try:
        supabase.table("player_status").upsert({
            "player_name": PLAYER_NAME,
            "current_location": location,
            "last_activity": activity,
            "updated_at": jetzt_iso
        }, on_conflict="player_name").execute()
    except Exception as fehler:
        print(f"[{timestamp_log}] ⚠ Cloud-Sync fehlgeschlagen: {fehler}")

    # Discord NUR benachrichtigen, wenn sich der Ort wirklich geändert hat
    if location != aktueller_ort:
        print(f"[{timestamp_log}] 🚀 Status-Wechsel: {aktueller_ort} -> {location} | {activity}")
        aktueller_ort = location
        if discord_info:
            titel, beschreibung, farbe = discord_info
            sende_discord_meldung(titel, beschreibung, farbe)

def update_quest(aktuelle_quest: str, status: str, naechste_quest: str):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] 📜 Quest-Update -> {aktuelle_quest} ({status}) | Nächste: {naechste_quest}")
    try:
        supabase.table("campaign_progress").upsert({
            "player_name": PLAYER_NAME,
            "current_quest": aktuelle_quest,
            "quest_status": status,
            "next_quest": naechste_quest
        }, on_conflict="player_name").execute()

        sende_discord_meldung(
            titel="📜 Quest-Status aktualisiert!",
            beschreibung=f"**{PLAYER_NAME}** hat den Status von **{aktuelle_quest}** auf **{status}** gesetzt!\nNächste Mission: *{naechste_quest}*",
            farbe=0xe5b95c
        )
    except Exception as fehler:
        print(f"[{timestamp}] ⚠️ Quest-Sync fehlgeschlagen: {fehler}")

# Initialer Status
warframe_laeuft = ist_warframe_aktiv()
if warframe_laeuft:
    update_status("Orbiter", "Agent gestartet - lausche live...",
                  ("📡 Operator im Sternensystem eingeklinkt!", "Der Warframe-Sync-Agent wurde gestartet. Status: **Im Orbiter**.", 0x2ed573))
else:
    update_status("Offline", "Warframe nicht aktiv")
    print("ℹ️ Warframe läuft aktuell nicht. Status auf Offline gesetzt.")

# 6. Live-Log-Schleife
with open(log_pfad, "r", encoding="utf-8", errors="ignore") as datei:
    datei.seek(0, os.SEEK_END)
    letzter_heartbeat = time.time()
    
    try:
        while True:
            zeile = datei.readline()
            if zeile:
                t = zeile.strip()
                t_low = t.lower()

                # 1. Dojo betreten
                if "initiatedojovisit" in t_low or "dojohub" in t_low:
                    update_status("Clan-Dojo", "Im Dojo unterwegs",
                                  ("🏰 Dojo betreten", f"**{PLAYER_NAME}** ist jetzt im Clan-Dojo.", 0xe5b95c))

                # 2. Dojo Forschungskonsole
                elif "researchselection.swf" in t_low:
                    update_status("Clan-Dojo", "An der Forschungskonsole")

                # 3. Schmiede im Orbiter
                elif "diegeticfoundry.swf" in t_low:
                    update_status("Orbiter", "Schmiede geöffnet")

                # 4. Relikt-Konsole
                elif "diegeticartifactcards.swf" in t_low:
                    update_status("Orbiter", "Relikt-Konsole geöffnet")

                # 5. Inventar
                elif "inventorytest.swf" in t_low:
                    update_status("Orbiter", "Im Inventar")

                # 6. Syndikate
                elif "themedsyndicates.swf" in t_low or "syndicateslite.swf" in t_low:
                    update_status("Orbiter", "Syndikats-Status prüfen")

                # 7. Open Worlds & Hubs
                elif "cetus" in t_low or "hub.map" in t_low:
                    update_status("Cetus (Erde)", "Auf der Erde / Cetus",
                                  ("🌍 Cetus betreten", f"**{PLAYER_NAME}** ist in Cetus eingetroffen.", 0x00e5ff))
                elif "fortuna" in t_low:
                    update_status("Fortuna (Venus)", "Auf der Venus / Fortuna",
                                  ("❄️ Fortuna betreten", f"**{PLAYER_NAME}** ist in Fortuna eingetroffen.", 0x00e5ff))
                elif "necralisk" in t_low or "deimoshub" in t_low:
                    update_status("Necralisk (Deimos)", "Auf Deimos / Necralisk",
                                  ("💀 Necralisk betreten", f"**{PLAYER_NAME}** ist auf Deimos.", 0x00e5ff))

                # 8. Zurück im Schiff
                elif "playership" in t_low and "finished loading resources" in t_low:
                    update_status("Orbiter", "Im Raumschiff",
                                  ("🚀 Zurück im Schiff", f"**{PLAYER_NAME}** ist wieder im Orbiter.", 0x2ed573))

                # 9. Quest-Events mitschneiden
                elif "quest [info]:" in t_low:
                    for q_key, (aktuelle_quest, naechste_quest) in QUEST_MAP.items():
                        if q_key.lower() in t_low:
                            q_status = "Abgeschlossen" if "completed quest" in t_low else "Aktiv"
                            update_quest(aktuelle_quest, q_status, naechste_quest)

                # 10. Spiel regulär beendet
                elif "cmdquit" in t_low or "main menu -- shutdown" in t_low:
                    update_status("Offline", "Warframe beendet",
                                  ("💤 Operator abgemeldet", f"**{PLAYER_NAME}** hat Warframe beendet.", 0xff4757))

            else:
                # Heartbeat alle 20 Sekunden
                if time.time() - letzter_heartbeat > 20:
                    laeuft_jetzt = ist_warframe_aktiv()

                    if laeuft_jetzt:
                        offline_counter = 0
                        if aktueller_ort == "Offline":
                            update_status("Orbiter", "Warframe gestartet",
                                          ("📡 Operator im Sternensystem eingeklinkt!", f"**{PLAYER_NAME}** ist online.", 0x2ed573))
                        else:
                            # Stiller Heartbeat an Supabase ohne Discord-Ping
                            update_status(aktueller_ort, "Aktiv im Spiel")
                    else:
                        offline_counter += 1
                        # Erst nach 3 Fehlversuchen (ca. 60s) wirklich auf Offline setzen
                        if offline_counter >= 3 and aktueller_ort != "Offline":
                            update_status("Offline", "Warframe beendet",
                                          ("💤 Operator abgemeldet", f"**{PLAYER_NAME}** hat Warframe beendet.", 0xff4757))

                    letzter_heartbeat = time.time()
                time.sleep(0.3)

    except KeyboardInterrupt:
        print("\nAgent gestoppt.")
        update_status("Offline", "Agent beendet",
                      ("💤 Agent gestoppt", f"Der Sync-Agent für **{PLAYER_NAME}** wurde geschlossen.", 0xff4757))