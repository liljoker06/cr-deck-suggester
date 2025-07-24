import os
import time
import random
import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URL)
    return client["clash_decks"]

def fetch_and_store_battles_for_all_players(limit=2):
    db = get_database()
    players = db["players"].find({}, {"player_tag": 1}).limit(limit)

    for player in players:
        player_tag = player.get("player_tag")
        if player_tag:
            fetch_and_store_battles(player_tag)
            delay = random.uniform(30, 90)  # entre 30s et 90s
            print(f"Pause de {delay:.1f} secondes avant le prochain joueur...")
            time.sleep(delay)

def fetch_and_store_battles(player_tag: str):
    url = f"https://royaleapi.com/player/{player_tag}/battles/csv"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://royaleapi.com/player/{player_tag}/battles",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "fr-FR,fr;q=0.7",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": os.getenv("ROYALEAPI_COOKIE", "")
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Erreur pour {player_tag} : {response.status_code}")
        return

    csv_content = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(csv_content))

    cols_to_keep = [
        "team_0_clan_tag",
        "team_0_crowns",
        "replayTag",
        "opponent_0_crowns",
        "opponent_0_tag",
        "opponent_0_clan_tag",
        "team_0_tag"
    ]
    df_filtered = df[[c for c in cols_to_keep if c in df.columns]]

    if df_filtered.empty:
        print(f"Aucune donnée pour {player_tag}")
        return

    db = get_database()
    battles_collection = db["battles"]

    new_records = []
    for record in df_filtered.to_dict(orient="records"):
        if not battles_collection.find_one({"replayTag": record["replayTag"]}):
            new_records.append(record)

    if new_records:
        battles_collection.insert_many(new_records)
        print(f"{len(new_records)} nouvelles batailles insérées pour {player_tag}")
    else:
        print(f"Aucune nouvelle bataille à insérer pour {player_tag}")

if __name__ == "__main__":
    fetch_and_store_battles_for_all_players(limit=2)  # 🔁 2 joueurs max par exécution
