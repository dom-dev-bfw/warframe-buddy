import os
from datetime import datetime, timezone
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SUPABASE_URL = "https://cvtdjitedrlfgzxkzjaj.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def send_discord_embed(embed):
    if not DISCORD_WEBHOOK_URL:
        print("Kein Discord Webhook hinterlegt.")
        return
    payload = {"embeds": [embed]}
    res = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    if res.status_code not in (200, 204):
        print(f"Fehler beim Senden: {res.status_code} - {res.text}")
    else:
        print("Discord Benachrichtigung erfolgreich gesendet!")

def post_monday_reset():
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
    if not SUPABASE_KEY:
        print("Kein Supabase Key vorhanden.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    try:
        url = f"{SUPABASE_URL}/rest/v1/weekly_checklist?is_done=eq.false&select=*"
        res = requests.get(url, headers=headers, timeout=10)
        open_tasks = res.json() if res.ok else []

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
            text += f"• **{t.get('player_name', 'Tenno')}**: `{t.get('task_id', '-')}`\n"

        embed = {
            "title": "⚠️ Deadline-Warnung: Wöchentlicher Reset naht!",
            "description": "Der Reset erfolgt in wenigen Stunden! Folgende Aufgaben sind noch offen:\n\n" + text,
            "color": 0xFF4757
        }
        send_discord_embed(embed)
    except Exception as e:
        print("Fehler beim Prüfen von Supabase:", e)

def check_arc_raiders_news():
    # Steam App ID für ARC Raiders: 1808500
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=1808500&count=1&maxlength=300&format=json"
    try:
        r = requests.get(url, timeout=10)
        if not r.ok:
            return
        
        data = r.json()
        news_items = data.get("appnews", {}).get("newsitems", [])
        if not news_items:
            return
        
        latest = news_items[0]
        title = latest.get("title")
        news_url = latest.get("url")
        contents = latest.get("contents", "")
        clean_contents = contents.replace("[b]", "**").replace("[/b]", "**").replace("[url]", "").replace("[/url]", "")

        embed = {
            "title": f"🚀 ARC Raiders News: {title}",
            "url": news_url,
            "description": clean_contents[:300] + ("..." if len(clean_contents) > 300 else ""),
            "color": 0xFF5722,
            "footer": {
                "text": "Embark Studios / Steam Newsfeed"
            }
        }
        send_discord_embed(embed)
    except Exception as e:
        print("Fehler beim Abrufen der ARC Raiders News:", e)

if __name__ == "__main__":
    weekday = datetime.now(timezone.utc).weekday()
    if weekday == 6:
        post_sunday_reminder()
    else:
        post_monday_reset()

    # News-Check aktivieren:
    check_arc_raiders_news()