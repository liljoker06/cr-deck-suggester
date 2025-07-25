import os
import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient
from dotenv import load_dotenv
import time
import random

load_dotenv()
 
def get_database():
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URL)
    return client["clash_decks"]
 
def fetch_and_store_battles(player_tag: str):
    url = f"https://royaleapi.com/player/{player_tag}/battles/csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Referer": f"https://royaleapi.com/player/{player_tag}/battles",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "fr-FR,fr;q=0.7",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": os.getenv("ROYALEAPI_COOKIE", "")
    }
 
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Erreur lors du téléchargement du CSV pour {player_tag} : {response.status_code}")
        print(response.text[:500])
        return
 
    csv_content = response.content.decode('utf-8')
    # Vérification simple du format CSV
    first_line = csv_content.splitlines()[0] if csv_content else ''
    if not csv_content or ',' not in first_line:
        print(f"⚠️ Le contenu reçu pour {player_tag} n'est pas un CSV valide :")
        print(csv_content[:300])
        return
 
    try:
        df = pd.read_csv(StringIO(csv_content))
    except Exception as e:
        print(f"❌ Erreur pandas pour {player_tag} : {e}")
        print(csv_content[:300])
        return
 
    cols_to_keep = [
        "team_0_clan_tag",
        "team_0_tag",
        "team_0_crowns",
        "replayTag",
        "opponent_0_clan_tag",
        "opponent_0_crowns",
        "opponent_0_tag"
    ]
    cols_existantes = [c for c in cols_to_keep if c in df.columns]
    df_filtered = df[cols_existantes]
    for col in ["team_0_tag", "opponent_0_tag", "replayTag", "team_0_clan_tag", "opponent_0_clan_tag"]:
        if col in df_filtered.columns:
            df_filtered.loc[:, col] = df_filtered[col].astype(str).str.replace(r"^#", "", regex=True)
    db = get_database()
    battles_collection = db["battles"]
    records = df_filtered.to_dict(orient="records")
    if records:
        battles_collection.insert_many(records)
        print(f"✅ {len(records)} batailles insérées dans la collection 'battles' pour {player_tag}.")
    else:
        print(f"⚠️ Aucun enregistrement à insérer pour {player_tag}.")
 
def get_all_player_tags():
    db = get_database()
    players_collection = db["players"]
    players = players_collection.find({}, {"player_tag": 1, "_id": 0})
    return [p["player_tag"] for p in players if "player_tag" in p]
 
if __name__ == "__main__":
    while True:
        player_tags = get_all_player_tags()
        if not player_tags:
            print("Aucun player_tag trouvé dans la base de données.")
            break

        for i in range(0, len(player_tags), 2):
            batch = player_tags[i:i+2]

            for player_tag in batch:
                fetch_and_store_battles(player_tag)

            # Pause entre chaque batch de 2 joueurs
            delay = random.randint(60, 120)  # entre 1 et 2 minutes
            print(f"⏱️ Attente de {delay} secondes avant les 2 prochains joueurs...")
            time.sleep(delay)
        
        # Optionnel : pause entre les cycles complets
        print("✅ Tous les joueurs ont été traités. Nouvelle boucle dans 5 minutes...")
        time.sleep(300)  # Pause de 5 minutes