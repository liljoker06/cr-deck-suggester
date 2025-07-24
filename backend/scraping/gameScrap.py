import os
import json
import time
import random
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Connexion à MongoDB
def get_database():
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URL)
    return client["clash_decks"]

# Crée le dossier "replays" si besoin
os.makedirs("replays", exist_ok=True)

# Headers HTTP
headers_template = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "fr-FR,fr;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": os.getenv("ROYALEAPI_COOKIE", "")
}

def fetch_replay_from_doc(doc):
    replay_tag = doc["replayTag"]
    team_tag = doc["team_0_tag"]
    opponent_tag = doc["opponent_0_tag"]
    team_crowns = doc.get("team_0_crowns", 0)
    opponent_crowns = doc.get("opponent_0_crowns", 0)

    url = (
        f"https://royaleapi.com/data/replay?"
        f"tag={replay_tag}&team_tags={team_tag}&opponent_tags={opponent_tag}"
        f"&team_crowns={team_crowns}&opponent_crowns={opponent_crowns}"
        f"&referrer_path=https://royaleapi.com/player/{team_tag}/battles"
    )

    headers = headers_template.copy()
    headers["Referer"] = f"https://royaleapi.com/player/{team_tag}/battles"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            path = f"replays/replay_{replay_tag}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON sauvegardé : {path}")
        except Exception as e:
            print(f"❌ Erreur parsing JSON pour {replay_tag} :", e)
    else:
        print(f"❌ Erreur HTTP {response.status_code} pour {replay_tag}")

if __name__ == "__main__":
    db = get_database()
    battles_collection = db["battles"]

    # On ne récupère que les replays non encore scrappés (ou tout si tu veux)
    battles = list(battles_collection.find({}, {
        "_id": 0,
        "replayTag": 1,
        "team_0_tag": 1,
        "opponent_0_tag": 1,
        "team_0_crowns": 1,
        "opponent_0_crowns": 1
    }))

    print(f"📦 {len(battles)} replays trouvés en base.")

    # Traitement par lot de 2
    for i in range(0, len(battles), 2):
        batch = battles[i:i+2]

        for doc in batch:
            replay_tag = doc.get("replayTag")
            if not replay_tag:
                continue

            path = f"replays/replay_{replay_tag}.json"
            if os.path.exists(path):
                print(f"🟡 Replay {replay_tag} déjà scrappé, on saute.")
                continue

            fetch_replay_from_doc(doc)

        delay = random.randint(60, 120)
        print(f"⏱️ Pause de {delay} secondes avant les 2 prochains replays...")
        time.sleep(delay)

    print("✅ Tous les replays ont été traités.")
