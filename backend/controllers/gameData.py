import os
import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient

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
        "Cookie": "__royaleapi_session_v2=f042666c90364d2984f951a8112ad809; NB_SRVID=srv2086659299; cf_clearance=pd.uBDkQ5c8.4A2uEXOX9Ak9lO8LYlEssy_T26UjZag-1753309437-1.2.1.1-CCuu4wnJhYJmGlR.UvgmSSjAqgdZwvjVZEfUnr.pCn0qKBxevu1uuNFytRG7iXTCeisuWHtWeg4ftHkX.ij4Q4SN8EmGd.IhomFmD1OEwKn2WQZJX1h_ibJGVkZ7p8dquOazVrtOHpoFkJPpxyXSHTuH35BrtkXpX7SEjra1bhLv1d_Ry7lH4YKYarQhARsheL0WBLJTcn3zHUFbwoEZcOiZb5xs_19hSZqYx7DO.oE"
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
    player_tags = get_all_player_tags()
    if not player_tags:
        print("Aucun player_tag trouvé dans la base de données.")
    else:
        for player_tag in player_tags:
            fetch_and_store_battles(player_tag)
