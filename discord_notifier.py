import os
import requests
from supabase import create_client

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SUPABASE_URL = "https://cvtdjitedrlfgzxkzjaj.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def send_discord_embed(embed):
    if not DISCORD_WEBHOOK_URL:
        print("Kein Discord Webhook hinterlegt.")
        return
    payload = {"embeds": [embed]}
    res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if res.status_code not in (200, 204):
        print(f"Fehler beim Senden: {res.status_code} - {res.text}")
    else:
        print("Discord Benachrichtigung erfolgreich gesendet!")

def post_monday_reset():
    # 1. Duviri Circuit aus API holen
    frames = "Keine Daten verfügbar"
    try:
        r = requests.get("https://api.warframestat.us/pc/duviriCycle", timeout=10)
        if r.ok:
            data = r.json()
            choices = data.get("choices", [])
            extracted = []
            for c in choices:
                if isinstance(c, str):
                    extracted.append(c)
                elif isinstance(c, dict) and "choices" in c:
                    extracted.extend(c["choices"])
                elif isinstance(c, dict) and "name" in c:
                    extracted.append(c["name"])
            if extracted:
                frames = ", ".join(extracted)
    except Exception as e:
        print("Fehler beim Abrufen von Duviri:", e)

    embed = {
        "title": "⚡ Neuer Warframe Wochen-Reset!",
        "description": "Die neue Woche hat begonnen. Zeit für Beute, Tenno!",
        "color": 0x00E5FF,
        "fields": [
            {
                "name": "🌀 Duviri Circuit Rotation (Frames & Incarnons)",
                "value": f"**{frames}**",
                "inline": False
            },
            {
                "name": "📋 Wöchentliche Prioritäten",
                "value": (
                    "• **Archon-Jagd:** Archon-Shard sichern\n"
                    "• **Netracells / EDA:** 5/5 Läufe für Archon-Scherben\n"
                    "• **Palladino (Iron Wake):** 10 Riven-Scherben tauschen\n"
                    "• **1999:** Wochenkalender prüfen"
                ),
                "inline": False
            }
        ],
        "footer": {
            "text": "The Lost Primarchs Duo Sync"
        }
    }
    send_discord_embed(embed)

def post_sunday_reminder():
    try:
        sb = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = sb.table("weekly_checklist").select("*").eq("is_done", False).execute()
        open_tasks = res.data or []

        if not open_tasks:
            embed = {
                "title": "🎉 Wochen-Checkliste komplett!",
                "description": "Alle Duo-Pflichtaufgaben wurden erledigt. Starke Leistung!",
                "color": 0x2ED573
            }
            send_discord_embed(embed)
            return

        text = ""
        for t in open_tasks:
            text += f"• **{t['player_name']}**: `{t['task_id']}`\n"

        embed = {
            "title": "⚠️ Deadline-Warnung: Wöchentlicher Reset naht!",
            "description": "Der Reset erfolgt in wenigen Stunden! Folgende Aufgaben sind noch offen:\n\n" + text,
            "color": 0xFF4757
        }
        send_discord_embed(embed)
    except Exception as e:
        print("Fehler beim Prüfen von Supabase:", e)

if __name__ == "__main__":
    action_type = os.getenv("ACTION_TYPE", "monday")
    if action_type == "monday":
        post_monday_reset()
    elif action_type == "sunday":
        post_sunday_reminder()