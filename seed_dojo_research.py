import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Vollständiger Katalog aller Warframe-Dojo-Forschungen nach Labor
DOJO_CATALOG = {
    "Tenno": [
        "Banshee", "Banshee Chassis", "Banshee Neuroptics", "Banshee Systems",
        "Nezha", "Nezha Chassis", "Nezha Neuroptics", "Nezha Systems",
        "Volt", "Volt Chassis", "Volt Neuroptics", "Volt Systems",
        "Wukong", "Wukong Chassis", "Wukong Neuroptics", "Wukong Systems",
        "Zephyr", "Zephyr Chassis", "Zephyr Neuroptics", "Zephyr Systems",
        "Yareli", "Yareli Chassis", "Yareli Neuroptics", "Yareli Systems",
        "Dagath", "Dagath Chassis", "Dagath Neuroptics", "Dagath Systems",
        "Itzal", "Itzal Harness", "Itzal Wings", "Itzal Systems",
        "Akstiletto", "Attica", "Castanas", "Daikyu", "Dual Kamas",
        "Dual Raza", "Gazal Machete", "Guandao", "Kavats Genetischer Code",
        "Komorebi", "Lacera", "Ninkondi", "Okina", "Pyrana", "Rapiere Destreza",
        "Shaku", "Sybaris", "Talons", "Tekko", "Tipedo", "Tonbo", "Venka",
        "Zhuge", "Dorlak", "Tenet Grigori", "Veldt"
    ],
    "Chem": [
        "Ignis", "Ignis Wraith", "Jat Kittag", "Marelok", "Ogris", "Buzlok",
        "Grattler", "Jat Kusar", "Twin Krohkur", "Krohkur", "Nukor", "Ack & Brunt",
        "Sobek", "Torid (Chem)", "Viper", "Dual Cleavers", "Brok Hammer Skin",
        "Vulkar", "Kraken", "Halikar", "Kesheg", "Twin Rogga", "Zarr",
        "Argonak", "Kuva Shildeg", "Detron", "Drakgoon", "Stug"
    ],
    "Energy": [
        "Amprex", "Arca Plasmor", "Arca Scisco", "Arca Titron", "Lenz", "Opticor",
        "Supra", "Lanka", "Fluctus", "Cyngas", "Dera", "Exergis", "Ferrox",
        "Glaxion", "Helios", "Helios Carapace", "Helios Cerebrum", "Helios Systems",
        "Kreska", "Lecta", "Obex", "Ocucor", "Plinx", "Prolva", "Provoke",
        "Quatz", "Secura Penta", "Serro", "Spectra", "Staticor", "Tetra", "Velocitus"
    ],
    "Bio": [
        "Hema", "Phage", "Synapse", "Torid", "Dual Toxocyst", "Mios", "Cerata",
        "Catabolyst", "Caustacyst", "Djinn", "Djinn Carapace", "Djinn Cerebrum", "Djinn Systems",
        "Embolist", "Gas City Pherliac", "Hirudo", "Iliac", "Mutalist Cernos",
        "Mutalist Quanta", "Pox", "Pupacyst", "Scoliac", "Sporothrix", "Tysis",
        "Zymos", "Bile Capsule"
    ],
    "Orokin": [
        "Bleeding Dragon Key", "Decaying Dragon Key", "Extinguished Dragon Key", "Hobbled Dragon Key",
        "Orokin Solar Rail", "Specter Regiment", "Cosmic Specter", "Force Specter", "Vapor Specter"
    ],
    "Ventkids": [
        "Bad Baby (K-Drive)", "Flatbelly (K-Drive)", "Needlenose (K-Drive)",
        "Runway (K-Drive)", "Step Child (K-Drive)", "Wingnut (K-Drive)"
    ]
}

def seed_full_catalog():
    records = []
    for lab, items in DOJO_CATALOG.items():
        for name in items:
            records.append({
                "lab": lab,
                "item_name": name,
                "status": "locked",
                "missing_resources": None
            })

    print(f"Übertrage {len(records)} Forschungen in 'dojo_research'...")

    # Batch-Upload in 40er-Schritten (unterstützt Upsert ohne Konflikte)
    for i in range(0, len(records), 40):
        batch = records[i:i+40]
        supabase.table("dojo_research").upsert(batch, on_conflict="item_name").execute()

    print("✅ Gesamter Forschungskatalog erfolgreich eingetragen!")

if __name__ == "__main__":
    seed_full_catalog()