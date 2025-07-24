import os
import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient

def get_database():
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URL)
    return client["clash_decks"]

def fetch_and_store_battles(player_tag="U2LYQJQVY"):
    url = f"https://royaleapi.com/player/{player_tag}/battles/csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Referer": f"https://royaleapi.com/player/{player_tag}/battles",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "fr-FR,fr;q=0.7",
        "X-Requested-With": "XMLHttpRequest",
        # Remplace le cookie par le tien si besoin, ou essaie sans
        "Cookie": "__royaleapi_session_v2=f042666c90364d2984f951a8112ad809; NB_SRVID=srv2086659299; cf_clearance=pd.uBDkQ5c8.4A2uEXOX9Ak9lO8LYlEssy_T26UjZag-1753309437-1.2.1.1-CCuu4wnJhYJmGlR.UvgmSSjAqgdZwvjVZEfUnr.pCn0qKBxevu1uuNFytRG7iXTCeisuWHtWeg4ftHkX.ij4Q4SN8EmGd.IhomFmD1OEwKn2WQZJX1h_ibJGVkZ7p8dquOazVrtOHpoFkJPpxyXSHTuH35BrtkXpX7SEjra1bhLv1d_Ry7lH4YKYarQhARsheL0WBLJTcn3zHUFbwoEZcOiZb5xs_19hSZqYx7DO.oE"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Erreur lors du téléchargement du CSV : {response.status_code}")
        print(response.text[:500])
        return

    csv_content = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(csv_content))

    cols_to_keep = [
        "team_0_clan_tag",
        "team_0_crowns",
        "replayTag",
        "opponent_0_crowns",
        "opponent_0_tag"
    ]
    cols_existantes = [c for c in cols_to_keep if c in df.columns]
    df_filtered = df[cols_existantes]

    # Connexion à MongoDB
    db = get_database()
    battles_collection = db["battles"]

    # Transformer les lignes en dictionnaires pour MongoDB
    records = df_filtered.to_dict(orient="records")

    # Insérer dans la collection battles (ajoute ou remplace selon besoin)
    if records:
        battles_collection.insert_many(records)
        print(f"✅ {len(records)} batailles insérées dans la collection 'battles'.")
    else:
        print("⚠️ Aucun enregistrement à insérer.")

if __name__ == "__main__":
    fetch_and_store_battles()
