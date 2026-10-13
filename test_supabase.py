from supabase import create_client, Client

# ==========================================
# KONFIGURATION & ZUGANGSDATEN
# ==========================================
SUPABASE_URL = "https://cvtdjitedrlfgzxkzjaj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2dGRqaXRlZHJsZmd6eGt6amFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA4NDk4NjYsImV4cCI6MjEwNjQyNTg2Nn0.i4VJ-7aLcoGCPiPUwQBwKzTQrccr6fFfY0fSSPFYyko"


# Trage hier den tatsächlichen Clan-Rang ein:
ECHTER_CLAN_RANG = 5  # <-- Passe diese Zahl an euren echten Rang an!
CLAN_NAME = "THELOSTPRIMARCHS"

print("========================================")
print("     WARFRAME BUDDY: SUPABASE TEST      ")
print("========================================")

try:
    # 1. Verbindung zur Supabase Cloud aufbauen
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Verbindung zur Supabase-Datenbank erfolgreich!")

    # 2. Den Clan-Rang in der Cloud aktualisieren (UPDATE)
    print(f"\nAktualisiere Rang fuer '{CLAN_NAME}' auf Rang {ECHTER_CLAN_RANG}...")
    supabase.table("dojo_info").update({
        "clan_rank": ECHTER_CLAN_RANG
    }).eq("clan_name", CLAN_NAME).execute()
    print("✓ Update erfolgreich an die Cloud gesendet!")

    # 3. Den aktuellen Stand frisch aus der Tabelle abfragen (SELECT)
    print("\nLese aktuelle Daten aus Supabase aus:")
    antwort = supabase.table("dojo_info").select("*").eq("clan_name", CLAN_NAME).execute()
    daten = antwort.data

    if daten:
        dojo = daten[0]
        print("----------------------------------------")
        print(f"🏰 Clan-Name:        {dojo.get('clan_name')}")
        print(f"🎖️  Aktueller Rang:   {dojo.get('clan_rank')}")
        print(f"🏷️  Clan-Stufe:       {dojo.get('clan_tier')}")
        print(f"✨ Level-Up bereit:  {'JA! 🎉' if dojo.get('level_up_ready') else 'Noch nicht'}")
        print(f"📝 Notiz:            {dojo.get('notes')}")
        print("----------------------------------------")
    else:
        print(f"Kein Eintrag fuer Clan '{CLAN_NAME}' gefunden.")

except Exception as fehler:
    print(f"\n❌ Fehler aufgetreten: {fehler}")

print("\n--- Testlauf beendet ---")