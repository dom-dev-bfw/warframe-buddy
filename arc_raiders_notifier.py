import os
import re
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def clean_steam_bbcode(text):
    if not text:
        return ""
    # HTML-Tags und BBCode entfernen
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\[\/?(b|i|u|url|img|list|\*)[^\]]*\]', '', clean)
    return clean.strip()

def check_arc_raiders_news():
    if not DISCORD_WEBHOOK_URL:
        print("Kein Discord Webhook hinterlegt.")
        return

    # Steam App ID für ARC Raiders: 1808500
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=1808500&count=1&maxlength=400&format=json"
    try:
        r = requests.get(url, timeout=10)
        if not r.ok:
            print(f"Steam API Fehler: {r.status_code}")
            return
        
        data = r.json()
        news_items = data.get("appnews", {}).get("newsitems", [])
        if not news_items:
            print("Keine News gefunden.")
            return

        latest = news_items[0]
        title = latest.get("title", "ARC Raiders Update")
        news_url = latest.get("url", "")
        raw_contents = latest.get("contents", "")
        clean_text = clean_steam_bbcode(raw_contents)

        if len(clean_text) > 280:
            clean_text = clean_text[:280] + "..."

        embed = {
            "title": f"🚀 ARC Raiders: {title}",
            "url": news_url,
            "description": clean_text if clean_text else "Keine Detailbeschreibung verfügbar.",
            "color": 0xFF5722,
            "footer": {
                "text": "Embark Studios / Steam Community"
            }
        }

        # Eigenes Bot-Branding für ARC Raiders
        payload = {
            "username": "ARC Raider HQ",
            "avatar_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1808500/header.jpg",
            "embeds": [embed]
        }

        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if res.status_code in (200, 204):
            print("ARC Raiders News erfolgreich gesendet!")
        else:
            print(f"Discord Fehler: {res.status_code} - {res.text}")

    except Exception as e:
        print("Fehler bei ARC Raiders:", e)

if __name__ == "__main__":
    check_arc_raiders_news()